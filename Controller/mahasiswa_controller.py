from models.mahasiswa_model import MahasiswaModel
from controllers.base_controller import (hasil, kosong, ke_int,
                                         cari_by_id, hasil_eksekusi)


class MahasiswaController:
    def __init__(self):
        self.model = MahasiswaModel()

    def _validasi(self, nim, nama, kelas):
        if kosong(nim) or kosong(nama) or kosong(kelas):
            return "NIM, nama, dan kelas wajib diisi."
        if len(str(nim).strip()) > 20:
            return "NIM maksimal 20 karakter."
        return None

    def tampil_semua(self):
        return hasil(True, "OK", self.model.get_all())

    def tampil_satu(self, id_mahasiswa):
        id_ = ke_int(id_mahasiswa)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        data = cari_by_id(self.model, "id_mahasiswa", id_)
        return hasil(True, "OK", data) if data else hasil(False, "Data tidak ditemukan.")

    def tambah(self, nim, nama, kelas):
        err = self._validasi(nim, nama, kelas)
        if err:
            return hasil(False, err)
        if any(m["nim"] == str(nim).strip() for m in self.model.get_all()):
            return hasil(False, f"NIM {nim} sudah terdaftar.")
        aff = self.model.create(str(nim).strip(), str(nama).strip(), str(kelas).strip())
        return hasil_eksekusi(self.model, aff, "Data mahasiswa berhasil ditambahkan.")

    def ubah(self, id_mahasiswa, nim, nama, kelas):
        id_ = ke_int(id_mahasiswa)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        err = self._validasi(nim, nama, kelas)
        if err:
            return hasil(False, err)
        if any(m["nim"] == str(nim).strip() and m["id_mahasiswa"] != id_
               for m in self.model.get_all()):
            return hasil(False, f"NIM {nim} sudah dipakai mahasiswa lain.")
        aff = self.model.update(id_, str(nim).strip(), str(nama).strip(), str(kelas).strip())
        return hasil_eksekusi(self.model, aff, "Data mahasiswa berhasil diperbarui.")

    def hapus(self, id_mahasiswa):
        id_ = ke_int(id_mahasiswa)
        if id_ is None:
            return hasil(False, "ID harus berupa angka.")
        aff = self.model.delete(id_)
        return hasil_eksekusi(self.model, aff, "Data mahasiswa berhasil dihapus.",
                              "Data tidak ditemukan.")
