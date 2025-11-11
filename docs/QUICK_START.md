# ⚡ Quick Start Guide

Get started with E2E testing in 3 minutes!

## 🎯 Step 1: Record Your First Test

```bash
python simple_recorder.py
```

Follow the prompts:
```
📁 Base test folder? (press Enter for 'e2e'): ⏎
✅ Base folder: /path/to/e2e

📊 Test Priority:
   1. P0 - Smoke Test (Critical: login, checkout, core flows)
   2. P1 - Regression (Important: CRUD, search, filters)
   3. P2 - Exploratory (Nice-to-have: edge cases, UI validation)
Choose priority [1-3] (default: 2): 1

🏷️  Test name (e.g., login, search, checkout): login

🌐 Website URL to test: https://map.chronicle.rip
```

Browser opens → Perform your test actions → Close browser when done ✅

## 🚀 Step 2: Run Your Test

### Option A: Interactive Menu (Recommended) 🎯
```bash
./run.sh
# or
python run_tests_interactive.py
```

**Interactive menu lets you:**
1. Choose priority (P0/P1/P2/All)
2. See all available scenarios
3. Run specific scenario or all scenarios

**Example flow:**
```
📊 Select Test Priority:
   P0: P0 - Smoke Test
        Tests available: 2
Choose priority [p0/p1/p2/all]: p0

📋 Available Scenarios in P0:
   1. login
   2. search
   0. Run ALL scenarios in P0
Choose scenario [0-2]: 1
```

### Option B: Command Line (For CI/CD)
```bash
# Run P0 smoke tests
python run_tests.py --priority p0

# Run P1 regression tests
python run_tests.py --priority p1

# Run specific test
python run_tests.py --test e2e/p0-smoke_test/login/tests/login_test.py

# Run all tests
python run_tests.py --all
```

### Check the results:
- ✅ Console shows pass/fail
- 📊 HTML report in `e2e/reports/report.html`
- 📸 Screenshots in `e2e/reports/screenshots/` (auto-captured on failure)

## 📋 Step 3: View All Tests

```bash
python run_tests.py --list
```

## 🎯 Priority Quick Reference

| Priority | When to Use | Examples |
|----------|-------------|----------|
| **P0** 🔥 | Must pass before release | Login, checkout, payment |
| **P1** 🔄 | Run on every build | CRUD, search, filters |
| **P2** 🔍 | Edge cases & UI | Tooltips, error messages |

## 💡 Tips

1. **Recording stuck?** Close the browser to save the test
2. **Test failing?** Check `e2e/reports/report.html` for details
3. **Need help?** Read [E2E_SYSTEM_README.md](E2E_SYSTEM_README.md)

## 🎉 That's It!

You now have:
- ✅ Automated test recording
- ✅ Smart enhancement (waits, validations)
- ✅ Priority-based organization
- ✅ Flexible test runner

**Happy Testing! 🚀**
