#!/usr/bin/env python3
"""
E2E Test Runner
Run tests by priority, category, or all tests
Supports P0 (smoke), P1 (regression), P2 (exploratory)
"""

import subprocess
import sys
import argparse
from pathlib import Path


class TestRunner:
    """Run E2E tests with priority-based filtering"""

    PRIORITIES = {
        'p0': {
            'name': 'Smoke Test',
            'folder': 'p0-smoke_test',
            'marker': 'smoke',
            'description': 'Critical tests that must pass'
        },
        'p1': {
            'name': 'Regression',
            'folder': 'p1-regression',
            'marker': 'regression',
            'description': 'Important features, run on every build'
        },
        'p2': {
            'name': 'Exploratory',
            'folder': 'p2-exploratory',
            'marker': 'exploratory',
            'description': 'Edge cases and UI validation'
        }
    }

    def __init__(self, base_folder='e2e'):
        self.base_folder = Path(base_folder)
        if not self.base_folder.exists():
            raise FileNotFoundError(f"E2E folder not found: {base_folder}")

    def run_all(self, verbose=True):
        """Run all tests across all priorities"""
        print("🚀 Running ALL E2E Tests")
        print("=" * 70)

        return self._run_pytest(
            test_path=str(self.base_folder),
            verbose=verbose,
            description="All Tests"
        )

    def run_priority(self, priority, verbose=True):
        """Run tests for specific priority"""
        if priority not in self.PRIORITIES:
            print(f"❌ Invalid priority: {priority}")
            print(f"   Valid options: {', '.join(self.PRIORITIES.keys())}")
            return False

        info = self.PRIORITIES[priority]
        priority_folder = self.base_folder / info['folder']

        if not priority_folder.exists():
            print(f"⚠️  No tests found for {priority.upper()}")
            print(f"   Folder doesn't exist: {priority_folder}")
            return False

        print(f"🚀 Running {priority.upper()} - {info['name']}")
        print(f"📝 {info['description']}")
        print("=" * 70)

        return self._run_pytest(
            test_path=str(priority_folder),
            verbose=verbose,
            description=f"{priority.upper()} Tests"
        )

    def run_multiple_priorities(self, priorities, verbose=True):
        """Run tests for multiple priorities"""
        print(f"🚀 Running Multiple Priorities: {', '.join([p.upper() for p in priorities])}")
        print("=" * 70)

        all_passed = True
        for priority in priorities:
            print(f"\n{'='*70}")
            print(f"Running {priority.upper()}...")
            print(f"{'='*70}\n")

            passed = self.run_priority(priority, verbose=verbose)
            if not passed:
                all_passed = False

        return all_passed

    def run_by_marker(self, marker, verbose=True):
        """Run tests by pytest marker"""
        print(f"🚀 Running tests with marker: @pytest.mark.{marker}")
        print("=" * 70)

        return self._run_pytest(
            test_path=str(self.base_folder),
            marker=marker,
            verbose=verbose,
            description=f"Marker: {marker}"
        )

    def run_specific_test(self, test_path, verbose=True):
        """Run a specific test file"""
        test_file = Path(test_path)

        if not test_file.exists():
            print(f"❌ Test file not found: {test_path}")
            return False

        print(f"🚀 Running specific test: {test_file.name}")
        print("=" * 70)

        return self._run_pytest(
            test_path=str(test_file),
            verbose=verbose,
            description=f"Test: {test_file.name}"
        )

    def list_tests(self):
        """List all available tests by priority"""
        print("📋 Available E2E Tests")
        print("=" * 70)

        for priority, info in self.PRIORITIES.items():
            priority_folder = self.base_folder / info['folder']

            if not priority_folder.exists():
                continue

            tests_folder = priority_folder / "tests"
            if not tests_folder.exists():
                continue

            test_files = list(tests_folder.glob("*_test.py"))

            print(f"\n{priority.upper()} - {info['name']}")
            print(f"   {info['description']}")
            print(f"   Folder: {info['folder']}/")

            if test_files:
                for test in sorted(test_files):
                    print(f"   • {test.name}")
            else:
                print("   (no tests yet)")

        print()

    def _run_pytest(self, test_path, marker=None, verbose=True, description=""):
        """Execute pytest with given parameters"""
        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
        ]

        if verbose:
            cmd.append("-v")

        if marker:
            cmd.extend(["-m", marker])

        # Always generate HTML report
        cmd.extend([
            "--html=e2e/reports/report.html",
            "--self-contained-html"
        ])

        # Ensure reports folder exists
        reports_folder = self.base_folder / "reports"
        reports_folder.mkdir(parents=True, exist_ok=True)

        print(f"📍 Command: {' '.join(cmd)}\n")

        result = subprocess.run(cmd)

        print("\n" + "=" * 70)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
        else:
            print(f"❌ {description} - FAILED")

        print(f"📊 Report: {reports_folder / 'report.html'}")
        print("=" * 70)

        return result.returncode == 0


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Run E2E tests by priority or category",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python run_tests.py --all

  # Run by priority
  python run_tests.py --priority p0
  python run_tests.py --priority p1,p2

  # Run by marker
  python run_tests.py --marker smoke

  # Run specific test
  python run_tests.py --test e2e/p0-smoke_test/tests/login_test.py

  # List all tests
  python run_tests.py --list

Priority Levels:
  p0 - Smoke Test: Critical features that must pass
  p1 - Regression: Important features, run on every build
  p2 - Exploratory: Edge cases and UI validation
        """
    )

    parser.add_argument('--all', action='store_true',
                        help='Run all tests')
    parser.add_argument('--priority', type=str,
                        help='Run tests by priority (p0, p1, p2) - can specify multiple: p0,p1')
    parser.add_argument('--marker', type=str,
                        help='Run tests by pytest marker (smoke, regression, exploratory)')
    parser.add_argument('--test', type=str,
                        help='Run specific test file')
    parser.add_argument('--list', action='store_true',
                        help='List all available tests')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Quiet mode (less verbose)')
    parser.add_argument('--base-folder', type=str, default='e2e',
                        help='Base E2E folder (default: e2e)')

    args = parser.parse_args()

    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    try:
        runner = TestRunner(base_folder=args.base_folder)

        verbose = not args.quiet

        # List tests
        if args.list:
            runner.list_tests()
            sys.exit(0)

        # Run all tests
        if args.all:
            success = runner.run_all(verbose=verbose)
            sys.exit(0 if success else 1)

        # Run by priority
        if args.priority:
            priorities = [p.strip() for p in args.priority.split(',')]
            if len(priorities) == 1:
                success = runner.run_priority(priorities[0], verbose=verbose)
            else:
                success = runner.run_multiple_priorities(priorities, verbose=verbose)
            sys.exit(0 if success else 1)

        # Run by marker
        if args.marker:
            success = runner.run_by_marker(args.marker, verbose=verbose)
            sys.exit(0 if success else 1)

        # Run specific test
        if args.test:
            success = runner.run_specific_test(args.test, verbose=verbose)
            sys.exit(0 if success else 1)

        # If we get here, no valid action was specified
        parser.print_help()

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
