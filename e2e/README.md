# Hhi Test

Recorded on: 2025-11-12 15:10
Website: Generated from existing script

## Run the test

### Option 1: Python
```bash
python3 run_test.py
```

### Option 2: Shell script
```bash
./run_test.sh
```

### Option 3: Direct pytest
```bash
pytest tests/hhi.py -v
```

## View results

Open `reports/report.html` in your browser

## Re-record

If you need to update the test:
```bash
python3 -m playwright codegen Generated from existing script --target python-pytest --output tests/hhi.py
```
