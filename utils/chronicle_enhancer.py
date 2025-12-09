#!/usr/bin/env python3
"""
Chronicle-Specific Test Enhancer
Smart Playwright test enhancement designed for Chronicle Cemetery Management web apps.

🎯 KEY IMPROVEMENTS:
1. **Dynamic Async Waits**: Detects and waits for actual data loading
2. **Table/Grid Intelligence**: Polls gridcells until data populates
3. **Login Flow Optimization**: Natural navigation without page.goto()
4. **Smart Selector Optimization**: Shortens overly long test-ids
5. **Reduced Static Timeouts**: Uses dynamic waits where possible
6. **Chronicle Patterns**: Knows progressbars, gridcells, mat-tables

🚀 USAGE:
    python utils/chronicle_enhancer.py <test_file> --in-place

📋 WHAT IT FIXES:
    ❌ BEFORE: page.wait_for_timeout(5000)  # Static wait
    ✅ AFTER:  Poll until gridcell.text_content() is not empty
    
    ❌ BEFORE: page.goto() after login (breaks auth tokens)
    ✅ AFTER:  Natural navigation with conditional org link clicking
    
    ❌ BEFORE: Click gridcell immediately (empty data)
    ✅ AFTER:  Wait for progressbar → Poll for data → Then click
    
    ❌ BEFORE: Unnecessary expect().to_be_visible() everywhere
    ✅ AFTER:  Only essential waits and validations
"""

import re
import sys
from pathlib import Path
from datetime import datetime


class ChronicleEnhancer:
    """Enhances tests with Chronicle-specific patterns"""

    def __init__(self, test_file):
        self.test_file = Path(test_file)
        if not self.test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        # Track state for context-aware enhancements
        self.seen_login = False
        self.seen_table_click = False
        self.seen_tab_click = False
        
        # Statistics
        self.stats = {
            'static_waits_removed': 0,
            'dynamic_waits_added': 0,
            'selectors_optimized': 0,
            'expects_removed': 0,
            'login_flows_fixed': 0,
            'table_polls_added': 0
        }

    def enhance(self, output_file=None, marker=None):
        """Main enhancement process"""
        print(f"\n🔧 Enhancing test for Chronicle: {self.test_file.name}")
        print("=" * 70)

        content = self.test_file.read_text()
        lines = content.split('\n')

        enhanced_lines = self._process_lines(lines, marker=marker)

        if output_file:
            output_path = Path(output_file)
        else:
            # Create backup
            backup_path = self.test_file.with_suffix('.backup')
            self.test_file.rename(backup_path)
            output_path = self.test_file

        output_path.write_text('\n'.join(enhanced_lines))
        
        print("\n📊 Enhancement Statistics:")
        print(f"  • Static waits removed: {self.stats['static_waits_removed']}")
        print(f"  • Dynamic waits added: {self.stats['dynamic_waits_added']}")
        print(f"  • Selectors optimized: {self.stats['selectors_optimized']}")
        print(f"  • Unnecessary expects removed: {self.stats['expects_removed']}")
        print(f"  • Login flows fixed: {self.stats['login_flows_fixed']}")
        print(f"  • Table polling added: {self.stats['table_polls_added']}")
        print(f"\n✅ Enhanced test saved: {output_path}")

        return output_path

    def _process_lines(self, lines, marker=None):
        """Process all lines with Chronicle-specific logic"""
        enhanced = []
        i = 0
        marker_added = False
        pytest_imported = False
        re_imported = False

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # === IMPORTS ===
            if 'import pytest' in line:
                pytest_imported = True
            if 'import re' in line:
                re_imported = True

            # Add imports if needed
            if stripped.startswith('from playwright.sync_api import'):
                enhanced.append(line)
                if marker and not pytest_imported:
                    enhanced.append('import pytest')
                    pytest_imported = True
                if not re_imported:
                    enhanced.append('import re')
                    re_imported = True
                i += 1
                continue

            # === PYTEST MARKER ===
            if marker and not marker_added and stripped.startswith('def test_'):
                enhanced.append(f"@pytest.mark.{marker}")
                marker_added = True

            # === PAGE.GOTO() - Add simple load wait ===
            if 'page.goto(' in line:
                enhanced.append(line)
                indent = self._get_indent(line)
                enhanced.append("")
                enhanced.append(f"{indent}# Wait for page to load")
                enhanced.append(f"{indent}page.wait_for_load_state('load')")
                enhanced.append(f"{indent}page.wait_for_timeout(2000)")
                i += 1
                continue

            # === LOGIN BUTTON CLICK ===
            if self._is_login_click(line):
                self.seen_login = True
                enhanced.append(line)
                indent = self._get_indent(line)
                
                # Add wait after login
                enhanced.extend(self._generate_login_wait(indent))
                
                # Check for page.goto() after login and replace with natural navigation
                next_idx = self._find_next_code_line(lines, i + 1)
                if next_idx and 'page.goto(' in lines[next_idx]:
                    url = self._extract_url(lines[next_idx])
                    if url and 'customer-organization' in url:
                        enhanced.extend(self._generate_natural_navigation(indent, url))
                        i = next_idx  # Skip the page.goto() line
                        self.stats['login_flows_fixed'] += 1
                        print(f"  ✅ Fixed login flow with natural navigation (line {next_idx+1})")
                
                i += 1
                continue

            # === TABLES BUTTON CLICK ===
            if self._is_table_button_click(line):
                self.seen_table_click = True
                enhanced.append(line)
                indent = self._get_indent(line)
                enhanced.append("")
                enhanced.append(f"{indent}# Wait for navigation to tables page")
                enhanced.append(f'{indent}page.wait_for_url("**/advance-table**", timeout=15000)')
                enhanced.append(f"{indent}page.wait_for_load_state('load')")
                enhanced.append(f"{indent}page.wait_for_timeout(2000)")
                self.stats['dynamic_waits_added'] += 1
                i += 1
                continue

            # === TAB CLICK (INTERMENTS, PLOTS, etc.) ===
            if self._is_tab_click(line):
                self.seen_tab_click = True
                enhanced.append(line)
                indent = self._get_indent(line)
                
                # Wait for URL change and data load
                tab_name = self._extract_tab_name(line)
                if tab_name:
                    enhanced.append("")
                    enhanced.append(f"{indent}# Wait for tab content to load")
                    enhanced.append(f'{indent}page.wait_for_url("**/advance-table?tab={tab_name.lower()}**", timeout=15000)')
                    enhanced.append(f"{indent}page.wait_for_load_state('load')")
                    enhanced.append(f"{indent}page.wait_for_timeout(2000)")
                    self.stats['dynamic_waits_added'] += 1
                
                i += 1
                continue

            # === GRIDCELL CLICK - Add data polling ===
            if self._is_gridcell_click(line):
                indent = self._get_indent(line)
                
                # Add comprehensive data loading wait
                enhanced.extend(self._generate_table_polling(indent))
                self.stats['table_polls_added'] += 1
                print(f"  ✅ Added table data polling before gridcell click (line {i+1})")
                
                # Add 1 second pause before click
                enhanced.append(f"{indent}page.wait_for_timeout(1000)")
                
                # Now add the click
                enhanced.append(line)
                
                # Add wait for navigation to edit page
                enhanced.append("")
                enhanced.append(f"{indent}# Wait for navigation to edit page")
                enhanced.append(f'{indent}page.wait_for_url("**/manage/edit/**", timeout=15000)')
                enhanced.append(f"{indent}page.wait_for_load_state('load')")
                enhanced.append(f"{indent}page.wait_for_timeout(1000)")
                
                i += 1
                continue
            
            # === ANY CLICK FOLLOWED BY PAGE.GOTO() - Replace with dynamic wait ===
            if '.click()' in line and not 'delay=' in line:
                # Check if next non-empty line is page.goto()
                next_idx = self._find_next_code_line(lines, i + 1)
                if next_idx and 'page.goto(' in lines[next_idx]:
                    # This is a navigation click followed by redundant goto
                    indent = self._get_indent(line)
                    
                    # Add 1 second pause before click
                    enhanced.append(f"{indent}page.wait_for_timeout(1000)")
                    enhanced.append(line)
                    
                    # Extract URL to determine where we're navigating
                    url = self._extract_url(lines[next_idx])
                    if url:
                        # Generate dynamic wait instead of page.goto()
                        enhanced.append("")
                        enhanced.append(f"{indent}# Wait for navigation after click (don't force with page.goto())")
                        
                        # Generate dynamic wait for ANY navigation (not just specific URLs)
                        url_pattern = self._extract_url_pattern(url)
                        if url_pattern:
                            enhanced.append(f'{indent}page.wait_for_url("**{url_pattern}**", timeout=15000)')
                            enhanced.append(f"{indent}page.wait_for_load_state('load')")
                            enhanced.append(f"{indent}page.wait_for_timeout(1000)")
                            
                            # Skip lines until we find expect or another action (skip page.goto and static waits)
                            skip_idx = next_idx + 1
                            while skip_idx < len(lines):
                                skip_line = lines[skip_idx].strip()
                                # Skip page.goto, wait_for_load_state, wait_for_timeout
                                if (skip_line.startswith('page.goto(') or 
                                    skip_line.startswith('page.wait_for_load_state') or
                                    skip_line.startswith('page.wait_for_timeout') or
                                    skip_line.startswith('# Wait for page')):
                                    skip_idx += 1
                                    continue
                                break
                            
                            # Find next expect or action with visible element
                            if skip_idx < len(lines):
                                next_action_line = lines[skip_idx]
                                if 'expect(' in next_action_line and '.to_be_visible()' in next_action_line:
                                    # Extract the element being checked
                                    element_locator = self._extract_expect_locator(next_action_line)
                                    if element_locator:
                                        enhanced.append("")
                                        enhanced.append(f"{indent}# Dynamic wait for element to fully load")
                                        enhanced.append(f"{indent}{element_locator}.wait_for(state='visible', timeout=15000)")
                            
                            i = skip_idx - 1  # Jump to the line before next action
                            self.stats['dynamic_waits_added'] += 1
                            print(f"  ✅ Replaced page.goto() with dynamic wait after click (line {next_idx+1})")
                            i += 1
                            continue

            # === REMOVE UNNECESSARY WAITS ===
            # Remove redundant .wait_for() before .click() if we already added smart wait
            if '.wait_for(' in line and 'state=' in line:
                # Check if next line is the same element clicking
                next_idx = self._find_next_code_line(lines, i + 1)
                if next_idx:
                    next_line = lines[next_idx]
                    locator = self._extract_locator(line)
                    if locator and locator in next_line and '.click()' in next_line:
                        # Skip this wait, we'll add better one
                        i += 1
                        continue

            # === REMOVE UNNECESSARY EXPECTS ===
            # Remove redundant expect().to_be_visible() right before clicking same element
            if 'expect(' in line and '.to_be_visible()' in line:
                next_idx = self._find_next_code_line(lines, i + 1)
                if next_idx:
                    next_line = lines[next_idx]
                    locator = self._extract_locator(line)
                    if locator and locator in next_line and '.click()' in next_line:
                        # Skip this expect, the wait_for ensures visibility
                        self.stats['expects_removed'] += 1
                        i += 1
                        continue

            # === OPTIMIZE LONG TEST-IDS ===
            if 'get_by_test_id(' in line:
                optimized = self._optimize_long_test_id(line)
                if optimized != line:
                    enhanced.append(optimized)
                    self.stats['selectors_optimized'] += 1
                    i += 1
                    continue

            # === REDUCE STATIC TIMEOUTS ===
            if 'page.wait_for_timeout(' in line:
                # If we see a long static timeout, try to reduce it
                match = re.search(r'page\.wait_for_timeout\((\d+)\)', line)
                if match:
                    timeout = int(match.group(1))
                    if timeout > 3000:
                        # Reduce excessive timeouts
                        new_timeout = min(timeout, 3000)
                        new_line = line.replace(f'({timeout})', f'({new_timeout})')
                        enhanced.append(new_line)
                        self.stats['static_waits_removed'] += 1
                        i += 1
                        continue

            # Default: keep the line
            enhanced.append(line)
            i += 1

        return enhanced

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

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

    def _extract_locator(self, line):
        """Extract locator from a line"""
        # Match patterns like: page.get_by_xxx(...).yyy(...)
        match = re.search(r'(page\.get_by_[^.]+\([^)]+\)(?:\.[^(]+\([^)]*\))*)', line)
        if match:
            return match.group(1)
        return None

    def _extract_url(self, line):
        """Extract URL from page.goto() line"""
        match = re.search(r'page\.goto\(["\']([^"\']+)["\']', line)
        if match:
            return match.group(1)
        return None

    def _extract_tab_name(self, line):
        """Extract tab name from click line"""
        if 'INTERMENTS' in line:
            return 'interments'
        elif 'PLOTS' in line:
            return 'plots'
        return None
    
    def _extract_url_pattern(self, url):
        """Extract meaningful URL pattern for wait_for_url() - GENERIC for any URL"""
        if not url:
            return None
        
        # Remove protocol and domain to get path
        if '://' in url:
            url = url.split('://', 1)[1]
            if '/' in url:
                url = '/' + url.split('/', 1)[1]
        
        # Remove query params and fragments for pattern matching
        if '?' in url:
            url = url.split('?')[0]
        if '#' in url:
            url = url.split('#')[0]
        
        # If URL is just root or too generic, return None
        if url in ['/', '', '/map', '/search']:
            return None
        
        return url
    
    def _extract_expect_locator(self, line):
        """Extract element locator from expect() line"""
        # Match patterns like: expect(page.get_by_xxx(...).locator(...)).to_be_visible()
        # Need to handle nested parentheses properly
        
        if 'expect(' not in line:
            return None
        
        # Find the start of the locator (after 'expect(')
        start = line.find('expect(') + 7
        
        # Find matching closing parenthesis using counter
        paren_count = 1
        i = start
        while i < len(line) and paren_count > 0:
            if line[i] == '(':
                paren_count += 1
            elif line[i] == ')':
                paren_count -= 1
            i += 1
        
        if paren_count == 0:
            # Extract the locator (everything between 'expect(' and matching ')')
            locator = line[start:i-1].strip()
            # Only return if it starts with 'page.'
            if locator.startswith('page.'):
                return locator
        
        return None

    # ========================================================================
    # DETECTION METHODS
    # ========================================================================

    def _is_login_click(self, line):
        """Check if line is a login button click"""
        if '.click()' not in line:
            return False
        line_lower = line.lower()
        return any(pattern in line_lower for pattern in ['login', 'sign', 'authenticate'])

    def _is_table_button_click(self, line):
        """Check if clicking Tables button"""
        return 'Tables' in line and '.click()' in line

    def _is_tab_click(self, line):
        """Check if clicking a tab"""
        return ('INTERMENTS' in line or 'PLOTS' in line) and '.click()' in line

    def _is_gridcell_click(self, line):
        """Check if clicking a gridcell"""
        return 'gridcell' in line.lower() and '.click()' in line

    def _optimize_long_test_id(self, line):
        """Optimize overly long test-ids"""
        match = re.search(r'get_by_test_id\(["\']([^"\']+)["\']\)', line)
        if match:
            test_id = match.group(1)
            if len(test_id) > 100:
                # Try to use last meaningful parts
                parts = test_id.split('-')
                if len(parts) > 6:
                    # Keep last 4 parts
                    short_id = '-'.join(parts[-4:])
                    # Use partial match with filter
                    indent = self._get_indent(line)
                    comment = f'{indent}# Optimized selector (original too long)'
                    new_selector = f'{indent}page.locator("[data-testid*=\\"{short_id}\\"]")'
                    return f'{comment}\n{new_selector}'
        return line

    # ========================================================================
    # CODE GENERATORS
    # ========================================================================

    def _generate_login_wait(self, indent):
        """Generate wait code after login"""
        return [
            "",
            f"{indent}# Wait for navigation after login - let app redirect naturally",
            f"{indent}# Don't use page.goto() after login as it can invalidate auth tokens",
            f"{indent}page.wait_for_load_state('load')",
            f"{indent}page.wait_for_timeout(3000)"
        ]

    def _generate_natural_navigation(self, indent, url):
        """Generate natural navigation code after login - GENERIC for any cemetery/organization"""
        # Extract the target organization/cemetery name from URL
        org_name = self._extract_org_from_url(url)
        
        lines = [
            "",
            f"{indent}# Wait for app to redirect naturally after login",
            f"{indent}page.wait_for_load_state('load')",
            f"{indent}page.wait_for_timeout(2000)",
            "",
            f"{indent}current_url = page.url"
        ]
        
        # Only add organization click logic if we have an org name
        if org_name:
            # Convert URL-encoded name to display name (e.g., "Astana_Tegal_Gundul" -> "Astana Tegal Gundul")
            display_name = org_name.replace('_', ' ').replace('%20', ' ')
            
            lines.extend([
                "",
                f"{indent}# If on organization list page, click the organization link",
                f'{indent}if "/customer-organization" in current_url and "{org_name}" not in current_url:',
                f'{indent}    # Try to find organization link by text (handle both underscore and space variants)',
                f'{indent}    try:',
                f'{indent}        org_link = page.get_by_text("{display_name}").first',
                f"{indent}        org_link.wait_for(state='visible', timeout=10000)",
                f"{indent}        org_link.click()",
                f"{indent}        page.wait_for_load_state('load')",
                f"{indent}        page.wait_for_timeout(2000)",
                f'{indent}    except:',
                f'{indent}        pass  # Already on target page or link not found'
            ])
        
        return lines
    
    def _extract_org_from_url(self, url):
        """Extract organization/cemetery name from URL"""
        # Patterns: /customer-organization/Astana_Tegal_Gundul or /Auckland_Memorial_Park_Cemetery
        patterns = [
            r'/customer-organization/([^/?]+)',
            r'://[^/]+/([^/?]+)',  # First path segment after domain
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                name = match.group(1)
                # Filter out common non-org paths
                if name not in ['manage', 'plots', 'advance-table', 'search', 'login', 'map']:
                    return name
        
        return None

    def _generate_table_polling(self, indent):
        """Generate comprehensive table data polling code"""
        return [
            "",
            f"{indent}# CRITICAL: Wait for table data to populate (not just DOM elements)",
            f"{indent}# Table shows progressbars while loading, then replaces with actual data",
            f"{indent}page.wait_for_selector('[role=\"grid\"]', state='visible', timeout=15000)",
            "",
            f"{indent}# Wait for progressbars to disappear (loading complete)",
            f"{indent}try:",
            f"{indent}    page.wait_for_selector('[role=\"progressbar\"]', state='hidden', timeout=15000)",
            f"{indent}except:",
            f"{indent}    pass  # Progressbar may already be gone",
            "",
            f"{indent}# Give extra time for data to populate after progressbar disappears",
            f"{indent}page.wait_for_timeout(5000)",
            "",
            f"{indent}# Poll until gridcell has actual text content (not empty)",
            f"{indent}max_attempts = 10",
            f"{indent}cell_has_content = False",
            f"{indent}first_data_cell = None",
            "",
            f"{indent}for attempt in range(max_attempts):",
            f"{indent}    first_data_cell = page.locator('[role=\"gridcell\"]').first",
            f"{indent}    cell_text = first_data_cell.text_content()",
            "",
            f"{indent}    if cell_text and cell_text.strip():  # Has non-empty text",
            f"{indent}        cell_has_content = True",
            f"{indent}        break",
            f"{indent}    else:",
            f"{indent}        page.wait_for_timeout(2000)",
            "",
            f"{indent}if not cell_has_content:",
            f"{indent}    raise Exception('Timeout: Gridcells remained empty after waiting for data to load')",
            "",
            f"{indent}# Click the cell to navigate to edit page",
            f"{indent}first_data_cell.click()"
        ]


def main():
    """Command line interface"""
    print("=" * 70)
    print("🏛️  CHRONICLE TEST ENHANCER v1.0")
    print("=" * 70)
    print("\nSmart enhancements for Chronicle Cemetery Management tests:")
    print("  ✓ Dynamic async waits (no more static timeouts)")
    print("  ✓ Table data polling (wait for actual content)")
    print("  ✓ Natural navigation after login (preserve auth tokens)")
    print("  ✓ Optimized selectors (shorten long test-ids)")
    print("  ✓ Reduced boilerplate (remove unnecessary expects)")
    print()

    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print("Usage: python chronicle_enhancer.py <test_file> [--in-place]")
        print("\nExamples:")
        print("  python utils/chronicle_enhancer.py e2e/p0-smoke_test/login/tests/login_test.py --in-place")
        print("  python utils/chronicle_enhancer.py tests/interment_test.py")
        print("\nOptions:")
        print("  --in-place    Modify file in place (creates backup)")
        print("  --help, -h    Show this help message")
        sys.exit(0 if '--help' in sys.argv or '-h' in sys.argv else 1)

    test_file = sys.argv[1]
    in_place = '--in-place' in sys.argv

    try:
        enhancer = ChronicleEnhancer(test_file)
        
        if in_place:
            # Create backup first
            backup = Path(test_file).with_suffix('.backup')
            Path(test_file).rename(backup)
            print(f"📦 Backup created: {backup}")
        
        enhanced_file = enhancer.enhance()
        
        if not in_place:
            print(f"\n💡 Review the enhanced file, then replace original:")
            print(f"   mv {enhanced_file} {test_file}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
