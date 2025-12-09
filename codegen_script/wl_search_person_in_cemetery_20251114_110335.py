import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auck")
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_role("button", name="3").nth(2).click()
    expect(page.get_by_role("button", name="Marker")).to_be_visible()
    page.get_by_role("button", name="Marker").click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery")
    page.get_by_test_id("autocomplete-base-routing-button-button").click()
    expect(page.locator("h3")).to_be_visible()
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("jian chen")
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.locator("cl-search-record-item").click()
    page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery/plots/LVT-J-12?from=map&zoom=24&backTo=%2FAuckland_Memorial_Park_Cemetery")
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-lvt-j-12-plot-details-public-div-main-title").get_by_text("LVT-J-12")).to_be_visible()
    expect(page.get_by_role("button", name="Jian Hong Chen 21/11/1927 -")).to_be_visible()
