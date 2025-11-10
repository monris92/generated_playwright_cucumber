#!/bin/bash

# Quick start script - Aktifkan virtual environment dan jalankan generator
# Author: Playwright to Cucumber Generator
# Date: $(date +"%Y-%m-%d")

echo "🚀 QUICK START - Playwright to Cucumber Generator"
echo "================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment belum ada! Jalankan setup_env.sh terlebih dahulu"
    echo "   Cara: ./setup_env.sh"
    exit 1
fi

# Check if Python script exists
if [ ! -f "enhanced_cucumber_generator_fixed_v2.py" ]; then
    echo "❌ File enhanced_cucumber_generator_fixed_v2.py tidak ditemukan!"
    exit 1
fi

# Activate virtual environment
echo "📦 Mengaktifkan virtual environment..."
source venv/bin/activate

# Check if playwright is available
if ! command -v playwright &> /dev/null; then
    echo "❌ Playwright tidak ditemukan di virtual environment!"
    echo "🔧 Mencoba install ulang..."
    pip install playwright
    playwright install
fi

echo "🎭 Menjalankan Playwright to Cucumber Generator..."
echo ""
echo "💡 PENTING: Pastikan menggunakan virtual environment!"
echo "   Current Python: $(which python)"
echo ""
python enhanced_cucumber_generator_fixed_v2.py
