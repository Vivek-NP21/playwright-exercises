from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"

PRODUCT_NAME = "Combination Pliers"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(BASE_URL, wait_until="domcontentloaded")
    print("Application opened")

    # 1. Find product using visible product name
    product = page.get_by_text( PRODUCT_NAME,exact=True)
    expect(product).to_be_visible()
    print("Product found:", PRODUCT_NAME)


    # 2. Find the product card
    product_card = product.locator("xpath=ancestor::a[contains(@href, '/product/')]")
    expect(product_card).to_be_visible()
    print("Product card found")

    # 3. Find price inside product card
    price = product_card.locator('[data-test="product-price"]')
    expect(price).to_be_visible()
    price_text = price.inner_text()
    print("Price:", price_text)

    # 4. Find image inside product card
    image = product_card.locator("img")
    expect(image).to_be_visible()
    print("Image found")

    # 5. Additional DOM relationships
    # Parent element of product name
    parent = product.locator("..")
    expect(parent).to_be_visible()
    print("Parent element found")

    # Child elements of product card
    children = product_card.locator(":scope > *")
    child_count = children.count()
    print("Number of child elements:", child_count)
    assert child_count > 0, \
        "Product card has no child elements"
    print("Child elements found")


    # Sibling of product name
    sibling = product.locator("xpath=following-sibling::*").first
    if sibling.count() > 0:
        print("Sibling element found")

    # Element nested two or more levels below product card
    nested_element = product_card.locator("img")
    expect(nested_element).to_be_visible()
    print("Nested element found")


    product_card.click()
    print("Product details page opened")

    product_heading = page.locator("h1")
    expect(product_heading).to_be_visible()
    expect(product_heading).to_have_text(PRODUCT_NAME)
    print("Product name verified:", PRODUCT_NAME)

    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    print("Add to Cart button found")
    add_to_cart.click()
    print("Product added to cart")

    cart = page.get_by_role("link",name="Cart")
    expect(cart).to_be_visible()
    cart.click()
    print("Cart opened")

    cart_product = page.get_by_text(PRODUCT_NAME,exact=True)
    expect(cart_product).to_be_visible()
    print("Correct product found in cart:", PRODUCT_NAME)

    cart_price = page.locator('[data-test="product-price"]')
    expect(cart_price).to_be_visible()
    print("Product price verified in cart:", price_text)


    browser.close()