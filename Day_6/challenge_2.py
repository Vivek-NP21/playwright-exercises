import asyncio
from playwright.async_api import async_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com/"

products_to_search = [
    "Combination Pliers",
    "Hammer",
    "Bolt Cutters",
    "Phillips Screwdriver",
    "Pliers"
]


async def search_product(browser, product_name):

    page = await browser.new_page()

    try:
        print(f"Searching for: {product_name}")

        await page.goto(BASE_URL)

        search_box = page.get_by_role("textbox", name="Search")
        await expect(search_box).to_be_visible()

        await search_box.fill(product_name)

        search_button = page.get_by_role("button", name="Search")
        await search_button.click()

        expected_product = page.get_by_role("heading",name=product_name,exact=True)

        await expect(expected_product).to_be_visible()

        print(f"{product_name} → PASS")

    except Exception as error:
        print(f"{product_name} → FAIL")
        print(f"Reason: {error}")

    finally:
        await page.close()


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        tasks = []

        for product in products_to_search:
            tasks.append(search_product(browser, product))

        await asyncio.gather(*tasks)

        await browser.close()


asyncio.run(main())