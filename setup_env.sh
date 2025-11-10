#!/bin/bash

# Script setup untuk virtual environment dan instalasi dependencies
# Author: Playwright to Cucumber Generator
# Date: $(date +"%Y-%m-%d")

echo "🎭 PLAYWRIGHT TO CUCUMBER - Environment Setup"
echo "=============================================="

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function untuk print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment belum ada, membuat virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_status "Virtual environment berhasil dibuat"
    else
        print_error "Gagal membuat virtual environment"
        exit 1
    fi
else
    print_status "Virtual environment sudah ada"
fi

# Activate virtual environment
print_status "Mengaktifkan virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrade pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    print_status "Installing packages dari requirements.txt..."
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_status "Dependencies berhasil diinstall"
    else
        print_error "Gagal install dependencies"
        exit 1
    fi
else
    print_error "File requirements.txt tidak ditemukan"
    exit 1
fi

# Install Playwright browsers
print_status "Installing Playwright browsers..."
playwright install

# Install system dependencies (jika diperlukan)
print_warning "Checking system dependencies..."
echo "Jika ada error tentang missing dependencies, jalankan:"
echo "sudo playwright install-deps"

print_status "Setup completed!"
echo ""
echo "📋 Cara menggunakan:"
echo "1. Aktifkan virtual environment: source venv/bin/activate"
echo "2. Jalankan generator: python enhanced_cucumber_generator_fixed_v2.py"
echo "3. Untuk menjalankan test: python run_tests.py [feature_name]"
echo ""
echo "🎉 Happy Testing!"
