from models.tugas_model import TugasModel
from controllers.base_controller import (hasil, kosong, ke_int, valid_tanggal,
                                         cari_by_id, hasil_eksekusi)


class TugasController:
    def __init__(self):
        self.model = TugasModel()

    def _validasi(self, id_pertemuan, nama_tugas, deadline):
        if ke_int(id_pertemuan) is None:
            return "ID pertemuan harus berupa angka."
        if kosong(nama_tugas):
            return "Nama tugas wajib diisi."
        if kosong(deadline) or not valid_tanggal(deadline, dengan_jam=True):
            return "Deadline harus berformat YYYY-MM-DD HH:MM:SS."
        return None

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_tugas):
        id_ = ke_int(id_tugas)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_tugas", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def tambah(self, id_pertemuan, nama_tugas, deadline):
        err = self._validasi(id_pertemuan, nama_tugas, deadline)
        if err:
            return hasil(False, err)
        aff = self.model.create(ke_int(id_pertemuan), str(nama_tugas).strip(),
                                str(deadline).strip())
        return hasil_eksekusi(self.model, aff, "Data tugas berhasil ditambahkan.")

    def ubah(self, id_tugas, id_pertemuan, nama_tugas, deadline):
        id_ = ke_int(id_tugas)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err = self._validasi(id_pertemuan, nama_tugas, deadline)
        if err:
            return hasil(False, err)
        aff = self.model.update(id_, ke_int(id_pertemuan), str(nama_tugas).strip(),
                                str(deadline).strip())
        return hasil_eksekusi(self.model, aff, "Data tugas berhasil diperbarui.")

    def hapus(self, id_tugas):
        id_ = ke_int(id_tugas)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data tugas berhasil dihapus.",
                              "Data tidak ditemukan.")
