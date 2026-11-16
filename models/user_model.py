from mysql.connector import Error

from config.database import Database


class UserModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "users"

    def get_by_username(self, username):
        rows = self.db.fetch_all(
            f"""SELECT u.id_user, u.username, u.password_hash, u.role, u.nama,
                       u.id_mahasiswa, u.nidn, u.status, m.nim
                FROM {self.table_name} u
                LEFT JOIN mahasiswa m ON u.id_mahasiswa = m.id_mahasiswa
                WHERE u.username = %s""", (username,))
        return rows[0] if rows else None

    def username_ada(self, username):
        return self.get_by_username(username) is not None

    def nidn_ada(self, nidn):
        return bool(self.db.fetch_all(
            f"SELECT 1 FROM {self.table_name} WHERE nidn = %s", (nidn,)))

    def register(self, username, password_hash, role, nama,
                 nim=None, kelas=None, nidn=None):
        """Simpan akun baru dalam satu transaksi.

        Untuk mahasiswa: jika NIM sudah ada di tabel mahasiswa, akun ditautkan
        ke baris itu. Jika belum, baris mahasiswa baru dibuat otomatis.
        Return (True, None) bila sukses, (False, pesan_error) bila gagal.
        """
        conn = self.db.get_connection()
        if not conn:
            return False, f"Koneksi database gagal: {self.db.last_error}"
        try:
            cur = conn.cursor(dictionary=True)
            id_mahasiswa = None
            if role == "mahasiswa":
                cur.execute("SELECT id_mahasiswa FROM mahasiswa WHERE nim = %s", (nim,))
                baris = cur.fetchone()
                if baris:
                    id_mahasiswa = baris["id_mahasiswa"]
                    cur.execute("SELECT 1 FROM users WHERE id_mahasiswa = %s", (id_mahasiswa,))
                    if cur.fetchone():
                        conn.rollback()
                        return False, f"NIM {nim} sudah memiliki akun."
                else:
                    cur.execute("INSERT INTO mahasiswa (nim, nama, kelas) VALUES (%s, %s, %s)",
                                (nim, nama, kelas))
                    id_mahasiswa = cur.lastrowid
            cur.execute(
                f"""INSERT INTO {self.table_name}
                    (username, password_hash, role, nama, id_mahasiswa, nidn)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                (username, password_hash, role, nama, id_mahasiswa, nidn))
            conn.commit()
            return True, None
        except Error as e:
            conn.rollback()
            self.db.last_error = str(e)
            if e.errno == 1062:
                return False, "Username atau data unik lain sudah terdaftar."
            return False, f"Gagal menyimpan akun: {e}"
        finally:
            conn.close()
