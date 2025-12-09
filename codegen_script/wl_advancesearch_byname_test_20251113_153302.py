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
    expect(page.get_by_test_id("input-start-typing-to-search")).to_be_visible()
    page.get_by_test_id("input-start-typing-to-search").click()
    page.get_by_test_id("input-start-typing-to-search").fill("auck")
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    page.get_by_text("Auckland Memorial Park &").click()
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()
    expect(page.get_by_test_id("mat-form-field-input-john")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-john").click()
    page.get_by_test_id("mat-form-field-input-john").fill("jian")
    expect(page.get_by_test_id("mat-form-field-input-doe")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-doe").click()
    page.get_by_test_id("mat-form-field-input-doe").fill("chen")
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click()
    expect(page.get_by_text("Jian Chen")).to_be_visible()
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
