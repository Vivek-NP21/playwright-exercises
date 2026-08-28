from playwright.async_api import async_playwright, expect
import uuid
import pytest


BASE_URL = "https://practicesoftwaretesting.com"

@pytest.mark.asyncio
async def test_product_search():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(BASE_URL)
            search_box = page.get_by_placeholder("Search")
            await search_box.fill("Hammer")
            await page.get_by_role("button",name="Search").click()
            await expect(page.get_by_text("Hammer",exact=True).first).to_be_visible()

        finally:
            await context.close()
            await browser.close()

@pytest.mark.asyncio
async def test_product_details():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(BASE_URL)
            await page.get_by_placeholder("Search").fill("Hammer")
            await page.get_by_role("button",name="Search").click()
            product = page.get_by_role("link",name="Thor Hammer",exact=False)
            await expect(product).to_be_visible()
            await product.click()
            await expect(page.get_by_role("heading",name="Thor Hammer",exact=True)).to_be_visible()
            await expect(page.get_by_text("$11.14",exact=True)).to_be_visible()
            await expect(page.get_by_text("The legendary Thor Hammer combines premium craftsmanship",exact=False)).to_be_visible()
            await expect(page.get_by_role("button",name="Add to cart",exact=True)).to_be_visible()

        finally:
            await context.close()
            await browser.close()

@pytest.mark.asyncio
async def test_product_category():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto("https://practicesoftwaretesting.com/")
            await page.locator('button[data-test="nav-categories"]').click()
            tool = page.locator('a[data-test="nav-power-tools"]')
            await expect(tool).to_be_visible()
            await tool.click()
            print("Selected category:", await tool.text_content())
            product_details = page.locator(".card")
            await expect(product_details.first).to_be_visible()
            product_count = await product_details.count()
            assert product_count > 0, \
                "No products are displayed"
            print("Number of products:",product_count)
            for i in range(product_count):
                product = product_details.nth(i)
                await expect(product).to_be_visible()
                product_name = await product.locator("h5").inner_text()
                print("Power Tools product:",product_name )

        finally:
            await context.close()
            await browser.close()


LOGIN_URL = "https://practicesoftwaretesting.com/auth/login"
REGISTER_URL = "https://practicesoftwaretesting.com/auth/register"


@pytest.mark.asyncio
async def test_registration():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:

            await page.goto(REGISTER_URL)
            page.locator('[data-test="register-form"]')
            unique_email = (f"testuser_{uuid.uuid4().hex[:10]}@gmail.com")
            await page.locator('[data-test="first-name"]').fill("vivek")
            await page.locator('[data-test="last-name"]').fill("NP")
            await page.locator('[data-test="dob"]').fill("2003-08-21")
            await page.locator('[data-test="country"]').select_option("India")
            await page.locator('[data-test="postal_code"]').fill("570014")
            await page.locator('[data-test="house_number"]').fill("48")
            await page.locator('[data-test="street"]').fill("street")
            await page.locator('[data-test="city"]').fill("mysore")
            await page.locator('[data-test="state"]').fill("karnataka")
            await page.locator('[data-test="phone"]').fill("9876543212")
            await page.locator('[data-test="email"]').fill(unique_email)
            await page.locator('[data-test="password"]').fill("Vivek@a1a2b3c4d5e")
            await page.locator('[data-test="register-submit"]').click()
            await expect(page).to_have_url(LOGIN_URL,)

        finally:
            await context.close()
            await browser.close()