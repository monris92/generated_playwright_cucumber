import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("toolbar-nav-menu")).to_be_visible()

    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
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
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_be_visible()
    page.get_by_role("button", name="Tables").click()

    # Wait for navigation to tables page
    page.wait_for_url("**/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    page.locator("a").filter(has_text="PERSONS").click()
    page.get_by_role("button", name="ADD PERSON").click()
    expect(page.get_by_test_id("customer-organization-advance-table-manage-add-person-person-add-h1-title-page")).to_be_visible()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-person-person-add-div-page-content").click(button="right")
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("ahmadXxX")
    page.get_by_role("textbox", name="First name").press("Tab")
    page.get_by_role("textbox", name="Last name").fill("faris")
    page.get_by_role("textbox", name="Title").click()
    page.get_by_role("textbox", name="Title").fill("mr")
    page.get_by_role("combobox", name="Gender").locator("span").click()
    expect(page.get_by_text("Female")).to_be_visible()
    page.get_by_text("Male", exact=True).click()
    expect(page.get_by_role("combobox", name="Gender Male")).to_be_visible()

    page.get_by_role("textbox", name="Phone (mobile)").click()
    page.get_by_role("textbox", name="Phone (mobile)").fill("+628962626")
    page.get_by_role("textbox", name="Phone (mobile)").click()
    page.get_by_role("textbox", name="Phone (mobile)").fill("+6289626261")
    page.get_by_role("textbox", name="Phone (home)").click()
    page.get_by_role("textbox", name="Phone (home)").fill("+6289626262")
    page.get_by_role("textbox", name="Phone (office)").click()
    page.get_by_role("textbox", name="Phone (office)").fill("+6289626263")
    page.get_by_test_id("customer-organization-advance-table-manage-add-person-mat-form-field-input-email").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-person-mat-form-field-input-email").fill("faris@chronicle.rip")
    page.get_by_test_id("customer-organization-advance-table-manage-add-person-mat-form-field-input-add-notes").click()
    page.get_by_test_id("customer-organization-advance-table-manage-add-person-mat-form-field-input-add-notes").fill("notes baru")
    with page.wait_api_response("api/v1/adv_table/interments/"):
        page.get_by_role("button", name="save").click()
    expect(page.get_by_role("gridcell", name="ahmadXxX")).to_be_visible()
    expect(page.get_by_role("grid")).to_contain_text("faris")
