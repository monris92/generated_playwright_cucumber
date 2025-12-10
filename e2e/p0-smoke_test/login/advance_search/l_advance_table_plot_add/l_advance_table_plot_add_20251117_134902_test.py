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
    expect(page.get_by_text("Or use Chronicle account")).to_be_visible()
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
    expect(page.get_by_role("button", name="Advanced")).to_be_visible()
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    page.get_by_role("button", name="Tables").click()

    # Wait for navigation to tables page
    page.wait_for_url("**/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()
    expect(page.get_by_role("button", name="ADD PLOT")).to_be_visible()
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    page.get_by_role("button", name="ADD PLOT").click()
    expect(page.get_by_role("heading", name="Add plot")).to_be_visible()
    expect(page.get_by_role("button", name="save")).to_be_visible()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-type-your-section-name").click()
    page.get_by_text("A close").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element").fill("Z")
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number").fill("1")
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()
    page.get_by_text("Occupied").click()
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()
    page.get_by_text("Cremation", exact=True).click()
    page.get_by_role("button", name="save").click()
    expect(page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("A Z")).to_be_visible()
