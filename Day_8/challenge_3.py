import re
import pytest
from playwright.async_api import async_playwright, expect

URL = "https://en.wikipedia.org/wiki/Software_testing"

@pytest.mark.asyncio
async def test_hover_dynamic_product_interaction():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. Navigate to Wikipedia
        await page.goto(URL)
        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software_testing/?$"))
        print("Wikipedia page opened")

        # 2. Identify the Software link
        software_links = page.locator("a[title='Software'][href='https://en.wikipedia.org/wiki/Software']")
        print("Number of Software links:", await software_links.count())
        # Use the first matching Software link
        software_link = software_links.first
        await expect(software_link).to_be_visible()
        print("Software link found")

        # 3. Capture initial state
        popup = page.locator(".mwe-popups")
        # Popup should not be visible before hover
        await expect(popup).not_to_be_visible()
        print("Initial state: popup is hidden")

        # 4. Hover over Software
        await software_link.hover()
        print("Mouse hovered over Software")

        # 5. Verify hover UI becomes visible
        await expect(popup).to_be_visible()
        print("Hover state: popup is visible")

        # 6. Interact with newly revealed element
        preview_link = popup.get_by_role("link",name=re.compile("Software", re.IGNORECASE)).first
        await expect(preview_link).to_be_visible()
        print("Preview link found")
        await preview_link.click()

        # 7. Verify resulting page
        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software/?$"))
        print("Result verified: Software page opened")

        # 8. Go back
        await page.go_back()
        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software_testing/?$"))
        print("Returned to Software Testing page")

        # 9. Move mouse away
        await page.mouse.move(10, 10)

        # 10. Verify popup disappears
        await expect(popup).not_to_be_visible()
        print("Final state: popup disappeared")
        await browser.close()