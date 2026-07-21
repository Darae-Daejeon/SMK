import re
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
NEWSLETTER = ROOT / "ETRI" / "newsletter" / "etri-medical-ai-newsletter.html"
PUBLIC_ASSET_BASE = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/"


class EtriNewsletterTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(NEWSLETTER.exists(), NEWSLETTER)
        self.html = NEWSLETTER.read_text(encoding="utf-8")

    def test_uses_email_safe_structure(self):
        self.assertIn('role="presentation"', self.html)
        self.assertIn('width="600"', self.html)
        self.assertNotIn("<script", self.html.lower())
        self.assertNotIn("<map", self.html.lower())
        self.assertNotRegex(self.html.lower(), r"display\s*:\s*(grid|flex)")

    def test_has_four_unique_smk_links(self):
        for number in range(1, 5):
            url = f"https://darae-daejeon.github.io/SMK/ETRI/tech-{number:02d}.html"
            self.assertEqual(self.html.count(url), 1, url)

    def test_has_clickable_contact_details(self):
        self.assertIn('href="mailto:yhj@daraebiz.com"', self.html)
        self.assertIn('href="tel:042-716-7084"', self.html)
        self.assertIn("yhj@daraebiz.com", self.html)
        self.assertIn("042-716-7084", self.html)

    def test_all_local_images_exist_and_declare_dimensions(self):
        tags = re.findall(r"<img\b[^>]*>", self.html, re.I)
        self.assertGreaterEqual(len(tags), 5)
        for tag in tags:
            src_match = re.search(r'src="([^"]+)"', tag)
            width_match = re.search(r'width="(\d+)"', tag)
            height_match = re.search(r'height="(\d+)"', tag)
            self.assertIsNotNone(src_match, tag)
            self.assertIsNotNone(width_match, tag)
            self.assertIsNotNone(height_match, tag)
            self.assertRegex(tag, r'alt="[^"]+"')
            self.assertTrue(src_match.group(1).startswith(PUBLIC_ASSET_BASE))
            relative_src = src_match.group(1).removeprefix(PUBLIC_ASSET_BASE)
            path = NEWSLETTER.parent / relative_src
            self.assertTrue(path.exists(), path)
            with Image.open(path) as image:
                self.assertEqual(
                    image.size,
                    (int(width_match.group(1)), int(height_match.group(1))),
                )


if __name__ == "__main__":
    unittest.main()
