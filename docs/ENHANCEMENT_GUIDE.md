# Test Enhancement System

## Overview

The test enhancement system automatically fixes common issues in recorded Playwright tests.

## What It Fixes

### 1. **Login Flow Issues** ✅
- **Problem**: After clicking login, tests don't wait for page to load
- **Fix**: Automatically adds:
  ```python
  page.wait_for_load_state('load')
  page.wait_for_timeout(2000)  # Wait for dynamic content
  ```

### 2. **Redundant page.goto() After Login** ✅
- **Problem**: Recorded test has `page.goto()` after login, but page auto-navigates
- **Fix**: Converts to URL validation:
  ```python
  # Instead of: page.goto("https://example.com/dashboard")
  # Does this:
  page.wait_for_url("**/dashboard", timeout=15000)
  expect(page).to_have_url("https://example.com/dashboard")
  ```

### 3. **Element Visibility Waits** ✅
- **Problem**: Tests check elements before they're visible
- **Fix**: Adds wait before expect():
  ```python
  page.get_by_test_id("username").wait_for(state='visible', timeout=10000)
  expect(page.get_by_test_id("username")).to_contain_text("user@example.com")
  ```

## How To Use

### Option 1: Automatic (Integrated with simple_recorder.py)

When you record a test with `simple_recorder.py`, enhancement happens automatically:

```bash
python simple_recorder.py
```

The recorder will:
1. ✅ Record your test
2. ✅ **Auto-enhance** it with smart waits
3. ✅ Create test runner
4. ✅ Ready to run!

### Option 2: Manual Enhancement of Existing Tests

Enhance an existing test file:

```bash
# Create enhanced version (keeps original)
python test_enhancer.py tests/mytest.py

# Review the .enhanced.py file, then:
mv tests/mytest.enhanced.py tests/mytest.py
```

Or enhance in-place:

```bash
python test_enhancer.py tests/mytest.py --in-place
```

## Detection Rules

The enhancer uses smart pattern matching:

### Login Button Detection
Looks for `.click()` on elements with IDs/names containing:
- `login`
- `sign in` / `signin`
- `submit`
- `authenticate`

### URL Navigation Detection
After login click, checks if next line is `page.goto()`

## Example Transformation

**Before (Recorded):**
```python
def test_example(page: Page) -> None:
    page.goto("https://example.com/")
    page.get_by_test_id("login-button").click()
    page.goto("https://example.com/dashboard")
    expect(page.get_by_test_id("username")).to_contain_text("user@example.com")
```

**After (Enhanced):**
```python
def test_example(page: Page) -> None:
    page.goto("https://example.com/")
    page.get_by_test_id("login-button").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for automatic navigation (instead of manual goto)
    page.wait_for_url("**/dashboard", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)

    # Validate we're on the correct page
    expect(page).to_have_url("https://example.com/dashboard")

    # Wait for element to be visible
    page.get_by_test_id("username").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("username")).to_contain_text("user@example.com")
```

## Benefits

✅ **No more timing issues** - Tests wait properly for elements
✅ **Handles redirects** - Waits for automatic navigation
✅ **More reliable** - Tests pass consistently
✅ **Zero effort** - Works automatically with recorder

## When Manual Tweaks Are Still Needed

The enhancer handles most common cases, but you may still need to:

1. **Adjust timeout values** - Some sites are slower/faster
2. **Add custom waits** - For specific AJAX calls or animations
3. **Handle complex flows** - Multi-step wizards, modals, etc.

### 4. **Screenshot Capture** ✅
- **Feature**: Automatic screenshot capture during test execution
- **What you get**:
  - Screenshots at key test steps (when you call `screenshot()` fixture)
  - Auto-screenshot on test failure
  - All screenshots embedded in HTML report
  - Screenshots saved in `e2e/reports/screenshots/`

#### How to Use Screenshots

**In your test:**
```python
@pytest.mark.smoke
def test_example(page: Page, screenshot) -> None:
    page.goto("https://example.com/login")
    screenshot("01_login_page")  # Capture screenshot with custom name

    page.fill("#username", "user@example.com")
    page.fill("#password", "password")
    screenshot("02_credentials_filled")

    page.click("#login-button")
    screenshot("03_after_login")

    # On failure, screenshot is auto-captured!
```

**Screenshot Features:**
- ✅ **Auto-naming**: Screenshots include test name + custom label + timestamp
- ✅ **Full page**: Captures entire page, not just viewport
- ✅ **Auto-embed**: All screenshots appear in HTML report
- ✅ **Failure capture**: If test fails, screenshot is automatically taken
- ✅ **Organized**: All saved in `e2e/reports/screenshots/` directory

**Example filename:**
```
test_example[chromium]_01_login_page_20251111_135035.png
test_example[chromium]_failed_20251111_135035.png  # Auto-captured on failure
```

## Future Enhancements

Potential improvements:
- Detect AJAX calls and add network idle waits
- Handle modal dialogs automatically
- Detect file uploads/downloads
- Add retry logic for flaky elements
- Video recording on test failure
