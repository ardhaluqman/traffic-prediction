import streamlit as st
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt

# Load the trained models
volume_model = pickle.load(open('traffic_volume_model.pkl', 'rb'))
class_model = pickle.load(open('traffic_class_model.pkl', 'rb'))

# Set page configuration
st.set_page_config(
    page_title="Prediksi Volume Lalu Lintas",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styles for modern UI
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;
    }
    .main-header {
        font-size: 2.8em;
        font-weight: bold;
        text-align: center;
        color: #0d6efd;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .sub-header {
        font-size: 1.4em;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .result-box {
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        font-size: 1.5em;
    }
    .low {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .medium {
        background: linear-gradient(135deg, #fff3cd, #ffeeba);
        color: #856404;
        border: 1px solid #ffeeba;
    }
    .high {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .volume-text {
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .traffic-icon {
        font-size: 3em;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add header
st.markdown(
    """
    <div class="main-header">🚦 Prediksi Volume Lalu Lintas 🚦</div>
    <div class="sub-header">Masukkan kondisi pada sidebar untuk memulai prediksi</div>
    """,
    unsafe_allow_html=True
)

# Sidebar input
st.sidebar.header("🌟 Masukkan Kondisi Prediksi")
temp = st.sidebar.number_input("🌡️ Suhu (Kelvin):", min_value=200.0, max_value=350.0, value=290.0)
rain_1h = st.sidebar.number_input("🌧️ Curah hujan dalam 1 jam terakhir (mm):", min_value=0.0, value=0.0)
snow_1h = st.sidebar.number_input("❄️ Curah salju dalam 1 jam terakhir (mm):", min_value=0.0, value=0.0)
clouds_all = st.sidebar.slider("☁️ Persentase tutupan awan (%):", min_value=0, max_value=100, value=50)
hour = st.sidebar.slider("⏰ Jam:", min_value=0, max_value=23, value=12)
day = st.sidebar.slider("📅 Hari dalam bulan:", min_value=1, max_value=31, value=15)
month = st.sidebar.slider("📆 Bulan:", min_value=1, max_value=12, value=6)
holiday = st.sidebar.selectbox("🎉 Status hari libur:", ['None', 'Christmas Day', 'Labor Day', 'New Year\'s Day', 'Thanksgiving Day', 'Washington\'s Birthday'])
weather_main = st.sidebar.selectbox("🌤️ Kondisi cuaca:", ['Clear', 'Clouds', 'Drizzle', 'Fog', 'Haze', 'Mist', 'Rain', 'Snow', 'Thunderstorm'])

# Prepare input data as DataFrame
input_data = pd.DataFrame({
    'holiday': [holiday],
    'weather_main': [weather_main],
    'temp': [temp],
    'rain_1h': [rain_1h],
    'snow_1h': [snow_1h],
    'clouds_all': [clouds_all],
    'hour': [hour],
    'day': [day],
    'month': [month]
})

# Prediction button
if st.sidebar.button("🔍 Prediksi Volume Lalu Lintas"):
    with st.spinner("⏳ Memproses prediksi..."):
        time.sleep(2)  # Simulate processing time
        volume_prediction = volume_model.predict(input_data)[0]
        class_prediction = class_model.predict(input_data)[0]

    # Define style classes and icons based on traffic classification
    if class_prediction == "Low Traffic":
        result_class = "low"
        result_icon = "🟢"
        result_text = "Lalu Lintas Rendah"
    elif class_prediction == "Medium Traffic":
        result_class = "medium"
        result_icon = "🟡"
        result_text = "Lalu Lintas Sedang"
    else:
        result_class = "high"
        result_icon = "🔴"
        result_text = "Lalu Lintas Tinggi"

    # Tampilkan hasil prediksi
    st.markdown("## 🔍 Hasil Prediksi Lalu Lintas")
    col1, col2 = st.columns(2)

    # Kolom 1: Informasi Prediksi
    with col1:
        st.markdown(
            f"""
            <div class="result-box {result_class}">
                <div class="traffic-icon">{result_icon}</div>
                <div class="volume-text"> Sekitar {int(volume_prediction)} Kendaraan</div>
                <div>{result_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Kolom 2: Detail Input
    with col2:
        st.markdown("### Ringkasan Kondisi Input")
        st.write(f"**Suhu (Kelvin):** {temp}")
        st.write(f"**Hujan (mm):** {rain_1h}")
        st.write(f"**Salju (mm):** {snow_1h}")
        st.write(f"**Awan (%):** {clouds_all}")
        st.write(f"**Jam:** {hour}")
        st.write(f"**Hari dalam bulan:** {day}")
        st.write(f"**Bulan:** {month}")
        st.write(f"**Hari Libur:** {holiday}")
        st.write(f"**Kondisi Cuaca:** {weather_main}")

    # Tabs untuk visualisasi dan info tambahan
    tabs = st.tabs(["📊 Visualisasi Input", "ℹ️ Informasi Tambahan"])

    # Tab 1: Visualisasi Input
    with tabs[0]:
        st.markdown("### Diagram Input Prediksi")
        fig, ax = plt.subplots(figsize=(10, 6))
        input_summary = {
            "Suhu": temp,
            "Hujan (mm)": rain_1h,
            "Salju (mm)": snow_1h,
            "Awan (%)": clouds_all,
            "Jam": hour,
            "Hari": day,
            "Bulan": month,
        }
        ax.bar(input_summary.keys(), input_summary.values(), color='skyblue')
        ax.set_title("Ringkasan Input Prediksi", fontsize=16, fontweight="bold")
        ax.set_ylabel("Nilai")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        st.pyplot(fig)

    # Tab 2: Informasi Tambahan
    with tabs[1]:
        st.markdown("### Informasi Tambahan")
        st.write("Berikut adalah beberapa poin yang dapat membantu interpretasi hasil prediksi:")
        st.write("- **Lalu lintas rendah** biasanya terjadi pada malam hari atau saat cuaca cerah.")
        st.write("- **Lalu lintas sedang** sering terjadi pada jam sibuk, seperti pagi hari kerja.")
        st.write("- **Lalu lintas tinggi** mungkin disebabkan oleh hujan lebat atau hari libur tertentu.")
        st.info("📌 **Catatan:** Hasil prediksi hanya estimasi berdasarkan data historis.")

    # Expander untuk melihat data input secara detail
    with st.expander("Lihat data input mentah"):
        st.write(input_data)
