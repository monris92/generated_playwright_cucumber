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

    # Test priority definitions
    PRIORITIES = {
        'p0': {
            'name': 'Smoke Test',
            'description': 'Critical features that must pass before release',
            'marker': 'smoke',
            'folder': 'p0-smoke_test'
        },
        'p1': {
            'name': 'Regression',
            'description': 'Important features, run on every build',
            'marker': 'regression',
            'folder': 'p1-regression'
        },
        'p2': {
            'name': 'Exploratory',
            'description': 'Edge cases, UI validation, nice-to-have tests',
            'marker': 'exploratory',
            'folder': 'p2-exploratory'
        }
    }

    def __init__(self):
        self.base_folder = None
        self.test_name = None
        self.website_url = None
        self.priority = None
        self.mode = None  # 'record' or 'generate'
        self.existing_script = None  # Path to existing script if mode is 'generate'

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

        # Record or use existing test
        if self.mode == 'record':
            recorded_file = self.record_test()
            if not recorded_file:
                return False
        else:  # generate mode
            recorded_file = self.generate_from_existing()
            if not recorded_file:
                return False

        # Enhance the test (add waits, fix common issues)
        self.enhance_test(recorded_file)

        # Make it runnable
        self.create_test_runner(recorded_file)

        # Show instructions
        self.show_success()
        return True

    def select_existing_script(self):
        """Select existing script from codegen_script folder"""
        codegen_folder = Path("codegen_script")

        if not codegen_folder.exists():
            print(f"\n❌ Folder 'codegen_script' not found!")
            print("   This folder should contain your recorded Playwright scripts.")
            return False

        # Find all Python files in codegen_script
        script_files = list(codegen_folder.glob("*.py"))

        if not script_files:
            print(f"\n❌ No Python scripts found in 'codegen_script' folder!")
            print("   Please record a test first using mode 1 (Record new test)")
            return False

        print(f"\n📂 Available scripts in 'codegen_script':")
        for idx, script in enumerate(script_files, 1):
            print(f"   {idx}. {script.name}")

        while True:
            choice = input(f"\nSelect script [1-{len(script_files)}]: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(script_files):
                self.existing_script = script_files[int(choice) - 1]
                print(f"✅ Selected: {self.existing_script.name}")
                return True
            print(f"❌ Please enter a number between 1 and {len(script_files)}")

    def generate_from_existing(self):
        """Generate test structure from existing script"""
        if not self.existing_script or not self.existing_script.exists():
            print("❌ No existing script found!")
            return None

        print(f"\n📋 Generating test from: {self.existing_script.name}")

        # Output to test-specific folder
        priority_folder = self.base_folder / self.PRIORITIES[self.priority]['folder']
        test_folder = priority_folder / self.test_name
        output_file = test_folder / "tests" / f"{self.test_name}_test.py"

        try:
            # Read the existing script
            script_content = self.existing_script.read_text()

            # Write to the new location
            output_file.write_text(script_content)

            print(f"✅ Test generated: {output_file.name}")
            print(f"   Source: {self.existing_script}")
            print(f"   Destination: {output_file}")

            return output_file

        except Exception as e:
            print(f"❌ Error generating test: {e}")
            return None

    def get_inputs(self):
        """Get user inputs"""
        # Use e2e folder by default (skip question if it exists)
        self.base_folder = Path("e2e").absolute()

        if not self.base_folder.exists():
            # Only ask if e2e doesn't exist yet
            folder = input("📁 Base test folder? (press Enter for 'e2e'): ").strip()
            if not folder:
                folder = "e2e"
            self.base_folder = Path(folder).absolute()

        print(f"✅ Base folder: {self.base_folder}")

        # Get test priority
        print("\n📊 Test Priority:")
        print("   1. P0 - Smoke Test (Critical: login, checkout, core flows)")
        print("   2. P1 - Regression (Important: CRUD, search, filters)")
        print("   3. P2 - Exploratory (Nice-to-have: edge cases, UI validation)")

        while True:
            choice = input("Choose priority [1-3] (default: 2): ").strip()
            if not choice:
                choice = '2'

            if choice in ['1', '2', '3']:
                priority_map = {'1': 'p0', '2': 'p1', '3': 'p2'}
                self.priority = priority_map[choice]
                priority_info = self.PRIORITIES[self.priority]
                print(f"✅ Selected: {self.priority.upper()} - {priority_info['name']}")
                break
            print("❌ Please enter 1, 2, or 3")

        # Ask mode: record new or generate from existing
        print("\n🎯 Choose mode:")
        print("   1. Record new test (open browser and record)")
        print("   2. Generate from existing script (use script from codegen_script folder)")

        while True:
            mode_choice = input("Choose mode [1-2] (default: 1): ").strip()
            if not mode_choice:
                mode_choice = '1'

            if mode_choice in ['1', '2']:
                self.mode = 'record' if mode_choice == '1' else 'generate'
                print(f"✅ Mode: {'Record new test' if self.mode == 'record' else 'Generate from existing script'}")
                break
            print("❌ Please enter 1 or 2")

        # If generate mode, select existing script
        if self.mode == 'generate':
            if not self.select_existing_script():
                print("❌ No script selected, switching to record mode")
                self.mode = 'record'

        # Get test name
        while True:
            test_name = input("\n🏷️  Test name (e.g., login, search, checkout): ").strip().lower()
            if test_name and test_name.replace('_', '').replace('-', '').isalnum():
                self.test_name = test_name
                break
            print("❌ Use only letters, numbers, hyphens, and underscores")

        # Get URL only if recording new test
        if self.mode == 'record':
            while True:
                url = input("\n🌐 Website URL to test: ").strip()
                if url.startswith(('http://', 'https://')):
                    self.website_url = url
                    break
                print("❌ URL must start with http:// or https://")
        else:
            # For generate mode, we'll extract URL from script or use placeholder
            self.website_url = "Generated from existing script"

    def create_structure(self):
        """Create folder structure with priority-based organization"""
        print(f"\n📂 Creating test structure...")

        # Get priority folder info
        priority_info = self.PRIORITIES[self.priority]
        priority_folder = self.base_folder / priority_info['folder']

        # Create test-specific folder
        test_folder = priority_folder / self.test_name

        # Create folders
        folders = [
            self.base_folder,
            priority_folder,
            test_folder,
            test_folder / "tests",
            test_folder / "reports"
        ]

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

        # Note: We don't create __init__.py to avoid import conflicts with pytest
        # pytest will discover tests without __init__.py files

        print(f"✅ Folders created in {priority_info['folder']}/{self.test_name}/")

    def record_test(self):
        """Record the test"""
        print("\n🎬 RECORDING")
        print("-" * 70)
        print(f"🌐 Target: {self.website_url}")
        print(f"📊 Priority: {self.priority.upper()} - {self.PRIORITIES[self.priority]['name']}")
        print("\n📝 Instructions:")
        print("   1. Browser will open")
        print("   2. Do your test actions")
        print("   3. Close browser when done")
        print("\nPress Enter to start...")
        input()

        # First record to codegen_script folder (original script)
        codegen_folder = Path("codegen_script")
        codegen_folder.mkdir(exist_ok=True)

        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        codegen_file = codegen_folder / f"{self.test_name}_{timestamp}.py"

        try:
            # Try to run playwright codegen
            cmd = [
                sys.executable, "-m", "playwright", "codegen",
                self.website_url,
                "--target", "python-pytest",
                "--output", str(codegen_file)
            ]

            print("🎥 Recording... (perform your test actions)")
            subprocess.run(cmd, check=True)

            if codegen_file.exists():
                print(f"✅ Original script saved: {codegen_file}")

                # Copy to test folder
                priority_folder = self.base_folder / self.PRIORITIES[self.priority]['folder']
                test_folder = priority_folder / self.test_name
                output_file = test_folder / "tests" / f"{self.test_name}_test.py"

                # Copy the content
                output_file.write_text(codegen_file.read_text())
                print(f"✅ Test copied to: {output_file.name}")

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

    def enhance_test(self, test_file):
        """Enhance the recorded test with smart waits and fixes"""
        print("\n🔧 Enhancing test with smart waits...")

        try:
            # Import the enhancer
            from utils.test_enhancer import TestEnhancer

            # Get priority marker
            marker = self.PRIORITIES[self.priority]['marker']

            enhancer = TestEnhancer(test_file)
            enhancer.enhance_in_place(marker=marker)

            print("✅ Test enhanced with:")
            print("   • Simple, reliable waits after page.goto()")
            print("   • Smart button click strategies:")
            print("     - Verify element visible and ENABLED")
            print("     - Wait for animations (500ms)")
            print("     - Click with delay (200ms)")
            print("   • Element visibility checks before assertions")
            print("   • URL validation instead of redundant page.goto()")
            print(f"   • Pytest marker: @pytest.mark.{marker}")
            print()
            print("   ℹ️  Using simple timeouts (not networkidle) for reliability")

        except Exception as e:
            print(f"⚠️  Enhancement skipped: {e}")
            print("   Test will still work, but may need manual tweaks")

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
