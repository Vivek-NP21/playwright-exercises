from playwright.sync_api import sync_playwright, expect
Base_url = "https://practicesoftwaretesting.com/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(Base_url)
    page.wait_for_timeout(2000)
    print("Application opened")

    products = page.locator("a[href^='/product/']")
    product_count = products.count()
    print("Number of products:", product_count)
    assert product_count > 0, \
        "No products are displayed"
    print("Products are displayed")


    cheapest_price = float("inf")
    cheapest_product = ""

    page_number = 1

    while True:

        print("Checking page:", page_number)
        products = page.locator("a[href^='/product/']")
        product_count = products.count()
        print("Number of products:", product_count)

        for i in range(product_count):
            product = products.nth(i)
            product_name = product.locator("h5").inner_text().strip()
            price_text = product.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text()
            price = float(price_text.replace("$", ""))
            print(product_name, "-", price_text)
            if price < cheapest_price:
                cheapest_price = price
                cheapest_product = product_name

        next_page = page.locator(f'a[aria-label="Page-{page_number + 1}"]')

        if next_page.count() == 0:
            break

        next_page.click()

        page.wait_for_timeout(1000)

        page_number += 1

    print("Cheapest product:")
    print( f"{cheapest_product} - ${cheapest_price:.2f}")

    page.wait_for_timeout(3000)

    browser.close()