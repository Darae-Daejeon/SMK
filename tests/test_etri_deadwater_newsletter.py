from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ETRI" / "deadwater-newsletter" / "index.html"
ASSETS = PAGE.parent / "assets"


def test_deadwater_newsletter_structure():
    html = PAGE.read_text(encoding="utf-8")

    assert "ETRI IP거래 기술목록" in html
    assert "--canvas-width: 800px" in html
    assert "ETRI기술번호" not in html
    assert "ETRI 기술번호" not in html
    assert "특허출원번호" in html
    assert "showreel" not in html.lower()
    assert "<video" not in html.lower()
    assert 'id="expertise"' not in html

    for number in range(1, 5):
        url = f"https://darae-daejeon.github.io/SMK/ETRI/tech-0{number}.html"
        assert html.count(url) == 1
        assert f'data-preview="assets/smk-0{number}.png"' in html
        assert (ASSETS / f"smk-0{number}.png").is_file()

    assert html.count('target="_blank"') == 4
    assert (ASSETS / "etri-logo.png").is_file()
    assert (ASSETS / "humane.woff2").is_file()
    assert (ASSETS / "inter.woff2").is_file()


def test_representative_patent_application_numbers():
    html = PAGE.read_text(encoding="utf-8")

    for number in (
        "10-2018-0147862",
        "10-2021-0179326",
        "10-2022-0189362",
        "10-2024-0172319",
    ):
        assert number in html

