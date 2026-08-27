from playwright.sync_api import sync_playwright, expect
import random

BASE_URL = "https://practicesoftwaretesting.com/"
REGISTER_URL = "https://practicesoftwaretesting.com/auth/register"
LOGIN_URL = "https://practicesoftwaretesting.com/auth/login"

registration_scenarios = [

    {
        "name": "Scenario 1 - Empty First Name",
        "first_name": "",
        "last_name": "NP",
        "dob": "2003-08-21",
        "country": "India",
        "postal_code": "570014",
        "house_number": "48",
        "street": " street",
        "city": "mysore",
        "state": "karnataka",
        "phone": "1234567898",
        "email": "vivek@gmail.com",
        "password": "vivek*1303",
        "valid": False
    },

    {
        "name": "Scenario 2 - Empty Last Name",
        "first_name": "vivek",
        "last_name": "",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "570014",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karnataka",
        "phone": "1234567897",
        "email": "vivek@gmail.com",
        "password": "vivek*1303",
        "valid": False
    },

    {
        "name": "Scenario 3 - Invalid Email",
        "first_name": "vivek",
        "last_name": "NP",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "570014",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karnataka",
        "phone": "1234567653",
        "email": "invalid-email",
        "password": "vivek*1303",
        "valid": False
    },

    {
        "name": "Scenario 4 - Missing Password",
        "first_name": "vivek",
        "last_name": "NP",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "570014",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karnataka",
        "phone": "1234568762",
        "email": "vivek@gmail.com",
        "password": "",
        "valid": False
    },

    {
        "name": "Scenario 5 - Invalid Password",
        "first_name": "vivek",
        "last_name": "NP",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "570014",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karanataka",
        "email": "vivek@gmail.com",
        "phone": "1234567891",
        "password": "123",
        "valid": False
    },

    {
        "name": "Scenario 6 - Missing Postal Code",
        "first_name": "vivek",
        "last_name": "np",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karanataka",
        "phone": "1234567891",
        "email": "vivek@gmail.com",
        "password": "vivek*1303",
        "valid": False
    },

    {
        "name": "Scenario 7 - Valid Registration",
        "first_name": "vivek",
        "last_name": "np",
        "dob": "2003-08-21",
        "country": "IN",
        "postal_code": "570014",
        "house_number": "48",
        "street": "street",
        "city": "mysore",
        "state": "karanataka",
        "phone": "1234567891",
        "email": "",
        "password": "vivek*1303",
        "valid": True
    }
]


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for test_data in registration_scenarios:

        print(test_data["name"])

        page.goto(REGISTER_URL)
        page.locator('[data-test="register-form"]').wait_for(state="visible",timeout=5000)
        print("Registration page opened")
        page.locator('[data-test="first-name"]').fill(test_data["first_name"])
        page.locator('[data-test="last-name"]').fill(test_data["last_name"])
        page.locator('[data-test="dob"]').fill(test_data["dob"])
        page.locator('[data-test="country"]').select_option(test_data["country"])

        page.locator('[data-test="postal_code"]').fill(test_data["postal_code"])
        page.locator('[data-test="house_number"]').fill(test_data["house_number"])
        if test_data["postal_code"]:
            page.get_by_role("status").wait_for(state="hidden",timeout=5000)
        page.locator('[data-test="street"]').fill(test_data["street"])
        page.locator('[data-test="city"]').fill(test_data["city"])
        page.locator('[data-test="state"]').fill(test_data["state"])
        page.locator('[data-test="phone"]').fill(test_data["phone"])

        email = test_data["email"]
        if test_data["valid"]:
            email = f"vivek_{random.randint(100000, 999999)}@gmail.com"
            print("Generated email:", email)
        page.locator('[data-test="email"]').fill(email)
        page.locator('[data-test="password"]').fill(test_data["password"])
        print("Registration details entered")

        page.locator('[data-test="register-submit"]').click()
        print("Register button clicked")

        if test_data["valid"]:
            expect(page).to_have_url(LOGIN_URL,timeout=5000)
            print("Registration successful")
            print("Redirected to login page")
            print("PASSED:", test_data["name"])
        else:
            expect(page.locator('[data-test="register-form"]')).to_be_visible(timeout=5000)
            print("Registration was blocked")
            print("PASSED:", test_data["name"])

    browser.close()