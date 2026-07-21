from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
ETRI_DIR = ROOT / "ETRI"
QA_DIR = ROOT / "tmp" / "etri-smk" / "qa"
TECH_FILES = [ETRI_DIR / f"tech-{index:02d}.html" for index in range(1, 5)]
A4_LANDSCAPE = (841.89, 595.28)


def is_a4_landscape(width: float, height: float, tolerance: float = 1.0) -> bool:
    expected_width, expected_height = A4_LANDSCAPE
    return abs(width - expected_width) <= tolerance and abs(height - expected_height) <= tolerance


def static_checks() -> list[str]:
    errors: list[str] = []
    css_path = ETRI_DIR / "assets" / "smk-print.css"
    if not css_path.is_file():
        errors.append(f"공통 CSS 누락: {css_path}")
    for html_path in TECH_FILES:
        if not html_path.is_file():
            errors.append(f"HTML 누락: {html_path}")
            continue
        html = html_path.read_text(encoding="utf-8")
        if html.count('class="smk-sheet"') != 1:
            errors.append(f"smk-sheet 개수 오류: {html_path.name}")
    return errors


def render_with_chromium() -> list[str]:
    from playwright.sync_api import sync_playwright

    QA_DIR.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for html_path in TECH_FILES:
            slug = html_path.stem
            page = browser.new_page(viewport={"width": 1440, "height": 1024}, device_scale_factor=1)
            console_errors: list[str] = []
            failed_requests: list[str] = []
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("requestfailed", lambda request: failed_requests.append(request.url))
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
            page.screenshot(path=str(QA_DIR / f"{slug}-screen.png"), full_page=False)
            overflow = page.locator(".smk-sheet").evaluate(
                "el => ({width: el.scrollWidth - el.clientWidth, height: el.scrollHeight - el.clientHeight})"
            )
            if overflow["width"] > 1 or overflow["height"] > 1:
                errors.append(f"{slug}: sheet overflow {overflow}")
            clipped_sections = page.locator(".section-block").evaluate_all(
                "els => els.map((el, index) => ({index, width: el.scrollWidth - el.clientWidth, height: el.scrollHeight - el.clientHeight}))"
                ".filter(item => item.width > 1 || item.height > 1)"
            )
            if clipped_sections:
                errors.append(f"{slug}: clipped sections {clipped_sections}")
            clipped_tags = page.locator(".tag").evaluate_all(
                "els => els.map((el, index) => ({index, width: el.scrollWidth - el.clientWidth}))"
                ".filter(item => item.width > 1)"
            )
            if clipped_tags:
                errors.append(f"{slug}: clipped tags {clipped_tags}")
            if console_errors:
                errors.append(f"{slug}: console errors: {' | '.join(console_errors)}")
            if failed_requests:
                errors.append(f"{slug}: failed resources: {' | '.join(failed_requests)}")
            page.pdf(
                path=str(QA_DIR / f"{slug}-print.pdf"),
                format="A4",
                landscape=True,
                print_background=True,
                prefer_css_page_size=True,
                display_header_footer=False,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            page.close()
        browser.close()
    return errors


def validate_pdfs() -> list[str]:
    errors: list[str] = []
    for html_path in TECH_FILES:
        pdf_path = QA_DIR / f"{html_path.stem}-print.pdf"
        if not pdf_path.is_file():
            errors.append(f"PDF 누락: {pdf_path}")
            continue
        reader = PdfReader(pdf_path)
        if len(reader.pages) != 1:
            errors.append(f"{pdf_path.name}: {len(reader.pages)} pages")
            continue
        box = reader.pages[0].mediabox
        width = float(box.width)
        height = float(box.height)
        if not is_a4_landscape(width, height):
            errors.append(f"{pdf_path.name}: {width:.2f}x{height:.2f}pt")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    errors = static_checks()
    if not args.static_only and not errors:
        errors.extend(render_with_chromium())
        errors.extend(validate_pdfs())

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.static_only:
        print("4 HTML / static checks passed")
    else:
        print("4 HTML / 4 PDF / 4 single-page A4 landscape / 0 errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
