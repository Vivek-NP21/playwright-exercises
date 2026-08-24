from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"
valid_searches = ["Hammer", "Pliers", "Screwdriver", "Wrench", "Saw"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    search_term = "Pliers"
    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    print("Application opened")

    search_box = page.get_by_role("textbox", name="search")
    expect(search_box).to_be_visible()
    search_box.fill(search_term)
    search_button = page.get_by_role("button", name="search")
    expect(search_button).to_be_visible()
    search_button.click()
    page.wait_for_timeout(2000)
    print("Searched for:", search_term)

    product_links = page.locator("a[href^='/product/']")
    product_count = product_links.count()
    assert product_count > 0, "No search results displayed"
    print("Search results displayed")

    expected_product = None
    for i in range(product_count):
        product = product_links.nth(i)
        name = product.locator("h5").inner_text()
        print("Result:", name)
        if search_term.lower() in name.lower():
            expected_product = product
            break
    assert expected_product is not None, \
        "Expected product was not found"
    print("Expected product is present")

    product_name = expected_product.locator("h5").inner_text()
    assert search_term.lower() in product_name.lower(), \
        "Product name does not match search"
    print("Product name verified")

    expected_product.click()
    page.wait_for_timeout(2000)
    print("Product clicked")
    product_heading = page.locator("h1")
    expect(product_heading).to_be_visible()
    actual_product_name = product_heading.inner_text()
    assert search_term.lower() in actual_product_name.lower(), \
        "Wrong product details page opened"
    print("Correct product opened")

    partial_search = "pliers"
    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    search_box = page.get_by_role("textbox", name="search")
    search_box.fill(partial_search)
    search_button = page.get_by_role("button", name="search")
    search_button.click()
    page.wait_for_timeout(2000)
    print("Searched for:", partial_search)
    product_links = page.locator("a[href^='/product/']")
    product_count = product_links.count()
    assert product_count > 0, \
        "No results displayed for partial search"
    print("Partial search results displayed")

    for i in range(product_count):
        product = product_links.nth(i)
        product_name = product.locator("h5").inner_text()
        print("Result:", product_name)
        assert partial_search.lower() in product_name.lower(), \
            "Search result does not contain searched text"
    print("All partial search results verified")

    invalid_search = "xyzabc123"
    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    search_box = page.get_by_role("textbox", name="search")
    search_box.fill(invalid_search)
    search_button = page.get_by_role("button", name="search")
    search_button.click()
    page.wait_for_timeout(2000)
    print("Searched for:", invalid_search)
    product_links = page.locator("a[href^='/product/']")
    product_count = product_links.count()
    assert product_count == 0, \
        "Products were displayed for invalid search"
    print("No product results displayed")

    no_results = page.get_by_text("There are no products found.")
    expect(no_results).to_be_visible()
    print("No-results message verified")

    for search_term in valid_searches:
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)
        search_box = page.get_by_role("textbox", name="search")
        search_box.fill(search_term)
        search_button = page.get_by_role("button", name="search")
        search_button.click()
        page.wait_for_timeout(1500)
        product_links = page.locator("a[href^='/product/']")
        product_count = product_links.count()
        print("\nSearch term:", search_term)
        print("Number of results:", product_count)
        assert product_count > 0, \
            "No results found for " + search_term

        found = False
        for i in range(product_count):
            product = product_links.nth(i)
            product_name = product.locator("h5").inner_text()
            print("Result:", product_name)
            if search_term.lower() in product_name.lower():
                found = True
                break
        assert found, \
            "Expected product not found for " + search_term
        print("Verified:", search_term)

    page.wait_for_timeout(3000)
    browser.close()