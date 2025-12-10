#!/usr/bin/env python3
"""
Simple Playwright Test Recorder
Records Playwright scripts and organizes them in a good structure
No complicated conversions - just simple, working tests!
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime


class SimpleRecorder:
    """Simple test recorder - record once, run anytime"""

    # Test priority definitions
    PRIORITIES = {
        'p0': {
            'name': 'Smoke Test',
            'description': 'Critical features that must pass before release',
            'marker': 'smoke',
            'folder': 'p0-smoke_test'
        },
        'p1': {
            'name': 'Regression',
            'description': 'Important features, run on every build',
            'marker': 'regression',
            'folder': 'p1-regression'
        },
        'p2': {
            'name': 'Exploratory',
            'description': 'Edge cases, UI validation, nice-to-have tests',
            'marker': 'exploratory',
            'folder': 'p2-exploratory'
        }
    }

    def __init__(self):
        self.base_folder = None
        self.test_name = None
        self.website_url = None
        self.priority = None
        self.category = None  # Category/folder for organizing tests
        self.subcategory = None  # Sub-category (e.g. public, login)
        self.mode = None  # 'record' or 'generate'
        self.existing_script = None  # Path to existing script if mode is 'generate'

    def run(self):
        """Main workflow"""
        print("=" * 70)
        print("🎬 SIMPLE PLAYWRIGHT TEST RECORDER")
        print("=" * 70)
        print("Record your test once → Run it anytime!")
        print()

        # Get inputs
        self.get_inputs()

        # If bulk generate mode, process all scripts
        if self.mode == 'bulk_generate':
            return self.bulk_generate_from_all()

        # Create structure
        self.create_structure()

        # Record or use existing test
        if self.mode == 'record':
            recorded_file = self.record_test()
            if not recorded_file:
                return False
        else:  # generate mode
            recorded_file = self.generate_from_existing()
            if not recorded_file:
                return False

        # Enhance the test (add waits, fix common issues)
        self.enhance_test(recorded_file)

        # Make it runnable
        self.create_test_runner(recorded_file)

        # Show instructions
        self.show_success()
        return True

    def select_existing_script(self):
        """Select existing script from codegen_script folder"""
        codegen_folder = Path("codegen_script")

        if not codegen_folder.exists():
            print(f"\n❌ Folder 'codegen_script' not found!")
            print("   This folder should contain your recorded Playwright scripts.")
            return False

        # Find all Python files in codegen_script
        script_files = list(codegen_folder.glob("*.py"))

        if not script_files:
            print(f"\n❌ No Python scripts found in 'codegen_script' folder!")
            print("   Please record a test first using mode 1 (Record new test)")
            return False

        print(f"\n📂 Available scripts in 'codegen_script':")
        for idx, script in enumerate(script_files, 1):
            print(f"   {idx}. {script.name}")

        while True:
            choice = input(f"\nSelect script [1-{len(script_files)}]: ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(script_files):
                self.existing_script = script_files[int(choice) - 1]
                print(f"✅ Selected: {self.existing_script.name}")
                return True
            print(f"❌ Please enter a number between 1 and {len(script_files)}")

    def generate_from_existing(self):
        """Generate test structure from existing script"""
        if not self.existing_script or not self.existing_script.exists():
            print("❌ No existing script found!")
            return None

        print(f"\n📋 Generating test from: {self.existing_script.name}")

        # Output to test-specific folder (subcategory/category/test)
        priority_folder = self.base_folder / self.PRIORITIES[self.priority]['folder']
        
        # Use test_name for the test file
        test_filename = f"{self.test_name}_test.py"
        
        # Build path: priority → subcategory → category → test
        if self.subcategory:
            if self.category:
                test_folder = priority_folder / self.subcategory / self.category / self.test_name
            else:
                test_folder = priority_folder / self.subcategory / self.test_name
        elif self.category:
            test_folder = priority_folder / self.category / self.test_name
        else:
            test_folder = priority_folder / self.test_name
            
        # Put test file directly in test folder (no tests/ subfolder)
        output_file = test_folder / test_filename

        try:
            # Read the existing script
            script_content = self.existing_script.read_text()

            # Write to the new location
            output_file.write_text(script_content)

            print(f"✅ Test generated: {output_file.name}")
            print(f"   Source: {self.existing_script}")
            print(f"   Destination: {output_file}")

            return output_file

        except Exception as e:
            print(f"❌ Error generating test: {e}")
            return None

    def get_inputs(self):
        """Get user inputs"""
        # Use e2e folder by default (skip question if it exists)
        self.base_folder = Path("e2e").absolute()

        if not self.base_folder.exists():
            # Only ask if e2e doesn't exist yet
            folder = input("📁 Base test folder? (press Enter for 'e2e'): ").strip()
            if not folder:
                folder = "e2e"
            self.base_folder = Path(folder).absolute()

        print(f"✅ Base folder: {self.base_folder}")

        # Get test priority
        print("\n📊 Test Priority:")
        print("   1. P0 - Smoke Test (Critical: login, checkout, core flows)")
        print("   2. P1 - Regression (Important: CRUD, search, filters)")
        print("   3. P2 - Exploratory (Nice-to-have: edge cases, UI validation)")

        while True:
            choice = input("Choose priority [1-3] (default: 2): ").strip()
            if not choice:
                choice = '2'

            if choice in ['1', '2', '3']:
                priority_map = {'1': 'p0', '2': 'p1', '3': 'p2'}
                self.priority = priority_map[choice]
                priority_info = self.PRIORITIES[self.priority]
                print(f"✅ Selected: {self.priority.upper()} - {priority_info['name']}")
                break
            print("❌ Please enter 1, 2, or 3")

        # Get category/folder first (after priority)
        self.get_category()

        # Ask mode: record new or generate from existing
        print("\n🎯 Choose mode:")
        print("   1. Record new test (open browser and record)")
        print("   2. Generate from existing script (single file)")
        print("   3. Bulk generate from ALL scripts in codegen_script folder")

        while True:
            mode_choice = input("Choose mode [1-3] (default: 1): ").strip()
            if not mode_choice:
                mode_choice = '1'

            if mode_choice in ['1', '2', '3']:
                if mode_choice == '1':
                    self.mode = 'record'
                elif mode_choice == '2':
                    self.mode = 'generate'
                else:
                    self.mode = 'bulk_generate'
                
                mode_text = {
                    'record': 'Record new test',
                    'generate': 'Generate from existing script',
                    'bulk_generate': 'Bulk generate from ALL scripts'
                }
                print(f"✅ Mode: {mode_text[self.mode]}")
                break
            print("❌ Please enter 1, 2, or 3")

        # If bulk generate mode, skip test name input
        if self.mode == 'bulk_generate':
            self.test_name = None  # Will be extracted from filenames
            return  # Skip to bulk generation

        # If generate mode, select existing script
        if self.mode == 'generate':
            if not self.select_existing_script():
                print("❌ No script selected, switching to record mode")
                self.mode = 'record'

        # Get test name
        while True:
            test_name = input("\n🏷️  Test name (e.g., login, search, checkout): ").strip().lower()
            if test_name and test_name.replace('_', '').replace('-', '').isalnum():
                self.test_name = test_name
                break
            print("❌ Use only letters, numbers, hyphens, and underscores")

        # Get URL only if recording new test
        if self.mode == 'record':
            while True:
                url = input("\n🌐 Website URL to test: ").strip()
                if url.startswith(('http://', 'https://')):
                    self.website_url = url
                    break
                print("❌ URL must start with http:// or https://")
        else:
            # For generate mode, we'll extract URL from script or use placeholder
            self.website_url = "Generated from existing script"

    def get_category(self):
        """Get subcategory and category for organizing tests"""
        priority_folder = self.base_folder / self.PRIORITIES[self.priority]['folder']
        
        # First ask for subcategory (public/login)
        print(f"\n📂 Sub-category (e.g., 'public', 'login'):")
        print("   Optional: Press Enter to skip")
        
        # Show existing subcategories if any
        if priority_folder.exists():
            subcategories = [d for d in priority_folder.iterdir() 
                           if d.is_dir() and not d.name.startswith('.')]
            if subcategories:
                print(f"\n   Existing sub-categories in {self.priority.upper()}:")
                for subcat in sorted(subcategories):
                    # Count tests in subcategory
                    test_count = len(list(subcat.glob("*/*/*/*_test.py")))
                    print(f"   • {subcat.name} ({test_count} tests)")
                print()
        
        subcategory = input("Enter sub-category name: ").strip().lower()
        if subcategory:
            if subcategory.replace('_', '').replace('-', '').isalnum():
                self.subcategory = subcategory
                print(f"✅ Sub-category: {subcategory}")
            else:
                print("⚠️  Invalid sub-category name, using none")
                self.subcategory = None
        else:
            self.subcategory = None
            print("✅ No sub-category")
        
        # Then ask for category (advance_search, person, search)
        print(f"\n📂 Category/Feature (e.g., 'advance_search', 'person', 'search'):")
        print("   This groups related tests together")
        
        # Show existing categories in selected subcategory
        if self.subcategory and priority_folder.exists():
            subcat_folder = priority_folder / self.subcategory
            if subcat_folder.exists():
                categories = [d for d in subcat_folder.iterdir() 
                             if d.is_dir() and not d.name.startswith('.')]
                if categories:
                    print(f"\n   Existing categories in {self.subcategory}:")
                    for cat in sorted(categories):
                        # Count tests in category
                        test_count = len(list(cat.glob("*/*/*_test.py")))
                        print(f"   • {cat.name} ({test_count} tests)")
                    print()
        
        while True:
            category = input("Enter category name (or press Enter to skip): ").strip().lower()
            
            # Allow empty for flat structure
            if not category:
                self.category = None
                print("✅ No category - test will be in flat structure")
                break
            
            # Validate category name
            if category.replace('_', '').replace('-', '').isalnum():
                self.category = category
                print(f"✅ Category: {category}")
                break
            
            print("❌ Use only letters, numbers, hyphens, and underscores")

    def create_structure(self):
        """Create folder structure: priority/subcategory/category/test/tests/"""
        print(f"\n📂 Creating test structure...")

        # Get priority folder info
        priority_info = self.PRIORITIES[self.priority]
        priority_folder = self.base_folder / priority_info['folder']

        # Build path: priority → subcategory → category → test
        if self.subcategory:
            if self.category:
                test_folder = priority_folder / self.subcategory / self.category / self.test_name
                path_display = f"{priority_info['folder']}/{self.subcategory}/{self.category}/{self.test_name}"
            else:
                test_folder = priority_folder / self.subcategory / self.test_name
                path_display = f"{priority_info['folder']}/{self.subcategory}/{self.test_name}"
        elif self.category:
            test_folder = priority_folder / self.category / self.test_name
            path_display = f"{priority_info['folder']}/{self.category}/{self.test_name}"
        else:
            test_folder = priority_folder / self.test_name
            path_display = f"{priority_info['folder']}/{self.test_name}"

        # Create folders (without tests/ subfolder for simplicity)
        folders = [
            self.base_folder,
            priority_folder
        ]

        # Add subcategory and category folders if needed
        if self.subcategory:
            folders.append(priority_folder / self.subcategory)
            if self.category:
                folders.append(priority_folder / self.subcategory / self.category)
        elif self.category:
            folders.append(priority_folder / self.category)
        
        folders.append(test_folder)

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

        print(f"✅ Folders created in {path_display}")

    def record_test(self):
        """Record the test"""
        print("\n🎬 RECORDING")
        print("-" * 70)
        print(f"🌐 Target: {self.website_url}")
        print(f"📊 Priority: {self.priority.upper()} - {self.PRIORITIES[self.priority]['name']}")
        print("\n📝 Instructions:")
        print("   1. Browser will open")
        print("   2. Do your test actions")
        print("   3. Close browser when done")
        print("\nPress Enter to start...")
        input()

        # First record to codegen_script folder (original script)
        codegen_folder = Path("codegen_script")
        codegen_folder.mkdir(exist_ok=True)

        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        codegen_file = codegen_folder / f"{self.test_name}_{timestamp}.py"

        try:
            # Try to run playwright codegen
            cmd = [
                sys.executable, "-m", "playwright", "codegen",
                self.website_url,
                "--target", "python-pytest",
                "--output", str(codegen_file)
            ]

            print("🎥 Recording... (perform your test actions)")
            subprocess.run(cmd, check=True)

            if codegen_file.exists():
                print(f"✅ Original script saved: {codegen_file}")

                # Copy to test folder (subcategory/category/test)
                priority_folder = self.base_folder / self.PRIORITIES[self.priority]['folder']
                
                # Build path: priority → subcategory → category → test
                if self.subcategory:
                    if self.category:
                        test_folder = priority_folder / self.subcategory / self.category / self.test_name
                    else:
                        test_folder = priority_folder / self.subcategory / self.test_name
                elif self.category:
                    test_folder = priority_folder / self.category / self.test_name
                else:
                    test_folder = priority_folder / self.test_name
                
                # Use simple test filename (no timestamp in final test file)
                test_filename = f"{self.test_name}_test.py"
                output_file = test_folder / test_filename

                # Ensure test folder exists
                test_folder.mkdir(parents=True, exist_ok=True)

                # Copy the content
                output_file.write_text(codegen_file.read_text())
                print(f"✅ Test copied to: {output_file.name}")

                return output_file
            else:
                print("❌ Recording failed - no file created")
                return None

        except subprocess.CalledProcessError as e:
            print(f"❌ Recording error: {e}")
            return None
        except FileNotFoundError:
            print("❌ Playwright not found!")
            print("💡 Install it: pip install playwright && playwright install")
            return None

    def enhance_test(self, test_file):
        """Enhance the recorded test with Chronicle-specific improvements"""
        print("\n🔧 Enhancing test with Chronicle patterns...")

        try:
            # Import the Chronicle enhancer
            from utils.chronicle_enhancer import ChronicleEnhancer

            # Get priority marker
            marker = self.PRIORITIES[self.priority]['marker']

            enhancer = ChronicleEnhancer(test_file)
            enhancer.enhance(marker=marker)

            print("✅ Test enhanced with:")
            print("   • Dynamic async waits (no static timeouts)")
            print("   • Table data polling (wait for actual content)")
            print("   • Natural navigation after login (preserve auth tokens)")
            print("   • Optimized selectors (shorter, more flexible)")
            print(f"   • Pytest marker: @pytest.mark.{marker}")
            print()
            print(f"📊 Enhancement Statistics:")
            print(f"   • Dynamic waits added: {enhancer.stats['dynamic_waits_added']}")
            print(f"   • Table polling added: {enhancer.stats['table_polls_added']}")
            print(f"   • Login flows fixed: {enhancer.stats['login_flows_fixed']}")
            print(f"   • Selectors optimized: {enhancer.stats['selectors_optimized']}")

        except Exception as e:
            print(f"⚠️  Enhancement skipped: {e}")
            print("   Test will still work, but may need manual tweaks")

    def create_test_runner(self, test_file):
        """Point user to the main interactive test runner"""
        print("\n✅ Test runner: Use run_tests_interactive.py")
        print(f"   Located at: {Path.cwd() / 'run_tests_interactive.py'}")

    def show_success(self):
        """Show success message"""
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Your test is ready!")
        print("=" * 70)
        
        # Build path display (subcategory → category → test)
        priority_info = self.PRIORITIES[self.priority]
        if self.subcategory:
            if self.category:
                test_path = f"{priority_info['folder']}/{self.subcategory}/{self.category}/{self.test_name}"
            else:
                test_path = f"{priority_info['folder']}/{self.subcategory}/{self.test_name}"
        elif self.category:
            test_path = f"{priority_info['folder']}/{self.category}/{self.test_name}"
        else:
            test_path = f"{priority_info['folder']}/{self.test_name}"
        
        print(f"\n📁 Location: {self.base_folder}/{test_path}")
        print(f"🏷️  Test: {self.test_name}")
        if self.subcategory:
            print(f"📂 Sub-category: {self.subcategory}")
        if self.category:
            print(f"📂 Category: {self.category}")
        print(f"📊 Priority: {self.priority.upper()} - {priority_info['name']}")
        print(f"🌐 URL: {self.website_url}")
        print("\n📋 How to run your test:")
        print("   python3 run_tests_interactive.py")
        print(f"   Then select: {self.priority.upper()}", end="")
        if self.subcategory:
            print(f" → {self.subcategory}", end="")
            if self.category:
                print(f" → {self.category}", end="")
        print(f" → {self.test_name}")

    def bulk_generate_from_all(self):
        """Bulk generate tests from all scripts in codegen_script folder"""
        codegen_folder = Path("codegen_script")
        
        if not codegen_folder.exists():
            print(f"\n❌ Folder 'codegen_script' not found!")
            return False
        
        # Find all Python files and sort alphabetically
        script_files = sorted(list(codegen_folder.glob("*.py")), key=lambda x: x.name.lower())
        
        if not script_files:
            print(f"\n❌ No Python scripts found in 'codegen_script' folder!")
            return False
        
        print(f"\n📦 Found {len(script_files)} scripts to process")
        priority_info = self.PRIORITIES[self.priority]
        if self.subcategory:
            if self.category:
                target_path = f"{priority_info['folder']}/{self.subcategory}/{self.category}"
            else:
                target_path = f"{priority_info['folder']}/{self.subcategory}"
        elif self.category:
            target_path = f"{priority_info['folder']}/{self.category}"
        else:
            target_path = priority_info['folder']
        print(f"📁 Target folder: {self.base_folder / target_path}")
        print("\n📄 Files:")
        for idx, script_file in enumerate(script_files, 1):
            print(f"   {idx:2d}. {script_file.name}")
        
        # Ask for range selection
        print(f"\n🎯 Select range to process (1-{len(script_files)})")
        print("   Examples: '1-5' or '10-15' or 'all' for all files")
        range_input = input("Enter range: ").strip().lower()
        
        if range_input == 'all':
            selected_files = script_files
            print(f"✅ Processing ALL {len(script_files)} files")
        else:
            try:
                if '-' not in range_input:
                    print("❌ Invalid format! Use format: '1-5' or 'all'")
                    return False
                
                start_str, end_str = range_input.split('-')
                start_idx = int(start_str.strip())
                end_idx = int(end_str.strip())
                
                if start_idx < 1 or end_idx > len(script_files) or start_idx > end_idx:
                    print(f"❌ Invalid range! Must be between 1-{len(script_files)}")
                    return False
                
                selected_files = script_files[start_idx-1:end_idx]
                print(f"✅ Processing files {start_idx}-{end_idx} ({len(selected_files)} files)")
                
            except ValueError:
                print("❌ Invalid input! Use format: '1-5' or 'all'")
                return False
        
        # Show selected files
        print("\n📋 Selected files:")
        for idx, script_file in enumerate(selected_files, 1):
            print(f"   • {script_file.name}")
        
        # Ask for confirmation
        confirmation = input(f"\nGenerate {len(selected_files)} tests? [y/N]: ").strip().lower()
        
        if confirmation not in ['y', 'yes']:
            print("❌ Bulk generation cancelled")
            return False
        
        print("=" * 70)
        
        # Statistics
        success_count = 0
        failed_count = 0
        failed_files = []
        
        # Process each script
        for idx, script_file in enumerate(selected_files, 1):
            print(f"\n[{idx}/{len(selected_files)}] Processing: {script_file.name}")
            print("-" * 70)
            
            try:
                # Set current script
                self.existing_script = script_file
                
                # Extract test name from filename (remove timestamp if exists)
                test_name = script_file.stem
                # Remove timestamp pattern (YYYYMMDD_HHMMSS)
                import re
                test_name = re.sub(r'_\d{8}_\d{6}$', '', test_name)
                self.test_name = test_name
                
                # Create structure for this test
                self.create_structure()
                
                # Generate from existing
                recorded_file = self.generate_from_existing()
                if not recorded_file:
                    failed_count += 1
                    failed_files.append(script_file.name)
                    print(f"   ❌ Failed to generate test from {script_file.name}")
                    continue
                
                # Enhance the test
                self.enhance_test(recorded_file)
                
                # Make it runnable
                self.create_test_runner(recorded_file)
                
                success_count += 1
                print(f"   ✅ Successfully generated: {self.test_name}")
                
            except Exception as e:
                failed_count += 1
                failed_files.append(script_file.name)
                print(f"   ❌ Error processing {script_file.name}: {e}")
                continue
        
        # Show summary
        print("\n" + "=" * 70)
        print("📊 BULK GENERATION SUMMARY")
        print("=" * 70)
        print(f"✅ Success: {success_count}/{len(selected_files)} tests")
        print(f"❌ Failed:  {failed_count}/{len(selected_files)} tests")
        
        if failed_files:
            print(f"\n❌ Failed files:")
            for fname in failed_files:
                print(f"   • {fname}")
        
        priority_info = self.PRIORITIES[self.priority]
        print(f"\n📁 Location: {self.base_folder}/{priority_info['folder']}")
        print(f"📊 Priority: {self.priority.upper()} - {priority_info['name']}")
        
        print("\n📋 How to run all tests:")
        print("   python3 run_tests_interactive.py")
        print(f"   Then select: {self.priority.upper()} → Run all tests")
        
        return True
        print("\n✨ That's it! Simple and working!")


def main():
    """Main entry point"""
    try:
        recorder = SimpleRecorder()
        success = recorder.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
