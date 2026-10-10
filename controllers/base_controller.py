from datetime import datetime


def hasil(sukses, pesan, data=None):
    return {"sukses": sukses, "pesan": pesan, "data": data}


def kosong(nilai):
    return nilai is None or str(nilai).strip() == ""


def ke_int(nilai):
    try:
        return int(str(nilai).strip())
    except (ValueError, TypeError):
        return None


def ke_float(nilai):
    try:
        return float(str(nilai).strip().replace(",", "."))
    except (ValueError, TypeError):
        return None


def valid_tanggal(teks, dengan_jam=False):
    fmt = "%Y-%m-%d %H:%M:%S" if dengan_jam else "%Y-%m-%d"
    try:
        datetime.strptime(str(teks).strip(), fmt)
        return True
    except ValueError:
        return False


def cari_by_id(model, kunci, id_):
    """Cari satu baris dari model.get_all() berdasarkan kolom id."""
    return next((d for d in model.get_all() if d.get(kunci) == id_), None)


def hasil_eksekusi(model, affected, pesan_ok, pesan_nol="Tidak ada perubahan data."):
    """Terjemahkan return Database.execute() (None = error SQL)."""
    if affected is None:
        return hasil(False, f"Gagal: {model.db.last_error}")
    if affected == 0:
        return hasil(False, pesan_nol)
    return hasil(True, pesan_ok)
