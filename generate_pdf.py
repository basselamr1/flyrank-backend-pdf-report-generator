from pathlib import Path

from playwright.sync_api import sync_playwright

from report_service import get_report_data
from report_template import build_report_html


def generate_pdf(report_id: int) -> str:
    report = get_report_data()
    html = build_report_html(report)

    output_path = Path("reports") / f"{report_id}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_content(html)

        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
        )

        browser.close()

    return str(output_path)