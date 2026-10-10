from models.pertemuan_model import PertemuanModel
from controllers.base_controller import (hasil, kosong, ke_int, valid_tanggal,
                                         cari_by_id, hasil_eksekusi)


class PertemuanController:
    def __init__(self):
        self.model = PertemuanModel()

    def _validasi(self, id_praktikum, pertemuan_ke, tanggal):
        if ke_int(id_praktikum) is None:
            return "ID praktikum harus berupa angka."
        ke = ke_int(pertemuan_ke)
        if ke is None or ke < 1:
            return "Pertemuan ke- harus angka minimal 1."
        if kosong(tanggal) or not valid_tanggal(tanggal):
            return "Tanggal harus berformat YYYY-MM-DD."
        return None

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_pertemuan):
        id_ = ke_int(id_pertemuan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_pertemuan", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def tambah(self, id_praktikum, pertemuan_ke, tanggal):
        err = self._validasi(id_praktikum, pertemuan_ke, tanggal)
        if err:
            return hasil(False, err)
        aff = self.model.create(ke_int(id_praktikum), ke_int(pertemuan_ke), str(tanggal).strip())
        return hasil_eksekusi(self.model, aff, "Data pertemuan berhasil ditambahkan.")

    def ubah(self, id_pertemuan, id_praktikum, pertemuan_ke, tanggal):
        id_ = ke_int(id_pertemuan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err = self._validasi(id_praktikum, pertemuan_ke, tanggal)
        if err:
            return hasil(False, err)
        aff = self.model.update(id_, ke_int(id_praktikum), ke_int(pertemuan_ke),
                                str(tanggal).strip())
        return hasil_eksekusi(self.model, aff, "Data pertemuan berhasil diperbarui.")

    def hapus(self, id_pertemuan):
        id_ = ke_int(id_pertemuan)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data pertemuan berhasil dihapus.",
                              "Data tidak ditemukan.")
