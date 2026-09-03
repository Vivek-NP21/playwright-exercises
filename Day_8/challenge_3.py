import re
import pytest
from playwright.async_api import async_playwright, expect

URL = "https://en.wikipedia.org/wiki/Software_testing"

@pytest.mark.asyncio
async def test_hover_dynamic_product_interaction():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(URL)
        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software_testing/?$"))
        print("Wikipedia page opened")

        software_links = page.locator("a[title='Software'][href='https://en.wikipedia.org/wiki/Software']")
        print("Number of Software links:", await software_links.count())
        software_link = software_links.first
        await expect(software_link).to_be_visible()
        print("Software link found")

        popup = page.locator(".mwe-popups")
        await expect(popup).not_to_be_visible()
        print("Initial state: popup is hidden")

        await software_link.hover()
        print("Mouse hovered over Software")

        await expect(popup).to_be_visible()
        print("Hover state: popup is visible")

        preview_link = popup.get_by_role("link",name=re.compile("Software", re.IGNORECASE)).first
        await expect(preview_link).to_be_visible()
        print("Preview link found")
        await preview_link.click()

        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software/?$"))
        print("Result verified: Software page opened")

        await page.go_back()
        await expect(page).to_have_url(re.compile(r"https://en\.wikipedia\.org/wiki/Software_testing/?$"))
        print("Returned to Software Testing page")

        await page.mouse.move(10, 10)

        await expect(popup).not_to_be_visible()
        print("Final state: popup disappeared")
        await browser.close()