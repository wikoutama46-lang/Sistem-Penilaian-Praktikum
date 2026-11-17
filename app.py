"""Titik masuk aplikasi. Semua View tersambung ke Controller lewat AplikasiController.

Saat dibuka, aplikasi menampilkan splash beranimasi (views/splash_view.py) sambil
memuat modul di latar belakang, lalu jendela utama muncul perlahan.

Jalankan dari folder proyek:  python app.py
(Pastikan MySQL Laragon sudah Start dan database/auth.sql sudah dijalankan.)
"""
import traceback

from views.splash_view import atur_id_aplikasi, fade_in, pasang_ikon, tampilkan_splash


def _muat_modul(lapor):
    """Dijalankan di thread latar selama splash tampil."""
    lapor("Memuat pustaka antarmuka ...", 0.10)
    import customtkinter  # noqa: F401
    lapor("Memuat modul database ...", 0.40)
    import mysql.connector  # noqa: F401
    from controllers.app_controller import AplikasiController
    lapor("Menyiapkan tampilan ...", 0.75)
    from views.app_view import AplikasiView
    lapor("Hampir selesai ...", 0.95)
    return AplikasiController, AplikasiView


def _tampilkan_galat():
    """Pada .exe tanpa konsol, galat tidak terlihat; tampilkan lewat kotak pesan."""
    import tkinter as tk
    from tkinter import messagebox
    akar = tk.Tk()
    akar.withdraw()
    messagebox.showerror("Sistem Penilaian Praktikum",
                         "Aplikasi gagal dimulai.\n\n" + traceback.format_exc(limit=3))
    akar.destroy()


def main():
    atur_id_aplikasi()
    AplikasiController, AplikasiView = tampilkan_splash(_muat_modul)
    app = AplikasiView()
    pasang_ikon(app)          # ikon logo pada jendela dan taskbar
    AplikasiController(app)
    fade_in(app)              # jendela utama muncul perlahan
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        _tampilkan_galat()
        raise
