from views_cli import base_view as b

KOLOM = [
    ("id_praktikum", "ID"),
    ("kode", "Kode"),
    ("nama", "Nama Praktikum"),
    ("semester", "Semester"),
]


def tampilkan_menu():
    return b.menu_crud("MENU PRAKTIKUM")


def tampilkan_daftar(data):
    b.judul("DAFTAR PRAKTIKUM")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL PRAKTIKUM")
    b.tampil_detail(data, KOLOM)


def input_tambah():
    b.judul("TAMBAH PRAKTIKUM")
    return {
        "kode": b.input_teks("Kode praktikum"),
        "nama": b.input_teks("Nama praktikum"),
        "semester": b.input_teks("Semester (contoh: Ganjil 2026/2027)"),
    }


def input_ubah(lama):
    b.judul("UBAH PRAKTIKUM")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "kode": b.input_teks("Kode praktikum", default=lama["kode"]),
        "nama": b.input_teks("Nama praktikum", default=lama["nama"]),
        "semester": b.input_teks("Semester", default=lama["semester"]),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID praktikum yang akan {aksi}")


def konfirmasi_hapus(data):
    return b.konfirmasi(
        f"Yakin hapus praktikum '{data['nama']}'? Pertemuan terkait ikut terhapus"
    )