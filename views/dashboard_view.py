"""Halaman Dashboard (GUI): ringkasan jumlah data, grafik statistik, dan pintasan ke Daftar/Form.

Grafik hanya digambar di sini (views/grafik.py); angkanya dihitung Controller
(controllers/statistik.py) dan dikirim lewat tampilkan_grafik(). Grafik yang datanya
tidak boleh dilihat peran pengguna otomatis disembunyikan oleh atur_akses().
"""
import customtkinter as ctk

from views import tema as t
from views.grafik import (GrafikBatang, GrafikDonat, GrafikGauge, GrafikGaris, GrafikKolom,
                          PALET, WARNA_GRADE)
from views.modul import MODUL, URUTAN

KOLOM_KARTU = 3
KOLOM_GRAFIK = 2

# (kunci, judul, keterangan, kelas grafik, modul yang dibutuhkan: cukup salah satu terlihat)
DAFTAR_GRAFIK = [
    ("kelas", "Mahasiswa per Kelas", "Sebaran jumlah mahasiswa", GrafikDonat, {"mahasiswa"}),
    ("ketuntasan", "Ketuntasan Nilai", "Persentase nilai akhir yang tuntas", GrafikGauge, {"nilai"}),
    ("grade", "Distribusi Nilai Akhir", "Jumlah nilai pada tiap grade", GrafikKolom, {"nilai"}),
    ("rata_praktikum", "Rata-rata Nilai per Praktikum", "Nilai akhir, skala 0-100",
     GrafikBatang, {"nilai"}),
    ("laporan", "Status Penilaian Laporan", "Laporan yang sudah dan belum dinilai",
     GrafikDonat, {"laporan"}),
    ("peringkat", "Peringkat Mahasiswa", "Rata-rata nilai akhir tertinggi", GrafikBatang, {"nilai"}),
    ("aktivitas", "Pertemuan dan Tugas per Praktikum", "Perbandingan jumlah kegiatan",
     GrafikKolom, {"pertemuan", "tugas"}),
    ("tren", "Jadwal Pertemuan per Bulan", "Jumlah pertemuan tiap bulan", GrafikGaris, {"pertemuan"}),
]


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_daftar=None, on_tambah=None):
        """on_daftar(kunci_modul) dan on_tambah(kunci_modul) dipasang oleh jendela utama."""
        super().__init__(master, fg_color=t.LATAR)
        self._on_daftar = on_daftar
        self._on_tambah = on_tambah
        self._lihat = set(URUTAN)   # modul yang boleh dilihat (diatur lewat atur_akses)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # seluruh isi dapat digulir karena grafik membuat halaman lebih tinggi dari jendela
        self.isi = ctk.CTkScrollableFrame(self, fg_color=t.LATAR, corner_radius=0,
                                          scrollbar_button_color="#C5CBDD",
                                          scrollbar_button_hover_color=t.NAVY_SEDANG)
        self.isi.grid(row=0, column=0, sticky="nsew")
        self.isi.grid_columnconfigure(0, weight=1)

        # Judul + sapaan
        kepala = t.panel(self.isi)
        kepala.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        t.judul(kepala, "Dashboard").pack(anchor="w", padx=15, pady=(12, 0))
        self.lbl_sapaan = t.teks(kepala, "Selamat datang. Pilih modul untuk mengelola data.",
                                 sekunder=True)
        self.lbl_sapaan.pack(anchor="w", padx=15, pady=(0, 12))

        self._bangun_kartu()
        self._bangun_grafik()

    # ---------- susunan ----------
    def _bangun_kartu(self):
        """Kartu ringkasan per modul."""
        area = ctk.CTkFrame(self.isi, fg_color="transparent")
        area.grid(row=1, column=0, padx=15, pady=0, sticky="nsew")
        for k in range(KOLOM_KARTU):
            area.grid_columnconfigure(k, weight=1, uniform="kartu")

        self.lbl_jumlah = {}
        self.kartu = {}
        self.btn_tambah = {}
        for i, kunci in enumerate(URUTAN):
            kartu = t.panel(area)
            kartu.grid(row=i // KOLOM_KARTU, column=i % KOLOM_KARTU,
                       padx=5, pady=5, sticky="nsew")
            self.kartu[kunci] = kartu
            kartu.grid_columnconfigure((0, 1), weight=1)

            t.teks(kartu, MODUL[kunci]["judul"], sekunder=True, tebal=True).grid(
                row=0, column=0, columnspan=2, padx=15, pady=(12, 0), sticky="w")
            lbl = t.judul(kartu, "0")
            lbl.grid(row=1, column=0, columnspan=2, padx=15, pady=(0, 8), sticky="w")
            self.lbl_jumlah[kunci] = lbl

            t.tombol(kartu, "Daftar", "utama", height=28,
                     command=lambda k=kunci: self._on_daftar and self._on_daftar(k)).grid(
                row=2, column=0, padx=(15, 4), pady=(0, 12), sticky="ew")
            btn = t.tombol(kartu, "Tambah", "kedua", height=28,
                           command=lambda k=kunci: self._on_tambah and self._on_tambah(k))
            btn.grid(row=2, column=1, padx=(4, 15), pady=(0, 12), sticky="ew")
            self.btn_tambah[kunci] = btn

    def _bangun_grafik(self):
        self.lbl_statistik = t.judul(self.isi, "Statistik")
        self.lbl_statistik.grid(row=2, column=0, padx=20, pady=(14, 2), sticky="w")

        self.area_grafik = ctk.CTkFrame(self.isi, fg_color="transparent")
        self.area_grafik.grid(row=3, column=0, padx=15, pady=(0, 20), sticky="nsew")
        for k in range(KOLOM_GRAFIK):
            self.area_grafik.grid_columnconfigure(k, weight=1, uniform="grafik")

        self.grafik = {}
        for kunci, judul, ket, kelas, butuh in DAFTAR_GRAFIK:
            panel = t.panel(self.area_grafik)
            panel.grid_columnconfigure(0, weight=1)
            t.teks(panel, judul, tebal=True).grid(row=0, column=0, padx=15, pady=(12, 0), sticky="w")
            ctk.CTkLabel(panel, text=ket, font=("Arial", 11), text_color=t.PLACEHOLDER).grid(
                row=1, column=0, padx=15, pady=(0, 4), sticky="w")
            kanvas = kelas(panel)
            kanvas.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
            self.grafik[kunci] = {"panel": panel, "kanvas": kanvas}
        self._susun_grafik()

    def _susun_grafik(self):
        """Tampilkan hanya grafik yang bisa dibuat dari modul yang boleh dilihat peran ini."""
        for g in self.grafik.values():
            g["panel"].grid_remove()
        tampil = [spek[0] for spek in DAFTAR_GRAFIK if spek[4] & self._lihat]
        for i, kunci in enumerate(tampil):
            baris, kolom = divmod(i, KOLOM_GRAFIK)
            sendiri = i == len(tampil) - 1 and len(tampil) % KOLOM_GRAFIK == 1
            self.grafik[kunci]["panel"].grid(
                row=baris, column=0 if sendiri else kolom,
                columnspan=KOLOM_GRAFIK if sendiri else 1, padx=5, pady=5, sticky="nsew")
        if tampil:
            self.lbl_statistik.grid()
        else:
            self.lbl_statistik.grid_remove()

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def tampilkan_ringkasan(self, jumlah):
        """jumlah: dict {kunci_modul: banyak_data}, contoh {"mahasiswa": 12}."""
        for kunci, lbl in self.lbl_jumlah.items():
            lbl.configure(text=str(jumlah.get(kunci, 0)))

    def tampilkan_grafik(self, stat):
        """stat: dict hasil controllers.statistik.hitung_statistik()."""
        g = {k: v["kanvas"] for k, v in self.grafik.items()}

        kelas = stat.get("kelas") or []
        g["kelas"].set_data(kelas, tengah=(str(sum(n for _, n in kelas)), "Mahasiswa"))

        g["ketuntasan"].set_data(stat.get("ketuntasan"))

        grade = stat.get("grade") or []
        g["grade"].set_data(
            [f"{x['grade']}  {x['batas']}" for x in grade],
            [("Jumlah nilai", [x["jumlah"] for x in grade],
              [WARNA_GRADE[x["grade"]] for x in grade])])

        g["rata_praktikum"].set_data(stat.get("rata_praktikum") or [], maks=100)

        lap = stat.get("laporan")
        if lap:
            g["laporan"].set_data(
                [("Sudah dinilai", lap["dinilai"]), ("Belum dinilai", lap["belum"])],
                tengah=(f"{lap['persen']}%", "sudah dinilai"))
        else:
            g["laporan"].set_data([])

        g["peringkat"].set_data(stat.get("peringkat") or [], maks=100, peringkat=True)

        akt = stat.get("aktivitas")
        if akt:
            g["aktivitas"].set_data(
                akt["label"], [(nama, nilai, PALET[i]) for i, (nama, nilai) in enumerate(akt["seri"])])
        else:
            g["aktivitas"].set_data([], [])

        g["tren"].set_data(stat.get("tren") or [])

    def atur_akses(self, boleh_lihat, boleh_tambah):
        """Tampilkan hanya kartu modul yang boleh dilihat; tombol Tambah mengikuti hak tambah."""
        self._lihat = set(boleh_lihat)
        for kartu in self.kartu.values():
            kartu.grid_remove()
        for i, kunci in enumerate(k for k in URUTAN if k in boleh_lihat):
            self.kartu[kunci].grid(row=i // KOLOM_KARTU, column=i % KOLOM_KARTU,
                                   padx=5, pady=5, sticky="nsew")
            self.btn_tambah[kunci].configure(
                state="normal" if kunci in boleh_tambah else "disabled")
        self._susun_grafik()

    def set_pengguna(self, nama):
        self.lbl_sapaan.configure(
            text=f"Selamat datang, {nama}. Pilih modul untuk mengelola data.")
