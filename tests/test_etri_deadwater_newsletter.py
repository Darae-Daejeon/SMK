from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ETRI" / "deadwater-newsletter" / "index.html"
ASSETS = PAGE.parent / "assets"


def test_original_deadwater_skeleton_is_preserved():
    html = PAGE.read_text(encoding="utf-8")

    # The source is a large self-contained document with embedded fonts.
    # The video/showreel bitmap is intentionally removed; embedded source fonts remain.
    assert len(html) > 90_000
    for selector in (
        'class="page-shell"',
        'class="studio-header"',
        'class="hero"',
        'class="hero-wordmark etri-hero-title"',
        'class="projects"',
        'class="project-list"',
        'class="project-preview"',
        'class="custom-cursor"',
    ):
        assert selector in html

    assert ".project-name {" in html
    assert "font-size: 80px" in html
    assert "--canvas-width" not in html
    assert "max-width: 800px" not in html


def test_etri_content_replaces_only_source_content():
    html = PAGE.read_text(encoding="utf-8")

    assert "ETRI IP거래 기술목록" in html
    assert 'src="assets/etri-logo.png"' in html
    assert html.count("한국전자통신연구원 IP거래 기술 목록") == 1
    assert ">ETRI IP<" not in html
    assert 'class="hero-copy"' not in html
    assert '<div class="showreel"' not in html.lower()
    assert "const showreel" not in html.lower()
    assert "<video" not in html.lower()
    assert 'id="expertise"' not in html
    assert "Expertise" not in html
    assert "ETRI기술번호" not in html
    assert "ETRI 기술번호" not in html
    assert '>SMK 보기</div>' in html
    assert '>Lecture</div>' not in html

    for number in range(1, 5):
        url = f"https://darae-daejeon.github.io/SMK/ETRI/tech-0{number}.html"
        assert html.count(url) == 1
        assert f'data-image="assets/smk-0{number}.png"' in html
        assert (ASSETS / f"smk-0{number}.png").is_file()

    assert html.count('target="_blank"') == 4
    assert "특허출원번호" not in html
    assert html.count('class="project-name"') == 4
    assert "white-space: nowrap" in html
    assert "z-index: 10" in html


def test_representative_patent_application_numbers():
    html = PAGE.read_text(encoding="utf-8")
    for number in (
        "10-2018-0147862",
        "10-2021-0179326",
        "10-2022-0189362",
        "10-2024-0172319",
    ):
        assert number in html
