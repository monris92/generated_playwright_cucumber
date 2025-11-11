"""
Global pytest configuration for E2E tests
Shared fixtures, hooks, and configurations
"""

import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
from pytest_html import extras


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
    """Hook to capture test execution status and attach screenshots"""
    outcome = yield
    rep = outcome.get_result()

    # Store report in item for access in fixtures
    setattr(item, f"rep_{rep.when}", rep)

    # Add screenshots to HTML report - must be done AFTER yield
    if rep.when == "call":
        # Get screenshots captured during test
        screenshots = getattr(item, "_screenshots", [])
        if screenshots:
            # Attach screenshots to report extras
            rep.extra = getattr(rep, "extra", []) + screenshots


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

    # Teardown - capture screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{test_name}_failed_{timestamp}.png"
        screenshot_path = Path(__file__).parent / "reports" / "screenshots" / screenshot_name

        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")

            # Attach screenshot to HTML report
            if not hasattr(request.node, "_screenshots_failure"):
                request.node._screenshots_failure = []
            relative_path = f"screenshots/{screenshot_name}"
            request.node._screenshots_failure.append(extras.image(relative_path))
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")

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
