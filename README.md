# Playwright E2E Test Tools

Kumpulan tools untuk merekam dan menjalankan automated tests menggunakan Playwright.

## Quick Start

### 1. Setup Environment
```bash
./setup_env.sh
```

### 2. Jalankan Test Interaktif (Recommended)
Tool utama untuk merekam dan menjalankan test:
```bash
python3 run_tests_interactive.py
```

### 3. Atau Rekam Test Manual
Tool sederhana untuk merekam test Playwright:
```bash
python3 simple_recorder.py
```

## Dokumentasi

Dokumentasi lengkap tersedia di folder `docs/`:

- **[QUICK_START.md](docs/QUICK_START.md)** - Panduan quick start
- **[E2E_SYSTEM_README.md](docs/E2E_SYSTEM_README.md)** - Dokumentasi sistem E2E
- **[ENHANCEMENT_GUIDE.md](docs/ENHANCEMENT_GUIDE.md)** - Panduan enhancement
- **[FULL_README.md](docs/FULL_README.md)** - Dokumentasi lengkap

## Struktur File

```
.
├── run_tests_interactive.py    # Test runner interaktif (MAIN)
├── run_tests.py               # Test runner non-interaktif
├── simple_recorder.py         # Simple test recorder
├── setup_env.sh              # Script setup environment
├── run.sh                    # Quick run script
├── requirements.txt          # Dependencies
├── docs/                     # Dokumentasi lengkap
├── e2e/                      # E2E test files
└── utils/                    # Utility scripts
    └── test_enhancer.py      # Test enhancer (auto-fix errors)
```

## Requirements

- Python 3.7+
- pip
- Node.js (untuk Playwright browsers)

## License

MIT
