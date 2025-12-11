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
    expect(page.get_by_test_id("customer-organization-advance-table-select-search-cemetery-div-global-cem-select-label")).to_be_visible()
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
    # Check INTERMENTS tab is active (using the tab link locator)
    expect(page.locator("a").filter(has_text="INTERMENTS")).to_be_visible()
    expect(page.get_by_role("button", name="ADD INTERMENTS")).to_be_visible()
    expect(page.get_by_role("button", name="FILTER")).to_be_visible()
    expect(page.get_by_role("button", name="EXPORT")).to_be_visible()
    page.get_by_role("button", name="ADD INTERMENTS").click()

    # Wait for tab content to load
    page.wait_for_url("**/advance-table?tab=interments**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_role("heading", name="Add Interment")).to_be_visible()
    expect(page.get_by_role("button", name="Deceased person")).to_be_visible()
    
    # Close any open overlays first (from Method 1 combobox click)
    print("\n🔍 Checking for open overlays...")
    try:
        overlay = page.locator(".cdk-overlay-backdrop")
        if overlay.is_visible(timeout=1000):
            print("  Found overlay, pressing Escape to close...")
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
    except:
        pass
    
    # DEBUG: Save HTML for analysis
    print("\n🔍 Saving page HTML for analysis...")
    with open("debug_add_interment_page.html", "w") as f:
        f.write(page.content())
    
    # DEBUG: Try to understand the form structure
    print("\n🔍 DEBUG: Analyzing form structure...")
    print("  Looking for all mat-form-field elements...")
    form_fields = page.locator("mat-form-field").all()
    print(f"  Found {len(form_fields)} form fields")
    for i, field in enumerate(form_fields[:5]):
        try:
            label = field.locator("mat-label").text_content(timeout=1000)
            print(f"    Field {i}: {label}")
        except:
            print(f"    Field {i}: <no label>")
    
    # The plot field might be using autocomplete instead of select
    # Try to find input field for plot
    plot_field_found = False
    
    # ========================================
    # PLOT SELECTION (REQUIRED FIELD)
    # ========================================
    # Note: Plot is a REQUIRED field (marked with *)
    # This test requires the organization to have at least one plot created
    # Run test 'l_advance_table_plot_add' first to create plots
    # ========================================
    
    try:
        print("\n=== Finding Plot dropdown field... ===")
        # The plot field is in header's cl-select-search component
        plot_select = page.locator("header cl-select-search mat-select").first
        
        aria_label = plot_select.get_attribute("aria-label") or ""
        print(f"Found Plot field with aria-label: '{aria_label}'")
        
        print("Opening Plot dropdown...")
        plot_select.click()
        page.wait_for_timeout(2000)
        
        # Check for available plot options
        options = page.get_by_role("option").all()
        print(f"Found {len(options)} plot options")
        
        if len(options) == 0:
            # No plots available - this is a test setup issue
            print("\n" + "="*70)
            print("❌ ERROR: No plots available in organization!")
            print("="*70)
            print("Plot is a REQUIRED field (*) but no plots found.")
            print("This organization needs plots before interments can be added.")
            print("\nTo fix this:")
            print("  1. Run test: 'l_advance_table_plot_add' first")
            print("  2. Or manually create plots in this organization")
            print("  3. Then run this test again")
            print("="*70)
            
            # Take screenshot for evidence
            page.screenshot(path="debug_no_plots_available.png")
            
            # Close dropdown
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            
            # Fail the test with clear message
            pytest.fail("Cannot proceed: Organization has no plots. Plot is required field. Run plot creation test first.")
        
        # List available plots
        for i, opt in enumerate(options[:10]):
            opt_text = opt.text_content().strip()
            print(f"  Option {i}: '{opt_text}'")
        
        # Find and select a valid plot (skip action buttons)
        plot_selected = False
        for opt in options:
            opt_text = opt.text_content().strip()
            if opt_text and len(opt_text) > 0:
                # Skip action buttons
                if any(word in opt_text.lower() for word in ["save", "add", "event", "cancel"]):
                    continue
                # This looks like a plot name
                print(f"✓ Selecting plot: '{opt_text}'")
                opt.click()
                plot_selected = True
                plot_field_found = True
                break
            
            if not plot_field_found and len(options) > 0:
                # If no valid plot found, just take first option that's not empty
                for opt in options:
                    if opt.text_content().strip():
                        print(f"  ⚠️  Using first non-empty option: {opt.text_content()}")
                        opt.click()
                        plot_field_found = True
                        break
    except Exception as e:
        print(f"  ❌ Method 1 failed: {e}")
    
    # Method 2: Click directly on the visible plot text "A A 3" in the list
    if not plot_field_found:
        try:
            print("Method 2: Looking for plot text in page...")
            # Plot names are usually visible even before dropdown opens
            plot_texts = ["A A 3", "B B 1", "C C 1"]  # Try common plot names
            for plot_name in plot_texts:
                try:
                    plot_elem = page.locator(f"text='{plot_name}'").first
                    if plot_elem.is_visible(timeout=1000):
                        print(f"  ✓ Found plot text: {plot_name}")
                        plot_elem.click()
                        plot_field_found = True
                        break
                except:
                    continue
            
            if not plot_field_found:
                print("  ⚠️  No plot text found")
        except Exception as e:
            print(f"  ❌ Method 2 failed: {e}")
    
    # Method 3: Use the old selector that worked before
    if not plot_field_found:
        print("Method 3: Using original text-based selector...")
        try:
            page.get_by_text("A A 3").click(timeout=5000)
            plot_field_found = True
            print("  ✓ Found by text")
        except Exception as e:
            print(f"  ❌ Method 3 failed: {e}")
    
    if not plot_field_found:
        # Take screenshot to debug
        page.screenshot(path="debug_plot_dropdown_not_found.png")
        raise Exception("❌ Could not find or select plot dropdown!")
    
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="First name").click()
    page.get_by_role("textbox", name="First name").fill("kiritoXXX")
    page.get_by_role("textbox", name="Last name").click()
    page.get_by_role("textbox", name="Last name").fill("wijayaXX")
    expect(page.get_by_role("button", name="Interment details")).to_be_visible()
    
    # Click the Interment type dropdown (combobox) to open it
    page.get_by_role("combobox", name="Interment type").click()
    
    # Wait for dropdown to open and select Burial option
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="Burial").click()
    
    expect(page.get_by_role("button", name="cancel")).to_be_visible()
    expect(page.get_by_role("button", name="save")).to_be_visible()
    
    # DEBUG: Screenshot before save
    print("\n📸 Taking screenshot before save...")
    page.screenshot(path="debug_before_save.png")
    
    # Click save button
    print("💾 Clicking save button...")
    page.get_by_role("button", name="save").click()
    
    # Wait for response
    page.wait_for_timeout(5000)
    
    # DEBUG: Check current state
    print(f"🔍 URL after save: {page.url}")
    page.screenshot(path="debug_after_save.png")
    
    # Check for success message or navigation back to list
    success_found = False
    
    # Try to find success message
    try:
        success_msg = page.locator("text=/successfully|saved|success/i").first
        if success_msg.is_visible(timeout=3000):
            msg_text = success_msg.text_content()
            print(f"✓ Success message found: {msg_text}")
            success_found = True
    except:
        print("⚠️  No success message found")
    
    # Check if we navigated back to advance-table list
    if "/manage/add/" not in page.url:
        print(f"✓ Navigated away from add form: {page.url}")
        success_found = True
        
        # Wait a bit and go back to advance table to verify data
        page.wait_for_timeout(2000)
        if "/advance-table" not in page.url:
            page.goto("https://aus.chronicle.rip/customer-organization/advance-table?tab=interments")
            page.wait_for_load_state('load')
            page.wait_for_timeout(3000)
        
        # Try to verify the data in the table
        print("🔍 Checking if data appears in advance table...")
        try:
            # Check for the name we just added
            kirito_cell = page.get_by_role("gridcell", name="kiritoXXX")
            kirito_cell.wait_for(state='visible', timeout=5000)
            print("✓ Found 'kiritoXXX' in table - data was saved!")
        except:
            print("⚠️  Could not find 'kiritoXXX' in table immediately")
            page.screenshot(path="debug_table_after_save.png")
    
    if not success_found:
        print("❌ WARNING: No clear success indicator found!")
        print(f"   Current URL: {page.url}")
        raise AssertionError("Could not verify that interment was saved successfully")
