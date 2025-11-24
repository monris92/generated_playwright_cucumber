import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-1").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADVANCED").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_role("button", name="ADVANCED").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("advanced-search-form-div-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("advanced-search-form-div-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()

    # Wait for element to be visible
    page.get_by_test_id("input-start-typing-to-search").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("input-start-typing-to-search")).to_be_visible()
    page.get_by_test_id("input-start-typing-to-search").click(delay=200)
    page.get_by_test_id("input-start-typing-to-search").fill("auck")

    # Wait for element to be visible
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    page.get_by_text("Auckland Memorial Park &").click(delay=200)
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()

    # Wait for element to be visible
    page.get_by_test_id("mat-form-field-input-john").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("mat-form-field-input-john")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-john").click(delay=200)
    page.get_by_test_id("mat-form-field-input-john").fill("jian")

    # Wait for element to be visible
    page.get_by_test_id("mat-form-field-input-doe").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("mat-form-field-input-doe")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-doe").click(delay=200)
    page.get_by_test_id("mat-form-field-input-doe").fill("chen")

    # Wait for element to be visible
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click(delay=200)

    # Wait for element to be visible
    page.get_by_text("Jian Chen").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Jian Chen")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
