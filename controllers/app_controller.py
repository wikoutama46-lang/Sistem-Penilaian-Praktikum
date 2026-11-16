"""Controller utama GUI: menyambungkan semua View ke Controller modul.

Alur: View (tombol) -> AplikasiController -> Controller modul -> Model -> MySQL.
View tetap pasif. Semua keputusan (hak akses, validasi, pesan) ada di Controller.
"""
from controllers.auth_controller import AuthController
from controllers.hak_akses import boleh as role_boleh, modul_boleh_lihat, MODUL_MILIK_SENDIRI
from controllers.laporan_controller import LaporanController
from controllers.mahasiswa_controller import MahasiswaController
from controllers.nilai_controller import NilaiController
from controllers.pertemuan_controller import PertemuanController
from controllers.praktikum_controller import PraktikumController
from controllers.tugas_controller import TugasController
from views.modul import URUTAN

PERAN_LABEL = {"asdos": "Asisten Dosen", "dosen": "Dosen", "mahasiswa": "Mahasiswa"}
PESAN_DILARANG = "Peran Anda tidak memiliki izin untuk aksi ini."


class AplikasiController:
    def __init__(self, app):
        self.app = app
        self.auth = AuthController()
        self.modul = {
            "mahasiswa": MahasiswaController(),
            "praktikum": PraktikumController(),
            "pertemuan": PertemuanController(),
            "tugas": TugasController(),
            "laporan": LaporanController(),
            "nilai": NilaiController(),
        }
        self.pengguna = None          # dict akun yang sedang login
        self._pasang()

    # ---------- pemasangan perintah ke View ----------
    def _pasang(self):
        a = self.app
        a.login.btn_masuk.configure(command=self.masuk)
        a.register.btn_daftar.configure(command=self.daftar)
        a.form.btn_simpan.configure(command=self.simpan)
        a.form.btn_update.configure(command=self.perbarui)
        a.form.btn_hapus.configure(command=self.hapus_dari_form)
        a.daftar.btn_hapus.configure(command=self.hapus_dari_daftar)
        a.on_modul_berubah = self.muat_daftar
        a.izin = self.boleh
        a.on_keluar = self.keluar
        a.form.setelah_bangun = self._sesuaikan_form

    # ---------- hak akses ----------
    @property
    def role(self):
        return self.pengguna["role"] if self.pengguna else None

    def boleh(self, aksi, kunci):
        return bool(self.pengguna) and role_boleh(self.role, kunci, aksi)

    def _tolak(self, view):
        view.tampilkan_pesan(PESAN_DILARANG, error=True)

    # ---------- autentikasi ----------
    def daftar(self):
        res = self.auth.daftar(self.app.register.ambil_input())
        self.app.register.tampilkan_pesan(res["pesan"], error=not res["sukses"])
        if res["sukses"]:
            self.app.register.kosongkan_form()
            self.app.tampilkan("login")

    def masuk(self):
        isi = self.app.login.ambil_input()
        res = self.auth.masuk(isi["username"], isi["password"])
        if not res["sukses"]:
            self.app.login.tampilkan_pesan(res["pesan"], error=True)
            return
        self.pengguna = res["data"]
        self.app.pengguna = self.pengguna
        self.app.login.kosongkan_form()
        self._terapkan_akses()
        self.app.dashboard.set_pengguna(
            f'{self.pengguna["nama"]} ({PERAN_LABEL[self.role]})')
        self._segarkan_dashboard()
        self.app.tampilkan("dashboard")

    def keluar(self):
        """Dipanggil View saat tombol Keluar ditekan: bersihkan sesi dan data di layar."""
        self.pengguna = None
        self.app.pengguna = None
        self.app.daftar.tampilkan_data([])
        self.app.form.kosongkan_form()

    def _terapkan_akses(self):
        a = self.app
        lihat = modul_boleh_lihat(self.role, URUTAN)
        tambah = {k for k in lihat if self.boleh("tambah", k)}
        a.dashboard.atur_akses(lihat, tambah)
        a.form.batasi_modul(lihat)
        a.daftar.batasi_modul(lihat)
        if lihat:
            a.modul_aktif = lihat[0]
            a.form.atur_modul(a.modul_aktif)
            a.daftar.atur_modul(a.modul_aktif)

    # ---------- data ----------
    def _ambil_data(self, kunci):
        """Data modul untuk pengguna saat ini. Mahasiswa hanya melihat miliknya."""
        if not self.boleh("lihat", kunci):
            return []
        baris = self.modul[kunci].tampil_semua()["data"] or []
        if self.role == "mahasiswa" and kunci in MODUL_MILIK_SENDIRI:
            nim = str(self.pengguna.get("nim") or "")
            baris = [b for b in baris if nim and str(b.get("nim")) == nim]
        return baris

    def muat_daftar(self, kunci):
        d = self.app.daftar
        d.tampilkan_data(self._ambil_data(kunci))
        for aksi, tombol in (("tambah", d.btn_tambah), ("ubah", d.btn_ubah),
                             ("hapus", d.btn_hapus)):
            tombol.configure(state="normal" if self.boleh(aksi, kunci) else "disabled")

    def _segarkan_dashboard(self):
        self.app.dashboard.tampilkan_ringkasan(
            {k: len(self._ambil_data(k)) for k in URUTAN})

    # ---------- form ----------
    def _sesuaikan_form(self, form):
        """Mahasiswa mengumpulkan laporan atas namanya sendiri dan tidak mengisi nilai."""
        if self.role == "mahasiswa" and form.modul == "laporan":
            form.kunci_field("id_mahasiswa", self.pengguna.get("id_mahasiswa") or "")
            form.kunci_field("nilai_laporan", "")

    def _input_aman(self, kunci, data):
        """Paksa data sesuai hak akses (berlaku walau tampilan diubah-ubah)."""
        if self.role == "mahasiswa" and kunci == "laporan":
            data["id_mahasiswa"] = str(self.pengguna.get("id_mahasiswa") or "")
            data["nilai_laporan"] = ""
        return data

    def _selesai_aksi(self, view, res, kosongkan=False):
        view.tampilkan_pesan(res["pesan"], error=not res["sukses"])
        if res["sukses"]:
            if kosongkan:
                view.kosongkan_form()
            self._segarkan_dashboard()
        return res["sukses"]

    def simpan(self):
        f = self.app.form
        kunci = f.modul
        if not self.boleh("tambah", kunci):
            return self._tolak(f)
        if kunci == "laporan" and self.role == "mahasiswa" \
                and not self.pengguna.get("id_mahasiswa"):
            return f.tampilkan_pesan("Akun Anda belum terhubung ke data mahasiswa.", error=True)
        res = self.modul[kunci].tambah(**self._input_aman(kunci, f.ambil_input()))
        self._selesai_aksi(f, res, kosongkan=True)

    def perbarui(self):
        f = self.app.form
        kunci = f.modul
        if not self.boleh("ubah", kunci):
            return self._tolak(f)
        id_ = f.id_terpilih()
        if id_ is None:
            return f.tampilkan_pesan("Pilih data dari Daftar lalu tekan Ubah.", error=True)
        res = self.modul[kunci].ubah(id_, **self._input_aman(kunci, f.ambil_input()))
        self._selesai_aksi(f, res)

    def hapus_dari_form(self):
        f = self.app.form
        kunci = f.modul
        if not self.boleh("hapus", kunci):
            return self._tolak(f)
        id_ = f.id_terpilih()
        if id_ is None or not f.konfirmasi_hapus():
            return
        res = self.modul[kunci].hapus(id_)
        if self._selesai_aksi(f, res):
            self.app.buka_daftar(kunci)

    def hapus_dari_daftar(self):
        d = self.app.daftar
        kunci = d.modul
        if not self.boleh("hapus", kunci):
            return self._tolak(d)
        id_ = d.id_terpilih()
        if id_ is None:
            return d.tampilkan_pesan("Pilih data pada tabel terlebih dahulu.", error=True)
        if not d.konfirmasi_hapus():
            return
        res = self.modul[kunci].hapus(id_)
        if self._selesai_aksi(d, res):
            self.muat_daftar(kunci)
