import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.regression
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to fully load
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("toolbar-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_contain_text("Login to your account")
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    page.get_by_test_id("login-mat-form-field-input-password").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content

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
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statuses-form-control-buttons").get_by_text("Vacant").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statuses-form-control-buttons").get_by_text("Vacant").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statuses-form-control-buttons").get_by_text("Vacant")).to_be_visible()
    page.locator("label").filter(has_text="Vacant").click()
    page.get_by_role("button", name="Done").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-selected-filters-span-content")).to_contain_text("Status Vacant")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-cdk-tree-node-button-toggle-a").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-cdk-tree-node-button-toggle-a").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-cdk-tree-node-button-toggle-a")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-cdk-tree-node-button-toggle-a").click()
    page.get_by_text("A B 2 Vacant").click()

    # Wait for element to be visible
    page.get_by_role("button", name="Add interment").wait_for(state='visible', timeout=100000)

    # Wait for element to be visible
    page.get_by_role("button", name="Add interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Add interment")).to_be_visible()
    page.get_by_role("button", name="Add interment").click()

    # Wait for element to be visible
    page.get_by_role("heading", name="Add Interment").wait_for(state='visible', timeout=100000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Add Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-add-interment-interment-add-form-header-header").get_by_role("heading").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-add-interment-interment-add-form-header-header").get_by_role("heading").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-add-interment-interment-add-form-header-header").get_by_role("heading")).to_contain_text("Add Interment")
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("ahmad")
    page.get_by_role("textbox", name="Last name").click()
    page.get_by_role("textbox", name="Last name").fill("faris")

    # Wait for button to be ready
    page.wait_for_load_state('networkidle', timeout=10000)
    page.get_by_role("button", name="Deceased person").click().wait_for(state='visible', timeout=10000)
    page.wait_for_timeout(300)  # Small delay for animations
    page.get_by_role("button", name="Deceased person").click()

    # Wait for element to be visible
    page.get_by_role("combobox", name="Interment type").locator("span").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_role("combobox", name="Interment type").locator("span").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("combobox", name="Interment type").locator("span")).to_be_visible()
    page.get_by_role("combobox", name="Interment type").locator("span").click()

    # Wait for element to be visible
    page.get_by_text("Burial").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_text("Burial").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("Burial")).to_be_visible()
    page.get_by_text("Burial").click()
    page.get_by_role("button", name="save").click()
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul/plots/A%20B%202?from=map&zoom=24")

    # Wait for page to fully load
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-header-h3-person-full-name").locator("span").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-header-h3-person-full-name").locator("span").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-header-h3-person-full-name").locator("span")).to_contain_text("ahmad faris")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-button-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-mat-expansion-panel-button-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Interment").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_role("heading", name="Edit Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-interment-edit-form-span-edit-plot").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-interment-edit-form-span-edit-plot").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-interment-edit-form-span-edit-plot")).to_contain_text("A B 2")
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-toolbar-manage-div-more-btn-wrapper").get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-toolbar-manage-button-mat-focus-indicator").click()
    page.get_by_role("button", name="Delete").click()

    # Wait for element to be visible
    page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="DELETE")).to_be_visible()
    page.get_by_role("button", name="DELETE").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-last-interment-dialog-button-no-option").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-last-interment-dialog-button-no-option").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-last-interment-dialog-button-no-option")).to_be_visible()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20b202-manage-edit-interment-last-interment-dialog-button-no-option").click()

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Change to vacant").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_role("menuitem", name="Change to vacant").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("menuitem", name="Change to vacant")).to_be_visible()
    page.get_by_role("menuitem", name="Change to vacant").click()
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul/plots/A%20B%202?from=map&zoom=24")

    # Wait for page to fully load
    page.wait_for_load_state('load')
    page.wait_for_load_state('networkidle')

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status")).to_contain_text("VACANT")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-div-main-title").get_by_text("A B").wait_for(state='visible', timeout=10000)

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-div-main-title").get_by_text("A B").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-div-main-title").get_by_text("A B")).to_be_visible()
