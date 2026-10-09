from config.database import Database
from models.mahasiswa_model import MahasiswaModel
from models.praktikum_model import PraktikumModel
from models.pertemuan_model import PertemuanModel
from models.tugas_model import TugasModel
from models.laporan_model import LaporanModel
from models.nilai_model import NilaiModel

print("=== Tes koneksi ===")
conn = Database().get_connection()
if not conn:
    raise SystemExit("Koneksi gagal. Start MySQL di Laragon & import database/database.sql dulu.")
print("Koneksi ke Laragon MySQL berhasil!")
conn.close()

print("\n=== Tes Read semua tabel ===")
for nama, model in [("mahasiswa", MahasiswaModel()), ("praktikum", PraktikumModel()),
                    ("pertemuan", PertemuanModel()), ("tugas", TugasModel()),
                    ("laporan", LaporanModel()), ("nilai", NilaiModel())]:
    print(f"{nama:<10}: {len(model.get_all())} baris")

print("\n=== Tes CRUD mahasiswa ===")
mhs = MahasiswaModel()
NIM = "99999999"
print("Create :", mhs.create(NIM, "Mahasiswa Uji", "C"))
baru = [m for m in mhs.get_all() if m["nim"] == NIM]
if baru:
    id_baru = baru[0]["id_mahasiswa"]
    print("Read   :", baru[0])
    print("Update :", mhs.update(id_baru, NIM, "Mahasiswa Uji (Edit)", "C"))
    print("Delete :", mhs.delete(id_baru))
else:
    print("Create gagal:", mhs.db.last_error)

print("\n=== Daftar Mahasiswa ===")
for m in mhs.get_all():
    print(f"[{m['id_mahasiswa']}] {m['nim']} | {m['nama']} | {m['kelas']}")
