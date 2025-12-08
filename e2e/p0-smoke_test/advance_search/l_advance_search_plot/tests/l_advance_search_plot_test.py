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

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-mat-form-field-input-mat-input-element")).to_be_visible()
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click(delay=2000)

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")

    # Wait for element to be visible
    page.get_by_test_id("login-mat-form-field-input-password").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-mat-form-field-input-password")).to_be_visible()
    page.get_by_test_id("login-mat-form-field-input-password").click(delay=2000)

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-button-mat-focus-indicator")).to_be_visible()
    expect(page.locator(".mat-checkbox-inner-container")).to_be_visible()
    page.locator(".mat-checkbox-inner-container").click()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click(delay=2000)

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for automatic navigation (instead of manual goto)
    page.wait_for_url("**/customer-organization/Astana_Tegal_Gundul", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)

    # Validate we're on the correct page
    expect(page).to_have_url("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-chronicle-admin-organization-toolbar-div-business-name-org").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-chronicle-admin-organization-toolbar-div-business-name-org")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Astana Tegal Gunduls faris+").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Advanced").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Advanced")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    page.get_by_role("button", name="Advanced").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("textbox", name="Plot ID").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("textbox", name="Plot ID")).to_be_visible()
    page.get_by_role("textbox", name="Plot ID").click()
    page.get_by_role("textbox", name="Plot ID").fill("B G 12")

    # Wait for element to be visible
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_visible()
    page.get_by_role("button", name="SEARCH").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-span-name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-span-name")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("B G").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("B G")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="plots found...").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-list").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-list")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-list").click(delay=200)

    # Wait for element to be visible
    page.get_by_text("B G 12 B. Wijaya").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("B G 12 B. Wijaya")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-cemetery-name-wrapper").get_by_text("Astana Tegal Gundul").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-cemetery-name-wrapper").get_by_text("Astana Tegal Gundul")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-main-title").get_by_text("B G 12").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-main-title").get_by_text("B G 12")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Budi Santoso Wijaya n/a - n/a").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Budi Santoso Wijaya n/a - n/a")).to_be_visible()
