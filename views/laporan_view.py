"""View Laporan (GUI desktop, customtkinter).
View bersifat pasif: tidak ada logika bisnis maupun SQL. Aksi tombol diatur Controller."""
import customtkinter as ctk
from tkinter import ttk, messagebox


class LaporanView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Penilaian Praktikum - Laporan")
        self.geometry("850x550")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # =========================================
        # FRAME KIRI: FORMULIR INPUT LAPORAN
        # =========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Laporan", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_id_tugas = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan ID Tugas")
        self.entry_id_tugas.pack(pady=8, padx=15, fill="x")

        self.entry_id_mahasiswa = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan ID Mahasiswa")
        self.entry_id_mahasiswa.pack(pady=8, padx=15, fill="x")

        self.entry_file_laporan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama/path file laporan")
        self.entry_file_laporan.pack(pady=8, padx=15, fill="x")

        self.entry_catatan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Catatan (opsional)")
        self.entry_catatan.pack(pady=8, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(20, 5), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        # =========================================
        # FRAME KANAN: TABEL DAFTAR LAPORAN
        # =========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Data Laporan", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "id_tugas", "id_mahasiswa", "file_laporan", "catatan",)
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("id_tugas", text="ID Tugas")
        self.tabel.heading("id_mahasiswa", text="ID Mahasiswa")
        self.tabel.heading("file_laporan", text="File Laporan")
        self.tabel.heading("catatan", text="Catatan")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("id_tugas", width=100)
        self.tabel.column("id_mahasiswa", width=100)
        self.tabel.column("file_laporan", width=150)
        self.tabel.column("catatan", width=150)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        """Mengembalikan isi form sebagai dictionary."""
        return {
            "id_tugas": self.entry_id_tugas.get().strip(),
            "id_mahasiswa": self.entry_id_mahasiswa.get().strip(),
            "file_laporan": self.entry_file_laporan.get().strip(),
            "catatan": self.entry_catatan.get().strip(),
        }

    def kosongkan_form(self):
        self.entry_id_tugas.delete(0, "end")
        self.entry_id_mahasiswa.delete(0, "end")
        self.entry_file_laporan.delete(0, "end")
        self.entry_catatan.delete(0, "end")

    def isi_form(self, data):
        """Mengisi form dari dictionary (misalnya saat baris tabel dipilih)."""
        self.kosongkan_form()
        self.entry_id_tugas.insert(0, "" if data.get("id_tugas") is None else str(data.get("id_tugas")))
        self.entry_id_mahasiswa.insert(0, "" if data.get("id_mahasiswa") is None else str(data.get("id_mahasiswa")))
        self.entry_file_laporan.insert(0, "" if data.get("file_laporan") is None else str(data.get("file_laporan")))
        self.entry_catatan.insert(0, "" if data.get("catatan") is None else str(data.get("catatan")))

    def tampilkan_data(self, daftar):
        """Menampilkan list of dict ke tabel."""
        self.tabel.delete(*self.tabel.get_children())
        for d in daftar:
            self.tabel.insert("", "end", values=(
                "" if d.get("id_laporan") is None else d.get("id_laporan"),
                "" if d.get("id_tugas") is None else d.get("id_tugas"),
                "" if d.get("id_mahasiswa") is None else d.get("id_mahasiswa"),
                "" if d.get("file_laporan") is None else d.get("file_laporan"),
                "" if d.get("catatan") is None else d.get("catatan"),
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
    app = LaporanView()
    # Data contoh hanya untuk menguji tampilan (boleh dihapus)
    app.tampilkan_data([{'id_laporan': 1, 'id_tugas': 1, 'id_mahasiswa': 1, 'file_laporan': 'laporan_erd.pdf', 'catatan': '-'}])
    app.mainloop()