<p align="center">
  <img src="assets/icon.png" alt="Logo Sistem Penilaian Praktikum" width="120">
</p>

<h1 align="center">SISTEM PENILAIAN PRAKTIKUM</h1>

<p align="center">
  Kelompok 04 | Kelas C | Program Studi S1 Sistem Informasi
</p>

<p align="center">
  <a href="https://github.com/wikoutama46-lang/Sistem-Penilaian-Praktikum/actions/workflows/ci_pipeline.yml">
    <img src="https://github.com/wikoutama46-lang/Sistem-Penilaian-Praktikum/actions/workflows/ci_pipeline.yml/badge.svg" alt="Status CI">
  </a>
</p>

## Anggota Kelompok

| No. | Nama | NIM | Peran Utama |
|---|---|---|---|
| 1 | Wiko Brenton Askelon Mangoli | F5212530098 | Pembuatan Models dan Controllers |
| 2 | Rofilla Ramadani Reynold | F5212530113 | Diagram Konteks, Use Case Diagram, Activity Diagram |
| 3 | Muhammad Fadhil Nasrullah | F5212530093 | Sequence Diagram, Class Diagram, Diagram Navigasi |
| 4 | Intan Anggraini | F5212530107 | DFD Level 1, DFD Level 2, Arsitektur Sistem |

## Deskripsi

Sistem Penilaian Praktikum adalah aplikasi untuk mengelola data mahasiswa, praktikum, pertemuan, tugas, laporan, dan nilai mahasiswa.

Aplikasi dibuat dengan Python dan MySQL (Laragon sebagai lingkungan database). Proyek menerapkan pola **Model, View, Controller** sesuai materi Rekayasa Perangkat Lunak.

Tampilan tersedia dalam dua bentuk:

- **GUI desktop** (`views/`): berbasis customtkinter dengan halaman Login, Daftar Akun, Dashboard, Form, dan Daftar Data. Sudah terhubung ke Controller dan database.
- **CLI** (`views_cli/`): tampilan berbasis teks di terminal.

## Fitur

- Login dan pendaftaran akun untuk tiga aktor: **Asisten Dosen**, **Dosen**, dan **Mahasiswa**.
- Password disimpan sebagai hash (PBKDF2-SHA256 dengan salt acak), bukan teks biasa.
- Pendaftaran Asisten Dosen dan Dosen memerlukan kode registrasi.
- Hak akses per aktor dicek di Controller, jadi tetap berlaku walaupun tampilan berubah.
- CRUD untuk enam modul: mahasiswa, praktikum, pertemuan, tugas, laporan, dan nilai.
- Dashboard dengan ringkasan jumlah data dan delapan grafik beranimasi (donat, kolom, batang, gauge, dan garis). Grafik menyesuaikan hak akses: tiap peran hanya melihat grafik dari data yang boleh dilihatnya.
- Mahasiswa hanya melihat laporan dan nilai miliknya sendiri.
- Animasi pembuka (splash) dan ikon logo pada aplikasi `.exe`.

## Grafik Dashboard

| Grafik | Jenis | Sumber data | Peran yang melihat |
|---|---|---|---|
| Mahasiswa per Kelas | Donat | Mahasiswa | Asisten Dosen |
| Ketuntasan Nilai | Gauge | Nilai | Semua |
| Distribusi Nilai Akhir | Kolom | Nilai | Semua |
| Rata-rata Nilai per Praktikum | Batang | Nilai | Semua |
| Status Penilaian Laporan | Donat | Laporan | Semua |
| Peringkat Mahasiswa | Batang berperingkat | Nilai | Semua (Mahasiswa hanya data miliknya) |
| Pertemuan dan Tugas per Praktikum | Kolom ganda | Pertemuan, Tugas | Asisten Dosen, Mahasiswa (hanya tugas) |
| Jadwal Pertemuan per Bulan | Garis | Pertemuan | Asisten Dosen |

Grafik digambar dengan tkinter Canvas, jadi tidak memerlukan matplotlib. Arahkan kursor ke batang, irisan, atau titik untuk melihat angka rinci. Angka dihitung di `controllers/statistik.py`. Nilai tuntas minimal 60, dan grade A (85 ke atas), B (70), C (60), D (50), E (di bawah 50) dapat diubah di berkas yang sama.

## Hak Akses

| Aktor | Modul yang dapat diakses |
|---|---|
| Asisten Dosen | Semua modul (mahasiswa, praktikum, pertemuan, tugas, laporan, nilai): lihat, tambah, ubah, hapus |
| Dosen | Praktikum, laporan, dan nilai: hanya lihat |
| Mahasiswa | Tugas: lihat. Laporan: lihat dan tambah (milik sendiri). Nilai: lihat (milik sendiri) |

Aturan lengkap ada di `controllers/hak_akses.py`.

## Tujuan

- Mengelola data mahasiswa, praktikum, pertemuan, tugas, laporan, dan nilai.
- Menerapkan Model, View, dan Controller.
- Menghubungkan Python dengan database MySQL.
- Menerapkan operasi CRUD pada database.
- Menerapkan autentikasi dan otorisasi berdasarkan aktor.

## Teknologi

- Python 3.10 atau lebih baru (CI memakai Python 3.13)
- MySQL (Laragon)
- `mysql-connector-python` (koneksi database)
- `customtkinter` (tampilan GUI desktop)
- `pytest` (pengujian)
- PyInstaller (pemaketan menjadi `.exe`)

## Struktur Proyek

```text
Sistem-Penilaian-Praktikum/
│
├── app.py                  # titik masuk aplikasi GUI (splash, lalu jendela utama)
├── demo_cli.py             # uji tampilan CLI tanpa database
├── demo_gui.py             # uji tampilan GUI tanpa database dan Controller
├── test_model.py           # uji koneksi dan CRUD pada model (butuh MySQL)
├── requirements.txt        # dependensi Python
├── pytest.ini              # konfigurasi pytest
├── build_exe.bat           # bangun .exe di Windows (klik dua kali)
├── AplikasiPenilaianPraktikum.spec   # konfigurasi PyInstaller
│
├── config/
│   ├── database.py         # koneksi Python <-> MySQL Laragon
│   └── keamanan.py         # hash password dan kode registrasi
│
├── models/                 # akses data (query SQL)
│   ├── user_model.py
│   ├── mahasiswa_model.py
│   ├── praktikum_model.py
│   ├── pertemuan_model.py
│   ├── tugas_model.py
│   ├── laporan_model.py
│   └── nilai_model.py
│
├── controllers/            # validasi, hak akses, dan alur proses
│   ├── app_controller.py   # menyambungkan View GUI ke Controller modul
│   ├── auth_controller.py  # login dan pendaftaran akun
│   ├── hak_akses.py        # aturan hak akses per aktor
│   ├── base_controller.py
│   ├── statistik.py        # perhitungan data grafik Dashboard
│   └── <modul>_controller.py   # satu file per modul
│
├── views/                  # tampilan GUI (customtkinter)
│   ├── splash_view.py      # animasi pembuka
│   ├── tema.py             # warna, font, dan komponen bersama
│   ├── grafik.py           # pustaka grafik (Canvas): donat, kolom, batang, gauge, garis
│   ├── modul.py            # konfigurasi field dan kolom tiap modul
│   ├── app_view.py         # jendela utama dan navigasi antarhalaman
│   ├── login_view.py       # halaman Login
│   ├── register_view.py    # halaman Daftar Akun
│   ├── dashboard_view.py   # halaman Dashboard (kartu ringkasan dan grafik)
│   ├── form_view.py        # halaman Form (tambah/ubah data)
│   └── daftar_view.py      # halaman Daftar Data
│
├── views_cli/              # tampilan CLI (terminal)
│   ├── base_view.py
│   └── <modul>_view.py     # satu file per modul
│
├── database/
│   ├── database.sql        # skema dan data awal database (lihat Catatan)
│   └── auth.sql            # tabel users untuk login
│
├── tests/
│   ├── test_auth.py        # unit test autentikasi dan hak akses (tanpa MySQL)
│   └── test_statistik.py   # unit test perhitungan statistik grafik (tanpa MySQL)
│
├── assets/                 # logo, ikon .exe, dan gambar splash
├── tools/
│   └── buat_aset.py        # membuat ulang ikon dari logo
│
└── README.md
```

> `views/buku_view.py` dan `views/mahasiswa_view.py` adalah sisa tampilan awal dan tidak dipakai oleh aplikasi saat ini.

## Cara Menjalankan

1. Jalankan **MySQL** di Laragon.
2. Pasang dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Pastikan `database/database.sql` ada. Database `sistem_penilaian_praktikum` dibuat otomatis saat aplikasi pertama kali terkoneksi.
4. Jalankan `database/auth.sql` di database tersebut (lewat HeidiSQL atau phpMyAdmin Laragon) untuk membuat tabel `users`.
5. Jalankan aplikasi:
   ```bash
   python app.py
   ```
6. Buat akun lewat tombol **Daftar** di halaman Login, lalu masuk.

Koneksi database (host, port, nama database, user, password) diatur di `config/database.py`. Nilai bawaan mengikuti Laragon: user `root` dengan password kosong.

### Kode Registrasi

Pendaftaran akun **Asisten Dosen** dan **Dosen** memerlukan kode registrasi. Mahasiswa tidak memerlukan kode. Nilai bawaan ada di `config/keamanan.py`; ganti lewat environment variable sebelum dipakai sungguhan, dan jangan menaruh kode asli di GitHub:

```bat
setx KODE_REG_ASDOS "kode-rahasia-asdos"
setx KODE_REG_DOSEN "kode-rahasia-dosen"
```

Buka terminal baru setelah menjalankan `setx` agar nilainya terbaca.

### Mode Uji Tanpa Database

| Perintah | Fungsi |
|---|---|
| `python demo_gui.py` | Melihat tampilan GUI dan grafik dengan data contoh. Login dengan username dan password apa saja |
| `python demo_cli.py` | Melihat tampilan CLI dengan data contoh |
| `python test_model.py` | Menguji koneksi dan CRUD pada model (butuh MySQL aktif) |

## Pengujian

Unit test autentikasi dan hak akses tidak membutuhkan MySQL karena `UserModel` di-mock:

```bash
pip install pytest pytest-cov
pytest -v
```

Dengan laporan cakupan, seperti yang dijalankan di CI:

```bash
pytest -v --cov=config --cov=controllers --cov-report=term-missing
```

## Membuat Aplikasi `.exe`

Aplikasi dapat dipaketkan menjadi satu file `.exe` berikon logo dan beranimasi pembuka. Pemaketan harus dilakukan di **Windows**.

**Cara mudah:** klik dua kali `build_exe.bat`.

**Lewat terminal:**

```bash
pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean AplikasiPenilaianPraktikum.spec
```

Hasilnya ada di `dist/AplikasiPenilaianPraktikum.exe`. Folder `build/` hanya berisi berkas sementara.

Saat `.exe` dibuka:

1. Gambar logo statis (`assets/boot_splash.png`) tampil seketika.
2. Splash beranimasi memuat modul di latar belakang dengan bar kemajuan.
3. Jendela Login muncul perlahan.

Lama splash dapat diubah lewat `DURASI_MIN_MS` di `views/splash_view.py`. Untuk mengganti logo, timpa `assets/logo.png`, lalu jalankan `python tools/buat_aset.py` (butuh `pip install pillow`).

Aplikasi `.exe` tetap membutuhkan MySQL Laragon yang aktif dan tabel `users` dari `database/auth.sql`.

## CI/CD

Workflow GitHub Actions (`.github/workflows/ci_pipeline.yml`) berjalan pada setiap push dan pull request ke `main`:

1. **test**: menjalankan unit test dengan `pytest`.
2. **build-exe**: membangun `.exe` di Windows lewat `AplikasiPenilaianPraktikum.spec` (tidak dijalankan pada pull request). Hasilnya dapat diunduh dari tab **Actions** sebagai artifact `AplikasiPenilaianPraktikum`.

## Status Integrasi

| Komponen | Status |
|---|---|
| Model dan Controller | Selesai, diuji lewat `test_model.py` |
| Autentikasi dan hak akses | Selesai, diuji lewat `tests/test_auth.py` |
| View CLI | Selesai, uji lewat `demo_cli.py` |
| View GUI | Selesai dan terhubung ke Controller lewat `app.py` |
| Pemaketan `.exe` | Selesai, ikon dan splash beranimasi |

## Catatan

- `database/database.sql` (skema dasar: tabel mahasiswa, praktikum, pertemuan, tugas, laporan, nilai) dibaca otomatis oleh `config/database.py`. Pastikan berkas ini tersedia di folder `database/` sebelum aplikasi dijalankan pertama kali.
- `database/auth.sql` tidak ikut dijalankan otomatis; jalankan manual satu kali untuk membuat tabel `users`.
- Jangan menaruh tanda titik koma di dalam komentar atau teks pada berkas SQL, karena `Database.setup_database()` memecah berkas berdasarkan tanda titik koma.
