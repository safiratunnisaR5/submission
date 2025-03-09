# Analisis Data Penyewaan Sepeda

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda berdasarkan data harian dan per jam. Analisis ini mencakup eksplorasi data, visualisasi tren, dan pembuatan model sederhana untuk memahami faktor yang mempengaruhi jumlah penyewaan sepeda.

├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
│   └── logo.jpg
├── data
│   ├── day.csv
│   └── hour.csv
├── README.md
├── notebook.ipynb
└── requirements.txt

## Dataset
Proyek ini menggunakan dua dataset utama:
1. `bike_sharing/day.csv` - Dataset penyewaan sepeda secara harian.
2. `bike_sharing/hour.csv` - Dataset penyewaan sepeda secara per jam.

### Struktur Data
Dataset memiliki kolom-kolom berikut:
- `instant`: Indeks unik setiap data.
- `dteday`: Tanggal penyewaan.
- `season`: Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin).
- `yr`: Tahun (0: 2011, 1: 2012).
- `mnth`: Bulan (1–12).
- `hr` (hanya di `hour.csv`): Jam (0–23).
- `holiday`: Apakah hari libur (0: Tidak, 1: Ya).
- `weekday`: Hari dalam seminggu (0: Minggu, 6: Sabtu).
- `workingday`: Hari kerja (0: Tidak, 1: Ya).
- `weathersit`: Kondisi cuaca (1: Cerah, 4: Hujan lebat/salju).
- `temp`: Suhu normalisasi (0–1, dikalikan 41.0 untuk mendapatkan Celcius).
- `atemp`: Suhu terasa (0–1).
- `hum`: Kelembaban relatif (0–1).
- `windspeed`: Kecepatan angin (0–1).
- `casual`: Jumlah pengguna non-terdaftar.
- `registered`: Jumlah pengguna terdaftar.
- `cnt`: Total jumlah penyewaan sepeda.

## Instalasi dan Penggunaan
### 1. Instalasi Paket yang Diperlukan
Sebelum menjalankan kode, pastikan semua dependensi telah diinstal:
```bash
pip install pandas numpy matplotlib seaborn streamlit
```

### 2. Menjalankan Notebook Jupyter
Untuk melihat analisis data secara interaktif, jalankan perintah berikut:
```bash
jupyter notebook Notebook.ipynb
```

### 3. Menjalankan Dashboard Streamlit
Jika proyek ini memiliki visualisasi interaktif dengan Streamlit, jalankan:
```bash
streamlit run dashboard.py
```

## Fitur Analisis
1. **Eksplorasi Data**
   - Menampilkan beberapa baris pertama dari dataset.
   - Menampilkan distribusi variabel seperti suhu, kecepatan angin, dan jumlah penyewaan sepeda.

2. **Visualisasi Data**
   - Grafik jumlah penyewaan sepeda berdasarkan waktu (harian dan per jam).
   - Analisis dampak cuaca dan musim terhadap penyewaan sepeda.
   
3. **Analisis RFM (Recency, Frequency, Monetary)**
   - Menghitung *recency* (berapa lama sejak terakhir menyewa).
   - Menghitung *frequency* (berapa kali pelanggan menyewa sepeda).
   - Menghitung *monetary* (total uang yang dihasilkan dari penyewaan).
   - Menampilkan grafik RFM untuk memahami pola penyewaan pelanggan.

## Hasil Analisis
- Tren Musiman: Penyewaan sepeda meningkat pada musim panas dan menurun saat musim dingin.
- Pengaruh Cuaca: Cuaca buruk mengurangi jumlah penyewaan sepeda.
- Waktu Populer: Jam sibuk (08:00-09:00 & 17:00-18:00) menunjukkan lonjakan pengguna terdaftar.

## Kontributor
- Safiratun Nisa (Developer & Data Analyst)


