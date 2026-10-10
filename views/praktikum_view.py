"""View Praktikum (GUI desktop, customtkinter).
View bersifat pasif: tidak ada logika bisnis maupun SQL. Aksi tombol diatur Controller."""
import customtkinter as ctk
from tkinter import ttk, messagebox


class PraktikumView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Penilaian Praktikum - Praktikum")
        self.geometry("850x500")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # =========================================
        # FRAME KIRI: FORMULIR INPUT PRAKTIKUM
        # =========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Praktikum", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_kode = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Kode Praktikum")
        self.entry_kode.pack(pady=8, padx=15, fill="x")

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Praktikum")
        self.entry_nama.pack(pady=8, padx=15, fill="x")

        self.entry_semester = ctk.CTkEntry(self.frame_kiri, placeholder_text="Semester (Misal: Ganjil 2026/2027)")
        self.entry_semester.pack(pady=8, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(20, 5), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        # =========================================
        # FRAME KANAN: TABEL DAFTAR PRAKTIKUM
        # =========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Data Praktikum", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "kode", "nama", "semester",)
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("kode", text="Kode")
        self.tabel.heading("nama", text="Nama Praktikum")
        self.tabel.heading("semester", text="Semester")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("kode", width=100)
        self.tabel.column("nama", width=150)
        self.tabel.column("semester", width=100)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        """Mengembalikan isi form sebagai dictionary."""
        return {
            "kode": self.entry_kode.get().strip(),
            "nama": self.entry_nama.get().strip(),
            "semester": self.entry_semester.get().strip(),
        }

    def kosongkan_form(self):
        self.entry_kode.delete(0, "end")
        self.entry_nama.delete(0, "end")
        self.entry_semester.delete(0, "end")

    def isi_form(self, data):
        """Mengisi form dari dictionary (misalnya saat baris tabel dipilih)."""
        self.kosongkan_form()
        self.entry_kode.insert(0, "" if data.get("kode") is None else str(data.get("kode")))
        self.entry_nama.insert(0, "" if data.get("nama") is None else str(data.get("nama")))
        self.entry_semester.insert(0, "" if data.get("semester") is None else str(data.get("semester")))

    def tampilkan_data(self, daftar):
        """Menampilkan list of dict ke tabel."""
        self.tabel.delete(*self.tabel.get_children())
        for d in daftar:
            self.tabel.insert("", "end", values=(
                "" if d.get("id_praktikum") is None else d.get("id_praktikum"),
                "" if d.get("kode") is None else d.get("kode"),
                "" if d.get("nama") is None else d.get("nama"),
                "" if d.get("semester") is None else d.get("semester"),
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
    app = PraktikumView()
    # Data contoh hanya untuk menguji tampilan (boleh dihapus)
    app.tampilkan_data([{'id_praktikum': 1, 'kode': 'BD01', 'nama': 'Basis Data', 'semester': 'Ganjil 2026/2027'}])
    app.mainloop()