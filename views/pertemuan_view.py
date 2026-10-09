from views import base_view as b

KOLOM = [
    ("id_pertemuan", "ID"),
    ("nama_praktikum", "Praktikum"),   # tampil jika controller melakukan JOIN
    ("pertemuan_ke", "Pertemuan"),
    ("topik", "Topik"),
    ("tanggal", "Tanggal"),
]


def tampilkan_menu():
    return b.menu_crud("MENU PERTEMUAN")


def tampilkan_daftar(data):
    b.judul("DAFTAR PERTEMUAN")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL PERTEMUAN")
    b.tampil_detail(data, KOLOM)


def input_tambah():
    """Controller sebaiknya menampilkan daftar praktikum dulu agar ID mudah dipilih."""
    b.judul("TAMBAH PERTEMUAN")
    return {
        "id_praktikum": b.minta_id("ID praktikum"),
        "pertemuan_ke": b.input_angka("Pertemuan ke-", minimum=1),
        "topik": b.input_teks("Topik"),
        "tanggal": b.input_tanggal("Tanggal"),
    }


def input_ubah(lama):
    b.judul("UBAH PERTEMUAN")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "id_praktikum": b.input_angka("ID praktikum", minimum=1, default=lama["id_praktikum"]),
        "pertemuan_ke": b.input_angka("Pertemuan ke-", minimum=1, default=lama["pertemuan_ke"]),
        "topik": b.input_teks("Topik", default=lama["topik"]),
        "tanggal": b.input_tanggal("Tanggal", default=lama["tanggal"]),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID pertemuan yang akan {aksi}")


def konfirmasi_hapus(data):
    return b.konfirmasi(
        f"Yakin hapus pertemuan ke-{data['pertemuan_ke']} ('{data['topik']}')?"
    )