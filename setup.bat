@echo off
REM Script untuk setup virtual environment dan instalasi dependencies
REM Untuk Windows

echo ========================================
echo 🚀 Setup Virtual Environment
echo ========================================

REM Cek apakah Python terinstall
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan. Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)

echo ✅ Python ditemukan
python --version

REM Membuat virtual environment
echo.
echo 📦 Membuat virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Gagal membuat virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment berhasil dibuat

REM Aktivasi virtual environment
echo.
echo 🔌 Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ Gagal mengaktifkan virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment aktif

REM Update pip
echo.
echo 📦 Update pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 📥 Menginstall dependencies dari requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Gagal menginstall dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup selesai!
echo ========================================
echo.
echo 📝 Cara menggunakan:
echo    1. Aktifkan virtual environment:
echo       venv\Scripts\activate
echo.
echo    2. Jalankan program:
echo       python main.py
echo.
echo    3. Untuk deaktivasi virtual environment:
echo       deactivate
echo.
echo ========================================
pause
