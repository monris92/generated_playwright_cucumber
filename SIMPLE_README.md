# 🎬 Simple Playwright Test Recorder

**Record your tests, run them anytime. Simple. Reliable. No complications.**

---

## 🚀 Quick Start (3 Steps)

### 1. Install (One Time)
```bash
pip install playwright pytest pytest-html
playwright install
```

### 2. Record Your Test
```bash
python3 simple_recorder.py
```

Answer 3 simple questions:
- Where to save? (default: `my_tests`)
- Test name? (e.g., `login`)
- Website URL? (e.g., `https://example.com`)

Then browser opens → Do your actions → Close browser → Done!

### 3. Run Your Test
```bash
cd my_tests
python3 run_test.py
```

View results in `reports/report.html`

**That's it! 🎉**

---

## 📁 What You Get

```
my_tests/
├── tests/
│   └── login.py              # Your recorded test
├── reports/
│   └── report.html           # Test results (after running)
├── run_test.py               # Simple runner
├── run_test.sh               # Shell runner
├── pytest.ini                # Pytest config
└── README.md                 # Instructions
```

---

## ✨ Features

- ✅ **Simple** - No complicated conversions or AI
- ✅ **Reliable** - Uses standard Playwright pytest format
- ✅ **Organized** - Clean folder structure
- ✅ **Reports** - HTML reports with screenshots
- ✅ **Easy** - Just record and run!

---

## 🎯 Examples

### Example 1: Login Test
```bash
python3 simple_recorder.py
```
- Folder: `my_tests`
- Test name: `login`
- URL: `https://myapp.com/login`

*Browser opens → Enter username → Enter password → Click login → Close*

Done! Run with `cd my_tests && python3 run_test.py`

### Example 2: Search Test
```bash
python3 simple_recorder.py
```
- Folder: `search_tests`
- Test name: `product_search`
- URL: `https://shop.com`

*Browser opens → Click search → Type "laptop" → Click search button → Close*

Done! Run with `cd search_tests && python3 run_test.py`

---

## 🔧 Common Tasks

### Run a specific test
```bash
pytest tests/login.py -v
```

### Run all tests in folder
```bash
pytest tests/ -v
```

### Run in headless mode
Edit your test file and change:
```python
browser = p.chromium.launch(headless=True)
```

### Re-record a test
```bash
python3 -m playwright codegen https://example.com --target python-pytest --output tests/mytest.py
```

---

## 🐛 Troubleshooting

### "Playwright not found"
```bash
pip install playwright
playwright install
```

### "pytest not found"
```bash
pip install pytest pytest-html
```

### Test fails to run
1. Make sure you're in the test folder: `cd my_tests`
2. Check if test file exists: `ls tests/`
3. Run with verbose: `pytest tests/yourtest.py -v -s`

---

## 💡 Tips

- **Keep tests simple** - Record one feature at a time
- **Use clear names** - `user_login` not `test123`
- **Organize folders** - One folder per feature
- **Check reports** - Always review `reports/report.html`

---

## 🆚 Why This Instead of Complex Generator?

| Complex Generator | Simple Recorder |
|-------------------|-----------------|
| AI conversion (can fail) | Direct recording (always works) |
| Gherkin/BDD format | Standard Playwright |
| Many dependencies | Just Playwright + pytest |
| Long setup | 3 commands |
| Hard to debug | Easy to understand |
| **Sometimes works** | **Always works** |

---

## 📦 Requirements

```
playwright>=1.40.0
pytest>=7.0.0
pytest-html>=3.0.0
```

That's all!

---

## ✅ You're Ready!

```bash
# Install
pip install playwright pytest pytest-html
playwright install

# Record
python3 simple_recorder.py

# Run
cd my_tests && python3 run_test.py
```

**Simple. Reliable. Just works.** 🚀
