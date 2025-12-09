import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_contain_text("Login to your account")
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").click()
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    page.get_by_test_id("login-mat-form-field-input-password").click()
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    page.get_by_test_id("login-login-screen-button-mat-focus-indicator").click()
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul")
    expect(page.get_by_role("button", name="Notifications")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-mat-panel-title-span-username")).to_contain_text("faris+astanaorg@chronicle.rip")
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
