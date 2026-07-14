import pandas as pd
import re
from modules.kamus import get_semua_kamus

def normalisasi_teks(teks):
    if pd.isna(teks): return ""
    teks = str(teks).lower().strip()
    teks = re.sub(r'\s+', ' ', teks)
    teks = teks.replace(',', '.')
    teks = re.sub(r'\s*/\s*', ' / ', teks)
    teks = re.sub(r'\s*-\s*', ' ', teks)
    teks = re.sub(r'\s+', ' ', teks)
    return teks.strip()

def ekstrak_data(df):
    """Mendeteksi kolom dan menstandarkan format dari satu dataframe"""
    df.columns = df.columns.str.lower().str.strip()
    # Deteksi kolom faktur
    col_faktur = next((col for col in df.columns if 'jual' in col or 'servis' in col or 'faktur' in col), None)
    # Deteksi kolom nama barang/jasa
    col_item = next((col for col in df.columns if 'nama' in col or 'barang' in col or 'item' in col), None)
    
    if not col_faktur or not col_item:
        return pd.DataFrame() # Return kosong jika format salah

    df_bersih = df.dropna(subset=[col_faktur, col_item]).copy()
    df_bersih['faktur_standar'] = df_bersih[col_faktur]
    df_bersih['item_bersih'] = df_bersih[col_item].apply(normalisasi_teks)
    
    return df_bersih[['faktur_standar', 'item_bersih']]

def proses_dataset(df_barang, df_servis=None):
    """
    Menggabungkan data barang dan servis, menstandarkan nama, 
    dan membentuk list keranjang transaksi.
    """
    list_df = []
    
    # 1. Ekstrak data barang
    if df_barang is not None and not df_barang.empty:
        ekstrak_brg = ekstrak_data(df_barang)
        if not ekstrak_brg.empty:
            list_df.append(ekstrak_brg)
            
    # 2. Ekstrak data servis (jika diunggah)
    if df_servis is not None and not df_servis.empty:
        ekstrak_srv = ekstrak_data(df_servis)
        if not ekstrak_srv.empty:
            list_df.append(ekstrak_srv)

    if not list_df:
        raise ValueError("File CSV tidak dikenali. Pastikan Anda mengunggah format tabel 'detail'.")

    # Gabungkan semua data yang ada
    df_gabungan = pd.concat(list_df, ignore_index=True)
    
    # 3. Terapkan Kamus Standardisasi (Mapping)
    kamus = get_semua_kamus()
    df_gabungan['item_standar'] = df_gabungan['item_bersih'].replace(kamus)
    
    # 4. Hapus duplikat dalam satu transaksi yang sama (misal beli 2 oli mpx di baris berbeda tapi faktur sama)
    df_gabungan = df_gabungan.drop_duplicates(subset=['faktur_standar', 'item_standar'])
    
    # 5. Bentuk keranjang (list of list)
    keranjang = df_gabungan.groupby('faktur_standar')['item_standar'].apply(list).tolist()
    
    return keranjang