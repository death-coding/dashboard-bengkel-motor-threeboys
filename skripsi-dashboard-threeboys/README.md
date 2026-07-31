# 🛒 Sistem Pendukung Keputusan: Rekomendasi Bundling Produk
**Studi Kasus:** Bengkel Motor Three Boys

Aplikasi web berbasis dasbor interaktif ini dibangun untuk membantu manajemen Bengkel Motor Three Boys dalam menemukan pola pembelian pelanggan (Market Basket Analysis) menggunakan **Algoritma Apriori**.

## 🚀 Fitur Utama
- **Upload Fleksibel:** Mendukung upload data transaksi barang dan jasa perbaikan secara bersamaan.
- **Natural Language Processing (NLP):** Dilengkapi modul pembersihan teks dan kamus standardisasi (Data Preprocessing).
- **Machine Learning Otomatis:** Otomatisasi pembentukan *Frequent Itemset* dan *Association Rules*.
- **Parameter Kustom:** Pengguna dapat mengatur *Minimum Support* dan *Confidence* melalui antarmuka (UI).

## 🛠️ Teknologi yang Digunakan
- **Bahasa Pemrograman:** Python 3.12
- **Data Science Library:** Pandas, MLxtend
- **Web Framework:** Streamlit

## 📝 Cara Penggunaan
1. Ekspor data transaksi barang dan jasa dari sistem POS bengkel (format CSV).
2. Unggah file CSV ke dalam sistem dasbor.
3. Atur parameter pendukung, lalu klik "Cari Paket Rekomendasi".
4. Unduh hasil rekomendasi dalam bentuk CSV untuk laporan strategi pemasaran.
