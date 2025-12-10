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
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-button-mat-focus-indicator")).to_be_visible()
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
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    page.get_by_role("button", name="Advanced").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-advanced-search-form-div-title")).to_be_visible()
    expect(page.get_by_role("button", name="Interment", exact=True)).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-interment-form-div-title-deceased")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-form-field-input-john").click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-form-field-input-john").fill("budi")
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-form-field-input-doe").click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-form-field-input-doe").fill("wijaya")
    page.get_by_role("button", name="SEARCH").click()
    expect(page.get_by_role("heading", name="plots found...")).to_be_visible()
    expect(page.get_by_text("Budi Wijaya")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-span-plot-id-title")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-list").click()
    expect(page.get_by_text("B G 12 B. Wijaya")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-cemetery-name-wrapper").get_by_text("Astana Tegal Gundul")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20g2012-plot-details-edit-div-main-title").get_by_text("B G 12")).to_be_visible()
    expect(page.get_by_role("button", name="Budi Santoso Wijaya n/a - n/a")).to_be_visible()
