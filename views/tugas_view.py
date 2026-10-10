"""View Tugas (GUI desktop, customtkinter).
View bersifat pasif: tidak ada logika bisnis maupun SQL. Aksi tombol diatur Controller."""
import customtkinter as ctk
from tkinter import ttk, messagebox


class TugasView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Penilaian Praktikum - Tugas")
        self.geometry("850x500")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # =========================================
        # FRAME KIRI: FORMULIR INPUT TUGAS
        # =========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Tugas", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_id_pertemuan = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan ID Pertemuan")
        self.entry_id_pertemuan.pack(pady=8, padx=15, fill="x")

        self.entry_nama_tugas = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Tugas")
        self.entry_nama_tugas.pack(pady=8, padx=15, fill="x")

        self.entry_deadline = ctk.CTkEntry(self.frame_kiri, placeholder_text="Deadline (YYYY-MM-DD HH:MM:SS)")
        self.entry_deadline.pack(pady=8, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(20, 5), padx=15, fill="x")

        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        # =========================================
        # FRAME KANAN: TABEL DAFTAR TUGAS
        # =========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kanan, text="Daftar Data Tugas", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "praktikum", "pertemuan_ke", "nama_tugas", "deadline",)
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("praktikum", text="Praktikum")
        self.tabel.heading("pertemuan_ke", text="Pertemuan Ke")
        self.tabel.heading("nama_tugas", text="Nama Tugas")
        self.tabel.heading("deadline", text="Deadline")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("praktikum", width=110)
        self.tabel.column("pertemuan_ke", width=90, anchor="center")
        self.tabel.column("nama_tugas", width=130)
        self.tabel.column("deadline", width=130)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)

    # ===== Method bantu untuk Controller (tanpa logika bisnis) =====
    def ambil_input(self):
        """Mengembalikan isi form sebagai dictionary."""
        return {
            "id_pertemuan": self.entry_id_pertemuan.get().strip(),
            "nama_tugas": self.entry_nama_tugas.get().strip(),
            "deadline": self.entry_deadline.get().strip(),
        }

    def kosongkan_form(self):
        self.entry_id_pertemuan.delete(0, "end")
        self.entry_nama_tugas.delete(0, "end")
        self.entry_deadline.delete(0, "end")

    def isi_form(self, data):
        """Mengisi form dari dictionary (misalnya saat baris tabel dipilih)."""
        self.kosongkan_form()
        self.entry_id_pertemuan.insert(0, "" if data.get("id_pertemuan") is None else str(data.get("id_pertemuan")))
        self.entry_nama_tugas.insert(0, "" if data.get("nama_tugas") is None else str(data.get("nama_tugas")))
        self.entry_deadline.insert(0, "" if data.get("deadline") is None else str(data.get("deadline")))

    def tampilkan_data(self, daftar):
        """Menampilkan list of dict ke tabel."""
        self.tabel.delete(*self.tabel.get_children())
        for d in daftar:
            self.tabel.insert("", "end", values=(
                "" if d.get("id_tugas") is None else d.get("id_tugas"),
                "" if d.get("nama_praktikum") is None else d.get("nama_praktikum"),
                "" if d.get("pertemuan_ke") is None else d.get("pertemuan_ke"),
                "" if d.get("nama_tugas") is None else d.get("nama_tugas"),
                "" if d.get("deadline") is None else d.get("deadline"),
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
    app = TugasView()
    # Data contoh hanya untuk menguji tampilan (boleh dihapus)
    app.tampilkan_data([{"id_tugas": 1, "nama_praktikum": "RPL", "pertemuan_ke": 1, "nama_tugas": "Membuat ERD", "deadline": "2026-10-16 23:59:00"}])
    app.mainloop()
