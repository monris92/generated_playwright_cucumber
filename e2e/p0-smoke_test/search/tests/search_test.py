import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page, screenshot) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    screenshot("01_home_page_loaded")

    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auck")
    screenshot("02_search_query_entered")

    # Wait for element to be visible
    page.get_by_text("Auck", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auck", exact=True)).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("search-cemetery-item-div-right").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("search-cemetery-item-div-right")).to_contain_text("Auck")
    screenshot("03_search_results_displayed")

    # Click on first search result (more reliable than specific index)
    page.locator('[data-testid*="search-cemetery-item-img"]').first.click()

    # Wait for navigation after click
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for automatic navigation (instead of manual goto)
    page.wait_for_url("**/Auckland_Memorial_Park_Cemetery", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)

    # Validate we're on the correct page
    expect(page).to_have_url("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")
    screenshot("04_detail_page_loaded")

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_contain_text("Auckland Memorial Park & Cemetery")

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-ng-component-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-ng-component-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("auckland-memorial-park-cemetery-ng-component-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-ng-component-button-mat-focus-indicator")).to_contain_text("CREATE AN ONLINE MEMORIAL")
    screenshot("05_final_verification")
