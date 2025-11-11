import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page, screenshot) -> None:
    page.goto("https://map.chronicle.rip/login")

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    screenshot("01_login_page_loaded")

    # Wait for element to be visible
    page.get_by_test_id("login-login-screen-h2-sign-in-text").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_contain_text("Login to your account")
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    page.get_by_test_id("login-mat-form-field-input-password").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    screenshot("02_credentials_filled")
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click()

    # Wait for navigation after login
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)  # Wait for dynamic content

    # Wait for automatic navigation (instead of manual goto)
    page.wait_for_url("**/customer-organization/Astana_Tegal_Gundul", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)

    # Validate we're on the correct page
    expect(page).to_have_url("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul")
    screenshot("03_logged_in_dashboard")

    # Wait for element to be visible
    page.get_by_role("button", name="Notifications").wait_for(state='visible', timeout=10000)
    expect(page.get_by_role("button", name="Notifications")).to_be_visible()

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-mat-panel-title-div-info").get_by_role("paragraph").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-mat-panel-title-div-info").get_by_role("paragraph")).to_contain_text("Astana Tegal Gunduls")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-mat-panel-title-span-username").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-mat-panel-title-span-username")).to_contain_text("faris+astanaorg@chronicle.rip")

    # Wait for element to be visible
    page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name").wait_for(state='visible', timeout=10000)
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_contain_text("Astana Tegal Gundul")
    screenshot("04_final_verification")
