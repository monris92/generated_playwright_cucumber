# Playwright Test Tools

Kumpulan tools untuk merekam dan menghasilkan automated tests menggunakan Playwright.

## Quick Start

### 1. Setup Environment
```bash
./setup_env.sh
```

### 2. Pilih Tool yang Sesuai

#### Simple Recorder (Direkomendasikan)
Tool sederhana untuk merekam test Playwright:
```bash
python3 simple_recorder.py
```

#### Cucumber BDD Generator (Advanced)
Menghasilkan test dalam format Cucumber BDD dengan AI:
```bash
python3 cucumber_generator.py
```

## Dokumentasi

Dokumentasi lengkap tersedia di folder `docs/`:

- **[WHICH_ONE.md](docs/WHICH_ONE.md)** - Panduan memilih tool yang tepat
- **[SIMPLE_README.md](docs/SIMPLE_README.md)** - Dokumentasi Simple Recorder
- **[FULL_README.md](docs/FULL_README.md)** - Dokumentasi lengkap Cucumber Generator

## Struktur File

```
.
├── simple_recorder.py          # Simple test recorder
├── cucumber_generator.py       # Cucumber BDD generator
├── setup_env.sh               # Script setup environment
├── requirements.txt           # Dependencies untuk Cucumber generator
├── requirements_simple.txt    # Dependencies untuk Simple recorder
└── docs/                      # Dokumentasi
    ├── WHICH_ONE.md          # Perbandingan tools
    ├── SIMPLE_README.md      # Panduan Simple Recorder
    └── FULL_README.md        # Panduan lengkap Cucumber
```

## Requirements

- Python 3.7+
- pip
- Node.js (untuk Playwright browsers)

## License

MIT
