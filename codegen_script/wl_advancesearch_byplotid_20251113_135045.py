import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_role("button", name="ADVANCED").click()
    expect(page.get_by_test_id("advanced-search-form-div-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()
    page.get_by_test_id("input-start-typing-to-search").click()
    page.get_by_test_id("input-start-typing-to-search").fill("auckl")
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    page.get_by_text("Auckland Memorial Park &").click()
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()
    expect(page.get_by_role("button", name="Plot")).to_be_visible()
    page.get_by_role("button", name="Plot").click()
    expect(page.get_by_test_id("mat-form-field-input-text")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-text").click()
    page.get_by_test_id("mat-form-field-input-text").fill("LVT")
    page.get_by_test_id("mat-form-field-input-text").click()
    page.get_by_test_id("mat-form-field-input-text").fill("LVT-J-12")
    page.get_by_role("button", name="SEARCH").click()
    expect(page.get_by_test_id("search-advance-advance-search-result-span-name")).to_be_visible()
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()
