"""Halaman Login (GUI). View pasif: hanya menampilkan komponen dan mengambil input."""
import customtkinter as ctk

from views import tema as t


class LoginView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=t.LATAR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.panel = t.panel(self, width=360)
        self.panel.grid(row=0, column=0)

        t.judul(self.panel, "Sistem Penilaian Praktikum").pack(pady=(28, 4), padx=30)
        t.teks(self.panel, "Silakan masuk untuk melanjutkan", sekunder=True).pack(pady=(0, 18))

        self.entry_username = t.entri(self.panel, "Username", width=280)
        self.entry_username.pack(pady=6, padx=30)

        self.entry_password = t.entri(self.panel, "Password", width=280, show="•")
        self.entry_password.pack(pady=6, padx=30)

        self.btn_masuk = t.tombol(self.panel, "Masuk", "utama", width=280)
        self.btn_masuk.pack(pady=(18, 28), padx=30)

        # Enter pada kolom isian sama dengan menekan tombol Masuk
        for kolom in (self.entry_username, self.entry_password):
            kolom.bind("<Return>", lambda _e: self.btn_masuk.invoke())

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        return {
            "username": self.entry_username.get().strip(),
            "password": self.entry_password.get(),
        }

    def kosongkan_form(self):
        self.entry_username.delete(0, "end")
        self.entry_password.delete(0, "end")

    def fokus(self):
        self.entry_username.focus_set()

    def tampilkan_pesan(self, teks, error=False):
        (t.pesan_error if error else t.pesan_info)(teks)