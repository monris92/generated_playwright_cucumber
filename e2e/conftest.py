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
from contextlib import contextmanager


# =============================================================================
# Page Helper Extensions
# =============================================================================

@contextmanager
def wait_api_response(page: Page, endpoint: str, timeout: int = 10000):
    """
    Helper to wait for specific API endpoint response.
    
    Usage:
        with page.wait_api_response("v1_search_plots-records-persons_list"):
            page.get_by_test_id("search-input").fill("search term") << ini adalah aksi sebelum validasi element yang akan di validasi.
        page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    
    ## contoh penggunaan actual :
    # Wait for search API response
    with page.wait_api_response("v1_search_plots-records-persons_list"):
        page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("HLA2-L-12")
    
    expect(page.locator("cl-search-plot-item")).to_be_visible()


    Args:
        page: Playwright Page object
        endpoint: Part of the API endpoint URL to wait for
        timeout: Timeout in milliseconds (default: 10000)
    """
    with page.expect_response(lambda r: endpoint in r.url, timeout=timeout):
        yield


# Monkey-patch the Page class to add convenience method
def _wait_api_response(self, endpoint: str, timeout: int = 10000):
    """
    Convenience method for waiting on API responses.
    
    Usage:
        with page.wait_api_response("v1_search_plots-records-persons_list"):
            page.get_by_test_id("search-input").fill("search term")
    """
    return wait_api_response(self, endpoint, timeout)

Page.wait_api_response = _wait_api_response






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
            # request.node._screenshots.append(extras.image(relative_path)) -- REMOVED to avoid duplication
            # Also embed the image as a base64 data URI so the report always shows inline
            try:
                with open(screenshot_path, "rb") as f:
                    img_bytes = f.read()
                b64 = base64.b64encode(img_bytes).decode("ascii")
                data_uri = f"data:image/png;base64,{b64}"

                thumb_html = get_thumb_html(data_uri, screenshot_name)
                request.node._screenshots.append(extras.html(thumb_html))
            except Exception as e:
                # If embedding fails, fall back to path-based thumbnail
                thumb_html = get_thumb_html(relative_path, screenshot_name)
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
            # request.node._screenshots.append(extras.image(relative_path)) -- REMOVED to avoid duplication
            
            # Add a clickable thumbnail that opens the modal
            # We need to know the index for the gallery
            current_count = len(request.node._screenshots)
            
            thumb_html = get_gallery_thumb_html(relative_path, screenshot_name, current_count)
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

    return "Unknown"


# =============================================================================
# HTML Report Customization
# =============================================================================

def pytest_html_results_table_header(cells):
    """Add Screenshots column to the HTML report"""
    cells.insert(2, "<th>Screenshots</th>")

def pytest_html_results_table_row(report, cells):
    """Add screenshots to the row"""
    if hasattr(report, "user_properties"):
        # Extract screenshots from user_properties if available
        # Note: pytest-html might not automatically pass extra to user_properties in all versions
        # So we might need to rely on the 'extra' attribute if we can access it here,
        # but standard hook signature only gives 'report' and 'cells'.
        # 'report' object should have 'extra' attribute if we populated it in makereport.
        pass
    
    # Create the cell content
    # We'll use a custom attribute on the report object that we populate in makereport
    screenshots_html = getattr(report, "screenshots_html", "")
    cells.insert(2, f'<td class="col-screenshots">{screenshots_html}</td>')

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

    # Collect all screenshots captured during the test
    # These are stored in item._screenshots as a list of html strings (thumbnails)
    # We want to aggregate them into a gallery
    
    screenshots = getattr(item, "_screenshots", []) or []
    
    # Check config/CLI for screenshot-on-success
    config = item.config
    try:
        enabled_cli = bool(config.getoption("screenshot_on_success"))
    except Exception:
        enabled_cli = False
    ini_val = config.getini("screenshot_on_success")
    enabled_ini = str(ini_val).lower() in ("1", "true", "yes")
    should_capture_on_success = enabled_cli or enabled_ini

    # Decide whether to capture final state now
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
                
                # Embed as base64
                try:
                    with open(screenshot_path, "rb") as f:
                        img_bytes = f.read()
                    b64 = base64.b64encode(img_bytes).decode("ascii")
                    data_uri = f"data:image/png;base64,{b64}"
                    
                    # Create a thumbnail for the gallery
                    thumb_html = get_gallery_thumb_html(data_uri, screenshot_name, len(screenshots))
                    screenshots.append(thumb_html)
                except Exception:
                    thumb_html = get_gallery_thumb_html(relative_path, screenshot_name, len(screenshots))
                    screenshots.append(thumb_html)
            except Exception as e:
                print(f"❌ Failed to capture screenshot: {e}")

    # Now format the screenshots for the report cell
    if screenshots:
        # Create a container for the gallery
        gallery_id = f"gallery-{item.nodeid.replace('/', '-').replace(':', '-').replace('.', '-')}"
        
        # Ensure all items are strings
        formatted_screenshots = []
        for s in screenshots:
            if isinstance(s, str):
                formatted_screenshots.append(s)
            elif isinstance(s, dict) and 'content' in s:
                formatted_screenshots.append(s['content'])
            elif hasattr(s, 'content'): # Handle object case if pytest-html changes
                formatted_screenshots.append(s.content)
            else:
                formatted_screenshots.append(str(s))

        # We'll create a horizontal scrollable container
        gallery_html = f"""
        <div class="screenshot-gallery" id="{gallery_id}" style="display: flex; overflow-x: auto; gap: 10px; max-width: 300px;">
            {''.join(formatted_screenshots)}
        </div>
        """
        rep.screenshots_html = gallery_html
        
        # Also add to extra for compatibility if needed, but we are using custom column
        # rep.extra = getattr(rep, "extra", []) + [extras.html(gallery_html)]
    else:
        rep.screenshots_html = ""


def get_gallery_thumb_html(src, alt, index):
    """Generate HTML for a gallery item"""
    # We'll use a simple onclick to open a larger view
    # The larger view logic is in the CSS/JS injected via assets (if possible) 
    # or we can inline it here.
    
    # Let's reuse the modal logic but make it better for "geser2" (sliding)
    # actually, the user wants to see history in the report.
    # A simple horizontal scroll of thumbnails that open a modal is good.
    
    onclick_js = (
        "var modal = document.getElementById('myModal');"
        "var modalImg = document.getElementById('img01');"
        "if (!modal) {"
            # Create modal if it doesn't exist (lazy init)
            "var d=document;"
            "var m=d.createElement('div');m.id='myModal';m.className='modal';"
            "m.style.cssText='display:none;position:fixed;z-index:9999;left:0;top:0;width:100%;height:100%;overflow:auto;background-color:rgba(0,0,0,0.9);';"
            "var c=d.createElement('span');c.className='close';c.innerHTML='&times;';"
            "c.style.cssText='position:absolute;top:15px;right:35px;color:#f1f1f1;font-size:40px;font-weight:bold;cursor:pointer;';"
            "c.onclick=function(){m.style.display='none'};m.appendChild(c);"
            
            "var i=d.createElement('img');i.className='modal-content';i.id='img01';"
            "i.style.cssText='margin:auto;display:block;max-width:90%;max-height:90vh;position:relative;top:50%;transform:translateY(-50%);';"
            "m.appendChild(i);"
            
            # Add navigation buttons for "geser2"
            "var prev=d.createElement('a');prev.innerHTML='&#10094;';"
            "prev.style.cssText='cursor:pointer;position:absolute;top:50%;width:auto;padding:16px;margin-top:-50px;color:white;font-weight:bold;font-size:20px;transition:0.6s ease;border-radius:0 3px 3px 0;user-select:none;-webkit-user-select:none;left:0;';"
            "m.appendChild(prev);"
            
            "var next=d.createElement('a');next.innerHTML='&#10095;';"
            "next.style.cssText='cursor:pointer;position:absolute;top:50%;width:auto;padding:16px;margin-top:-50px;color:white;font-weight:bold;font-size:20px;transition:0.6s ease;border-radius:3px 0 0 3px;user-select:none;-webkit-user-select:none;right:0;';"
            "m.appendChild(next);"

            "d.body.appendChild(m);"
            
            "m.onclick=function(e){if(e.target===m)m.style.display='none'};"
            
            # Logic to handle navigation
            "window.currentImgIndex = 0;"
            "window.galleryImages = [];"
            
            "window.showModal = function(src, galleryId, index) {"
                "var g = document.getElementById(galleryId);"
                "window.galleryImages = Array.from(g.getElementsByTagName('img')).map(img => img.src);"
                "window.currentImgIndex = index;"
                "m.style.display='block';"
                "i.src = src;"
            "};"
            
            "window.changeImg = function(n) {"
                "window.currentImgIndex += n;"
                "if (window.currentImgIndex >= window.galleryImages.length) {window.currentImgIndex = 0;}"
                "if (window.currentImgIndex < 0) {window.currentImgIndex = window.galleryImages.length - 1;}"
                "i.src = window.galleryImages[window.currentImgIndex];"
            "};"
            
            "prev.onclick = function() { window.changeImg(-1); };"
            "next.onclick = function() { window.changeImg(1); };"
            
            # Keyboard navigation
            "document.addEventListener('keydown', function(e) {"
                "if (m.style.display === 'block') {"
                    "if (e.key === 'ArrowLeft') { window.changeImg(-1); }"
                    "if (e.key === 'ArrowRight') { window.changeImg(1); }"
                    "if (e.key === 'Escape') { m.style.display = 'none'; }"
                "}"
            "});"
        "}"
        
        # Call the show function
        f"window.showModal(this.querySelector('img').src, this.parentElement.id, {index});"
    )

    return (
        f"""<div onclick="{onclick_js}" style="cursor:pointer;display:inline-block;flex:0 0 auto;">"""
        f"""<img src="{src}" alt="{alt}" class="thumb-img" """
        f"""style="height:50px;width:auto;border:1px solid #ddd;border-radius:4px;object-fit:cover;">"""
        f"""</div>"""
    )
