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
    assert product_count >= 5, \
        "Less than 5 products are available"
    print("At least 5 products are available")

    mismatches = []
    products_checked = 0
    while products_checked < 5:
        print("Checking product:", products_checked + 1)
        products = page.locator("a[href^='/product/']")
        product = products.nth(products_checked)
        listing_name = product.locator("h5").inner_text().strip()
        listing_price_text = product.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text().strip()
        listing_price = float(listing_price_text.replace("$", ""))
        print("Listing name:", listing_name)
        print("Listing price:", listing_price_text)
        product.click()
        page.wait_for_timeout(1000)

        details_name = page.locator("h1").inner_text().strip()
        details_price_text = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first.inner_text().strip()
        details_price = float(details_price_text.replace("$", ""))
        print("Details name:", details_name)
        print("Details price:", details_price_text)
        if listing_name != details_name:
            mismatches.append( f"{listing_name}: " f"Name mismatch | " f"Listing='{listing_name}' | " f"Details='{details_name}'")
            print("Name mismatch")
        else:
            print("Name matched")

        if listing_price != details_price:
            mismatches.append(f"{listing_name}: " f"Price mismatch | " f"Listing='{listing_price_text}' | " f"Details='{details_price_text}'")
            print("Price mismatch")
        else:
            print("Price matched")

        page.go_back()
        page.wait_for_timeout(1000)
        expect(page.locator("a[href^='/product/']").first).to_be_visible()
        print("Returned to product listing")
        products_checked += 1

    if len(mismatches) == 0:
        print("All 5 products matched")
        print("Name and price are consistent")
    else:
        print("Mismatches found:", len(mismatches))
        for mismatch in mismatches:
            print(mismatch)
    assert len(mismatches) == 0, \
        "Product consistency validation failed"

    page.wait_for_timeout(3000)

    browser.close()