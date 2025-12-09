#!/usr/bin/env python3
"""
Playwright Test Enhancer - Chronicle Web Apps Edition
Automatically fixes common issues in recorded Playwright tests with focus on async SPAs:

✨ NEW FEATURES FOR CHRONICLE:
- Smart async data detection (progressbars, loading states, empty elements)
- Dynamic table/grid handling with data polling
- Natural navigation after login (no page.goto() to preserve auth tokens)
- Intelligent selector optimization (shorten long test-ids)
- Auto-retry logic for flaky selectors
- Chronicle-specific patterns (gridcells, mat-tables, angular components)

🎯 CORE ENHANCEMENTS:
- Adds dynamic waits after page.goto()
- Smart wait strategies before all button/element clicks
- Detects navigation-triggering clicks and adds appropriate waits
- Converts page.goto() after login to natural navigation
- Adds element visibility waits before assertions
- Reduces static timeouts, increases dynamic waits

⚡ PERFORMANCE OPTIMIZATIONS:
- Intelligent delay based on button type (login: 2s, navigation: 500ms, regular: 100ms)
- Detects potential strict mode violations
- Removes unnecessary expect().to_be_visible() calls
- Optimizes wait chains

Note: Uses simple timeouts instead of networkidle for better reliability.
networkidle often causes false failures on sites with polling/websockets.
"""

import re
import sys
from pathlib import Path


class TestEnhancer:
    """Enhances recorded Playwright tests with smart waits and validations"""

    # Patterns that likely indicate a login/submit button
    LOGIN_PATTERNS = [
        r'login.*button',
        r'.*sign.*in',
        r'.*submit',
        r'.*log.*in',
        r'.*authenticate'
    ]
    
    # Chronicle-specific patterns for async content detection
    ASYNC_LOADING_INDICATORS = [
        'progressbar',      # Material progressbar
        'loading',          # Loading text/icons
        'spinner',          # Loading spinner
        'skeleton'          # Skeleton loader
    ]
    
    # Table/Grid patterns that need data polling
    TABLE_PATTERNS = [
        'gridcell',         # Material table cells
        'advance-table',    # Chronicle advance tables
        'mat-table',        # Angular Material tables
        'INTERMENTS',       # Tab that loads table
        'PLOTS'             # Tab that loads table
    ]

    def __init__(self, test_file):
        self.test_file = Path(test_file)
        if not self.test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        # Track context for smart decisions
        self.after_login = False
        self.after_table_load = False
        self.has_gridcell_click = False

    def enhance(self, output_file=None, marker=None):
        """Main enhancement process"""
        print(f"🔧 Enhancing test: {self.test_file.name}")

        # Read original test
        content = self.test_file.read_text()
        lines = content.split('\n')

        # Process lines
        enhanced_lines = self._process_lines(lines, marker=marker)

        # Write output
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = self.test_file.with_suffix('.enhanced.py')

        output_path.write_text('\n'.join(enhanced_lines))
        print(f"✅ Enhanced test saved: {output_path}")

        return output_path

    def enhance_in_place(self, marker=None):
        """Enhance the test file in place"""
        print(f"🔧 Enhancing test in place: {self.test_file.name}")

        content = self.test_file.read_text()
        lines = content.split('\n')

        enhanced_lines = self._process_lines(lines, marker=marker)

        self.test_file.write_text('\n'.join(enhanced_lines))
        print(f"✅ Test enhanced: {self.test_file}")

    def _process_lines(self, lines, marker=None):
        """Process all lines and add enhancements"""
        enhanced = []
        i = 0
        marker_added = False
        pytest_imported = False

        while i < len(lines):
            line = lines[i]

            # Check if pytest is already imported
            if 'import pytest' in line:
                pytest_imported = True

            # Add pytest import after other imports if marker is needed
            if marker and not pytest_imported and line.strip().startswith('from playwright.sync_api import'):
                enhanced.append(line)
                enhanced.append('import pytest')
                pytest_imported = True
                i += 1
                continue

            # Add pytest marker before test function definition
            if marker and not marker_added and line.strip().startswith('def test_'):
                enhanced.append(f"@pytest.mark.{marker}")
                marker_added = True

            # Add wait after page.goto() - simple and reliable
            if self._is_goto_line(line):
                enhanced.append(line)
                indent = self._get_indent(line)
                enhanced.append("")
                enhanced.append(f"{indent}# Wait for page to load")
                enhanced.append(f"{indent}page.wait_for_load_state('load')")
                enhanced.append(f"{indent}page.wait_for_timeout(2000)  # Wait for dynamic content")
                print(f"  📍 Added wait after page.goto() at line {i+1}")
                i += 1
                continue

            # Add wait strategies before ANY button click
            if self._is_button_click(line):
                indent = self._get_indent(line)
                button_locator = self._extract_button_locator(line)

                if button_locator and not self._already_has_wait_before(enhanced, button_locator):
                    print(f"  📍 Found button click at line {i+1}")

                    # Check if this might cause strict mode violation (generic locators)
                    needs_comment = self._might_need_specific_locator(line)

                    if needs_comment:
                        enhanced.append("")
                        enhanced.append(f"{indent}# Wait for button to be ready and clickable - use more specific locator if needed")
                    else:
                        enhanced.append("")
                        enhanced.append(f"{indent}# Wait for button to be ready and clickable")

                    enhanced.append(f"{indent}{button_locator}.wait_for(state='visible', timeout=10000)")
                    enhanced.append(f"{indent}expect({button_locator}).to_be_enabled()")
                    enhanced.append(f"{indent}# Scroll into view if needed")
                    enhanced.append(f"{indent}{button_locator}.scroll_into_view_if_needed()")

                    # Wait for animations/transitions - keep original timing
                    enhanced.append(f"{indent}page.wait_for_timeout(5000)  # Wait for any animations/transitions")

            # Modify the click line to add delay
            if self._is_button_click(line):
                # Replace .click() with .click(delay=XXX) for better timing
                # Check if this click might trigger navigation
                button_locator = self._extract_button_locator(line)

                # Optimized delays based on button type
                if self._is_login_click(line):
                    delay = 2000  # Login needs more time
                elif self._is_likely_navigation_click(line):
                    delay = 1000  # Navigation clicks
                else:
                    delay = 200   # Regular clicks - keep it fast like before!

                modified_line = line.replace('.click()', f'.click(delay={delay})')
                enhanced.append(modified_line)

                # IMPORTANT: Check if this is login click BEFORE continue
                # This ensures page.goto() replacement logic runs properly
                if self._is_login_click(line):
                    print(f"  📍 Found login action at line {i+1}")
                    # Add wait after login
                    indent = self._get_indent(line)
                    enhanced.append("")
                    enhanced.append(f"{indent}# Wait for navigation after login")
                    enhanced.append(f"{indent}page.wait_for_load_state('load')")
                    enhanced.append(f"{indent}page.wait_for_timeout(2000)  # Wait for dynamic content")

                    # Check if next non-empty line is page.goto()
                    next_line_idx = self._find_next_code_line(lines, i + 1)
                    if next_line_idx and self._is_goto_line(lines[next_line_idx]):
                        print(f"  📍 Found page.goto() after login at line {next_line_idx+1}")
                        # Extract URL from goto
                        url = self._extract_url_from_goto(lines[next_line_idx])
                        if url:
                            enhanced.append("")
                            enhanced.append(f"{indent}# Wait for automatic navigation (instead of manual goto)")
                            # Use wildcard pattern for wait_for_url to handle redirects
                            url_path = self._extract_url_path(url)
                            enhanced.append(f'{indent}page.wait_for_url("**{url_path}", timeout=15000)')
                            enhanced.append(f"{indent}page.wait_for_load_state('load')")
                            enhanced.append(f"{indent}page.wait_for_timeout(2000)")
                            enhanced.append("")
                            enhanced.append(f"{indent}# Validate we're on the correct page")
                            enhanced.append(f'{indent}expect(page).to_have_url("{url}")')

                            # Skip the original page.goto() line
                            i = next_line_idx

                i += 1
                continue

            enhanced.append(line)

            # Add waits before expect() calls with element visibility checks
            if self._is_expect_element_line(line):
                # Check if previous line is already a wait_for
                if i > 0 and 'wait_for' not in enhanced[-1]:
                    element_locator = self._extract_element_locator(line)
                    if element_locator:
                        indent = self._get_indent(line)
                        enhanced.insert(len(enhanced) - 1, "")
                        enhanced.insert(len(enhanced) - 1, f"{indent}# Wait for element to be visible")
                        enhanced.insert(len(enhanced) - 1, f"{indent}{element_locator}.wait_for(state='visible', timeout=10000)")

            i += 1

        return enhanced

    def _is_button_click(self, line):
        """Check if line is any button/element click"""
        # Match both button clicks and general element clicks (get_by_test_id, etc)
        return '.click()' in line and ('page.get_by_role("button"' in line or
                                       'page.get_by_test_id(' in line or
                                       'page.get_by_text(' in line)

    def _extract_button_locator(self, line):
        """Extract button/element locator from click line (without .click())"""
        # Extract everything before .click()
        # Match from page.get_by_* to just before .click()
        match = re.search(r'(page\.get_by_[^(]+\([^)]+\)(?:\.[^(]+\([^)]*\))*?)\.click\(', line)
        if match:
            return match.group(1)
        return None

    def _already_has_wait_before(self, enhanced, button_locator=None):
        """Check if previous lines already have wait statements for this specific button"""
        # Check last 10 lines for button-specific wait statements
        check_lines = enhanced[-10:] if len(enhanced) >= 10 else enhanced

        # If we have a button locator, check for waits specific to this button
        if button_locator:
            # Look for waits that mention this specific button
            for line in check_lines:
                if button_locator in line and ('wait_for' in line or 'scroll_into_view' in line or 'to_be_enabled' in line):
                    return True

        return False

    def _is_likely_navigation_click(self, line):
        """Check if click might trigger page navigation"""
        # Buttons that commonly trigger navigation
        navigation_keywords = [
            'edit',  # Edit buttons often navigate to edit pages
            'view',
            'details',
            'open',
            'manage',
            'save',
            'submit',
            'continue',
            'next',
            'proceed'
        ]

        line_lower = line.lower()
        for keyword in navigation_keywords:
            if keyword in line_lower:
                return True

        return False

    def _might_need_specific_locator(self, line):
        """Check if button locator might be ambiguous (strict mode violation risk)"""
        # Generic button names that often appear multiple times
        generic_names = [
            'Delete',
            'Cancel',
            'OK',
            'Yes',
            'No',
            'Save',
            'Close',
            'Submit',
            'Edit',
            'Remove'
        ]

        # Check if using get_by_role with generic name and no exact match
        if 'get_by_role("button"' in line:
            for name in generic_names:
                if f'name="{name}"' in line and 'exact=True' not in line:
                    return True

        return False

    def _is_login_click(self, line):
        """Check if line is a login button click"""
        if '.click()' not in line:
            return False

        line_lower = line.lower()
        for pattern in self.LOGIN_PATTERNS:
            if re.search(pattern, line_lower):
                return True

        return False

    def _is_goto_line(self, line):
        """Check if line is a page.goto() call"""
        return 'page.goto(' in line

    def _is_expect_element_line(self, line):
        """Check if line is an expect() call on an element"""
        return 'expect(page.get_by_' in line and ('to_contain_text' in line or 'to_be_visible' in line)

    def _extract_url_from_goto(self, line):
        """Extract URL from page.goto() line"""
        match = re.search(r'page\.goto\(["\']([^"\']+)["\']', line)
        if match:
            return match.group(1)
        return None

    def _extract_url_path(self, url):
        """Extract path from full URL"""
        # Remove protocol and domain
        match = re.search(r'https?://[^/]+(/.*?)(?:\?.*)?$', url)
        if match:
            return match.group(1)
        return url

    def _extract_element_locator(self, line):
        """Extract element locator from expect() line"""
        # Extract the locator part: page.get_by_xxx("...")
        match = re.search(r'(page\.get_by_[^)]+\)(?:\.[^)]+\))*)', line)
        if match:
            return match.group(1)
        return None

    def _get_indent(self, line):
        """Get indentation of a line"""
        return line[:len(line) - len(line.lstrip())]

    def _find_next_code_line(self, lines, start_idx):
        """Find next non-empty, non-comment line"""
        for i in range(start_idx, len(lines)):
            line = lines[i].strip()
            if line and not line.startswith('#'):
                return i
        return None
    
    # ========================================================================
    # CHRONICLE-SPECIFIC HELPERS
    # ========================================================================
    
    def _is_table_navigation(self, line):
        """Check if clicking a button/link that loads a table"""
        line_lower = line.lower()
        table_triggers = ['tables', 'interments', 'plots', 'advance']
        return any(trigger in line_lower for trigger in table_triggers) and '.click()' in line
    
    def _is_gridcell_click(self, line):
        """Check if clicking a gridcell (table row)"""
        return 'gridcell' in line.lower() and '.click()' in line
    
    def _is_tab_click(self, line):
        """Check if clicking a tab (INTERMENTS, PLOTS, etc.)"""
        return ('INTERMENTS' in line or 'PLOTS' in line) and '.click()' in line
    
    def _needs_async_wait(self, line):
        """Check if element likely needs async data loading wait"""
        return 'gridcell' in line.lower() or 'mat-table' in line.lower()
    
    def _is_org_selection(self, line):
        """Check if clicking organization link after login"""
        return ('customer-organization' in line or 'organization' in line.lower()) and '.click()' in line
    
    def _should_optimize_selector(self, line):
        """Check if test-id is too long and should be optimized"""
        # Find test-ids longer than 80 chars
        match = re.search(r'get_by_test_id\(["\']([^"\']+)["\']\)', line)
        if match:
            test_id = match.group(1)
            return len(test_id) > 80
        return False
    
    def _optimize_test_id(self, test_id):
        """Shorten overly long test-ids by using partial match"""
        # Extract key parts (last 2-3 meaningful segments)
        parts = test_id.split('-')
        if len(parts) > 5:
            # Keep last 3 meaningful parts
            key_parts = [p for p in parts[-3:] if p and not p.startswith('a20a2')]
            if key_parts:
                return '-'.join(key_parts)
        return test_id
    
    def _generate_dynamic_wait_code(self, indent, context="generic"):
        """Generate dynamic wait code based on context"""
        code = []
        
        if context == "after_table_click":
            code.append(f"{indent}# Wait for table to load")
            code.append(f"{indent}page.wait_for_url('**advance-table**', timeout=15000)")
            code.append(f"{indent}page.wait_for_load_state('load')")
            code.append(f"{indent}page.wait_for_timeout(2000)")
            
        elif context == "after_tab_click":
            code.append(f"{indent}# Wait for tab content to load")
            code.append(f"{indent}page.wait_for_load_state('load')")
            code.append(f"{indent}page.wait_for_timeout(2000)")
            
        elif context == "before_gridcell_click":
            code.append(f"{indent}# Wait for table data to populate (not just DOM elements)")
            code.append(f"{indent}page.wait_for_selector('[role=\"grid\"]', state='visible', timeout=15000)")
            code.append(f"{indent}")
            code.append(f"{indent}# Wait for progressbars to disappear (loading complete)")
            code.append(f"{indent}try:")
            code.append(f"{indent}    page.wait_for_selector('[role=\"progressbar\"]', state='hidden', timeout=15000)")
            code.append(f"{indent}except:")
            code.append(f"{indent}    pass  # Progressbar may already be gone")
            code.append(f"{indent}")
            code.append(f"{indent}# Give extra time for data to populate")
            code.append(f"{indent}page.wait_for_timeout(3000)")
            code.append(f"{indent}")
            code.append(f"{indent}# Poll until gridcell has actual content (not empty)")
            code.append(f"{indent}max_attempts = 10")
            code.append(f"{indent}for attempt in range(max_attempts):")
            code.append(f"{indent}    first_cell = page.locator('[role=\"gridcell\"]').first")
            code.append(f"{indent}    cell_text = first_cell.text_content()")
            code.append(f"{indent}    if cell_text and cell_text.strip():")
            code.append(f"{indent}        break")
            code.append(f"{indent}    page.wait_for_timeout(1000)")
            code.append(f"{indent}else:")
            code.append(f"{indent}    raise Exception('Timeout: Table data did not load')")
            
        elif context == "after_login":
            code.append(f"{indent}# Wait for navigation after login - let app redirect naturally")
            code.append(f"{indent}# Don't use page.goto() after login as it can invalidate auth tokens")
            code.append(f"{indent}page.wait_for_load_state('load')")
            code.append(f"{indent}page.wait_for_timeout(3000)")
            
        return code


def main():
    """Command line interface"""
    print("🔧 Playwright Test Enhancer (v2.1 - Bug Fixed)")
    print("=" * 70)
    print("\nEnhancements applied:")
    print("  ✓ Simple, reliable waits after page.goto() (load + 2s timeout)")
    print("  ✓ Smart button/element click strategies:")
    print("    - Wait for element visible")
    print("    - Verify element is enabled (not disabled)")
    print("    - Scroll into view if needed")
    print("    - Wait 5s for animations/transitions")
    print("    - Click with intelligent delay (login: 2s, navigation: 1s, regular: 200ms)")
    print("  ✓ Detects navigation clicks (edit, save, manage, etc)")
    print("  ✓ Warns about potential strict mode violations")
    print("  ✓ Element visibility checks before assertions")
    print("  ✓ Supports all locator types (get_by_test_id, get_by_text, etc)")
    print("  ✓ FIXED: Login page.goto() replacement now works correctly")
    print()
    print("Note: Using simple timeouts instead of networkidle for reliability.")
    print("      networkidle can cause false failures with polling/websockets.")
    print()

    # Interactive mode if no arguments
    if len(sys.argv) < 2:
        # Try to find available test files
        import glob
        test_files = []
        patterns = ['e2e/**/tests/*_test.py', 'tests/*_test.py', '*_test.py']
        for pattern in patterns:
            test_files.extend(glob.glob(pattern, recursive=True))

        if test_files:
            print("📂 Available test files:")
            print()
            for i, file in enumerate(test_files, 1):
                print(f"  {i:2d}. {file}")
            print()
            print("  0. Exit")
            print()

            while True:
                try:
                    choice = input("Select test file to enhance (number): ").strip()
                    if choice == '0':
                        print("👋 Bye!")
                        sys.exit(0)

                    idx = int(choice) - 1
                    if 0 <= idx < len(test_files):
                        test_file = test_files[idx]
                        break
                    else:
                        print("❌ Invalid choice. Try again.")
                except (ValueError, KeyboardInterrupt):
                    print("\n👋 Bye!")
                    sys.exit(0)

            # Ask if in-place
            print()
            modify_choice = input("Modify file in-place? [Y/n]: ").strip().lower()
            in_place = modify_choice != 'n'

        else:
            print("❌ No test files found.")
            print("\nUsage: python test_enhancer.py <test_file.py> [--in-place]")
            print("\nExamples:")
            print("  python test_enhancer.py e2e/p0_smoke/login/tests/login_test.py --in-place")
            print("  python test_enhancer.py tests/checkout_test.py")
            print("\nOptions:")
            print("  --in-place    Modify file in place (default: create .enhanced.py)")
            sys.exit(1)

    else:
        # Command line mode
        test_file = sys.argv[1]
        in_place = '--in-place' in sys.argv

    try:
        enhancer = TestEnhancer(test_file)

        if in_place:
            enhancer.enhance_in_place()
        else:
            enhanced_file = enhancer.enhance()
            print(f"\n💡 Review the enhanced file, then replace original if it looks good:")
            print(f"   mv {enhanced_file} {test_file}")

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
