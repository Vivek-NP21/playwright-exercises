from playwright.sync_api import sync_playwright, expect


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://practicesoftwaretesting.com/")
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")

    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")

    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")

    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")

    guest_tab = page.get_by_role("tab",name="Continue as Guest")
    expect(guest_tab).to_be_visible()
    guest_tab.click()
    print("Continue as Guest tab selected")

    guest_email = page.locator('[data-test="guest-email"]')
    guest_first_name = page.locator('[data-test="guest-first-name"]')
    guest_last_name = page.locator('[data-test="guest-last-name"]')
    expect(guest_email).to_be_visible()
    expect(guest_first_name).to_be_visible()
    expect(guest_last_name).to_be_visible()
    guest_email.fill("viveknp@gmail.com")
    guest_first_name.fill("Vivek")
    guest_last_name.fill("NP")
    print("Valid guest information entered")

    page.locator('[data-test="guest-submit"]').click()
    print("Continue as Guest clicked")
    page.wait_for_load_state("networkidle")
    print("Moved to next checkout step")

    print("Current URL:", page.url)



    page.goto("https://practicesoftwaretesting.com/")
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()

    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")

    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")

    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")

    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")

    page.get_by_role("tab",name="Continue as Guest").click()
    print("Continue as Guest tab selected")

    page.locator('[data-test="guest-submit"]').click()
    print("Submitted empty form")

    expect(page.locator('[data-test="guest-email"]')).to_be_visible()
    expect(page.locator('[data-test="guest-first-name"]')).to_be_visible()
    expect(page.locator('[data-test="guest-last-name"]')).to_be_visible()
    print("Mandatory field validation displayed")
    print("Checkout was blocked")



    page.goto("https://practicesoftwaretesting.com/")
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()

    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")

    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")

    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")

    page.get_by_role("button",name="Proceed to checkout").click()
    print("Checkout page opened")

    page.get_by_role("tab",name="Continue as Guest").click()
    print("Continue as Guest tab selected")

    page.locator('[data-test="guest-email"]').fill("invalidemail")
    page.locator('[data-test="guest-first-name"]').fill("Vivek")
    page.locator('[data-test="guest-last-name"]').fill("NP")
    print("Invalid email entered")
    page.locator('[data-test="guest-submit"]').click()
    print("Submitted invalid information")
    expect(page.locator('[data-test="guest-email"]')).to_be_visible()
    print("Invalid information rejected")
    print("Checkout was blocked")



    page.goto("https://practicesoftwaretesting.com/")
    page.locator('[data-test="search-query"]').fill("Combination Pliers")
    page.locator('[data-test="search-submit"]').click()
    page.locator("a").filter(has_text="Combination Pliers").first.click()
    print("Product selected")
    page.wait_for_load_state("networkidle")
    page.get_by_role("button",name="Add to cart").click()
    print("Product added to cart")

    page.locator('[data-test="nav-cart"]').click()
    print("Cart opened")

    product_name = page.locator('[data-test="product-title"]').first.inner_text()
    product_price = page.locator('[data-test="product-price"]').first.inner_text()
    quantity = page.locator('[data-test="product-quantity"]').first.input_value()
    total = page.locator('[data-test="cart-total"]').inner_text()
    print("\nBefore Checkout")
    print("Product Name:", product_name)
    print("Product Price:", product_price)
    print("Quantity:", quantity)
    print("Total:", total)

    page.get_by_role("button",name="Proceed to checkout").click()
    print("\nCheckout page opened")

    checkout_product_name = page.locator('[data-test="product-title"]').first.inner_text()
    checkout_product_price = page.locator('[data-test="product-price"]').first.inner_text()
    checkout_quantity = page.locator('[data-test="product-quantity"]').first.input_value()
    checkout_total = page.locator('[data-test="cart-total"]').inner_text()
    print("\nAfter Checkout")
    print("Product Name:", checkout_product_name)
    print("Product Price:", checkout_product_price)
    print("Quantity:", checkout_quantity)
    print("Total:", checkout_total)

    assert checkout_product_name == product_name
    print("Product name matches")
    assert checkout_product_price == product_price
    print("Product price matches")
    assert checkout_quantity == quantity
    print("Quantity matches")
    assert checkout_total == total
    print("Total matches")
    browser.close()