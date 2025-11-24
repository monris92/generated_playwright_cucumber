import re
from playwright.sync_api import Page, expect


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

    # Wait for button to be ready and clickable
    page.get_by_test_id("input-start-typing-to-search").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("input-start-typing-to-search")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("input-start-typing-to-search").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("input-start-typing-to-search").click(delay=200)
    page.get_by_test_id("input-start-typing-to-search").fill("auckl")

    # Wait for element to be visible
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    page.get_by_text("Auckland Memorial Park &").click(delay=200)
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()

    # Wait for element to be visible
    page.get_by_role("button", name="Plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Plot")).to_be_visible()
    page.get_by_role("button", name="Plot").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("mat-form-field-input-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("mat-form-field-input-text")).to_be_visible()
    page.get_by_test_id("mat-form-field-input-text").click(delay=200)
    page.get_by_test_id("mat-form-field-input-text").fill("LVT")
    page.get_by_test_id("mat-form-field-input-text").click(delay=200)
    page.get_by_test_id("mat-form-field-input-text").fill("LVT-J-12")

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="SEARCH").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="SEARCH").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("search-advance-advance-search-result-span-name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("search-advance-advance-search-result-span-name")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="plots found...").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()
