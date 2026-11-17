"""Unit test perhitungan statistik Dashboard (tanpa MySQL dan tanpa tampilan)."""
from datetime import date, datetime
from decimal import Decimal

from controllers.statistik import (BATAS_LULUS, angka, grade_dari, hitung_statistik)


def baris_nilai(nim, nama, praktikum, akhir):
    return {"nim": nim, "nama": nama, "nama_praktikum": praktikum, "nilai_akhir": akhir}


# ---------- fungsi dasar ----------
def test_angka_menerima_berbagai_bentuk():
    assert angka(80) == 80.0
    assert angka("72,5") == 72.5
    assert angka(Decimal("90.00")) == 90.0
    assert angka(None) is None
    assert angka("") is None
    assert angka("abc") is None
    assert angka(float("nan")) is None


def test_grade_dari_batas():
    assert grade_dari(100) == "A"
    assert grade_dari(85) == "A"
    assert grade_dari(84.99) == "B"
    assert grade_dari(70) == "B"
    assert grade_dari(60) == "C"
    assert grade_dari(50) == "D"
    assert grade_dari(49.9) == "E"
    assert grade_dari(0) == "E"


# ---------- data kosong ----------
def test_data_kosong_tidak_error():
    stat = hitung_statistik({})
    assert stat["kelas"] == []
    assert stat["grade"] == []
    assert stat["rata_praktikum"] == []
    assert stat["ketuntasan"] is None
    assert stat["laporan"] is None
    assert stat["aktivitas"] is None
    assert stat["tren"] == []
    assert stat["peringkat"] == []


# ---------- tiap statistik ----------
def test_mahasiswa_per_kelas_terurut_dan_kelas_kosong():
    data = {"mahasiswa": [{"kelas": "C"}, {"kelas": "A"}, {"kelas": "C"}, {"kelas": ""}, {}]}
    assert hitung_statistik(data)["kelas"] == [("-", 2), ("A", 1), ("C", 2)]


def test_distribusi_grade_selalu_lengkap_a_sampai_e():
    data = {"nilai": [baris_nilai("1", "A", "P", 90), baris_nilai("2", "B", "P", 72),
                      baris_nilai("3", "C", "P", 30)]}
    grade = hitung_statistik(data)["grade"]
    assert [g["grade"] for g in grade] == ["A", "B", "C", "D", "E"]
    assert [g["jumlah"] for g in grade] == [1, 1, 0, 0, 1]
    assert grade[0]["batas"].endswith("85")
    assert grade[-1]["batas"].startswith("<")


def test_nilai_akhir_kosong_diabaikan():
    data = {"nilai": [baris_nilai("1", "A", "P", None), baris_nilai("2", "B", "P", ""),
                      baris_nilai("3", "C", "P", 80)]}
    stat = hitung_statistik(data)
    assert stat["ketuntasan"]["total"] == 1
    assert stat["rata_praktikum"] == [("P", 80.0)]


def test_rata_rata_per_praktikum_terurut_menurun():
    data = {"nilai": [baris_nilai("1", "A", "Basis Data", 60), baris_nilai("2", "B", "Basis Data", 70),
                      baris_nilai("1", "A", "RPL", 90)]}
    assert hitung_statistik(data)["rata_praktikum"] == [("RPL", 90.0), ("Basis Data", 65.0)]


def test_ketuntasan():
    data = {"nilai": [baris_nilai("1", "A", "P", 90), baris_nilai("2", "B", "P", BATAS_LULUS),
                      baris_nilai("3", "C", "P", 40), baris_nilai("4", "D", "P", 59.9)]}
    k = hitung_statistik(data)["ketuntasan"]
    assert (k["lulus"], k["total"], k["persen"]) == (2, 4, 50)
    assert k["rata"] == 62.5
    assert k["batas"] == BATAS_LULUS


def test_status_laporan():
    data = {"laporan": [{"nilai_laporan": 80}, {"nilai_laporan": None}, {"nilai_laporan": ""},
                        {"nilai_laporan": Decimal("0")}]}
    lap = hitung_statistik(data)["laporan"]
    assert (lap["dinilai"], lap["belum"], lap["persen"]) == (2, 2, 50)


def test_aktivitas_gabungan_pertemuan_dan_tugas():
    data = {"pertemuan": [{"nama_praktikum": "RPL"}, {"nama_praktikum": "RPL"},
                          {"nama_praktikum": "BD"}],
            "tugas": [{"nama_praktikum": "RPL"}, {"nama_praktikum": "Web"}]}
    akt = hitung_statistik(data)["aktivitas"]
    assert akt["label"] == ["BD", "RPL", "Web"]
    assert akt["seri"] == [("Pertemuan", [1, 2, 0]), ("Tugas", [0, 1, 1])]


def test_aktivitas_hanya_tugas_untuk_peran_tanpa_modul_pertemuan():
    akt = hitung_statistik({"tugas": [{"nama_praktikum": "RPL"}]})["aktivitas"]
    assert akt["seri"] == [("Tugas", [1])]


def test_tren_per_bulan_terurut_kronologis_dan_menerima_date():
    data = {"pertemuan": [{"tanggal": "2026-10-06"}, {"tanggal": date(2026, 9, 1)},
                          {"tanggal": datetime(2026, 9, 8, 10, 0)}, {"tanggal": "2025-12-30"},
                          {"tanggal": "tidak valid"}, {"tanggal": None}]}
    assert hitung_statistik(data)["tren"] == [("Des 25", 1), ("Sep 26", 2), ("Okt 26", 1)]


def test_peringkat_rata_rata_per_mahasiswa_maksimal_lima():
    nilai = [baris_nilai(str(i), f"Mhs{i}", "P", 50 + i) for i in range(8)]
    nilai.append(baris_nilai("7", "Mhs7", "Q", 100))     # Mhs7 rata-rata (57 + 100) / 2 = 78,5
    peringkat = hitung_statistik({"nilai": nilai})["peringkat"]
    assert len(peringkat) == 5
    assert peringkat[0] == ("Mhs7", 78.5)
    assert [n for _, n in peringkat] == sorted([n for _, n in peringkat], reverse=True)
