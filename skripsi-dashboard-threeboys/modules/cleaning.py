"""
=========================================================
CLEANING DATA
=========================================================

Berisi fungsi untuk:

1. Membersihkan nama kolom
2. Parsing tanggal lama dan baru
3. Normalisasi teks
4. Membersihkan isi kolom
5. Menghapus duplikasi item
=========================================================
"""

import pandas as pd
import re
# =====================================================
# MEMBERSIHKAN NAMA KOLOM
# =====================================================
def bersihkan_kolom(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", "", regex=False)
        .str.replace("\t", "", regex=False)
    )
    return df

# =====================================================
# PARSING TANGGAL
# =====================================================
FORMAT_LAMA = [
    "%d/%m/%Y %H.%M",
    "%d/%m/%Y %H:%M"
]
FORMAT_BARU = "%Y-%m-%d %H:%M:%S"

def parse_tanggal(teks):
    if pd.isna(teks):
        return pd.NaT
    teks = str(teks).strip()
    # format lama
    for fmt in FORMAT_LAMA:
        try:
            return pd.to_datetime(
                teks,
                format=fmt
            )
        except:
            pass
    # format baru
    try:
        return pd.to_datetime(
            teks,
            format=FORMAT_BARU
        )
    except:
        return pd.NaT

# =====================================================
# KONVERSI KOLOM TANGGAL
# =====================================================
def ubah_tanggal(df, nama_kolom):
    df[nama_kolom] = (
        df[nama_kolom]
        .astype(str)
        .apply(parse_tanggal)
    )
    return df

# =====================================================
# FILTER PERIODE
# =====================================================
def filter_tanggal(
        df,
        nama_kolom,
        tanggal_awal,
        tanggal_akhir
):
    tanggal_awal = pd.to_datetime(
        tanggal_awal
    )

    tanggal_akhir = pd.to_datetime(
        tanggal_akhir
    )

    return df[
        (df[nama_kolom] >= tanggal_awal)
        &
        (df[nama_kolom] <= tanggal_akhir)
    ]

# =====================================================
# NORMALISASI TEKS
# =====================================================
def normalisasi_teks(teks):
    if pd.isna(teks):
        return ""
    teks = str(teks)
    teks = teks.lower()
    teks = teks.strip()

    # hilangkan spasi berlebih
    teks = re.sub(
        r"\s+",
        " ",
        teks
    )

    # koma menjadi titik
    teks = teks.replace(",", ".")
    # rapikan slash
    teks = re.sub(
        r"\s*/\s*",
        " / ",
        teks
    )

    # rapikan strip
    teks = re.sub(
        r"\s*-\s*",
        " ",
        teks
    )

    # hilangkan spasi ganda
    teks = re.sub(
        r"\s+",
        " ",
        teks
    )
    return teks.strip()


# =====================================================
# MEMBERSIHKAN KOLOM ITEM
# =====================================================
def buat_item_bersih(
        df,
        nama_kolom
):
    df["item_bersih"] = (
        df[nama_kolom]
        .fillna("")
        .apply(normalisasi_teks)
    )
    return df


# =====================================================
# HAPUS DUPLIKAT ITEM DALAM TRANSAKSI
# =====================================================
def hapus_duplikat_item(
        dataframe,
        kolom_faktur,
        kolom_item
):
    dataframe = (
        dataframe
        .drop_duplicates(
            subset=[
                kolom_faktur,
                kolom_item
            ]
        )
    )
    return dataframe

# =====================================================
# RINGKASAN DATASET
# =====================================================
def info_dataset(df):
    hasil = {
        "Jumlah Baris":
            len(df),
        "Jumlah Kolom":
            len(df.columns),
        "Kolom":
            list(df.columns)
    }
    return hasil


# =====================================================
# PIPELINE CLEANING
# =====================================================
def cleaning_data(
        df,
        kolom_tanggal,
        kolom_item=None
):
    df = bersihkan_kolom(df)
    df = ubah_tanggal(
        df,
        kolom_tanggal
    )
    if kolom_item is not None:
        df = buat_item_bersih(
            df,
            kolom_item
        )
    return df