import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auckland")
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_text("Auckland Memorial Park &").click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
