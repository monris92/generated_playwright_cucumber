# Login Test

Recorded on: 2025-12-08 11:53
Website: https://map.chronicle.rip

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
pytest tests/login.py -v
```

## View results

Open `reports/report.html` in your browser

## Re-record

If you need to update the test:
```bash
python3 -m playwright codegen https://map.chronicle.rip --target python-pytest --output tests/login.py
```
