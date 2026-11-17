"""Layar pembuka (splash) beranimasi untuk Sistem Penilaian Praktikum.

Hanya memakai tkinter bawaan Python (tanpa Pillow), digambar vektor di Canvas.

Urutan animasi (+- 2,8 detik):
  1. kaki-kaki chip (ungu) memanjang keluar
  2. badan chip (cyan) muncul membesar
  3. tanda centang tergambar, titik ungu muncul, riak cahaya menyebar
  4. teks "// SISTEM PENILAIAN" dan "Praktikum_" diketik, kursor berkedip
  5. bar kemajuan terisi sesuai pemuatan modul yang sebenarnya, lalu jendela memudar

Pemakaian (lihat app.py):
    hasil = tampilkan_splash(fungsi_muat)
    fungsi_muat(lapor) dijalankan di thread latar sambil animasi berjalan;
    lapor("teks status", pecahan_0_sampai_1) memperbarui status dan bar kemajuan.
"""
import math
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import font as tkfont

# ---------- Palet (diambil dari logo) ----------
WARNA_LATAR = "#070C16"
CYAN = "#22D3EE"
UNGU = "#8B5CF6"
CHIP_GELAP = "#0B1220"
GARIS_DALAM = "#135668"
TEKS_TERANG = "#F1F7FF"
TEKS_REDUP = "#5C6B84"
GARIS_JENDELA = "#16304A"

LEBAR, TINGGI = 640, 360          # ukuran dasar (piksel pada 100% skala layar)
DURASI_MIN_MS = 2800              # lama minimum splash; ubah bila ingin lebih singkat/lama
JUDUL_ATAS = "// SISTEM PENILAIAN"
JUDUL_UTAMA = "Praktikum"


# ---------- Utilitas umum ----------
def jalur_aset(*bagian):
    """Lokasi berkas aset, baik saat dijalankan dari kode sumber maupun dari .exe PyInstaller."""
    dasar = getattr(sys, "_MEIPASS", None)
    if dasar is None:
        dasar = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(dasar, "assets", *bagian)


def aktifkan_dpi_aware():
    """Agar splash tajam di layar dengan skala 125%/150% (Windows)."""
    if sys.platform.startswith("win"):
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def atur_id_aplikasi(app_id="kelompok04.sistempenilaianpraktikum"):
    """Agar ikon aplikasi (bukan ikon Python) muncul di taskbar Windows."""
    if sys.platform.startswith("win"):
        import ctypes
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass


def pasang_ikon(jendela):
    """Pasang icon.ico pada jendela utama. CustomTkinter menimpa ikon setelah ~200 ms,
    karena itu dipasang ulang sedikit setelahnya."""
    if not sys.platform.startswith("win"):
        return
    ico = jalur_aset("icon.ico")

    def _pasang():
        try:
            jendela.iconbitmap(ico)
        except Exception:
            pass
    jendela.after(300, _pasang)


def fade_in(jendela, durasi_ms=280, langkah=14):
    """Jendela utama muncul perlahan setelah splash menghilang."""
    try:
        jendela.attributes("-alpha", 0.0)
    except tk.TclError:
        return

    def _naik(i=1):
        try:
            jendela.attributes("-alpha", min(1.0, i / langkah))
            if i < langkah:
                jendela.after(max(1, durasi_ms // langkah), _naik, i + 1)
        except tk.TclError:
            pass
    jendela.after(30, _naik)


def _batas(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def _ease_out(x):
    return 1 - (1 - x) ** 3


def _ease_in_out(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def _ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def _campur(warna_a, warna_b, t):
    """Campur dua warna hex; t=0 -> a, t=1 -> b."""
    a = [int(warna_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(warna_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _pilih_font(root, kandidat, cadangan):
    ada = set(tkfont.families(root))
    return next((f for f in kandidat if f in ada), cadangan)


# ---------- Pemuat di thread latar ----------
class _Pemuat(threading.Thread):
    def __init__(self, fungsi):
        super().__init__(daemon=True)
        self._fungsi = fungsi
        self.teks = "Memulai ..."
        self.pecahan = 0.0
        self.selesai = False
        self.hasil = None
        self.galat = None

    def lapor(self, teks, pecahan):
        self.teks, self.pecahan = teks, _batas(pecahan)

    def run(self):
        try:
            self.hasil = self._fungsi(self.lapor)
        except BaseException as e:      # dibawa ke thread utama
            self.galat = e
        finally:
            self.selesai = True


# ---------- Jendela splash ----------
class SplashView:
    def __init__(self, pemuat, durasi_min_ms=DURASI_MIN_MS):
        aktifkan_dpi_aware()
        self.root = tk.Tk()
        self.pemuat = pemuat
        self.durasi = durasi_min_ms
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.configure(bg=WARNA_LATAR)
        try:
            self.root.attributes("-topmost", True)
        except tk.TclError:
            pass

        self.k = max(1.0, self.root.winfo_fpixels("1i") / 96.0)   # skala layar
        self.w, self.h = round(LEBAR * self.k), round(TINGGI * self.k)
        x = (self.root.winfo_screenwidth() - self.w) // 2
        y = (self.root.winfo_screenheight() - self.h) // 2 - round(20 * self.k)
        self.root.geometry(f"{self.w}x{self.h}+{x}+{max(0, y)}")

        self.c = tk.Canvas(self.root, width=self.w, height=self.h, bg=WARNA_LATAR,
                           highlightthickness=0, bd=0)
        self.c.pack()

        mono = _pilih_font(self.root, ("Cascadia Mono", "Consolas", "DejaVu Sans Mono",
                                       "Menlo", "Courier New"), "Courier")
        sans = _pilih_font(self.root, ("Segoe UI", "Arial", "Helvetica", "DejaVu Sans"), "Arial")
        self.f_atas = tkfont.Font(family=mono, size=-self.s(15))
        self.f_judul = tkfont.Font(family=sans, size=-self.s(54), weight="bold")
        self.f_kecil = tkfont.Font(family=mono, size=-self.s(11))
        self.f_footer = tkfont.Font(family=sans, size=-self.s(10))

        self.maju = 0.0           # nilai bar kemajuan yang ditampilkan
        self.mulai = None
        self.fade_langkah = 0
        self.hasil = None

        # lapisan statis (tidak digambar ulang tiap frame)
        self.c.create_rectangle(0, 0, self.w - 1, self.h - 1, outline=GARIS_JENDELA)
        self.c.create_text(self.w // 2, self.h - self.s(22), text="Kelompok 04  \u00b7  Kelas C  \u00b7  S1 Sistem Informasi",
                           fill=TEKS_REDUP, font=self.f_footer)

    def s(self, v):
        return round(v * self.k)

    # ---------- penggambaran ----------
    def _rrect(self, x1, y1, x2, y2, r, **kw):
        """Persegi bersudut melengkung halus (tiap sudut dibuat dari titik busur)."""
        r = max(0.0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
        titik = []
        for cx, cy, awal in ((x2 - r, y1 + r, -90), (x2 - r, y2 - r, 0),
                             (x1 + r, y2 - r, 90), (x1 + r, y1 + r, 180)):
            for i in range(9):
                a = math.radians(awal + i * 10)
                titik += [cx + r * math.cos(a), cy + r * math.sin(a)]
        return self.c.create_polygon(titik, tags="anim", **kw)

    def _chip(self, t):
        """Chip pada koordinat logo asli (pusat 0,0; badan +-183, ujung kaki +-281)."""
        c = self.c
        pusat_x, pusat_y = self.s(150), self.s(150)
        u = self.s(190) / 562.0                      # skala satuan logo -> piksel
        g = 0.55 + 0.45 * _ease_out_back(_batas((t - 150) / 600))
        U = u * g

        def X(v): return pusat_x + v * U
        def Y(v): return pusat_y + v * U

        # kaki chip (memanjang bergiliran)
        lebar_kaki = max(2, 22 * U)
        posisi = (-86.5, 0, 86.5)
        for i, d in enumerate(posisi):
            p = _ease_out(_batas((t - 40 * i) / 520))
            ujung = 150 + (281 - 150) * p
            for (x1, y1, x2, y2) in ((d, -150, d, -ujung), (d, 150, d, ujung),
                                     (-150, d, -ujung, d), (150, d, ujung, d)):
                c.create_line(X(x1), Y(y1), X(x2), Y(y2), fill=UNGU, width=lebar_kaki,
                              capstyle="round", tags="anim")

        if t < 150:
            return
        # badan chip
        self._rrect(X(-183), Y(-183), X(183), Y(183), 75 * U, fill=CYAN, outline=CYAN)
        self._rrect(X(-161), Y(-161), X(161), Y(161), 52 * U, fill=CHIP_GELAP, outline=CHIP_GELAP)
        self._rrect(X(-131), Y(-131), X(133), Y(133), 32 * U, fill="", outline=GARIS_DALAM,
                    width=max(1, 7 * U))

        # titik ungu
        pd = _batas((t - 1100) / 320)
        if pd > 0:
            r = 14 * U * _ease_out_back(pd)
            c.create_oval(X(-102) - r, Y(-102) - r, X(-102) + r, Y(-102) + r,
                          fill=UNGU, outline=UNGU, tags="anim")

        # tanda centang (tergambar bertahap)
        pc = _ease_in_out(_batas((t - 700) / 480))
        if pc > 0:
            a, b, d = (-91, 6), (-27, 70), (97, -75)
            s1, s2 = math.hypot(b[0] - a[0], b[1] - a[1]), math.hypot(d[0] - b[0], d[1] - b[1])
            jarak = pc * (s1 + s2)
            titik = [a]
            if jarak <= s1:
                f = jarak / s1
                titik.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
            else:
                f = (jarak - s1) / s2
                titik += [b, (b[0] + (d[0] - b[0]) * f, b[1] + (d[1] - b[1]) * f)]
            datar = [v for p in titik for v in (X(p[0]), Y(p[1]))]
            c.create_line(*datar, fill=CYAN, width=36 * U, capstyle="round",
                          joinstyle="round", tags="anim")

        # riak cahaya setelah centang selesai
        pr = _batas((t - 1150) / 750)
        if 0 < pr < 1:
            rr = (183 + 90 * _ease_out(pr)) * U
            c.create_oval(X(0) - rr, Y(0) - rr, X(0) + rr, Y(0) + rr,
                          outline=_campur(CYAN, WARNA_LATAR, pr), width=max(1, 3 * U * (1 - pr)),
                          tags="anim")

    def _teks(self, t):
        c = self.c
        x0 = self.s(270)
        # baris atas: diketik, tiap huruf ditempatkan dengan jarak tetap
        n = int(_batas((t - 900) / 34, 0, len(JUDUL_ATAS)))
        adv = self.f_atas.measure("M") + self.s(4)
        for i, ch in enumerate(JUDUL_ATAS[:n]):
            if ch != " ":
                c.create_text(x0 + i * adv, self.s(108), text=ch, fill=CYAN, anchor="w",
                              font=self.f_atas, tags="anim")
        # judul besar
        m = int(_batas((t - 1350) / 62, 0, len(JUDUL_UTAMA)))
        y_judul = self.s(158)
        teks = JUDUL_UTAMA[:m]
        if teks:
            c.create_text(x0 - self.s(2), y_judul, text=teks, fill=TEKS_TERANG, anchor="w",
                          font=self.f_judul, tags="anim")
        if t >= 1350:
            lebar_teks = self.f_judul.measure(teks) if teks else 0
            kedip = t < 1350 + 62 * len(JUDUL_UTAMA) + 200 or int((t - 1900) / 450) % 2 == 0
            if kedip:
                kx = x0 - self.s(2) + lebar_teks + self.s(6)
                base = y_judul + self.s(30)
                c.create_rectangle(kx, base, kx + self.s(34), base + self.s(6), fill=UNGU,
                                   outline=UNGU, tags="anim")

    def _bar(self, t, selesai_min):
        c = self.c
        x1, x2 = self.s(50), self.w - self.s(50)
        y = self.h - self.s(62)
        c.create_text(x1, y - self.s(14), text=self.pemuat.teks if not selesai_min else "Siap.",
                      fill=TEKS_REDUP, anchor="w", font=self.f_kecil, tags="anim")
        c.create_text(x2, y - self.s(14), text=f"{int(self.maju * 100):d}%", fill=TEKS_REDUP,
                      anchor="e", font=self.f_kecil, tags="anim")
        c.create_rectangle(x1, y, x2, y + self.s(4), fill="#0F1B2D", outline="", tags="anim")
        if self.maju > 0:
            xe = x1 + (x2 - x1) * self.maju
            c.create_rectangle(x1, y, xe, y + self.s(4), fill=CYAN, outline="", tags="anim")
            c.create_rectangle(max(x1, xe - self.s(18)), y, xe, y + self.s(4), fill=UNGU,
                               outline="", tags="anim")

    # ---------- siklus animasi ----------
    def _frame(self):
        t = (time.perf_counter() - self.mulai) * 1000.0
        waktu_cukup = t >= self.durasi
        # bar: dibatasi oleh waktu DAN pemuatan nyata, agar tidak penuh sebelum aplikasi siap
        nyata = 1.0 if self.pemuat.selesai else min(0.92, self.pemuat.pecahan)
        target = min(_batas(t / self.durasi), nyata)
        self.maju += (target - self.maju) * 0.18
        if abs(target - self.maju) < 0.004:
            self.maju = target

        self.c.delete("anim")
        self._chip(t)
        self._teks(t)
        self._bar(t, waktu_cukup and self.pemuat.selesai and self.maju >= 0.999)

        if waktu_cukup and self.pemuat.selesai and self.maju >= 0.999:
            self.root.after(160, self._pudar)
        else:
            self.root.after(15, self._frame)

    def _pudar(self):
        self.fade_langkah += 1
        try:
            self.root.attributes("-alpha", max(0.0, 1 - self.fade_langkah / 10))
        except tk.TclError:
            self.fade_langkah = 10
        if self.fade_langkah >= 10:
            self.root.destroy()
        else:
            self.root.after(22, self._pudar)

    def jalankan(self):
        self.root.deiconify()
        self.root.update()
        _tutup_splash_pyinstaller()
        self.pemuat.start()
        self.mulai = time.perf_counter()
        self._frame()
        self.root.mainloop()


def _tutup_splash_pyinstaller():
    """Tutup gambar statis bawaan PyInstaller (--splash) begitu splash beranimasi tampil."""
    try:
        import pyi_splash  # hanya ada di dalam .exe hasil PyInstaller
        pyi_splash.close()
    except Exception:
        pass


def tampilkan_splash(fungsi_muat, durasi_min_ms=DURASI_MIN_MS):
    """Tampilkan splash beranimasi sambil menjalankan `fungsi_muat(lapor)` di thread latar.

    Mengembalikan nilai kembalian fungsi_muat. Bila splash tidak bisa ditampilkan
    (mis. tanpa layar), fungsi_muat langsung dijalankan tanpa animasi.
    """
    pemuat = _Pemuat(fungsi_muat)
    try:
        splash = SplashView(pemuat, durasi_min_ms)
    except tk.TclError:
        _tutup_splash_pyinstaller()
        return fungsi_muat(lambda *_: None)
    splash.jalankan()
    if pemuat.galat is not None:
        # coba sekali lagi di thread utama; bila gagal lagi, galat aslinya yang muncul
        return fungsi_muat(lambda *_: None)
    return pemuat.hasil
