#!/usr/bin/env python3
"""
Interactive E2E Test Runner
Provides a menu-driven interface to run tests by priority and scenario
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional


class InteractiveTestRunner:
    """Interactive test runner with menu-driven interface"""

    PRIORITIES = {
        'p0': {
            'name': 'P0 - Smoke Test',
            'folder': 'p0-smoke_test',
            'description': 'Critical features that must pass before release'
        },
        'p1': {
            'name': 'P1 - Regression',
            'folder': 'p1-regression',
            'description': 'Important features, run on every build'
        },
        'p2': {
            'name': 'P2 - Exploratory',
            'folder': 'p2-exploratory',
            'description': 'Edge cases, UI validation, nice-to-have tests'
        }
    }

    def __init__(self, base_folder='e2e'):
        self.base_folder = Path(base_folder)
        if not self.base_folder.exists():
            raise FileNotFoundError(f"E2E folder not found: {base_folder}")

    def run(self):
        """Main interactive workflow supporting both category and flat test structures"""
        print("=" * 70)
        print("🧪 INTERACTIVE E2E TEST RUNNER")
        print("=" * 70)
        print()

        # Step 1: Choose priority or all
        priority = self.choose_priority()

        if priority == 'all':
            self.run_all_tests()
            return

        # Step 2: Get categories and flat tests for the priority
        categories, flat_tests = self.get_categories_and_tests(priority)

        if not categories and not flat_tests:
            print(f"\n⚠️  No test scenarios found for {priority.upper()}")
            print(f"   Create tests in: {self.base_folder / self.PRIORITIES[priority]['folder']}")
            return

        # Step 3: Choose category, flat test, or all
        selection = self.choose_category_or_test(priority, categories, flat_tests)

        if selection['type'] == 'all':
            self.run_priority_tests(priority)
        elif selection['type'] == 'category':
            # Step 4: Choose specific test within category or all tests in category
            category_name = selection['name']
            test_choice = self.choose_test_in_category(priority, category_name)
            
            if test_choice == 'all':
                self.run_category_tests(priority, category_name)
            else:
                self.run_specific_test(priority, test_choice, category_name)
        else:  # flat test
            self.run_specific_test(priority, selection['name'])

    def choose_priority(self) -> str:
        """Let user choose test priority"""
        print("📊 Select Test Priority:")
        print()

        # List priorities with test counts
        for key, info in self.PRIORITIES.items():
            priority_folder = self.base_folder / info['folder']
            test_count = self.count_tests(priority_folder)
            print(f"   {key.upper()}: {info['name']}")
            print(f"        {info['description']}")
            print(f"        Tests available: {test_count}")
            print()

        print(f"   ALL: Run all tests across all priorities")
        print()

        while True:
            choice = input("Choose priority [p0/p1/p2/all] (default: p0): ").strip().lower()
            if not choice:
                choice = 'p0'

            if choice in ['p0', 'p1', 'p2', 'all']:
                if choice != 'all':
                    print(f"✅ Selected: {self.PRIORITIES[choice]['name']}")
                else:
                    print(f"✅ Selected: Run ALL tests")
                return choice

            print("❌ Invalid choice. Please choose p0, p1, p2, or all")

    def get_categories_and_tests(self, priority: str) -> tuple:
        """
        Get categories and flat tests separately.
        
        Returns:
            tuple: (categories, flat_tests)
            - categories: list of dicts with category info
            - flat_tests: list of dicts with flat test info
        """
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        categories = []
        flat_tests = []

        if not priority_folder.exists():
            return categories, flat_tests

        for item in sorted(priority_folder.iterdir()):
            if not item.is_dir() or item.name.startswith('.'):
                continue

            # First check if it has subdirectories (category structure)
            has_test_subdirs = False
            category_test_count = 0
            for subitem in sorted(item.iterdir()):
                if not subitem.is_dir() or subitem.name.startswith('.'):
                    continue
                # Check for test files in tests/ subfolder
                if (subitem / "tests").exists():
                    sub_test_files = list((subitem / "tests").glob("*_test.py"))
                    if sub_test_files:
                        has_test_subdirs = True
                        category_test_count += len(sub_test_files)
                # Also check for subcategory structure (public/login)
                for sub_subitem in subitem.iterdir():
                    if sub_subitem.is_dir() and not sub_subitem.name.startswith('.'):
                        if (sub_subitem / "tests").exists():
                            subsub_test_files = list((sub_subitem / "tests").glob("*_test.py"))
                            if subsub_test_files:
                                has_test_subdirs = True
                                category_test_count += len(subsub_test_files)

            if has_test_subdirs:
                # It's a category folder
                categories.append({
                    'name': item.name,
                    'folder': item,
                    'test_count': category_test_count
                })
            else:
                # Check if it's a direct test folder with tests/ subfolder
                test_files = list((item / "tests").glob("*_test.py")) if (item / "tests").exists() else []
                if test_files:
                    flat_tests.append({
                        'name': item.name,
                        'folder': item,
                        'test_files': test_files,
                        'test_count': len(test_files)
                    })

        return categories, flat_tests

    def get_tests_in_category(self, priority: str, category_name: str) -> List[Dict]:
        """Get all test folders within a category (supports subcategories like public/login)"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        category_folder = priority_folder / category_name
        tests = []

        if not category_folder.exists():
            return tests

        for item in sorted(category_folder.iterdir()):
            if not item.is_dir() or item.name.startswith('.'):
                continue

            # Check if this is a subcategory (e.g., public, login)
            # Subcategories contain test folders, not test files directly
            has_subdirs = any(sub.is_dir() and not sub.name.startswith('.') for sub in item.iterdir())
            
            if has_subdirs:
                # This is a subcategory, scan its contents
                for test_folder in sorted(item.iterdir()):
                    if not test_folder.is_dir() or test_folder.name.startswith('.'):
                        continue
                    
                    # Look for test files in tests/ subfolder
                    test_files = list((test_folder / "tests").glob("*_test.py")) if (test_folder / "tests").exists() else []
                    if test_files:
                        tests.append({
                            'name': f"{item.name}/{test_folder.name}",
                            'folder': test_folder,
                            'test_files': test_files,
                            'test_count': len(test_files)
                        })
            else:
                # Direct test folder (no subcategory)
                # Look for test files in tests/ subfolder
                test_files = list((item / "tests").glob("*_test.py")) if (item / "tests").exists() else []
                if test_files:
                    tests.append({
                        'name': item.name,
                        'folder': item,
                        'test_files': test_files,
                        'test_count': len(test_files)
                    })

        return tests

    def choose_category_or_test(self, priority: str, categories: List[Dict], flat_tests: List[Dict]) -> Dict:
        """Let user choose a category, flat test, or all"""
        print(f"\n📋 Available in {priority.upper()}:")
        print()

        options = []
        idx = 1

        # List categories first
        if categories:
            print("  📂 Categories:")
            for category in categories:
                print(f"   {idx}. {category['name']} ({category['test_count']} tests)")
                options.append({
                    'type': 'category',
                    'name': category['name'],
                    'data': category
                })
                idx += 1
            print()

        # Then list flat tests
        if flat_tests:
            print("  📝 Tests:")
            for test in flat_tests:
                print(f"   {idx}. {test['name']}")
                options.append({
                    'type': 'test',
                    'name': test['name'],
                    'data': test
                })
                idx += 1
            print()

        print(f"   0. Run ALL tests in {priority.upper()}")
        print()

        while True:
            try:
                choice = input(f"Choose [0-{len(options)}] (default: 0): ").strip()
                if not choice:
                    choice = '0'

                choice_num = int(choice)

                if choice_num == 0:
                    print(f"✅ Selected: Run ALL in {priority.upper()}")
                    return {'type': 'all'}
                elif 1 <= choice_num <= len(options):
                    selected = options[choice_num - 1]
                    print(f"✅ Selected: {selected['name']}")
                    return selected
                else:
                    print(f"❌ Invalid choice. Please choose 0-{len(options)}")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number 0-{len(options)}")

    def choose_test_in_category(self, priority: str, category_name: str) -> str:
        """Let user choose a specific test within a category"""
        tests = self.get_tests_in_category(priority, category_name)

        print(f"\n📋 Tests in category '{category_name}':")
        print()

        for idx, test in enumerate(tests, 1):
            print(f"   {idx}. {test['name']}")
            print(f"      Tests: {test['test_count']} file(s)")
            for test_file in test['test_files']:
                print(f"        • {test_file.name}")
            print()

        print(f"   0. Run ALL tests in '{category_name}'")
        print()

        while True:
            try:
                choice = input(f"Choose [0-{len(tests)}] (default: 0): ").strip()
                if not choice:
                    choice = '0'

                choice_num = int(choice)

                if choice_num == 0:
                    print(f"✅ Selected: Run ALL tests in '{category_name}'")
                    return 'all'
                elif 1 <= choice_num <= len(tests):
                    selected = tests[choice_num - 1]
                    print(f"✅ Selected: {selected['name']}")
                    return selected['name']
                else:
                    print(f"❌ Invalid choice. Please choose 0-{len(tests)}")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number 0-{len(tests)}")

    def count_tests(self, priority_folder: Path) -> int:
        """Count total test files in a priority folder (supports subcategory and tests/ subfolder)"""
        if not priority_folder.exists():
            return 0

        # Count with tests/ subfolder:
        # priority/test/tests/*.py
        # priority/category/test/tests/*.py
        # priority/category/subcategory/test/tests/*.py
        direct_tests = list(priority_folder.glob("*/tests/*_test.py"))
        category_tests = list(priority_folder.glob("*/*/tests/*_test.py"))
        subcategory_tests = list(priority_folder.glob("*/*/*/tests/*_test.py"))
        
        return len(direct_tests) + len(category_tests) + len(subcategory_tests)

    def run_all_tests(self):
        """Run all tests across all priorities"""
        print("\n" + "=" * 70)
        print("🚀 Running ALL E2E Tests")
        print("=" * 70)
        print()

        self._execute_pytest(
            test_path=str(self.base_folder),
            description="ALL Tests"
        )

    def run_priority_tests(self, priority: str):
        """Run all tests for a specific priority"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']

        print("\n" + "=" * 70)
        print(f"🚀 Running {self.PRIORITIES[priority]['name']}")
        print(f"📝 {self.PRIORITIES[priority]['description']}")
        print("=" * 70)
        print()

        self._execute_pytest(
            test_path=str(priority_folder),
            description=f"{priority.upper()} Tests"
        )

    def run_category_tests(self, priority: str, category_name: str):
        """Run all tests in a category"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        category_folder = priority_folder / category_name

        print("\n" + "=" * 70)
        print(f"🚀 Running Category: {category_name}")
        print(f"📊 Priority: {self.PRIORITIES[priority]['name']}")
        print("=" * 70)
        print()

        self._execute_pytest(
            test_path=str(category_folder),
            description=f"{priority.upper()}/{category_name}"
        )

    def run_specific_test(self, priority: str, test_name: str, category_name: Optional[str] = None):
        """Run a specific test (with optional category)"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        
        if category_name:
            test_folder = priority_folder / category_name / test_name
            test_path_display = f"{priority.upper()}/{category_name}/{test_name}"
        else:
            test_folder = priority_folder / test_name
            test_path_display = f"{priority.upper()}/{test_name}"
        
        # Test files are directly in test_folder (flat structure)

        print("\n" + "=" * 70)
        print(f"🚀 Running Test: {test_name}")
        if category_name:
            print(f"📂 Category: {category_name}")
        print(f"📊 Priority: {self.PRIORITIES[priority]['name']}")
        print("=" * 70)
        print()

        self._execute_pytest(
            test_path=str(test_folder),
            description=test_path_display
        )

    def _execute_pytest(self, test_path: str, description: str):
        """Execute pytest with given parameters"""
        # Ask user for browser display mode
        print("\n🖥️  Browser Display Mode:")
        print("   1. 🚀 Headless - Terminal only (faster, no browser window)")
        print("   2. 👁️  Headed - Show live browser (watch test execution)")
        print()
        
        headless = True
        try:
            mode_choice = input("Choose mode [1/2] (default: 1): ").strip()
            if mode_choice == '2':
                headless = False
                print("✅ Headed mode: Browser will be visible during test")
            else:
                print("✅ Headless mode: Running in terminal only")
        except Exception:
            headless = True
        
        print()
        
        # Ask user whether to enable screenshot-on-success (default: N)
        enable_success = False
        try:
            ans = input("Capture screenshots on success? (y/N): ").strip().lower()
            if ans == 'y':
                enable_success = True
        except Exception:
            enable_success = False

        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
            "-v",
            "--html", str(self.base_folder / "reports" / "report.html"),
            "--self-contained-html",
        ]

        # Add headless/headed flag
        # pytest-playwright uses --headed flag (no value needed for headed mode)
        # Default is headless, so only add flag if user wants headed
        if not headless:
            cmd.append("--headed")

        if enable_success:
            cmd.append("--screenshot-on-success")

        # Ensure reports folder exists
        reports_folder = self.base_folder / "reports"
        reports_folder.mkdir(parents=True, exist_ok=True)

        print(f"📍 Test Path: {test_path}")
        print(f"📍 Command: {' '.join(cmd)}")
        print()

        result = subprocess.run(cmd)

        print("\n" + "=" * 70)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
        else:
            print(f"❌ {description} - FAILED")

        print(f"📊 HTML Report: {reports_folder / 'report.html'}")
        print("=" * 70)

        return result.returncode == 0


def main():
    """Main entry point"""
    try:
        runner = InteractiveTestRunner()
        runner.run()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test runner interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
