"""Membuat ulang aset ikon dari assets/logo.png.

Hasil : assets/icon.ico        ikon .exe (16-256 px)
        assets/icon.png        ikon jendela 256 px
        assets/boot_splash.png gambar statis yang tampil seketika saat .exe dibuka
Jalankan dari folder proyek:  python tools/buat_aset.py   (butuh: pip install pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASET = os.path.join(ROOT, "assets")
BG = (7, 12, 22)          # harus sama dengan WARNA_LATAR di views/splash_view.py
LEBAR, TINGGI = 640, 360   # harus sama dengan ukuran jendela splash


def potong_chip(logo):
    """Ambil bagian chip (kiri) dari logo lebar, lalu jadikan persegi."""
    alpha = logo.split()[3]
    kolom = [x for x in range(logo.width) if alpha.crop((x, 0, x + 1, logo.height)).getbbox()]
    batas = next(kolom[i] for i in range(len(kolom) - 1) if kolom[i + 1] - kolom[i] > 50)
    chip = logo.crop((0, 0, batas + 1, logo.height))
    chip = chip.crop(chip.getbbox())
    sisi = max(chip.size)
    kanvas = Image.new("RGBA", (sisi, sisi), (0, 0, 0, 0))
    kanvas.paste(chip, ((sisi - chip.width) // 2, (sisi - chip.height) // 2))
    return kanvas


def main():
    logo = Image.open(os.path.join(ASET, "logo.png")).convert("RGBA")
    chip = potong_chip(logo)
    pad = int(chip.width * 0.06)
    ikon = Image.new("RGBA", (chip.width + 2 * pad,) * 2, (0, 0, 0, 0))
    ikon.paste(chip, (pad, pad))

    ikon.resize((256, 256), Image.LANCZOS).save(os.path.join(ASET, "icon.png"))
    ikon.save(os.path.join(ASET, "icon.ico"),
              sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    # gambar statis untuk splash bawaan PyInstaller (tampil sebelum Python siap)
    gambar = Image.new("RGB", (LEBAR, TINGGI), BG)
    c = chip.resize((150, 150), Image.LANCZOS)
    gambar.paste(c, ((LEBAR - 150) // 2, 70), c)
    d = ImageDraw.Draw(gambar)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    teks = "// MEMUAT APLIKASI ..."
    w = d.textlength(teks, font=font)
    d.text(((LEBAR - w) / 2, 260), teks, fill=(34, 211, 238), font=font)
    d.rectangle((0, 0, LEBAR - 1, TINGGI - 1), outline=(34, 60, 90))
    gambar.save(os.path.join(ASET, "boot_splash.png"))
    print("Aset dibuat di", ASET)


if __name__ == "__main__":
    main()
