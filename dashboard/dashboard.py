import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Mengatur style seaborn
sns.set(style="whitegrid")

# Menentukan path yang fleksibel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "main_data.csv")
LOGO_PATH = os.path.join(BASE_DIR, "logo.jpg")

# Membaca data dengan path yang benar
df_day = pd.read_csv(CSV_PATH)

# Mengonversi kolom 'date' menjadi datetime
df_day['date'] = pd.to_datetime(df_day['date'], format="%Y-%m-%d", errors='coerce')

# Menghapus baris dengan nilai 'date' yang NaT
df_day = df_day.dropna(subset=['date'])

# Fungsi untuk mengkodekan gambar menjadi base64
def img_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Sidebar dengan logo dan filter tanggal
with st.sidebar:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/jpg;base64,{img_to_base64(LOGO_PATH)}" width="150">
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.title('Penyewaan Sepeda Dashboard')

    start_date, end_date = st.date_input(
        'Pilih Rentang Waktu',
        [df_day['date'].min(), df_day['date'].max()],
        df_day['date'].min(), df_day['date'].max()
    )

    show_dataset = st.checkbox("Tampilkan Dataset", value=True)
    show_season_rentals = st.checkbox("Tampilkan Visualisasi Musim", value=True)
    show_weather_rentals = st.checkbox("Tampilkan Visualisasi Cuaca", value=True)

# Filter data berdasarkan rentang tanggal
filtered_df = df_day[(df_day['date'] >= pd.to_datetime(start_date)) & (df_day['date'] <= pd.to_datetime(end_date))]

st.header('Dashboard Penyewaan Sepeda')

# Menampilkan dataset
if show_dataset:
    st.subheader("Dataset")
    st.write(filtered_df)
    st.write("""
        Dataset ini berisi data penyewaan sepeda, termasuk informasi seperti tanggal, jam, musim, cuaca, jumlah penyewa terdaftar (registered), dan jumlah penyewa kasual (casual).
        Tujuan utama dari dataset ini adalah untuk menganalisis pola penyewaan sepeda dan faktor-faktor yang mempengaruhinya.
    """)

# Visualisasi Musim
if show_season_rentals:
    st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim")
    season_rentals = filtered_df.groupby('season')[['registered', 'casual']].sum().reset_index()
    season_rentals_melted = season_rentals.melt(id_vars=['season'], value_vars=['registered', 'casual'],
                                                var_name='rental_type', value_name='total_rentals')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='total_rentals', hue='rental_type', data=season_rentals_melted, palette='Set2', ax=ax1)
    ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Jumlah Penyewaan Sepeda')
    ax1.legend(title='Tipe Penyewaan')
    st.pyplot(fig1)
    st.write("""
        Grafik ini menampilkan jumlah penyewaan sepeda (terdaftar dan kasual) untuk setiap musim.
        Memungkinkan kita untuk melihat musim mana yang memiliki jumlah penyewaan tertinggi. 
        Barplot digunakan untuk memvisualisasikan perbandingan jumlah penyewaan sepeda berdasarkan musim. 
        
        Data ini menunjukkan jumlah penyewaan untuk setiap jenis penyewa (registered dan casual). 
        Berdasarkan hasil eksplorasi, bisa dilihat bahwa musim fall memiliki jumlah penyewaan terbanyak, 
        sedangkan springer adalah musim dengan jumlah penyewaan terendah.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Persentase Penyewaan Sepeda Berdasarkan Musim")
    season_rentals['total_rentals'] = season_rentals['registered'] + season_rentals['casual']
    total_rentals_all_seasons = season_rentals['total_rentals'].sum()
    season_rentals['percentage'] = (season_rentals['total_rentals'] / total_rentals_all_seasons) * 100
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='percentage', data=season_rentals, palette='Set2', ax=ax2)
    ax2.set_title('Persentase Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Persentase Penyewaan (%)')
    st.pyplot(fig2)
    st.write("""
        Grafik ini menampilkan persentase penyewaan sepeda untuk setiap musim.
        Memberikan gambaran proporsi penyewaan di setiap musim terhadap total penyewaan.
        Dengan adanya visualisasi ini, kita bisa melihat musim apa saja yang paling diminati oleh pelanggan untuk menyewa sepeda.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

# Visualisasi Cuaca
if show_weather_rentals:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
    weather_rentals = filtered_df.groupby('weather')[['registered', 'casual']].sum().reset_index()
    heatmap_data = weather_rentals[['weather', 'registered', 'casual']].set_index('weather')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data.T, annot=True, cmap='coolwarm', fmt='g', cbar_kws={'label': 'Jumlah Penyewaan Sepeda'}, ax=ax3)
    ax3.set_title('Peta Panas Pengaruh Cuaca terhadap Penyewaan Sepeda', fontsize=16)
    ax3.set_xlabel('Kondisi Cuaca')
    ax3.set_ylabel('Tipe Penyewaan')
    st.pyplot(fig3)
    st.write("""
        Heatmap ini menampilkan korelasi antara kondisi cuaca dan jumlah penyewaan sepeda (terdaftar dan kasual).
        Memungkinkan kita untuk melihat kondisi cuaca mana yang paling kondusif untuk penyewaan sepeda.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Persentase Penyewaan Sepeda Berdasarkan Cuaca")
    weather_rentals['total_rentals'] = weather_rentals['registered'] + weather_rentals['casual']
    total_rentals_all_weather = weather_rentals['total_rentals'].sum()
    weather_rentals['percentage'] = (weather_rentals['total_rentals'] / total_rentals_all_weather) * 100
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    ax4.pie(weather_rentals['percentage'], labels=weather_rentals['weather'], autopct='%1.1f%%', startangle=90, 
            wedgeprops={'width': 0.3}, colors=sns.color_palette('Set3', len(weather_rentals)))
    ax4.set_title('Persentase Penyewaan Sepeda Berdasarkan Cuaca', fontsize=16)
    ax4.axis('equal')
    st.pyplot(fig4)
    st.write("""
        Donut Chart ini menampilkan persentase penyewaan sepeda untuk setiap kondisi cuaca.
        Memberikan gambaran proporsi penyewaan di setiap kondisi cuaca terhadap total penyewaan.
        Dengan adanya visualisasi ini, kita bisa melihat bagaimana pengaruh cuaca terhadap jumlah penyewa sepeda.
             
        Barplot menunjukkan pengaruh kondisi cuaca terhadap total penyewaan sepeda. 
        Misalnya, cuaca cerah (clear) kemungkinan akan memiliki jumlah penyewaan yang lebih tinggi dibandingkan dengan cuaca hujan. 
        Visualisasi ini juga akan menunjukkan persentase penyewaan sepeda berdasarkan kondisi cuaca. 
        Dan dapat dengan jelas dilihat cuaca mana yang memiliki kontribusi terbesar terhadap penyewaan sepeda.
    """)

st.markdown("""
<style>
.footer {
    left: 0;
    bottom: 0;
    width: 100%;
    color: white;
    text-align: center;
    padding: 10px;
}
</style>
<div class="footer">    
    <p>Copyright © 2025 Penyewaan Sepeda</p>
</div>
""", unsafe_allow_html=True)