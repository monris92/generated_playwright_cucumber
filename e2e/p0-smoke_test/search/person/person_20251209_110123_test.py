import re
from playwright.sync_api import Page, expect
import pytest


@pytest.mark.smoke
def test_example(page: Page) -> None:
    page.goto("https://map.chronicle.rip/")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("auck")
    expect(page.get_by_text("Auck", exact=True)).to_be_visible()
    expect(page.get_by_test_id("search-cemetery-item-div-right")).to_contain_text("Auckland Memorial Park & Cemetery")
    page.wait_for_timeout(1000)
    page.locator("cl-search-cemetery-item").click()

    # Wait for navigation after click (don't force with page.goto())
    page.wait_for_url("**/Auckland_Memorial_Park_Cemetery**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)

    # Dynamic wait for element to fully load
    page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3").wait_for(state='visible', timeout=15000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").locator("h3")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-perfect-scrollbar-div-cemetery-detail-header").get_by_role("paragraph")).to_contain_text("Public")
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-search-plots-records-annotation-h5-cemetery-name")).to_be_visible()

    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("Carlos Jay Humphris")
    expect(page.locator("cl-search-record-item")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-search-record-item-span-name").locator("span")).to_contain_text("Carlos Jay Humphris")
    page.wait_for_timeout(1000)
    page.locator("cl-search-record-item").click()

    # Wait for navigation after click (don't force with page.goto())
    page.wait_for_url("**/Auckland_Memorial_Park_Cemetery/plots/HLA2-L-11**", timeout=15000)
    page.wait_for_load_state('load')
    page.wait_for_timeout(1000)

    # Dynamic wait for element to fully load
    page.get_by_text("Auckland Memorial Park &").wait_for(state='visible', timeout=15000)
    expect(page.get_by_text("Auckland Memorial Park &")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-hla2-l-11-mat-expansion-panel-header-h3-person-full-name").locator("span")).to_contain_text("Carlos Jay Humphris")
    page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").click()
    
    # Wait for search API response
    with page.wait_api_response("v1_search_plots-records-persons_list"):
        page.get_by_test_id("autocomplete-base-routing-input-autocomplete-search-input").fill("HLA2-L-12")
    
    expect(page.locator("cl-search-plot-item")).to_be_visible()
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-hla2-l-11-search-plot-item-span-title").locator("span")).to_contain_text("HLA2-L-12")
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-hla2-l-11-search-plot-item-span-plot-label")).to_contain_text("Reserved")
    page.locator("cl-search-plot-item").click()

    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-hla2-l-11-plot-details-public-div-main-title").get_by_text("HLA2-L-")).to_be_visible()
    # page.goto("https://map.chronicle.rip/Auckland_Memorial_Park_Cemetery/plots/HLA2-L-12?from=map&zoom=24&backTo=%2FAuckland_Memorial_Park_Cemetery%2Fplots%2FHLA2-L-11%3Ffrom%3Dmap%26zoom%3D24")

    # Wait for page to load
    page.wait_for_load_state('load')
    page.wait_for_timeout(2000)
    expect(page.get_by_test_id("auckland-memorial-park-cemetery-plots-hla2-l-12-plot-details-public-span-plot-status")).to_contain_text("RESERVED")
