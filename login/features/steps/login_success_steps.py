from playwright.sync_api import expect
from pytest_bdd import given, when, then
import pytest
import re
@given("User navigates to 'https://map.chronicle.rip/'")
def navigate_to_website(page):
    page.goto('https://map.chronicle.rip/')
    page.wait_for_load_state('networkidle')
@when("User clicks 'Login'")
def click_login(page):
    page.get_by_role('button', name='Login').click()
    page.wait_for_timeout(1000)
@then("'Login to your account' should be visible'")
def verify_login_heading(page):
    try:
        expect(page.get_by_role('heading', name='Login to your account')).to_be_visible()
    except:
        page.wait_for_timeout(1500)
        expect(page.get_by_role('heading', name='Login to your account')).to_be_visible()
@when("User enters 'faris+astanaorg@chronicle.rip' in the Email box")
def enter_email(page):
    page.get_by_role('textbox', name='Email').click()
    page.get_by_role('textbox', name='Email').fill('faris+astanaorg@chronicle.rip')
    page.get_by_role('textbox', name='Email').press('Tab')
    page.wait_for_timeout(1000)
@when("User enters '12345' in the Password box")
def enter_password(page):
    page.get_by_role('textbox', name='Password').click()
    page.get_by_role('textbox', name='Password').fill('12345')
    page.wait_for_timeout(1000)
@when("User clicks 'LOGIN'")
def click_login_button(page):
    page.get_by_role('button', name='LOGIN').click()
    page.wait_for_timeout(5000)
@then("User navigates to 'https://aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul'")
def navigate_to_customer_organization(page):
    expect(page).to_have_url(re.compile(r'.*aus.chronicle.rip/customer-organization/Astana_Tegal_Gundul.*'))
@then("'Astana Tegal Gundul' should be visible")
def verify_astana_tegal_gundul(page):
    try:
        expect(page.get_by_role('heading', name='Astana Tegal Gundul', exact=True)).to_be_visible()
    except:
        page.wait_for_timeout(1500)
        expect(page.get_by_role('heading', name='Astana Tegal Gundul', exact=True)).to_be_visible()
@then("'Private' should be visible")
def verify_private_text(page):
    try:
        expect(page.locator('perfect-scrollbar')).to_contain_text('Private')
    except:
        page.wait_for_timeout(1500)
        expect(page.locator('perfect-scrollbar')).to_contain_text('Private')