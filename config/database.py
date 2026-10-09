import os
import mysql.connector
from mysql.connector import Error

SQL_FILE = os.path.join(os.path.dirname(__file__), "..", "database", "database.sql")


class Database:
    """Jembatan Python <-> MySQL Laragon.

    Jika database belum ada di Laragon, otomatis dibuat dan diisi dari
    database/database.sql saat pertama kali terkoneksi.
    """

    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.db_name = "sistem_penilaian_praktikum"
        self.username = "root"
        self.password = ""          # default Laragon: kosong
        self.conn = None
        self.last_error = None

    def _connect(self, dengan_database=True):
        params = dict(host=self.host, port=self.port,
                      user=self.username, password=self.password)
        if dengan_database:
            params["database"] = self.db_name
        return mysql.connector.connect(**params)

    def setup_database(self):
        """Buat database + tabel + data awal dari database.sql."""
        try:
            conn = self._connect(dengan_database=False)
            cursor = conn.cursor()
            with open(SQL_FILE, encoding="utf-8") as f:
                statements = [s.strip() for s in f.read().split(";") if s.strip()]
            for stmt in statements:
                cursor.execute(stmt)
            conn.commit()
            cursor.close()
            conn.close()
            print("Database & tabel berhasil dibuat di Laragon MySQL.")
            return True
        except (Error, OSError) as e:
            self.last_error = str(e)
            print(f"Setup database gagal: {e}")
            return False

    def get_connection(self):
        try:
            self.conn = self._connect()
        except Error as e:
            if e.errno == 1049 and self.setup_database():   # Unknown database
                try:
                    self.conn = self._connect()
                except Error as e2:
                    self.last_error = str(e2)
                    print(f"Koneksi gagal: {e2}")
                    return None
            else:
                self.last_error = str(e)
                print(f"Koneksi gagal: {e}")
                return None
        return self.conn if self.conn.is_connected() else None

    def fetch_all(self, query, params=None):
        """SELECT -> list of dict. Kosong jika gagal."""
        conn = self.get_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            self.last_error = str(e)
            print(f"Query gagal: {e}")
            return []
        finally:
            conn.close()

    def execute(self, query, params=None):
        """INSERT/UPDATE/DELETE. Return jumlah baris terpengaruh, None jika error."""
        conn = self.get_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected
        except Error as e:
            conn.rollback()
            self.last_error = str(e)
            print(f"Query gagal: {e}")
            return None
        finally:
            conn.close()
