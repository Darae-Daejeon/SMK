# KRIBB Strain SMK Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 하나의 공통 JSON과 공통 HTML 템플릿으로 KRIBB 균주 기술 목록·상세 SMK·반응형 사이드바·A4 세로 인쇄물을 제공한다.

**Architecture:** `KRIBB/data/technologies.json`을 단일 데이터 원본으로 사용한다. `index.html`은 기술 목록을, `smk.html?tech={id}`는 선택 기술의 01~08 고정 섹션을 브라우저 JavaScript로 렌더링한다. 화면 레이아웃과 인쇄 레이아웃을 분리하고, 인쇄 시 JavaScript가 섹션 전체 높이를 측정하여 A4 페이지 컨테이너에 섹션 단위로 재배치한다.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript ES Modules, SVG, Python `unittest`, Playwright, pypdf, Poppler

## Global Constraints

- GitHub Pages 정적 호스팅만 사용한다.
- 백엔드, 데이터베이스, BAT 파일, 프런트엔드 프레임워크를 사용하지 않는다.
- 공통 상세 HTML은 `KRIBB/smk.html` 1개만 사용한다.
- 모든 기술 데이터는 `KRIBB/data/technologies.json` 1개에 저장한다.
- 목차는 01~08 순서와 명칭을 고정한다.
- 화면 본문은 A4 규격으로 제한하지 않는다.
- 인쇄 시에만 A4 세로 2~3페이지를 적용한다.
- 인쇄 페이지 경계에서 목차 섹션 전체를 분할하지 않는다.
- 관련 데이터는 1~3개, 적용제품은 3~5개, IP 포트폴리오는 최대 5개로 제한한다.
- KRIBB 공식 국·영문 시그니처, 컬러 심벌, 흑백 심벌을 임의 변형 없이 사용한다.
- P2025-033 미공개 출원서 데이터는 공개 배포 대상에서 제외하고 로컬 검증용으로 표시한다.
- 기존 사용자 변경사항과 ETRI·catholic 파일은 수정하지 않는다.

---

## File Structure

```text
KRIBB/
├─ index.html                         # JSON 기반 기술 목록 랜딩페이지
├─ smk.html                           # 공통 상세 템플릿과 렌더링 마운트 지점
├─ data/
│  └─ technologies.json               # 공개·비공개 기술을 포함한 단일 데이터 원본
├─ css/
│  ├─ common.css                      # 디자인 토큰, 기본 서체, 공통 요소
│  ├─ landing.css                     # 기술 목록 전용 레이아웃
│  ├─ screen.css                      # 상세 화면·반응형 사이드바
│  └─ print.css                       # A4 세로 페이지와 인쇄 전용 요소
├─ js/
│  ├─ catalog.js                      # JSON 로드·검증·기술 검색
│  ├─ landing.js                      # 랜딩페이지 렌더링
│  ├─ smk-renderer.js                 # 01~08 상세 섹션 렌더링
│  ├─ charts.js                       # SVG 막대·선 차트 렌더링
│  ├─ sidebar.js                      # 스크롤 연동 사이드바·모바일 서랍
│  └─ print-layout.js                 # 섹션 단위 A4 페이지 조립
└─ assets/
   ├─ kribb-ci/
   │  ├─ kribb-signature-ko-en.png
   │  ├─ kribb-symbol-color.png
   │  └─ kribb-symbol-bw.png
   └─ motifs/
      └─ microbe-watermark.svg
scripts/
└─ verify_kribb_smk.py                # 로컬 서버·브라우저·PDF 통합 QA
tests/
├─ test_kribb_data.py                 # JSON 구조·범위·공개 상태 검증
├─ test_kribb_static.py               # HTML·CSS·JS·자산 계약 검증
└─ test_kribb_print.py                # PDF 페이지·섹션 분할 검증
```

---

### Task 1: KRIBB 데이터 계약과 예시 기술 데이터

**Files:**
- Create: `KRIBB/data/technologies.json`
- Create: `tests/test_kribb_data.py`

**Interfaces:**
- Produces: `catalog.technologies: Technology[]`
- Produces: `Technology.id`, `visibility`, `title`, `researcher`, `classification`, `strain`, `patent`, `experiments`, `charts`, `products`, `coreElements`, `utilizationSteps`, `portfolio`
- Consumes: 박승환 등록특허 PDF와 P2025-033 미공개 출원서 PDF

- [ ] **Step 1: Write the failing JSON contract test**

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "KRIBB" / "data" / "technologies.json"


class KribbDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.technologies = cls.data["technologies"]

    def test_ids_are_unique_and_required_sections_exist(self):
        ids = [item["id"] for item in self.technologies]
        self.assertEqual(len(ids), len(set(ids)))
        required = {
            "classification", "strain", "patent", "experiments", "charts",
            "products", "coreElements", "utilizationSteps", "portfolio",
        }
        for item in self.technologies:
            self.assertTrue(required.issubset(item), item["id"])

    def test_array_limits_match_template_contract(self):
        for item in self.technologies:
            self.assertIn(len(item["charts"]), range(1, 4))
            self.assertIn(len(item["products"]), range(3, 6))
            self.assertEqual(len(item["utilizationSteps"]), 4)
            self.assertLessEqual(len(item["portfolio"]), 5)

    def test_unpublished_application_is_not_public(self):
        p2025 = next(item for item in self.technologies if item["id"] == "p2025-033")
        self.assertEqual(p2025["visibility"], "private")
```

- [ ] **Step 2: Run the data test and verify failure**

Run: `python -m unittest tests.test_kribb_data -v`

Expected: FAIL because `KRIBB/data/technologies.json` does not exist.

- [ ] **Step 3: Create the catalog with both technology objects**

Use this top-level structure and exact field names:

```json
{
  "schemaVersion": 1,
  "technologies": [
    {
      "id": "park-1020220067778",
      "visibility": "public",
      "title": "암 조직을 선택 표적화하고 종양 성장을 억제하는 인체유래 유산균",
      "researcher": "박승환",
      "classification": {
        "major": "",
        "middle": "",
        "minor": "",
        "extension": ""
      },
      "strain": {
        "depositNumber": "KCTC 14228BP",
        "depositDate": "2020.07.06",
        "microorganismName": "Lactobacillus paracasei subsp. tolerance KGMB04157",
        "microorganismType": "세균",
        "aliases": ["KGMB04157", "V1bio04157", "BCT04157"],
        "origin": "한국인 장내 마이크로바이옴 유래",
        "coreFeature": "암 표적성·항암효과·진단 및 전달 플랫폼 확장"
      },
      "patent": {
        "title": "락티카제이바실러스 속 또는 락토바실러스 속 균주를 유효성분으로 포함하는 암 진단, 예방 또는 치료용 조성물",
        "number": "10-2833393",
        "differentiators": []
      },
      "experiments": [],
      "charts": [],
      "products": [],
      "coreElements": [],
      "utilizationSteps": [],
      "portfolio": [],
      "sources": []
    }
  ]
}
```

Complete the arrays from the supplied source files. For every chart include:

```json
{
  "id": "same-species-antitumor",
  "type": "bar",
  "title": "동일 종 균주 대비 항암효과",
  "unit": "세포 생존율 (%)",
  "labels": ["Control", "KCTC 14228BP", "KCTC 3189", "KCTC 3510"],
  "values": [100, 48, 92, 85],
  "sourceFigure": "등록특허 10-2833393 도면 9",
  "valueStatus": "estimated-from-figure"
}
```

Use `valueStatus` values only from `exact`, `estimated-from-figure`, or `qualitative`.

- [ ] **Step 4: Run the data contract test**

Run: `python -m unittest tests.test_kribb_data -v`

Expected: PASS with two unique technologies, valid list limits, and `p2025-033` marked private.

- [ ] **Step 5: Commit the data contract**

```powershell
git add -- KRIBB/data/technologies.json tests/test_kribb_data.py
git commit -m "feat: define KRIBB SMK technology data contract"
```

---

### Task 2: Common page shells, design tokens, and official CI assets

**Files:**
- Create: `KRIBB/index.html`
- Create: `KRIBB/smk.html`
- Create: `KRIBB/css/common.css`
- Create: `KRIBB/css/landing.css`
- Create: `KRIBB/assets/kribb-ci/kribb-signature-ko-en.png`
- Create: `KRIBB/assets/kribb-ci/kribb-symbol-color.png`
- Create: `KRIBB/assets/kribb-ci/kribb-symbol-bw.png`
- Create: `KRIBB/assets/motifs/microbe-watermark.svg`
- Create: `tests/test_kribb_static.py`

**Interfaces:**
- Produces: `#technology-list`, `#smk-root`, `#screen-sidebar`, `#print-root`, `#status-message`
- Produces: CSS tokens `--kribb-blue`, `--kribb-light-blue`, `--kribb-ink`, `--kribb-soft`
- Consumes: official CI archive `https://www.kribb.re.kr/file/ci_png.zip`

- [ ] **Step 1: Write failing static contract tests**

```python
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KRIBB = ROOT / "KRIBB"


class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])


class KribbStaticTests(unittest.TestCase):
    def test_page_mount_points_exist(self):
        expected = {
            "index.html": {"technology-list", "status-message"},
            "smk.html": {"smk-root", "screen-sidebar", "print-root", "status-message"},
        }
        for name, ids in expected.items():
            parser = IdParser()
            parser.feed((KRIBB / name).read_text(encoding="utf-8"))
            self.assertTrue(ids.issubset(parser.ids), name)

    def test_official_ci_assets_and_watermark_exist(self):
        for relative in (
            "assets/kribb-ci/kribb-signature-ko-en.png",
            "assets/kribb-ci/kribb-symbol-color.png",
            "assets/kribb-ci/kribb-symbol-bw.png",
            "assets/motifs/microbe-watermark.svg",
        ):
            self.assertTrue((KRIBB / relative).is_file(), relative)
```

- [ ] **Step 2: Run the static test and verify failure**

Run: `python -m unittest tests.test_kribb_static -v`

Expected: FAIL because the pages and assets do not exist.

- [ ] **Step 3: Create semantic page shells**

`KRIBB/index.html` must contain:

```html
<main class="landing-shell">
  <header class="landing-hero"></header>
  <p id="status-message" role="status" aria-live="polite"></p>
  <section id="technology-list" aria-label="기술 목록"></section>
</main>
<script type="module" src="./js/landing.js"></script>
```

`KRIBB/smk.html` must contain:

```html
<aside id="screen-sidebar" class="screen-only" aria-label="문서 목차"></aside>
<p id="status-message" role="status" aria-live="polite"></p>
<main id="smk-root" class="screen-only"></main>
<main id="print-root" class="print-only"></main>
<script type="module" src="./js/smk-renderer.js"></script>
```

- [ ] **Step 4: Add KRIBB design tokens and official assets**

Define in `common.css`:

```css
:root {
  --kribb-blue: #071f66;
  --kribb-light-blue: #64c3ec;
  --kribb-ink: #13233a;
  --kribb-muted: #607086;
  --kribb-line: #dce5ef;
  --kribb-soft: #f1f6fa;
  --kribb-white: #ffffff;
  --content-max: 1180px;
}
```

Extract the official PNG archive, visually identify the color symbol, black symbol, and Korean/English signature, then copy them under normalized filenames. Do not recolor, crop, stretch, or redraw the logo.

- [ ] **Step 5: Run static tests**

Run: `python -m unittest tests.test_kribb_static -v`

Expected: PASS for mount points and four required assets.

- [ ] **Step 6: Commit the page shells and assets**

```powershell
git add -- KRIBB/index.html KRIBB/smk.html KRIBB/css/common.css KRIBB/css/landing.css KRIBB/assets tests/test_kribb_static.py
git commit -m "feat: add KRIBB SMK page shells and brand assets"
```

---

### Task 3: Catalog loader and JSON-driven landing page

**Files:**
- Create: `KRIBB/js/catalog.js`
- Create: `KRIBB/js/landing.js`
- Modify: `KRIBB/css/landing.css`
- Create: `scripts/verify_kribb_smk.py`

**Interfaces:**
- Produces: `loadCatalog(url): Promise<Catalog>`
- Produces: `getTechnology(catalog, id): Technology | null`
- Produces: `getPublicTechnologies(catalog): Technology[]`
- Consumes: `#technology-list`, `#status-message`

- [ ] **Step 1: Create a failing browser verification for the landing page**

Create `scripts/verify_kribb_smk.py` with a local `ThreadingHTTPServer`, a Playwright Chromium session, an `errors` list, the `--screen-only` argument, and the following landing-page assertions:

```python
page.goto(f"{base_url}/KRIBB/", wait_until="networkidle")
cards = page.locator("[data-technology-id]")
if cards.count() != 1:
    errors.append(f"landing: expected 1 public card, got {cards.count()}")
if page.locator('[data-technology-id="p2025-033"]').count():
    errors.append("landing: private technology is visible")
href = page.locator('[data-technology-id="park-1020220067778"] a').get_attribute("href")
if href != "./smk.html?tech=park-1020220067778":
    errors.append(f"landing: unexpected detail href {href}")
```

- [ ] **Step 2: Run the browser verification and verify failure**

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: FAIL because `catalog.js` and `landing.js` do not exist.

- [ ] **Step 3: Implement catalog loading and validation**

`catalog.js` exports:

```javascript
export async function loadCatalog(url = "./data/technologies.json") {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`기술 데이터 로드 실패: HTTP ${response.status}`);
  const catalog = await response.json();
  if (catalog.schemaVersion !== 1 || !Array.isArray(catalog.technologies)) {
    throw new Error("지원하지 않는 기술 데이터 형식입니다.");
  }
  return catalog;
}

export function getPublicTechnologies(catalog) {
  return catalog.technologies.filter((item) => item.visibility === "public");
}

export function getTechnology(catalog, id) {
  return catalog.technologies.find((item) => item.id === id) ?? null;
}
```

- [ ] **Step 4: Implement the landing renderer**

Each public technology card must have `data-technology-id`, title, researcher, deposit number, and the exact detail link `./smk.html?tech={id}`. Catch loader errors and write the Korean error message into `#status-message` without injecting raw HTML.

- [ ] **Step 5: Run the landing verification**

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: PASS for one public card, zero private cards, correct detail link, zero console errors, and zero failed resources.

- [ ] **Step 6: Commit the landing page**

```powershell
git add -- KRIBB/js/catalog.js KRIBB/js/landing.js KRIBB/css/landing.css scripts/verify_kribb_smk.py
git commit -m "feat: render KRIBB technology landing page from JSON"
```

---

### Task 4: Fixed 01–08 SMK renderer and SVG charts

**Files:**
- Create: `KRIBB/js/charts.js`
- Create: `KRIBB/js/smk-renderer.js`
- Create: `KRIBB/css/screen.css`
- Modify: `KRIBB/smk.html`
- Modify: `tests/test_kribb_static.py`
- Modify: `scripts/verify_kribb_smk.py`

**Interfaces:**
- Produces: `renderChart(chart): SVGElement`
- Produces: `renderTechnology(technology, root): HTMLElement[]`
- Produces section IDs `section-01` through `section-08`
- Consumes: `getTechnology`, URL query `tech`, and the `Technology` data contract

- [ ] **Step 1: Add failing section and chart checks**

Add to the browser verification:

```python
page.goto(f"{base_url}/KRIBB/smk.html?tech=park-1020220067778", wait_until="networkidle")
section_ids = page.locator(".smk-section").evaluate_all("els => els.map(el => el.id)")
expected = [f"section-{index:02d}" for index in range(1, 9)]
if section_ids != expected:
    errors.append(f"detail: section order {section_ids}")
if page.locator(".evidence-chart svg").count() != 3:
    errors.append("detail: expected 3 SVG charts")
```

- [ ] **Step 2: Run verification and confirm failure**

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: FAIL because the detailed renderer and chart renderer do not exist.

- [ ] **Step 3: Implement accessible SVG bar charts**

`renderChart` must create an SVG with `role="img"`, `aria-labelledby`, title, axes, labels, values, unit, and source footer. Use a viewBox so the chart scales without raster blur. Apply a distinct hatch pattern or stroke in addition to color for comparison groups.

Core signature:

```javascript
export function renderChart(chart) {
  if (!Array.isArray(chart.labels) || chart.labels.length !== chart.values.length) {
    throw new Error(`${chart.id}: 차트 라벨과 값의 개수가 다릅니다.`);
  }
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 640 360");
  svg.setAttribute("role", "img");
  return svg;
}
```

- [ ] **Step 4: Implement the fixed section renderer**

Render the exact fixed headings and IDs:

```javascript
const SECTION_TITLES = [
  "균주 정보",
  "특허 정보",
  "실험 내용",
  "관련 데이터",
  "기술(균주) 적용제품",
  "기술 핵심요소",
  "기술활용 절차",
  "연구자 보유 균주 및 특허",
];
```

Use DOM APIs and `textContent`; do not concatenate untrusted JSON into `innerHTML`. Render fixed table headers exactly as specified in the design spec. Hide only empty classification cells; keep all 01–08 sections present.

- [ ] **Step 5: Add responsive screen styling**

- Desktop: content max width 1180px, charts 1–3 columns, products in a readable grid or table.
- Tablet: charts and products 2 columns when space permits.
- Mobile: charts, product cards, and process steps 1 column; no horizontal body overflow.
- Keep screen document continuous and free from A4 width or height constraints.

- [ ] **Step 6: Run static and browser verification**

Run: `python -m unittest tests.test_kribb_static -v`

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: eight ordered sections, three SVG charts for Park, zero console errors, zero failed resources, and no horizontal overflow at 1440×900, 1024×768, 768×1024, and 390×844.

- [ ] **Step 7: Commit the detailed renderer**

```powershell
git add -- KRIBB/smk.html KRIBB/js/charts.js KRIBB/js/smk-renderer.js KRIBB/css/screen.css tests/test_kribb_static.py scripts/verify_kribb_smk.py
git commit -m "feat: render fixed KRIBB SMK sections and SVG charts"
```

---

### Task 5: Scroll-linked responsive sidebar

**Files:**
- Create: `KRIBB/js/sidebar.js`
- Modify: `KRIBB/js/smk-renderer.js`
- Modify: `KRIBB/css/screen.css`
- Modify: `scripts/verify_kribb_smk.py`

**Interfaces:**
- Produces: `initSidebar({ sections, root }): { destroy(): void }`
- Consumes: `.smk-section`, `#screen-sidebar`, URL hashes `#section-01` through `#section-08`

- [ ] **Step 1: Add failing sidebar interaction checks**

```python
page.goto(f"{base_url}/KRIBB/smk.html?tech=park-1020220067778", wait_until="networkidle")
page.locator("#section-04").scroll_into_view_if_needed()
page.wait_for_timeout(250)
active = page.locator("#screen-sidebar [aria-current='location']").get_attribute("href")
if active != "#section-04":
    errors.append(f"sidebar: active link is {active}")
page.locator("#screen-sidebar").hover()
if page.locator("#screen-sidebar").get_attribute("data-expanded") != "true":
    errors.append("sidebar: hover did not expand")
```

- [ ] **Step 2: Run verification and confirm failure**

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: FAIL because sidebar behavior is not implemented.

- [ ] **Step 3: Implement IntersectionObserver-based active state**

Use one observer with a center-weighted root margin:

```javascript
const observer = new IntersectionObserver(onEntries, {
  root: null,
  rootMargin: "-25% 0px -55% 0px",
  threshold: [0, 0.25, 0.5, 0.75, 1],
});
```

When a section becomes active:

- Set exactly one link to `aria-current="location"`.
- Set the rail progress from 0% to 100% using section index.
- Replace the URL hash with `history.replaceState` without adding history entries.
- Update the mobile tab number.

- [ ] **Step 4: Implement desktop expansion and mobile drawer**

- Desktop default width: 76px.
- Desktop expanded width: 220px.
- Expand on hover, focus-within, or explicit toggle.
- Overlay the expanded menu without changing main content width.
- At widths below 820px, hide the rail and show an edge tab.
- Mobile drawer closes after link selection, Escape, or outside click.
- Use `aria-expanded`, `aria-controls`, focus return, and visible focus styles.

- [ ] **Step 5: Run browser verification**

Run: `python scripts/verify_kribb_smk.py --screen-only`

Expected: correct active section after scrolling, expanding desktop rail, working mobile drawer, correct hash, and zero console errors.

- [ ] **Step 6: Commit the sidebar**

```powershell
git add -- KRIBB/js/sidebar.js KRIBB/js/smk-renderer.js KRIBB/css/screen.css scripts/verify_kribb_smk.py
git commit -m "feat: add scroll-linked responsive SMK sidebar"
```

---

### Task 6: Section-atomic A4 portrait print layout

**Files:**
- Create: `KRIBB/js/print-layout.js`
- Create: `KRIBB/css/print.css`
- Create: `tests/test_kribb_print.py`
- Modify: `KRIBB/js/smk-renderer.js`
- Modify: `scripts/verify_kribb_smk.py`

**Interfaces:**
- Produces: `composePrintPages({ sourceRoot, printRoot }): PrintLayoutResult`
- Produces: `.print-page`, `.print-page__body`, `.print-page__watermark`, `data-section-id`
- Returns: `{ pageCount: number, placements: Array<{sectionId, pageIndex}> }`
- Consumes: fully rendered `.smk-section` elements

- [ ] **Step 1: Write failing PDF and placement tests**

`tests/test_kribb_print.py`:

```python
import json
import unittest
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "tmp" / "kribb-smk" / "qa"


class KribbPrintTests(unittest.TestCase):
    def test_park_pdf_is_a4_portrait_two_or_three_pages(self):
        pdf = QA / "park-1020220067778-print.pdf"
        reader = PdfReader(pdf)
        self.assertIn(len(reader.pages), (2, 3))
        for page in reader.pages:
            self.assertLess(float(page.mediabox.width), float(page.mediabox.height))

    def test_each_section_has_exactly_one_page_placement(self):
        placements = json.loads((QA / "park-1020220067778-placements.json").read_text(encoding="utf-8"))
        ids = [item["sectionId"] for item in placements]
        self.assertEqual(ids, [f"section-{index:02d}" for index in range(1, 9)])
        self.assertEqual(len(ids), len(set(ids)))
```

- [ ] **Step 2: Run print tests and verify failure**

Run: `python -m unittest tests.test_kribb_print -v`

Expected: FAIL because no PDF or placement ledger exists.

- [ ] **Step 3: Implement A4 print page containers**

`print.css` must include:

```css
@page { size: A4 portrait; margin: 0; }

@media print {
  .screen-only, #screen-sidebar { display: none !important; }
  .print-only { display: block !important; }
  .print-page {
    width: 210mm;
    height: 297mm;
    break-after: page;
    position: relative;
    overflow: hidden;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }
  .print-page:last-child { break-after: auto; }
  .print-section { break-inside: avoid; page-break-inside: avoid; }
}
```

- [ ] **Step 4: Implement section-atomic page composition**

Algorithm:

```javascript
export function composePrintPages({ sourceRoot, printRoot }) {
  printRoot.replaceChildren();
  const placements = [];
  let page = createPrintPage(0);
  printRoot.append(page.element);

  for (const section of sourceRoot.querySelectorAll(".smk-section")) {
    const clone = section.cloneNode(true);
    clone.classList.add("print-section");
    page.body.append(clone);

    if (page.body.scrollHeight > page.body.clientHeight + 1) {
      clone.remove();
      page = createPrintPage(page.index + 1);
      printRoot.append(page.element);
      page.body.append(clone);
    }

    if (page.body.scrollHeight > page.body.clientHeight + 1) {
      throw new Error(`${section.id} 섹션이 A4 한 페이지를 초과합니다.`);
    }
    placements.push({ sectionId: section.id, pageIndex: page.index });
  }
  return { pageCount: page.index + 1, placements };
}
```

Keep `#print-root` measurable on screen with a temporary `.is-measuring` class that positions it at `left: -100000px`, sets `visibility: hidden`, and applies the same 210mm page width and print typography without affecting document flow. Remove `.is-measuring` after composition. Run composition after fonts and images resolve using `await document.fonts.ready` and decoded images. Store the returned result as `window.__KRIBB_PRINT_LAYOUT__` and add an event handler to recompute on `beforeprint`.

- [ ] **Step 5: Add print headers, footers, and residual-space watermark**

- Page 1 header: official Korean/English signature.
- Page 2 onward: official color symbol.
- Footer: page number and technology ID.
- Watermark: SVG `<img>` positioned after content; keep it outside section boxes and below text stacking context.
- Do not rely on CSS `background-image` for required printed visuals.

- [ ] **Step 6: Extend browser QA to export PDF and placement ledger**

Use Playwright:

```python
page.emulate_media(media="print")
placements = page.evaluate("() => window.__KRIBB_PRINT_LAYOUT__.placements")
(QA_DIR / f"{tech_id}-placements.json").write_text(
    json.dumps(placements, ensure_ascii=False, indent=2), encoding="utf-8"
)
page.pdf(
    path=str(QA_DIR / f"{tech_id}-print.pdf"),
    format="A4",
    print_background=True,
    prefer_css_page_size=True,
    display_header_footer=False,
    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
)
```

- [ ] **Step 7: Run print verification**

Run: `python scripts/verify_kribb_smk.py`

Run: `python -m unittest tests.test_kribb_print -v`

Expected: Park PDF is A4 portrait with 2–3 pages; section IDs 01–08 each occur on exactly one page; no page overflow; no console errors.

- [ ] **Step 8: Commit the print system**

```powershell
git add -- KRIBB/js/print-layout.js KRIBB/css/print.css KRIBB/js/smk-renderer.js scripts/verify_kribb_smk.py tests/test_kribb_print.py
git commit -m "feat: compose section-atomic A4 SMK print pages"
```

---

### Task 7: Full source-backed content, error states, and final visual QA

**Files:**
- Modify: `KRIBB/data/technologies.json`
- Modify: `KRIBB/js/catalog.js`
- Modify: `KRIBB/js/smk-renderer.js`
- Modify: `KRIBB/css/common.css`
- Modify: `KRIBB/css/screen.css`
- Modify: `KRIBB/css/print.css`
- Modify: `scripts/verify_kribb_smk.py`
- Modify: `tests/test_kribb_data.py`
- Modify: `tests/test_kribb_static.py`
- Modify: `tests/test_kribb_print.py`

**Interfaces:**
- Consumes: all components from Tasks 1–6
- Produces: validated public Park example and private local P2025-033 example
- Produces: `tmp/kribb-smk/qa/` screenshots, PDFs, page PNGs, and QA summary

- [ ] **Step 1: Add failing error-state and source-integrity tests**

Test the following:

- Missing `tech` query displays a Korean selection message and a link to `index.html`.
- Unknown technology ID displays `기술을 찾을 수 없습니다`.
- Private technology displays only when `?tech=p2025-033&preview=1` is present.
- Public landing does not list private technology.
- Every chart has `sourceFigure` and `valueStatus`.
- Every source item records local source filename and page or figure locator.

- [ ] **Step 2: Complete Park and P2025-033 content from the source PDFs**

- Park: validate patent number, deposit number/date, strain aliases, experiment wording, chart values/status, applied products, four core elements, four utilization steps, and up to five related portfolio entries.
- P2025-033: validate deposit number/date, strain name, salt-stress experiments, chart candidates, agricultural products/services, four core elements, four utilization steps, and related portfolio entries available in the supplied material.
- Do not infer classification values; retain empty strings until provided.
- Do not publish the private technology in the landing list.

- [ ] **Step 3: Implement all user-facing error states**

Use a shared status renderer that accepts a safe text message and optional local link. Do not expose stack traces or local filesystem paths in the page.

- [ ] **Step 4: Run the complete automated suite**

Run: `python -m unittest tests.test_kribb_data tests.test_kribb_static tests.test_kribb_print -v`

Run: `python scripts/verify_kribb_smk.py`

Expected: all tests PASS; zero console errors; zero failed resources; no horizontal overflow; valid 2–3-page PDFs for both local examples.

- [ ] **Step 5: Render and inspect every final PDF page**

Render PDFs with Poppler:

```powershell
& 'C:\Users\JEON\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe' -png -r 180 'tmp\kribb-smk\qa\park-1020220067778-print.pdf' 'tmp\kribb-smk\qa\park-page'
& 'C:\Users\JEON\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe' -png -r 180 'tmp\kribb-smk\qa\p2025-033-print.pdf' 'tmp\kribb-smk\qa\p2025-page'
```

Inspect every PNG individually for:

- section title and body on the same page;
- no section split across pages;
- no clipped table rows, chart labels, or process steps;
- correct first-page signature and later-page symbol;
- watermark only in unused space;
- readable light-blue and deep-blue contrast;
- no unintended blank final page.

- [ ] **Step 6: Inspect desktop and mobile screen captures**

Inspect screenshots at 1440×900, 1024×768, 768×1024, and 390×844. Verify rail expansion, active section, mobile drawer, charts, tables, and no body overflow.

- [ ] **Step 7: Run final regression checks after visual fixes**

Run: `python -m unittest tests.test_kribb_data tests.test_kribb_static tests.test_kribb_print -v`

Run: `python scripts/verify_kribb_smk.py`

Expected: all tests PASS after the final visual polish, with regenerated screenshots and PDFs.

- [ ] **Step 8: Commit the completed template**

```powershell
git add -- KRIBB scripts/verify_kribb_smk.py tests/test_kribb_data.py tests/test_kribb_static.py tests/test_kribb_print.py
git commit -m "feat: complete reusable KRIBB strain SMK template"
```

---

## Plan Self-Review

- Spec coverage: landing, shared JSON, fixed sections, charts, responsive sidebar, branding, private data handling, A4 print composition, and visual QA are each assigned to a task.
- Placeholder scan: no deferred implementation items remain.
- Interface consistency: `Technology.id`, `visibility`, section IDs, chart fields, and print placement fields use the same names across tasks.
- Scope: GitHub push and Pages deployment are excluded until the user explicitly requests publication.
