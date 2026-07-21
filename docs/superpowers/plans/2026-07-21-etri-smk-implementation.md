# ETRI SMK Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ETRI 기술자료 4건을 근거로 A4 가로 한 페이지 인쇄가 가능한 기술별 SMK HTML 4개와 통합 목록을 제작한다.

**Architecture:** 원본 PPTX/PDF는 읽기 전용으로 유지한다. 추출 스크립트가 원문 텍스트와 후보 이미지를 작업 폴더에 생성하고, 각 SMK HTML은 공통 CSS를 사용해 A4 가로 규격을 공유한다. 별도 검증 스크립트가 HTML 구조, 링크, 인쇄 CSS, PDF 페이지 크기와 페이지 수를 자동 검사한다.

**Tech Stack:** HTML5, CSS3 print media, Python 3, PowerPoint COM, pypdf/pdfplumber, Poppler, Playwright Chromium

## Global Constraints

- 기준 캔버스는 A4 가로 `297mm × 210mm`다.
- CSS `@page`는 `size: A4 landscape; margin: 0;`을 사용한다.
- 문서 내부 상하좌우 안전여백은 `8mm`로 통일한다.
- 기술별 SMK는 인쇄 시 정확히 한 페이지만 생성한다.
- 원본 자료의 기술 범위와 표현을 우선한다.
- 근거가 없는 시장규모, 성능 우위, 사업화 단계는 추가하지 않는다.
- 기존 `catholic/레퍼런스-smk.html`의 색상, 제목 위계, 정보 블록 구조를 재사용한다.
- 원본 PPTX와 PDF는 수정하지 않는다.

---

### Task 1: 원본 자료 추출 및 근거 정리

**Files:**
- Create: `scripts/extract_etri_smk_sources.py`
- Create: `tmp/etri-smk/source-notes/tech-01.txt`
- Create: `tmp/etri-smk/source-notes/tech-02.txt`
- Create: `tmp/etri-smk/source-notes/tech-03.txt`
- Create: `tmp/etri-smk/source-notes/tech-04.txt`
- Create: `tmp/etri-smk/rendered/tech-01/`
- Create: `tmp/etri-smk/rendered/tech-02/`
- Create: `tmp/etri-smk/rendered/tech-03/`
- Create: `tmp/etri-smk/rendered/tech-04/`

**Interfaces:**
- Consumes: 다운로드 폴더의 PPTX 3개와 PDF 1개
- Produces: UTF-8 원문 노트와 기술별 전체 페이지 PNG

- [ ] **Step 1: 원본 파일 존재 여부 검사 작성**

  - `SOURCE_MAP`에 원본 파일명, 결과 기술번호, 렌더 폴더명을 고정한다.
  - 누락 파일이 있으면 경로를 포함한 `FileNotFoundError`를 발생시킨다.

- [ ] **Step 2: PPTX·PDF 추출 구현**

  - PPTX는 `python-pptx`로 슬라이드 순서와 텍스트를 추출한다.
  - PowerPoint COM `Slides.Export(..., "PNG", 1920, 1080)`로 전체 슬라이드를 렌더링한다.
  - PDF는 `pypdf`로 텍스트를 추출하고 `pdftoppm -png -r 150`으로 전체 페이지를 렌더링한다.
  - 각 노트에 원본 파일명, 기술번호, 페이지별 텍스트를 기록한다.

- [ ] **Step 3: 추출 실행 및 결과 검사**

  Run: `python scripts/extract_etri_smk_sources.py`

  Expected: 기술별 노트 4개 생성, 모든 원본 페이지가 PNG로 생성, 오류 0건

- [ ] **Step 4: 기술별 근거 요약 작성**

  - 각 원본의 기술명, 기술 개요, 기존 방식의 한계, 핵심 구성, 차별성, 적용 분야, 도입 효과를 원문 기준으로 정리한다.
  - 대표 도면은 글자 식별성과 기술 설명 적합성을 기준으로 기술별 1~2개 선정한다.
  - 원문에서 확인되지 않은 수치와 TRL은 제외한다.

- [ ] **Step 5: 작업 단위 커밋**

  Run: `git add scripts/extract_etri_smk_sources.py && git commit -m "build: extract ETRI SMK source evidence"`

  Expected: 추출 스크립트만 커밋되고 `tmp/etri-smk` 산출물은 커밋하지 않음

---

### Task 2: A4 공통 인쇄 스타일과 검증 테스트

**Files:**
- Create: `ETRI/assets/smk-print.css`
- Create: `scripts/verify_etri_smk.py`
- Create: `tests/test_etri_smk.py`

**Interfaces:**
- Consumes: `ETRI/tech-01.html`부터 `ETRI/tech-04.html`까지의 `.smk-sheet` 구조
- Produces: 공통 A4 인쇄 스타일과 자동 검증 명령

- [ ] **Step 1: 실패하는 인쇄 규격 테스트 작성**

  - 기술 HTML 4개 존재 여부를 검사한다.
  - 공통 CSS에 `@page`, `size: A4 landscape`, `297mm`, `210mm`, `8mm`, `print-color-adjust: exact`가 있는지 검사한다.
  - 각 HTML에 `.smk-sheet`가 정확히 1개 있는지 검사한다.
  - 각 HTML의 로컬 이미지 경로가 실제 파일을 가리키는지 검사한다.

- [ ] **Step 2: 테스트 실패 확인**

  Run: `python -m unittest tests.test_etri_smk -v`

  Expected: `ETRI/assets/smk-print.css` 또는 `ETRI/tech-01.html` 누락으로 FAIL

- [ ] **Step 3: 공통 CSS 구현**

  - `.smk-sheet`를 `width:297mm; height:210mm; padding:8mm; overflow:hidden;`으로 고정한다.
  - `@media print`에서 화면 축소 변환, 그림자, 외부 배경을 제거한다.
  - `break-after: avoid-page`, `break-inside: avoid`, `page-break-after: avoid`를 적용한다.
  - 화면에서는 `transform: scale(var(--sheet-scale))`로 전체 종이를 중앙 표시한다.

- [ ] **Step 4: 정적 검증기 구현**

  Run: `python scripts/verify_etri_smk.py --static-only`

  Expected: HTML이 아직 없으므로 누락 파일을 명시하고 비정상 종료

- [ ] **Step 5: 작업 단위 커밋**

  Run: `git add ETRI/assets/smk-print.css scripts/verify_etri_smk.py tests/test_etri_smk.py && git commit -m "test: define A4 SMK print contract"`

  Expected: 공통 인쇄 규격과 검증 코드가 커밋됨

---

### Task 3: 기술별 SMK HTML 4종 제작

**Files:**
- Create: `ETRI/tech-01.html`
- Create: `ETRI/tech-02.html`
- Create: `ETRI/tech-03.html`
- Create: `ETRI/tech-04.html`
- Create: `ETRI/assets/tech-01/`
- Create: `ETRI/assets/tech-02/`
- Create: `ETRI/assets/tech-03/`
- Create: `ETRI/assets/tech-04/`

**Interfaces:**
- Consumes: Task 1의 원문 노트·대표 도면, Task 2의 `smk-print.css`
- Produces: 독립 열람과 A4 단면 인쇄가 가능한 기술별 SMK 4개

- [ ] **Step 1: 템플릿 구조 이식**

  - `catholic/레퍼런스-smk.html`의 색상 변수, 제목 위계, 섹션 구성을 유지한다.
  - 최상위 문서 요소는 `<article class="smk-sheet">` 하나만 사용한다.
  - 공통 CSS는 `<link rel="stylesheet" href="assets/smk-print.css">`로 연결한다.

- [ ] **Step 2: 기술별 문안 입력**

  - 기술명과 한 줄 핵심 가치를 상단에 배치한다.
  - 본문은 기술 개요, 기존 방식의 한계, 핵심 구성, 차별성, 적용 분야, 도입 효과 순으로 구성한다.
  - 각 bullet은 하나의 주장만 담고, 원문의 기술적 한계를 벗어나지 않는다.

- [ ] **Step 3: 대표 도면 배치**

  - 선정한 원본 페이지 PNG를 기술별 assets 폴더에 복사한다.
  - 필요한 경우 의미를 보존하는 범위에서 자른 PNG를 추가한다.
  - `<figure>`와 `<figcaption>`에 원본 자료 페이지를 표기한다.

- [ ] **Step 4: 출처와 기술 링크 입력**

  - 하단에 ETRI 기술번호와 제공된 기술이전 상세 링크를 입력한다.
  - 출처는 원본 PPTX 또는 PDF 파일명과 슬라이드·페이지 번호를 함께 표기한다.

- [ ] **Step 5: 정적 테스트 통과 확인**

  Run: `python -m unittest tests.test_etri_smk -v`

  Expected: 모든 정적 구조·링크·인쇄 규격 테스트 PASS

- [ ] **Step 6: 작업 단위 커밋**

  Run: `git add ETRI/tech-0*.html ETRI/assets && git commit -m "feat: add four printable ETRI SMKs"`

  Expected: 기술별 HTML과 사용 이미지가 커밋됨

---

### Task 4: 통합 목록 갱신

**Files:**
- Modify: `ETRI/index.html`
- Test: `tests/test_etri_smk.py`

**Interfaces:**
- Consumes: 기술별 HTML의 기술명, 기술번호, 분야, 파일명
- Produces: 4개 기술로 연결되는 통합 목록

- [ ] **Step 1: 실패하는 목록 테스트 추가**

  - `총 4건` 표시를 검사한다.
  - `tech-01.html`부터 `tech-04.html`까지 각 링크가 정확히 한 번 존재하는지 검사한다.
  - 빈 상태 문구 `등록된 SMK가 없습니다.`가 제거됐는지 검사한다.

- [ ] **Step 2: 실패 확인**

  Run: `python -m unittest tests.test_etri_smk -v`

  Expected: 현재 `총 0건`과 빈 상태 행 때문에 FAIL

- [ ] **Step 3: 목록 4건 입력**

  - 기술명, 분야, ETRI 기술번호, `SMK 보기` 링크를 표에 입력한다.
  - 기존 반응형 표 구조와 시각 스타일을 유지한다.

- [ ] **Step 4: 테스트 통과 확인**

  Run: `python -m unittest tests.test_etri_smk -v`

  Expected: 전체 PASS

- [ ] **Step 5: 작업 단위 커밋**

  Run: `git add ETRI/index.html tests/test_etri_smk.py && git commit -m "feat: list ETRI SMK pages"`

  Expected: 통합 목록과 목록 검증이 커밋됨

---

### Task 5: 브라우저 렌더링 및 A4 한 페이지 인쇄 QA

**Files:**
- Create: `tmp/etri-smk/qa/tech-01-screen.png`
- Create: `tmp/etri-smk/qa/tech-02-screen.png`
- Create: `tmp/etri-smk/qa/tech-03-screen.png`
- Create: `tmp/etri-smk/qa/tech-04-screen.png`
- Create: `tmp/etri-smk/qa/tech-01-print.pdf`
- Create: `tmp/etri-smk/qa/tech-02-print.pdf`
- Create: `tmp/etri-smk/qa/tech-03-print.pdf`
- Create: `tmp/etri-smk/qa/tech-04-print.pdf`

**Interfaces:**
- Consumes: 완성된 기술별 HTML 4개
- Produces: 화면 캡처, 인쇄 PDF, 자동 QA 결과

- [ ] **Step 1: Chromium 화면 렌더링**

  - Playwright로 각 `file:///.../ETRI/tech-0N.html`을 연다.
  - 화면 크기 `1440×1024`에서 전체 A4 종이 화면 캡처를 저장한다.
  - 콘솔 오류와 로드 실패 리소스가 0건인지 기록한다.

- [ ] **Step 2: A4 가로 PDF 출력**

  - `page.pdf(format="A4", landscape=True, print_background=True, margin={top:"0", right:"0", bottom:"0", left:"0"})`를 사용한다.
  - 브라우저 머리글·바닥글은 비활성화한다.

- [ ] **Step 3: PDF 규격 자동 검사**

  Run: `python scripts/verify_etri_smk.py`

  Expected: 4개 PDF 모두 1페이지, 가로 A4 `841.89×595.28pt` 허용오차 ±1pt, 오류 0건

- [ ] **Step 4: 전체 크기 시각 검사**

  - 4개 화면 캡처와 PDF 렌더 PNG를 각각 원본 크기로 확인한다.
  - 잘림, 겹침, 과도한 줄바꿈, 흐린 도면, 불균등 여백을 수정한다.
  - 수정 후 Step 1부터 Step 3까지 다시 실행한다.

- [ ] **Step 5: 최종 검증 커밋**

  Run: `git add ETRI scripts/verify_etri_smk.py tests/test_etri_smk.py && git commit -m "fix: complete ETRI SMK print QA"`

  Expected: 필요한 최종 수정만 커밋되고 `tmp/etri-smk/qa`는 커밋하지 않음

---

### Task 6: 최종 인수검사

**Files:**
- Verify: `ETRI/index.html`
- Verify: `ETRI/tech-01.html`
- Verify: `ETRI/tech-02.html`
- Verify: `ETRI/tech-03.html`
- Verify: `ETRI/tech-04.html`

**Interfaces:**
- Consumes: 모든 완성 산출물과 QA 결과
- Produces: 사용자 전달 가능한 최종 상태

- [ ] **Step 1: 전체 자동 검사 실행**

  Run: `python -m unittest tests.test_etri_smk -v`

  Expected: 전체 PASS

- [ ] **Step 2: 최종 인쇄 검사 실행**

  Run: `python scripts/verify_etri_smk.py`

  Expected: `4 HTML / 4 PDF / 4 single-page A4 landscape / 0 errors`

- [ ] **Step 3: 작업트리 범위 확인**

  Run: `git status --short`

  Expected: 사용자 기존 미추적 파일은 보존되고, 본 작업의 필수 파일은 모두 커밋 상태

