from views_cli import base_view as b

KOLOM = [("id_mahasiswa", "ID"), ("nim", "NIM"), ("nama", "Nama"), ("email", "Email")]


def tampilkan_menu():
    return b.menu_crud("MENU MAHASISWA")


def tampilkan_daftar(data):
    b.judul("DAFTAR MAHASISWA")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL MAHASISWA")
    b.tampil_detail(data, KOLOM)


def input_tambah():
    b.judul("TAMBAH MAHASISWA")
    return {
        "nim": b.input_teks("NIM"),
        "nama": b.input_teks("Nama"),
        "email": b.input_teks("Email (opsional)", wajib=False),
    }


def input_ubah(lama):
    b.judul("UBAH MAHASISWA")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "nim": b.input_teks("NIM", default=lama["nim"]),
        "nama": b.input_teks("Nama", default=lama["nama"]),
        "email": b.input_teks("Email", wajib=False, default=lama.get("email") or ""),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID mahasiswa yang akan {aksi}")


def konfirmasi_hapus(data):
    return b.konfirmasi(f"Yakin hapus mahasiswa '{data['nama']}' ({data['nim']})?")