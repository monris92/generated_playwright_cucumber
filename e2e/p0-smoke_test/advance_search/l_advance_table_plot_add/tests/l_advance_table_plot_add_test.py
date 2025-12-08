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
    page.get_by_test_id("login-login-screen-img-logo").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-img-logo")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("Or use Chronicle account").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Or use Chronicle account")).to_be_visible()

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
    page.get_by_role("button", name="Advanced").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Advanced")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Astana Tegal Gunduls faris+").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-side-menu-section-sectionId").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Tables").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Tables")).to_be_visible()
    page.get_by_role("button", name="Tables").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="FILTER").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD PLOT").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD PLOT")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("PLOTS 186").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("PLOTS 186")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD PLOT").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD PLOT")).to_be_visible()
    page.get_by_role("button", name="ADD PLOT").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Add plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Add plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-type-your-section-name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-type-your-section-name")).to_be_visible()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-type-your-section-name").click(delay=1000)

    # Wait for button to be ready and clickable
    page.get_by_text("A close").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A close")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("A close").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("A close").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element")).to_be_visible()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element").click(delay=1000)
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-mat-input-element").fill("Z")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number")).to_be_visible()
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number").click(delay=1000)
    page.get_by_test_id("customer-organization-advance-table-manage-add-plot-plot-add-div-plot-position").get_by_test_id("customer-organization-advance-table-manage-add-plot-mat-form-field-input-number").fill("1")
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()

    # Wait for button to be ready and clickable
    page.get_by_text("Occupied").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Occupied")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("Occupied").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("Occupied").click(delay=200)
    expect(page.locator(".mat-select-placeholder").first).to_be_visible()
    page.locator(".mat-select-placeholder").first.click()

    # Wait for button to be ready and clickable
    page.get_by_text("Cremation", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Cremation", exact=True)).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("Cremation", exact=True).scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("Cremation", exact=True).click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save")).to_be_visible()
    page.get_by_role("button", name="save").click(delay=1000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("A Z").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("A Z")).to_be_visible()
