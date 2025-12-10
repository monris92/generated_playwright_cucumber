import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-img-logo")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    page.get_by_test_id("login-mat-form-field-input-password").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    expect(page.locator(".mat-checkbox-inner-container")).to_be_visible()
    page.locator(".mat-checkbox-inner-container").click()
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)

    # Wait for app to redirect naturally after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)

    current_url = page.url

    # If on organization list page, click the organization link
    if "/customer-organization" in current_url and "Astana_Tegal_Gundul" not in current_url:
        # Try to find organization link by text (handle both underscore and space variants)
        try:
            org_link = page.get_by_text("Astana Tegal Gundul").first
            org_link.wait_for(state='visible', timeout=10000)
            org_link.click()
            page.wait_for_load_state('load')
            page.wait_for_timeout(2000)
        except:
            pass  # Already on target page or link not found
    expect(page.get_by_test_id("customer-organization-chronicle-admin-organization-toolbar-div-business-name-org")).to_be_visible()
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
    page.get_by_role("button", name="Tables").click()

    # Wait for navigation to tables page
    page.wait_for_url("**/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROIS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for tab content to load
    page.wait_for_url("**/advance-table?tab=interments**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_text("INTERMENTS 18")).to_be_visible()
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()
    expect(page.get_by_role("button", name="EXPORT")).to_be_visible()
    page.get_by_role("button", name="ADD INTERMENTS").click()

    # Wait for tab content to load
    page.wait_for_url("**/advance-table?tab=interments**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()
    expect(page.get_by_text("AllPlot *")).to_be_visible()
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    page.get_by_text("AllPlot *").click()
    page.get_by_text("A A 3").click()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("kirito")
    page.get_by_role("textbox", name="Last name").click()
    page.get_by_role("textbox", name="Last name").fill("wijaya")
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()
    expect(page.locator(".mat-form-field-infix.ng-tns-c122-985")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c183-986").click()
    page.get_by_text("Burial").click()
    expect(page.get_by_role("button", name="cancel")).to_be_visible()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="save").click()

    # Wait for navigation after click (don't force with page.goto())
    page.wait_for_url("**/customer-organization/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)

    # Dynamic wait for element to fully load
    page.get_by_text("Data saved successfully").wait_for(state='visible', timeout=15000)
    expect(page.get_by_text("Data saved successfully")).to_be_visible()
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
