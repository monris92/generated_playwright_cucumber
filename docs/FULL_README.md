# 🎭 Playwright to Cucumber BDD Generator

Convert Playwright recordings into production-ready Cucumber BDD test projects with AI-powered automation.

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)

---

## ✨ Features

- **🎬 Record Once, Test Forever**: Record your actions with Playwright, get complete BDD tests
- **🤖 AI-Powered**: Mistral AI converts scripts to clean, maintainable BDD format
- **🚀 Zero Configuration**: Works out of the box with sensible defaults
- **✅ Production Ready**: Includes error handling, timeouts, and retry logic
- **📊 Detailed Reports**: HTML test reports with screenshots on failure
- **🔧 Maintainable**: Clean code structure, well-documented, easy to modify

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download this repository
cd playwright_cucumber_generator

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 2. Generate Your Test Project

```bash
# Run the generator
python cucumber_generator.py
```

You'll be prompted for:
- **Project folder**: Where to create your test project
- **Feature name**: e.g., `login`, `search`, `checkout`
- **Website URL**: The site you want to test

### 3. Record Your Test

A browser will open automatically:
1. Perform the actions you want to test
2. Close the browser when done
3. The script is saved automatically

### 4. Wait for AI Conversion

The generator will:
- ✅ Convert your recording to BDD format
- ✅ Create feature files (Gherkin)
- ✅ Generate step definitions
- ✅ Set up test runners
- ✅ Validate everything works

### 5. Run Your Tests

```bash
# Navigate to your project
cd your_project_name

# Run tests
./run_tests.sh

# Or use Python directly
python run_tests.py
```

View results in `reports/report_your_feature.html`

---

## 📁 What Gets Generated

```
your_project/
├── features/
│   ├── your_feature/
│   │   └── your_feature.feature          # Gherkin scenarios
│   └── steps/
│       └── your_feature_steps.py         # Step definitions
├── tests/
│   └── recorded_your_feature.py          # Original Playwright recording
├── config/
│   └── test_config.json                  # Configuration
├── reports/                              # Test reports (generated on run)
├── test_your_feature.py                  # Main test file
├── run_tests.py                          # Python runner
├── run_tests.sh                          # Shell runner
└── pytest.ini                            # Pytest configuration
```

---

## 🎯 How It Works

```
┌─────────────────┐
│  1. Setup       │  Configure project (folder, feature name, URL)
└────────┬────────┘
         │
┌────────▼────────┐
│  2. Record      │  Browser opens → You perform actions → Recording saved
└────────┬────────┘
         │
┌────────▼────────┐
│  3. Convert     │  AI transforms Playwright → Cucumber BDD
└────────┬────────┘
         │
┌────────▼────────┐
│  4. Validate    │  Check syntax, fix issues, ensure everything works
└────────┬────────┘
         │
┌────────▼────────┐
│  5. Ready! 🎉   │  Run tests and get detailed reports
└─────────────────┘
```

---

## 🛠️ Requirements

**System Requirements:**
- Python 3.8 or higher
- Internet connection (for AI conversion)
- 2GB RAM minimum

**Python Dependencies:**
```
playwright>=1.44.0
pytest>=8.4.0
pytest-bdd>=8.1.0
pytest-html>=4.1.0
requests>=2.31.0
```

All dependencies are in `requirements.txt`

---

## 📋 Usage Examples

### Example 1: Login Test

```bash
python cucumber_generator.py
```
- **Folder**: `/home/user/tests/login`
- **Feature**: `login`
- **URL**: `https://example.com`

**Record**: Enter username → Enter password → Click login

**Result**: Complete BDD test project ready to run!

### Example 2: E-commerce Search

```bash
python cucumber_generator.py
```
- **Folder**: `/home/user/tests/search`
- **Feature**: `product_search`
- **URL**: `https://shop.example.com`

**Record**: Click search → Type "laptop" → Click search button → Verify results

**Result**: Automated search test with assertions!

---

## 🔧 Configuration

### Mistral AI Setup

The generator uses Mistral AI for conversion. The API key is included for demo purposes. For production use:

1. Get your API key from [Mistral AI](https://mistral.ai/)
2. Edit `cucumber_generator.py`
3. Replace the API key:
   ```python
   self.mistral_api_key = "YOUR_API_KEY_HERE"
   ```

### Test Configuration

Each project has a `config/test_config.json`:

```json
{
  "project_name": "Test_your_feature",
  "website_url": "https://example.com",
  "feature_label": "your_feature",
  "playwright_config": {
    "headless": false,
    "timeout": 30000
  }
}
```

Modify as needed for your use case.

---

## 🎨 Generated Test Example

### Feature File (Gherkin)
```gherkin
Feature: Login functionality
  @login
  Scenario: Successful user login
    Given User navigates to the login page
    When User enters 'testuser' in username field
    And User enters 'password123' in password field
    And User clicks 'LOGIN' button
    Then 'Welcome' message should be visible
```

### Step Definitions (Python)
```python
from playwright.sync_api import expect
from pytest_bdd import given, when, then

@given("User navigates to the login page")
def navigate_to_login(page):
    page.goto('https://example.com/login')
    page.wait_for_load_state('networkidle')

@when("User enters 'testuser' in username field")
def enter_username(page):
    page.get_by_label('Username').fill('testuser')

@when("User clicks 'LOGIN' button")
def click_login(page):
    page.get_by_role('button', name='LOGIN').click()
    page.wait_for_timeout(2000)

@then("'Welcome' message should be visible")
def verify_welcome(page):
    expect(page.get_by_text('Welcome')).to_be_visible()
```

---

## 🐛 Troubleshooting

### Issue: "Playwright not found"
```bash
pip install playwright
playwright install
```

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "AI conversion failed"
- Check internet connection
- Verify API key is valid
- Try again (sometimes API can be temporarily unavailable)

### Issue: "Tests fail to run"
```bash
# Ensure you're in the project directory
cd your_project

# Check if feature files exist
ls features/your_feature/

# Try running with verbose output
python run_tests.py your_feature
```

---

## 🎓 Best Practices

### Feature Naming
- ✅ Use descriptive names: `user_login`, `product_search`
- ✅ Use underscores or hyphens: `checkout_flow`, `admin-panel`
- ❌ Avoid spaces: `user login` → use `user_login`
- ❌ Avoid special characters: `user@login` → use `user_login`

### Recording Tips
- 🎯 Keep actions simple and focused
- 🐌 Don't rush - Playwright captures everything
- 🔍 Use clear, unique selectors (labels, roles, unique text)
- ✅ Verify final state (look for confirmation messages)

### Project Organization
```
tests/
├── login/          # Login functionality tests
├── search/         # Search feature tests
├── checkout/       # Checkout process tests
└── admin/          # Admin panel tests
```

---

## 📚 Advanced Usage

### Running Tests in Headless Mode

Edit `test_your_feature.py`:
```python
browser = p.chromium.launch(headless=True, slow_mo=0)
```

### Parallel Test Execution

```bash
pip install pytest-xdist
pytest test_your_feature.py -n 4
```

### Custom Reporters

```bash
# JUnit XML
pytest test_your_feature.py --junitxml=reports/junit.xml

# Allure
pip install allure-pytest
pytest test_your_feature.py --alluredir=reports/allure
allure serve reports/allure
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional AI model support
- More test frameworks (Jest, Selenium)
- Visual regression testing
- CI/CD integration templates
- More assertion patterns

---

## 📄 License

MIT License - feel free to use this in your projects!

---

## 🙏 Credits

Built with:
- **Playwright**: Browser automation
- **Mistral AI**: Intelligent code conversion
- **pytest-bdd**: BDD testing framework
- **Python**: Gluing it all together

---

## 📞 Support

Having issues? Check:
1. This README for common solutions
2. Generated `reports/` for test failures
3. Python logs for error details

---

**Made with ❤️ for the testing community**

*Transform your manual tests into automated BDD tests in minutes!*
