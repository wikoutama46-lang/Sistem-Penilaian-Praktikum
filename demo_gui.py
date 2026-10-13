"""Uji tampilan GUI tanpa database dan tanpa Controller (data contoh di memori).
Jalankan dari folder proyek:  python demo_gui.py
Login: isi username dan password apa saja.
(Tampilan CLI tetap tersedia lewat:  python demo_cli.py)
"""
from views.app_view import AplikasiView

DATA_CONTOH = {
    "mahasiswa": [
        {"id_mahasiswa": 1, "nim": "F5212530098", "nama": "Wiko Brenton Askelon Mangoli", "kelas": "C"},
        {"id_mahasiswa": 2, "nim": "F5212530001", "nama": "Contoh Mahasiswa Dua", "kelas": "C"},
    ],
    "praktikum": [
        {"id_praktikum": 1, "nama_praktikum": "Rekayasa Perangkat Lunak", "asisten_dosen": "Asisten A"},
        {"id_praktikum": 2, "nama_praktikum": "Basis Data", "asisten_dosen": "Asisten B"},
    ],
    "pertemuan": [
        {"id_pertemuan": 1, "nama_praktikum": "Rekayasa Perangkat Lunak", "pertemuan_ke": 1, "tanggal": "2026-09-01"},
        {"id_pertemuan": 2, "nama_praktikum": "Rekayasa Perangkat Lunak", "pertemuan_ke": 2, "tanggal": "2026-09-08"},
    ],
    "tugas": [
        {"id_tugas": 1, "nama_praktikum": "Rekayasa Perangkat Lunak", "pertemuan_ke": 1,
         "nama_tugas": "Use Case Diagram", "deadline": "2026-09-05 23:59:00"},
    ],
    "laporan": [
        {"id_laporan": 1, "nim": "F5212530098", "nama": "Wiko Brenton Askelon Mangoli",
         "nama_praktikum": "Rekayasa Perangkat Lunak", "pertemuan_ke": 1,
         "judul_laporan": "Laporan Use Case", "nilai_laporan": 85},
    ],
    "nilai": [
        {"id_nilai": 1, "nim": "F5212530098", "nama": "Wiko Brenton Askelon Mangoli",
         "nama_praktikum": "Rekayasa Perangkat Lunak", "nilai_tugas": 90,
         "nilai_laporan": 85, "nilai_kehadiran": 100, "nilai_akhir": 90.0},
    ],
}


def main():
    app = AplikasiView()
    app.dashboard.tampilkan_ringkasan({k: len(v) for k, v in DATA_CONTOH.items()})
    app.on_modul_berubah = lambda kunci: app.daftar.tampilkan_data(DATA_CONTOH.get(kunci, []))
    app.mainloop()


if __name__ == "__main__":
    main()