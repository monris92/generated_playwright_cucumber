import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.regression
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-mat-form-field-input-mat-input-element")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click(delay=2000)

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")

    # Wait for button to be ready and clickable
    page.get_by_test_id("login-mat-form-field-input-password").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-mat-form-field-input-password")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("login-mat-form-field-input-password").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("login-mat-form-field-input-password").click(delay=2000)

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")

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
    page.get_by_role("button", name="Notifications").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Notifications")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="Advanced").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Advanced")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Advanced").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Advanced").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-advanced-search-form-div-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-advanced-search-form-div-title")).to_be_visible()
    page.get_by_role("combobox", name="Status").locator("span").click()
    page.get_by_role("option", name="Vacant").locator("mat-pseudo-checkbox").click()
    page.locator(".cdk-overlay-backdrop.cdk-overlay-transparent-backdrop").click()

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="Plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Plot")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Plot").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Plot").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-accordion-div-5").get_by_role("button", name="ROI").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-accordion-div-5").get_by_role("button", name="ROI")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-accordion-div-5").get_by_role("button", name="ROI").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("customer-organization-astana-tegal-gundul-mat-accordion-div-5").get_by_role("button", name="ROI").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="Interment", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Interment", exact=True)).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Interment", exact=True).scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Interment", exact=True).click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="SEARCH").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="SEARCH")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="SEARCH").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="SEARCH").click(delay=200)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-title")).to_be_visible()
    expect(page.locator(".photo").first).to_be_visible()
    expect(page.locator(".plot-label").first).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-result").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-advance-advance-search-result-div-search-result")).to_contain_text("Vacant")
    page.locator(".plot-label").first.click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status")).to_be_visible()

    # Wait for element to be visible
    page.get_by_role("button", name="Add interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Add interment")).to_be_visible()
    page.get_by_role("button", name="Add interment").click(delay=2000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Add Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("ahmad")
    page.get_by_role("textbox", name="Last name").click()
    page.get_by_role("textbox", name="Last name").fill("faris")

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="Deceased person").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Deceased person")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Deceased person").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Deceased person").click(delay=200)
    page.get_by_role("combobox", name="Interment type").locator("span").click()

    # Wait for button to be ready and clickable
    page.get_by_text("Burial").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Burial")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_text("Burial").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_text("Burial").click(delay=200)

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="save", exact=True).wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="save", exact=True)).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="save", exact=True).scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="save", exact=True).click(delay=1000)
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul/plots/A%20B%2010?from=map&zoom=24")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_text("INTERMENTS").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("INTERMENTS")).to_be_visible()
    page.locator(".ps__thumb-y").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-button-mat-focus-indicator")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-button-mat-focus-indicator")).to_contain_text("Edit interment")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-header-h3-person-full-name").locator("span").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-header-h3-person-full-name").locator("span")).to_contain_text("ahmad faris")
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-mat-expansion-panel-button-mat-focus-indicator").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-button-mat-focus-indicator")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click(delay=1000)

    # Wait for button to be ready and clickable - use more specific locator if needed
    page.get_by_role("button", name="Delete").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Delete")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Delete").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Delete").click(delay=2000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Delete Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Delete Interment")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="DELETE")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="DELETE").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="DELETE").click(delay=2000)

    # Wait for element to be visible
    page.get_by_role("heading", name="This plot is empty").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="This plot is empty")).to_be_visible()

    # Wait for button to be ready and clickable
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-last-interment-dialog-button-no-option").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-last-interment-dialog-button-no-option")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-last-interment-dialog-button-no-option").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b2010-manage-edit-interment-last-interment-dialog-button-no-option").click(delay=1000)

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Change to vacant").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("menuitem", name="Change to vacant")).to_be_visible()
    page.get_by_role("menuitem", name="Change to vacant").click()

    # Wait for element to be visible
    page.get_by_text("Interment record removed").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Interment record removed")).to_be_visible()
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul/plots/A%20B%2010?from=map&zoom=24")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b2010-plot-details-edit-span-plot-status")).to_contain_text("VACANT")
