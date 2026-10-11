# News Scraper — Hilirisasi Batubara

Aplikasi web scraping berita menggunakan Python, SerpApi, Pandas, Requests, dan Trafilatura untuk mengumpulkan metadata serta isi artikel berita terkait hilirisasi batubara di Indonesia.

Project ini dikembangkan untuk membantu pengumpulan dataset penelitian Natural Language Processing (NLP), khususnya analisis sentimen dan Aspect-Based Sentiment Analysis (ABSA) pada berita batubara.

## 1. Fitur

- Mengumpulkan hasil pencarian berita melalui Google News menggunakan SerpApi.
- Mendukung beberapa keyword pencarian.
- Memfilter hasil berdasarkan rentang tahun.
- Menggunakan pagination untuk mendapatkan lebih banyak hasil berita.
- Menghapus URL artikel duplikat.
- Mengekstrak isi artikel menggunakan Trafilatura.
- Membersihkan teks dari whitespace berlebihan.
- Menyimpan dataset dalam format CSV yang kompatibel dengan Microsoft Excel.
- Menyimpan dataset final dan dataset cadangan yang mencakup URL artikel.

## 2. Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python 3.12 | Bahasa pemrograman |
| SerpApi | Mengambil hasil pencarian Google News |
| Pandas | Mengolah dan menyimpan dataset |
| Requests | Library untuk komunikasi HTTP |
| Trafilatura | Mengekstrak isi artikel dari halaman web |
| CSV | Format penyimpanan dataset |

## 3. Struktur Project

```text
data_scrapper/
├── .venv/
├── dataset/
│   ├── dataset_berita_hilirisasi.csv
│   └── dataset_berita_hilirisasi_backup.csv
├── scrap.py
└── README.md
```

Keterangan:

- `.venv/`: virtual environment Python.
- `dataset/`: direktori penyimpanan hasil scraping.
- `scrap.py`: program utama untuk mengambil data berita.
- `README.md`: dokumentasi project.

Folder dan file dataset akan dibuat secara otomatis oleh program ketika proses scraping dijalankan.

## 4. Persyaratan

Pastikan perangkat telah memiliki:

- Windows 10 atau Windows 11.
- Python 3.12 yang dapat dijalankan melalui virtual environment.
- `uv` untuk mengelola instalasi paket Python.
- Akun SerpApi dengan API key yang masih aktif.
- Koneksi internet.

## 5. Mendapatkan API Key SerpApi

1. Buka https://serpapi.com/.
2. Buat akun atau masuk ke akun yang sudah tersedia.
3. Buka dashboard SerpApi.
4. Cari API key pada halaman pengelolaan akun.
5. Salin API key untuk digunakan saat menjalankan program.

Jangan menyimpan API key langsung di dalam source code atau mengunggahnya ke repositori publik.

Jika API key sudah terlanjur terekspos, buat atau aktifkan key pengganti melalui dashboard SerpApi sebelum melanjutkan.

## 6. Instalasi Project

### 6.1. Buka terminal

Jalankan Command Prompt (CMD), kemudian masuk ke direktori project:

```cmd
cd C:\Users\...\...\data_scrapper
```

### 6.2. Buat virtual environment

Jika virtual environment belum tersedia:

```cmd
uv venv --python 3.12
```

### 6.3. Aktifkan virtual environment

```cmd
.venv\Scripts\activate
```

Jika berhasil, terminal akan menampilkan awalan `(data_scrapper)` atau nama environment yang digunakan.

### 6.4. Instal dependensi

```cmd
uv pip install --python .venv\Scripts\python.exe pandas serpapi requests trafilatura
```

Perintah tersebut memasang seluruh library yang dibutuhkan ke virtual environment project.

### 6.5. Verifikasi instalasi

```cmd
python -c "import pandas; import serpapi; import requests; import trafilatura; print('Semua library berhasil diinstal')"
```

Jika berhasil, terminal akan menampilkan:

```text
Semua library berhasil diinstal
```

## 7. Konfigurasi API Key

Karena project dijalankan menggunakan Command Prompt (CMD), gunakan sintaks berikut:

```cmd
set SERPAPI_KEY=API_KEY_KAMU
```

Ganti `API_KEY_KAMU` dengan API key milikmu.

Periksa apakah environment variable sudah tersedia:

```cmd
if defined SERPAPI_KEY (echo API key tersedia) else (echo API key belum tersedia)
```

Variabel yang dibuat menggunakan `set` hanya berlaku selama sesi CMD tersebut masih aktif.

Jika membuka terminal baru, masukkan kembali API key sebelum menjalankan program.

Jangan menuliskan API key asli di README, source code, atau repositori Git.

## 8. Konfigurasi Scraping

Pengaturan utama berada di dalam `scrap.py`.

### 8.1. Keyword pencarian

Contoh keyword yang digunakan:

```python
keywords = [
    "Hilirisasi batubara",
    "Harga Batubara Acuan",
    "Dampak lingkungan tambang"
]
```

Keyword dapat ditambahkan sesuai kebutuhan penelitian.

### 8.2. Rentang tahun

```python
years = range(2020, 2026)
```

Konfigurasi tersebut mencakup tahun 2020 sampai 2025.

### 8.3. Jumlah halaman

```python
MAX_PAGES = 10
```

Setiap kelompok pencarian meminta maksimal 10 halaman, bergantung pada ketersediaan hasil dan penghentian pagination oleh program.

Perhatikan bahwa setiap permintaan pencarian dapat menggunakan search credit SerpApi. Periksa kuota akun sebelum meningkatkan jumlah halaman atau keyword.

## 9. Menjalankan Program

Pastikan virtual environment aktif dan API key telah diatur.

Jalankan:

```cmd
python scrap.py
```

Program akan menjalankan tahapan berikut:

1. Mengirim keyword ke Google News melalui SerpApi.
2. Mengambil metadata berita dari setiap halaman.
3. Memproses pencarian berdasarkan tahun.
4. Menghapus URL duplikat.
5. Mengunjungi URL artikel untuk mencoba mengekstrak isi.
6. Membersihkan teks artikel.
7. Memfilter artikel yang gagal diekstrak atau memiliki isi kurang dari 200 karakter.
8. Menyimpan hasil ke dalam direktori `dataset/`.
9. Menampilkan ringkasan hasil scraping.

## 10. Struktur Dataset

### 10.1. Dataset utama

File:

```text
dataset/dataset_berita_hilirisasi.csv
```

Dataset utama memiliki empat kolom.

| Kolom | Tipe data | Deskripsi |
|---|---|---|
| `title` | String | Judul artikel berita |
| `isi` | String | Isi artikel yang berhasil diekstrak |
| `tanggal` | String | Tanggal atau informasi tanggal dari hasil pencarian |
| `sumber` | String | Nama media atau penerbit berita |

Contoh:

| title | isi | tanggal | sumber |
|---|---|---|---|
| Pemerintah Dorong Hilirisasi Batubara | Pemerintah mendorong pengembangan industri hilirisasi batubara... | 2024-05-12 | CNBC Indonesia |
| Harga Batubara Acuan Mengalami Perubahan | Harga batubara acuan mengalami perubahan berdasarkan kebijakan... | 2023-08-21 | Kontan |

Data pada tabel merupakan ilustrasi struktur, bukan hasil scraping aktual.

### 10.2. Dataset cadangan

File:

```text
dataset/dataset_berita_hilirisasi_backup.csv
```

Dataset cadangan menyimpan informasi tambahan seperti:

- `keyword`
- `title`
- `link`
- `tanggal`
- `sumber`
- `isi`

URL artikel dipertahankan agar sumber data dapat diperiksa kembali dan proses pengumpulan data bisa diaudit.

## 11. Target Jumlah Data

Target penelitian adalah mengumpulkan sekitar 1.000–3.000 artikel berita dengan isi yang berhasil diekstrak.

Jumlah artikel akhir tidak dijamin sama dengan jumlah hasil pencarian karena terdapat kemungkinan:

- URL duplikat.
- Artikel yang sudah dihapus.
- Artikel yang dibatasi paywall.
- Halaman yang gagal diakses.
- Halaman yang tidak dapat diekstrak.
- Hasil pencarian yang tidak relevan dengan penelitian.

Jika jumlah artikel valid belum mencapai target, tambahkan keyword yang relevan, perluas periode penelitian, atau tingkatkan jumlah halaman secara bertahap setelah memeriksa kuota API.

Jangan hanya meningkatkan jumlah halaman karena hasil pencarian dapat berulang.

## 12. Penanganan Masalah

### Error: `ModuleNotFoundError: No module named 'pandas'`

Pasang dependensi ke virtual environment yang digunakan:

```cmd
uv pip install --python .venv\Scripts\python.exe pandas serpapi requests trafilatura
```

### Error: `No module named pip`

Virtual environment mungkin tidak menyediakan `pip`. Gunakan `uv pip install` seperti perintah di atas.

### Error: `SERPAPI_KEY belum ditemukan`

Pastikan API key diatur pada terminal CMD yang sama:

```cmd
set SERPAPI_KEY=API_KEY_KAMU
```

Periksa:

```cmd
if defined SERPAPI_KEY (echo API key tersedia) else (echo API key belum tersedia)
```

### Hasil scraping sedikit

Periksa jumlah keyword, rentang tahun, jumlah halaman, dan hasil deduplikasi. Tambahkan variasi keyword yang masih relevan dengan topik penelitian.

### Isi artikel kosong

Tidak semua situs mengizinkan pengambilan konten atau memiliki struktur halaman yang mudah diekstrak. Periksa URL sumber, koneksi internet, pembatasan akses, dan log program.

Artikel yang gagal diekstrak tidak otomatis berarti artikelnya tidak tersedia.

### API key atau kuota bermasalah

Periksa dashboard SerpApi untuk mengetahui status key, penggunaan pencarian, dan sisa kuota. Jangan menaruh API key di repositori publik atau membagikannya dalam log.

## 13. Catatan Metodologi Penelitian

Untuk menjaga kualitas dataset:

1. Tetapkan kriteria inklusi dan eksklusi artikel.
2. Hapus duplikat berdasarkan URL dan, jika diperlukan, kemiripan judul.
3. Validasi tanggal publikasi.
4. Pastikan isi artikel relevan dengan topik batubara.
5. Simpan URL sumber pada dataset cadangan.
6. Catat jumlah artikel yang ditemukan, duplikat, gagal diekstrak, dan lolos validasi.
7. Periksa ketentuan penggunaan SerpApi dan situs berita terkait pengambilan serta penggunaan konten.

Hasil scraping sebaiknya divalidasi sebelum digunakan sebagai dataset pelatihan atau pengujian model NLP.

## 14. Referensi Dokumentasi

- SerpApi: https://serpapi.com/
- Google News API: https://serpapi.com/google-news-api
- SerpApi Python Integration: https://serpapi.com/integrations/python
- Pandas Documentation: https://pandas.pydata.org/docs/
- Trafilatura Documentation: https://trafilatura.readthedocs.io/

---

Dikembangkan menggunakan Python untuk mendukung pengumpulan dan pengolahan dataset berita batubara dalam penelitian NLP.
