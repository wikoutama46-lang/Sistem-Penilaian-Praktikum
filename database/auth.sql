-- =====================================================================
-- AUTH & AKTOR  |  Sistem Penilaian Praktikum
-- Jalankan di database yang SUDAH ADA (HeidiSQL / phpMyAdmin Laragon).
-- Hash password dibuat oleh Python (PBKDF2-SHA256 + salt), BUKAN oleh SQL.
-- Kolom password_hash hanya menyimpan string hasilnya.
-- Catatan: jangan taruh tanda titik-koma di dalam komentar/teks, karena
-- Database.setup_database() memecah file SQL berdasarkan titik-koma.
-- =====================================================================

USE sistem_penilaian_praktikum;

-- 1) Tabel users: satu tabel untuk 3 aktor (asdos, dosen, mahasiswa) -----
CREATE TABLE IF NOT EXISTS users (
    id_user        BIGINT       NOT NULL AUTO_INCREMENT,
    username       VARCHAR(30)  NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    role           ENUM('asdos','dosen','mahasiswa') NOT NULL,
    nama           VARCHAR(100) NOT NULL,
    id_mahasiswa   BIGINT       NULL,
    nidn           VARCHAR(20)  NULL,
    status         ENUM('aktif','nonaktif') NOT NULL DEFAULT 'aktif',
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_id_mahasiswa (id_mahasiswa),
    UNIQUE KEY uq_users_nidn (nidn),
    KEY idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2) Relasi akun mahasiswa -> tabel mahasiswa -----------------------------
-- Tipe id_mahasiswa harus SAMA PERSIS dengan kolom di tabel mahasiswa.
-- Cek dulu:  SHOW CREATE TABLE mahasiswa;
-- Kamus data dokumen memakai BIGINT, ERD memakai INT. Jika di database
-- Anda INT, ubah tipe kolom users.id_mahasiswa lebih dulu:
--   ALTER TABLE users MODIFY id_mahasiswa INT NULL;
ALTER TABLE users
    ADD CONSTRAINT fk_users_mahasiswa
    FOREIGN KEY (id_mahasiswa) REFERENCES mahasiswa (id_mahasiswa)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- =====================================================================
-- JIKA TABEL users SUDAH ADA dengan kolom password teks biasa (opsional)
-- Jalankan satu per satu. Akun lama tidak bisa di-hash lewat SQL,
-- jadi minta pemiliknya daftar ulang atau reset lewat aplikasi.
-- =====================================================================
-- ALTER TABLE users CHANGE password password_hash VARCHAR(255) NOT NULL;
-- ALTER TABLE users MODIFY role ENUM('asdos','dosen','mahasiswa') NOT NULL;
-- ALTER TABLE users ADD COLUMN nama VARCHAR(100) NOT NULL DEFAULT '' AFTER role;
-- ALTER TABLE users ADD COLUMN id_mahasiswa BIGINT NULL;
-- ALTER TABLE users ADD COLUMN nidn VARCHAR(20) NULL;
-- ALTER TABLE users ADD COLUMN status ENUM('aktif','nonaktif') NOT NULL DEFAULT 'aktif';
-- ALTER TABLE users ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- =====================================================================
-- QUERY YANG DIPAKAI APLIKASI (sudah ada di models/user_model.py)
-- =====================================================================
-- Ambil akun untuk login (hash dibandingkan di Python):
--   SELECT id_user, username, password_hash, role, nama, id_mahasiswa, nidn, status
--   FROM users WHERE username = %s
--
-- Daftar akun baru:
--   INSERT INTO users (username, password_hash, role, nama, id_mahasiswa, nidn)
--   VALUES (%s, %s, %s, %s, %s, %s)

-- =====================================================================
-- QUERY BANTU UNTUK PENGECEKAN / DEMO
-- =====================================================================
-- Jumlah akun per aktor:
-- SELECT role, COUNT(*) AS jumlah FROM users GROUP BY role;

-- Daftar akun (hash sengaja tidak ditampilkan):
-- SELECT id_user, username, role, nama, status, created_at FROM users ORDER BY id_user;

-- Akun mahasiswa beserta data NIM-nya:
-- SELECT u.username, m.nim, m.nama, m.kelas
-- FROM users u JOIN mahasiswa m ON u.id_mahasiswa = m.id_mahasiswa
-- WHERE u.role = 'mahasiswa';

-- Nonaktifkan / aktifkan akun:
-- UPDATE users SET status = 'nonaktif' WHERE username = 'contoh';
-- UPDATE users SET status = 'aktif'    WHERE username = 'contoh';

-- Pastikan tidak ada password tersimpan sebagai teks biasa (hash PBKDF2 diawali 'pbkdf2_sha256$'):
-- SELECT username FROM users WHERE password_hash NOT LIKE 'pbkdf2_sha256$%';
