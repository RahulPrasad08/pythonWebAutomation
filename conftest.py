# conftest.py
import os

import pytest
import openpyxl
# ... other utility imports ...

# CORE SELENIUM IMPORTS
from selenium import webdriver # <--- MUST BE PRESENT AND CORRECT
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# conftest.py


# Constants for data file
FILE_PATH = r"D:\Python\DataDriven\Login.xlsx"
SHEET_NAME = "Registration"
# Define the mapping between Excel Header Names and Web Element Locators (By.ID)
FIELD_MAPPINGS = {
    "FirstName": "firstName",
    "Lastname": "lastName",
    "Email": "userEmail",
    # Add other fields as needed
}


def get_excel_data():
    """
    Reads the data from the Excel file and returns a list of dictionaries,
    where each dictionary represents one test case (row of data).
    """
    try:
        workbook = openpyxl.load_workbook(FILE_PATH)
        sheet = workbook[SHEET_NAME]
    except FileNotFoundError:
        pytest.fail(f"Data file not found at: {FILE_PATH}")
    except KeyError:
        pytest.fail(f"Sheet '{SHEET_NAME}' not found in the workbook.")

    data_iterator = iter(sheet.values)

    try:
        # 1. Extract the Header Row and convert tuple to list for easier indexing
        header_row = list(next(data_iterator))
    except StopIteration:
        pytest.fail("Sheet is empty.")

    test_cases = []

    # 2. Iterate through data rows
    for row_values in data_iterator:
        # Create a dictionary: {Header: Value, ...} for the row
        test_data = dict(zip(header_row, row_values))

        # Simple validation: ensure a necessary field isn't empty
        if not test_data.get("FirstName"):
            print("Skipping row: FirstName is empty.")
            continue

        # Filter the data to only include columns we care about in the mappings
        filtered_data = {
            header: value
            for header, value in test_data.items()
            if header in FIELD_MAPPINGS
        }

        test_cases.append((filtered_data, FIELD_MAPPINGS))

    if not test_cases:
        pytest.fail("No valid test data rows found.")

    return test_cases


@pytest.fixture(params=get_excel_data())
def test_data(request):
    """Pytest fixture that yields test data for each row."""
    # request.param will be the tuple (filtered_data, FIELD_MAPPINGS)
    return request.param


# Fixture to initialize and quit the WebDriver
# conftest.py

# ... (Existing imports: pytest, openpyxl, selenium, webdriver_manager) ...

# NOTE: The test_data fixture must be defined *before* driver_setup uses it
@pytest.fixture(params=get_excel_data())
def test_data(request):
    """Pytest fixture that yields test data for each row."""
    # This fixture correctly accesses request.param
    return request.param


@pytest.fixture(scope="function")
# 🎯 FIX HERE: Accept 'test_data' as an argument
def driver_setup(request, test_data):
    """
    Initializes WebDriver and updates the test node name for reporting.

    The 'test_data' argument ensures this fixture receives the value yielded
    by the parameterized test_data fixture.
    """


    # test_data is now the *value* yielded by the test_data fixture.
    # It's a tuple: (filtered_data_dict, FIELD_MAPPINGS_dict)
    data_row = test_data[0]  # Access the dictionary of filtered data

    first_name = data_row.get('FirstName', 'UNKNOWN_USER')

    # REPORTING STEP 1: Update the test name for the report
    request.node.name = f"{request.node.name}[user: {first_name}]"

    # WebDriver Initialization
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    yield driver

    # REPORTING STEP 2: Capture Screenshot on Failure (requires pytest_runtest_makereport hook)
    if request.node.rep_call.failed:
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        # Use data_row info for clearer file name
        screenshot_name = f"{screenshot_dir}/FAIL_{first_name}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n--- 📸 Screenshot saved: {screenshot_name} ---")

    driver.quit()