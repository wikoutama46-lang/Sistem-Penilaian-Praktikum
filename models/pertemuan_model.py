from config.database import Database


class PertemuanModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "pertemuan"

    def get_all(self):
        query = f"""
            SELECT pe.id_pertemuan, pr.nama_praktikum, pe.pertemuan_ke, pe.tanggal
            FROM {self.table_name} pe
            JOIN praktikum pr ON pe.id_praktikum = pr.id_praktikum
            ORDER BY pe.id_pertemuan
        """
        return self.db.fetch_all(query)

    def create(self, id_praktikum, pertemuan_ke, tanggal):
        query = f"INSERT INTO {self.table_name} (id_praktikum, pertemuan_ke, tanggal) VALUES (%s, %s, %s)"
        return self.db.execute(query, (id_praktikum, pertemuan_ke, tanggal))

    def update(self, id_pertemuan, id_praktikum, pertemuan_ke, tanggal):
        query = f"UPDATE {self.table_name} SET id_praktikum=%s, pertemuan_ke=%s, tanggal=%s WHERE id_pertemuan=%s"
        return self.db.execute(query, (id_praktikum, pertemuan_ke, tanggal, id_pertemuan))

    def delete(self, id_pertemuan):
        query = f"DELETE FROM {self.table_name} WHERE id_pertemuan=%s"
        return self.db.execute(query, (id_pertemuan,))
