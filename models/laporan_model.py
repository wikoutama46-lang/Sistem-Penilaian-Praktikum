from config.database import Database


class LaporanModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "laporan"

    def get_all(self):
        query = f"""
            SELECT l.id_laporan, m.nim, m.nama, pr.nama_praktikum, pe.pertemuan_ke,
                   l.judul_laporan, l.nilai_laporan
            FROM {self.table_name} l
            JOIN mahasiswa m ON l.id_mahasiswa = m.id_mahasiswa
            JOIN pertemuan pe ON l.id_pertemuan = pe.id_pertemuan
            JOIN praktikum pr ON pe.id_praktikum = pr.id_praktikum
            ORDER BY l.id_laporan
        """
        return self.db.fetch_all(query)

    def create(self, id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan):
        query = f"""INSERT INTO {self.table_name}
                    (id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan)
                    VALUES (%s, %s, %s, %s)"""
        return self.db.execute(query, (id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan))

    def update(self, id_laporan, id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan):
        query = f"""UPDATE {self.table_name}
                    SET id_mahasiswa=%s, id_pertemuan=%s, judul_laporan=%s, nilai_laporan=%s
                    WHERE id_laporan=%s"""
        return self.db.execute(query, (id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan, id_laporan))

    def delete(self, id_laporan):
        query = f"DELETE FROM {self.table_name} WHERE id_laporan=%s"
        return self.db.execute(query, (id_laporan,))
