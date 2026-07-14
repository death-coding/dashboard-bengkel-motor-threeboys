"""
=========================================================
VALIDATOR DATASET POS
=========================================================
Digunakan untuk memvalidasi file CSV sebelum diproses.

Tahapan:
1. Memastikan file tidak kosong
2. Memastikan separator benar
3. Memastikan kolom wajib tersedia
4. Menghapus spasi pada nama kolom
=========================================================
"""

import pandas as pd

# =====================================================
# Membaca CSV otomatis (; atau ,)
# =====================================================
def baca_csv(uploaded_file):
    """
    Membaca file CSV tanpa pengguna perlu tahu separator.
    Return
    ------
    dataframe
    """
    try:
        df = pd.read_csv(uploaded_file, sep=";")
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    return df


# =====================================================
# Mengecek dataframe kosong
# =====================================================
def cek_kosong(df):
    if df.empty:
        raise ValueError(
            "Dataset kosong."
        )
    return True


# =====================================================
# Mengecek kolom wajib
# =====================================================
def cek_kolom(df, kolom_wajib):
    kolom_df = list(df.columns)
    hilang = []
    for kolom in kolom_wajib:
        if kolom not in kolom_df:
            hilang.append(kolom)
    if len(hilang) > 0:
        raise ValueError(
            "Kolom berikut tidak ditemukan : "
            + ", ".join(hilang)
        )
    return True

# =====================================================
# Menghapus spasi nama kolom
# =====================================================
def bersihkan_nama_kolom(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", "")
        .str.replace("\t", "")
    )
    return df

# =====================================================
# Ringkasan Dataset
# =====================================================
def ringkasan_dataset(df):
    info = {
        "jumlah_baris": df.shape[0],
        "jumlah_kolom": df.shape[1],
        "nama_kolom": list(df.columns)
    }
    return info

# =====================================================
# Validator lengkap
# =====================================================
def validasi_dataset(df, kolom_wajib):
    df = bersihkan_nama_kolom(df)
    cek_kosong(df)
    cek_kolom(df, kolom_wajib)
    return True