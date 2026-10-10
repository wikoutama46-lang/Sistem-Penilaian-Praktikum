from models.laporan_model import LaporanModel
from controllers.base_controller import (hasil, kosong, ke_int, ke_float,
                                         cari_by_id, hasil_eksekusi)


class LaporanController:
    def __init__(self):
        self.model = LaporanModel()

    def _validasi(self, id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan):
        """Return (error, nilai_laporan_terkonversi). Nilai boleh kosong (belum dinilai)."""
        if ke_int(id_mahasiswa) is None or ke_int(id_pertemuan) is None:
            return "ID mahasiswa dan ID pertemuan harus berupa angka.", None
        if kosong(judul_laporan):
            return "Judul laporan wajib diisi.", None
        if kosong(nilai_laporan):
            return None, None
        nilai = ke_float(nilai_laporan)
        if nilai is None or not 0 <= nilai <= 100:
            return "Nilai laporan harus angka 0-100.", None
        return None, nilai

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_laporan):
        id_ = ke_int(id_laporan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_laporan", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def tambah(self, id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan=None):
        err, nilai = self._validasi(id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan)
        if err:
            return hasil(False, err)
        aff = self.model.create(ke_int(id_mahasiswa), ke_int(id_pertemuan),
                                str(judul_laporan).strip(), nilai)
        return hasil_eksekusi(self.model, aff, "Data laporan berhasil ditambahkan.")

    def ubah(self, id_laporan, id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan=None):
        id_ = ke_int(id_laporan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err, nilai = self._validasi(id_mahasiswa, id_pertemuan, judul_laporan, nilai_laporan)
        if err:
            return hasil(False, err)
        aff = self.model.update(id_, ke_int(id_mahasiswa), ke_int(id_pertemuan),
                                str(judul_laporan).strip(), nilai)
        return hasil_eksekusi(self.model, aff, "Data laporan berhasil diperbarui.")

    def hapus(self, id_laporan):
        id_ = ke_int(id_laporan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data laporan berhasil dihapus.",
                              "Data tidak ditemukan.")
