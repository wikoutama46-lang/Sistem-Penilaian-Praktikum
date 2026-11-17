"""Uji tampilan GUI tanpa database dan tanpa Controller (data contoh di memori).
Jalankan dari folder proyek:  python demo_gui.py
Login: isi username dan password apa saja.
(Tampilan CLI tetap tersedia lewat:  python demo_cli.py)
"""
from controllers.statistik import hitung_statistik
from views.app_view import AplikasiView

def _mahasiswa():
    nama = ["Wiko Brenton", "Rofilla Ramadani", "Muhammad Fadhil", "Intan Anggraini", "Dewi Lestari",
            "Rizky Pratama", "Siti Aisyah", "Budi Santoso", "Nadia Putri", "Andi Saputra",
            "Maya Sari", "Fajar Nugroho"]
    return [{"id_mahasiswa": i + 1, "nim": f"F52125300{i + 10}", "nama": n,
             "kelas": "C" if i % 3 != 2 else ("A" if i % 2 else "B")} for i, n in enumerate(nama)]


PRAKTIKUM = ["Rekayasa Perangkat Lunak", "Basis Data", "Pemrograman Web", "Jaringan Komputer"]
MHS = _mahasiswa()
SKOR = [(90, 85, 100), (78, 80, 90), (88, 92, 95), (70, 65, 80), (55, 60, 70), (95, 90, 100),
        (62, 58, 75), (45, 50, 60), (82, 79, 85), (73, 70, 90), (66, 72, 80), (58, 49, 65)]


def _nilai():
    baris = []
    for i, m in enumerate(MHS):
        for j, prak in enumerate(PRAKTIKUM[:3]):
            t, l, h = SKOR[(i + j) % len(SKOR)]
            t, l = min(100, t + j * 2), max(0, l - j)
            baris.append({"id_nilai": len(baris) + 1, "nim": m["nim"], "nama": m["nama"],
                          "nama_praktikum": prak, "nilai_tugas": t, "nilai_laporan": l,
                          "nilai_kehadiran": h, "nilai_akhir": round(t * 0.4 + l * 0.4 + h * 0.2, 2)})
    return baris


BULAN = ["2026-08-04", "2026-08-18", "2026-09-01", "2026-09-08", "2026-09-22",
         "2026-10-06", "2026-10-13", "2026-10-27", "2026-11-03", "2026-11-10"]

DATA_CONTOH = {
    "mahasiswa": MHS,
    "praktikum": [{"id_praktikum": i + 1, "nama_praktikum": p, "asisten_dosen": f"Asisten {chr(65 + i)}"}
                  for i, p in enumerate(PRAKTIKUM)],
    "pertemuan": [{"id_pertemuan": i + 1, "nama_praktikum": PRAKTIKUM[i % 4], "pertemuan_ke": i // 4 + 1,
                   "tanggal": tgl} for i, tgl in enumerate(BULAN)],
    "tugas": [{"id_tugas": i + 1, "nama_praktikum": PRAKTIKUM[i % 3], "pertemuan_ke": i // 3 + 1,
               "nama_tugas": f"Tugas {i + 1}", "deadline": "2026-12-01 23:59:00"} for i in range(8)],
    "laporan": [{"id_laporan": i + 1, "nim": MHS[i % 12]["nim"], "nama": MHS[i % 12]["nama"],
                 "nama_praktikum": PRAKTIKUM[i % 3], "pertemuan_ke": 1,
                 "judul_laporan": f"Laporan {i + 1}", "nilai_laporan": 70 + i if i % 4 else None}
                for i in range(14)],
    "nilai": _nilai(),
}


def main():
    app = AplikasiView()
    app.dashboard.tampilkan_ringkasan({k: len(v) for k, v in DATA_CONTOH.items()})
    app.dashboard.tampilkan_grafik(hitung_statistik(DATA_CONTOH))
    app.on_modul_berubah = lambda kunci: app.daftar.tampilkan_data(DATA_CONTOH.get(kunci, []))
    app.mainloop()


if __name__ == "__main__":
    main()