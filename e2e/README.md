# Wl Advancesearch Deceased In Cemetery Test

Recorded on: 2025-11-14 12:50
Website: https://map.chronicle.rip/

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
pytest tests/wl_advancesearch_deceased_in_cemetery.py -v
```

## View results

Open `reports/report.html` in your browser

## Re-record

If you need to update the test:
```bash
python3 -m playwright codegen https://map.chronicle.rip/ --target python-pytest --output tests/wl_advancesearch_deceased_in_cemetery.py
```
