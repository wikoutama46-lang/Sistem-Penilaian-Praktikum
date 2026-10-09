from config.database import Database


class PraktikumModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "praktikum"

    def get_all(self):
        return self.db.fetch_all(f"SELECT * FROM {self.table_name} ORDER BY id_praktikum")

    def create(self, nama_praktikum, asisten_dosen):
        query = f"INSERT INTO {self.table_name} (nama_praktikum, asisten_dosen) VALUES (%s, %s)"
        return self.db.execute(query, (nama_praktikum, asisten_dosen))

    def update(self, id_praktikum, nama_praktikum, asisten_dosen):
        query = f"UPDATE {self.table_name} SET nama_praktikum=%s, asisten_dosen=%s WHERE id_praktikum=%s"
        return self.db.execute(query, (nama_praktikum, asisten_dosen, id_praktikum))

    def delete(self, id_praktikum):
        query = f"DELETE FROM {self.table_name} WHERE id_praktikum=%s"
        return self.db.execute(query, (id_praktikum,))
