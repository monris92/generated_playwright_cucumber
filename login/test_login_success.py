import pytest
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

# Set working directory to ensure proper path resolution
os.chdir(Path(__file__).parent)

# Import step definitions - CRITICAL for test execution
from features.steps.login_success_steps import *

# Load scenarios for login_success feature - using relative path from current working dir
scenarios('features/login_success/login_success.feature')

@pytest.fixture(scope="session")
def browser():
    """Create browser instance"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        yield browser
        browser.close()

@pytest.fixture(scope="function") 
def context(browser):
    """Create browser context"""
    context = browser.new_context()
    context.grant_permissions([])
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """Create new page"""
    page = context.new_page()
    yield page
    page.close()
