from models.praktikum_model import PraktikumModel
from controllers.base_controller import (hasil, kosong, ke_int,
                                         cari_by_id, hasil_eksekusi)


class PraktikumController:
    def __init__(self):
        self.model = PraktikumModel()

    def _validasi(self, nama_praktikum, asisten_dosen):
        if kosong(nama_praktikum) or kosong(asisten_dosen):
            return "Nama praktikum dan asisten/dosen wajib diisi."
        return None

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_praktikum):
        id_ = ke_int(id_praktikum)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_praktikum", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def tambah(self, nama_praktikum, asisten_dosen):
        err = self._validasi(nama_praktikum, asisten_dosen)
        if err:
            return hasil(False, err)
        aff = self.model.create(str(nama_praktikum).strip(), str(asisten_dosen).strip())
        return hasil_eksekusi(self.model, aff, "Data praktikum berhasil ditambahkan.")

    def ubah(self, id_praktikum, nama_praktikum, asisten_dosen):
        id_ = ke_int(id_praktikum)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err = self._validasi(nama_praktikum, asisten_dosen)
        if err:
            return hasil(False, err)
        aff = self.model.update(id_, str(nama_praktikum).strip(), str(asisten_dosen).strip())
        return hasil_eksekusi(self.model, aff, "Data praktikum berhasil diperbarui.")

    def hapus(self, id_praktikum):
        id_ = ke_int(id_praktikum)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data praktikum berhasil dihapus.",
                              "Data tidak ditemukan.")
