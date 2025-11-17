#!/usr/bin/env python3
"""
Test Runner for l_advance_table_plot_delete
"""
import subprocess
import sys
from pathlib import Path

def run_test():
    project_dir = Path(__file__).parent
    test_file = project_dir / "tests" / "l_advance_table_plot_delete.py"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False

    print(f"🚀 Running test: l_advance_table_plot_delete")
    print(f"📁 Location: {test_file}")
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
        print("\n✅ Test PASSED!")
    else:
        print("\n❌ Test FAILED!")

    print(f"📊 Report: {project_dir / 'reports' / 'report.html'}")
    return result.returncode == 0

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
