# 🎯 E2E Test System with Priority Management

Professional E2E testing system with automated test recording, enhancement, and priority-based organization.

## 📁 Folder Structure

```
e2e/
├── p0-smoke_test/          # Critical tests (must pass before release)
│   ├── tests/
│   │   ├── login_test.py
│   │   ├── checkout_test.py
│   │   └── __init__.py
│   └── reports/
│
├── p1-regression/          # Important tests (run on every build)
│   ├── tests/
│   │   ├── search_test.py
│   │   ├── crud_test.py
│   │   └── __init__.py
│   └── reports/
│
├── p2-exploratory/         # Nice-to-have tests (edge cases, UI)
│   ├── tests/
│   │   ├── edge_cases_test.py
│   │   ├── ui_validation_test.py
│   │   └── __init__.py
│   └── reports/
│
├── conftest.py             # Shared fixtures & configuration
├── pytest.ini              # Global pytest config
└── reports/                # Global test reports

simple_recorder.py          # Test recorder with auto-enhancement
test_enhancer.py            # Smart test enhancement engine
run_tests.py                # Test runner with priority filtering
```

## 🎬 Recording Tests

### Quick Start

```bash
python simple_recorder.py
```

### Interactive Flow

```
📁 Base test folder? (press Enter for 'e2e'):
✅ Base folder: /path/to/e2e

📊 Test Priority:
   1. P0 - Smoke Test (Critical: login, checkout, core flows)
   2. P1 - Regression (Important: CRUD, search, filters)
   3. P2 - Exploratory (Nice-to-have: edge cases, UI validation)
Choose priority [1-3] (default: 2): 1
✅ Selected: P0 - Smoke Test

🏷️  Test name (e.g., login, search, checkout): login

🌐 Website URL to test: https://map.chronicle.rip

🎬 RECORDING
   1. Browser will open
   2. Do your test actions
   3. Close browser when done
```

### What Happens Automatically

1. ✅ **Records** your test actions
2. ✅ **Enhances** with smart waits and fixes:
   - Waits after login buttons
   - Converts `page.goto()` after login → URL validation
   - Adds element visibility waits
3. ✅ **Adds pytest marker** (`@pytest.mark.smoke` / `regression` / `exploratory`)
4. ✅ **Organizes** into correct priority folder
5. ✅ **Creates** test runner

## 🚀 Running Tests

### Run All Tests

```bash
python run_tests.py --all
```

### Run by Priority

```bash
# Run P0 (smoke tests only)
python run_tests.py --priority p0

# Run P1 (regression tests)
python run_tests.py --priority p1

# Run multiple priorities
python run_tests.py --priority p0,p1
```

### Run by Pytest Marker

```bash
# Run all smoke tests
python run_tests.py --marker smoke

# Run all regression tests
python run_tests.py --marker regression
```

### Run Specific Test

```bash
python run_tests.py --test e2e/p0-smoke_test/tests/login_test.py
```

### List All Tests

```bash
python run_tests.py --list
```

Output:
```
📋 Available E2E Tests
======================================================================

P0 - Smoke Test
   Critical features that must pass before release
   Folder: p0-smoke_test/
   • login_test.py
   • checkout_test.py

P1 - Regression
   Important features, run on every build
   Folder: p1-regression/
   • search_test.py
   • crud_test.py

P2 - Exploratory
   Edge cases and UI validation
   Folder: p2-exploratory/
   • ui_validation_test.py
```

## 📊 Test Priorities Explained

### P0 - Smoke Test 🔥
**Critical features that MUST pass before release**

Examples:
- User login
- Payment/checkout flow
- Core business functionality
- Critical user journeys

**When to run:**
- Before every release
- After critical bug fixes
- Pre-deployment validation

### P1 - Regression 🔄
**Important features, run on every build**

Examples:
- CRUD operations
- Search functionality
- Filters and sorting
- User management
- Data validation

**When to run:**
- Every build/CI pipeline
- After feature changes
- Regular regression testing

### P2 - Exploratory 🔍
**Nice-to-have tests for edge cases and UI**

Examples:
- Edge case scenarios
- UI element validation
- Error message checks
- Tooltips and labels
- Visual regression

**When to run:**
- Before major releases
- During QA cycles
- Manual test runs

## 🎨 Test Enhancement Features

### Automatic Enhancements

The system automatically adds these improvements to recorded tests:

#### 1. Login Flow Handling
**Before:**
```python
page.get_by_test_id("login-button").click()
page.goto("https://example.com/dashboard")
```

**After:**
```python
page.get_by_test_id("login-button").click()

# Wait for navigation after login
page.wait_for_load_state('load')
page.wait_for_timeout(2000)

# Wait for automatic navigation (instead of manual goto)
page.wait_for_url("**/dashboard", timeout=15000)
page.wait_for_load_state('load')
page.wait_for_timeout(2000)

# Validate we're on the correct page
expect(page).to_have_url("https://example.com/dashboard")
```

#### 2. Element Visibility Waits
**Before:**
```python
expect(page.get_by_test_id("username")).to_contain_text("user@example.com")
```

**After:**
```python
# Wait for element to be visible
page.get_by_test_id("username").wait_for(state='visible', timeout=10000)
expect(page.get_by_test_id("username")).to_contain_text("user@example.com")
```

#### 3. Pytest Markers
**Before:**
```python
def test_login(page: Page) -> None:
    # test code
```

**After:**
```python
@pytest.mark.smoke
def test_login(page: Page) -> None:
    # test code
```

## 🔧 Manual Test Enhancement

For existing tests that need enhancement:

```bash
# Create enhanced version (keeps original)
python test_enhancer.py e2e/p0-smoke_test/tests/login_test.py

# Review the .enhanced.py file, then replace
mv e2e/p0-smoke_test/tests/login_test.enhanced.py e2e/p0-smoke_test/tests/login_test.py

# Or enhance in-place
python test_enhancer.py e2e/p0-smoke_test/tests/login_test.py --in-place
```

## 📈 CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install playwright pytest-playwright pytest-html
          playwright install chromium
      - name: Run P0 Smoke Tests
        run: python run_tests.py --priority p0

  regression-tests:
    runs-on: ubuntu-latest
    needs: smoke-tests
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install playwright pytest-playwright pytest-html
          playwright install chromium
      - name: Run P1 Regression Tests
        run: python run_tests.py --priority p1
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    stages {
        stage('Smoke Tests') {
            steps {
                sh 'python run_tests.py --priority p0'
            }
        }
        stage('Regression Tests') {
            when {
                branch 'main'
            }
            steps {
                sh 'python run_tests.py --priority p1'
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'e2e/reports',
                reportFiles: 'report.html',
                reportName: 'E2E Test Report'
            ])
        }
    }
}
```

## 🛠️ Advanced Usage

### Custom Pytest Options

```bash
# Run with custom markers
python run_tests.py --priority p0 --marker slow

# Quiet mode
python run_tests.py --priority p1 --quiet

# Custom base folder
python run_tests.py --all --base-folder my_tests
```

### Direct Pytest Commands

```bash
# Run all smoke tests
pytest -m smoke

# Run all tests except exploratory
pytest -m "not exploratory"

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto -m smoke

# Run with custom timeout
pytest --timeout=300 -m regression
```

## 📝 Best Practices

### 1. Test Naming Convention
```
{feature}_{action}_test.py

Examples:
- login_success_test.py
- search_products_test.py
- checkout_payment_test.py
```

### 2. Priority Guidelines

**P0 Criteria:**
- Blocks user from core functionality
- Affects revenue/payments
- Critical security issue
- Total system failure

**P1 Criteria:**
- Important feature not working
- Workaround exists
- Affects multiple users
- Data integrity issues

**P2 Criteria:**
- Minor UI issues
- Edge cases
- Nice-to-have features
- Cosmetic issues

### 3. Test Organization

Group related tests:
```
e2e/p0-smoke_test/tests/
├── auth/
│   ├── login_test.py
│   └── logout_test.py
└── checkout/
    ├── payment_test.py
    └── confirmation_test.py
```

## 🔍 Troubleshooting

### Tests Timing Out

Increase waits in test:
```python
page.wait_for_timeout(5000)  # Wait 5 seconds
page.wait_for_url("**/page", timeout=30000)  # 30 second timeout
```

### Element Not Found

Add explicit wait:
```python
page.get_by_test_id("element").wait_for(state="visible", timeout=15000)
```

### Network Issues

Use `networkidle` only for stable pages:
```python
page.goto("https://example.com", wait_until="load")  # Better than "networkidle"
```

## 📚 Related Documentation

- [ENHANCEMENT_GUIDE.md](ENHANCEMENT_GUIDE.md) - Details on test enhancement
- [Playwright Docs](https://playwright.dev/python/) - Official Playwright docs
- [Pytest Docs](https://docs.pytest.org/) - Official Pytest docs

## 🎉 Quick Reference

```bash
# Record new test
python simple_recorder.py

# Run all tests
python run_tests.py --all

# Run smoke tests
python run_tests.py --priority p0

# List tests
python run_tests.py --list

# Enhance existing test
python test_enhancer.py path/to/test.py --in-place
```

---

**Happy Testing! 🚀**
