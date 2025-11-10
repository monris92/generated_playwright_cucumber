#!/usr/bin/env python3
"""
Playwright to Cucumber BDD Generator
Converts Playwright recordings into production-ready Cucumber BDD test projects
"""

import subprocess
import os
import requests
import json
import sys
import re
import py_compile
import logging
import stat
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CucumberGenerator:
    """Main generator class for converting Playwright scripts to Cucumber BDD format"""

    def __init__(self):
        """Initialize the generator with Mistral AI configuration"""
        self.mistral_api_key = "jXiU2TQZM4Rj13JJD44Gp0mm4iLZVCJx"
        self.mistral_api_url = "https://api.mistral.ai/v1/chat/completions"
        self.base_folder = None
        self.feature_label = None
        self.website_url = None

    def run_workflow(self):
        """Run the complete workflow: setup -> record -> convert"""
        try:
            print("=" * 70)
            print("🎭 PLAYWRIGHT TO CUCUMBER BDD GENERATOR")
            print("=" * 70)

            # Step 1: Setup project
            self.setup_project()

            # Step 2: Record Playwright script
            recorded_file = self.record_playwright_script()
            if not recorded_file:
                logger.error("Recording failed")
                return False

            # Step 3: Convert to Cucumber
            success = self.convert_to_cucumber(recorded_file)
            if not success:
                logger.error("Conversion failed")
                return False

            # Step 4: Show success message
            self.show_completion_message()
            return True

        except KeyboardInterrupt:
            print("\n\n⏹️  Workflow cancelled by user.")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            print(f"\n❌ Unexpected error: {e}")
            return False

    # ========================================
    # PROJECT SETUP
    # ========================================

    def setup_project(self):
        """Setup project structure and get user inputs"""
        print("\n📋 PROJECT SETUP")
        print("-" * 70)

        # Get project location
        self._get_project_folder()

        # Get feature name
        self._get_feature_name()

        # Get website URL
        self._get_website_url()

        # Create project structure
        self._create_project_structure()

        logger.info(f"Project created at: {self.base_folder}")

    def _get_project_folder(self):
        """Get and validate project folder location"""
        while True:
            folder_input = input("\n📁 Enter project folder (or press Enter for current folder): ").strip()

            if not folder_input:
                self.base_folder = Path.cwd()
                print(f"✅ Using current folder: {self.base_folder}")
                break
            else:
                folder_path = Path(folder_input)
                if not folder_path.exists():
                    create = input(f"📂 Folder '{folder_path}' doesn't exist. Create it? (y/n): ").strip().lower()
                    if create in ['y', 'yes']:
                        try:
                            folder_path.mkdir(parents=True, exist_ok=True)
                            self.base_folder = folder_path
                            print(f"✅ Folder created: {folder_path}")
                            break
                        except Exception as e:
                            print(f"❌ Error creating folder: {e}")
                            continue
                else:
                    self.base_folder = folder_path
                    print(f"✅ Using folder: {self.base_folder}")
                    break

    def _get_feature_name(self):
        """Get and validate feature name"""
        while True:
            feature = input("\n🏷️  Enter feature name (e.g., login, search, checkout): ").strip().lower()
            if feature and feature.replace('_', '').replace('-', '').isalnum():
                self.feature_label = feature
                print(f"✅ Feature: {self.feature_label}")
                break
            else:
                print("❌ Feature name must be alphanumeric (underscores and hyphens allowed)")

    def _get_website_url(self):
        """Get and validate website URL"""
        while True:
            url = input("\n🌐 Enter website URL to test: ").strip()
            if url.startswith(('http://', 'https://')):
                self.website_url = url
                print(f"✅ Target URL: {self.website_url}")
                break
            else:
                print("❌ URL must start with http:// or https://")

    def _create_project_structure(self):
        """Create complete project structure with all necessary files"""
        print("\n📂 Creating project structure...")

        # Create folders
        folders = [
            "features",
            f"features/{self.feature_label}",
            "features/steps",
            "tests",
            "config",
            "reports"
        ]

        for folder in folders:
            (self.base_folder / folder).mkdir(parents=True, exist_ok=True)

        # Create configuration files
        self._create_config_file()
        self._create_pytest_config()

        # Create runner scripts
        self._create_python_runner()
        self._create_shell_runner()

        print("✅ Project structure created")

    def _create_config_file(self):
        """Create test configuration file"""
        config = {
            "project_name": f"Test_{self.feature_label}",
            "created_date": datetime.now().isoformat(),
            "website_url": self.website_url,
            "feature_label": self.feature_label,
            "mistral_config": {
                "model": "mistral-large-latest",
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "playwright_config": {
                "headless": False,
                "timeout": 30000
            }
        }

        config_file = self.base_folder / "config" / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        logger.info(f"Config file created: {config_file}")

    def _create_pytest_config(self):
        """Create pytest.ini configuration"""
        config = f"""[tool:pytest]
bdd_features_base_dir = features
markers =
    {self.feature_label}: {self.feature_label} feature tests
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""

        pytest_file = self.base_folder / "pytest.ini"
        with open(pytest_file, 'w', encoding='utf-8') as f:
            f.write(config)

        logger.info("pytest.ini created")

    def _create_python_runner(self):
        """Create Python test runner script"""
        content = f'''#!/usr/bin/env python3
"""
Test Runner for {self.feature_label}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import sys
import subprocess
from pathlib import Path

def run_tests(feature_name):
    """Run tests for the specified feature"""
    print(f"🧪 Running tests for: {{feature_name}}")

    # Validate feature exists
    feature_dir = Path(__file__).parent / "features" / feature_name
    if not feature_dir.exists():
        print(f"❌ Feature directory not found: {{feature_dir}}")
        return False

    test_file = Path(__file__).parent / f"test_{{feature_name}}.py"
    if not test_file.exists():
        print(f"❌ Test file not found: {{test_file}}")
        return False

    # Setup reports directory
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    # Find Python executable (prefer venv)
    python_exe = find_python()
    print(f"🐍 Using Python: {{python_exe}}")

    # Run pytest
    cmd = [
        python_exe, "-m", "pytest",
        str(test_file),
        "--html", str(reports_dir / f"report_{{feature_name}}.html"),
        "--self-contained-html",
        "-v", "--tb=short"
    ]

    print(f"🚀 Running: {{' '.join(cmd)}}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"✅ Tests passed! Report: {{reports_dir / f'report_{{feature_name}}.html'}}")
        return True
    else:
        print(f"❌ Tests failed! Check: {{reports_dir / f'report_{{feature_name}}.html'}}")
        return False

def find_python():
    """Find the best Python executable"""
    # Try parent venv
    parent_venv = Path(__file__).parent.parent / "venv" / "bin" / "python"
    if parent_venv.exists():
        return str(parent_venv)

    # Try local venv
    local_venv = Path(__file__).parent / "venv" / "bin" / "python"
    if local_venv.exists():
        return str(local_venv)

    # Use current Python
    return sys.executable

if __name__ == "__main__":
    feature = sys.argv[1] if len(sys.argv) > 1 else "{self.feature_label}"
    run_tests(feature)
'''

        runner_file = self.base_folder / "run_tests.py"
        with open(runner_file, 'w', encoding='utf-8') as f:
            f.write(content)
        runner_file.chmod(runner_file.stat().st_mode | stat.S_IEXEC)

        logger.info("Python runner created")

    def _create_shell_runner(self):
        """Create shell script runner"""
        content = f'''#!/bin/bash
# Test Runner for {self.feature_label}

echo "🎭 Test Runner for {self.feature_label}"
echo "========================================"

PROJECT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_DIR")"
VENV_PYTHON="$PARENT_DIR/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found: $VENV_PYTHON"
    echo "💡 Please ensure venv is set up in parent directory"
    exit 1
fi

FEATURE_NAME="${self.feature_label}"
[ $# -eq 1 ] && FEATURE_NAME="$1"

echo "🎯 Running feature: $FEATURE_NAME"
cd "$PROJECT_DIR"

"$VENV_PYTHON" run_tests.py "$FEATURE_NAME"

echo "✅ Done! Check reports/report_${{FEATURE_NAME}}.html"
'''

        shell_file = self.base_folder / "run_tests.sh"
        with open(shell_file, 'w', encoding='utf-8') as f:
            f.write(content)
        shell_file.chmod(shell_file.stat().st_mode | stat.S_IEXEC)

        logger.info("Shell runner created")

    # ========================================
    # PLAYWRIGHT RECORDING
    # ========================================

    def record_playwright_script(self):
        """Record user actions using Playwright Codegen"""
        print("\n🎬 RECORDING PHASE")
        print("-" * 70)
        print(f"🌐 Target: {self.website_url}")
        print("\n📝 Instructions:")
        print("   1. Browser will open automatically")
        print("   2. Perform the actions you want to test")
        print("   3. Close the browser when finished")
        print("\nPress Enter to start recording...")
        input()

        output_file = self.base_folder / "tests" / f"recorded_{self.feature_label}.py"
        playwright_cmd = self._get_playwright_command()

        try:
            cmd = playwright_cmd + ["codegen", self.website_url, "--output", str(output_file)]
            logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"✅ Script recorded: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"Recording failed: {e}")
            print(f"❌ Recording failed: {e}")
            return None
        except FileNotFoundError:
            print("❌ Playwright not found!")
            print("💡 Install with: pip install playwright && playwright install")
            return None

    def _get_playwright_command(self):
        """Get the Playwright command to execute"""
        import shutil

        # Try to find playwright executable
        playwright_path = shutil.which('playwright')
        if playwright_path:
            return [playwright_path]

        # Try Python module
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'playwright', '--help'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return [sys.executable, '-m', 'playwright']
        except:
            pass

        # Default fallback
        return ['playwright']

    # ========================================
    # CUCUMBER CONVERSION
    # ========================================

    def convert_to_cucumber(self, recorded_file):
        """Convert recorded Playwright script to Cucumber BDD format"""
        print("\n🤖 CONVERSION PHASE")
        print("-" * 70)
        print("Converting to Cucumber BDD format using AI...")

        try:
            # Read the recorded script
            with open(recorded_file, 'r', encoding='utf-8') as f:
                script_content = f.read()

            # Generate BDD files using AI
            feature_content, steps_content = self._generate_bdd_with_ai(script_content)

            # Validate and fix any issues
            steps_content = self._validate_and_fix(feature_content, steps_content)

            # Save generated files
            self._save_bdd_files(feature_content, steps_content)

            # Create test file
            self._create_test_file()

            print("✅ Conversion completed successfully")
            return True

        except Exception as e:
            logger.exception(f"Conversion failed: {e}")
            print(f"❌ Conversion failed: {e}")
            return False

    def _generate_bdd_with_ai(self, script_content):
        """Generate BDD feature and steps using Mistral AI"""
        prompt = self._build_ai_prompt(script_content)

        # Call Mistral AI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.mistral_api_key}"
        }

        payload = {
            "model": "mistral-large-latest",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 4096,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(
            self.mistral_api_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        # Parse response
        result = response.json()
        content = json.loads(result["choices"][0]["message"]["content"])

        feature = self._clean_markdown(content["feature"])
        steps = self._clean_markdown(content["steps"])

        return feature, steps

    def _build_ai_prompt(self, script_content):
        """Build the AI prompt for conversion"""
        return f"""Convert this Playwright Python script into Cucumber BDD format.

REQUIREMENTS:
1. Feature file: Use single quotes (') in Gherkin steps
2. Step definitions: Use double quotes (") for decorators
3. Add @{self.feature_label} tag to feature
4. Include proper imports: playwright.sync_api, pytest_bdd, pytest, re
5. Add wait_for_load_state('networkidle') after page.goto()
6. Add appropriate timeouts for actions
7. Include try-catch blocks for assertions
8. Ensure every feature step has matching step definition

Playwright Script:
{script_content}

Website URL: {self.website_url}

Return JSON with this structure:
{{
    "feature": "Complete Gherkin feature file",
    "steps": "Complete Python step definitions"
}}"""

    def _clean_markdown(self, content):
        """Remove markdown formatting from content"""
        if not content:
            return content

        lines = content.split('\n')
        cleaned = []

        for line in lines:
            # Skip markdown code blocks
            if line.strip().startswith('```'):
                continue
            if line.strip():
                cleaned.append(line.rstrip())

        return '\n'.join(cleaned)

    def _validate_and_fix(self, feature_content, steps_content):
        """Validate quote consistency and fix any issues"""
        # Extract steps from feature
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
        feature_texts = {step[1].strip() for step in feature_steps}

        # Extract step decorators
        step_decorators = re.findall(r'@(given|when|then)\("([^"]+)"\)', steps_content)
        step_texts = {step[1].strip() for step in step_decorators}

        # Check for mismatches
        missing = feature_texts - step_texts
        if missing:
            logger.warning(f"Missing step definitions for: {missing}")
            print(f"⚠️  Auto-fixing step definition mismatches...")
            steps_content = self._fix_step_definitions(feature_content, steps_content)

        return steps_content

    def _fix_step_definitions(self, feature_content, steps_content):
        """Fix step definition quote inconsistencies"""
        # Extract feature steps
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)

        # Build mapping
        step_map = {}
        for step in feature_steps:
            normalized = step[1].strip().replace('"', "'")
            step_map[normalized] = step[1].strip()

        # Fix decorators
        def fix_decorator(match):
            decorator_type = match.group(1)
            current_text = match.group(2)
            normalized = current_text.replace('"', "'")

            if normalized in step_map:
                correct_text = step_map[normalized]
                escaped = correct_text.replace('"', '\\"')
                return f'@{decorator_type}("{escaped}")'

            return match.group(0)

        fixed_content = re.sub(
            r'@(given|when|then)\("([^"]+)"\)',
            fix_decorator,
            steps_content
        )

        return fixed_content

    def _save_bdd_files(self, feature_content, steps_content):
        """Save feature and step definition files"""
        # Save feature file
        feature_file = self.base_folder / "features" / self.feature_label / f"{self.feature_label}.feature"
        with open(feature_file, 'w', encoding='utf-8') as f:
            f.write(feature_content)
        print(f"✅ Feature file: {feature_file}")

        # Save steps file
        steps_file = self.base_folder / "features" / "steps" / f"{self.feature_label}_steps.py"
        with open(steps_file, 'w', encoding='utf-8') as f:
            f.write(steps_content)
        print(f"✅ Steps file: {steps_file}")

        # Validate Python syntax
        self._validate_python_syntax(steps_file)

    def _validate_python_syntax(self, file_path):
        """Validate Python file syntax"""
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"✅ Syntax validation passed")
            logger.info(f"Syntax valid: {file_path}")
        except py_compile.PyCompileError as e:
            logger.error(f"Syntax error: {e}")
            print(f"❌ Syntax error in generated file: {e}")

    def _create_test_file(self):
        """Create pytest test file"""
        content = f'''import pytest
from pytest_bdd import scenarios
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

# Set working directory
os.chdir(Path(__file__).parent)

# Import step definitions
from features.steps.{self.feature_label}_steps import *

# Load feature scenarios
scenarios('features/{self.feature_label}/{self.feature_label}.feature')

@pytest.fixture(scope="session")
def browser():
    """Create browser instance"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser):
    """Create browser context"""
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create new page"""
    page = context.new_page()
    yield page
    page.close()
'''

        test_file = self.base_folder / f"test_{self.feature_label}.py"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Test file: {test_file}")

    # ========================================
    # COMPLETION
    # ========================================

    def show_completion_message(self):
        """Show workflow completion message with next steps"""
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your Cucumber BDD project is ready!")
        print("=" * 70)
        print(f"\n📁 Project Location: {self.base_folder}")
        print(f"🏷️  Feature Name: {self.feature_label}")
        print(f"🌐 Target URL: {self.website_url}")
        print("\n📋 Next Steps:")
        print(f"   1. cd {self.base_folder}")
        print(f"   2. ./run_tests.sh")
        print(f"\n📊 View Results: reports/report_{self.feature_label}.html")
        print("\n🚀 Happy Testing!")


def main():
    """Main entry point"""
    generator = CucumberGenerator()
    success = generator.run_workflow()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
