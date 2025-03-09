import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Paksa backend non-GUI agar kompatibel di Streamlit Cloud
matplotlib.use("Agg")

# Load Data
try:
    st_cleaned_tiantan = pd.read_csv('cleaned_Tiantan.csv', parse_dates=['datetime'])
    st_cleaned_shunyi = pd.read_csv('cleaned_Shunyi.csv', parse_dates=['datetime'])
    st_cleaned_wanliu = pd.read_csv('cleaned_Wanliu.csv', parse_dates=['datetime'])
except FileNotFoundError:
    st.error("File data tidak ditemukan! Pastikan file CSV tersedia atau gunakan `st.file_uploader()`.")

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Hitung rata-rata tahunan
if 'st_cleaned_tiantan' in locals():
    st_tiantan_avg = st_cleaned_tiantan.groupby(st_cleaned_tiantan['datetime'].dt.year)[pollutants].mean()
    st_shunyi_avg = st_cleaned_shunyi.groupby(st_cleaned_shunyi['datetime'].dt.year)[pollutants].mean()
    st_wanliu_avg = st_cleaned_wanliu.groupby(st_cleaned_wanliu['datetime'].dt.year)[pollutants].mean()
else:
    st.stop()

# Sidebar Menu dengan Button
st.sidebar.title("📌 Pilih Visualisasi")

if "selected_button" not in st.session_state:
    st.session_state.selected_button = "Perbandingan Rata-rata"

# Ketika tombol ditekan, ubah state
if st.sidebar.button("Perbandingan Rata-rata"):
    st.session_state.selected_button = "Perbandingan Rata-rata"

if st.sidebar.button("Tren Polusi"):
    st.session_state.selected_button = "Tren Polusi"

if st.sidebar.button("Kadar Polutan"):
    st.session_state.selected_button = "Kadar Polutan"

# Menampilkan Visualisasi Berdasarkan Pilihan
if st.session_state.selected_button == "Perbandingan Rata-rata":
    st.title("📊 Perbandingan Rata-rata Kualitas Udara")
    
    comparison_df = pd.DataFrame({
        'Tiantan': st_tiantan_avg.mean(),
        'Shunyi': st_shunyi_avg.mean(),
        'Wanliu': st_wanliu_avg.mean()
    }).T

    # Perbaikan cara membuat heatmap
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(comparison_df, annot=True, fmt=".1f", cmap="coolwarm", ax=ax)
    ax.set_title("Perbandingan Rata-rata Kualitas Udara (2013-2017)")
    ax.set_xlabel("Polutan")
    ax.set_ylabel("Stasiun")
    
    st.pyplot(fig)  # Harus pakai fig, bukan plt

elif st.session_state.selected_button == "Tren Polusi":
    st.title("📈 Tren Polusi Udara (2013-2017)")
    
    pollutant_choice = st.selectbox("Pilih Polutan:", pollutants)
    
    # Buat grafik dengan cara yang benar
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(st_tiantan_avg.index, st_tiantan_avg[pollutant_choice], label="Tiantan", marker='o')
    ax.plot(st_shunyi_avg.index, st_shunyi_avg[pollutant_choice], label="Shunyi", marker='s')
    ax.plot(st_wanliu_avg.index, st_wanliu_avg[pollutant_choice], label="Wanliu", marker='^')
    
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Konsentrasi (µg/m³ atau mg/m³)")
    ax.legend()
    ax.set_title(f"Tren {pollutant_choice} di Tiantan, Shunyi, Wanliu")
    
    st.pyplot(fig)

elif st.session_state.selected_button == "Kadar Polutan":
    st.title("🌍 Kadar Polutan - CO2")

    # Slider untuk input kadar CO2
    kadar = st.slider("Masukkan kadar CO2 (µg/m³ atau mg/m³)", 0, 500, 100)
    st.write(f"**Kadar CO2:** {kadar} µg/m³")

    # Menampilkan gambar berdasarkan kadar CO2
    if kadar < 50:
        st.image("assets/good.jpg", caption="Kualitas Udara Baik 😊")
    elif kadar < 100:
        st.image("assets/moderate.jpeg", caption="Kualitas Udara Sedang 😐")
    elif kadar < 200:
        st.image("assets/unhealthy.jpg", caption="Kualitas Udara Tidak Sehat 😷")
    else:
        st.image("assets/hazardous.jpeg", caption="Kualitas Udara Berbahaya ☠️")
