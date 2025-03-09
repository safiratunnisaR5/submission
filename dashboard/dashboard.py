import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Mengubah style seaborn
sns.set(style='darkgrid')

# Menyiapkan dataframe yang diperlukan (dari analisis sebelumnya)
def create_rfm_recap(df):
    # Memastikan kolom 'date' dan 'hr' ada
    if 'date' not in df.columns or 'hr' not in df.columns:
        raise KeyError("Kolom 'date' atau 'hr' tidak ditemukan dalam dataset.")
    if 'total' not in df.columns:
        raise KeyError("Kolom 'total' tidak ditemukan dalam dataset.")

    # Membuat ID sesi unik
    df['session_id'] = df['date'].astype(str) + '_' + df['hr'].astype(str)

    today_date = df['date'].max() + pd.Timedelta(days=1)  # Hari berikutnya untuk menghitung recency
    rfm_df = df.groupby('session_id').agg(
        recency=('date', lambda x: (today_date - x.max()).days),  # Waktu sejak penyewaan terakhir
        frequency=('session_id', 'count'),  # Jumlah penyewaan
        monetary=('total', 'sum')  # Jumlah total penyewaan sepeda
    ).reset_index()

    return rfm_df

# Membaca data (sesuaikan dengan nama file atau sumber data yang digunakan)
df_day = pd.read_csv("dashboard/main_data.csv")  # Gantilah sesuai dengan nama dataset

# Mengonversi kolom 'date' menjadi datetime
df_day['date'] = pd.to_datetime(df_day['date'], errors='coerce')

# Menghilangkan baris dengan nilai 'date' yang tidak valid (NaT)
df_day = df_day.dropna(subset=['date'])

# Membuat RFM recap
rfm_recap_df = create_rfm_recap(df_day)

# Filter tanggal pada sidebar
min_date = df_day['date'].min()
max_date = df_day['date'].max()

# Tambahkan CSS untuk mengubah latar belakang dan sidebar
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    [data-testid="stSidebar"] {
        background-color: pink;
    }
    .stApp {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.image("dashboard/logo.jpg", width=150)  # Logo sewa sepeda
    st.title('Penyewaan Sepeda Dashboard')

    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Menampilkan data jika dicentang

    # Checkbox untuk menampilkan dataset
    show_dataset = st.checkbox("Tampilkan Dataset")

    show_rfm = st.checkbox("Tampilkan RFM Metrics")

    show_rfm_details = st.checkbox("Tampilkan Informasi Lengkap RFM")



# Filter data berdasarkan rentang waktu yang dipilih
filtered_df = df_day[(df_day['date'] >= pd.to_datetime(start_date)) & (df_day['date'] <= pd.to_datetime(end_date))]

# Update RFM recap berdasarkan rentang waktu yang dipilih
rfm_recap_df = create_rfm_recap(filtered_df)

# Membuat UI Dashboard


st.header('Dashboard Penyewaan Sepeda')

# RFM Metrics: Recency, Frequency, and Monetary
# **Selalu hitung dan simpan data RFM agar bisa digunakan di grafik**
top_recency = rfm_recap_df.sort_values(by='recency', ascending=True).head(5)
top_frequency = rfm_recap_df.sort_values(by='frequency', ascending=False).head(5)
top_monetary = rfm_recap_df.sort_values(by='monetary', ascending=False).head(5)

if show_dataset:
    st.subheader("Dataset")
    st.write(df_day)

if show_rfm:
    st.subheader("RFM Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Top 5 Recency (Hari Terakhir Menyewa)")
        st.write(top_recency[['session_id', 'recency']])

    with col2:
        st.subheader("Top 5 Frequency (Penyewaan Terbanyak)")
        st.write(top_frequency[['session_id', 'frequency']])

    with col3:
        st.subheader("Top 5 Monetary (Pendapatan Tertinggi)")
        st.write(top_monetary[['session_id', 'monetary']])

# **Visualisasi tetap tampil tanpa tergantung checkbox**
st.subheader('Visualisasi RFM')

col1, col2, col3 = st.columns(3)

# Plot Recency
with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    barplot = sns.barplot(data=top_recency, x='session_id', y='recency', ax=ax, color='tab:blue')
    ax.set_title("Recency (Hari Terakhir Menyewa)", fontsize=15)
    ax.set_ylabel("Recency (Hari)", fontsize=12)
    ax.set_xlabel("Session ID", fontsize=12)
    for bar in barplot.patches:
        barplot.annotate(format(bar.get_height(), '.0f'),
                         (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                         ha='center', va='center',
                         xytext=(0, 5),
                         textcoords='offset points')
    st.pyplot(fig)

# Plot Frequency
with col2:
    fig, ax = plt.subplots(figsize=(8, 5))
    barplot = sns.barplot(data=top_frequency, x='session_id', y='frequency', ax=ax, color='tab:green')
    ax.set_title("Frequency (Penyewaan Terbanyak)", fontsize=15)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_xlabel("Session ID", fontsize=12)
    for bar in barplot.patches:
        barplot.annotate(format(bar.get_height(), '.0f'),
                         (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                         ha='center', va='center',
                         xytext=(0, 5),
                         textcoords='offset points')
    st.pyplot(fig)

# Plot Monetary
with col3:
    fig, ax = plt.subplots(figsize=(8, 5))
    barplot = sns.barplot(data=top_monetary, x='session_id', y='monetary', ax=ax, color='tab:red')
    ax.set_title("Monetary (Pendapatan Tertinggi)", fontsize=15)
    ax.set_ylabel("Monetary (Total Revenue)", fontsize=12)
    ax.set_xlabel("Session ID", fontsize=12)
    for bar in barplot.patches:
        barplot.annotate(format(bar.get_height(), '.0f'),
                         (bar.get_x() + bar.get_width() / 2., bar.get_height()),
                         ha='center', va='center',
                         xytext=(0, 5),
                         textcoords='offset points')
    st.pyplot(fig)

# Menampilkan tabel RFM yang lebih lengkap
if show_rfm_details:
    st.subheader("Informasi Lengkap RFM")
    st.write(rfm_recap_df)
# Footer dengan copyright
st.caption("Copyright © 2025 Penyewaan Sepeda")
