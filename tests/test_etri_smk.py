import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ETRI = ROOT / "ETRI"
TECH_FILES = [ETRI / f"tech-{index:02d}.html" for index in range(1, 5)]


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.local_assets: list[str] = []
        self.sheet_count = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        if "smk-sheet" in classes:
            self.sheet_count += 1
        for key in ("src", "href"):
            value = values.get(key, "")
            parsed = urlparse(value)
            if value and not parsed.scheme and not value.startswith("#"):
                self.local_assets.append(value)


class EtriSmkTests(unittest.TestCase):
    def test_a4_landscape_measurement_accepts_one_point_tolerance(self):
        from scripts.verify_etri_smk import is_a4_landscape

        self.assertTrue(is_a4_landscape(841.89, 595.28))
        self.assertTrue(is_a4_landscape(841.0, 596.0))
        self.assertFalse(is_a4_landscape(595.28, 841.89))

    def test_print_css_declares_exact_a4_landscape_contract(self):
        css = (ETRI / "assets" / "smk-print.css").read_text(encoding="utf-8")
        compact = re.sub(r"\s+", " ", css)
        self.assertIn("size: A4 landscape", compact)
        self.assertIn("width: 297mm", compact)
        self.assertIn("height: 210mm", compact)
        self.assertIn("padding: 8mm", compact)
        self.assertIn("print-color-adjust: exact", compact)

    def test_each_technology_has_one_sheet_and_existing_local_assets(self):
        for html_path in TECH_FILES:
            with self.subTest(html=html_path.name):
                parser = AssetParser()
                parser.feed(html_path.read_text(encoding="utf-8"))
                self.assertEqual(parser.sheet_count, 1)
                for asset in parser.local_assets:
                    self.assertTrue((html_path.parent / asset).resolve().is_file(), asset)

    def test_each_technology_includes_source_and_etri_link(self):
        tech_ids = [
            "3610-2021-02099",
            "3610-2023-00011",
            "5310-2023-00421",
            "5310-2025-00388",
        ]
        for html_path, tech_id in zip(TECH_FILES, tech_ids):
            with self.subTest(html=html_path.name):
                html = html_path.read_text(encoding="utf-8")
                self.assertIn(tech_id, html)
                self.assertIn("https://itec.etri.re.kr/", html)
                self.assertRegex(html, r"원본 자료[^<]*(PPTX|PDF)")

    def test_index_lists_exactly_four_smk_pages(self):
        html = (ETRI / "index.html").read_text(encoding="utf-8")
        self.assertIn("총 4건", html)
        self.assertNotIn("등록된 SMK가 없습니다.", html)
        for index in range(1, 5):
            self.assertEqual(html.count(f'href="tech-{index:02d}.html"'), 1)


if __name__ == "__main__":
    unittest.main()
