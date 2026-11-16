"""Titik masuk aplikasi. Semua View tersambung ke Controller lewat AplikasiController.

Jalankan dari folder proyek:  python app.py
(Pastikan MySQL Laragon sudah Start dan database/auth.sql sudah dijalankan.)
"""
from controllers.app_controller import AplikasiController
from views.app_view import AplikasiView


def main():
    app = AplikasiView()
    AplikasiController(app)
    app.mainloop()


if __name__ == "__main__":
    main()
