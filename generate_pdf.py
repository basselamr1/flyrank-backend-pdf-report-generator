import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from main import get_report_data
from report_template import build_report_html


async def generate_pdf():
    report = get_report_data()

    html = build_report_html(report)

    output_path = Path("reports/test.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:

        browser = await playwright.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        await page.set_content(html)

        await page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
        )

        await browser.close()

    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    asyncio.run(generate_pdf())