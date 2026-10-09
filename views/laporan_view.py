"""View Laporan (tampilan console). Tidak mengakses database."""

def _judul(teks):
    print("\n" + "=" * 60)
    print(teks.center(60))
    print("=" * 60)

def _menu(nama, tambahan=None):
    _judul(nama)
    print("1. Lihat data")
    print("2. Tambah data")
    print("3. Ubah data")
    print("4. Hapus data")
    for kode, label in (tambahan or {}).items():
        print(f"{kode}. {label}")
    print("0. Kembali")
    return input("\nPilih menu: ").strip()

def _input_teks(label, wajib=True, default=None):
    """Jika default diisi (mode ubah), Enter kosong = pakai nilai lama."""
    petunjuk = f" [{default}]" if default not in (None, "") else ""
    while True:
        nilai = input(f"{label}{petunjuk}: ").strip()
        if not nilai and default is not None:
            return default
        if not nilai and wajib:
            print(f"[ERROR] {label} tidak boleh kosong.")
            continue
        return nilai

def _tabel(data, kolom):
    """data: list of dict. kolom: list (key, header). Kolom tanpa data dilewati."""
    if not data:
        print("\n[INFO] Data kosong.")
        return
    kolom = [(k, h) for k, h in kolom if any(k in baris for baris in data)]
    teks = lambda baris, k: "-" if baris.get(k) in (None, "") else str(baris.get(k))
    lebar = [min(max(len(h), *(len(teks(b, k)) for b in data)), 30) for k, h in kolom]
    potong = lambda t, w: t if len(t) <= w else t[: w - 3] + "..."
    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"
    print(garis)
    print("| " + " | ".join(h.ljust(w) for (_, h), w in zip(kolom, lebar)) + " |")
    print(garis)
    for baris in data:
        print("| " + " | ".join(
            potong(teks(baris, k), w).ljust(w) for (k, _), w in zip(kolom, lebar)
        ) + " |")
    print(garis)
    print(f"Total: {len(data)} data")


def _detail(data, kolom):
    for key, label in kolom:
        nilai = "-" if data.get(key) in (None, "") else data.get(key)
        print(f"{label:<18}: {nilai}")

def _konfirmasi(pertanyaan):
    return input(f"{pertanyaan} (y/n): ").strip().lower() == "y"

def _input_angka(label, tipe=int, minimum=None, maksimum=None, default=None):
    petunjuk = f" [{default}]" if default is not None else ""
    while True:
        mentah = input(f"{label}{petunjuk}: ").strip()
        if not mentah and default is not None:
            return default
        try:
            nilai = tipe(mentah)
        except ValueError:
            print(f"[ERROR] {label} harus berupa angka.")
            continue
        if minimum is not None and nilai < minimum:
            print(f"[ERROR] {label} minimal {minimum}.")
            continue
        if maksimum is not None and nilai > maksimum:
            print(f"[ERROR] {label} maksimal {maksimum}.")
            continue
        return nilai


# ============ FUNGSI YANG DIPAKAI CONTROLLER ============

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
    return _menu("MENU LAPORAN")


def tampilkan_daftar(data):
    _judul("DAFTAR LAPORAN")
    _tabel(data, KOLOM)


def tampilkan_detail(data):
    _judul("DETAIL LAPORAN")
    _detail(data, KOLOM_DETAIL)


def input_tambah():
    _judul("TAMBAH LAPORAN")
    return {
        "id_tugas": _input_angka("ID tugas", minimum=1),
        "id_mahasiswa": _input_angka("ID mahasiswa", minimum=1),
        "file_laporan": _input_teks("Nama/path file laporan"),
        "catatan": _input_teks("Catatan (opsional)", wajib=False),
    }


def input_ubah(lama):
    _judul("UBAH LAPORAN")
    print("(Tekan Enter untuk mempertahankan nilai lama)")
    return {
        "id_tugas": _input_angka("ID tugas", minimum=1, default=lama["id_tugas"]),
        "id_mahasiswa": _input_angka("ID mahasiswa", minimum=1, default=lama["id_mahasiswa"]),
        "file_laporan": _input_teks("Nama/path file laporan", default=lama["file_laporan"]),
        "catatan": _input_teks("Catatan", wajib=False, default=lama.get("catatan") or ""),
    }


def minta_id(aksi="dipilih"):
    return _input_angka(f"Masukkan ID laporan yang akan {aksi}", minimum=1)


def konfirmasi_hapus(data):
    return _konfirmasi(f"Yakin hapus laporan ID {data['id_laporan']}? Nilainya ikut terhapus")
