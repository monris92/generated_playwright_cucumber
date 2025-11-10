# 🔧 Troubleshooting Guide

## ❌ Error: "No such file or directory: 'playwright'"

**Problem:** Playwright is not found in the system PATH.

**Solutions (in order of preference):**

1. **Use the Fixed Runner Script (RECOMMENDED):**
   ```bash
   ./run_fixed.sh
   ```

2. **Manual Virtual Environment Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install playwright requests
   playwright install
   python enhanced_cucumber_generator_fixed_v2.py
   ```

3. **Test your setup:**
   ```bash
   python3 test_playwright_detection.py
   ```

## ❌ Error: externally-managed-environment

**Problem:** 
```
error: externally-managed-environment
× This environment is externally managed
```

**Solution:**
```bash
# Gunakan virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Atau gunakan script setup yang sudah disediakan:**
```bash
./setup_env.sh
```

---

## ❌ Error: python3-venv not available

**Problem:** 
```
The virtual environment was not created successfully because ensurepip is not available
```

**Solution:**
```bash
# Install python3-venv
sudo apt update
sudo apt install python3.12-venv

# Lalu buat virtual environment
python3 -m venv venv
source venv/bin/activate
```

---

## ❌ Error: Playwright browsers not installed

**Problem:**
```
Host system is missing dependencies to run browsers
```

**Solution:**
```bash
# Aktifkan virtual environment dulu
source venv/bin/activate

# Install browsers
playwright install

# Install system dependencies
sudo playwright install-deps
```

---

## ❌ Error: ImportError pytest_bdd

**Problem:**
```
ModuleNotFoundError: No module named 'pytest_bdd'
```

**Solution:**
```bash
# Pastikan virtual environment aktif
source venv/bin/activate

# Install ulang requirements
pip install -r requirements.txt
```

---

## ❌ Error: Permission denied

**Problem:**
```
./setup_env.sh: Permission denied
```

**Solution:**
```bash
# Buat file executable
chmod +x setup_env.sh
chmod +x start.sh

# Lalu jalankan
./setup_env.sh
```

---

## ✅ Verifikasi Setup

Untuk memastikan setup sukses, jalankan commands berikut:

```bash
# Check virtual environment
source venv/bin/activate
which python  # Harus menunjuk ke venv/bin/python

# Check dependencies
pip list | grep playwright
pip list | grep pytest-bdd

# Check Playwright
playwright --version
```

---

## 🎯 Workflow yang Benar

1. **Setup sekali saja:**
   ```bash
   ./setup_env.sh
   ```

2. **Jalankan generator:**
   ```bash
   ./start.sh
   ```

3. **Jalankan test:**
   ```bash
   source venv/bin/activate
   python run_tests.py [feature_name]
   ```

---

## 📞 Still Having Issues?

1. **Check Virtual Environment:**
   ```bash
   which python
   # Output harus: /path/to/your/project/venv/bin/python
   ```

2. **Reinstall Everything:**
   ```bash
   rm -rf venv
   ./setup_env.sh
   ```

3. **Manual Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
   sudo playwright install-deps
   ```
