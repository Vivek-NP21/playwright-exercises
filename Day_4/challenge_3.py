from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    print("Application opened")

    cheapest_price = float("inf")
    cheapest_product = ""
    cheapest_url = ""

    most_expensive_price = float("-inf")
    most_expensive_product = ""
    most_expensive_url = ""

    page_number = 1

    while True:
        print("\nChecking page:", page_number)
        products = page.locator("a[href^='/product/']")
        product_count = products.count()
        print("Number of products:", product_count)
        assert product_count > 0, "No products are displayed"
        for i in range(product_count):
            product = products.nth(i)
            out_of_stock = product.locator("[data-test='out-of-stock']")
            if out_of_stock.count() > 0:
                print("Skipping out-of-stock product")
                continue
            product_name = product.locator("h5").inner_text().strip()
            price_text = product.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text()
            price = float(price_text.replace("$", ""))
            product_url = product.get_attribute("href")
            print(product_name,"-",price_text)

            if price < cheapest_price:
                cheapest_price = price
                cheapest_product = product_name
                cheapest_url = product_url

            if price > most_expensive_price:
                most_expensive_price = price
                most_expensive_product = product_name
                most_expensive_url = product_url

        next_page = page.locator(f'a[aria-label="Page-{page_number + 1}"]')
        if next_page.count() == 0:
            break
        next_page.click()
        page.wait_for_timeout(1000)
        page_number += 1

    print("Product:", cheapest_product)
    print(f"Price: ${cheapest_price:.2f}")

    print("Product:", most_expensive_product)
    print(f"Price: ${most_expensive_price:.2f}")

    page.goto(BASE_URL.rstrip("/") + cheapest_url)
    page.wait_for_timeout(1000)
    print("Opened:", cheapest_product)

    product_page_name = page.locator("[data-test='product-name']").inner_text().strip()
    print("Product page name:", product_page_name)
    assert product_page_name == cheapest_product, \
        "Cheapest product name does not match"
    print("Cheapest product name verified")

    product_page_price_text = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text()
    product_page_price = float(product_page_price_text.replace("$", ""))
    print("Product page price:", product_page_price_text)
    assert product_page_price == cheapest_price, \
        "Cheapest product price does not match"
    print("Cheapest product price verified")

    page.get_by_role("button",name="Add to cart").click()
    page.wait_for_timeout(1000)
    print("Cheapest product added to cart")

    page.get_by_role("link",name="Cart").click()
    page.wait_for_timeout(1000)
    print("Cart opened")

    cart_product = page.locator("[data-test='product-title']")
    expect(cart_product).to_contain_text(cheapest_product)
    print("Cheapest product verified in cart")

    page.goto(BASE_URL.rstrip("/") + most_expensive_url)
    page.wait_for_timeout(1000)
    print("Opened:", most_expensive_product)

    expensive_page_name = page.locator("[data-test='product-name']").inner_text().strip()
    expensive_page_name = expensive_page_name.split("\n")[0].strip()
    print("Product page name:", expensive_page_name)
    assert expensive_page_name == most_expensive_product, \
        "Most expensive product name does not match"
    print("Most expensive product name verified")

    expensive_page_price_text = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text()
    expensive_page_price = float(expensive_page_price_text.replace("$", ""))
    print("Product page price:", expensive_page_price_text)
    assert expensive_page_price == most_expensive_price, \
        "Most expensive product price does not match"
    print("Most expensive product price verified")

    page.get_by_role("button",name="Add to cart").click()
    page.wait_for_timeout(1000)
    print("Most expensive product added to cart")

    page.get_by_role("link",name="Cart").click()
    page.wait_for_timeout(1000)
    print("Cart opened")

    cart_product = page.get_by_text(most_expensive_product,exact=True)
    expect(cart_product).to_be_visible()    
    print("Most expensive product verified in cart")

    browser.close()





