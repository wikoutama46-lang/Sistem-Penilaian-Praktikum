"""Konfigurasi modul untuk halaman Form dan Daftar (hanya data tampilan, tanpa logika).

Kunci field sengaja sama dengan nama parameter di controller (tambah/ubah),
sedangkan kunci kolom sama dengan kolom hasil model.get_all().

field : (kunci, label, placeholder, wajib)
kolom : (kunci, judul kolom, lebar)
"""

MODUL = {
    "mahasiswa": {
        "judul": "Mahasiswa",
        "id": "id_mahasiswa",
        "field": [
            ("nim", "NIM", "Masukkan NIM", True),
            ("nama", "Nama", "Masukkan nama mahasiswa", True),
            ("kelas", "Kelas", "Masukkan kelas (contoh: C)", True),
        ],
        "kolom": [
            ("id_mahasiswa", "ID", 50),
            ("nim", "NIM", 130),
            ("nama", "Nama", 260),
            ("kelas", "Kelas", 80),
        ],
    },
    "praktikum": {
        "judul": "Praktikum",
        "id": "id_praktikum",
        "field": [
            ("nama_praktikum", "Nama Praktikum", "Masukkan nama praktikum", True),
            ("asisten_dosen", "Asisten Dosen", "Masukkan nama asisten dosen", True),
        ],
        "kolom": [
            ("id_praktikum", "ID", 50),
            ("nama_praktikum", "Nama Praktikum", 300),
            ("asisten_dosen", "Asisten Dosen", 250),
        ],
    },
    "pertemuan": {
        "judul": "Pertemuan",
        "id": "id_pertemuan",
        "field": [
            ("id_praktikum", "ID Praktikum", "Masukkan ID praktikum", True),
            ("pertemuan_ke", "Pertemuan Ke-", "Masukkan nomor pertemuan", True),
            ("tanggal", "Tanggal", "Tanggal (YYYY-MM-DD)", True),
        ],
        "kolom": [
            ("id_pertemuan", "ID", 50),
            ("nama_praktikum", "Praktikum", 280),
            ("pertemuan_ke", "Pertemuan", 90),
            ("tanggal", "Tanggal", 120),
        ],
    },
    "tugas": {
        "judul": "Tugas",
        "id": "id_tugas",
        "field": [
            ("id_pertemuan", "ID Pertemuan", "Masukkan ID pertemuan", True),
            ("nama_tugas", "Nama Tugas", "Masukkan nama tugas", True),
            ("deadline", "Deadline", "Deadline (YYYY-MM-DD HH:MM:SS)", True),
        ],
        "kolom": [
            ("id_tugas", "ID", 50),
            ("nama_praktikum", "Praktikum", 200),
            ("pertemuan_ke", "Pertemuan", 80),
            ("nama_tugas", "Nama Tugas", 200),
            ("deadline", "Deadline", 150),
        ],
    },
    "laporan": {
        "judul": "Laporan",
        "id": "id_laporan",
        "field": [
            ("id_mahasiswa", "ID Mahasiswa", "Masukkan ID mahasiswa", True),
            ("id_pertemuan", "ID Pertemuan", "Masukkan ID pertemuan", True),
            ("judul_laporan", "Judul Laporan", "Masukkan judul laporan", True),
            ("nilai_laporan", "Nilai Laporan", "Nilai 0-100 (opsional)", False),
        ],
        "kolom": [
            ("id_laporan", "ID", 50),
            ("nim", "NIM", 100),
            ("nama", "Mahasiswa", 150),
            ("nama_praktikum", "Praktikum", 140),
            ("pertemuan_ke", "Pert.", 50),
            ("judul_laporan", "Judul Laporan", 170),
            ("nilai_laporan", "Nilai", 60),
        ],
    },
    "nilai": {
        "judul": "Nilai",
        "id": "id_nilai",
        "field": [
            ("id_mahasiswa", "ID Mahasiswa", "Masukkan ID mahasiswa", True),
            ("id_praktikum", "ID Praktikum", "Masukkan ID praktikum", True),
            ("nilai_tugas", "Nilai Tugas", "Nilai 0-100", True),
            ("nilai_laporan", "Nilai Laporan", "Nilai 0-100", True),
            ("nilai_kehadiran", "Nilai Kehadiran", "Nilai 0-100", True),
        ],
        "kolom": [
            ("id_nilai", "ID", 40),
            ("nim", "NIM", 100),
            ("nama", "Mahasiswa", 150),
            ("nama_praktikum", "Praktikum", 130),
            ("nilai_tugas", "Tugas", 55),
            ("nilai_laporan", "Laporan", 60),
            ("nilai_kehadiran", "Hadir", 55),
            ("nilai_akhir", "Akhir", 55),
        ],
    },
}

URUTAN = list(MODUL)


def kunci_dari_judul(judul):
    """Cari kunci modul dari judul yang tampil di menu pilihan."""
    return next(k for k, m in MODUL.items() if m["judul"] == judul)