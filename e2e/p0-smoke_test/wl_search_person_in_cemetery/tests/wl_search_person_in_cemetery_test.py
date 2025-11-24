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

    # Wait for button to be ready and clickable
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auck")

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="3").nth(2).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="3").nth(2)).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="3").nth(2).scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="3").nth(2).click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="Marker").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Marker")).to_be_visible()
    page.get_by_role("button", name="Marker").click(delay=200)
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for button to be ready and clickable
    page.get_by_test_id("autocomplete-base-routing-button-button").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-button-button")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("autocomplete-base-routing-button-button").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("autocomplete-base-routing-button-button").click(delay=200)
    expect(page.locator("h3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("jian chen")

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click(delay=200)
    page.locator("cl-search-record-item").click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery/plots/LVT-J-12?from=map&zoom=24&backTo=%2FAuckland_Memorial_Park_Cemetery")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-plots-lvt-j-12-plot-details-public-div-main-title").get_by_text("LVT-J-12").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-lvt-j-12-plot-details-public-div-main-title").get_by_text("LVT-J-12")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Jian Hong Chen 21/11/1927 -").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Jian Hong Chen 21/11/1927 -")).to_be_visible()
