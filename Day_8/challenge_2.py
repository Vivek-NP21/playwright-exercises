from playwright.async_api import async_playwright, expect
import asyncio
import re

BASE_URL = "https://practicesoftwaretesting.com/"

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        print("Home page opened")

        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/?$"))
        print("Home page verified")


        products = page.locator("a[href^='/product/']")
        await expect(products.first).to_be_visible()
        await page.wait_for_load_state("networkidle")
        product_count = await products.count()
        print("Number of products:", product_count)
        assert product_count > 0, \
            "No products found"
        selected_product = None
        for i in range(product_count):
            product = products.nth(i)
            out_of_stock = product.locator('[data-test="out-of-stock"]')
            if await out_of_stock.count() > 0:
                continue
            selected_product = product
            break
        assert selected_product is not None, \
            "No available product found"
        await selected_product.click()
        await expect(page.locator("h1")).to_be_visible()
        await page.wait_for_load_state("networkidle")
        await expect(page.locator("h1")).not_to_have_text("")
        first_product_name = (await page.locator("h1").inner_text()).strip()
        print("First product:", first_product_name)

        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/product/.+"))
        print("First product page verified")

        related_products = page.locator("a[href^='/product/']")
        await expect(related_products.first).to_be_visible()
        await page.wait_for_load_state("networkidle")
        related_count = await related_products.count()
        print("Related products:", related_count)

        second_product = None
        for i in range(related_count):
            product = related_products.nth(i)
            product_name = await product.inner_text()
            if product_name.strip() != first_product_name.strip():
                second_product = product
                break
        assert second_product is not None, \
            "Second product not found"
        await second_product.click()
        await expect(page.locator("h1")).to_be_visible()
        await page.wait_for_load_state("networkidle")
        await expect(page.locator("h1")).not_to_have_text(first_product_name)
        second_product_name = (await page.locator("h1").inner_text()).strip()
        print("Second product:", second_product_name)
        assert second_product_name != first_product_name.strip(), \
            "Second product name matches first product - navigation " \
            "did not actually change page"

        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/product/.+"))
        print("Second product page verified")

        await page.reload()
        print("Second product page refreshed")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/product/.+"))

        await expect(page.locator("h1")).to_have_text(second_product_name)

        second_product_after_refresh = await page.locator("h1").inner_text()
        print("Product after refresh:",second_product_after_refresh)
        print("Refresh verified successfully")

        contact_link = page.get_by_role("link",name="Contact")
        await contact_link.click()
        await expect(page.locator("h1")).to_be_visible()
        print("Contact page opened")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        print("Contact page verified")


        await page.go_back()
        print("Went back to second product")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        await expect(page.locator("h1")).to_have_text(second_product_name)

        second_product_after_back = await page.locator("h1").inner_text()
        print("Product after back:",second_product_after_back)
        print("Second product restored successfully")
        await page.go_back()
        print("Went back to first product")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))

        await expect(page.locator("h1")).to_have_text(first_product_name)
        first_product_after_back = await page.locator("h1").inner_text()
        print("Product after back:",first_product_after_back)
        print("First product restored successfully")


        await page.go_back()
        print("Went back to home page")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        print("Home page restored successfully")
        await page.go_forward()

        print("Went forward to first product")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        await expect(page.locator("h1")).to_have_text(first_product_name)
        first_product_after_forward = await page.locator("h1").inner_text()
        print("Product after forward:",first_product_after_forward)
        print("First product restored after forward")

        await page.go_forward()
        print("Went forward to second product")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        await expect(page.locator("h1")).to_have_text( second_product_name)
        second_product_after_forward = await page.locator("h1").inner_text()
        print("Product after forward:",second_product_after_forward)
        print("Second product restored after forward")

        await page.go_forward()
        print("Went forward to Contact page")
        await expect(page).to_have_url(re.compile(r"https://practicesoftwaretesting\.com/contact"))
        print("Contact page restored after forward")
        await browser.close()


asyncio.run(main())