# ETRI Medical AI Newsletter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ETRI 의료·헬스케어 인공지능 기술 4종을 기업에 소개하고 각 공개 SMK로 연결하는 600px 폭의 이메일 뉴스레터 HTML과 PNG 자산을 제작한다.

**Architecture:** `scripts/build_etri_newsletter.py`가 기술 메타데이터와 기존 ETRI 대표 이미지를 입력으로 받아 뉴스레터용 PNG 자산과 표 기반 HTML을 생성한다. `tests/test_etri_newsletter.py`는 공개 링크, 연락처, 이메일 호환 구조, 이미지 치수와 로컬 자산 경로를 검사하고, Playwright 검증은 데스크톱·모바일 렌더링과 외부 리소스 오류를 확인한다.

**Tech Stack:** Python 3, Pillow, HTML5 table layout, inline CSS, Playwright Chromium, unittest

## Global Constraints

- 메일 본문 기준 폭은 `600px`다.
- 기술 카드 4개는 각각 별도 PNG 이미지와 별도 `<a>` 링크를 사용한다.
- 링크는 `https://darae-daejeon.github.io/SMK/ETRI/tech-01.html`부터 `tech-04.html`까지 사용한다.
- 이메일은 `mailto:yhj@daraebiz.com`으로 연결한다.
- 전화번호는 `tel:042-716-7084`로 연결한다.
- 프레젠테이션용 `<table>`과 인라인 스타일을 사용한다.
- 자바스크립트, 외부 폰트, CSS 그리드, 플렉스 레이아웃, 이미지맵은 사용하지 않는다.
- 이미지의 `width`, `height`, 대체 텍스트를 명시한다.
- 기존 ETRI SMK의 원본 기반 대표 이미지를 재사용한다.
- GitHub Pages 배포 설정과 기존 SMK 상세 페이지는 수정하지 않는다.

---

### Task 1: 뉴스레터 구조 계약 테스트

**Files:**
- Create: `tests/test_etri_newsletter.py`
- Verify: `ETRI/tech-01.html`
- Verify: `ETRI/tech-02.html`
- Verify: `ETRI/tech-03.html`
- Verify: `ETRI/tech-04.html`

**Interfaces:**
- Consumes: `ETRI/newsletter/etri-medical-ai-newsletter.html`과 `ETRI/newsletter/assets/*.png`
- Produces: 뉴스레터 파일·링크·연락처·이미지 계약을 검사하는 `EtriNewsletterTests`

- [ ] **Step 1: 실패하는 계약 테스트 작성**

```python
import re
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
NEWSLETTER = ROOT / "ETRI" / "newsletter" / "etri-medical-ai-newsletter.html"
ASSET_DIR = ROOT / "ETRI" / "newsletter" / "assets"


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
            src = re.search(r'src="([^"]+)"', tag).group(1)
            width = int(re.search(r'width="(\d+)"', tag).group(1))
            height = int(re.search(r'height="(\d+)"', tag).group(1))
            self.assertRegex(tag, r'alt="[^"]+"')
            path = NEWSLETTER.parent / src
            self.assertTrue(path.exists(), path)
            with Image.open(path) as image:
                self.assertEqual(image.size, (width, height))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 테스트가 산출물 누락으로 실패하는지 확인**

Run: `python -m unittest tests.test_etri_newsletter -v`

Expected: `ETRI/newsletter/etri-medical-ai-newsletter.html` 누락으로 FAIL

- [ ] **Step 3: 테스트 파일만 커밋**

```bash
git add tests/test_etri_newsletter.py
git commit -m "test: define ETRI newsletter contract"
```

---

### Task 2: 뉴스레터 이미지와 HTML 생성기

**Files:**
- Create: `scripts/build_etri_newsletter.py`
- Create: `ETRI/newsletter/etri-medical-ai-newsletter.html`
- Create: `ETRI/newsletter/assets/newsletter-header.png`
- Create: `ETRI/newsletter/assets/tech-01-card.png`
- Create: `ETRI/newsletter/assets/tech-02-card.png`
- Create: `ETRI/newsletter/assets/tech-03-card.png`
- Create: `ETRI/newsletter/assets/tech-04-card.png`
- Test: `tests/test_etri_newsletter.py`

**Interfaces:**
- Consumes: `ETRI/assets/tech-01/representative.png`부터 `ETRI/assets/tech-04/representative.png`까지와 고정 `TECHNOLOGIES` 메타데이터
- Produces: `build_assets() -> list[Path]`, `build_html() -> Path`, 600px 폭의 PNG 5개와 발송용 HTML 1개

- [ ] **Step 1: 기술 메타데이터와 이미지 렌더링 함수 구현**

```python
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "ETRI" / "newsletter"
ASSET_DIR = OUTPUT_DIR / "assets"
TECHNOLOGIES = [
    {
        "number": "01",
        "title": "미래 건강 예측을 위한 의료지능 딥러닝 엔진 기술",
        "value": "개인의 의료 데이터를 분석해 미래 건강 위험을 예측",
        "field": "의료 데이터 분석 · 미래 건강 예측",
        "source": ROOT / "ETRI" / "assets" / "tech-01" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-01.html",
        "accent": "#17A7A0",
    },
    {
        "number": "02",
        "title": "미래 건강상태 및 예후 예측을 위한 헬스케어 인공지능 기술",
        "value": "불확실성을 반영한 건강상태와 예후 확률 예측",
        "field": "확률 기반 예후 예측 · 임상 의사결정 지원",
        "source": ROOT / "ETRI" / "assets" / "tech-02" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-02.html",
        "accent": "#2878D0",
    },
    {
        "number": "03",
        "title": "개인 맞춤형 건강 관리 프로그램을 계획하는 인공지능 헬스케어 기술",
        "value": "개인의 상태와 목표에 맞춘 건강 관리 계획 수립",
        "field": "맞춤형 건강 관리 · 치료계획 최적화",
        "source": ROOT / "ETRI" / "assets" / "tech-03" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-03.html",
        "accent": "#6557C8",
    },
    {
        "number": "04",
        "title": "미래 건강 상태의 맞춤형 예측 및 최적 관리를 위한 인공지능 기술",
        "value": "개인별 미래 건강상태 예측과 관리 전략 최적화",
        "field": "맞춤형 예측 · 건강 관리 최적화",
        "source": ROOT / "ETRI" / "assets" / "tech-04" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-04.html",
        "accent": "#D06C43",
    },
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def cover(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as image:
        converted = image.convert("RGB")
        scale = max(size[0] / converted.width, size[1] / converted.height)
        resized = converted.resize((round(converted.width * scale), round(converted.height * scale)))
        left = (resized.width - size[0]) // 2
        top = (resized.height - size[1]) // 2
        return resized.crop((left, top, left + size[0], top + size[1]))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def build_assets() -> list[Path]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    header = Image.new("RGB", (600, 250), "#102A43")
    draw = ImageDraw.Draw(header)
    draw.rounded_rectangle((32, 28, 174, 62), radius=17, fill="#17A7A0")
    draw.text((50, 35), "ETRI TECHNOLOGY", font=load_font(15, True), fill="white")
    draw.text((32, 88), "의료·헬스케어 AI", font=load_font(36, True), fill="white")
    draw.text((32, 138), "기업의 다음 서비스를 위한 기술 4선", font=load_font(24, True), fill="#8EE3DC")
    draw.text((32, 194), "예측 · 예후 · 맞춤형 계획 · 최적 관리", font=load_font(16), fill="#D8E7F2")
    header_path = ASSET_DIR / "newsletter-header.png"
    header.save(header_path, optimize=True)

    outputs = [header_path]
    for tech in TECHNOLOGIES:
        canvas = Image.new("RGB", (600, 300), "#FFFFFF")
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((0, 0, 12, 300), fill=tech["accent"])
        draw.rounded_rectangle((30, 24, 92, 56), radius=16, fill=tech["accent"])
        draw.text((49, 31), tech["number"], font=load_font(14, True), fill="white")
        title_font = load_font(22, True)
        y = 76
        for line in wrap_text(draw, tech["title"], title_font, 288)[:3]:
            draw.text((32, y), line, font=title_font, fill="#102A43")
            y += 34
        draw.text((32, 186), tech["value"], font=load_font(14), fill="#40566B")
        draw.text((32, 218), tech["field"], font=load_font(13, True), fill=tech["accent"])
        draw.rounded_rectangle((32, 252, 166, 282), radius=15, fill="#102A43")
        draw.text((53, 258), "SMK 자세히 보기", font=load_font(13, True), fill="white")
        visual = cover(tech["source"], (240, 300))
        canvas.paste(visual, (360, 0))
        path = ASSET_DIR / f"tech-{tech['number']}-card.png"
        canvas.save(path, optimize=True)
        outputs.append(path)
    return outputs
```

- [ ] **Step 2: 600px 표 기반 HTML 생성 함수 구현**

```python
def build_html() -> Path:
    cards = []
    for tech in TECHNOLOGIES:
        cards.append(f'''<tr><td style="padding:0 0 14px 0;">
          <a href="{tech['url']}" target="_blank" rel="noopener noreferrer" style="display:block; text-decoration:none;">
            <img src="assets/tech-{tech['number']}-card.png" width="600" height="300" alt="{tech['title']} SMK 자세히 보기" style="display:block; width:600px; max-width:100%; height:auto; border:0;">
          </a>
        </td></tr>''')

    html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ETRI 의료 AI 기술이전 안내</title></head>
<body style="margin:0; padding:0; background:#eef2f6;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse; background:#eef2f6;"><tr><td align="center" style="padding:24px 0;">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:600px; max-width:100%; border-collapse:collapse; background:#ffffff;">
<tr><td><img src="assets/newsletter-header.png" width="600" height="250" alt="ETRI 의료 헬스케어 AI 기술이전 안내" style="display:block; width:600px; max-width:100%; height:auto; border:0;"></td></tr>
<tr><td style="padding:28px 32px 20px 32px; font-family:'Malgun Gothic',Arial,sans-serif; color:#263445; font-size:15px; line-height:1.7;">기업의 디지털 헬스케어 서비스 개발과 고도화에 활용 가능한 ETRI 기술 4종을 소개합니다.</td></tr>
{''.join(cards)}
<tr><td style="padding:30px 32px; background:#102a43; color:#ffffff; font-family:'Malgun Gothic',Arial,sans-serif; font-size:15px; line-height:1.8;">기술이전 및 사업화 상담<br><a href="mailto:yhj@daraebiz.com" style="color:#8ee3dc; text-decoration:none;">yhj@daraebiz.com</a> · <a href="tel:042-716-7084" style="color:#8ee3dc; text-decoration:none;">042-716-7084</a></td></tr>
</table></td></tr></table></body></html>'''
    output = OUTPUT_DIR / "etri-medical-ai-newsletter.html"
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    assets = build_assets()
    html_path = build_html()
    print(f"generated {len(assets)} images and {html_path}")
```

- [ ] **Step 3: 생성기를 실행해 PNG와 HTML 생성**

Run: `python scripts/build_etri_newsletter.py`

Expected: `ETRI/newsletter/assets`에 PNG 5개, `ETRI/newsletter`에 HTML 1개 생성

- [ ] **Step 4: 계약 테스트 통과 확인**

Run: `python -m unittest tests.test_etri_newsletter -v`

Expected: 4 tests PASS

- [ ] **Step 5: 생성기와 산출물 커밋**

```bash
git add scripts/build_etri_newsletter.py ETRI/newsletter tests/test_etri_newsletter.py
git commit -m "feat: add ETRI medical AI newsletter"
```

---

### Task 3: 데스크톱·모바일 렌더링 QA

**Files:**
- Create: `scripts/verify_etri_newsletter.py`
- Create: `tmp/etri-newsletter/desktop.png`
- Create: `tmp/etri-newsletter/mobile.png`
- Modify: `scripts/build_etri_newsletter.py` only if rendered defects require asset or HTML corrections
- Modify: `ETRI/newsletter/etri-medical-ai-newsletter.html` only through the generator

**Interfaces:**
- Consumes: `file:///C:/Users/JEON/Documents/기술판매/ETRI/newsletter/etri-medical-ai-newsletter.html`
- Produces: 600px 데스크톱 화면과 360px 모바일 화면의 렌더링 증거, `0` failed resources, `0` console errors

- [ ] **Step 1: 데스크톱·모바일 화면 캡처**

```python
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "ETRI" / "newsletter" / "etri-medical-ai-newsletter.html").as_uri()
OUTPUT = ROOT / "tmp" / "etri-newsletter"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for name, viewport in [
                ("desktop", {"width": 900, "height": 1000}),
                ("mobile", {"width": 360, "height": 800}),
            ]:
                page = browser.new_page(viewport=viewport)
                console_errors: list[str] = []
                failed_resources: list[str] = []
                page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
                page.on("requestfailed", lambda request: failed_resources.append(request.url))
                page.goto(URL, wait_until="networkidle")
                assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
                assert not console_errors, console_errors
                assert not failed_resources, failed_resources
                page.screenshot(path=str(OUTPUT / f"{name}.png"), full_page=True)
                page.close()
        finally:
            browser.close()
    print("2 screenshots / 0 overflow / 0 console errors / 0 failed resources")


if __name__ == "__main__":
    main()
```

Run: `python scripts/verify_etri_newsletter.py`

Expected: `desktop.png`, `mobile.png`, horizontal overflow assertion PASS, console errors 0

- [ ] **Step 2: 두 캡처를 원본 크기로 시각 검사**

- 데스크톱: 600px 뉴스레터가 중앙 정렬되고 카드 사이 간격이 일정해야 한다.
- 모바일: 카드가 360px 화면에 비율대로 축소되고 기술명과 연락처가 잘리지 않아야 한다.
- 공통: 글자 겹침, 이미지 늘어짐, 흐린 대표 이미지, 비정상 공백이 없어야 한다.

- [ ] **Step 3: 전체 테스트 재실행**

Run: `python -m unittest tests.test_etri_newsletter tests.test_etri_smk -v`

Expected: 뉴스레터 테스트와 기존 ETRI SMK 테스트 전체 PASS

- [ ] **Step 4: 작업 범위 확인**

Run: `git status --short`

Expected: 기존 사용자 변경은 보존되고 뉴스레터 관련 필수 파일은 커밋 상태

- [ ] **Step 5: 검증기와 렌더링 수정사항 커밋**

```bash
git add scripts/verify_etri_newsletter.py scripts/build_etri_newsletter.py ETRI/newsletter
git commit -m "test: verify ETRI newsletter rendering"
```
