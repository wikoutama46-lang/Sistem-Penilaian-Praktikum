"""Hak akses per aktor (sesuai SRS bagian 2.2). Aksi: lihat, tambah, ubah, hapus.

Aturan ini dicek di Controller (bukan hanya disembunyikan di tampilan),
jadi tetap berlaku walaupun tampilan berubah.
"""
SEMUA = {"lihat", "tambah", "ubah", "hapus"}

AKSES = {
    # Asisten Dosen: mengelola seluruh data praktikum dan nilai
    "asdos": {m: set(SEMUA) for m in
              ("mahasiswa", "praktikum", "pertemuan", "tugas", "laporan", "nilai")},
    # Dosen: hanya memantau data praktikum, laporan, dan nilai
    "dosen": {"praktikum": {"lihat"}, "laporan": {"lihat"}, "nilai": {"lihat"}},
    # Mahasiswa: lihat tugas, kumpulkan laporan sendiri, lihat nilai sendiri
    "mahasiswa": {"tugas": {"lihat"}, "laporan": {"lihat", "tambah"}, "nilai": {"lihat"}},
}

# Modul yang datanya hanya boleh dilihat pemiliknya saat role = mahasiswa
MODUL_MILIK_SENDIRI = ("laporan", "nilai")


def boleh(role, modul, aksi):
    return aksi in AKSES.get(role, {}).get(modul, ())


def modul_boleh_lihat(role, urutan):
    return [m for m in urutan if boleh(role, m, "lihat")]
