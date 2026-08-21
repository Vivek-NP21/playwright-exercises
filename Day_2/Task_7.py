from playwright.sync_api import sync_playwright, expect
Base_url="https://practicesoftwaretesting.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()

    page.goto(Base_url)
    page.wait_for_timeout(2000)
    print("application opend")

    products=page.locator('a[href^="/product/"]')
    product_count=products.count()
    print("no of products: ",product_count)
    assert product_count>0,\
        "no product are there"
    for i in range (product_count):
        product= products.nth(i)
        if product.locator('[data-test="out-of-stock"]').count() > 0:
            continue
        expect(product).to_be_visible()
        product.click()
        page.wait_for_timeout(2000)
        break
    print("Product selected")

    product_name=page.locator("h1")
    expect(product_name).to_be_visible()
    product_name_text=product_name.inner_text()
    print("product name:",product_name_text)
    assert product_name_text.strip() !="",\
        "product name is empty"
    print("product name verified")


    product_price=page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    expect(product_price).to_be_visible()
    product_price_text=product_price.inner_text()
    print("product price: ",product_price_text)
    assert "$" in product_price_text,\
        "product price is not dispalyed"
    print("product price verified")

    product_image=page.locator("figure img").first
    expect(product_image).to_be_visible()
    image_source=product_image.get_attribute("src")
    assert image_source,\
        "product iage is not there"
    print("product image verified")

    descp=page.locator("p").filter(has_text=".").first
    expect(descp).to_be_visible()
    descp_text=descp.inner_text()
    print("product description: ",descp_text)
    assert descp_text.strip() !="",\
        "product description is empty"
    print("product desription verified")

    quantity=page.get_by_role("spinbutton",name="Quantity")
    expect(quantity).to_be_visible()
    print("quantity control verified")

    add_to_cart= page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    print("add to cart button verified")

    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("product added to cart")

    cart=page.get_by_role("link",name="Cart")
    cart.click()
    page.wait_for_timeout(5000)
    print("cart opened")

    cart_product=page.get_by_text(product_name_text,exact=True)
    expect(cart_product).to_be_visible()
    print("product name verified in cart:",product_name_text)

    cart_price = page.locator('[data-test="product-price"]')    
    expect(cart_price).to_be_visible()
    cart_price_text=cart_price.inner_text()
    assert cart_price_text==product_price_text,\
        "product price in cart does not match"
    print("product price verified in cart:",product_price_text)

    page.wait_for_timeout(3000)
    browser.close()