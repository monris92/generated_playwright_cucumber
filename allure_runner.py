#!/usr/bin/env python3
"""
🎯 Advanced Allure Test Runner
Enhanced reporting with Allure integration
"""

import sys
import subprocess
import json
import shutil
import webbrowser
from pathlib import Path
import time

def check_allure_installation():
    """Check if Allure CLI is installed"""
    import os
    try:
        # Add Java path to environment for subprocess
        env = os.environ.copy()
        env['PATH'] = '/opt/homebrew/opt/openjdk/bin:' + env.get('PATH', '')
        
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True, env=env)
        if result.returncode == 0:
            print(f"✅ Allure CLI found: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_allure_cli():
    """Provide instructions to install Allure CLI"""
    print("\n📦 Installing Allure CLI...")
    print("\n🔧 Installation options:")
    print("1. npm install -g allure-commandline")
    print("2. brew install allure (macOS)")
    print("3. Download from: https://github.com/allure-framework/allure2/releases")
    
    choice = input("\n⚡ Try npm install automatically? (y/n): ")
    if choice.lower() == 'y':
        try:
            print("Installing Allure CLI via npm...")
            result = subprocess.run(["npm", "install", "-g", "allure-commandline"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Allure CLI installed successfully!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js first.")
            return False
    return False

def run_tests_with_allure(project_path, feature_label):
    """Run tests with comprehensive Allure reporting"""
    project_path = Path(project_path).resolve()
    
    print(f"\n🚀 Running tests for: {feature_label}")
    print(f"📁 Project: {project_path}")
    
    # Setup directories
    reports_dir = project_path / "reports"
    allure_results_dir = reports_dir / "allure-results"
    allure_report_dir = reports_dir / "allure-report"
    
    # Clean and create directories
    if allure_results_dir.exists():
        shutil.rmtree(allure_results_dir)
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    if allure_report_dir.exists():
        shutil.rmtree(allure_report_dir)
    allure_report_dir.mkdir(parents=True, exist_ok=True)
    
    # Test file - check both possible locations
    test_file = project_path / f"test_{feature_label}.py"
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        # List available files for debugging
        print(f"📁 Available files in {project_path}:")
        for f in project_path.iterdir():
            print(f"  - {f.name}")
        return False
    
    print(f"✅ Found test file: {test_file}")
    
    # Create environment properties for Allure
    env_props = allure_results_dir / "environment.properties"
    with open(env_props, 'w') as f:
        f.write(f"""# Test Environment
Feature.Name={feature_label}
Browser=Chromium
Test.Framework=Playwright + pytest-bdd
Reporting=Allure
Execution.Date={time.strftime('%Y-%m-%d %H:%M:%S')}
Python.Version={sys.version.split()[0]}
""")
    
    # Run pytest with Allure
    print("\n🧪 Running tests...")
    cmd = [
        "pytest", 
        str(test_file),
        "--alluredir", str(allure_results_dir),
        "--html", str(reports_dir / f"report_{feature_label}.html"),
        "--self-contained-html",
        "-v", "--tb=short",
        "--capture=no"  # Show real-time output
    ]
    
    print(f"🔍 Command: {' '.join(cmd)}")
    print(f"📂 Working directory: {project_path}")
    
    try:
        # Run in the project directory
        result = subprocess.run(cmd, cwd=project_path, text=True)
        
        if result.returncode == 0:
            print("\n✅ Tests completed successfully!")
        else:
            print("\n⚠️ Tests completed with issues")
        
        # Generate Allure report
        if check_allure_installation():
            print("\n📊 Generating Allure report...")
            
            # Setup environment with Java path
            import os
            env = os.environ.copy()
            env['PATH'] = '/opt/homebrew/opt/openjdk/bin:' + env.get('PATH', '')
            
            # Generate static report
            generate_cmd = [
                "allure", "generate", str(allure_results_dir),
                "-o", str(allure_report_dir), "--clean"
            ]
            
            gen_result = subprocess.run(generate_cmd, capture_output=True, text=True, env=env)
            
            if gen_result.returncode == 0:
                print(f"✅ Allure report generated: {allure_report_dir / 'index.html'}")
                
                # Ask to open report
                open_choice = input("\n🌐 Open Allure report in browser? (y/n): ")
                if open_choice.lower() == 'y':
                    report_url = f"file://{allure_report_dir.absolute() / 'index.html'}"
                    webbrowser.open(report_url)
                    print(f"🚀 Opened: {report_url}")
                
                # Offer to serve report
                serve_choice = input("\n🖥️  Start Allure server for interactive report? (y/n): ")
                if serve_choice.lower() == 'y':
                    print("\n🌐 Starting Allure server...")
                    print("Press Ctrl+C to stop the server")
                    try:
                        subprocess.run(["allure", "serve", str(allure_results_dir)], env=env)
                    except KeyboardInterrupt:
                        print("\n⏹️ Server stopped")
                
            else:
                print(f"❌ Report generation failed: {gen_result.stderr}")
        else:
            print("\n⚠️ Allure CLI not found")
            if install_allure_cli():
                print("✅ Please run the script again to generate Allure report")
        
        print(f"\n📋 Report Summary:")
        print(f"📄 HTML Report: {reports_dir / f'report_{feature_label}.html'}")
        print(f"📊 Allure Results: {allure_results_dir}")
        print(f"🎯 Allure Report: {allure_report_dir / 'index.html'}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python allure_runner.py <project_path> <feature_label>")
        print("Example: python allure_runner.py ./testproject login")
        return
    
    project_path = sys.argv[1]
    feature_label = sys.argv[2]
    
    print("🎭 ADVANCED ALLURE TEST RUNNER")
    print("=" * 50)
    
    run_tests_with_allure(project_path, feature_label)

if __name__ == "__main__":
    main()
