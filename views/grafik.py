"""Grafik untuk Dashboard, digambar langsung di tkinter Canvas.

Tanpa matplotlib maupun Pillow, jadi tidak menambah dependensi dan ukuran .exe tetap kecil.
Semua grafik:
  - beranimasi saat halaman tampil (batang tumbuh, donat menyapu, jarum gauge naik)
  - menyesuaikan ukuran jendela (digambar ulang saat ukuran berubah)
  - menampilkan tooltip saat kursor diarahkan ke batang, irisan, atau titik
  - menampilkan keadaan "Belum ada data" bila kosong

Kelas  : GrafikDonat, GrafikKolom, GrafikBatang, GrafikGauge, GrafikGaris
Pakai  : grafik = GrafikKolom(master); grafik.set_data(...); grafik.pack/grid(...)
View bersifat pasif: data sudah dihitung Controller (controllers/statistik.py).
"""
import math
import time
import tkinter as tk
from tkinter import font as tkfont

from views import tema as t

# ---------- Warna ----------
PALET = ["#2FB5CA", "#8B5CF6", "#F5A524", "#3BB78F", "#E5566D", "#4C6FFF", "#9AA3B8"]
WARNA_GRADE = {"A": "#3BB78F", "B": "#2FB5CA", "C": "#F5A524", "D": "#F07F3C", "E": "#C73E4A"}
EMAS, PERAK, PERUNGGU = "#F5A524", "#9AA3B8", "#C9854A"
HIJAU, KUNING, MERAH = "#3BB78F", "#F5A524", "#C73E4A"
GARIS_BANTU = "#E6E9F2"
TRACK = "#EEF0F7"
TEKS_SUMBU = t.PLACEHOLDER


# ---------- Fungsi bantu ----------
def ease_out(x):
    return 1 - (1 - x) ** 3


def campur(warna_a, warna_b, bobot):
    """Campur dua warna hex; bobot 0 -> a, 1 -> b."""
    a = [int(warna_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(warna_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * bobot) for i in range(3))


def fmt(n):
    """Angka bulat tanpa desimal, selain itu satu desimal berkoma (gaya Indonesia)."""
    if abs(n - round(n)) < 1e-9:
        return str(int(round(n)))
    return f"{n:.1f}".replace(".", ",")


def potong(teks, lebar, font):
    """Pangkas teks dengan elipsis agar muat dalam lebar piksel."""
    teks = str(teks)
    if lebar <= 0:
        return ""
    if font.measure(teks) <= lebar:
        return teks
    while teks and font.measure(teks + "\u2026") > lebar:
        teks = teks[:-1]
    return teks.rstrip() + "\u2026" if teks else ""


def skala_bagus(nilai_maks, jumlah=4, bulat=False):
    """Batas atas dan langkah sumbu yang 'enak dibaca'."""
    if nilai_maks <= 0:
        return 1, 1
    kasar = nilai_maks / jumlah
    pangkat = 10 ** math.floor(math.log10(kasar))
    langkah = pangkat * 10
    for faktor in (1, 2, 2.5, 5, 10):
        langkah = faktor * pangkat
        if langkah * jumlah >= nilai_maks:
            break
    if bulat:
        langkah = max(1, math.ceil(langkah))
    return math.ceil(nilai_maks / langkah - 1e-9) * langkah, langkah


def poligon_bulat(x1, y1, x2, y2, r, atas=True, bawah=True):
    """Titik persegi dengan sudut melengkung; atas/bawah memilih sisi yang dibulatkan."""
    r = max(0.0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    titik = []

    def busur(cx, cy, awal):
        for i in range(7):
            a = math.radians(awal + i * 15)
            titik.extend((cx + r * math.cos(a), cy + r * math.sin(a)))

    busur(x2 - r, y1 + r, -90) if atas else titik.extend((x2, y1))
    busur(x2 - r, y2 - r, 0) if bawah else titik.extend((x2, y2))
    busur(x1 + r, y2 - r, 90) if bawah else titik.extend((x1, y2))
    busur(x1 + r, y1 + r, 180) if atas else titik.extend((x1, y1))
    return titik


def kurva_halus(titik, langkah=10, tegang=0.25):
    """Kurva mulus (Hermite). Tangen vertikal dinolkan di puncak/lembah agar tidak melambung."""
    if len(titik) < 3:
        return list(titik)
    p = [titik[0]] + list(titik) + [titik[-1]]

    def tangen(a, b, c):
        mx, my = tegang * (c[0] - a[0]), tegang * (c[1] - a[1])
        if (b[1] - a[1]) * (c[1] - b[1]) <= 0:      # puncak, lembah, atau datar
            my = 0.0
        return mx, my

    hasil = []
    for i in range(1, len(p) - 2):
        p1, p2 = p[i], p[i + 1]
        m1, m2 = tangen(p[i - 1], p1, p2), tangen(p1, p2, p[i + 2])
        for s in range(langkah):
            u = s / langkah
            h00, h10 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u
            h01, h11 = -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
            hasil.append((h00 * p1[0] + h10 * m1[0] + h01 * p2[0] + h11 * m2[0],
                          h00 * p1[1] + h10 * m1[1] + h01 * p2[1] + h11 * m2[1]))
    hasil.append(titik[-1])
    return hasil


# ---------- Dasar ----------
class Grafik(tk.Canvas):
    TINGGI = 220
    DURASI_MS = 700

    def __init__(self, master, **kw):
        super().__init__(master, bg=t.PUTIH, highlightthickness=0, bd=0, **kw)
        self.k = max(1.0, self.winfo_fpixels("1i") / 96.0)     # skala layar (DPI)
        self.configure(height=self.px(self.TINGGI))
        self.f_kecil = tkfont.Font(family="Arial", size=-self.px(11))
        self.f_tebal = tkfont.Font(family="Arial", size=-self.px(11), weight="bold")
        self.f_sedang = tkfont.Font(family="Arial", size=-self.px(15), weight="bold")
        self.f_besar = tkfont.Font(family="Arial", size=-self.px(28), weight="bold")
        self.p = 1.0               # kemajuan animasi 0..1
        self._job = None
        self._t0 = 0.0
        self._hit = []             # daerah yang memunculkan tooltip
        self.bind("<Configure>", lambda e: self.gambar_ulang())
        self.bind("<Map>", lambda e: self.animasi())
        self.bind("<Motion>", self._gerak)
        self.bind("<Leave>", lambda e: self.delete("tip"))

    # ----- utilitas -----
    def px(self, v):
        return max(1, round(v * self.k))

    def kosong(self):
        return True

    def gambar(self, w, h):
        raise NotImplementedError

    # ----- siklus gambar -----
    def gambar_ulang(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 40 or h < 40:
            return
        self.delete("all")
        self._hit = []
        if self.kosong():
            self._gambar_kosong(w, h)
        else:
            self.gambar(w, h)

    def _gambar_kosong(self, w, h):
        cx, cy = w / 2, h / 2 - self.px(8)
        lebar, jarak = self.px(10), self.px(6)
        for i, tinggi in enumerate((16, 28, 22)):
            x = cx - 1.5 * lebar - jarak + i * (lebar + jarak)
            self.create_polygon(poligon_bulat(x, cy + self.px(14) - self.px(tinggi),
                                              x + lebar, cy + self.px(14), self.px(3)),
                                fill=TRACK, outline=TRACK)
        self.create_text(cx, cy + self.px(34), text="Belum ada data",
                         font=self.f_kecil, fill=t.TEKS_NONAKTIF)

    def animasi(self):
        self._batal()
        if self.kosong():
            return
        self._t0 = time.perf_counter()
        self._langkah()

    def _langkah(self):
        x = (time.perf_counter() - self._t0) * 1000 / self.DURASI_MS
        self.p = ease_out(min(1.0, x))
        self.gambar_ulang()
        if x < 1:
            self._job = self.after(16, self._langkah)
        else:
            self._job = None
            self.p = 1.0

    def _batal(self):
        if self._job:
            try:
                self.after_cancel(self._job)
            except tk.TclError:
                pass
            self._job = None

    def _terapkan_data(self):
        self._batal()
        self.p = 1.0
        self.gambar_ulang()

    # ----- tooltip -----
    def _gerak(self, e):
        self.delete("tip")
        teks = self._cari(e.x, e.y)
        if not teks:
            return
        pad = self.px(6)
        isi = self.create_text(0, 0, text=teks, font=self.f_tebal, fill=t.PUTIH,
                               anchor="nw", justify="left", tags="tip")
        x1, y1, x2, y2 = self.bbox(isi)
        lebar, tinggi = x2 - x1 + 2 * pad, y2 - y1 + 2 * pad
        x, y = e.x + self.px(12), e.y - tinggi - self.px(8)
        if x + lebar > self.winfo_width() - 2:
            x = e.x - lebar - self.px(12)
        if y < 2:
            y = e.y + self.px(14)
        x = max(2, x)
        self.coords(isi, x + pad, y + pad)
        latar = self.create_polygon(poligon_bulat(x, y, x + lebar, y + tinggi, self.px(6)),
                                    fill=t.NAVY, outline=t.NAVY, tags="tip")
        self.tag_lower(latar, isi)

    def _cari(self, x, y):
        for daerah in self._hit:
            jenis = daerah[0]
            if jenis == "kotak":
                _, x1, y1, x2, y2, teks = daerah
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return teks
            elif jenis == "donat":
                _, cx, cy, r_dalam, r_luar, irisan = daerah
                dx, dy = x - cx, y - cy
                jarak = math.hypot(dx, dy)
                if r_dalam <= jarak <= r_luar:
                    sudut = math.degrees(math.atan2(dx, -dy)) % 360
                    for awal, akhir, teks in irisan:
                        if awal <= sudut < akhir:
                            return teks
            elif jenis == "titik":
                _, px_, py_, teks = daerah
                if abs(x - px_) <= self.px(18) and abs(y - py_) <= self.px(40):
                    return teks
        return None


# ---------- Donat ----------
class GrafikDonat(Grafik):
    """Donat dengan legenda. data: [(label, jumlah)]; tengah: (teks besar, teks kecil)."""
    MAKS_LEGENDA = 6

    def set_data(self, data, tengah=None):
        data = [(str(l), float(v)) for l, v in data]
        if len(data) > self.MAKS_LEGENDA:
            data.sort(key=lambda x: -x[1])
            sisa = sum(v for _, v in data[self.MAKS_LEGENDA - 1:])
            data = data[:self.MAKS_LEGENDA - 1] + [("Lainnya", sisa)]
        self.data, self.tengah = data, tengah
        self._terapkan_data()

    def kosong(self):
        return not getattr(self, "data", None) or sum(v for _, v in self.data) <= 0

    def gambar(self, w, h):
        total = sum(v for _, v in self.data)
        pad = self.px(14)
        garis_tengah = min(h - 2 * pad, w * 0.44)
        cx, cy = pad + garis_tengah / 2, h / 2
        tebal = garis_tengah * 0.2
        r_luar = garis_tengah / 2
        r_tengah = r_luar - tebal / 2
        kotak = (cx - r_tengah, cy - r_tengah, cx + r_tengah, cy + r_tengah)

        self.create_oval(*kotak, outline=TRACK, width=tebal)
        acum, irisan = 0.0, []
        beberapa = sum(1 for _, v in self.data if v > 0) > 1
        for i, (label, nilai) in enumerate(self.data):
            if nilai <= 0:
                continue
            warna = PALET[i % len(PALET)]
            frac = nilai / total
            sapuan = frac * 360
            jeda = 2.0 if beberapa else 0.0
            tampak = max(0.1, (sapuan - jeda)) * self.p
            if frac > 0.9995:
                self.create_oval(*kotak, outline=warna, width=tebal)
            else:
                self.create_arc(*kotak, start=90 - (acum * 360 + jeda / 2), extent=-tampak,
                                style="arc", outline=warna, width=tebal)
            irisan.append((acum * 360, (acum + frac) * 360,
                           f"{label}\n{fmt(nilai)} ({frac * 100:.0f}%)"))
            acum += frac
        self._hit.append(("donat", cx, cy, r_luar - tebal, r_luar, irisan))

        if self.tengah:
            self.create_text(cx, cy - self.px(7), text=self.tengah[0], font=self.f_besar,
                             fill=t.NAVY)
            self.create_text(cx, cy + self.px(16), text=self.tengah[1], font=self.f_kecil,
                             fill=TEKS_SUMBU)

        # legenda
        x0 = cx + r_luar + self.px(26)
        x1 = w - pad
        baris = self.px(26)
        y = cy - baris * len(self.data) / 2 + baris / 2
        for i, (label, nilai) in enumerate(self.data):
            warna = PALET[i % len(PALET)]
            kotak_l = self.px(10)
            self.create_polygon(poligon_bulat(x0, y - kotak_l / 2, x0 + kotak_l, y + kotak_l / 2,
                                              self.px(3)), fill=warna, outline=warna)
            nilai_teks = f"{fmt(nilai)}  \u00b7  {nilai / total * 100:.0f}%"
            lebar_nilai = self.f_kecil.measure(nilai_teks)
            self.create_text(x1, y, text=nilai_teks, anchor="e", font=self.f_kecil, fill=TEKS_SUMBU)
            self.create_text(x0 + kotak_l + self.px(8), y, anchor="w", font=self.f_tebal,
                             text=potong(label, x1 - lebar_nilai - x0 - kotak_l - self.px(18),
                                         self.f_tebal), fill=t.NAVY)
            y += baris


# ---------- Kolom ----------
class GrafikKolom(Grafik):
    """Kolom vertikal satu atau banyak seri.

    label : [str]            nama tiap kelompok pada sumbu X
    seri  : [(nama, [nilai], warna atau [warna per kelompok])]
    """

    def set_data(self, label, seri, bulat=True):
        self.label, self.seri, self.bulat = list(label), list(seri), bulat
        self.data = bool(self.label)
        self._terapkan_data()

    def kosong(self):
        seri = getattr(self, "seri", None)
        return not seri or not any(v for _, nilai, _ in seri for v in nilai)

    def gambar(self, w, h):
        banyak_seri = len(self.seri)
        ada_legenda = banyak_seri > 1
        kiri, kanan = self.px(34), self.px(12)
        atas = self.px(44) if ada_legenda else self.px(26)
        bawah = self.px(28)
        x0, x1, y0, y1 = kiri, w - kanan, atas, h - bawah
        maks = max(v for _, nilai, _ in self.seri for v in nilai)
        batas, langkah = skala_bagus(maks, 4, self.bulat)

        # garis bantu + angka sumbu Y
        v = 0
        while v <= batas + 1e-9:
            y = y1 - (v / batas) * (y1 - y0)
            self.create_line(x0, y, x1, y, fill=GARIS_BANTU if v else "#CBD0E0")
            self.create_text(x0 - self.px(6), y, text=fmt(v), anchor="e",
                             font=self.f_kecil, fill=TEKS_SUMBU)
            v += langkah

        n = len(self.label)
        slot = (x1 - x0) / n
        lebar_kel = min(slot * 0.72, self.px(56) * banyak_seri)
        jarak = self.px(3)
        lebar_bar = (lebar_kel - jarak * (banyak_seri - 1)) / banyak_seri
        for i, nama_label in enumerate(self.label):
            kiri_kel = x0 + slot * i + (slot - lebar_kel) / 2
            for s, (nama, nilai, warna) in enumerate(self.seri):
                nilai_i = nilai[i]
                warna_i = warna[i] if isinstance(warna, (list, tuple)) else warna
                bx1 = kiri_kel + s * (lebar_bar + jarak)
                bx2 = bx1 + lebar_bar
                tinggi = (nilai_i / batas) * (y1 - y0) * self.p
                if nilai_i > 0:
                    by1 = y1 - max(tinggi, 1)
                    self.create_polygon(poligon_bulat(bx1, by1, bx2, y1, min(self.px(6), lebar_bar / 2),
                                                      atas=True, bawah=False),
                                        fill=warna_i, outline=warna_i)
                    if lebar_bar >= self.px(16):
                        self.create_text((bx1 + bx2) / 2, by1 - self.px(9), text=fmt(nilai_i),
                                         font=self.f_tebal, fill=t.NAVY)
                judul = f"{nama_label}\n{nama}: {fmt(nilai_i)}" if banyak_seri > 1 \
                    else f"{nama_label}: {fmt(nilai_i)}"
                self._hit.append(("kotak", bx1, y0, bx2, y1, judul))
            self.create_text(x0 + slot * (i + 0.5), y1 + self.px(14), font=self.f_kecil,
                             text=potong(nama_label, slot - self.px(4), self.f_kecil), fill=TEKS_SUMBU)

        if ada_legenda:
            x = x1
            for nama, _, warna in reversed(self.seri):
                warna_l = warna[0] if isinstance(warna, (list, tuple)) else warna
                lebar_t = self.f_kecil.measure(nama)
                self.create_text(x, self.px(12), text=nama, anchor="e", font=self.f_kecil, fill=t.NAVY)
                x -= lebar_t + self.px(6)
                ukuran = self.px(10)
                self.create_polygon(poligon_bulat(x - ukuran, self.px(12) - ukuran / 2, x,
                                                  self.px(12) + ukuran / 2, self.px(3)),
                                    fill=warna_l, outline=warna_l)
                x -= ukuran + self.px(16)


# ---------- Batang horizontal ----------
class GrafikBatang(Grafik):
    """Batang horizontal. data: [(label, nilai)]. peringkat=True menampilkan nomor urut."""

    def set_data(self, data, maks=100, peringkat=False):
        self.data = [(str(l), float(v)) for l, v in data]
        self.maks, self.peringkat = maks, peringkat
        self._terapkan_data()

    def kosong(self):
        return not getattr(self, "data", None)

    def _warna(self, i):
        if self.peringkat:
            return (EMAS, PERAK, PERUNGGU)[i] if i < 3 else PALET[0]
        return PALET[i % len(PALET)]

    def gambar(self, w, h):
        pad = self.px(14)
        n = len(self.data)
        baris = min(self.px(34), (h - 2 * pad) / n)
        y = (h - baris * n) / 2
        lebar_nomor = self.px(26) if self.peringkat else 0
        lebar_label = min(max(self.f_tebal.measure(l) for l, _ in self.data) + self.px(8),
                          (w - 2 * pad) * 0.36)
        x_bar0 = pad + lebar_nomor + lebar_label + self.px(8)
        x_bar1 = w - pad - self.px(40)
        tebal = min(self.px(14), baris * 0.5)
        for i, (label, nilai) in enumerate(self.data):
            cy = y + baris * i + baris / 2
            warna = self._warna(i)
            if self.peringkat:
                r = self.px(10)
                self.create_oval(pad, cy - r, pad + 2 * r, cy + r, fill=warna, outline=warna)
                self.create_text(pad + r, cy, text=str(i + 1), font=self.f_tebal, fill=t.PUTIH)
            self.create_text(pad + lebar_nomor, cy, anchor="w", font=self.f_tebal, fill=t.NAVY,
                             text=potong(label, lebar_label, self.f_tebal))
            self.create_polygon(poligon_bulat(x_bar0, cy - tebal / 2, x_bar1, cy + tebal / 2, tebal / 2),
                                fill=TRACK, outline=TRACK)
            panjang = (x_bar1 - x_bar0) * min(1.0, nilai / self.maks) * self.p
            if panjang > 1:
                self.create_polygon(poligon_bulat(x_bar0, cy - tebal / 2, x_bar0 + max(panjang, tebal),
                                                  cy + tebal / 2, tebal / 2),
                                    fill=warna, outline=warna)
            self.create_text(w - pad, cy, text=fmt(nilai * self.p if self.p < 1 else nilai),
                             anchor="e", font=self.f_tebal, fill=t.NAVY)
            self._hit.append(("kotak", pad, cy - baris / 2, w - pad, cy + baris / 2,
                              f"{label}: {fmt(nilai)}"))


# ---------- Gauge ----------
class GrafikGauge(Grafik):
    """Busur setengah lingkaran untuk persentase.

    data: dict persen, lulus, total, rata   (None = belum ada data)
    """

    def set_data(self, data):
        self.data = data
        self._terapkan_data()

    def kosong(self):
        return not getattr(self, "data", None)

    @staticmethod
    def _warna(persen):
        return HIJAU if persen >= 75 else KUNING if persen >= 50 else MERAH

    def gambar(self, w, h):
        d = self.data
        pad = self.px(14)
        lebar_gauge = w * 0.58
        cx = pad + lebar_gauge / 2
        tebal = self.px(20)
        cy = h - pad - self.px(30)
        r_tengah = min(lebar_gauge / 2 - pad - tebal / 2, cy - pad - tebal / 2)
        kotak = (cx - r_tengah, cy - r_tengah, cx + r_tengah, cy + r_tengah)
        warna = self._warna(d["persen"])
        frac = d["persen"] / 100 * self.p

        self.create_arc(*kotak, start=0, extent=180, style="arc", outline=TRACK, width=tebal)
        for sx in (-r_tengah, r_tengah):
            self.create_oval(cx + sx - tebal / 2, cy - tebal / 2, cx + sx + tebal / 2, cy + tebal / 2,
                             fill=TRACK, outline=TRACK)
        if frac > 0:
            self.create_arc(*kotak, start=180, extent=-180 * frac, style="arc", outline=warna, width=tebal)
            self.create_oval(cx - r_tengah - tebal / 2, cy - tebal / 2, cx - r_tengah + tebal / 2,
                             cy + tebal / 2, fill=warna, outline=warna)
            a = math.radians(180 - 180 * frac)
            ex, ey = cx + r_tengah * math.cos(a), cy - r_tengah * math.sin(a)
            self.create_oval(ex - tebal / 2, ey - tebal / 2, ex + tebal / 2, ey + tebal / 2,
                             fill=warna, outline=warna)

        self.create_text(cx, cy - self.px(8), text=f"{d['persen'] * self.p:.0f}%", font=self.f_besar,
                         fill=t.NAVY, anchor="s")
        self.create_text(cx, cy - self.px(8), text="tuntas", font=self.f_kecil, fill=TEKS_SUMBU,
                         anchor="n")
        self.create_text(cx - r_tengah, cy + tebal / 2 + self.px(10), text="0%", font=self.f_kecil,
                         fill=TEKS_SUMBU)
        self.create_text(cx + r_tengah, cy + tebal / 2 + self.px(10), text="100%", font=self.f_kecil,
                         fill=TEKS_SUMBU)

        # statistik pendamping di sisi kanan
        x0, x1 = pad + lebar_gauge + self.px(6), w - pad
        butir = [("Rata-rata nilai akhir", fmt(d["rata"] if d["rata"] is not None else 0), t.NAVY),
                 (f"Tuntas (\u2265 {d.get('batas', 60)})", f"{d['lulus']} dari {d['total']}", HIJAU),
                 ("Belum tuntas", str(d["total"] - d["lulus"]), MERAH if d["total"] - d["lulus"] else TEKS_SUMBU)]
        tinggi_butir = (h - 2 * pad) / len(butir)
        for i, (judul, isi, warna_isi) in enumerate(butir):
            y = pad + tinggi_butir * i
            if i:
                self.create_line(x0, y, x1, y, fill=GARIS_BANTU)
            self.create_text(x0, y + tinggi_butir * 0.30, text=potong(judul, x1 - x0, self.f_kecil),
                             anchor="w", font=self.f_kecil, fill=TEKS_SUMBU)
            self.create_text(x0, y + tinggi_butir * 0.68, text=isi, anchor="w",
                             font=self.f_sedang, fill=warna_isi)


# ---------- Garis ----------
class GrafikGaris(Grafik):
    """Grafik garis berarea. data: [(label, nilai)]."""

    def set_data(self, data, warna=PALET[0]):
        self.data = [(str(l), float(v)) for l, v in data]
        self.warna = warna
        self._terapkan_data()

    def kosong(self):
        return not getattr(self, "data", None)

    def gambar(self, w, h):
        kiri, kanan, atas, bawah = self.px(34), self.px(22), self.px(22), self.px(28)
        x0, x1, y0, y1 = kiri, w - kanan, atas, h - bawah
        maks = max(v for _, v in self.data)
        batas, langkah = skala_bagus(maks, 4, True)

        v = 0
        while v <= batas + 1e-9:
            y = y1 - (v / batas) * (y1 - y0)
            self.create_line(x0, y, x1, y, fill=GARIS_BANTU if v else "#CBD0E0")
            self.create_text(x0 - self.px(6), y, text=fmt(v), anchor="e", font=self.f_kecil,
                             fill=TEKS_SUMBU)
            v += langkah

        n = len(self.data)
        if n == 1:
            xs = [(x0 + x1) / 2]
        else:
            sisi = self.px(14)
            xs = [x0 + sisi + (x1 - x0 - 2 * sisi) * i / (n - 1) for i in range(n)]
        ys = [y1 - (v / batas) * (y1 - y0) * self.p for _, v in self.data]
        titik = list(zip(xs, ys))

        if n > 1:
            mulus = [(x, min(max(y, y0 - self.px(4)), y1)) for x, y in kurva_halus(titik)]
            area = [(mulus[0][0], y1)] + mulus + [(mulus[-1][0], y1)]
            self.create_polygon([c for p in area for c in p], fill=campur(self.warna, "#FFFFFF", 0.82),
                                outline="")
            self.create_line([c for p in mulus for c in p], fill=self.warna, width=self.px(3),
                             capstyle="round", joinstyle="round")
        for (x, y), (label, nilai) in zip(titik, self.data):
            r = self.px(5)
            self.create_oval(x - r, y - r, x + r, y + r, fill=t.PUTIH, outline=self.warna, width=self.px(2))
            if n <= 8:
                self.create_text(x, y - self.px(14), text=fmt(nilai), font=self.f_tebal, fill=t.NAVY)
            self._hit.append(("titik", x, y, f"{label}: {fmt(nilai)}"))

        langkah_label = max(1, math.ceil(n * (self.f_kecil.measure("Mmm 00") + self.px(10)) / (x1 - x0)))
        for i, (label, _) in enumerate(self.data):
            if i % langkah_label == 0:
                self.create_text(xs[i], y1 + self.px(14), text=label, font=self.f_kecil, fill=TEKS_SUMBU)
