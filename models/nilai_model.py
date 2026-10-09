from config.database import Database

# Bobot nilai akhir otomatis (dipakai hanya jika nilai_akhir dikosongkan).
# Ubah sesuai ketentuan asisten/dosen.
BOBOT_TUGAS = 0.4
BOBOT_LAPORAN = 0.4
BOBOT_KEHADIRAN = 0.2


class NilaiModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "nilai"

    def get_all(self):
        query = f"""
            SELECT n.id_nilai, m.nim, m.nama, pr.nama_praktikum,
                   n.nilai_tugas, n.nilai_laporan, n.nilai_kehadiran, n.nilai_akhir
            FROM {self.table_name} n
            JOIN mahasiswa m ON n.id_mahasiswa = m.id_mahasiswa
            JOIN praktikum pr ON n.id_praktikum = pr.id_praktikum
            ORDER BY n.id_nilai
        """
        return self.db.fetch_all(query)

    @staticmethod
    def hitung_nilai_akhir(nilai_tugas, nilai_laporan, nilai_kehadiran):
        if None in (nilai_tugas, nilai_laporan, nilai_kehadiran):
            return None
        return round(float(nilai_tugas) * BOBOT_TUGAS
                     + float(nilai_laporan) * BOBOT_LAPORAN
                     + float(nilai_kehadiran) * BOBOT_KEHADIRAN, 2)

    def create(self, id_mahasiswa, id_praktikum, nilai_tugas, nilai_laporan,
               nilai_kehadiran, nilai_akhir=None):
        if nilai_akhir is None:
            nilai_akhir = self.hitung_nilai_akhir(nilai_tugas, nilai_laporan, nilai_kehadiran)
        query = f"""INSERT INTO {self.table_name}
                    (id_mahasiswa, id_praktikum, nilai_tugas, nilai_laporan, nilai_kehadiran, nilai_akhir)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
        return self.db.execute(query, (id_mahasiswa, id_praktikum, nilai_tugas,
                                       nilai_laporan, nilai_kehadiran, nilai_akhir))

    def update(self, id_nilai, id_mahasiswa, id_praktikum, nilai_tugas, nilai_laporan,
               nilai_kehadiran, nilai_akhir=None):
        if nilai_akhir is None:
            nilai_akhir = self.hitung_nilai_akhir(nilai_tugas, nilai_laporan, nilai_kehadiran)
        query = f"""UPDATE {self.table_name}
                    SET id_mahasiswa=%s, id_praktikum=%s, nilai_tugas=%s,
                        nilai_laporan=%s, nilai_kehadiran=%s, nilai_akhir=%s
                    WHERE id_nilai=%s"""
        return self.db.execute(query, (id_mahasiswa, id_praktikum, nilai_tugas,
                                       nilai_laporan, nilai_kehadiran, nilai_akhir, id_nilai))

    def delete(self, id_nilai):
        query = f"DELETE FROM {self.table_name} WHERE id_nilai=%s"
        return self.db.execute(query, (id_nilai,))
