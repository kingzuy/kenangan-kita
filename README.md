# 🛍️ Scraper Shopee Excel

Script Python sederhana yang menggunakan pustaka `requests` dan `BeautifulSoup` untuk melakukan web scraping data produk dari Shopee, serta `pandas` untuk menyimpan data ke file Excel.

---

## 📋 Deskripsi

Proyek ini adalah sebuah script Python untuk melakukan web scraping data produk dari Shopee dan menyimpannya dalam format Excel (.xlsx).

### Data yang Diambil:
- ✅ Nama Produk
- ✅ Gambar Produk (URL)
- ✅ Detail Keterangan
- ✅ Jumlah Stok

---

## 🔧 Kebutuhan Sistem

- **Python 3.7+**
- **Koneksi Internet**
- **Sistem Operasi:** Windows, Linux, atau macOS

---

## 🚀 Instalasi

### **Metode 1: Instalasi Otomatis (Recommended)**

#### **Windows:**
1. Download semua file ke satu folder
2. Double-click file `setup.bat`
3. Tunggu hingga instalasi selesai
4. Virtual environment akan otomatis dibuat dan dependencies terinstall

#### **Linux/Mac:**
1. Download semua file ke satu folder
2. Beri permission execute:
   ```bash
   chmod +x setup.sh
   ```
3. Jalankan script:
   ```bash
   ./setup.sh
   ```

---

### **Metode 2: Instalasi Manual**

#### **Step 1: Clone/Download Repository**
```bash
git <url>
cd kenangan-kita
```

#### **Step 2: Buat Virtual Environment**

**Windows:**
```cmd
python -m venv venv
```

**Linux/Mac:**
```bash
python3 -m venv venv
```

#### **Step 3: Aktifkan Virtual Environment**

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### **Step 4: Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## 💻 Cara Menggunakan

### **1. Aktifkan Virtual Environment**

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### **2. Jalankan Script**
```bash
python main.py
```

### **3. Hasil Output**
Setelah script selesai dijalankan, file **`lelang_kpk_detailed.xlsx`** akan dibuat di direktori yang sama.

### **4. Deaktivasi Virtual Environment**
```bash
deactivate
```

---

## 📁 Struktur Project

```
kenangan-kita/
│
├── main.py                  # Script utama scraper
├── requirements.txt         # Daftar dependencies
├── setup.sh                # Setup script untuk Linux/Mac
├── setup.bat               # Setup script untuk Windows
├── README.md               # Dokumentasi lengkap
├── .gitignore              # Git ignore file
├── venv/                   # Virtual environment (dibuat otomatis)
└── lelang_kpk_detailed.xlsx    # Output file (dibuat setelah running)
```

---

## 📦 Dependencies

Library yang digunakan:

```
requests >= 2.31.0          # Untuk HTTP requests
beautifulsoup4 >= 4.12.0    # Untuk parsing HTML
pandas >= 2.0.0             # Untuk manipulasi data
openpyxl >= 3.1.0           # Untuk export ke Excel
lxml >= 4.9.0               # Parser HTML tambahan
```

---

## 🔧 Troubleshooting

### **Error: "Python tidak ditemukan"**
**Solusi:**
- Install Python dari [python.org](https://www.python.org/downloads/)
- Pastikan Python ditambahkan ke PATH

### **Error: "pip tidak ditemukan"**
**Solusi:**
```bash
python -m ensurepip --upgrade
```

### **Error: "Permission denied" (Linux/Mac)**
**Solusi:**
```bash
chmod +x setup.sh
```

### **Error: "Module not found"**
**Solusi:**
- Pastikan virtual environment aktif
- Install ulang dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### **Scraping Gagal / Tidak Ada Data**
**Kemungkinan Penyebab:**
- ⚠️ Shopee menggunakan JavaScript rendering (gunakan Selenium)
- ⚠️ IP address di-block karena terlalu banyak request
- ⚠️ Struktur HTML Shopee berubah
- ⚠️ Perlu tambahkan headers dan cookies

---

## ⚠️ DISCLAIMER

**PENTING - HARAP DIBACA:**

- Web scraping adalah tindakan yang **sensitif** dan bisa melanggar **Terms of Service (ToS)** dari website target
- Pastikan Anda telah membaca dan memahami **syarat layanan Shopee** sebelum menggunakan script ini
- Penggunaan script ini adalah **tanggung jawab pengguna**
- Script ini dibuat untuk **tujuan edukasi dan pembelajaran**
- Jangan gunakan untuk tujuan komersial tanpa izin
- Gunakan dengan **bijak dan bertanggung jawab**

### Rekomendasi:
- Gunakan delay/sleep antar request
- Jangan melakukan scraping terlalu agresif
- Pertimbangkan menggunakan API resmi jika tersedia
- Hormati robots.txt dari website

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Jika Anda menemukan bug atau ingin menambah fitur:

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

## 📄 Lisensi

Proyek ini berada di bawah **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 Kontak & Support

Jika ada pertanyaan atau butuh bantuan:

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/username/scraper-shopee-excel/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/username/scraper-shopee-excel/discussions)

---

## 🎯 Roadmap

- [ ] Tambah support untuk multiple pages
- [ ] Tambah progress bar
- [ ] Export ke format CSV
- [ ] GUI interface
- [ ] Support proxy rotation
- [ ] Rate limiting otomatis
- [ ] Logging system

---

## 🙏 Acknowledgments

- [Requests](https://requests.readthedocs.io/) - HTTP library
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel handling

---

## 📝 Changelog

### Version 1.0.0 (2025-10-31)
- ✅ Initial release
- ✅ Basic scraping functionality
- ✅ Excel export feature
- ✅ Virtual environment setup scripts

---

**Proyek ini akan terus diperbarui. Terima kasih telah mengunjungi! ⭐**

---

<div align="center">
  <sub>Built with ❤️ by Your Name</sub>
</div>
