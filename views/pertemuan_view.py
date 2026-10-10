"""View Pertemuan (GUI desktop, customtkinter).
View bersifat pasif: tidak ada logika bisnis maupun SQL. Aksi tombol diatur Controller."""
import customtkinter as ctk
from tkinter import ttk, messagebox


class PertemuanView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Penilaian Praktikum - Pertemuan")
        self.geometry("850x550")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # =========================================
        # FRAME KIRI: FORMULIR INPUT PERTEMUAN
        # =========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Pertemuan", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_id_praktikum = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan ID Praktikum")
        self.entry_id_praktikum.pack(pady=8, padx=15, fill="x")

        self.entry_pertemuan_ke = ctk.CTkEntry(self.frame_kiri, placeholder_text="Pertemuan ke- (Misal: 1)")
        self.entry_pertemuan_ke.pack(pady=8, padx=15, fill="x")

        self.entry_topik = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Topik Pertemuan")
        self.entry_topik.pack(pady=8, padx=15, fill="x")

        self.entry_tanggal = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tanggal (YYYY-MM-DD)")
        self.entry_tanggal.pack(pady=8, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(20, 5), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        # =========================================
        # FRAME KANAN: TABEL DAFTAR PERTEMUAN
        # =========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Data Pertemuan", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "id_praktikum", "pertemuan_ke", "topik", "tanggal",)
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("id_praktikum", text="ID Praktikum")
        self.tabel.heading("pertemuan_ke", text="Pertemuan Ke")
        self.tabel.heading("topik", text="Topik")
        self.tabel.heading("tanggal", text="Tanggal")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("id_praktikum", width=100)
        self.tabel.column("pertemuan_ke", width=100)
        self.tabel.column("topik", width=150)
        self.tabel.column("tanggal", width=100)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        """Mengembalikan isi form sebagai dictionary."""
        return {
            "id_praktikum": self.entry_id_praktikum.get().strip(),
            "pertemuan_ke": self.entry_pertemuan_ke.get().strip(),
            "topik": self.entry_topik.get().strip(),
            "tanggal": self.entry_tanggal.get().strip(),
        }

    def kosongkan_form(self):
        self.entry_id_praktikum.delete(0, "end")
        self.entry_pertemuan_ke.delete(0, "end")
        self.entry_topik.delete(0, "end")
        self.entry_tanggal.delete(0, "end")

    def isi_form(self, data):
        """Mengisi form dari dictionary (misalnya saat baris tabel dipilih)."""
        self.kosongkan_form()
        self.entry_id_praktikum.insert(0, "" if data.get("id_praktikum") is None else str(data.get("id_praktikum")))
        self.entry_pertemuan_ke.insert(0, "" if data.get("pertemuan_ke") is None else str(data.get("pertemuan_ke")))
        self.entry_topik.insert(0, "" if data.get("topik") is None else str(data.get("topik")))
        self.entry_tanggal.insert(0, "" if data.get("tanggal") is None else str(data.get("tanggal")))

    def tampilkan_data(self, daftar):
        """Menampilkan list of dict ke tabel."""
        self.tabel.delete(*self.tabel.get_children())
        for d in daftar:
            self.tabel.insert("", "end", values=(
                "" if d.get("id_pertemuan") is None else d.get("id_pertemuan"),
                "" if d.get("id_praktikum") is None else d.get("id_praktikum"),
                "" if d.get("pertemuan_ke") is None else d.get("pertemuan_ke"),
                "" if d.get("topik") is None else d.get("topik"),
                "" if d.get("tanggal") is None else d.get("tanggal"),
            ))

    def id_terpilih(self):
        """ID dari baris yang dipilih di tabel, atau None."""
        pilihan = self.tabel.selection()
        return self.tabel.item(pilihan[0])["values"][0] if pilihan else None

    def tampilkan_pesan(self, teks, error=False):
        tampil = messagebox.showerror if error else messagebox.showinfo
        tampil("Sistem Penilaian Praktikum", teks)


# Blok eksekusi untuk menguji tampilan grafis
if __name__ == "__main__":
    app = PertemuanView()
    # Data contoh hanya untuk menguji tampilan (boleh dihapus)
    app.tampilkan_data([{'id_pertemuan': 1, 'id_praktikum': 1, 'pertemuan_ke': 1, 'topik': 'Pengenalan ERD', 'tanggal': '2026-10-09'}])
    app.mainloop()