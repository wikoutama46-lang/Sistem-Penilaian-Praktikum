
from datetime import datetime

LEBAR = 70
GARIS = "=" * LEBAR


# ---------- Pesan ----------
def judul(teks):
    print(f"\n{GARIS}\n{teks.center(LEBAR)}\n{GARIS}")


def pesan_sukses(teks):
    print(f"\n[BERHASIL] {teks}")


def pesan_error(teks):
    print(f"\n[ERROR] {teks}")


def pesan_info(teks):
    print(f"\n[INFO] {teks}")


def jeda():
    input("\nTekan Enter untuk melanjutkan...")


# ---------- Input ----------
def input_teks(label, wajib=True, default=None):
    """Jika default diisi (mode ubah), Enter kosong = pakai nilai lama."""
    petunjuk = f" [{default}]" if default not in (None, "") else ""
    while True:
        nilai = input(f"{label}{petunjuk}: ").strip()
        if not nilai and default is not None:
            return default
        if not nilai and wajib:
            pesan_error(f"{label} tidak boleh kosong.")
            continue
        return nilai


def input_angka(label, tipe=int, minimum=None, maksimum=None, default=None):
    petunjuk = f" [{default}]" if default is not None else ""
    while True:
        mentah = input(f"{label}{petunjuk}: ").strip()
        if not mentah and default is not None:
            return default
        try:
            nilai = tipe(mentah)
        except ValueError:
            pesan_error(f"{label} harus berupa angka.")
            continue
        if minimum is not None and nilai < minimum:
            pesan_error(f"{label} minimal {minimum}.")
            continue
        if maksimum is not None and nilai > maksimum:
            pesan_error(f"{label} maksimal {maksimum}.")
            continue
        return nilai


def input_tanggal(label, default=None, dengan_jam=False):
    """Mengembalikan string siap simpan ke MySQL (DATE atau DATETIME)."""
    fmt_input = "%Y-%m-%d %H:%M" if dengan_jam else "%Y-%m-%d"
    fmt_db = "%Y-%m-%d %H:%M:%S" if dengan_jam else "%Y-%m-%d"
    contoh = "YYYY-MM-DD HH:MM" if dengan_jam else "YYYY-MM-DD"
    petunjuk = f" [{default}]" if default else ""
    while True:
        mentah = input(f"{label} ({contoh}){petunjuk}: ").strip()
        if not mentah and default:
            return str(default)
        try:
            return datetime.strptime(mentah, fmt_input).strftime(fmt_db)
        except ValueError:
            pesan_error(f"Format salah. Gunakan {contoh}.")


def konfirmasi(pertanyaan):
    return input(f"{pertanyaan} (y/n): ").strip().lower() == "y"


def minta_id(label):
    return input_angka(label, tipe=int, minimum=1)


# ---------- Menu ----------
def menu_crud(nama, tambahan=None):
    """tambahan: dict {kode: label}, contoh {"5": "Rekap nilai"}."""
    judul(nama)
    print("1. Lihat data")
    print("2. Tambah data")
    print("3. Ubah data")
    print("4. Hapus data")
    for kode, label in (tambahan or {}).items():
        print(f"{kode}. {label}")
    print("0. Kembali")
    return input("\nPilih menu: ").strip()


# ---------- Tabel ----------
def tampil_tabel(data, kolom):
    """
    data  : list of dict (hasil query dengan cursor dictionary=True)
    kolom : list of (key, header). Kolom yang key-nya tidak ada di data dilewati.
    """
    if not data:
        pesan_info("Data kosong.")
        return

    kolom = [(k, h) for k, h in kolom if any(k in baris for baris in data)]
    sel = lambda baris, k: "-" if baris.get(k) in (None, "") else str(baris.get(k))
    lebar = [
        max(len(h), *(len(sel(b, k)) for b in data)) for k, h in kolom
    ]
    lebar = [min(w, 30) for w in lebar]  # potong teks panjang

    def potong(teks, w):
        return teks if len(teks) <= w else teks[: w - 3] + "..."

    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"
    print(garis)
    print("| " + " | ".join(h.ljust(w) for (_, h), w in zip(kolom, lebar)) + " |")
    print(garis)
    for baris in data:
        print("| " + " | ".join(
            potong(sel(baris, k), w).ljust(w) for (k, _), w in zip(kolom, lebar)
        ) + " |")
    print(garis)
    print(f"Total: {len(data)} data")


def tampil_detail(data, kolom):
    for key, label in kolom:
        nilai = "-" if data.get(key) in (None, "") else data.get(key)
        print(f"{label:<18}: {nilai}")