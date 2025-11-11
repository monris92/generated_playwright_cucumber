#!/usr/bin/env python3
"""
Simple Playwright Test Recorder
Records Playwright scripts and organizes them in a good structure
No complicated conversions - just simple, working tests!
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime


class SimpleRecorder:
    """Simple test recorder - record once, run anytime"""

    def __init__(self):
        self.base_folder = None
        self.test_name = None
        self.website_url = None

    def run(self):
        """Main workflow"""
        print("=" * 70)
        print("🎬 SIMPLE PLAYWRIGHT TEST RECORDER")
        print("=" * 70)
        print("Record your test once → Run it anytime!")
        print()

        # Get inputs
        self.get_inputs()

        # Create structure
        self.create_structure()

        # Record test
        recorded_file = self.record_test()
        if not recorded_file:
            return False

        # Make it runnable
        self.create_test_runner(recorded_file)

        # Show instructions
        self.show_success()
        return True

    def get_inputs(self):
        """Get user inputs"""
        # Get folder
        folder = input("📁 Where to save tests? (press Enter for 'my_tests'): ").strip()
        if not folder:
            folder = "my_tests"

        self.base_folder = Path(folder).absolute()
        print(f"✅ Tests will be saved in: {self.base_folder}")

        # Get test name
        while True:
            test_name = input("\n🏷️  Test name (e.g., login, search, checkout): ").strip().lower()
            if test_name and test_name.replace('_', '').replace('-', '').isalnum():
                self.test_name = test_name
                break
            print("❌ Use only letters, numbers, hyphens, and underscores")

        # Get URL
        while True:
            url = input("\n🌐 Website URL to test: ").strip()
            if url.startswith(('http://', 'https://')):
                self.website_url = url
                break
            print("❌ URL must start with http:// or https://")

    def create_structure(self):
        """Create folder structure"""
        print(f"\n📂 Creating test structure...")

        # Create folders
        folders = [
            self.base_folder,
            self.base_folder / "tests",
            self.base_folder / "reports"
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

        print("✅ Folders created")

    def record_test(self):
        """Record the test"""
        print("\n🎬 RECORDING")
        print("-" * 70)
        print(f"🌐 Target: {self.website_url}")
        print("\n📝 Instructions:")
        print("   1. Browser will open")
        print("   2. Do your test actions")
        print("   3. Close browser when done")
        print("\nPress Enter to start...")
        input()

        output_file = self.base_folder / "tests" / f"{self.test_name}.py"

        try:
            # Try to run playwright codegen
            cmd = [
                sys.executable, "-m", "playwright", "codegen",
                self.website_url,
                "--target", "python-pytest",
                "--output", str(output_file)
            ]

            print("🎥 Recording... (perform your test actions)")
            subprocess.run(cmd, check=True)

            if output_file.exists():
                print(f"✅ Test recorded: {output_file.name}")
                return output_file
            else:
                print("❌ Recording failed - no file created")
                return None

        except subprocess.CalledProcessError as e:
            print(f"❌ Recording error: {e}")
            return None
        except FileNotFoundError:
            print("❌ Playwright not found!")
            print("💡 Install it: pip install playwright && playwright install")
            return None

    def create_test_runner(self, test_file):
        """Create simple test runner"""
        print("\n🔧 Setting up test runner...")

        # Create pytest.ini
        pytest_config = f"""[pytest]
testpaths = tests
python_files = *.py
python_functions = test_*
addopts =
    -v
    --html=reports/report.html
    --self-contained-html
"""

        pytest_file = self.base_folder / "pytest.ini"
        pytest_file.write_text(pytest_config)

        # Create run script
        run_script = f"""#!/usr/bin/env python3
\"\"\"
Test Runner for {self.test_name}
\"\"\"
import subprocess
import sys
from pathlib import Path

def run_test():
    project_dir = Path(__file__).parent
    test_file = project_dir / "tests" / "{self.test_name}.py"

    if not test_file.exists():
        print(f"❌ Test file not found: {{test_file}}")
        return False

    print(f"🚀 Running test: {self.test_name}")
    print(f"📁 Location: {{test_file}}")
    print()

    cmd = [
        sys.executable, "-m", "pytest",
        str(test_file),
        "-v",
        "--html", "reports/report.html",
        "--self-contained-html"
    ]

    result = subprocess.run(cmd, cwd=project_dir)

    if result.returncode == 0:
        print("\\n✅ Test PASSED!")
    else:
        print("\\n❌ Test FAILED!")

    print(f"📊 Report: {{project_dir / 'reports' / 'report.html'}}")
    return result.returncode == 0

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
"""

        run_file = self.base_folder / "run_test.py"
        run_file.write_text(run_script)
        run_file.chmod(0o755)

        # Create shell runner
        shell_script = f"""#!/bin/bash
# Simple test runner

cd "$(dirname "$0")"

echo "🚀 Running test: {self.test_name}"
python3 run_test.py
"""

        shell_file = self.base_folder / "run_test.sh"
        shell_file.write_text(shell_script)
        shell_file.chmod(0o755)

        # Create README
        readme = f"""# {self.test_name.replace('_', ' ').title()} Test

Recorded on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Website: {self.website_url}

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
pytest tests/{self.test_name}.py -v
```

## View results

Open `reports/report.html` in your browser

## Re-record

If you need to update the test:
```bash
python3 -m playwright codegen {self.website_url} --target python-pytest --output tests/{self.test_name}.py
```
"""

        readme_file = self.base_folder / "README.md"
        readme_file.write_text(readme)

        print("✅ Test runner created")

    def show_success(self):
        """Show success message"""
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your test is ready!")
        print("=" * 70)
        print(f"\n📁 Location: {self.base_folder}")
        print(f"🏷️  Test: {self.test_name}")
        print(f"🌐 URL: {self.website_url}")
        print("\n📋 How to run your test:")
        print(f"   cd {self.base_folder}")
        print(f"   python3 run_test.py")
        print("\n📊 Results will be in: reports/report.html")
        print("\n✨ That's it! Simple and working!")


def main():
    """Main entry point"""
    try:
        recorder = SimpleRecorder()
        success = recorder.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
