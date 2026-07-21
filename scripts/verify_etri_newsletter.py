from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Route, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
NEWSLETTER = ROOT / "ETRI" / "newsletter" / "etri-medical-ai-newsletter.html"
ASSET_DIR = NEWSLETTER.parent / "assets"
PUBLIC_ASSET_PREFIX = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/assets/"
OUTPUT = ROOT / "tmp" / "etri-newsletter"


def serve_local_asset(route: Route) -> None:
    filename = route.request.url.removeprefix(PUBLIC_ASSET_PREFIX)
    path = ASSET_DIR / filename
    if not path.exists() or path.parent != ASSET_DIR:
        route.abort("failed")
        return
    route.fulfill(path=path, content_type="image/png")


def main() -> None:
    if not NEWSLETTER.exists():
        raise FileNotFoundError(NEWSLETTER)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            for name, viewport in [
                ("desktop", {"width": 900, "height": 1000}),
                ("mobile", {"width": 360, "height": 800}),
            ]:
                page = browser.new_page(viewport=viewport, device_scale_factor=1)
                console_errors: list[str] = []
                failed_resources: list[str] = []
                page.on(
                    "console",
                    lambda message: console_errors.append(message.text)
                    if message.type == "error"
                    else None,
                )
                page.on("requestfailed", lambda request: failed_resources.append(request.url))
                page.route(f"{PUBLIC_ASSET_PREFIX}*", serve_local_asset)
                page.goto(NEWSLETTER.as_uri(), wait_until="networkidle")

                overflow = page.evaluate(
                    "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                )
                if overflow:
                    measurements = page.evaluate(
                        """() => ({
                            viewport: document.documentElement.clientWidth,
                            document: document.documentElement.scrollWidth,
                            body: document.body.getBoundingClientRect().width,
                            tables: [...document.querySelectorAll('table')].map((element) => ({
                                declaredWidth: element.getAttribute('width'),
                                width: Math.round(element.getBoundingClientRect().width),
                                scrollWidth: element.scrollWidth
                            })),
                            images: [...document.querySelectorAll('img')].map((element) => ({
                                width: Math.round(element.getBoundingClientRect().width),
                                scrollWidth: element.scrollWidth
                            }))
                        })"""
                    )
                    raise AssertionError(f"{name}: horizontal overflow: {measurements}")
                if console_errors:
                    raise AssertionError(f"{name}: console errors: {console_errors}")
                if failed_resources:
                    raise AssertionError(f"{name}: failed resources: {failed_resources}")

                body_width = page.locator('table[width="600"]').first.evaluate(
                    "element => Math.round(element.getBoundingClientRect().width)"
                )
                expected_width = 600 if name == "desktop" else 360
                if body_width != expected_width:
                    raise AssertionError(
                        f"{name}: content width {body_width}px, expected {expected_width}px"
                    )

                page.screenshot(path=str(OUTPUT / f"{name}.png"), full_page=True)
                page.close()
        finally:
            browser.close()

    print("2 screenshots / 0 overflow / 0 console errors / 0 failed resources")


if __name__ == "__main__":
    main()
