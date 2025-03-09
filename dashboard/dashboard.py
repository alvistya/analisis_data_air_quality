import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
st_cleaned_tiantan = pd.read_csv('/mount/src/analisis_data_air_quality/dashboard/cleaned_Tiantan.csv', parse_dates=['datetime'])
st_cleaned_shunyi = pd.read_csv('/mount/src/analisis_data_air_quality/dashboard/cleaned_Shunyi.csv', parse_dates=['datetime'])
st_cleaned_wanliu = pd.read_csv('/mount/src/analisis_data_air_quality/dashboard/cleaned_Wanliu.csv', parse_dates=['datetime'])

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Hitung rata-rata tahunan
st_tiantan_avg = st_cleaned_tiantan.groupby(st_cleaned_tiantan['datetime'].dt.year)[pollutants].mean()
st_shunyi_avg = st_cleaned_shunyi.groupby(st_cleaned_shunyi['datetime'].dt.year)[pollutants].mean()
st_wanliu_avg = st_cleaned_wanliu.groupby(st_cleaned_wanliu['datetime'].dt.year)[pollutants].mean()

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
    plt.figure(figsize=(10, 5))
    sns.heatmap(comparison_df, annot=True, fmt=".1f", cmap="coolwarm")
    plt.title("Perbandingan Rata-rata Kualitas Udara (2013-2017)")
    plt.xlabel("Polutan")
    plt.ylabel("Stasiun")
    st.pyplot(plt)

elif st.session_state.selected_button == "Tren Polusi":
    st.title("📈 Tren Polusi Udara (2013-2017)")
    pollutant_choice = st.selectbox("Pilih Polutan:", pollutants)
    plt.figure(figsize=(8, 4))
    plt.plot(st_tiantan_avg.index, st_tiantan_avg[pollutant_choice], label="Tiantan", marker='o')
    plt.plot(st_shunyi_avg.index, st_shunyi_avg[pollutant_choice], label="Shunyi", marker='s')
    plt.plot(st_wanliu_avg.index, st_wanliu_avg[pollutant_choice], label="Wanliu", marker='^')
    plt.xlabel("Tahun")
    plt.ylabel("Konsentrasi (µg/m³ atau mg/m³)")
    plt.legend()
    plt.title(f"Tren {pollutant_choice} di Tiantan, Shunyi, Wanliu")
    st.pyplot(plt)

elif st.session_state.selected_button == "Kadar Polutan":
    st.title("🌍 Kadar Polutan - CO2")

    # Slider untuk input kadar CO2
    kadar = st.slider("Masukkan kadar CO2 (µg/m³ atau mg/m³)", 0, 500, 100)
    st.write(f"**Kadar CO2:** {kadar} µg/m³")

    # Menampilkan gambar berdasarkan kadar CO2
    if kadar < 50:
        st.image("/mount/src/analisis_data_air_quality/dashboard/assets/good.jpg", caption="Kualitas Udara Baik 😊")
    elif kadar < 100:
        st.image("/mount/src/analisis_data_air_quality/dashboard/assets/moderate.jpeg", caption="Kualitas Udara Sedang 😐")
    elif kadar < 200:
        st.image("/mount/src/analisis_data_air_quality/dashboard/assets/unhealthy.jpg", caption="Kualitas Udara Tidak Sehat 😷")
    else:
        st.image("/mount/src/analisis_data_air_quality/dashboard/assets/hazardous.jpeg", caption="Kualitas Udara Berbahaya ☠️")

