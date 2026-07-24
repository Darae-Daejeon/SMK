import re
import unittest
from pathlib import Path


HTML_PATH = Path(__file__).parents[1] / "ETRI" / "newsletter" / "da_logo.html"

EXPECTED_LINKS = [
    "https://forms.gle/wdT2K3nX5MCzDR4cA",
    "https://forms.gle/wdT2K3nX5MCzDR4cA",
    "https://daraebiz.com/",
    "https://www.youtube.com/@etri3581",
    "https://itec.etri.re.kr/httx/itec/main/index.do?",
    "https://drive.google.com/file/d/1hgaR8iTq-Tj5gEQn47vLQPvEXifuflJh/view?usp=drive_link",
    "https://drive.google.com/file/d/1V1ExsZVXwSAhlakpZH2_s9dG5wvBgAGC/view?usp=drive_link",
    "https://drive.google.com/file/d/1oHkGR1nhhJjDxISuPoXYsPcfAd9VrJ79/view?usp=drive_link",
    "https://drive.google.com/file/d/1lvwRyJBPH1sHLn7bbsZv3mUN77W1vC-0/view?usp=drive_link",
    "https://drive.google.com/file/d/1cJlqE2hX9QMi7OeFA8yzT6s-AF4WrMj6/view?usp=drive_link",
    "https://drive.google.com/file/d/1PSrz9pGqgeLttNUOU4NpgjtgfgrRtubf/view?usp=drive_link",
    "https://drive.google.com/file/d/1VOhdFRy5GT4P936wfcy-lkdxP_cRFR4u/view?usp=drive_link",
    "https://drive.google.com/file/d/1xbAHKq56G782pyq7Huh_j9aeFhS3Uvq7/view?usp=drive_link",
    "https://drive.google.com/file/d/1aST-XPjI_ppy1bmh6ZsZzVCUkNJP1xCX/view?usp=drive_link",
    "https://drive.google.com/file/d/1mtKaEEzeDPiWLgu6nPovK-IEayH31bnH/view?usp=drive_link",
    "https://drive.google.com/file/d/1-SHC_iQHbiSGBXShliD48TCiGMeGqHV8/view?usp=drive_link",
    "https://drive.google.com/file/d/1j1wZ1U8-uEQ5FjmUsJVCw4mEv_mMpfwY/view?usp=drive_link",
]


class DaLogoHtmlTests(unittest.TestCase):
    def test_preserves_all_17_links_in_the_image_map(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        areas = re.findall(r"<area\b[^>]+>", html, flags=re.DOTALL)
        hrefs = [re.search(r'href="([^"]+)"', area).group(1) for area in areas]

        self.assertEqual(EXPECTED_LINKS, hrefs)
        self.assertTrue(all('target="_blank"' in area for area in areas))
        self.assertTrue(all('coords="' in area for area in areas))
        self.assertIn('usemap="#newsletter-map"', html)
        self.assertIn('width="800"', html)
        self.assertIn('height="2137"', html)


if __name__ == "__main__":
    unittest.main()
