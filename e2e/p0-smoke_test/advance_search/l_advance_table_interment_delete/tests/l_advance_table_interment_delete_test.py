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
    page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()

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
    page.get_by_test_id("login-login-screen-div-remember-me").locator("label").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-div-remember-me").locator("label")).to_be_visible()
    page.locator(".mat-checkbox-inner-container").click()

    # Wait for button to be ready and clickable
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-button-mat-focus-indicator")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
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
    page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_be_visible()

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
    page.get_by_text("PLOTS 186").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROIS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for element to be visible
    page.get_by_text("INTERMENTS 20").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("INTERMENTS 20")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="A A 3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="kirito").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="saputra", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="saputra", exact=True)).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="wijaya", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
    page.get_by_role("gridcell", name="A A 3").click()

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="Astana Tegal Gundul - A A").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - A A")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-interment-edit-form-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-interment-edit-form-span-edit-plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Deceased person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    page.get_by_role("button", name="Deceased person").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("textbox", name="First name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("textbox", name="First name")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)
    expect(page.locator(".cdk-overlay-backdrop")).to_be_visible()
    page.locator(".cdk-overlay-backdrop").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("button", name="Delete").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Delete")).to_be_visible()
    page.get_by_role("button", name="Delete").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Delete Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Delete Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="DELETE")).to_be_visible()
    page.get_by_role("button", name="DELETE").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="This plot is empty").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="This plot is empty")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-last-interment-dialog-button-no-option").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-last-interment-dialog-button-no-option")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-last-interment-dialog-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-last-interment-dialog-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("Would you like to keep the").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Would you like to keep the")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-last-interment-dialog-button-no-option").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Change to vacant").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("menuitem", name="Change to vacant")).to_be_visible()
    page.get_by_role("menuitem", name="Change to vacant").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("button", name="Delete").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Delete")).to_be_visible()
    page.get_by_role("button", name="Delete").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Delete Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Delete Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="DELETE")).to_be_visible()
    page.get_by_role("button", name="DELETE").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_test_id("not-found-not-found-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("not-found-not-found-button-mat-focus-indicator")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("not-found-not-found-button-mat-focus-indicator").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("not-found-not-found-button-mat-focus-indicator").click(delay=200)
