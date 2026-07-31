import streamlit as st
import pandas as pd
import altair as alt  
from modules.preprocess import proses_dataset
from modules.apriori import proses_apriori

st.set_page_config(page_title="Rekomendasi Bundling", page_icon="📈", layout="wide")

# ==========================================
# BAGIAN ATAS: LOGO & JUDUL
# ==========================================
col_logo, col_judul = st.columns([1, 8]) 

with col_logo:
    try:
        st.image("skripsi-dashboard-threeboys/assets/logo-bengkel.jpg", use_container_width=True)
    except Exception:
        pass 

with col_judul:
    st.title("Dasbor Rekomendasi Bundling Bengkel Motor Three Boys")
    st.write("Unggah laporan transaksi kasir (Ekspor CSV 3-6 bulan terakhir dari database). Sistem akan otomatis mencari paket barang & jasa yang sering dibeli bersamaan.")

st.markdown("---")

# ==========================================
# BAGIAN TENGAH: PENGATURAN PARAMETER
# ==========================================
st.header("⚙️ Pengaturan Pencarian")
st.write("Sesuaikan angka di bawah jika hasil paket dirasa terlalu sedikit atau terlalu banyak.")

col_slider1, col_slider2 = st.columns(2)

with col_slider1:
    support_persen = st.slider(
        "Batas Minimal Terjual Bersamaan (%)",
        min_value=0.10,
        max_value=5.00,
        value=0.50,
        step=0.10,
        format="%.2f%%"
    )
    # Teks dinamis yang otomatis berubah mengikuti tarikan slider
    jumlah_nota = int(support_persen * 10)
    st.caption(f"💡 **Penjelasan:** Angka {support_persen:.2f}% berarti kombinasi barang minimal pernah muncul di **{jumlah_nota} dari 1000** nota pelanggan.")

with col_slider2:
    confidence_persen = st.slider(
        "Tingkat Kepastian Pasangan (%)",
        min_value=5,
        max_value=100,
        value=10,
        step=5,
        format="%d%%"
    )
    # Teks dinamis yang otomatis berubah mengikuti tarikan slider
    st.caption(f"💡 **Penjelasan:** Angka {confidence_persen}% berarti jika barang A dibeli, ada kepastian minimal **{confidence_persen}%** barang B pasti ikut dibeli.")

st.markdown("<br>", unsafe_allow_html=True) 

# ==========================================
# BAGIAN BAWAH: UPLOAD FILE & PROSES ANALISIS
# ==========================================
col_up1, col_up2 = st.columns(2)
with col_up1:
    st.info("📦 WAJIB: Upload Laporan Barang")
    file_barang = st.file_uploader("Upload tbl_jual_detail.csv", type=["csv"])
with col_up2:
    st.info("🔧 OPSIONAL: Upload Laporan Servis")
    file_servis = st.file_uploader("Upload tbl_jasaservis_detail.csv", type=["csv"])

if file_barang is not None:
    try:
        df_barang = pd.read_csv(file_barang, sep=None, engine='python')
        
        # --- VALIDASI FILE BARANG ---
        kolom_wajib_barang = {'no_jual', 'nama_brg'}
        if not kolom_wajib_barang.issubset(df_barang.columns):
            st.error("❌ ERROR: Data Barang Tidak Sesuai!")
            st.warning("Pastikan Anda mengunggah file **tbl_jual_detail.csv**. Sistem mendeteksi Anda mungkin salah memasukkan tabel master data.")
            st.stop()
            
        df_servis = None
        if file_servis is not None:
            df_servis = pd.read_csv(file_servis, sep=None, engine='python')
            
            # --- VALIDASI FILE SERVIS ---
            kolom_wajib_servis = {'no_servis', 'nama_servis'}
            if not kolom_wajib_servis.issubset(df_servis.columns):
                st.error("❌ ERROR: Data Jasa Servis Tidak Sesuai!")
                st.warning("Pastikan Anda mengunggah file **tbl_jasaservis_detail.csv**.")
                st.stop()
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            mulai_proses = st.button("🚀 Cari Paket Rekomendasi Sekarang", use_container_width=True)
            
        if mulai_proses:
            with st.spinner("Sistem sedang menganalisis ribuan data transaksi Anda..."):
                basket = proses_dataset(df_barang, df_servis)
                support_decimal = support_persen / 100
                confidence_decimal = confidence_persen / 100
                frequent, rules, matrix = proses_apriori(basket, support_decimal, confidence_decimal)

            st.success("Analisis selesai! Berikut adalah hasilnya:")

            # Dashboard Ringkasan Metrik
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Nota Transaksi", matrix.shape[0])
            c2.metric("Total Jenis Barang/Servis", matrix.shape[1])
            c3.metric("Paket Promo Ditemukan", len(rules))

            st.divider()
            st.subheader("💡 Tabel Rekomendasi Paket Promo (Bundling)")

            if len(rules) == 0:
                st.warning("Belum ditemukan pola kebiasaan pelanggan yang kuat. Silakan geser pengaturan ke angka yang lebih rendah.")
            else:
                hasil = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
                hasil["antecedents"] = hasil["antecedents"].apply(lambda x: " + ".join(list(x)))
                hasil["consequents"] = hasil["consequents"].apply(lambda x: " + ".join(list(x)))
                
                df_grafik = hasil.copy()
                df_grafik['Nama Paket'] = df_grafik['antecedents'] + " ➔ " + df_grafik['consequents']
                
                hasil = hasil.rename(columns={
                    "antecedents": "Jika Pelanggan Beli",
                    "consequents": "Maka Tawarkan Ini",
                    "support": "Frekuensi Muncul",
                    "confidence": "Peluang Sukses",
                    "lift": "Kekuatan Hubungan (Lift)"
                })
                
                hasil['Frekuensi Muncul'] = (hasil['Frekuensi Muncul'] * 100).apply(lambda x: f"{x:.2f}%")
                hasil['Peluang Sukses'] = (hasil['Peluang Sukses'] * 100).apply(lambda x: f"{x:.2f}%")
                hasil['Kekuatan Hubungan (Lift)'] = hasil['Kekuatan Hubungan (Lift)'].apply(lambda x: f"{x:.2f} x Lipat")

                st.dataframe(hasil, use_container_width=True)

                csv_export = hasil.to_csv(index=False, sep=";").encode("utf-8-sig")
                st.download_button(
                    label="📥 Download Hasil Tabel Disini",
                    data=csv_export,
                    file_name="hasil_rekomendasi_threeboys.csv",
                    mime="text/csv"
                )

                st.divider()
                
                st.subheader("📊 Visualisasi Performa Paket Rekomendasi")
                
                top_confidence = df_grafik.sort_values('confidence', ascending=False).head(5)
                top_lift = df_grafik.sort_values('lift', ascending=False).head(5)

                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.markdown("**Top 5 Paket dengan Peluang Sukses Tertinggi**")
                    chart1 = alt.Chart(top_confidence).mark_bar(color='#4CAF50', cornerRadiusEnd=4).encode(
                        x=alt.X('confidence:Q', title='Peluang Sukses (Confidence)', axis=alt.Axis(format='%')),
                        y=alt.Y('Nama Paket:N', sort='-x', title='Kombinasi Paket'),
                        tooltip=[alt.Tooltip('Nama Paket:N', title='Paket'), alt.Tooltip('confidence:Q', title='Peluang', format='.2%')]
                    ).properties(height=350)
                    st.altair_chart(chart1, use_container_width=True)

                with col_chart2:
                    st.markdown("**Top 5 Paket dengan Kekuatan Hubungan (Lift) Tertinggi**")
                    chart2 = alt.Chart(top_lift).mark_bar(color='#FF9800', cornerRadiusEnd=4).encode(
                        x=alt.X('lift:Q', title='Kekuatan Hubungan (x Lipat)'),
                        y=alt.Y('Nama Paket:N', sort='-x', title='Kombinasi Paket'),
                        tooltip=[alt.Tooltip('Nama Paket:N', title='Paket'), alt.Tooltip('lift:Q', title='Lift', format='.2f')]
                    ).properties(height=350)
                    st.altair_chart(chart2, use_container_width=True)
                    
    except Exception as e:
        st.error(f"Terjadi kesalahan teknis: {e}")
