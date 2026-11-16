"""Halaman Sign Up (GUI). View pasif: hanya menampilkan komponen dan mengambil input.

Isian tambahan menyesuaikan aktor yang dipilih:
  Mahasiswa     -> NIM, Kelas
  Dosen         -> NIDN, Kode registrasi
  Asisten Dosen -> Kode registrasi
"""
import customtkinter as ctk

from views import tema as t

PERAN = {"Mahasiswa": "mahasiswa", "Asisten Dosen": "asdos", "Dosen": "dosen"}
# kunci input tambahan yang tampil untuk tiap peran
EXTRA = {"mahasiswa": ("nim", "kelas"), "dosen": ("nidn", "kode"), "asdos": ("kode",)}


class RegisterView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=t.LATAR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.panel = t.panel(self)
        self.panel.grid(row=0, column=0)

        t.judul(self.panel, "Daftar Akun Baru").grid(
            row=0, column=0, columnspan=2, pady=(22, 2), padx=30)
        t.teks(self.panel, "Pilih peran lalu lengkapi data di bawah",
               sekunder=True).grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.pilih_peran = t.menu_pilihan(self.panel, list(PERAN), command=self._peran_dipilih,
                                          width=300)
        self.pilih_peran.grid(row=2, column=0, columnspan=2, pady=(0, 8))

        # Kolom kiri: data umum
        kiri = ctk.CTkFrame(self.panel, fg_color="transparent")
        kiri.grid(row=3, column=0, padx=(30, 8), sticky="n")
        self.entry_nama = t.entri(kiri, "Nama lengkap", width=250)
        self.entry_username = t.entri(kiri, "Username", width=250)
        self.entry_password = t.entri(kiri, "Password (min. 8 karakter)", width=250, show="•")
        self.entry_konfirmasi = t.entri(kiri, "Ulangi password", width=250, show="•")
        for e in (self.entry_nama, self.entry_username, self.entry_password, self.entry_konfirmasi):
            e.pack(pady=5)

        # Kolom kanan: data khusus peran (dibangun sekali, ditampilkan sesuai peran)
        self.kanan = ctk.CTkFrame(self.panel, fg_color="transparent")
        self.kanan.grid(row=3, column=1, padx=(8, 30), sticky="n")
        self.entry_extra = {
            "nim": t.entri(self.kanan, "NIM", width=250),
            "kelas": t.entri(self.kanan, "Kelas (contoh: C)", width=250),
            "nidn": t.entri(self.kanan, "NIDN", width=250),
            "kode": t.entri(self.kanan, "Kode registrasi", width=250, show="•"),
        }

        bar = ctk.CTkFrame(self.panel, fg_color="transparent")
        bar.grid(row=4, column=0, columnspan=2, pady=(14, 22))
        self.btn_daftar = t.tombol(bar, "Daftar", "utama", width=150)
        self.btn_daftar.pack(side="left", padx=6)
        self.btn_kembali = t.tombol(bar, "Kembali ke Login", "garis", width=150)
        self.btn_kembali.pack(side="left", padx=6)

        self._peran_dipilih(self.pilih_peran.get())

    def _peran_dipilih(self, label):
        for e in self.entry_extra.values():
            e.pack_forget()
        for kunci in EXTRA[PERAN[label]]:
            self.entry_extra[kunci].pack(pady=5)

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        return {
            "role": PERAN[self.pilih_peran.get()],
            "nama": self.entry_nama.get().strip(),
            "username": self.entry_username.get().strip(),
            "password": self.entry_password.get(),
            "konfirmasi": self.entry_konfirmasi.get(),
            "nim": self.entry_extra["nim"].get().strip(),
            "kelas": self.entry_extra["kelas"].get().strip(),
            "nidn": self.entry_extra["nidn"].get().strip(),
            "kode": self.entry_extra["kode"].get(),
        }

    def kosongkan_form(self):
        for e in (self.entry_nama, self.entry_username, self.entry_password,
                  self.entry_konfirmasi, *self.entry_extra.values()):
            e.delete(0, "end")

    def fokus(self):
        self.entry_nama.focus_set()

    def tampilkan_pesan(self, teks, error=False):
        (t.pesan_error if error else t.pesan_info)(teks)
