"""Jendela utama GUI: menyusun halaman Login, Dashboard, Form, dan Daftar.

View ini belum terhubung ke Controller. Semua tombol aksi data (Simpan, Perbarui, Hapus)
hanya memberi pesan "belum terhubung". Nanti Controller cukup memasang perintah baru:

    app.form.btn_simpan.configure(command=...)
    app.login.btn_masuk.configure(command=...)
    app.on_modul_berubah = lambda kunci: app.daftar.tampilkan_data(...)
"""
import customtkinter as ctk

from views import tema as t
from views.dashboard_view import DashboardView
from views.daftar_view import DaftarView
from views.form_view import FormView
from views.login_view import LoginView
from views.modul import MODUL, URUTAN


class AplikasiView(ctk.CTk):
    def __init__(self):
        super().__init__()
        t.terapkan_tema()
        self.title(t.JUDUL_JENDELA)
        self.geometry("850x500")
        self.minsize(850, 500)
        self.configure(fg_color=t.LATAR)
        t.gaya_tabel()

        self.modul_aktif = URUTAN[0]
        self.on_modul_berubah = None   # diisi Controller: fungsi(kunci_modul) untuk memuat data

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.navbar = self._buat_navbar()
        self.login = LoginView(self)
        self.dashboard = DashboardView(self, on_daftar=self.buka_daftar, on_tambah=self.buka_form)
        self.form = FormView(self, on_ganti_modul=self._modul_diganti_form,
                             on_lihat_daftar=lambda: self.buka_daftar(self.form.modul))
        self.daftar = DaftarView(self, on_ganti_modul=self._modul_diganti_daftar)
        self._halaman = {"login": self.login, "dashboard": self.dashboard,
                         "form": self.form, "daftar": self.daftar}

        self._pasang_perintah_awal()
        self.tampilkan("login")

    # ---------- susunan ----------
    def _buat_navbar(self):
        bar = ctk.CTkFrame(self, fg_color=t.NAVY, corner_radius=0, height=48)
        bar.grid_columnconfigure(0, weight=1)
        t.judul(bar, t.JUDUL_JENDELA, warna=t.PUTIH).grid(
            row=0, column=0, padx=20, pady=10, sticky="w")
        menu = [("Dashboard", lambda: self.tampilkan("dashboard")),
                ("Form", lambda: self.buka_form(self.modul_aktif)),
                ("Daftar", lambda: self.buka_daftar(self.modul_aktif)),
                ("Keluar", self.keluar)]
        for i, (label, aksi) in enumerate(menu, start=1):
            t.tombol(bar, label, "navbar", width=90, command=aksi).grid(
                row=0, column=i, padx=(0, 6 if i < len(menu) else 14))
        return bar

    def tampilkan(self, nama):
        for halaman in self._halaman.values():
            halaman.grid_remove()
        if nama == "login":
            self.navbar.grid_remove()
        else:
            self.navbar.grid(row=0, column=0, sticky="ew")
        self._halaman[nama].grid(row=1, column=0, sticky="nsew")
        if nama == "login":
            self.login.fokus()

    # ---------- navigasi (hanya urusan tampilan) ----------
    def buka_daftar(self, kunci=None):
        self.modul_aktif = kunci or self.modul_aktif
        self.daftar.atur_modul(self.modul_aktif)
        self._muat(self.modul_aktif)
        self.tampilkan("daftar")

    def buka_form(self, kunci=None, data=None):
        """data=None -> mode tambah; data=dict baris -> mode ubah."""
        self.modul_aktif = kunci or self.modul_aktif
        self.form.atur_modul(self.modul_aktif, data)
        self.tampilkan("form")

    def keluar(self):
        self.login.kosongkan_form()
        self.tampilkan("login")

    def _muat(self, kunci):
        if self.on_modul_berubah:
            self.on_modul_berubah(kunci)

    def _modul_diganti_form(self, kunci):
        self.modul_aktif = kunci

    def _modul_diganti_daftar(self, kunci):
        self.modul_aktif = kunci
        self._muat(kunci)

    # ---------- perintah sementara (diganti Controller nanti) ----------
    def _pasang_perintah_awal(self):
        self.login.btn_masuk.configure(command=self._masuk_sementara)
        self.form.btn_simpan.configure(command=lambda: self._simpan_sementara("Simpan"))
        self.form.btn_update.configure(command=lambda: self._simpan_sementara("Perbarui"))
        self.form.btn_hapus.configure(command=lambda: self._hapus_sementara(self.form))
        self.daftar.btn_tambah.configure(command=lambda: self.buka_form(self.modul_aktif))
        self.daftar.btn_ubah.configure(command=self._ubah_dari_daftar)
        self.daftar.btn_hapus.configure(command=self._hapus_dari_daftar)
        self.daftar.btn_muat.configure(command=lambda: self._muat(self.modul_aktif))

    def _masuk_sementara(self):
        isi = self.login.ambil_input()
        if not isi["username"] or not isi["password"]:
            self.login.tampilkan_pesan("Username dan password wajib diisi.", error=True)
            return
        self.dashboard.set_pengguna(isi["username"])
        self.login.kosongkan_form()
        self.tampilkan("dashboard")

    def _simpan_sementara(self, aksi):
        kosong = self.form.field_wajib_kosong()
        if kosong:
            self.form.tampilkan_pesan("Field wajib diisi: " + ", ".join(kosong) + ".", error=True)
            return
        self._belum_terhubung(self.form, aksi)

    def _hapus_sementara(self, view):
        if view.konfirmasi_hapus():
            self._belum_terhubung(view, "Hapus")

    def _ubah_dari_daftar(self):
        data = self.daftar.data_terpilih()
        if data is None:
            self.daftar.tampilkan_pesan("Pilih data pada tabel terlebih dahulu.", error=True)
            return
        self.buka_form(self.modul_aktif, data)

    def _hapus_dari_daftar(self):
        if self.daftar.data_terpilih() is None:
            self.daftar.tampilkan_pesan("Pilih data pada tabel terlebih dahulu.", error=True)
            return
        self._hapus_sementara(self.daftar)

    @staticmethod
    def _belum_terhubung(view, aksi):
        view.tampilkan_pesan(f"Aksi '{aksi}' belum terhubung ke Controller.")