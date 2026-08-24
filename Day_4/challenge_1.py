from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(BASE_URL)
    print("Application opened")

    search_box = page.get_by_placeholder("Search")
    search_box.fill("pliers")
    page.get_by_role("button", name="Search").click()
    products = page.locator('a[href^="/product/"]')
    expect(products.first).to_be_visible()
    print("Product search completed")

    selected_product = None
    for i in range(products.count()):
        product = products.nth(i)
        out_of_stock = product.locator('[data-test="out-of-stock"]')
        if out_of_stock.count() == 0:
            selected_product = product
            break
    assert selected_product is not None, "No available product found"
    selected_product.click()

    product_name = page.locator('[data-test="product-name"]').inner_text()
    product_price_text = page.locator('[data-test="unit-price"]').inner_text()
    product_price = float(product_price_text.replace("$", "").strip())
    print("Product name:", product_name)
    print("Product price:", product_price)
    expect(page.locator('[data-test="product-name"]')).to_have_text(product_name)
    expect(page.locator('[data-test="unit-price"]')).to_be_visible()

    page.get_by_role("button", name="Add to cart").click()
    print("Product added to cart")

    page.get_by_role("link", name="Cart").click()
    print("Cart opened")

    cart_product = page.locator('[data-test="product-title"]')
    expect(cart_product).to_have_text(product_name)
    print("Product verified in cart")

    cart_price_text = page.locator('[data-test="product-price"]').inner_text()
    cart_price = float(cart_price_text.replace("$", "").strip())
    assert cart_price == product_price, (
        f"Expected price ${product_price}, " f"but cart shows ${cart_price}")
    print("Product price verified")

    quantity_input = page.locator('[data-test="product-quantity"]')
    quantity_input.fill("2")
    page.wait_for_timeout(2000)
    expect(quantity_input).to_have_value("2")
    print("Quantity changed to 2")

    expected_total = product_price * 2
    cart_total_text = page.locator('[data-test="cart-total"]').inner_text()
    cart_total = float(cart_total_text.replace("$", "").strip())
    assert cart_total == expected_total, (
        f"Expected total ${expected_total:.2f}, " f"but cart shows ${cart_total:.2f}")
    print("Cart total verified")
    print(f"Expected total: ${expected_total:.2f}")
    print(f"Actual total: ${cart_total:.2f}")

    cart_row = page.locator("tr").filter(has_text=product_name)
    remove_button = cart_row.locator("a.btn.btn-danger")
    expect(remove_button).to_be_visible()
    remove_button.click()
    print("Product removed:", product_name)

    expect(page.locator("tr").filter(has_text=product_name)).to_have_count(0)
    print("Cart is empty")
    page.wait_for_timeout(3000)
    browser.close()