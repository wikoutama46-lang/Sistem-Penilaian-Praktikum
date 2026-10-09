from views import base_view as b

KOLOM = [
    ("id_nilai", "ID"),
    ("nim", "NIM"),                    # tampil jika controller melakukan JOIN
    ("nama_mahasiswa", "Mahasiswa"),
    ("judul_tugas", "Tugas"),
    ("nilai", "Nilai"),
    ("komentar", "Komentar"),
]
KOLOM_REKAP = [
    ("nim", "NIM"),
    ("nama_mahasiswa", "Mahasiswa"),
    ("jumlah_laporan", "Jml Laporan"),
    ("rata_rata", "Rata-rata"),
]


def tampilkan_menu():
    return b.menu_crud("MENU NILAI", tambahan={"5": "Rekap nilai per praktikum"})


def tampilkan_daftar(data):
    b.judul("DAFTAR NILAI")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL NILAI")
    b.tampil_detail(data, KOLOM)


def tampilkan_rekap(nama_praktikum, data):
    b.judul(f"REKAP NILAI - {nama_praktikum}")
    b.tampil_tabel(data, KOLOM_REKAP)


def input_tambah():
    b.judul("INPUT NILAI")
    return {
        "id_laporan": b.minta_id("ID laporan yang dinilai"),
        "nilai": b.input_angka("Nilai (0-100)", tipe=float, minimum=0, maksimum=100),
        "komentar": b.input_teks("Komentar (opsional)", wajib=False),
    }


def input_ubah(lama):
    b.judul("UBAH NILAI")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "nilai": b.input_angka("Nilai (0-100)", tipe=float, minimum=0, maksimum=100,
                               default=float(lama["nilai"])),
        "komentar": b.input_teks("Komentar", wajib=False, default=lama.get("komentar") or ""),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID nilai yang akan {aksi}")


def minta_id_praktikum():
    return b.minta_id("Masukkan ID praktikum untuk direkap")


def konfirmasi_hapus(data):
    return b.konfirmasi(f"Yakin hapus nilai ID {data['id_nilai']}?")