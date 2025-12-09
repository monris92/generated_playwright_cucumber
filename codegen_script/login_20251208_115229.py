import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_role("button", name="ADVANCED").click()
    expect(page.get_by_role("region", name="Deceased Person")).to_be_visible()

    page.get_by_role("combobox", name="Cemeteries").locator("span").click()
    expect(page.get_by_test_id("input-start-typing-to-search")).to_be_visible()
    page.get_by_test_id("input-start-typing-to-search").click()
    page.get_by_test_id("input-start-typing-to-search").fill("astana")
    page.get_by_test_id("button-button").click()
    expect(page.get_by_role("option", name="AVOCA - Roman Catholic")).to_be_visible()

    page.get_by_test_id("input-start-typing-to-search").click()
    page.get_by_role("option", name="AVOCA - Roman Catholic").locator("mat-pseudo-checkbox").click()
    expect(page.get_by_role("combobox", name="Cemeteries AVOCA - Roman")).to_be_visible()

    page.get_by_test_id("input-start-typing-to-search").click()
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()
    page.get_by_role("button", name="Deceased Person").click()
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click()
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()
