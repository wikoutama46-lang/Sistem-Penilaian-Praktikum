"""Tema dan komponen bersama semua halaman GUI (mengikuti pedoman antarmuka 7.1).

Palet : cyan-teal #2FB5CA (aksen utama, Simpan), #179AB0 (aksen kedua, Perbarui, hover),
        navy #2A334B (judul, header tabel), #3D476A (panel, teks sekunder),
        latar jendela #EEEFF6. Tombol Hapus tetap merah.
Font  : Arial, judul panel 16 pt tebal, selebihnya ukuran standar widget.
"""
import customtkinter as ctk
from tkinter import ttk, messagebox

# ---------- Warna ----------
CYAN = "#2FB5CA"
CYAN_GELAP = "#179AB0"
NAVY = "#2A334B"
NAVY_SEDANG = "#3D476A"
LATAR = "#EEEFF6"
PUTIH = "#FFFFFF"
MERAH = "#C73E4A"
MERAH_HOVER = "#A32F3A"
TEKS_NONAKTIF = "#8A90A6"
PLACEHOLDER = "#6B7390"
HOVER_TIPIS = "#DDE1EE"

# ---------- Font ----------
F_JUDUL = ("Arial", 16, "bold")
F_TEKS = ("Arial", 13)
F_TEBAL = ("Arial", 13, "bold")

JUDUL_JENDELA = "Sistem Penilaian Praktikum"

# gaya tombol: (warna isi, warna hover, warna teks, warna garis)
_GAYA_TOMBOL = {
    "utama": (CYAN, CYAN_GELAP, NAVY, None),
    "kedua": (CYAN_GELAP, NAVY_SEDANG, PUTIH, None),
    "bahaya": (MERAH, MERAH_HOVER, PUTIH, None),
    "garis": ("transparent", HOVER_TIPIS, NAVY, NAVY_SEDANG),
    "navbar": ("transparent", NAVY_SEDANG, PUTIH, None),
}


def terapkan_tema():
    ctk.set_appearance_mode("light")


def gaya_tabel():
    """Gaya ttk.Treeview agar serasi dengan palet (dipanggil sekali setelah jendela dibuat)."""
    gaya = ttk.Style()
    gaya.theme_use("clam")
    gaya.configure("Treeview", background=PUTIH, fieldbackground=PUTIH,
                   foreground=NAVY, rowheight=26, font=("Arial", 10),
                   bordercolor=NAVY_SEDANG, borderwidth=1)
    gaya.configure("Treeview.Heading", background=NAVY, foreground=PUTIH,
                   font=("Arial", 10, "bold"), relief="flat", padding=4)
    gaya.map("Treeview", background=[("selected", CYAN)],
             foreground=[("selected", NAVY)])
    gaya.map("Treeview.Heading", background=[("active", NAVY_SEDANG)])


# ---------- Komponen ----------
def panel(master, **kw):
    return ctk.CTkFrame(master, fg_color=PUTIH, border_width=1,
                        border_color=NAVY_SEDANG, corner_radius=8, **kw)


def judul(master, isi, warna=NAVY, **kw):
    return ctk.CTkLabel(master, text=isi, font=F_JUDUL, text_color=warna, **kw)


def teks(master, isi, sekunder=False, tebal=False, **kw):
    return ctk.CTkLabel(master, text=isi, font=F_TEBAL if tebal else F_TEKS,
                        text_color=NAVY_SEDANG if sekunder else NAVY, **kw)


def entri(master, placeholder, **kw):
    return ctk.CTkEntry(master, placeholder_text=placeholder, font=F_TEKS,
                        fg_color=PUTIH, border_color=NAVY_SEDANG,
                        text_color=NAVY, placeholder_text_color=PLACEHOLDER, **kw)


def tombol(master, label, gaya="utama", **kw):
    isi, hover, warna_teks, garis = _GAYA_TOMBOL[gaya]
    opsi = dict(text=label, font=F_TEBAL, fg_color=isi, hover_color=hover,
                text_color=warna_teks, text_color_disabled=TEKS_NONAKTIF)
    if garis:
        opsi.update(border_width=1, border_color=garis)
    opsi.update(kw)
    return ctk.CTkButton(master, **opsi)


def menu_pilihan(master, nilai, command=None, **kw):
    return ctk.CTkOptionMenu(
        master, values=nilai, command=command, font=F_TEKS, dropdown_font=F_TEKS,
        fg_color=NAVY_SEDANG, button_color=NAVY, button_hover_color=CYAN_GELAP,
        text_color=PUTIH, dropdown_fg_color=PUTIH, dropdown_text_color=NAVY,
        dropdown_hover_color=CYAN, **kw)


# ---------- Messagebox ----------
def pesan_info(isi):
    messagebox.showinfo(JUDUL_JENDELA, isi)


def pesan_error(isi):
    messagebox.showerror(JUDUL_JENDELA, isi)


def konfirmasi(isi):
    return messagebox.askyesno(JUDUL_JENDELA, isi)