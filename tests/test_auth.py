"""Unit test autentikasi & otorisasi (Modul 7-8).

Tidak butuh MySQL: UserModel di-mock, jadi aman dijalankan di GitHub Actions.
Jalankan:  pytest -v
"""
from unittest.mock import patch

import pytest

from config import keamanan
from config.keamanan import (hash_password, verifikasi_password,
                             kode_registrasi_benar, KODE_REGISTRASI)
from controllers.auth_controller import AuthController
from controllers.hak_akses import boleh, modul_boleh_lihat


# ---------------------------------------------------------------- fixture
@pytest.fixture
def iterasi_cepat(monkeypatch):
    """Kurangi iterasi PBKDF2 agar test cepat (hash tetap valid)."""
    monkeypatch.setattr(keamanan, "ITERASI", 1000)


@pytest.fixture
def auth():
    """AuthController dengan UserModel palsu (tanpa database)."""
    with patch("controllers.auth_controller.UserModel") as MockModel:
        ctrl = AuthController()
        ctrl.model = MockModel.return_value
        ctrl.model.username_ada.return_value = False
        ctrl.model.nidn_ada.return_value = False
        ctrl.model.register.return_value = (True, None)
        yield ctrl


def data_mahasiswa(**ubah):
    d = {"role": "mahasiswa", "nama": "Budi", "username": "budi_01",
         "password": "rahasia123", "konfirmasi": "rahasia123",
         "nim": "F5212530001", "kelas": "C"}
    d.update(ubah)
    return d


# ------------------------------------------------------- hashing password
def test_iterasi_sesuai_rekomendasi():
    assert keamanan.ITERASI >= 600_000


def test_hash_berformat_dan_bukan_teks_biasa(iterasi_cepat):
    h = hash_password("admin123")
    assert h.startswith("pbkdf2_sha256$")
    assert "admin123" not in h
    assert len(h.split("$")) == 4


def test_hash_konsisten_untuk_password_sama(iterasi_cepat):
    h = hash_password("admin123")
    assert verifikasi_password("admin123", h) is True


def test_password_salah_ditolak(iterasi_cepat):
    assert verifikasi_password("salah", hash_password("admin123")) is False


def test_salt_acak_membuat_hash_berbeda(iterasi_cepat):
    assert hash_password("sama") != hash_password("sama")


def test_hash_rusak_tidak_membuat_error():
    assert verifikasi_password("x", "bukan-hash") is False
    assert verifikasi_password("x", None) is False
    assert verifikasi_password("x", "md5$1$00$00") is False


# --------------------------------------------------------- kode registrasi
def test_kode_registrasi(monkeypatch):
    monkeypatch.setitem(KODE_REGISTRASI, "asdos", "KODE-UJI")
    assert kode_registrasi_benar("asdos", "KODE-UJI") is True
    assert kode_registrasi_benar("asdos", "salah") is False
    assert kode_registrasi_benar("asdos", None) is False
    assert kode_registrasi_benar("mahasiswa", "") is True   # tanpa kode


# ------------------------------------------------------------------ login
def test_login_kolom_kosong(auth):
    assert auth.masuk("", "abc")["sukses"] is False
    assert auth.masuk("budi", "  ")["sukses"] is False
    auth.model.get_by_username.assert_not_called()


def test_login_username_tidak_ditemukan(auth):
    auth.model.get_by_username.return_value = None
    res = auth.masuk("hantu", "apa-saja")
    assert res["sukses"] is False
    assert "salah" in res["pesan"].lower()


def test_login_password_salah(auth, iterasi_cepat):
    auth.model.get_by_username.return_value = {
        "password_hash": hash_password("benar123"), "status": "aktif"}
    assert auth.masuk("budi", "salah123")["sukses"] is False


def test_login_berhasil_dan_hash_tidak_bocor(auth, iterasi_cepat):
    auth.model.get_by_username.return_value = {
        "id_user": 1, "username": "budi", "role": "mahasiswa", "nama": "Budi",
        "password_hash": hash_password("benar123"), "status": "aktif"}
    res = auth.masuk("budi", "benar123")
    assert res["sukses"] is True
    assert res["data"]["role"] == "mahasiswa"
    assert "password_hash" not in res["data"]


def test_login_akun_nonaktif(auth, iterasi_cepat):
    auth.model.get_by_username.return_value = {
        "password_hash": hash_password("benar123"), "status": "nonaktif"}
    res = auth.masuk("budi", "benar123")
    assert res["sukses"] is False
    assert "tidak aktif" in res["pesan"].lower()


# ------------------------------------------------------------- registrasi
@pytest.mark.parametrize("ubah", [
    {"role": "admin"},                          # peran tidak dikenal
    {"nama": ""},                               # nama kosong
    {"username": "a b"},                        # username tidak valid
    {"password": "pendek", "konfirmasi": "pendek"},   # < 8 karakter
    {"konfirmasi": "beda-sekali"},              # konfirmasi tidak sama
    {"nim": ""},                                # mahasiswa tanpa NIM
    {"kelas": ""},                              # mahasiswa tanpa kelas
])
def test_daftar_input_tidak_valid(auth, ubah):
    res = auth.daftar(data_mahasiswa(**ubah))
    assert res["sukses"] is False
    auth.model.register.assert_not_called()


def test_daftar_dosen_wajib_nidn(auth, monkeypatch):
    monkeypatch.setitem(KODE_REGISTRASI, "dosen", "KODE-DOSEN")
    d = {"role": "dosen", "nama": "Pak Dosen", "username": "pakdosen",
         "password": "rahasia123", "konfirmasi": "rahasia123",
         "nidn": "", "kode": "KODE-DOSEN"}
    assert auth.daftar(d)["sukses"] is False


def test_daftar_asdos_kode_salah(auth, monkeypatch):
    monkeypatch.setitem(KODE_REGISTRASI, "asdos", "KODE-ASDOS")
    d = {"role": "asdos", "nama": "Kak Asdos", "username": "kakasdos",
         "password": "rahasia123", "konfirmasi": "rahasia123", "kode": "tebak"}
    res = auth.daftar(d)
    assert res["sukses"] is False
    auth.model.register.assert_not_called()


def test_daftar_username_sudah_dipakai(auth):
    auth.model.username_ada.return_value = True
    assert auth.daftar(data_mahasiswa())["sukses"] is False
    auth.model.register.assert_not_called()


def test_daftar_berhasil_menyimpan_hash_bukan_teks_biasa(auth, iterasi_cepat):
    res = auth.daftar(data_mahasiswa())
    assert res["sukses"] is True
    args = auth.model.register.call_args.args
    assert args[1].startswith("pbkdf2_sha256$")     # password_hash
    assert "rahasia123" not in args[1]


def test_daftar_gagal_dari_database(auth, iterasi_cepat):
    auth.model.register.return_value = (False, "NIM sudah memiliki akun.")
    res = auth.daftar(data_mahasiswa())
    assert res["sukses"] is False
    assert "NIM" in res["pesan"]


# ------------------------------------------------- otorisasi (RBAC)
def test_asdos_boleh_semua_aksi():
    for modul in ("mahasiswa", "praktikum", "pertemuan", "tugas", "laporan", "nilai"):
        for aksi in ("lihat", "tambah", "ubah", "hapus"):
            assert boleh("asdos", modul, aksi)


def test_dosen_hanya_melihat():
    assert boleh("dosen", "nilai", "lihat")
    assert not boleh("dosen", "nilai", "ubah")
    assert not boleh("dosen", "mahasiswa", "lihat")


def test_mahasiswa_terbatas():
    assert boleh("mahasiswa", "nilai", "lihat")
    assert boleh("mahasiswa", "laporan", "tambah")
    assert not boleh("mahasiswa", "nilai", "tambah")
    assert not boleh("mahasiswa", "laporan", "hapus")
    assert not boleh("mahasiswa", "mahasiswa", "lihat")


def test_role_tidak_dikenal_ditolak():
    assert not boleh("hacker", "nilai", "lihat")
    assert not boleh(None, "nilai", "lihat")


def test_modul_boleh_lihat_mengikuti_role():
    urutan = ["mahasiswa", "praktikum", "pertemuan", "tugas", "laporan", "nilai"]
    assert modul_boleh_lihat("dosen", urutan) == ["praktikum", "laporan", "nilai"]
    assert modul_boleh_lihat("mahasiswa", urutan) == ["tugas", "laporan", "nilai"]
