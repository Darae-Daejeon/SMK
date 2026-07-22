import base64
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ETRI" / "deadwater-newsletter" / "reference" / "deadwater.html"
ASSETS = ROOT / "ETRI" / "deadwater-newsletter" / "assets"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r"font-family:\s*[\"'](?P<family>[^\"']+)[\"'];.*?"
        r"src:\s*url\([\"']?data:font/woff2;base64,(?P<data>[A-Za-z0-9+/=]+)[\"']?\)",
        re.S,
    )
    fonts = {match.group("family"): match.group("data") for match in pattern.finditer(text)}
    wanted = {"Humane Local": "humane.woff2", "Inter Local": "inter.woff2"}

    ASSETS.mkdir(parents=True, exist_ok=True)
    for family, filename in wanted.items():
        if family not in fonts:
            raise RuntimeError(f"Font not found: {family}")
        (ASSETS / filename).write_bytes(base64.b64decode(fonts[family]))


if __name__ == "__main__":
    main()
