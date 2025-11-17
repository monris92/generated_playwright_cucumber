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

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("PLOTS 186").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROIS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for element to be visible
    page.get_by_text("INTERMENTS 18").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("INTERMENTS 18")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD INTERMENTS").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="FILTER").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="EXPORT").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="EXPORT")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="ADD INTERMENTS").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()
    page.get_by_role("button", name="ADD INTERMENTS").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Add Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_text("AllPlot *").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("AllPlot *")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Deceased person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    page.get_by_text("AllPlot *").click(delay=200)

    # Wait for element to be visible
    page.get_by_text("A A 3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A A 3")).to_be_visible()
    page.get_by_text("A A 3").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("textbox", name="First name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("textbox", name="First name")).to_be_visible()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("kirito")

    # Wait for element to be visible
    page.get_by_role("textbox", name="Last name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("textbox", name="Last name")).to_be_visible()
    page.get_by_role("textbox", name="Last name").click()
    page.get_by_role("textbox", name="Last name").fill("wijaya")

    # Wait for element to be visible
    page.get_by_role("button", name="Interment details").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()
    expect(page.locator(".mat-form-field-infix.ng-tns-c122-985")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c183-986").click()

    # Wait for element to be visible
    page.get_by_text("Burial").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Burial")).to_be_visible()
    page.get_by_text("Burial").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("button", name="cancel").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="cancel")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="save").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save")).to_be_visible()
    page.get_by_role("button", name="save").click(delay=1000)
    page.goto("https://aus.chronicle.rip/customer-organization/advance-table?tab=interments")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_text("Data saved successfully").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Data saved successfully")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="A A 3").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="kirito").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("gridcell", name="wijaya", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
