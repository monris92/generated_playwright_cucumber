#!/bin/bash

# QUICK FIX - Jalankan generator dengan virtual environment yang benar
# Gunakan ini jika error "playwright not found"

echo "🔧 QUICK FIX - Virtual Environment Generator"
echo "============================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 Current directory: $SCRIPT_DIR"

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment tidak ditemukan!"
    echo "🔧 Menjalankan setup..."
    if [ -f "setup_env.sh" ]; then
        ./setup_env.sh
    else
        echo "❌ setup_env.sh tidak ditemukan!"
        exit 1
    fi
fi

# Use absolute path for virtual environment
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"
VENV_PLAYWRIGHT="$SCRIPT_DIR/venv/bin/playwright"

echo "🔍 Checking paths:"
echo "   Python: $VENV_PYTHON"
echo "   Playwright: $VENV_PLAYWRIGHT"

# Verify paths exist
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Python tidak ditemukan di virtual environment!"
    exit 1
fi

if [ ! -f "$VENV_PLAYWRIGHT" ]; then
    echo "❌ Playwright tidak ditemukan di virtual environment!"
    echo "🔧 Mencoba install..."
    "$VENV_PYTHON" -m pip install playwright
    "$VENV_PYTHON" -m playwright install
    
    # Verify installation
    if "$VENV_PYTHON" -m playwright --help > /dev/null 2>&1; then
        echo "✅ Playwright berhasil diinstall!"
    else
        echo "❌ Gagal install Playwright. Silakan cek koneksi internet dan coba lagi."
        exit 1
    fi
fi

# Run the generator
echo "🎭 Menjalankan generator dengan virtual environment..."
echo "💡 Tip: Jika masih ada error, pastikan:"
echo "   - Koneksi internet stabil untuk download browser"
echo "   - Folder memiliki permission yang cukup"
echo ""
"$VENV_PYTHON" enhanced_cucumber_generator_fixed_v2.py

echo ""
echo "✅ Generator selesai! Periksa file yang dihasilkan di folder project Anda."
