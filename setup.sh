#!/bin/bash

# Script untuk setup virtual environment dan instalasi dependencies
# Untuk Linux/Mac

echo "========================================"
echo "🚀 Setup Virtual Environment"
echo "========================================"

# Cek apakah Python terinstall
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 tidak ditemukan. Silakan install Python terlebih dahulu."
    exit 1
fi

echo "✅ Python3 ditemukan: $(python3 --version)"

# Membuat virtual environment
echo ""
echo "📦 Membuat virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Gagal membuat virtual environment"
    exit 1
fi

echo "✅ Virtual environment berhasil dibuat"

# Aktivasi virtual environment
echo ""
echo "🔌 Mengaktifkan virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Gagal mengaktifkan virtual environment"
    exit 1
fi

echo "✅ Virtual environment aktif"

# Update pip
echo ""
echo "📦 Update pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Menginstall dependencies dari requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Gagal menginstall dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Setup selesai!"
echo "========================================"
echo ""
echo "📝 Cara menggunakan:"
echo "   1. Aktifkan virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Jalankan program:"
echo "      python main.py"
echo ""
echo "   3. Untuk deaktivasi virtual environment:"
echo "      deactivate"
echo ""
echo "========================================"
