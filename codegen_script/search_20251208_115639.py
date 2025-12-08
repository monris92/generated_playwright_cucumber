import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("autocomplete-base-routing-div-filter-content")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auck")
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    expect(page.get_by_test_id("search-cemetery-item-div-right")).to_contain_text("Auck")
    page.locator("cl-search-cemetery-item").click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_contain_text("Auckland Memorial Park & Cemetery")
