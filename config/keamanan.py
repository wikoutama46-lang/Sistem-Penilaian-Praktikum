"""Keamanan akun: hashing password (PBKDF2-SHA256 + salt acak) dan kode registrasi aktor.

Hanya memakai pustaka standar Python, jadi tidak perlu pip install tambahan.
Format hash tersimpan di kolom users.password_hash:
    pbkdf2_sha256$<iterasi>$<salt hex>$<hash hex>
"""
import hashlib
import hmac
import os
import secrets

ALGORITMA = "pbkdf2_sha256"
ITERASI = 600_000          # rekomendasi OWASP untuk PBKDF2-HMAC-SHA256

# Kode registrasi agar tidak sembarang orang bisa mendaftar sebagai Asdos/Dosen.
# Ubah lewat environment variable (jangan commit kode asli ke GitHub):
#   setx KODE_REG_ASDOS "kode-rahasia-asdos"
#   setx KODE_REG_DOSEN "kode-rahasia-dosen"
# Mahasiswa tidak memerlukan kode.
KODE_REGISTRASI = {
    "asdos": os.environ.get("KODE_REG_ASDOS", "ASDOS-2026"),
    "dosen": os.environ.get("KODE_REG_DOSEN", "DOSEN-2026"),
}


def hash_password(password):
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERASI)
    return f"{ALGORITMA}${ITERASI}${salt.hex()}${dk.hex()}"


def verifikasi_password(password, hash_tersimpan):
    """True jika password cocok dengan hash tersimpan."""
    try:
        algoritma, iterasi, salt_hex, hash_hex = hash_tersimpan.split("$")
        if algoritma != ALGORITMA:
            return False
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt_hex), int(iterasi))
        return hmac.compare_digest(dk.hex(), hash_hex)
    except (ValueError, AttributeError):
        return False


# Hash palsu untuk menyamakan waktu proses saat username tidak ditemukan
HASH_PALSU = hash_password(secrets.token_hex(8))


def kode_registrasi_benar(role, kode):
    asli = KODE_REGISTRASI.get(role)
    if asli is None:
        return True            # role tanpa kode (mahasiswa)
    return hmac.compare_digest(str(kode or "").encode(), asli.encode())
