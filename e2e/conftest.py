"""
Global pytest configuration for E2E tests
Shared fixtures, hooks, and configurations
"""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
from pytest_html import extras
import base64


def pytest_addoption(parser):
    """Add CLI and ini options for screenshot behavior"""
    parser.addoption(
        "--screenshot-on-success",
        action="store_true",
        dest="screenshot_on_success",
        default=False,
        help="Capture screenshot when a test succeeds",
    )
    parser.addini(
        "screenshot_on_success",
        "Capture screenshot when a test succeeds (true/false)",
        default="false",
    )


# =============================================================================
# Pytest Hooks
# =============================================================================

def pytest_configure(config):
    """Configure pytest before test run"""
    # Ensure reports directory exists
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    # Ensure screenshots directory exists
    screenshots_dir = reports_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection"""
    # Add markers based on test location
    for item in items:
        test_path = Path(item.fspath)

        # Auto-add markers based on folder structure
        if "p0-smoke_test" in str(test_path):
            item.add_marker(pytest.mark.smoke)
        elif "p1-regression" in str(test_path):
            item.add_marker(pytest.mark.regression)
        elif "p2-exploratory" in str(test_path):
            item.add_marker(pytest.mark.exploratory)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status and attach screenshots."""
    outcome = yield
    rep = outcome.get_result()

    # Keep report reference on the item for fixtures
    setattr(item, f"rep_{rep.when}", rep)

    # Only act on the call phase
    if rep.when != "call":
        return

    extras_list = getattr(item, "_screenshots", []) or []

    # Check config/CLI for screenshot-on-success
    config = item.config
    try:
        enabled_cli = bool(config.getoption("screenshot_on_success"))
    except Exception:
        enabled_cli = False
    ini_val = config.getini("screenshot_on_success")
    enabled_ini = str(ini_val).lower() in ("1", "true", "yes")
    should_capture_on_success = enabled_cli or enabled_ini

    # Decide whether to capture now
    want_capture = False
    label = None
    if rep.failed:
        want_capture = True
        label = "failed"
    elif rep.passed and should_capture_on_success:
        want_capture = True
        label = "passed"

    if want_capture:
        page = item.funcargs.get("page") if "page" in item.funcargs else None
        if page is not None:
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{test_name}_{label}_{timestamp}.png"
            screenshot_path = Path(__file__).parent / "reports" / "screenshots" / screenshot_name
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"📸 Screenshot saved: {screenshot_path}")

                relative_path = f"screenshots/{screenshot_name}"
                extras_list.append(extras.image(relative_path))

                # Try embedding as base64 for reliability
                try:
                    with open(screenshot_path, "rb") as f:
                        img_bytes = f.read()
                    b64 = base64.b64encode(img_bytes).decode("ascii")
                    data_uri = f"data:image/png;base64,{b64}"
                    thumb_html = (
                        f'<a href="{data_uri}" target="_blank">'
                        f'<img src="{data_uri}" alt="{screenshot_name}" '
                        f'style="max-width:400px;border:1px solid #ddd;border-radius:4px;">'
                        f'</a>'
                        f'<div style="font-size:0.85em;color:#666;margin-top:4px;">{screenshot_name}</div>'
                    )
                    extras_list.append(extras.html(thumb_html))
                except Exception:
                    thumb_html = (
                        f'<a href="{relative_path}" target="_blank">'
                        f'<img src="{relative_path}" alt="{screenshot_name}" '
                        f'style="max-width:400px;border:1px solid #ddd;border-radius:4px;">'
                        f'</a>'
                        f'<div style="font-size:0.85em;color:#666;margin-top:4px;">{screenshot_name}</div>'
                    )
                    extras_list.append(extras.html(thumb_html))
            except Exception as e:
                print(f"❌ Failed to capture screenshot: {e}")

    if extras_list:
        rep.extra = getattr(rep, "extra", []) + extras_list


# =============================================================================
# Shared Fixtures
# =============================================================================

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application under test"""
    # Override this in individual test files or via command line
    return "https://map.chronicle.rip"


@pytest.fixture(scope="session")
def test_data_dir():
    """Directory for test data files"""
    return Path(__file__).parent / "test_data"


@pytest.fixture(autouse=True)
def test_setup_teardown(request, page: Page):
    """Setup and teardown for each test with screenshot capture"""
    # Setup
    test_name = request.node.name
    print(f"\n{'='*70}")
    print(f"Starting test: {test_name}")
    print(f"{'='*70}")

    yield

    # Teardown - capture screenshot on failure and optionally on success
    # Ensure unified screenshots list exists
    if not hasattr(request.node, "_screenshots"):
        request.node._screenshots = []

    def _capture_and_register(label: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{label}_{timestamp}.png"
        screenshot_path = Path(__file__).parent / "reports" / "screenshots" / screenshot_name
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")

            relative_path = f"screenshots/{screenshot_name}"
            request.node._screenshots.append(extras.image(relative_path))
            # Also embed the image as a base64 data URI so the report always shows inline
            try:
                with open(screenshot_path, "rb") as f:
                    img_bytes = f.read()
                b64 = base64.b64encode(img_bytes).decode("ascii")
                data_uri = f"data:image/png;base64,{b64}"

                thumb_html = (
                    f'<a href="{data_uri}" target="_blank">'
                    f'<img src="{data_uri}" alt="{screenshot_name}" '
                    f'style="max-width:400px;border:1px solid #ddd;border-radius:4px;">'
                    f'</a>'
                    f'<div style="font-size:0.85em;color:#666;margin-top:4px;">{screenshot_name}</div>'
                )
                request.node._screenshots.append(extras.html(thumb_html))
            except Exception as e:
                # If embedding fails, fall back to path-based thumbnail
                thumb_html = (
                    f'<a href="{relative_path}" target="_blank">'
                    f'<img src="{relative_path}" alt="{screenshot_name}" '
                    f'style="max-width:400px;border:1px solid #ddd;border-radius:4px;">'
                    f'</a>'
                    f'<div style="font-size:0.85em;color:#666;margin-top:4px;">{screenshot_name}</div>'
                )
                request.node._screenshots.append(extras.html(thumb_html))
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")
        

    # Always capture failure screenshots
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        _capture_and_register("failed")

    # Capture on success if enabled via CLI flag or pytest.ini
    enabled_cli = False
    try:
        enabled_cli = bool(request.config.getoption("screenshot_on_success"))
    except Exception:
        enabled_cli = False
    ini_val = request.config.getini("screenshot_on_success")
    enabled_ini = str(ini_val).lower() in ("1", "true", "yes")
    if hasattr(request.node, 'rep_call') and request.node.rep_call.passed and (enabled_cli or enabled_ini):
        _capture_and_register("passed")

    print(f"\n{'='*70}")
    print(f"Finished test: {test_name}")
    print(f"{'='*70}\n")


@pytest.fixture
def screenshot(request, page: Page):
    """Fixture to capture screenshots on demand during tests"""
    # Initialize screenshot list for this test
    if not hasattr(request.node, "_screenshots"):
        request.node._screenshots = []

    def _capture(name: str = None):
        test_name = request.node.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_{name or 'step'}_{timestamp}.png"
        screenshot_path = Path(__file__).parent / "reports" / "screenshots" / screenshot_name

        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot captured: {screenshot_name}")

            # Store screenshot for later attachment to HTML report
            relative_path = f"screenshots/{screenshot_name}"
            request.node._screenshots.append(extras.image(relative_path))
            # Add a clickable thumbnail that opens the full image in a new tab
            thumb_html = (
                f'<a href="{relative_path}" target="_blank">'
                f'<img src="{relative_path}" alt="{screenshot_name}" '
                f'style="max-width:400px;border:1px solid #ddd;border-radius:4px;">'
                f'</a>'
                f'<div style="font-size:0.85em;color:#666;margin-top:4px;">{screenshot_name}</div>'
            )
            request.node._screenshots.append(extras.html(thumb_html))

            return screenshot_path
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")
            return None

    return _capture


# =============================================================================
# Playwright Fixtures (if needed)
# =============================================================================

# Uncomment if you need custom browser configuration
#
# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     """Custom browser context arguments"""
#     return {
#         **browser_context_args,
#         "viewport": {"width": 1920, "height": 1080},
#         "ignore_https_errors": True,
#     }


# =============================================================================
# Helper Functions
# =============================================================================

def get_test_priority(test_path):
    """Get priority level from test path"""
    path_str = str(test_path)
    if "p0-smoke_test" in path_str:
        return "P0"
    elif "p1-regression" in path_str:
        return "P1"
    elif "p2-exploratory" in path_str:
        return "P2"
    return "Unknown"
