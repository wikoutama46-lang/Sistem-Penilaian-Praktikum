"""Uji tampilan CLI tanpa database (data sementara di memori).
Jalankan dari folder proyek:  python demo_cli.py
"""
from views_cli import mahasiswa_view as view

data = [
    {"id_mahasiswa": 1, "nim": "F5212530098",
     "nama": "Wiko Brenton Askelon Mangoli", "email": None},
]


def cari(id_):
    return next((d for d in data if d["id_mahasiswa"] == id_), None)


def main():
    while True:
        pilih = view.tampilkan_menu()
        if pilih == "1":
            view.tampilkan_daftar(data)
        elif pilih == "2":
            baru = view.input_tambah()
            baru["id_mahasiswa"] = max((d["id_mahasiswa"] for d in data), default=0) + 1
            data.append(baru)
        elif pilih == "3":
            lama = cari(view.minta_id("diubah"))
            if lama:
                lama.update(view.input_ubah(lama))
        elif pilih == "4":
            target = cari(view.minta_id("dihapus"))
            if target and view.konfirmasi_hapus(target):
                data.remove(target)
        elif pilih == "0":
            break


if __name__ == "__main__":
    main()