import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auckland")

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("Auckland Memorial Park &").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("Auckland Memorial Park &").click(delay=200)
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
