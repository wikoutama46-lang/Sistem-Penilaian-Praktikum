"""Halaman Dashboard (GUI): ringkasan jumlah data tiap modul dan pintasan ke Daftar/Form."""
import customtkinter as ctk

from views import tema as t
from views.modul import MODUL, URUTAN

KOLOM_KARTU = 3


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_daftar=None, on_tambah=None):
        """on_daftar(kunci_modul) dan on_tambah(kunci_modul) dipasang oleh jendela utama."""
        super().__init__(master, fg_color=t.LATAR)
        self.grid_columnconfigure(0, weight=1)

        # Judul + sapaan
        kepala = t.panel(self)
        kepala.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        t.judul(kepala, "Dashboard").pack(anchor="w", padx=15, pady=(12, 0))
        self.lbl_sapaan = t.teks(kepala, "Selamat datang. Pilih modul untuk mengelola data.",
                                 sekunder=True)
        self.lbl_sapaan.pack(anchor="w", padx=15, pady=(0, 12))

        # Kartu ringkasan per modul
        area = ctk.CTkFrame(self, fg_color="transparent")
        area.grid(row=1, column=0, padx=15, pady=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        for k in range(KOLOM_KARTU):
            area.grid_columnconfigure(k, weight=1, uniform="kartu")

        self.lbl_jumlah = {}
        for i, kunci in enumerate(URUTAN):
            kartu = t.panel(area)
            kartu.grid(row=i // KOLOM_KARTU, column=i % KOLOM_KARTU,
                       padx=5, pady=5, sticky="nsew")
            kartu.grid_columnconfigure((0, 1), weight=1)

            t.teks(kartu, MODUL[kunci]["judul"], sekunder=True, tebal=True).grid(
                row=0, column=0, columnspan=2, padx=15, pady=(12, 0), sticky="w")
            lbl = t.judul(kartu, "0")
            lbl.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 8), sticky="w")
            self.lbl_jumlah[kunci] = lbl

            t.tombol(kartu, "Daftar", "utama", height=28,
                     command=lambda k=kunci: on_daftar and on_daftar(k)).grid(
                row=2, column=0, padx=(15, 4), pady=(0, 12), sticky="ew")
            t.tombol(kartu, "Tambah", "kedua", height=28,
                     command=lambda k=kunci: on_tambah and on_tambah(k)).grid(
                row=2, column=1, padx=(4, 15), pady=(0, 12), sticky="ew")

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def tampilkan_ringkasan(self, jumlah):
        """jumlah: dict {kunci_modul: banyak_data}, contoh {"mahasiswa": 12}."""
        for kunci, lbl in self.lbl_jumlah.items():
            lbl.configure(text=str(jumlah.get(kunci, 0)))

    def set_pengguna(self, nama):
        self.lbl_sapaan.configure(
            text=f"Selamat datang, {nama}. Pilih modul untuk mengelola data.")