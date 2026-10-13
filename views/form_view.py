"""Halaman Form (GUI): input data satu modul. Mode Tambah (kosong) atau Ubah (terisi)."""
import customtkinter as ctk

from views import tema as t
from views.modul import MODUL, URUTAN, kunci_dari_judul


class FormView(ctk.CTkFrame):
    def __init__(self, master, on_ganti_modul=None, on_lihat_daftar=None):
        super().__init__(master, fg_color=t.LATAR)
        self._on_ganti_modul = on_ganti_modul
        self.modul = URUTAN[0]
        self._id_data = None          # ID baris yang sedang diubah (None = mode tambah)
        self.entri = {}               # {kunci_field: CTkEntry}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.panel = t.panel(self)
        self.panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.panel.grid_columnconfigure(0, weight=1)
        self.panel.grid_rowconfigure(2, weight=1)

        # Baris judul + pilihan modul
        kepala = ctk.CTkFrame(self.panel, fg_color="transparent")
        kepala.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        kepala.grid_columnconfigure(0, weight=1)
        self.lbl_judul = t.judul(kepala, "Form Data")
        self.lbl_judul.grid(row=0, column=0, sticky="w")
        t.teks(kepala, "Modul:", sekunder=True).grid(row=0, column=1, padx=(0, 8))
        self.pilih_modul = t.menu_pilihan(
            kepala, [MODUL[k]["judul"] for k in URUTAN], command=self._modul_dipilih, width=140)
        self.pilih_modul.grid(row=0, column=2)

        self.lbl_mode = t.teks(self.panel, "", sekunder=True)
        self.lbl_mode.grid(row=1, column=0, padx=20, pady=(2, 8), sticky="w")

        # Area isian (dibangun ulang setiap modul berganti)
        self.frame_field = ctk.CTkFrame(self.panel, fg_color="transparent")
        self.frame_field.grid(row=2, column=0, padx=20, sticky="nsew")
        self.frame_field.grid_columnconfigure((0, 1), weight=1, uniform="isian")

        # Tombol aksi
        bar = ctk.CTkFrame(self.panel, fg_color="transparent")
        bar.grid(row=3, column=0, padx=20, pady=(8, 18), sticky="ew")
        self.btn_simpan = t.tombol(bar, "Simpan", "utama", width=110)
        self.btn_update = t.tombol(bar, "Perbarui", "kedua", width=110)
        self.btn_hapus = t.tombol(bar, "Hapus", "bahaya", width=110)
        self.btn_bersihkan = t.tombol(bar, "Bersihkan", "garis", width=110)
        self.btn_daftar = t.tombol(bar, "Lihat Daftar", "garis", width=120,
                                   command=on_lihat_daftar)
        for tb in (self.btn_simpan, self.btn_update, self.btn_hapus, self.btn_bersihkan):
            tb.pack(side="left", padx=(0, 8))
        self.btn_daftar.pack(side="right")
        self.btn_bersihkan.configure(command=self.kosongkan_form)

        self.atur_modul(self.modul)

    # ---------- internal ----------
    def _modul_dipilih(self, judul_modul):
        kunci = kunci_dari_judul(judul_modul)
        self.atur_modul(kunci)
        if self._on_ganti_modul:
            self._on_ganti_modul(kunci)

    def _bangun_field(self):
        for w in self.frame_field.winfo_children():
            w.destroy()
        self.entri = {}
        for i, (kunci, label, placeholder, wajib) in enumerate(MODUL[self.modul]["field"]):
            baris, kolom = divmod(i, 2)
            sel = ctk.CTkFrame(self.frame_field, fg_color="transparent")
            sel.grid(row=baris, column=kolom, padx=6, pady=4, sticky="ew")
            sel.grid_columnconfigure(0, weight=1)
            t.teks(sel, label + (" *" if wajib else ""), sekunder=True).grid(
                row=0, column=0, sticky="w")
            kolom_input = t.entri(sel, placeholder)
            kolom_input.grid(row=1, column=0, sticky="ew")
            self.entri[kunci] = kolom_input

    def _atur_mode(self):
        ubah = self._id_data is not None
        self.btn_simpan.configure(state="disabled" if ubah else "normal")
        self.btn_update.configure(state="normal" if ubah else "disabled")
        self.btn_hapus.configure(state="normal" if ubah else "disabled")
        self.pilih_modul.configure(state="disabled" if ubah else "normal")
        nama = MODUL[self.modul]["judul"]
        self.lbl_judul.configure(text=f"Form Data {nama}")
        self.lbl_mode.configure(
            text=(f"Mode ubah: {nama} ID {self._id_data}" if ubah
                  else "Mode tambah: isi data baru, lalu tekan Simpan.   * wajib diisi"))

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def atur_modul(self, kunci, data=None):
        """Tampilkan form modul `kunci`. Jika `data` (dict) diberikan, form masuk mode ubah."""
        self.modul = kunci
        self.pilih_modul.set(MODUL[kunci]["judul"])
        self._bangun_field()
        self._id_data = None
        if data is not None:
            self._id_data = data.get(MODUL[kunci]["id"])
            self.isi_form(data)
        self._atur_mode()

    def ambil_input(self):
        """Isi form sebagai dict {kunci_field: teks}."""
        return {k: e.get().strip() for k, e in self.entri.items()}

    def isi_form(self, data):
        self.kosongkan_form()
        for kunci, kolom in self.entri.items():
            nilai = data.get(kunci)
            if nilai not in (None, ""):
                kolom.insert(0, str(nilai))

    def kosongkan_form(self):
        for kolom in self.entri.values():
            kolom.delete(0, "end")

    def id_terpilih(self):
        """ID data yang sedang diubah, atau None bila mode tambah."""
        return self._id_data

    def field_wajib_kosong(self):
        """Daftar label field wajib yang masih kosong."""
        isi = self.ambil_input()
        return [label for kunci, label, _p, wajib in MODUL[self.modul]["field"]
                if wajib and not isi.get(kunci)]

    def tampilkan_pesan(self, teks, error=False):
        (t.pesan_error if error else t.pesan_info)(teks)

    def konfirmasi_hapus(self):
        return t.konfirmasi("Yakin ingin menghapus data ini?")