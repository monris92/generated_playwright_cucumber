import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-1").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADVANCED").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="3").nth(2).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="3").nth(2)).to_be_visible()
    page.get_by_role("button", name="3").nth(2).click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="Marker").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Marker")).to_be_visible()
    page.get_by_role("button", name="Marker").click(delay=200)
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    expect(page.locator("h3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADVANCED").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_role("button", name="ADVANCED").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-advanced-search-form-div-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-advanced-search-form-div-title")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Plot")).to_be_visible()
    page.get_by_role("button", name="Plot").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_test_id("auckland-memorial-park-cemetery-mat-form-field-input-number").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-mat-form-field-input-number")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("auckland-memorial-park-cemetery-mat-form-field-input-number").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("auckland-memorial-park-cemetery-mat-form-field-input-number").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_text("LVT").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("LVT")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("LVT").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("LVT").click(delay=200)
    page.locator(".mat-select-placeholder").first.click()
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()
    page.get_by_test_id("auckland-memorial-park-cemetery-mat-form-field-input-12").fill("12")

    # Wait for element to be visible
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click(delay=200)
    expect(page.locator("div").filter(has_text="LVT-J-12|Auckland Memorial").nth(3)).to_be_visible()
    page.locator("div").filter(has_text="LVT-J-12|Auckland Memorial").nth(3).click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery/plots/LVT-J-12?from=map&zoom=24&backTo=%2FAuckland_Memorial_Park_Cemetery%2Fsearch%2Fadvance")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_text("LVT-J-12 J. Chen").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("LVT-J-12 J. Chen")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-plots-lvt-j-12-plot-details-public-div-main-title").get_by_text("LVT-J-12").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-lvt-j-12-plot-details-public-div-main-title").get_by_text("LVT-J-12")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Jian Hong Chen 21/11/1927 -").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Jian Hong Chen 21/11/1927 -")).to_be_visible()
