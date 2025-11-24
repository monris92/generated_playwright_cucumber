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
        """Main interactive workflow"""
        print("=" * 70)
        print("🧪 INTERACTIVE E2E TEST RUNNER")
        print("=" * 70)
        print()

        # Step 1: Choose priority or all
        priority = self.choose_priority()

        if priority == 'all':
            self.run_all_tests()
            return

        # Step 2: Get available scenarios for the priority
        scenarios = self.get_scenarios(priority)

        if not scenarios:
            print(f"\n⚠️  No test scenarios found for {priority.upper()}")
            print(f"   Create tests in: {self.base_folder / self.PRIORITIES[priority]['folder']}")
            return

        # Step 3: Choose scenario or all scenarios in priority
        scenario = self.choose_scenario(priority, scenarios)

        if scenario == 'all':
            self.run_priority_tests(priority)
        else:
            self.run_specific_test(priority, scenario)

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

    def get_scenarios(self, priority: str) -> List[Dict]:
        """Get list of test scenarios for a priority"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        scenarios = []

        if not priority_folder.exists():
            return scenarios

        # Look for scenario folders (each scenario has its own folder)
        for scenario_folder in sorted(priority_folder.iterdir()):
            if not scenario_folder.is_dir():
                continue

            # Check if it has a tests folder with test files
            tests_folder = scenario_folder / "tests"
            if tests_folder.exists():
                test_files = list(tests_folder.glob("*_test.py"))
                if test_files:
                    scenarios.append({
                        'name': scenario_folder.name,
                        'folder': scenario_folder,
                        'test_files': test_files,
                        'test_count': len(test_files)
                    })

        return scenarios

    def choose_scenario(self, priority: str, scenarios: List[Dict]) -> str:
        """Let user choose a specific scenario"""
        print(f"\n📋 Available Scenarios in {priority.upper()}:")
        print()

        for idx, scenario in enumerate(scenarios, 1):
            print(f"   {idx}. {scenario['name']}")
            print(f"      Tests: {scenario['test_count']} file(s)")
            for test_file in scenario['test_files']:
                print(f"        • {test_file.name}")
            print()

        print(f"   0. Run ALL scenarios in {priority.upper()}")
        print()

        while True:
            try:
                choice = input(f"Choose scenario [0-{len(scenarios)}] (default: 0): ").strip()
                if not choice:
                    choice = '0'

                choice_num = int(choice)

                if choice_num == 0:
                    print(f"✅ Selected: Run ALL scenarios in {priority.upper()}")
                    return 'all'
                elif 1 <= choice_num <= len(scenarios):
                    selected = scenarios[choice_num - 1]
                    print(f"✅ Selected: {selected['name']}")
                    return selected['name']
                else:
                    print(f"❌ Invalid choice. Please choose 0-{len(scenarios)}")
            except ValueError:
                print(f"❌ Invalid input. Please enter a number 0-{len(scenarios)}")

    def count_tests(self, priority_folder: Path) -> int:
        """Count total test files in a priority folder"""
        if not priority_folder.exists():
            return 0

        test_files = list(priority_folder.glob("*/tests/*_test.py"))
        return len(test_files)

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

    def run_specific_test(self, priority: str, scenario_name: str):
        """Run a specific test scenario"""
        priority_folder = self.base_folder / self.PRIORITIES[priority]['folder']
        scenario_folder = priority_folder / scenario_name
        tests_folder = scenario_folder / "tests"

        print("\n" + "=" * 70)
        print(f"🚀 Running Test: {scenario_name}")
        print(f"📊 Priority: {self.PRIORITIES[priority]['name']}")
        print("=" * 70)
        print()

        self._execute_pytest(
            test_path=str(tests_folder),
            description=f"{priority.upper()}/{scenario_name}"
        )

    def _execute_pytest(self, test_path: str, description: str):
        """Execute pytest with given parameters"""
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
