import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input")).to_be_visible()
    expect(page.get_by_role("button", name="Marker").first).to_be_visible()

    page.get_by_role("button", name="ADVANCED").click()
    expect(page.get_by_test_id("advanced-search-form-div-title")).to_be_visible()
    page.get_by_role("combobox", name="Cemeteries").locator("span").click()
    expect(page.get_by_role("listbox", name="Cemeteries")).to_be_visible()

    page.get_by_test_id("input-start-typing-to-search").click()
    page.get_by_test_id("input-start-typing-to-search").fill("auck")
    expect(page.locator("mat-pseudo-checkbox")).to_be_visible()
    page.locator("mat-pseudo-checkbox").click()
    page.get_by_role("combobox", name="Cemeteries Auckland Memorial").press("Escape")
    page.get_by_test_id("mat-form-field-input-john").click()
    page.get_by_test_id("mat-form-field-input-john").fill("a")
    page.get_by_role("button", name="Deceased Person").click()
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click()
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()
    expect(page.get_by_text("in 1 cemeteries")).to_be_visible()
    expect(page.get_by_test_id("search-advance-advance-search-result-div-search-result").locator("div").filter(has_text="ROSEG-G-27|Auckland Memorial").first).to_be_visible()
