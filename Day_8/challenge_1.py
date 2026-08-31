import pytest
from pathlib import Path
from playwright.async_api import async_playwright, expect

BASE_URL = "https://practice.expandtesting.com/upload"

PROJECT_PATH = Path(__file__).parent

VALID_FOLDER = PROJECT_PATH / "test-data" / "valid"
INVALID_FOLDER = PROJECT_PATH / "test-data" / "invalid"


@pytest.mark.asyncio
async def test_valid_file_upload():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        print("\nApplication opened")
        file_input = page.locator("input[type='file']")
        valid_file = VALID_FOLDER / "sample_text.txt"
        await file_input.set_input_files(str(valid_file))
        print("Valid file selected")

        selected_file = await file_input.evaluate("input => input.files[0].name")
        assert selected_file == "sample_text.txt"
        print("File selection verified")
        await page.get_by_role("button",name="Upload").click()
        print("Upload button clicked")

        await expect(page.locator("body")).to_contain_text("sample_text.txt")
        print("Upload successful")
        await browser.close()



@pytest.mark.asyncio
async def test_invalid_file_upload():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        print("\nApplication opened")
        file_input = page.locator("input[type='file']")
        invalid_file = INVALID_FOLDER / "large_file.txt"
        await file_input.set_input_files(str(invalid_file))
        print("Invalid file selected")
        file_count = await file_input.evaluate("input => input.files.name")
        print("Number of selected files:", file_count)

        assert file_count == 0
        print("Invalid file selection verified")
        await page.get_by_role("button",name="Upload").click()
        print("Upload button clicked")

        await expect(page.locator("body")).to_contain_text("500 KB")
        print("Invalid file rejected")
        await browser.close()

@pytest.mark.parametrize(
    "file_name",
    [
        "sample_text.txt",
        "sample_pdf.pdf",
        "sample_image.png"
    ]
)
@pytest.mark.asyncio
async def test_multiple_file_types(file_name):

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(BASE_URL)
        print(f"\nTesting file: {file_name}")
        file_path = VALID_FOLDER / file_name
        file_input = page.locator("input[type='file']")
        await file_input.set_input_files(str(file_path))
        print(f"{file_name} selected")
        selected_file = await file_input.evaluate("input => input.files[0].name")
        assert selected_file == file_name
        print(f"{file_name} selection verified")
        await page.get_by_role("button",name="Upload").click()
        print(f"{file_name} uploaded")

        await expect(page.locator("body")).to_contain_text(file_name)
        print(f"{file_name} → PASS")
        await browser.close()
