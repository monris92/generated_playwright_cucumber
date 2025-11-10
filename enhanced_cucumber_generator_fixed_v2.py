import subprocess
import os
import requests
import json
import sys
import re
import py_compile
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CucumberGenerator:
    def __init__(self):
        self.mistral_api_key = "jXiU2TQZM4Rj13JJD44Gp0mm4iLZVCJx"
        self.mistral_api_url = "https://api.mistral.ai/v1/chat/completions"
        self.base_folder = None
        self.feature_label = None
        self.website_url = None
        
    def setup_project_structure(self):
        """Setup project structure and get user inputs"""
        print("=" * 60)
        print("🎭 PLAYWRIGHT TO CUCUMBER GENERATOR")
        print("=" * 60)
        
        # Get folder location
        while True:
            folder_input = input("\n📁 Masukkan lokasi folder project (atau tekan Enter untuk folder saat ini): ").strip()
            
            if not folder_input:
                self.base_folder = Path.cwd()
                print(f"✅ Menggunakan folder saat ini: {self.base_folder}")
                break
            else:
                folder_path = Path(folder_input)
                if not folder_path.exists():
                    create_folder = input(f"📂 Folder '{folder_path}' belum ada. Buat folder baru? (y/n): ").strip().lower()
                    if create_folder in ['y', 'yes']:
                        try:
                            folder_path.mkdir(parents=True, exist_ok=True)
                            self.base_folder = folder_path
                            print(f"✅ Folder '{folder_path}' berhasil dibuat!")
                            break
                        except Exception as e:
                            print(f"❌ Error membuat folder: {e}")
                            continue
                    else:
                        continue
                else:
                    self.base_folder = folder_path
                    print(f"✅ Menggunakan folder: {self.base_folder}")
                    break
        
        # Get feature label
        while True:
            self.feature_label = input("\n🏷️  Masukkan nama feature (contoh: pencarian, login, checkout): ").strip().lower()
            if self.feature_label and self.feature_label.replace('_', '').replace('-', '').isalnum():
                print(f"✅ Feature label: {self.feature_label}")
                break
            else:
                print("❌ Feature label harus berupa kata tanpa spasi dan karakter khusus!")
        
        # Get website URL
        while True:
            self.website_url = input("\n🌐 Masukkan URL website yang akan ditest: ").strip()
            if self.website_url.startswith(('http://', 'https://')):
                print(f"✅ Target URL: {self.website_url}")
                break
            else:
                print("❌ URL harus dimulai dengan http:// atau https://")
        
        # Create folder structure
        self.create_folder_structure()
        self.create_config_file()
        self.create_runner_script()
        # Create shell script runner
        self.create_shell_runner()
        
        print(f"📁 Project structure created in: {self.base_folder}")
        
    def create_folder_structure(self):
        """Create folder structure for the project"""
        folders = [
            "features",
            f"features/{self.feature_label}",
            "features/steps",
            "tests",
            "config",
            "reports"
        ]
        
        for folder in folders:
            folder_path = self.base_folder / folder
            folder_path.mkdir(parents=True, exist_ok=True)
        
        print("📂 Folder structure created!")
    
    def create_config_file(self):
        """Create configuration file"""
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
        
        print(f"⚙️  Config file: {config_file}")
    
    def create_runner_script(self):
        """Create test runner script"""
        runner_content = f'''#!/usr/bin/env python3
"""
🎭 Playwright to Cucumber Test Runner
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Feature: {self.feature_label}
"""

import sys
import subprocess
import json
from pathlib import Path

def load_config():
    """Load test configuration"""
    config_file = Path(__file__).parent / "config" / "test_config.json"
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_specific_feature(feature_label):
    """Run tests for specific feature label"""
    print(f"🧪 Running tests for feature: {{feature_label}}")
    
    # Find feature files with the label
    feature_dir = Path(__file__).parent / "features" / feature_label
    if not feature_dir.exists():
        print(f"❌ Feature directory not found: {{feature_dir}}")
        return False
    
    feature_files = list(feature_dir.glob("*.feature"))
    if not feature_files:
        print(f"❌ No feature files found in {{feature_dir}}")
        return False
    
    # Run pytest for the specific feature
    test_file = Path(__file__).parent / f"test_{{feature_label}}.py"
    if not test_file.exists():
        print(f"❌ Test file not found: {{test_file}}")
        return False
    
    print(f"🚀 Running: {{test_file}}")
    
    # Create reports directory
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Find the correct Python executable (preferably from virtual environment)
    def find_python_executable():
        # Try virtual environment from parent directory first
        parent_venv = Path(__file__).parent.parent / "venv" / "bin" / "python"
        if parent_venv.exists():
            return str(parent_venv)
        
        # Try local virtual environment
        local_venv = Path(__file__).parent / "venv" / "bin" / "python"
        if local_venv.exists():
            return str(local_venv)
        
        # Fallback to current Python
        return sys.executable
    
    python_exe = find_python_executable()
    print(f"🐍 Using Python: {{python_exe}}")
    
    # Run pytest with HTML report using the correct Python executable
    cmd = [
        python_exe, "-m", "pytest", 
        str(test_file),
        "--html", str(reports_dir / f"report_{{feature_label}}.html"),
        "--self-contained-html",
        "-v", "--tb=short"
    ]
    
    try:
        print(f"🔧 Running command: {{' '.join(cmd)}}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Tests passed! Report: {{reports_dir / f'report_{{feature_label}}.html'}}")
            return True
        else:
            print(f"❌ Tests failed! Check report: {{reports_dir / f'report_{{feature_label}}.html'}}")
            print("💡 Make sure all dependencies are installed in the virtual environment")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {{e}}")
        print("💡 Try running with virtual environment activated:")
        print(f"   source ../venv/bin/activate && python run_tests.py {{feature_label}}")
        return False

def main():
    if len(sys.argv) > 1:
        feature_label = sys.argv[1]
        run_specific_feature(feature_label)
    else:
        config = load_config()
        print(f"📋 Available feature: {{config['feature_label']}}")
        print(f"Usage: python run_tests.py {{config['feature_label']}}")

if __name__ == "__main__":
    main()
'''
        
        runner_file = self.base_folder / "run_tests.py"
        with open(runner_file, 'w', encoding='utf-8') as f:
            f.write(runner_content)
        
        print(f"🎯 Runner script: {runner_file}")
    
    def create_shell_runner(self):
        """Create shell script runner"""
        shell_content = f'''#!/bin/bash

# Enhanced Test Runner for {self.feature_label}
# This script handles virtual environment automatically

echo "🎭 Enhanced Test Runner for {self.feature_label}"
echo "==============================================="

# Get the directory where this script is located
PROJECT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_DIR")"
VENV_PYTHON="$PARENT_DIR/venv/bin/python"

echo "📍 Project directory: $PROJECT_DIR"
echo "🐍 Looking for Python at: $VENV_PYTHON"

# Check if parent virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found at: $VENV_PYTHON"
    echo "💡 Please run the generator from the parent directory first:"
    echo "   cd '$PARENT_DIR'"
    echo "   ./run_fixed.sh"
    exit 1
fi

# Get feature name from command line or use default
FEATURE_NAME="${self.feature_label}"
if [ $# -eq 1 ]; then
    FEATURE_NAME="$1"
fi

echo "🎯 Running feature: $FEATURE_NAME"

# Change to project directory
cd "$PROJECT_DIR"

echo "🚀 Running tests with virtual environment Python..."
echo ""

# Run the Python test runner with the correct Python executable
"$VENV_PYTHON" run_tests.py "$FEATURE_NAME"

echo ""
echo "✅ Test runner finished!"
echo "📊 Check reports/report_${{FEATURE_NAME}}.html for detailed results"
'''

        shell_file = self.base_folder / "run_tests.sh"
        with open(shell_file, 'w', encoding='utf-8') as f:
            f.write(shell_content)
        
        # Make it executable
        import stat
        shell_file.chmod(shell_file.stat().st_mode | stat.S_IEXEC)
        
        print(f"🔧 Shell runner: {shell_file}")
    
    def record_script(self):
        """Record script with Playwright Codegen"""
        print(f"\n🎬 Starting Playwright Codegen recording for '{self.feature_label}'...")
        print(f"🌐 Target URL: {self.website_url}")
        print("\n📝 Instructions:")
        print("1. Browser akan terbuka otomatis")
        print("2. Lakukan aksi yang ingin ditest")
        print("3. Tutup browser untuk menyelesaikan recording")
        print("\nPress Enter to start recording...")
        input()
        
        record_output = self.base_folder / "tests" / f"recorded_{self.feature_label}.py"
        
        # Get the correct playwright path from virtual environment
        playwright_path = self.get_playwright_path()
        
        try:
            # Handle both direct executable and python module execution
            if playwright_path.endswith(" -m playwright"):
                # Split the command for subprocess
                cmd_parts = playwright_path.split() + ["codegen", self.website_url, "--output", str(record_output)]
            else:
                cmd_parts = [playwright_path, "codegen", self.website_url, "--output", str(record_output)]
            
            logging.info(f"Running command: {' '.join(cmd_parts)}")
            subprocess.run(cmd_parts, check=True, text=True)
            
            print(f"✅ Script recorded: {record_output}")
            return record_output
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during recording: {e}")
            logging.error(f"Playwright recording failed: {e}")
            return None
        except FileNotFoundError:
            print(f"❌ Playwright not found!")
            print("💡 Please ensure Playwright is properly installed:")
            print("   1. Activate virtual environment: source venv/bin/activate")
            print("   2. Install Playwright: pip install playwright")
            print("   3. Install browsers: playwright install")
            print("   4. Run this script again")
            logging.error(f"Playwright executable not found at: {playwright_path}")
            return None
    
    def get_playwright_path(self):
        """Get the correct playwright executable path"""
        import shutil
        import sys
        
        logging.info("Searching for Playwright executable...")
        
        # First try to find playwright in current virtual environment
        if hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix:
            # We're in a virtual environment
            venv_playwright = Path(sys.prefix) / 'bin' / 'playwright'
            if venv_playwright.exists() and venv_playwright.is_file():
                logging.info(f"Found Playwright in current venv: {venv_playwright}")
                return str(venv_playwright)
        
        # Try to find playwright in the script's local virtual environment
        script_dir = Path(__file__).parent
        venv_playwright = script_dir / 'venv' / 'bin' / 'playwright'
        if venv_playwright.exists() and venv_playwright.is_file():
            logging.info(f"Found Playwright in local venv: {venv_playwright}")
            return str(venv_playwright)
        
        # Try common venv locations
        possible_venv_paths = [
            script_dir / '.venv' / 'bin' / 'playwright',
            script_dir / 'env' / 'bin' / 'playwright',
            Path.home() / '.local' / 'bin' / 'playwright'
        ]
        
        for path in possible_venv_paths:
            if path.exists() and path.is_file():
                logging.info(f"Found Playwright at: {path}")
                return str(path)
        
        # Fallback to system playwright
        playwright_path = shutil.which('playwright')
        if playwright_path:
            logging.info(f"Found system Playwright: {playwright_path}")
            return playwright_path
        
        # If nothing found, check if we can find python executable with playwright module
        try:
            result = subprocess.run([sys.executable, '-m', 'playwright', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                logging.info("Found Playwright via python module")
                return f"{sys.executable} -m playwright"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        logging.error("Playwright executable not found")
        # Return the expected venv path for error message
        return str(script_dir / 'venv' / 'bin' / 'playwright')

    def convert_to_cucumber(self, recorded_file):
        """Convert recorded script to Cucumber format"""
        print(f"\n🤖 Converting to Cucumber format using Mistral AI...")
        logging.info(f"Starting conversion of {recorded_file}")
        
        try:
            # Read recorded script
            with open(recorded_file, "r", encoding='utf-8') as file:
                script_content = file.read()
            logging.info("Successfully read recorded script")
                
            # Ultra-optimized prompt with enhanced quote consistency and error prevention
            prompt_content = f"""Convert the following Playwright Python script into a Cucumber feature file (Gherkin syntax) and corresponding step definitions in Python. 

ULTRA-CRITICAL REQUIREMENTS - FOLLOW EXACTLY:

1. TEXT PRESERVATION (MANDATORY):
   - Preserve EXACT text from the script, character-by-character.
   - Example: If script contains "websites", use "websites" (NOT "website").
   - Do NOT modify singular/plural forms, capitalization, or any text content.
   - Ensure ALL text in steps matches the original script exactly.

2. QUOTE CONSISTENCY (MANDATORY):
   - Feature file: Use SINGLE quotes (') for all text content in Gherkin steps.
   - Step definitions: Use DOUBLE quotes (") for decorator strings, but preserve inner quotes EXACTLY as they appear in the feature file.
   - Example: Feature step: When User enters 'auck' in the search box
   - Step definition MUST be: @when("User enters 'auck' in the search box")
   - Validate that every step in the feature file has a matching step definition with IDENTICAL text (except for outer double quotes in decorators).

3. ERROR PREVENTION:
   - Avoid typos by double-checking all generated text against the input script.
   - Ensure proper syntax for Python decorators (@given, @when, @then) with no missing or extra characters.
   - Use exact locator text from the script for page interactions (e.g., page.get_by_text('exact text')).
   - Validate that all generated steps are syntactically correct and executable.

4. ROBUST TIMING & ERROR HANDLING:
   - Add page.wait_for_load_state('networkidle') after every page.goto().
   - Add page.wait_for_timeout(1000-3000ms) after button clicks, with 5000ms for login/submit actions.
   - Wrap critical assertions in try-except blocks with a single retry after page.wait_for_timeout(1500).
   - For visibility checks, add page.wait_for_timeout(3000) before retries.

5. NATURAL NAVIGATION STRATEGY:
   - Detect post-action navigation (e.g., page.goto() after login/submit/click) and avoid generating separate navigation steps.
   - Example: After "When User clicks 'LOGIN'", use longer timeout (5000ms) and expect natural redirect instead of adding "When User navigates to X".
   - Use expect(page).to_have_url() for URL assertions, with regex for flexibility (e.g., re.compile(r'.*example.com/page.*')).

6. CODE STRUCTURE:
   - Import EXACTLY: from playwright.sync_api import expect, from pytest_bdd import given, when, then, import pytest, import re.
   - Do NOT include scenarios() call in step definitions.
   - Use 4-space indentation for all code blocks.
   - Ensure no markdown code blocks (```) or formatting in output.

7. BDD BEST PRACTICES:
   - Feature file must include tag: @{self.feature_label}
   - Feature name must be descriptive and include '{self.feature_label}'.
   - Use Given/When/Then structure, with atomic and testable steps.
   - Ensure every Gherkin step has a corresponding step definition.

Playwright Script:
{script_content}

EXAMPLE OUTPUT FORMAT (NO MARKDOWN):

Feature file:
Feature: {self.feature_label} Testing
  @{self.feature_label}
  Scenario: Test {self.feature_label} functionality
    Given User navigates to the website
    When User enters 'search term' in the box
    Then 'Result' should be visible

Step definitions:
from playwright.sync_api import expect
from pytest_bdd import given, when, then
import pytest
import re

@given("User navigates to the website")
def navigate_to_website(page):
    page.goto('{self.website_url}')
    page.wait_for_load_state('networkidle')

@when("User enters 'search term' in the box")
def enter_search_term(page):
    page.get_by_role('textbox', name='Search').click()
    page.wait_for_timeout(1000)
    page.get_by_role('textbox', name='Search').fill('search term')

@then("'Result' should be visible")
def verify_result(page):
    try:
        expect(page.get_by_text('Result', exact=True)).to_be_visible()
    except:
        page.wait_for_timeout(1500)
        expect(page.get_by_text('Result', exact=True)).to_be_visible()

Return your response as JSON with this exact structure:
{{
    "feature": "Complete Gherkin feature file with @{self.feature_label} tag",
    "steps": "Complete Python step definitions with DOUBLE quotes for decorators"
}}"""

            messages = [{
                "role": "user", 
                "content": prompt_content
            }]
            
            # API request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json", 
                "Authorization": f"Bearer {self.mistral_api_key}"
            }
            
            payload = {
                "model": "mistral-large-latest",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4096,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                self.mistral_api_url,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            
            # Parse result
            response_data = response.json()
            result = json.loads(response_data["choices"][0]["message"]["content"])
            logging.info("Successfully parsed AI response")
            
            # Clean up the result to remove any remaining markdown
            feature_content = self.clean_markdown_formatting(result["feature"])
            steps_content = self.clean_markdown_formatting(result["steps"])
            logging.info("Cleaned markdown formatting")
            
            # Enhanced validation with multiple checks
            validation_issues = self.validate_quote_consistency(feature_content, steps_content)
            enhanced_issues = self.enhanced_quote_validation(feature_content, steps_content)
            all_issues = validation_issues + enhanced_issues
            
            if all_issues:
                print("⚠️  Validation issues found:")
                for issue in all_issues:
                    print(f"   • {issue}")
                    logging.warning(f"Validation issue: {issue}")
                print("🔧 Auto-fixing quote inconsistencies...")
                steps_content = self.fix_quote_inconsistencies(feature_content, steps_content)
                logging.info("Applied quote consistency fixes")
            
            # Save files
            feature_output = self.base_folder / "features" / self.feature_label / f"{self.feature_label}.feature"
            steps_output = self.base_folder / "features" / "steps" / f"{self.feature_label}_steps.py"
            
            with open(feature_output, "w", encoding='utf-8') as f:
                f.write(feature_content)
            print(f"✅ Feature file: {feature_output}")
            
            with open(steps_output, "w", encoding='utf-8') as f:
                f.write(steps_content)
            print(f"✅ Steps file: {steps_output}")
            logging.info(f"Generated steps file: {steps_output}")
            
            # Auto post-process generated files
            self.post_process_generated_files()
            
            # Create test file with robust path handling and pytest config
            self.create_test_file()
            self.create_pytest_config()
            
            return True
            
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            logging.error(f"Conversion failed: {e}")
            return False
    
    def clean_markdown_formatting(self, content):
        """Remove any markdown formatting from content"""
        if not content:
            return content
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip markdown code blocks and markers
            if line.strip().startswith('```') or line.strip() == '```':
                continue
            # Skip empty lines that might be markdown artifacts
            if line.strip():
                cleaned_lines.append(line.rstrip())
        
        return '\n'.join(cleaned_lines)
    
    def validate_quote_consistency(self, feature_content, steps_content):
        """Validate that quotes in feature and step definitions match and decorators use double quotes"""
        import re
        
        issues = []
        
        # Extract step text from feature file
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
        
        # Extract step decorators from steps file
        step_decorators = re.findall(r'@(given|when|then)\(([\'"])(.+?)([\'"])\)', steps_content)
        
        # Create mappings
        feature_step_texts = {step[1].strip() for step in feature_steps}
        step_def_texts = {step[2].strip() for step in step_decorators}
        
        # Check for quote type in decorators
        for decorator in step_decorators:
            quote_type = decorator[1]
            step_text = decorator[2].strip()
            if quote_type != '"':
                issues.append(f"Invalid quote type in step definition: '@{decorator[0]}({quote_type}{step_text}{quote_type})' - must use double quotes")
        
        # Check for text mismatches
        for feature_text in feature_step_texts:
            if feature_text not in step_def_texts:
                similar_found = False
                for step_text in step_def_texts:
                    if self.normalize_quotes(feature_text) == self.normalize_quotes(step_text):
                        issues.append(f"Quote mismatch: Feature has '{feature_text}' but step def has '{step_text}'")
                        similar_found = True
                        break
                if not similar_found:
                    issues.append(f"Missing step definition for: '{feature_text}'")
    
        return issues
    
    def normalize_quotes(self, text):
        """Normalize quotes for comparison"""
        return text.replace('"', "'").replace(''', "'").replace(''', "'")
    
    def fix_quote_inconsistencies(self, feature_content, steps_content):
        """Fix quote inconsistencies by ensuring step definitions match feature file exactly with double quotes for decorators"""
        import re
        
        # Extract step text from feature file
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
        
        # Create mapping of normalized text to exact feature text
        feature_mapping = {}
        for step in feature_steps:
            normalized = self.normalize_quotes(step[1].strip())
            exact_text = step[1].strip()
            feature_mapping[normalized] = exact_text
            print(f"🔧 Feature step mapping: '{exact_text}' -> normalized: '{normalized}'")
            
        # Replace step decorators in steps content
        def replace_decorator(match):
            decorator_type = match.group(1)
            current_text = match.group(2)
            normalized_current = self.normalize_quotes(current_text)
            
            if normalized_current in feature_mapping:
                correct_text = feature_mapping[normalized_current]
                # Always use double quotes for decorator, escape internal double quotes
                escaped_text = correct_text.replace('"', '\\"')
                fixed_decorator = f'@{decorator_type}("{escaped_text}")'
                print(f"🔧 Fixed: @{decorator_type}('{current_text}') -> {fixed_decorator}")
                return fixed_decorator
            else:
                print(f"⚠️  No match found for: '{current_text}' (normalized: '{normalized_current}')")
            
            return match.group(0)  # No change if no match found
        
        # Apply replacements
        fixed_content = re.sub(r'@(given|when|then)\([\'"](.+?)[\'"]\)', replace_decorator, steps_content)
        
        return fixed_content
    
    def post_process_generated_files(self):
        """Auto post-process generated files for better reliability"""
        print(f"\n🔧 Post-processing generated files...")
        logging.info("Starting post-processing")
        
        # Apply natural navigation optimization
        self.optimize_natural_navigation()
        
        # Validate Python syntax for generated files
        steps_file = self.base_folder / 'features' / 'steps' / f'{self.feature_label}_steps.py'
        test_file = self.base_folder / f"test_{self.feature_label}.py"
        
        syntax_valid = True
        for file in [steps_file, test_file]:
            if file.exists():
                if not self.validate_python_file(file):
                    syntax_valid = False
        
        if syntax_valid:
            print(f"✅ Post-processing completed! All files validated")
            logging.info("Post-processing completed successfully")
        else:
            print(f"⚠️  Post-processing completed with syntax warnings")
            logging.warning("Post-processing completed with syntax issues")
    
    def optimize_natural_navigation(self):
        """Optimize navigation flow by detecting and removing unnecessary manual navigation steps"""
        print(f"🚀 Optimizing natural navigation flow...")
        
        feature_file = self.base_folder / 'features' / self.feature_label / f'{self.feature_label}.feature'
        steps_file = self.base_folder / 'features' / 'steps' / f'{self.feature_label}_steps.py'
        
        if not feature_file.exists() or not steps_file.exists():
            return
            
        # Read current files
        with open(feature_file, 'r', encoding='utf-8') as f:
            feature_content = f.read()
            
        with open(steps_file, 'r', encoding='utf-8') as f:
            steps_content = f.read()
        
        # Detect post-authentication navigation patterns
        post_auth_patterns = [
            (r"(When.*[Cc]lick.*['\"]LOGIN['\"].*)\n\s*When.*[Nn]avigate.*to.*['\"]https?://[^'\"]+['\"]", r"\1"),
            (r"(When.*[Cc]lick.*['\"]SUBMIT['\"].*)\n\s*When.*[Nn]avigate.*to.*['\"]https?://[^'\"]+['\"]", r"\1"),
            (r"(When.*[Cc]lick.*['\"]Sign.*[Ii]n['\"].*)\n\s*When.*[Nn]avigate.*to.*['\"]https?://[^'\"]+['\"]", r"\1"),
            (r"(When.*[Cc]lick.*['\"]Log.*[Ii]n['\"].*)\n\s*When.*[Nn]avigate.*to.*['\"]https?://[^'\"]+['\"]", r"\1"),
        ]
        
        # Remove unnecessary navigation steps from feature file
        optimized_feature = feature_content
        navigation_removed = False
        
        for pattern, replacement in post_auth_patterns:
            if re.search(pattern, optimized_feature, re.MULTILINE):
                optimized_feature = re.sub(pattern, replacement, optimized_feature, flags=re.MULTILINE)
                navigation_removed = True
                
        # Enhance login/submit timeouts in step definitions
        login_timeout_patterns = [
            (r"(@when\(['\"].*[Cc]lick.*['\"]LOGIN['\"].*['\"].*\).*def.*\):.*page\.get_by_role.*\.click\(\))(.*page\.wait_for_timeout\(\d+\))?", 
             r"\1\n    # Wait for login to complete and natural redirect\n    page.wait_for_timeout(5000)\n    page.wait_for_load_state('networkidle')"),
            (r"(@when\(['\"].*[Cc]lick.*['\"]SUBMIT['\"].*['\"].*\).*def.*\):.*page\.get_by_role.*\.click\(\))(.*page\.wait_for_timeout\(\d+\))?", 
             r"\1\n    # Wait for submit to complete and natural redirect\n    page.wait_for_timeout(5000)\n    page.wait_for_load_state('networkidle')"),
        ]
        
        optimized_steps = steps_content
        for pattern, replacement in login_timeout_patterns:
            optimized_steps = re.sub(pattern, replacement, optimized_steps, flags=re.DOTALL)
        
        # Remove corresponding navigation step definitions
        nav_step_patterns = [
            r"@when\(['\"]User navigates to ['\"]https?://[^'\"]+['\"]['\"].*?\).*?def.*?:.*?page\.goto\(.*?\).*?(?=@|\Z)",
            r"@when\(['\"].*[Nn]avigate.*to.*['\"]https?://[^'\"]+['\"].*?\).*?def.*?:.*?page\.goto\(.*?\).*?(?=@|\Z)",
        ]
        
        for pattern in nav_step_patterns:
            if re.search(pattern, optimized_steps, re.DOTALL):
                optimized_steps = re.sub(pattern, "", optimized_steps, flags=re.DOTALL)
                navigation_removed = True
        
        # Write optimized files if changes were made
        if navigation_removed:
            with open(feature_file, 'w', encoding='utf-8') as f:
                f.write(optimized_feature)
                
            with open(steps_file, 'w', encoding='utf-8') as f:
                f.write(optimized_steps)
                
            print(f"✅ Natural navigation optimization applied - removed manual navigation steps")
        else:
            print(f"ℹ️  No manual navigation patterns detected - keeping original flow")    
    def create_test_file(self):
        """Create pytest test file with robust path handling to avoid IndexError"""
        test_content = f'''import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

# Set working directory to ensure proper path resolution
os.chdir(Path(__file__).parent)

# Import step definitions - CRITICAL for test execution
from features.steps.{self.feature_label}_steps import *

# Load scenarios for {self.feature_label} feature - using relative path from current working dir
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
    context.grant_permissions([])
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
            f.write(test_content)
        
        print(f"✅ Test file: {test_file}")
    
    def create_pytest_config(self):
        """Create pytest.ini configuration file to avoid path issues"""
        pytest_config = f'''[tool:pytest]
bdd_features_base_dir = features
markers =
    {self.feature_label}: marks tests as {self.feature_label} feature tests
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
'''
        
        pytest_file = self.base_folder / "pytest.ini"
        with open(pytest_file, 'w', encoding='utf-8') as f:
            f.write(pytest_config)
        
        print(f"✅ Pytest config: {pytest_file}")
    
    def run_workflow(self):
        """Run the complete workflow"""
        try:
            # Setup
            self.setup_project_structure()
            
            # Record
            recorded_file = self.record_script()
            if not recorded_file:
                return False
            
            # Convert
            success = self.convert_to_cucumber(recorded_file)
            if not success:
                return False
            
            # Final instructions
            print("\n" + "=" * 60)
            print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📁 Project folder: {self.base_folder}")
            print(f"🏷️  Feature label: {self.feature_label}")
            print("\n📋 Next steps:")
            print(f"1. cd \"{self.base_folder}\"")
            print("\n🚀 Option 1 - Easy Shell Runner (RECOMMENDED):")
            print(f"   ./run_tests.sh")
            print("\n🚀 Option 2 - Manual with Virtual Environment:")
            print("   source ../venv/bin/activate")
            print(f"   python run_tests.py {self.feature_label}")
            print("\n🚀 Option 3 - Direct Path:")
            print(f"   ../venv/bin/python run_tests.py {self.feature_label}")
            print(f"\n📊 Check results: reports/report_{self.feature_label}.html")
            print("\n🔥 Happy Testing!")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Workflow dibatalkan oleh user.")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False

    def validate_python_file(self, file_path):
        """Validate Python file syntax"""
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"✅ Python file {file_path} is syntactically correct")
            logging.info(f"Python syntax validation passed for {file_path}")
            return True
        except py_compile.PyCompileError as e:
            print(f"❌ Syntax error in {file_path}: {e}")
            logging.error(f"Python syntax validation failed for {file_path}: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Could not validate {file_path}: {e}")
            logging.warning(f"Could not validate {file_path}: {e}")
            return False

    def enhanced_quote_validation(self, feature_content, steps_content):
        """Enhanced validation specifically for quote patterns and common typos"""
        import re
        
        issues = []
        
        # Check for common typo patterns in step definitions
        typo_patterns = [
            (r"@then\(['\"][^'\"]*['\"]['\"]", "Malformed decorator - missing space or quote"),
            (r"@(given|when|then)\(['\"][^'\"]*should be visible[^'\"]*['\"]", "Check 'should be visible' pattern"),
            (r"@(given|when|then)\(['\"][^'\"]*Private[^'\"]*['\"]", "Check 'Private' text preservation"),
        ]
        
        for pattern, description in typo_patterns:
            if re.search(pattern, steps_content, re.IGNORECASE):
                issues.append(f"Potential issue detected: {description}")
        
        # Validate that all feature steps have exact matches in step definitions
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
        step_decorators = re.findall(r'@(given|when|then)\("([^"]+)"\)', steps_content)
        
        feature_texts = {step[1].strip() for step in feature_steps}
        step_def_texts = {step[1].strip() for step in step_decorators}
        
        missing_steps = feature_texts - step_def_texts
        if missing_steps:
            for missing in missing_steps:
                issues.append(f"Missing exact step definition for: '{missing}'")
        
        return issues
def main():
    generator = CucumberGenerator()
    generator.run_workflow()

if __name__ == "__main__":
    main()
