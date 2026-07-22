from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ETRI" / "deadwater-newsletter" / "index.html"
REFERENCE = PAGE.parent / "reference" / "deadwater.html"
OUT = ROOT / "tmp" / "etri-deadwater-newsletter"


def add_to_combined(canvas: Image.Image, image: Image.Image, x: int, label: str) -> None:
    width = 520
    ratio = width / image.width
    resized = image.resize((width, round(image.height * ratio)), Image.Resampling.LANCZOS)
    canvas.paste(resized, (x, 52))
    draw = ImageDraw.Draw(canvas)
    draw.text((x, 15), label, fill="#111111")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    console_errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.goto(PAGE.as_uri(), wait_until="load")
        page.locator(".reveal").evaluate_all("els => els.forEach(el => el.classList.add('is-visible'))")
        page.screenshot(path=str(OUT / "desktop.png"), full_page=True)

        shell_width = page.locator(".page-shell").evaluate("el => Math.round(el.getBoundingClientRect().width)")
        assert shell_width == 1440, shell_width
        assert page.locator(".project-link").count() == 4
        assert page.locator("video").count() == 0
        assert page.locator("#expertise").count() == 0

        second = page.locator(".project-link").nth(1)
        second.hover(position={"x": 250, "y": 80})
        page.wait_for_timeout(250)
        assert page.locator(".project-preview").get_attribute("data-visible") == "true"
        assert page.locator(".project-preview img").get_attribute("src") == "assets/smk-02.png"
        page.screenshot(path=str(OUT / "hover-tech-02.png"), full_page=False)

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        mobile.goto(PAGE.as_uri(), wait_until="load")
        mobile.screenshot(path=str(OUT / "mobile.png"), full_page=True)
        assert mobile.locator("body").evaluate("el => el.scrollWidth") == 390

        reference = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        reference.goto(REFERENCE.as_uri(), wait_until="load")
        reference.locator(".reveal").evaluate_all("els => els.forEach(el => el.classList.add('is-visible'))")
        expertise = reference.locator("#expertise")
        clip_height = round(expertise.bounding_box()["y"]) if expertise.count() else 1500
        reference.screenshot(
            path=str(OUT / "reference-before-expertise.png"),
            clip={"x": 0, "y": 0, "width": 1440, "height": clip_height},
        )
        browser.close()

    if console_errors:
        raise AssertionError(f"console errors: {console_errors}")

    source = Image.open(OUT / "reference-before-expertise.png").convert("RGB")
    result = Image.open(OUT / "desktop.png").convert("RGB")
    scaled_source_height = round(source.height * 520 / source.width)
    scaled_result_height = round(result.height * 520 / result.width)
    combined = Image.new("RGB", (1080, max(scaled_source_height, scaled_result_height) + 72), "#e8e8e4")
    add_to_combined(combined, source, 15, "REFERENCE — DEADWATER / BEFORE EXPERTISE")
    add_to_combined(combined, result, 545, "IMPLEMENTATION — ETRI IP TECHNOLOGY LIST")
    combined.save(OUT / "comparison.png", quality=95)


if __name__ == "__main__":
    main()
