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
    expect(page.locator(".flex-box")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("PLOTS 186").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROIS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD INTERMENTS").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()

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
    page.get_by_role("button", name="Deceased person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Interment details").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Story").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Story")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Documents").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Documents")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("button", name="Move Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Move Interment")).to_be_visible()
    page.get_by_role("button", name="Move Interment").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-assign-plot-h4-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-assign-plot-h4-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder.ng-tns-c184-1022")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c184-1022").click()

    # Wait for button to be ready and clickable
    page.get_by_text("Astana Tegal Gundul", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Astana Tegal Gundul", exact=True)).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("Astana Tegal Gundul", exact=True).scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("Astana Tegal Gundul", exact=True).click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_text("AllPlot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("AllPlot")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("AllPlot").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("AllPlot").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search").click(delay=1000)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search").fill("A A")

    # Wait for element to be visible
    page.get_by_text("A A 4").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A A 4")).to_be_visible()
    page.get_by_text("A A 4").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="Assign").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Assign")).to_be_visible()
    page.get_by_role("button", name="Assign").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("gridcell", name="A A 4").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="A A 4")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="kirito").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="saputra", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="saputra", exact=True)).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="wijaya", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
    page.get_by_role("gridcell", name="A A 4").click()

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("heading", name="Astana Tegal Gundul - A A").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - A A")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-interment-edit-form-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-interment-edit-form-span-edit-plot")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Deceased person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Interment details").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Story").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Story")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Documents").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Documents")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("button", name="Move Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Move Interment")).to_be_visible()
    page.get_by_role("button", name="Move Interment").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-h4-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-h4-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder.ng-tns-c184-1535")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c184-1535").click()

    # Wait for element to be visible
    page.get_by_text("Astana Tegal Gundul", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Astana Tegal Gundul", exact=True)).to_be_visible()
    page.get_by_text("Astana Tegal Gundul", exact=True).click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All").click(delay=1000)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-input-start-typing-to-search").fill("A A")

    # Wait for element to be visible
    page.get_by_role("option", name="A A 4").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-mat-option-div-person-info").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("option", name="A A 4").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-mat-option-div-person-info")).to_be_visible()
    page.get_by_role("option", name="A A 4").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-mat-option-div-person-info").click()

    # Wait for element to be visible
    page.get_by_text("A A 4Plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A A 4Plot")).to_be_visible()
    page.locator("#mat-select-value-65").click()

    # Wait for element to be visible
    page.get_by_text("A A 3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A A 3")).to_be_visible()
    page.get_by_text("A A 3").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="Assign").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Assign")).to_be_visible()
    page.get_by_role("button", name="Assign").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("gridcell", name="A A 3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="kirito").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("saputra", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("saputra", exact=True)).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="wijaya", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
