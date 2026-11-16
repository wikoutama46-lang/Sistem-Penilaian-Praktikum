import re

from config.keamanan import (hash_password, verifikasi_password, HASH_PALSU,
                             kode_registrasi_benar)
from controllers.base_controller import hasil, kosong
from models.user_model import UserModel

ROLE = ("asdos", "dosen", "mahasiswa")
POLA_USERNAME = re.compile(r"^[A-Za-z0-9_.]{4,30}$")
MIN_PASSWORD = 8


class AuthController:
    def __init__(self):
        self.model = UserModel()

    def _validasi_daftar(self, data):
        role = data.get("role")
        if role not in ROLE:
            return "Pilih peran (Asisten Dosen, Dosen, atau Mahasiswa)."
        if kosong(data.get("nama")) or kosong(data.get("username")) or kosong(data.get("password")):
            return "Nama, username, dan password wajib diisi."
        if len(data["nama"].strip()) > 100:
            return "Nama maksimal 100 karakter."
        if not POLA_USERNAME.match(data["username"].strip()):
            return "Username 4-30 karakter: huruf, angka, titik, atau underscore."
        if len(data["password"]) < MIN_PASSWORD:
            return f"Password minimal {MIN_PASSWORD} karakter."
        if data["password"] != data.get("konfirmasi"):
            return "Konfirmasi password tidak sama."
        if role == "mahasiswa":
            if kosong(data.get("nim")) or kosong(data.get("kelas")):
                return "NIM dan kelas wajib diisi untuk mahasiswa."
            if len(data["nim"].strip()) > 20:
                return "NIM maksimal 20 karakter."
        if role == "dosen":
            if kosong(data.get("nidn")):
                return "NIDN wajib diisi untuk dosen."
            if len(data["nidn"].strip()) > 20:
                return "NIDN maksimal 20 karakter."
        if role in ("asdos", "dosen") and not kode_registrasi_benar(role, data.get("kode")):
            return "Kode registrasi salah. Hubungi pengelola praktikum."
        return None

    def daftar(self, data):
        """data: dict role, nama, username, password, konfirmasi, nim, kelas, nidn, kode."""
        err = self._validasi_daftar(data)
        if err:
            return hasil(False, err)
        username = data["username"].strip()
        if self.model.username_ada(username):
            return hasil(False, f"Username '{username}' sudah dipakai.")
        role = data["role"]
        nidn = data["nidn"].strip() if role == "dosen" else None
        if nidn and self.model.nidn_ada(nidn):
            return hasil(False, f"NIDN {nidn} sudah terdaftar.")
        ok, pesan = self.model.register(
            username, hash_password(data["password"]), role, data["nama"].strip(),
            nim=data.get("nim", "").strip() or None,
            kelas=data.get("kelas", "").strip() or None, nidn=nidn)
        if not ok:
            return hasil(False, pesan)
        return hasil(True, "Akun berhasil dibuat. Silakan masuk.")

    def masuk(self, username, password):
        if kosong(username) or kosong(password):
            return hasil(False, "Username dan password wajib diisi.")
        user = self.model.get_by_username(username.strip())
        if user is None:
            verifikasi_password(password, HASH_PALSU)   # samakan waktu proses
            return hasil(False, "Username atau password salah.")
        if not verifikasi_password(password, user["password_hash"]):
            return hasil(False, "Username atau password salah.")
        if user["status"] != "aktif":
            return hasil(False, "Akun tidak aktif.")
        profil = {k: v for k, v in user.items() if k != "password_hash"}
        return hasil(True, "Login berhasil.", profil)
