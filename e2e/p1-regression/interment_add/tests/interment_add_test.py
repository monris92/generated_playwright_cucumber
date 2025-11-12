import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.regression
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to fully load
    #page.wait_for_load_state('load')
    # page.wait_for_load_state('networkidle')
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_contain_text("Login to your account")
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click()

    # Wait for navigation after login
    #page.wait_for_load_state('load')
    # page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    page.get_by_test_id("login-mat-form-field-input-password").click()

    # Wait for navigation after login
#page.wait_for_load_state('load')
    # page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click()

    # Wait for navigation after login
#page.wait_for_load_state('load')
    # page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)  # Wait for dynamic content

    # Wait for automatic navigation (instead of manual goto)
    page.wait_for_url("**/customer-organization/Astana_Tegal_Gundul", timeout=15000)
#page.wait_for_load_state('load')
    # page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)

    # Validate we're on the correct page
    expect(page).to_have_url("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul")

    # Wait for element to be visible
    page.get_by_role("button", name="Notifications").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Notifications")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator")).to_contain_text("See all Plots")
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statistic-a-mat-focus-indicator").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-h3-1").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-h3-1")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator")).to_contain_text("FILTER")
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-perfect-scrollbar-button-mat-focus-indicator").click()
    expect(page.locator("label").filter(has_text="Vacant")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statuses-form-control-buttons").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-statuses-form-control-buttons")).to_contain_text("Vacant")
    page.locator("label").filter(has_text="Vacant").click()

    # Wait for button to be fully ready and clickable
    #page.wait_for_load_state('networkidle', timeout=10000)
    page.get_by_role("button", name="Done").wait_for(state='attached', timeout=10000)
    page.get_by_role("button", name="Done").wait_for(state='visible', timeout=10000)
    # Ensure button is enabled and not disabled
    expect(page.get_by_role("button", name="Done")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Done").scroll_into_view_if_needed()
    page.wait_for_timeout(500)  # Wait for any animations/transitions
    page.get_by_role("button", name="Done").click(delay=200)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-cdk-tree-node-button-toggle-a").click()

    # Wait for element to be visible
    page.get_by_text("A B 2 Vacant").wait_for(state='visible', timeout=10000)
    expect(page.get_by_text("A B 2 Vacant")).to_be_visible()
    page.get_by_text("A B 2 Vacant").click()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-plot-status")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-div-main-title").locator("span").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-div-main-title").locator("span")).to_contain_text("A B 2")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-add-interment-title").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-a20b202-plot-details-edit-span-add-interment-title")).to_contain_text("Add interment")

    # Wait for button to be fully ready and clickable
    #page.wait_for_load_state('networkidle', timeout=10000)
    page.get_by_role("button", name="Add interment").wait_for(state='attached', timeout=10000)
    page.get_by_role("button", name="Add interment").wait_for(state='visible', timeout=10000)
    # Ensure button is enabled and not disabled
    expect(page.get_by_role("button", name="Add interment")).to_be_enabled()
    # Scroll into view if needed
    page.get_by_role("button", name="Add interment").scroll_into_view_if_needed()
    page.wait_for_timeout(5000)  # Wait for any animations/transitions
    page.get_by_role("button", name="Add interment").click(delay=200)

    # Wait for element to be visible
    page.get_by_role("heading", name="Add Interment").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()
