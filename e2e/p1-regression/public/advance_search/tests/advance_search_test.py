import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.regression
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Marker").first.wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Marker").first).to_be_visible()


    # Wait for button to be ready and clickable
    page.get_by_role("button", name="ADVANCED").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADVANCED")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="ADVANCED").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="ADVANCED").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("advanced-search-form-div-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("advanced-search-form-div-title")).to_be_visible()
    page.get_by_role("combobox", name="Cemeteries").locator("span").click()

    # Wait for element to be visible
    page.get_by_role("listbox", name="Cemeteries").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("listbox", name="Cemeteries")).to_be_visible()


    # Wait for button to be ready and clickable
    page.get_by_test_id("input-start-typing-to-search").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("input-start-typing-to-search")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("input-start-typing-to-search").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("input-start-typing-to-search").click(delay=200)
    page.get_by_test_id("input-start-typing-to-search").fill("auck")
    expect(page.locator("mat-pseudo-checkbox")).to_be_visible()
    page.locator("mat-pseudo-checkbox").click()
    page.get_by_role("combobox", name="Cemeteries Auckland Memorial").press("Escape")

    # Wait for button to be ready and clickable
    page.get_by_test_id("mat-form-field-input-john").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("mat-form-field-input-john")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("mat-form-field-input-john").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("mat-form-field-input-john").click(delay=200)
    page.get_by_test_id("mat-form-field-input-john").fill("a")

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="Deceased Person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased Person")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Deceased Person").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Deceased Person").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="plots found...").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("in 1 cemeteries").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("in 1 cemeteries")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("search-advance-advance-search-result-div-search-result").locator("div").filter(has_text="ROSEG-G-27|Auckland Memorial").first.wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("search-advance-advance-search-result-div-search-result").locator("div").filter(has_text="ROSEG-G-27|Auckland Memorial").first).to_be_visible()
