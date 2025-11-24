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
    page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()

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
    page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-side-menu-section-sectionId").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Tables").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Tables")).to_be_visible()
    page.get_by_role("button", name="Tables").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD PLOT").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD PLOT")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="B G 13").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="B G 13")).to_be_visible()
    page.get_by_role("gridcell", name="B G 13").click()

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Edit Plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="Astana Tegal Gundul - B G").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - B G")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Edit Plot Id").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("menuitem", name="Edit Plot Id")).to_be_visible()
    page.get_by_role("menuitem", name="Edit Plot Id").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-h4-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-h4-title")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").click(delay=1000)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").fill("14")

    # Wait for element to be visible
    page.get_by_role("button", name="Save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Save")).to_be_visible()
    page.get_by_role("button", name="Save").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Warning").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Warning")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Proceed").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Proceed")).to_be_visible()
    page.get_by_role("button", name="Proceed").click(delay=1000)

    # Wait for element to be visible
    page.get_by_text("Your changes have been").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Your changes have been")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save")).to_be_visible()
    page.get_by_role("button", name="save").click(delay=1000)
    page.goto("https://aus.chronicle.rip/customer-organization/advance-table?tab=plots")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_text("Data saved successfully").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Data saved successfully")).to_be_visible()

    # Wait for button to be ready and clickable - use more specific locator if needed
    page.get_by_role("button", name="Close").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Close")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Close").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Close").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("gridcell", name="B G 14").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="B G 14")).to_be_visible()
    page.get_by_role("gridcell", name="B G 14").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="Astana Tegal Gundul - B G").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - B G")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-13").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-13")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Edit Plot Id").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("menuitem", name="Edit Plot Id")).to_be_visible()
    page.get_by_role("menuitem", name="Edit Plot Id").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-h4-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-h4-title")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Number$")).nth(2)).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").click(delay=1000)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-change-plot-id-form-plot-id-form").get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-mat-form-field-input-number").fill("13")

    # Wait for element to be visible
    page.get_by_role("button", name="Save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Save")).to_be_visible()
    page.get_by_role("button", name="Save").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Warning").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Warning")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Proceed").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Proceed")).to_be_visible()
    page.get_by_role("button", name="Proceed").click(delay=1000)

    # Wait for element to be visible
    page.get_by_text("Your changes have been").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Your changes have been")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-manage-edit-plot-plot-edit-span-edit-plot")).to_be_visible()

    # Wait for button to be ready and clickable - use more specific locator if needed
    page.get_by_role("button", name="Close").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Close")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Close").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Close").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save")).to_be_visible()
    page.get_by_role("button", name="save").click(delay=1000)
    page.goto("https://aus.chronicle.rip/customer-organization/advance-table?tab=plots")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_text("Data saved successfully").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Data saved successfully")).to_be_visible()
