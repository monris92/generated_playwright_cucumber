import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://map.chronicle.rip/")
    page.get_by_role("button", name="Login").click()
    page.get_by_role("textbox", name="Email").click()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()
    expect(page.get_by_role("heading")).to_contain_text("Login to your account")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("faris+astanaorg@chronicle.rip")
    page.get_by_role("textbox", name="Email").press("Tab")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("12345")
    page.get_by_role("button", name="LOGIN").click()
    page.goto("https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul")
    expect(page.get_by_role("heading", name="Astana Tegal Gundul", exact=True)).to_be_visible()
    expect(page.locator("perfect-scrollbar")).to_contain_text("Private")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
