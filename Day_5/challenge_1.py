from playwright.sync_api import sync_playwright, expect
Base_url = "https://practicesoftwaretesting.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(Base_url)
    page.wait_for_timeout(2000)
    print("Application opened")

    all_products = []
    page_number = 1

    while True:
        print("Checking page:", page_number)
        products = page.locator("a[href^='/product/']")
        product_count = products.count()
        print("Number of products:", product_count)
        assert product_count > 0, \
            "No products are displayed"
        print("Products are displayed")

        current_page_products = []
        for i in range(product_count):
            product = products.nth(i)
            product_name = product.locator("h5").inner_text().strip()
            print("Product:", product_name)
            current_page_products.append(product_name)

        print(f"Page {page_number}: "f"{len(current_page_products)} products")

        if page_number > 1:
            assert current_page_products != previous_page_products, \
                f"Page {page_number} contains the same products as previous page"
            print("Current page products are different from previous page")
        all_products.extend(current_page_products)
        previous_page_products = current_page_products.copy()
        next_page = page.locator(f'a[aria-label="Page-{page_number + 1}"]')

        if next_page.count() == 0:
            print("No more pages")
            break
        print("Next page found")

        next_page.click()
        page.wait_for_timeout(1000)
        page_number += 1

    unique_products = set(all_products)

    print("Total products:", len(all_products))
    print("Total unique products:", len(unique_products))
    assert len(all_products) == len(unique_products), \
        "Duplicate products found across pages"
    print("No product appears more than once")
    print("Pagination test passed")

    page.wait_for_timeout(3000)
    browser.close()