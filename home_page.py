from playwright.sync_api import sync_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(BASE_URL)
    page.wait_for_timeout(3000)


    expect(page).to_have_url(BASE_URL)
    print("Application loaded successfully")


    expect(page).to_have_title(
        "Practice Software Testing - Toolshop - v5.0"
    )
    print("Page title verified")


    navigation = page.locator("nav").first
    expect(navigation).to_be_visible()
    print("Main navigation is visible")


    products = page.locator(
        "a[href^='/product/']"
    )
    product_count = products.count()
    print("Number of products:", product_count)
    assert product_count > 0, \
        "No products are available."
    expect(products.first).to_be_visible()
    print("Products are displayed")


    first_product = products.first
    first_product.click()
    page.wait_for_timeout(3000)
    assert "/product/" in page.url, \
        "Product page did not open"
    print("Product selected successfully")

    print("HOME PAGE TEST PASSED")

    page.wait_for_timeout(5000)

    browser.close()