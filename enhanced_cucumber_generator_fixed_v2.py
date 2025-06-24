import subprocess
import os
import requests
import json
import sys
import re
from datetime import datetime
from pathlib import Path

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
        
        print(f"\n📁 Project structure created in: {self.base_folder}")
        
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
    
    # Run pytest with HTML report
    cmd = [
        "pytest", 
        str(test_file),
        "--html", str(reports_dir / f"report_{{feature_label}}.html"),
        "--self-contained-html",
        "-v", "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Tests passed! Report: {{reports_dir / f'report_{{feature_label}}.html'}}")
            return True
        else:
            print(f"❌ Tests failed! Check report: {{reports_dir / f'report_{{feature_label}}.html'}}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {{e}}")
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
        
        try:
            subprocess.run([
                "playwright", "codegen", self.website_url, 
                "--output", str(record_output)
            ], check=True, text=True)
            
            print(f"✅ Script recorded: {record_output}")
            return record_output
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during recording: {e}")
            return None

    def convert_to_cucumber(self, recorded_file):
        """Convert recorded script to Cucumber format"""
        print(f"\n🤖 Converting to Cucumber format using Mistral AI...")
        
        try:
            # Read recorded script
            with open(recorded_file, "r", encoding='utf-8') as file:
                script_content = file.read()
                
            # Enhanced prompt with strict text and quote consistency requirements
            prompt_content = f"""Convert the following Playwright Python script into a Cucumber feature file (Gherkin syntax) and corresponding step definitions in Python. 

ULTRA-CRITICAL REQUIREMENTS - FOLLOW EXACTLY:

1. TEXT PRESERVATION (ABSOLUTELY CRITICAL):
   - PRESERVE EXACT TEXT: If script shows "websites", feature MUST use "websites" (not "website")
   - NO WORD CHANGES: Never change singular/plural, never modify any words
   - CHARACTER-BY-CHARACTER MATCHING: Preserve exactly as recorded

2. QUOTE CONSISTENCY (MANDATORY):
   - Feature file: Use single quotes for text content
   - Step definitions: Use DOUBLE quotes for decorator, preserve inner quotes exactly
   - Example: Feature has "When User enters 'auck' in the search box"
   - Step definition MUST be: @when("User enters 'auck' in the search box")
   - NEVER change inner quote patterns

3. ROBUST TIMING & ERROR HANDLING:
   - Add page.wait_for_load_state('networkidle') after every page.goto()
   - Add page.wait_for_load_state('networkidle') after button clicks
   - Add page.wait_for_timeout(1000-3000ms) after button clicks
   - Wrap critical assertions in try-catch blocks with retries
   - For heading visibility, add wait_for_timeout(3000) before retry

4. NATURAL NAVIGATION STRATEGY (CRITICAL):
   - DETECT POST-ACTION NAVIGATION: If script shows page.goto() immediately after login/submit/click, this suggests natural redirect
   - AVOID MANUAL NAVIGATION: Do NOT generate separate navigation steps after authentication actions
   - TRUST APPLICATION FLOW: Let the application handle its own redirects after login/submit
   - ENHANCED POST-ACTION TIMEOUTS: Use longer timeouts (5000ms) after login/submit buttons
   - EXAMPLE: Instead of "When User clicks LOGIN" + "When User navigates to X", use "When User clicks LOGIN" + longer timeout + "Then X should be visible"

5. CODE STRUCTURE:
   - Import EXACTLY: from playwright.sync_api import expect, from pytest_bdd import given, when, then, import pytest, import re
   - DO NOT include scenarios() call in step definitions
   - NO markdown code blocks or formatting
   - Each function should have proper indentation
   - Use expect(page).to_have_url() for URL assertions, NOT expect(page.url)

6. BDD BEST PRACTICES:
   - Feature name: descriptive and include label "{self.feature_label}"
   - Include @{self.feature_label} tag
   - Use Given/When/Then structure
   - Each step should be atomic and testable

Playwright Script:
{script_content}

EXAMPLE OUTPUT FORMAT:

Step definitions should look EXACTLY like this (NO MARKDOWN):
from playwright.sync_api import expect
from pytest_bdd import given, when, then
import pytest
import re

@given("User navigates to the website")
def navigate_to_website(page):
    page.goto('https://example.com')
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

@then("User should navigate to 'https://example.com/page'")
def verify_navigation(page):
    try:
        expect(page).to_have_url(re.compile(r'.*example.com/page.*'))
    except:
        page.wait_for_timeout(2000)
        expect(page).to_have_url(re.compile(r'.*example.com/page.*'))

Return your response as JSON with this exact structure:
{{
    "feature": "Complete Gherkin feature file with @{self.feature_label} tag",
    "steps": "Complete Python step definitions with DOUBLE quotes for decorators - NO MARKDOWN"
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
            
            # Clean up the result to remove any remaining markdown
            feature_content = self.clean_markdown_formatting(result["feature"])
            steps_content = self.clean_markdown_formatting(result["steps"])
            
            # Validate quote consistency between feature and steps
            validation_issues = self.validate_quote_consistency(feature_content, steps_content)
            if validation_issues:
                print("⚠️  Quote consistency issues found:")
                for issue in validation_issues:
                    print(f"   • {issue}")
                print("🔧 Auto-fixing quote inconsistencies...")
                steps_content = self.fix_quote_inconsistencies(feature_content, steps_content)
            
            # Save files
            feature_output = self.base_folder / "features" / self.feature_label / f"{self.feature_label}.feature"
            steps_output = self.base_folder / "features" / "steps" / f"{self.feature_label}_steps.py"
            
            with open(feature_output, "w", encoding='utf-8') as f:
                f.write(feature_content)
            print(f"✅ Feature file: {feature_output}")
            
            with open(steps_output, "w", encoding='utf-8') as f:
                f.write(steps_content)
            print(f"✅ Steps file: {steps_output}")
            
            # Auto post-process generated files
            self.post_process_generated_files()
            
            # Create test file with robust path handling and pytest config
            self.create_test_file()
            self.create_pytest_config()
            
            return True
            
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
    
    def clean_markdown_formatting(self, content):
        """Remove any markdown formatting from content"""
        if not content:
            return content
            
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove markdown code blocks
            if line.strip().startswith('```') and (line.strip().endswith('```') or 'python' in line.lower() or 'gherkin' in line.lower()):
                continue
            # Remove standalone markdown markers
            if line.strip() == '```':
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def validate_quote_consistency(self, feature_content, steps_content):
        """Validate that quotes in feature and step definitions match"""
        import re
        
        issues = []
        
        # Extract step text from feature file
        feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
        
        # Extract step decorators from steps file
        step_decorators = re.findall(r'@(given|when|then)\([\'"](.+?)[\'"]\)', steps_content)
        
        # Create mappings
        feature_step_texts = {step[1].strip() for step in feature_steps}
        step_def_texts = {step[1].strip() for step in step_decorators}
        
        # Check for mismatches
        for feature_text in feature_step_texts:
            if feature_text not in step_def_texts:
                # Look for similar texts with different quotes
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
        """Fix quote inconsistencies by making step definitions match feature file exactly"""
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
                # Always use double quotes for decorator, preserve inner quotes exactly
                fixed_decorator = f'@{decorator_type}("{correct_text}")'
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
        
        # Apply natural navigation optimization
        self.optimize_natural_navigation()
        
        # Built-in validation and fixes already handled by:
        # 1. validate_quote_consistency()
        # 2. fix_quote_inconsistencies() 
        # 3. clean_markdown_formatting()
        # 4. optimize_natural_navigation() - NEW
        # External post-processor no longer needed
        
        print(f"✅ Post-processing completed! (Built-in fixes applied)")
    
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
        browser = p.chromium.launch(headless=False)
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
            print(f"2. python run_tests.py {self.feature_label}")
            print(f"3. Check reports/report_{self.feature_label}.html")
            print("\n🔥 Happy Testing!")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Workflow dibatalkan oleh user.")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False

def main():
    generator = CucumberGenerator()
    generator.run_workflow()

if __name__ == "__main__":
    main()
