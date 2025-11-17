import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Note: os and WebDriverWait imports are not strictly needed for this basic example,
# but can be kept if they are used elsewhere.

# 1. Define a fixture to handle the WebDriver setup and teardown
#    This ensures each test gets a fresh, independent driver instance.
@pytest.fixture
def browser():
    # Setup: Create a new driver instance for the test
    # Set up Chrome options if needed (e.g., headless mode)
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Uncomment for headless execution
    # chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Yield the driver instance to the test function
    yield driver

    # Teardown: Close the driver after the test completes
    driver.quit()


# 2. Corrected Test Function for Google
#    The test function now accepts the 'browser' fixture as an argument.
def test_google(browser):
    """Test to navigate to Google and print the title."""
    browser.get("https://www.google.com/")
    print(f"\nGoogle Title: {browser.title}")
    assert "Google" in browser.title


# 3. Corrected Test Function for Facebook
def test_facebook(browser):
    """Test to navigate to Facebook and print the title."""
    browser.get("https://www.facebook.com/")
    print(f"\nFacebook Title: {browser.title}")
    # Facebook's title often changes, asserting for the main site is safe
    assert "Facebook" in browser.title or "Log in" in browser.title


# 4. Corrected Test Function for Instagram
def test_instagram(browser):
    """Test to navigate to Instagram and print the title."""
    browser.get("https://www.instagram.com/")
    print(f"\nInstagram Title: {browser.title}")
    assert "Instagram" in browser.title