from views_cli import base_view as b

KOLOM = [
    ("id_tugas", "ID"),
    ("nama_praktikum", "Praktikum"),   # tampil jika controller melakukan JOIN
    ("pertemuan_ke", "Pertemuan"),
    ("nama_tugas", "Nama Tugas"),
    ("deadline", "Deadline"),
]


def tampilkan_menu():
    return b.menu_crud("MENU TUGAS")


def tampilkan_daftar(data):
    b.judul("DAFTAR TUGAS")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL TUGAS")
    b.tampil_detail(data, KOLOM)


def input_tambah():
    """Controller sebaiknya menampilkan daftar pertemuan dulu agar ID mudah dipilih."""
    b.judul("TAMBAH TUGAS")
    return {
        "id_pertemuan": b.minta_id("ID pertemuan"),
        "nama_tugas": b.input_teks("Nama tugas"),
        "deadline": b.input_tanggal("Deadline", dengan_jam=True),
    }


def input_ubah(lama):
    b.judul("UBAH TUGAS")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "id_pertemuan": b.input_angka("ID pertemuan", minimum=1, default=lama.get("id_pertemuan")),
        "nama_tugas": b.input_teks("Nama tugas", default=lama["nama_tugas"]),
        "deadline": b.input_tanggal("Deadline", default=lama["deadline"], dengan_jam=True),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID tugas yang akan {aksi}")


def konfirmasi_hapus(data):
    return b.konfirmasi(f"Yakin hapus tugas '{data['nama_tugas']}'?")
