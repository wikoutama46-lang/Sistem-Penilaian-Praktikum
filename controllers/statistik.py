"""Perhitungan statistik untuk grafik Dashboard.

Murni Python (tanpa tampilan dan tanpa database), sehingga mudah diuji.
Masukan : dict {kunci_modul: [baris, ...]} sesuai data yang boleh dilihat pengguna.
Keluaran: dict berisi data siap gambar untuk tiap grafik. Modul yang datanya
          kosong menghasilkan nilai kosong (None atau list kosong).
"""
import math
from collections import Counter, OrderedDict

BATAS_LULUS = 60                       # nilai akhir minimal dinyatakan tuntas
GRADE = (("A", 85), ("B", 70), ("C", 60), ("D", 50), ("E", 0))
JUMLAH_PERINGKAT = 5
NAMA_BULAN = ("Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
              "Jul", "Agu", "Sep", "Okt", "Nov", "Des")


def angka(nilai):
    """Ubah ke float. None, teks kosong, atau bukan angka -> None."""
    if nilai is None or str(nilai).strip() == "":
        return None
    try:
        hasil = float(str(nilai).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None
    return None if math.isnan(hasil) else hasil


def grade_dari(nilai):
    for huruf, batas in GRADE:
        if nilai >= batas:
            return huruf
    return GRADE[-1][0]


def _rata(daftar):
    return round(sum(daftar) / len(daftar), 1) if daftar else None


def _bulan(tanggal):
    """(tahun, bulan) dari date/datetime atau teks 'YYYY-MM-DD'. Tidak valid -> None."""
    if tanggal is None:
        return None
    if hasattr(tanggal, "year") and hasattr(tanggal, "month"):
        return tanggal.year, tanggal.month
    try:
        tahun, bulan = str(tanggal).strip()[:7].split("-")
        tahun, bulan = int(tahun), int(bulan)
    except ValueError:
        return None
    return (tahun, bulan) if 1 <= bulan <= 12 else None


def _kelas(baris):
    per_kelas = Counter((str(b.get("kelas") or "").strip() or "-") for b in baris)
    return sorted(per_kelas.items())


def _grade(nilai_akhir):
    """Jumlah nilai per grade, selalu lengkap A-E (yang kosong bernilai 0)."""
    if not nilai_akhir:
        return []
    jumlah = Counter(grade_dari(n) for n in nilai_akhir)
    daftar = []
    for i, (huruf, batas) in enumerate(GRADE):
        if i == len(GRADE) - 1:
            keterangan = f"< {GRADE[i - 1][1]}"
        else:
            keterangan = f"\u2265 {batas}"
        daftar.append({"grade": huruf, "batas": keterangan, "jumlah": jumlah.get(huruf, 0)})
    return daftar


def _rata_praktikum(baris_nilai):
    kumpulan = OrderedDict()
    for b in baris_nilai:
        n = angka(b.get("nilai_akhir"))
        if n is not None:
            kumpulan.setdefault(str(b.get("nama_praktikum") or "-"), []).append(n)
    hasil = [(nama, _rata(v)) for nama, v in kumpulan.items()]
    return sorted(hasil, key=lambda x: (-x[1], x[0]))


def _ketuntasan(nilai_akhir):
    if not nilai_akhir:
        return None
    lulus = sum(1 for n in nilai_akhir if n >= BATAS_LULUS)
    total = len(nilai_akhir)
    return {"persen": round(lulus * 100 / total), "lulus": lulus, "total": total,
            "rata": _rata(nilai_akhir), "batas": BATAS_LULUS}


def _laporan(baris):
    if not baris:
        return None
    dinilai = sum(1 for b in baris if angka(b.get("nilai_laporan")) is not None)
    total = len(baris)
    return {"dinilai": dinilai, "belum": total - dinilai,
            "persen": round(dinilai * 100 / total)}


def _aktivitas(pertemuan, tugas):
    per_pertemuan = Counter(str(b.get("nama_praktikum") or "-") for b in pertemuan)
    per_tugas = Counter(str(b.get("nama_praktikum") or "-") for b in tugas)
    nama = sorted(set(per_pertemuan) | set(per_tugas))
    if not nama:
        return None
    seri = []
    if pertemuan:
        seri.append(("Pertemuan", [per_pertemuan.get(n, 0) for n in nama]))
    if tugas:
        seri.append(("Tugas", [per_tugas.get(n, 0) for n in nama]))
    return {"label": nama, "seri": seri}


def _tren(pertemuan):
    per_bulan = Counter(b for b in (_bulan(p.get("tanggal")) for p in pertemuan) if b)
    return [(f"{NAMA_BULAN[bln - 1]} {thn % 100:02d}", per_bulan[(thn, bln)])
            for thn, bln in sorted(per_bulan)]


def _peringkat(baris_nilai):
    """Rata-rata nilai akhir per mahasiswa (NIM), diambil lima tertinggi."""
    kumpulan = OrderedDict()
    for b in baris_nilai:
        n = angka(b.get("nilai_akhir"))
        if n is None:
            continue
        kunci = str(b.get("nim") or b.get("nama") or "-")
        nama = str(b.get("nama") or kunci)
        kumpulan.setdefault(kunci, (nama, []))[1].append(n)
    hasil = [(nama, _rata(v)) for nama, v in kumpulan.values()]
    hasil.sort(key=lambda x: (-x[1], x[0]))
    return hasil[:JUMLAH_PERINGKAT]


def hitung_statistik(data):
    """Hitung seluruh statistik grafik Dashboard dari data modul yang boleh dilihat."""
    mahasiswa = data.get("mahasiswa") or []
    pertemuan = data.get("pertemuan") or []
    tugas = data.get("tugas") or []
    laporan = data.get("laporan") or []
    nilai = data.get("nilai") or []
    nilai_akhir = [n for n in (angka(b.get("nilai_akhir")) for b in nilai) if n is not None]

    return {
        "kelas": _kelas(mahasiswa),
        "grade": _grade(nilai_akhir),
        "rata_praktikum": _rata_praktikum(nilai),
        "ketuntasan": _ketuntasan(nilai_akhir),
        "laporan": _laporan(laporan),
        "aktivitas": _aktivitas(pertemuan, tugas),
        "tren": _tren(pertemuan),
        "peringkat": _peringkat(nilai),
    }
