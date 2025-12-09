import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("toolbar-nav-menu")).to_be_visible()

    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    expect(page.get_by_test_id("search-cemeteries-annotation-h5-scope")).to_be_visible()

    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
