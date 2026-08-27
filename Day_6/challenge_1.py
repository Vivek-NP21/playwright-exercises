import asyncio
import time
from playwright.async_api import async_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"

products = [
    "Combination Pliers",
    "Hammer",
    "Bolt Cutters",
    "Pliers",
    "Claw Hammer"
]


async def validate_product(browser, product):

    page = await browser.new_page()

    await page.goto(BASE_URL)

    search_box = page.get_by_role("textbox", name="Search")
    await search_box.fill(product)

    search_button = page.get_by_role("button", name="Search")
    await search_button.click()

    product_result = page.locator("a[href^='/product/']").filter(has=page.get_by_role("heading", name=product, exact=True))

    await expect(product_result).to_be_visible()

    print(product, "→ PASS")

    await page.close()


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        print("sequential execution")

        start_time = time.perf_counter()
        for product in products:
            await validate_product(browser, product)
        sequential_time = time.perf_counter() - start_time
        print(f"Sequential execution: {sequential_time:.2f} seconds")


        print("parallel execution")
        start_time = time.perf_counter()
        tasks = []
        for product in products:
            tasks.append(validate_product(browser, product))
        await asyncio.gather(*tasks)
        parallel_time = time.perf_counter() - start_time
        print(f"Parallel execution:   {parallel_time:.2f} seconds")

        await browser.close()

asyncio.run(main())