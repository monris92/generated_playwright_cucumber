#!/usr/bin/env python3
"""
Quick validation script to ensure the generator is ready to use
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🔍 Validating Playwright-to-Cucumber Generator Setup...")
    print("=" * 60)
    
    issues = []
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        issues.append("❌ Virtual environment not found. Run: ./run_fixed.sh")
    else:
        print("✅ Virtual environment found")
    
    # Check if enhanced generator exists
    generator_file = Path("enhanced_cucumber_generator_fixed_v2.py")
    if not generator_file.exists():
        issues.append("❌ Generator file not found")
    else:
        print("✅ Generator file found")
    
    # Test Playwright detection
    try:
        from enhanced_cucumber_generator_fixed_v2 import CucumberGenerator
        generator = CucumberGenerator()
        playwright_path = generator.get_playwright_path()
        print(f"✅ Playwright detected at: {playwright_path}")
    except Exception as e:
        issues.append(f"❌ Playwright detection failed: {e}")
    
    # Check scripts are executable
    scripts = ["run_fixed.sh", "test_playwright_detection.py"]
    for script in scripts:
        script_path = Path(script)
        if script_path.exists() and script_path.stat().st_mode & 0o111:
            print(f"✅ {script} is executable")
        else:
            issues.append(f"❌ {script} not executable. Run: chmod +x {script}")
    
    print("\n" + "=" * 60)
    
    if issues:
        print("🚨 ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        print("\n💡 Run this to fix most issues:")
        print("   ./run_fixed.sh")
    else:
        print("🎉 ALL CHECKS PASSED!")
        print("\n🚀 Ready to use! Run:")
        print("   ./run_fixed.sh")
        print("\n📚 For help, check:")
        print("   - README.md")
        print("   - TROUBLESHOOTING.md")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
