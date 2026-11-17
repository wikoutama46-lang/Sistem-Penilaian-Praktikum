# Logo .exe + Animasi Pembuka — Sistem Penilaian Praktikum

## Isi paket
| Berkas | Fungsi |
|---|---|
| `assets/icon.ico` | Ikon `.exe` (16–256 px), dibuat dari logo chip |
| `assets/icon.png` | Ikon jendela 256 px |
| `assets/boot_splash.png` | Gambar statis yang tampil seketika saat `.exe` diklik |
| `assets/logo.png` | Logo asli (sumber) |
| `views/splash_view.py` | Animasi splash (tkinter murni, tanpa Pillow) |
| `app.py` | Titik masuk baru: splash → muat modul → jendela utama fade-in |
| `AplikasiPenilaianPraktikum.spec` | Konfigurasi PyInstaller (ikon + splash) |
| `build_exe.bat` | Klik dua kali di Windows untuk membangun `.exe` |
| `.github/workflows/ci_pipeline.yml` | CI yang sudah memakai file `.spec` |
| `tools/buat_aset.py` | Membuat ulang ikon bila logo diganti |

## Cara pasang
1. Ekstrak zip ini **ke folder utama repo** (sejajar `app.py` lama), timpa `app.py` dan `ci_pipeline.yml`.
2. Uji tanpa `.exe`: `python app.py`
3. Bangun `.exe` di Windows: klik dua kali `build_exe.bat`
   Hasil: `dist\AplikasiPenilaianPraktikum.exe`
   (Atau cukup `git push`; job `build-exe` di GitHub Actions menghasilkan `.exe` otomatis.)

## Urutan animasi saat `.exe` dibuka
1. Gambar statis logo muncul langsung (saat `.exe` mengekstrak diri).
2. Splash beranimasi: kaki chip memanjang → chip muncul → centang tergambar + riak cahaya → teks `// SISTEM PENILAIAN` dan `Praktikum_` diketik, kursor berkedip.
3. Bar kemajuan mengikuti pemuatan modul yang sebenarnya.
4. Splash memudar, jendela Login muncul perlahan.

## Kustomisasi
- Lama splash: ubah `DURASI_MIN_MS` di `views/splash_view.py` (default 2800 ms).
- Warna: konstanta di bagian atas `splash_view.py`.
- Ganti logo: timpa `assets/logo.png`, lalu `pip install pillow` dan `python tools/buat_aset.py`.
- Ubah teks status: fungsi `_muat_modul` di `app.py`.

## Catatan
- Ikon tidak berubah di Explorer? Windows menyimpan cache ikon; ganti nama `.exe` atau restart Explorer.
- Antivirus kadang menandai `.exe` PyInstaller `--onefile` (false positive); tambahkan pengecualian jika perlu.
- Bila aplikasi gagal mulai (mis. MySQL Laragon belum jalan), muncul kotak pesan galat, bukan menghilang diam-diam.
