from config.database import Database


class TugasModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "tugas"

    def get_all(self):
        query = f"""
            SELECT t.id_tugas, pr.nama_praktikum, pe.pertemuan_ke, t.nama_tugas, t.deadline
            FROM {self.table_name} t
            JOIN pertemuan pe ON t.id_pertemuan = pe.id_pertemuan
            JOIN praktikum pr ON pe.id_praktikum = pr.id_praktikum
            ORDER BY t.id_tugas
        """
        return self.db.fetch_all(query)

    def create(self, id_pertemuan, nama_tugas, deadline):
        query = f"INSERT INTO {self.table_name} (id_pertemuan, nama_tugas, deadline) VALUES (%s, %s, %s)"
        return self.db.execute(query, (id_pertemuan, nama_tugas, deadline))

    def update(self, id_tugas, id_pertemuan, nama_tugas, deadline):
        query = f"UPDATE {self.table_name} SET id_pertemuan=%s, nama_tugas=%s, deadline=%s WHERE id_tugas=%s"
        return self.db.execute(query, (id_pertemuan, nama_tugas, deadline, id_tugas))

    def delete(self, id_tugas):
        query = f"DELETE FROM {self.table_name} WHERE id_tugas=%s"
        return self.db.execute(query, (id_tugas,))
