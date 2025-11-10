#!/usr/bin/env python3
"""
Test script to verify Playwright path detection
"""
import sys
from pathlib import Path

# Add the current directory to Python path to import our generator
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_cucumber_generator_fixed_v2 import CucumberGenerator

def test_playwright_detection():
    print("🧪 Testing Playwright path detection...")
    print("=" * 50)
    
    generator = CucumberGenerator()
    
    try:
        playwright_path = generator.get_playwright_path()
        print(f"✅ Found Playwright at: {playwright_path}")
        
        # Test if the path actually works
        import subprocess
        
        if playwright_path.endswith(" -m playwright"):
            cmd_parts = playwright_path.split() + ["--help"]
        else:
            cmd_parts = [playwright_path, "--help"]
        
        result = subprocess.run(cmd_parts, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Playwright executable is working correctly!")
            print("🎉 You can now run the generator safely.")
            return True
        else:
            print(f"❌ Playwright found but not working: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Playwright: {e}")
        print("💡 Please run: ./run_fixed.sh to set up the environment")
        return False

if __name__ == "__main__":
    success = test_playwright_detection()
    sys.exit(0 if success else 1)
