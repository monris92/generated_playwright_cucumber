import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-img-logo")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-div-under-button").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-div-sign-up-info").get_by_test_id("login-login-screen-a-mat-focus-indicator")).to_be_visible()
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
    expect(page.locator(".mat-checkbox-inner-container")).to_be_visible()
    page.locator(".mat-checkbox-inner-container").click()
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
    expect(page.get_by_test_id("customer-organization-chronicle-admin-organization-toolbar-div-business-name-org")).to_be_visible()
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-h3-cemetery-name")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-perfect-scrollbar-button-mat-focus-indicator")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
    page.get_by_role("button", name="Tables").click()

    # Wait for navigation to tables page
    page.wait_for_url("**/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.locator(".flex-box")).to_be_visible()
    expect(page.get_by_text("PLOTS 186")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROIS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for tab content to load
    page.wait_for_url("**/advance-table?tab=interments**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()
    expect(page.get_by_role("gridcell", name="saputra", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()

    # CRITICAL: Wait for table data to populate (not just DOM elements)
    # Table shows progressbars while loading, then replaces with actual data
    page.wait_for_selector('[role="grid"]', state='visible', timeout=15000)

    # Wait for progressbars to disappear (loading complete)
    try:
        page.wait_for_selector('[role="progressbar"]', state='hidden', timeout=15000)
    except:
        pass  # Progressbar may already be gone

    # Give extra time for data to populate after progressbar disappears
    page.wait_for_timeout(5000)

    # Poll until gridcell has actual text content (not empty)
    max_attempts = 10
    cell_has_content = False
    first_data_cell = None

    for attempt in range(max_attempts):
        first_data_cell = page.locator('[role="gridcell"]').first
        cell_text = first_data_cell.text_content()

        if cell_text and cell_text.strip():  # Has non-empty text
            cell_has_content = True
            break
        else:
            page.wait_for_timeout(2000)

    if not cell_has_content:
        raise Exception('Timeout: Gridcells remained empty after waiting for data to load')

    # Click the cell to navigate to edit page
    first_data_cell.click()
    page.wait_for_timeout(1000)
    page.get_by_role("gridcell", name="A A 3").click()

    # Wait for navigation to edit page
    page.wait_for_url("**/manage/edit/**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - A A")).to_be_visible()
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()
    expect(page.get_by_role("button", name="Story")).to_be_visible()
    expect(page.get_by_role("button", name="Documents")).to_be_visible()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"div-more-btn-wrapper\"]")
    page.get_by_role("button", name="Move Interment").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-assign-plot-h4-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder.ng-tns-c184-1022")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c184-1022").click()
    page.get_by_text("Astana Tegal Gundul", exact=True).click()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"form-assign-id-form\"]")
    page.get_by_text("AllPlot").click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search").click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a203-manage-edit-interment-input-start-typing-to-search").fill("A A")
    page.get_by_text("A A 4").click()
    page.get_by_role("button", name="Assign").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    expect(page.get_by_role("gridcell", name="A A 4")).to_be_visible()
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()
    expect(page.get_by_role("gridcell", name="saputra", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()

    # CRITICAL: Wait for table data to populate (not just DOM elements)
    # Table shows progressbars while loading, then replaces with actual data
    page.wait_for_selector('[role="grid"]', state='visible', timeout=15000)

    # Wait for progressbars to disappear (loading complete)
    try:
        page.wait_for_selector('[role="progressbar"]', state='hidden', timeout=15000)
    except:
        pass  # Progressbar may already be gone

    # Give extra time for data to populate after progressbar disappears
    page.wait_for_timeout(5000)

    # Poll until gridcell has actual text content (not empty)
    max_attempts = 10
    cell_has_content = False
    first_data_cell = None

    for attempt in range(max_attempts):
        first_data_cell = page.locator('[role="gridcell"]').first
        cell_text = first_data_cell.text_content()

        if cell_text and cell_text.strip():  # Has non-empty text
            cell_has_content = True
            break
        else:
            page.wait_for_timeout(2000)

    if not cell_has_content:
        raise Exception('Timeout: Gridcells remained empty after waiting for data to load')

    # Click the cell to navigate to edit page
    first_data_cell.click()
    page.wait_for_timeout(1000)
    page.get_by_role("gridcell", name="A A 4").click()

    # Wait for navigation to edit page
    page.wait_for_url("**/manage/edit/**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()
    expect(page.get_by_role("heading", name="Astana Tegal Gundul - A A")).to_be_visible()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"form-span-edit-plot\"]")
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()
    expect(page.get_by_role("button", name="Story")).to_be_visible()
    expect(page.get_by_role("button", name="Documents")).to_be_visible()
    # Optimized selector (original too long)
    page.locator("[data-testid*=\"div-more-btn-wrapper\"]")
    page.get_by_role("button", name="Move Interment").click()
    expect(page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-h4-title")).to_be_visible()
    expect(page.locator(".mat-select-placeholder.ng-tns-c184-1535")).to_be_visible()
    page.locator(".mat-select-placeholder.ng-tns-c184-1535").click()
    page.get_by_text("Astana Tegal Gundul", exact=True).click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-assign-plot-form-assign-id-form").get_by_text("All").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-input-start-typing-to-search").fill("A A")
    page.get_by_role("option", name="A A 4").get_by_test_id("customer-organization-astana-tegal-gundul-a20a204-manage-edit-interment-mat-option-div-person-info").click()
    expect(page.get_by_text("A A 4Plot")).to_be_visible()
    page.locator("#mat-select-value-65").click()
    page.get_by_text("A A 3").click()
    page.get_by_role("button", name="Assign").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
    expect(page.get_by_role("gridcell", name="A A 3")).to_be_visible()
    expect(page.get_by_role("gridcell", name="kirito")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-advance-table-mat-sidenav-content-div-table-wrapper").get_by_text("saputra", exact=True)).to_be_visible()
    expect(page.get_by_role("gridcell", name="wijaya", exact=True)).to_be_visible()
