#!/usr/bin/env python3
"""
🎭 Playwright to Cucumber Test Runner
Generated on: 2025-11-10 16:11:20
Feature: login
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
    print(f"🧪 Running tests for feature: {feature_label}")
    
    # Find feature files with the label
    feature_dir = Path(__file__).parent / "features" / feature_label
    if not feature_dir.exists():
        print(f"❌ Feature directory not found: {feature_dir}")
        return False
    
    feature_files = list(feature_dir.glob("*.feature"))
    if not feature_files:
        print(f"❌ No feature files found in {feature_dir}")
        return False
    
    # Run pytest for the specific feature
    test_file = Path(__file__).parent / f"test_{feature_label}.py"
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"🚀 Running: {test_file}")
    
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
    print(f"🐍 Using Python: {python_exe}")
    
    # Run pytest with HTML report using the correct Python executable
    cmd = [
        python_exe, "-m", "pytest", 
        str(test_file),
        "--html", str(reports_dir / f"report_{feature_label}.html"),
        "--self-contained-html",
        "-v", "--tb=short"
    ]
    
    try:
        print(f"🔧 Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Tests passed! Report: {reports_dir / f'report_{feature_label}.html'}")
            return True
        else:
            print(f"❌ Tests failed! Check report: {reports_dir / f'report_{feature_label}.html'}")
            print("💡 Make sure all dependencies are installed in the virtual environment")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        print("💡 Try running with virtual environment activated:")
        print(f"   source ../venv/bin/activate && python run_tests.py {feature_label}")
        return False

def main():
    if len(sys.argv) > 1:
        feature_label = sys.argv[1]
        run_specific_feature(feature_label)
    else:
        config = load_config()
        print(f"📋 Available feature: {config['feature_label']}")
        print(f"Usage: python run_tests.py {config['feature_label']}")

if __name__ == "__main__":
    main()
