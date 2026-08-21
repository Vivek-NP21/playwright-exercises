from playwright.sync_api import sync_playwright, expect
Base_url="https://practicesoftwaretesting.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()

    page.goto(Base_url)
    page.wait_for_timeout(2000)
    print("application opend")

    categories = page.get_by_role("button", name="Categories")
    expect(categories).to_be_visible()
    categories.click()
    page.wait_for_timeout(1000)
    print("categories opend")

    hand_tools=page.get_by_text("Hand Tools", exact=True).first
    expect(hand_tools).to_be_visible()
    hand_tools.click()
    page.wait_for_timeout(2000)
    print("hand tools category selected")

    expect(page).to_have_url("https://practicesoftwaretesting.com/category/hand-tools")
    print("category page displayed")

    products= page.locator( 'a[href^="/product/"]')
    product_count=products.count()
    print("no of product displayed:" , product_count)
    assert product_count>0,\
        "no product are displayed"
    print("product are displayed")

    for i in range (product_count):
        product = products.nth(i)
        product_name=product.inner_text()
        print("product",i+1,":",product_name)
        expect(product).to_be_visible()

    page.wait_for_timeout(3000)
    browser.close()


            