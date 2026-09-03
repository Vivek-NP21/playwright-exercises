from playwright.sync_api import sync_playwright,expect

def test_strict_mode_locator():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.amazon.in/",wait_until="domcontentloaded")
        print("Amazon opened")

        search_box = page.locator("#twotabsearchtextbox")
        search_box.wait_for(state="visible")
        search_box.fill("wireless mouse")
        search_box.press("Enter")
        page.wait_for_load_state("domcontentloaded")
        print("Product search completed")

        product_cards = page.locator('[data-component-type="s-search-result"]')
        product_count = product_cards.count()
        print("Product cards found:",product_count)
        assert product_count > 0

        selected_product = None
        product_name = None
        for i in range(product_count):
            card = product_cards.nth(i)
            title = card.locator("h2")
            if title.count() == 0:
                continue
            name = title.inner_text()

            if name.strip():
                selected_product = card
                product_name = name
                break
        assert selected_product is not None
        print("Selected product:",product_name)



        broad_locator = page.get_by_role("button",name="Add to cart")
        broad_count = broad_locator.count()
        print("Locator matched:",broad_count,"elements")

        if broad_count > 1:
            print("Multiple elements matched.")
            print("This locator is too broad.")
            print("Playwright would throw a strict-mode violation if click() was called.")

        elif broad_count == 1:
            print("Only one Add to Cart button is currently exposed.")

        else:
            print("Amazon does not expose these controls with this role on the current page.")


        fixed_locator = selected_product.locator('input[value="Add to Cart"]')
        fixed_count = fixed_locator.count()
        if fixed_count == 0:
            fixed_locator = selected_product.get_by_role("button",name="Add to cart")
            fixed_count = fixed_locator.count()
        print("Locator matched:",fixed_count,"element")

        assert fixed_count == 1, ("Expected exactly one Add to Cart ""element inside the selected product")
        print("Unique Add to Cart button identified")

        fixed_locator.click()
        print("Product added to cart")

        cart = page.locator("#nav-cart").click()
        print("Cart opened")

        cart_product = page.get_by_text(product_name,exact=False)
        expect(cart_product).to_be_visible()

        print("Product successfully verified in cart:")
        print(product_name)

        browser.close()

if __name__ == "__main__":

    test_strict_mode_locator()