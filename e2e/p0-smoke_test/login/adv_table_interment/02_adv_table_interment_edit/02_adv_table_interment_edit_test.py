import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(20000)
    expect(page.get_by_test_id("toolbar-a-1")).to_be_visible()
    expect(page.get_by_test_id("autocomplete-base-routing-div-search-field")).to_be_visible()
    expect(page.get_by_role("button", name="ADVANCED")).to_be_visible()
    expect(page.get_by_test_id("toolbar-a-about-chronicle")).to_be_visible()
    page.get_by_test_id("toolbar-a-mat-focus-indicator").click()
    expect(page.get_by_test_id("login-login-screen-img-logo")).to_be_visible()
    expect(page.get_by_test_id("login-login-screen-h2-sign-in-text")).to_be_visible()
    expect(page.get_by_text("Or use Chronicle account")).to_be_visible()
    page.wait_for_timeout(20000)
    expect(page.locator("div").filter(has_text=re.compile(r"^Email \*$"))).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Email \*$")).click()
    page.get_by_test_id("login-mat-form-field-input-mat-input-element").fill("faris+astanaorg@chronicle.rip")
    expect(page.locator("div").filter(has_text=re.compile(r"^Password \*$"))).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Password \*$")).click()
    page.get_by_test_id("login-mat-form-field-input-password").fill("12345")
    page.get_by_test_id("login-login-screen-div-remember-me").get_by_text("Remember me").click()

    # Wait for navigation after login - let app redirect naturally
    # Don't use page.goto() after login as it can invalidate auth tokens
    page.wait_for_load_state('load')
    page.wait_for_timeout(3000)
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
    expect(page.get_by_test_id("customer-organization-autocomplete-base-routing-div-search-field")).to_be_visible()
    expect(page.get_by_role("button", name="Advanced")).to_be_visible()
    expect(page.get_by_role("button", name="Astana Tegal Gunduls faris+")).to_be_visible()
    expect(page.get_by_test_id("customer-organization-side-menu-section-sectionId")).to_be_visible()
    page.get_by_role("button", name="Tables").click()
    page.wait_for_timeout(2000)

    # Wait for navigation to tables page
    page.wait_for_url("**/advance-table**", timeout=500000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()
    expect(page.get_by_role("button", name="EXPORT")).to_be_visible()
    expect(page.get_by_role("button", name="ADD PLOT")).to_be_visible()
    expect(page.locator("a").filter(has_text="BUSINESS")).to_be_visible()
    expect(page.locator("a").filter(has_text="PERSONS")).to_be_visible()
    expect(page.locator("a").filter(has_text="ROISX")).to_be_visible()
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    page.locator("a").filter(has_text="INTERMENTS").click()

    # Wait for tab content to load
    page.wait_for_url("**/advance-table?tab=interments**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()
    expect(page.get_by_role("button", name="EXPORT")).to_be_visible()
    page.get_by_role("button", name="FILTER").click()
    expect(page.get_by_test_id("customer-organization-advance-table-mat-dialog-container-h2-mat-dialog-title")).to_be_visible()
    expect(page.locator("div").filter(has_text=re.compile(r"^Section$")).nth(2)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Section$")).nth(2).click()
    page.get_by_role("option", name="A").click()
    expect(page.locator("div").filter(has_text=re.compile(r"^Row$")).nth(2)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Row$")).nth(2).click()
    page.get_by_placeholder("Row").fill("z")
    page.get_by_role("button", name="APPLY").click()
    expect(page.get_by_role("gridcell", name="A Z")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Kirito")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Kazuto")).to_be_visible()

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
    page.get_by_role("gridcell", name="Kirito").click()

    # Wait for navigation to edit page
    page.wait_for_url("**/manage/edit/**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)
    expect(page.get_by_role("heading", name="Edit Interment")).to_be_visible()
    expect(page.get_by_text("Create certificate")).to_be_visible()
    page.get_by_role("button", name="Deceased person").click()
    expect(page.locator("div").filter(has_text=re.compile(r"^Title$")).nth(2)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Title$")).nth(2).click()
    page.get_by_role("textbox", name="Title").fill("Mr")
    page.wait_for_timeout(5000)
    expect(page.locator('[formcontrolname="gender"]')).to_be_visible()
    page.locator('[formcontrolname="gender"]').click()
    page.get_by_role("option", name="Male", exact=True).click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Interment details").click()
    expect(page.locator("div").filter(has_text=re.compile(r"^Unit$")).nth(1)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Unit$")).nth(1).click()
    page.get_by_role("option", name="Centimeters (cm)").click()
    page.wait_for_timeout(5000)
    expect(page.locator("div").filter(has_text=re.compile(r"^Interment depth$")).nth(2)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Interment depth$")).nth(2).click()
    page.get_by_role("spinbutton", name="Interment depth").fill("40")
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="interment applicant").click()
    page.get_by_test_id("customer-organization-astana-tegal-gundul-a20z201-manage-edit-interment-interment-edit-form-div-applicant-dropdown").get_by_text("Person").click()
    expect(page.locator("div").filter(has_text=re.compile(r"^First name \*$")).nth(5)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^First name \*$")).nth(5).click()
    expect(page.locator("div").filter(has_text=re.compile(r"^Last name \*$")).nth(5)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Last name \*$")).nth(5).click()
    page.get_by_role("textbox", name="Last name").fill("wijaya")
    page.wait_for_timeout(5000)
    expect(page.locator("div").filter(has_text=re.compile(r"^Last name \*$")).nth(5)).to_be_visible()
    page.locator("div").filter(has_text=re.compile(r"^Last name \*$")).nth(5).click()
    page.get_by_role("textbox", name="Last name").fill("wijaya")
    page.get_by_text("Budi Santoso WijayaJl.").click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="next of kin").click()
    page.locator("div").filter(has_text=re.compile(r"^Last name \*$")).nth(5).click()
    page.get_by_role("textbox", name="Last name").fill("pratama")
    page.get_by_text("Agus Setiawan PratamaJl.").click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="funeral minister").click()
    page.get_by_role("textbox", name="Business name").fill("mas")
    page.get_by_text("Masjid Raya BandungJl. Dago").click()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="funeral director").click()
    page.get_by_role("textbox", name="Business name").fill("rumah duka")
    page.get_by_text("Rumah Duka SejahteraJl. Gatot").click()
    page.wait_for_timeout(5000)
    expect(page.get_by_role("listitem").filter(has_text="Interment ApplicantBapak Budi")).to_be_visible()
    expect(page.get_by_role("listitem").filter(has_text="Next of kinBapak Agus")).to_be_visible()
    expect(page.get_by_role("listitem").filter(has_text="Funeral ministerMasjid Raya")).to_be_visible()
    expect(page.get_by_role("listitem").filter(has_text="Funeral directorRumah Duka")).to_be_visible()
    page.get_by_role("button", name="save").click()

    # Wait for navigation after click (don't force with page.goto())
    page.wait_for_url("**/customer-organization/advance-table**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)

    # Dynamic wait for element to fully load
    page.get_by_role("gridcell", name="A Z").wait_for(state='visible', timeout=15000)
    expect(page.get_by_role("gridcell", name="A Z")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Kirito")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Kazuto")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Male")).to_be_visible()
    expect(page.get_by_role("gridcell", name="40")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Budi Santoso Wijaya")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Agus Setiawan Pratama")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Rumah Duka Sejahtera")).to_be_visible()
    expect(page.get_by_role("gridcell", name="Masjid Raya Bandung")).to_be_visible()
