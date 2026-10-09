from config.database import Database


class MahasiswaModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "mahasiswa"

    def get_all(self):
        return self.db.fetch_all(f"SELECT * FROM {self.table_name} ORDER BY id_mahasiswa")

    def create(self, nim, nama, kelas):
        query = f"INSERT INTO {self.table_name} (nim, nama, kelas) VALUES (%s, %s, %s)"
        return self.db.execute(query, (nim, nama, kelas))

    def update(self, id_mahasiswa, nim, nama, kelas):
        query = f"UPDATE {self.table_name} SET nim=%s, nama=%s, kelas=%s WHERE id_mahasiswa=%s"
        return self.db.execute(query, (nim, nama, kelas, id_mahasiswa))

    def delete(self, id_mahasiswa):
        query = f"DELETE FROM {self.table_name} WHERE id_mahasiswa=%s"
        return self.db.execute(query, (id_mahasiswa,))
