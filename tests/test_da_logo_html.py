import re
import unittest
from pathlib import Path


HTML_PATH = Path(__file__).parents[1] / "ETRI" / "newsletter" / "da_logo.html"

EXPECTED_LINKS = [
    "https://forms.gle/5DG5d9RDGpjtquh4A",
    "https://forms.gle/5DG5d9RDGpjtquh4A",
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
    def test_preserves_all_17_links_as_responsive_hotspots(self):
        html = HTML_PATH.read_text(encoding="utf-8")
        anchors = re.findall(r'<a class="hotspot"[^>]+>', html)
        hrefs = [re.search(r'href="([^"]+)"', anchor).group(1) for anchor in anchors]

        self.assertEqual(EXPECTED_LINKS, hrefs)
        self.assertTrue(all('target="_blank"' in anchor for anchor in anchors))
        self.assertTrue(all('data-coords="' in anchor for anchor in anchors))
        self.assertIn("left: calc(var(--x) / 800 * 100%);", html)
        self.assertIn("top: calc(var(--y) / 2137 * 100%);", html)


if __name__ == "__main__":
    unittest.main()
