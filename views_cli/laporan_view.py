from views_cli import base_view as b

KOLOM = [
    ("id_laporan", "ID"),
    ("nim", "NIM"),                    # tampil jika controller melakukan JOIN
    ("nama_mahasiswa", "Mahasiswa"),
    ("judul_tugas", "Tugas"),
    ("file_laporan", "File"),
    ("tanggal_kumpul", "Dikumpulkan"),
]
KOLOM_DETAIL = KOLOM + [("catatan", "Catatan")]


def tampilkan_menu():
    return b.menu_crud("MENU LAPORAN")


def tampilkan_daftar(data):
    b.judul("DAFTAR LAPORAN")
    b.tampil_tabel(data, KOLOM)


def tampilkan_detail(data):
    b.judul("DETAIL LAPORAN")
    b.tampil_detail(data, KOLOM_DETAIL)


def input_tambah():
    b.judul("TAMBAH LAPORAN")
    return {
        "id_tugas": b.minta_id("ID tugas"),
        "id_mahasiswa": b.minta_id("ID mahasiswa"),
        "file_laporan": b.input_teks("Nama/path file laporan"),
        "catatan": b.input_teks("Catatan (opsional)", wajib=False),
    }


def input_ubah(lama):
    b.judul("UBAH LAPORAN")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "id_tugas": b.input_angka("ID tugas", minimum=1, default=lama["id_tugas"]),
        "id_mahasiswa": b.input_angka("ID mahasiswa", minimum=1, default=lama["id_mahasiswa"]),
        "file_laporan": b.input_teks("Nama/path file laporan", default=lama["file_laporan"]),
        "catatan": b.input_teks("Catatan", wajib=False, default=lama.get("catatan") or ""),
    }


def minta_id(aksi="dipilih"):
    return b.minta_id(f"Masukkan ID laporan yang akan {aksi}")


def konfirmasi_hapus(data):
    return b.konfirmasi(f"Yakin hapus laporan ID {data['id_laporan']}? Nilainya ikut terhapus")