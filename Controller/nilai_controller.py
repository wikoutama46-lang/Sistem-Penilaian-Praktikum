from models.nilai_model import NilaiModel
from controllers.base_controller import (hasil, kosong, ke_int, ke_float,
                                         cari_by_id, hasil_eksekusi)


class NilaiController:
    def __init__(self):
        self.model = NilaiModel()

    @staticmethod
    def _skor(nilai, label, wajib=True):
        """Return (error, float). Skor harus 0-100."""
        if kosong(nilai):
            return (f"{label} wajib diisi.", None) if wajib else (None, None)
        angka = ke_float(nilai)
        if angka is None or not 0 <= angka <= 100:
            return f"{label} harus angka 0-100.", None
        return None, angka

    def _validasi(self, id_mahasiswa, id_praktikum, tugas, laporan, kehadiran, akhir):
        if ke_int(id_mahasiswa) is None or ke_int(id_praktikum) is None:
            return "ID mahasiswa dan ID praktikum harus berupa angka.", None
        hasil_skor = []
        for nilai, label, wajib in [(tugas, "Nilai tugas", True),
                                    (laporan, "Nilai laporan", True),
                                    (kehadiran, "Nilai kehadiran", True),
                                    (akhir, "Nilai akhir", False)]:
            err, angka = self._skor(nilai, label, wajib)
            if err:
                return err, None
            hasil_skor.append(angka)
        return None, hasil_skor   # [tugas, laporan, kehadiran, akhir(None=otomatis)]

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_nilai):
        id_ = ke_int(id_nilai)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_nilai", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def hitung_nilai_akhir(self, nilai_tugas, nilai_laporan, nilai_kehadiran):
        """Pratinjau nilai akhir otomatis tanpa menyimpan ke database."""
        err, skor = self._validasi(1, 1, nilai_tugas, nilai_laporan, nilai_kehadiran, None)
        if err:
            return hasil(False, err)
        return hasil(True, "OK", self.model.hitung_nilai_akhir(*skor[:3]))

    def tambah(self, id_mahasiswa, id_praktikum, nilai_tugas, nilai_laporan,
               nilai_kehadiran, nilai_akhir=None):
        err, skor = self._validasi(id_mahasiswa, id_praktikum, nilai_tugas,
                                   nilai_laporan, nilai_kehadiran, nilai_akhir)
        if err:
            return hasil(False, err)
        aff = self.model.create(ke_int(id_mahasiswa), ke_int(id_praktikum), *skor)
        return hasil_eksekusi(self.model, aff, "Data nilai berhasil ditambahkan.")

    def ubah(self, id_nilai, id_mahasiswa, id_praktikum, nilai_tugas, nilai_laporan,
             nilai_kehadiran, nilai_akhir=None):
        id_ = ke_int(id_nilai)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err, skor = self._validasi(id_mahasiswa, id_praktikum, nilai_tugas,
                                   nilai_laporan, nilai_kehadiran, nilai_akhir)
        if err:
            return hasil(False, err)
        aff = self.model.update(id_, ke_int(id_mahasiswa), ke_int(id_praktikum), *skor)
        return hasil_eksekusi(self.model, aff, "Data nilai berhasil diperbarui.")

    def hapus(self, id_nilai):
        id_ = ke_int(id_nilai)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data nilai berhasil dihapus.",
                              "Data tidak ditemukan.")
