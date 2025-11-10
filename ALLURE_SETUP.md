# 📊 Allure Reporting Setup Guide

Complete step-by-step guide for setting up Allure reporting with the Playwright to Cucumber BDD Generator.

## 📋 Prerequisites

Before setting up Allure, ensure you have:
- Python 3.8+ installed
- Node.js and npm installed (for Allure CLI)
- Basic understanding of command line

## 🚀 Quick Setup (All Platforms)

### Step 1: Install Python Dependencies
```bash
# These are already included in requirements.txt
pip install allure-pytest allure-python-commons
```

### Step 2: Install Java (Required for Allure CLI)

#### macOS:
```bash
# Option 1: Using Homebrew (recommended)
brew install openjdk

# Option 2: Using official installer
# Download from: https://adoptopenjdk.net/

# Set PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export JAVA_HOME="/opt/homebrew/opt/openjdk"
```

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install OpenJDK 11
sudo apt install openjdk-11-jdk

# Verify installation
java -version

# Set JAVA_HOME (add to ~/.bashrc)
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$PATH"
```

#### Windows:
```batch
# Download OpenJDK from: https://adoptopenjdk.net/
# Run installer and follow instructions

# Add to System PATH:
# 1. Open System Properties → Advanced → Environment Variables
# 2. Add JAVA_HOME: C:\Program Files\AdoptOpenJDK\jdk-11.0.x.x
# 3. Add to PATH: %JAVA_HOME%\bin

# Verify in Command Prompt:
java -version
```

### Step 3: Install Allure CLI

#### Option 1: Using npm (Recommended - Cross Platform)
```bash
# Install globally
npm install -g allure-commandline

# Verify installation
allure --version
```

#### Option 2: Using Homebrew (macOS only)
```bash
brew install allure

# Verify installation
allure --version
```

#### Option 3: Manual Installation (All Platforms)
```bash
# Download from: https://github.com/allure-framework/allure2/releases
# Extract to desired location
# Add to PATH environment variable
```

## ✅ Verification

Test your complete setup:

```bash
# 1. Test Java
java -version
# Expected: openjdk version "11.0.x" or higher

# 2. Test Allure CLI
allure --version
# Expected: 2.x.x

# 3. Test Python packages
python -c "import allure; print('✅ Allure Python integration OK!')"

# 4. Test complete workflow
cd your_project_folder
python allure_runner.py test_project test_feature
```

## 🎯 Usage Examples

### Basic Usage
```bash
# Generate test project first
python enhanced_cucumber_generator_fixed_v2.py

# Run with Allure reporting
python allure_runner.py my_project login
```

### Advanced Usage
```bash
# Run tests and open report automatically
python allure_runner.py my_project checkout

# When prompted:
# 🌐 Open Allure report in browser? (y/n): y
# 🖥️  Start Allure server for interactive report? (y/n): y
```

### Manual Allure Commands
```bash
# Generate static HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Serve interactive report
allure serve reports/allure-results

# Open static report in browser
open reports/allure-report/index.html  # macOS
start reports/allure-report/index.html  # Windows
xdg-open reports/allure-report/index.html  # Linux
```

## 🔧 Troubleshooting

### Issue: "Unable to locate a Java Runtime"
**Solution:**
```bash
# Check if Java is installed
java -version

# If not installed, install Java (see Step 2 above)
# If installed but not found, check PATH:
echo $JAVA_HOME
echo $PATH

# Add to PATH (adjust path as needed):
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
```

### Issue: "allure: command not found"
**Solution:**
```bash
# Check npm installation
npm list -g allure-commandline

# If not installed:
npm install -g allure-commandline

# If installed but not found, check npm global path:
npm config get prefix
# Add to PATH: {prefix}/bin
```

### Issue: "Permission denied" on macOS/Linux
**Solution:**
```bash
# Make runner executable
chmod +x allure_runner.py

# Or run with python explicitly
python allure_runner.py project_folder feature_name
```

### Issue: Port already in use for Allure server
**Solution:**
```bash
# Find process using port
lsof -i :53134

# Kill process if needed
kill -9 <PID>

# Or start server on different port
allure serve -p 8080 reports/allure-results
```

## 📊 Understanding Allure Reports

### Generated Files Structure:
```
project_folder/
├── reports/
│   ├── allure-results/          # Raw test data (JSON)
│   │   ├── environment.properties
│   │   ├── *-result.json        # Test results
│   │   ├── *-attachment.*       # Screenshots, logs
│   │   └── ...
│   ├── allure-report/           # Generated HTML report
│   │   ├── index.html          # Main report page
│   │   ├── data/               # Report data
│   │   └── ...
│   └── report_feature.html     # Basic HTML report
```

### Key Report Sections:
1. **Overview** - Summary statistics and graphs
2. **Categories** - Failure categorization
3. **Suites** - Test organization by feature
4. **Graphs** - Visual analytics and trends
5. **Timeline** - Execution flow over time
6. **Behaviors** - BDD scenarios grouped by epic/feature

## 🎨 Customization

### Environment Properties
The generator automatically creates `environment.properties`:
```properties
Feature.Name=login
Browser=Chromium
Test.Framework=Playwright + pytest-bdd
Reporting=Allure
Execution.Date=2025-08-03 10:30:00
Python.Version=3.11.10
```

### Custom Categories
Create `categories.json` in allure-results for custom failure categorization:
```json
[
  {
    "name": "UI Errors",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*ElementNotFound.*"
  },
  {
    "name": "Timeout Issues",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*TimeoutError.*"
  }
]
```

## 🏆 Best Practices

1. **Always run tests in clean environment** - Delete old allure-results before new runs
2. **Use descriptive step names** - They appear in the report timeline
3. **Attach relevant data** - Screenshots, logs, input data for better debugging
4. **Organize by features** - Use proper BDD structure for better report organization
5. **Regular cleanup** - Archive old reports to save disk space

## 📚 Additional Resources

- [Allure Official Documentation](https://docs.qameta.io/allure/)
- [Allure Pytest Plugin](https://github.com/allure-framework/allure-python)
- [Allure CLI Documentation](https://github.com/allure-framework/allure2)
- [Java Installation Guide](https://adoptopenjdk.net/installation.html)

---

**Need help?** Check the main README troubleshooting section or create an issue in the repository.
