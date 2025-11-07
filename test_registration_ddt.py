# test_registration_ddt.py
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# URL constant defined here for clarity, or in conftest if preferred
URL = "https://demoqa.com/automation-practice-form"


# --- Generic Interaction Class (Same as before) ---
class SeleniumActions:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def find_element(self, locator_value, by=By.ID):
        try:
            return self.wait.until(
                EC.presence_of_element_located((by, locator_value))
            )
        except TimeoutException:
            # In a pytest context, better to let the exception bubble up to fail the test
            raise

    def type_text(self, locator_value, text, by=By.ID):
        element = self.find_element(locator_value, by)
        if element:
            element.clear()
            element.send_keys(str(text))
            return True
        return False

    def click_element(self, locator_value, by=By.ID):
        element = self.wait.until(
            EC.element_to_be_clickable((by, locator_value))
        )
        # Using execute_script to ensure the element is clickable if obscured
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()


# --- Pytest Test Function ---

# The test uses the fixtures 'driver_setup' (for browser) and 'test_data' (for Excel row)
def test_form_registration(driver_setup, test_data):
    """
    Main test function. Pytest will execute this once for every row in the Excel sheet.
    """
    # Unpack the test_data tuple yielded by the fixture
    data_row, field_mappings = test_data

    # Initialize the browser helper class
    actions = SeleniumActions(driver_setup)

    # Navigate to the URL
    driver_setup.get(URL)

    print(f"\n--- Running Test Case: {data_row.get('FirstName')} {data_row.get('Lastname')} ---")

    try:
        # 1. Dynamic Input Filling Loop
        for excel_header, element_id in field_mappings.items():
            cell_value = data_row.get(excel_header)

            if cell_value is None:
                continue

            # Use the generic type_text method
            actions.type_text(element_id, cell_value, By.ID)
            print(f"  > Populated '{excel_header}' with: {cell_value}")

        # 2. Submit the form (Example: The actual submit ID)
        # actions.click_element("submit", By.ID)

        # 3. Assertion (Crucial for a successful test)
        # Example: Check if the submission confirmation modal appears.
        # confirmation_locator = (By.CLASS_NAME, "modal-header")
        # assert actions.find_element(confirmation_locator[1], confirmation_locator[0]), "Submission Modal did not appear."

        # Placeholder for a successful test print
        print("✅ Data entry complete. Add explicit assertion for final verification.")

    except Exception as e:
        # Pytest will automatically catch unhandled exceptions and mark the test as FAILED
        pytest.fail(f"Test case failed due to: {e}")