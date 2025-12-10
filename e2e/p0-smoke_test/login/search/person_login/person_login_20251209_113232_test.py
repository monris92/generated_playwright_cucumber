import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("toolbar-a-mat-focus-indicator")).to_be_visible()
    expect(page.get_by_role("button", name="Marker").first).to_be_visible()

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
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_contain_text("Astana Tegal Gundul")
    expect(page.get_by_test_id("customer-organization-mat-panel-title-div-info").get_by_role("paragraph")).to_contain_text("Astana Tegal Gunduls")
    page.get_by_test_id("customer-organization-autocomplete-input-input-autocomplete-search-input").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-plots-records-annotation-h5-cemetery-name")).to_be_visible()
    page.get_by_test_id("customer-organization-autocomplete-input-input-autocomplete-search-input").click()
    page.get_by_test_id("customer-organization-autocomplete-input-input-autocomplete-search-input").fill("Anak Pertama Uno")
    expect(page.locator("cl-search-person-item")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-search-person-item-span-name").locator("span")).to_contain_text("Anak Pertama Uno")
    page.locator("cl-search-person-item").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20f201-plot-details-edit-div-main-title").get_by_text("B F")).to_be_visible()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"h3-person-full-name\"]")
    page.get_by_test_id("customer-organization-autocomplete-input-input-autocomplete-search-input").click()
    page.get_by_test_id("customer-organization-autocomplete-input-input-autocomplete-search-input").fill("Wahid")
    expect(page.locator("cl-search-person-item").filter(has_text="B F 2 1 / 1 Monumental Anak")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20f201-autocomplete-plots-persons-div-search-result")).to_contain_text("Wahid")
    expect(page.locator("cl-search-person-item").filter(has_text="B F 2 1 / 1 Monumental Anak")).to_be_visible()
    page.locator("cl-search-person-item").filter(has_text="B F 2 1 / 1 Monumental Anak").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-plots-b20f201-plot-details-edit-div-main-title").get_by_text("B F")).to_be_visible()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"h3-person-full-name\"]")
    page.wait_for_timeout(3000)
