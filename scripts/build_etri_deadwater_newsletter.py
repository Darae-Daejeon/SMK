import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ETRI" / "deadwater-newsletter" / "reference" / "deadwater.html"
OUTPUT = ROOT / "ETRI" / "deadwater-newsletter" / "index.html"


PROJECTS = """      <section class="projects" aria-label="ETRI IP거래 보유기술">
        <ul class="project-list">
          <li class="reveal">
            <a class="project-link" href="https://darae-daejeon.github.io/SMK/ETRI/tech-01.html" target="_blank" rel="noopener" data-image="assets/smk-01.png">
              <span class="project-name">미래 건강 예측을 위한 의료지능 딥러닝 엔진 기술</span>
              <span class="project-meta"><span>의료 인공지능</span><span>10-2018-0147862</span></span>
              <span class="project-mobile-media"><img src="assets/smk-01.png" alt="미래 건강 예측 의료지능 딥러닝 엔진 기술 SMK"></span>
            </a>
          </li>
          <li class="reveal">
            <a class="project-link" href="https://darae-daejeon.github.io/SMK/ETRI/tech-02.html" target="_blank" rel="noopener" data-image="assets/smk-02.png">
              <span class="project-name">미래 건강상태 및 예후 예측을 위한 헬스케어 인공지능 기술</span>
              <span class="project-meta"><span>확률 기반 예후 예측</span><span>10-2021-0179326</span></span>
              <span class="project-mobile-media"><img src="assets/smk-02.png" alt="미래 건강상태 및 예후 예측 헬스케어 인공지능 기술 SMK"></span>
            </a>
          </li>
          <li class="reveal">
            <a class="project-link" href="https://darae-daejeon.github.io/SMK/ETRI/tech-03.html" target="_blank" rel="noopener" data-image="assets/smk-03.png">
              <span class="project-name">개인 맞춤형 건강 관리 프로그램을 계획하는 인공지능 헬스케어 기술</span>
              <span class="project-meta"><span>맞춤형 치료계획</span><span>10-2022-0189362</span></span>
              <span class="project-mobile-media"><img src="assets/smk-03.png" alt="개인 맞춤형 건강관리 인공지능 헬스케어 기술 SMK"></span>
            </a>
          </li>
          <li class="reveal">
            <a class="project-link" href="https://darae-daejeon.github.io/SMK/ETRI/tech-04.html" target="_blank" rel="noopener" data-image="assets/smk-04.png">
              <span class="project-name">미래 건강 상태의 맞춤형 예측 및 최적 관리를 위한 인공지능 기술</span>
              <span class="project-meta"><span>예측·최적관리</span><span>10-2024-0172319</span></span>
              <span class="project-mobile-media"><img src="assets/smk-04.png" alt="미래 건강 맞춤형 예측 및 최적관리 인공지능 기술 SMK"></span>
            </a>
          </li>
        </ul>

        <aside class="project-preview" aria-hidden="true">
          <img src="assets/smk-01.png" alt="">
          <span class="preview-caption">SMK 자세히 보기</span>
        </aside>
      </section>
"""


OVERRIDES = """
    /* ETRI content adaptation: the original Deadwater layout remains authoritative. */
    .studio-header img {
      width: 88px;
      height: auto;
      object-fit: contain;
    }
    .etri-hero-title {
      right: var(--gutter);
      bottom: clamp(42px, 5vw, 82px);
      width: calc(100% - (var(--gutter) * 2));
      margin: 0;
      color: var(--ink);
      font-family: "Noto Serif KR", "HCR Batang", "Batang", "BatangChe", serif;
      font-size: clamp(24px, 5.45vw, 106px);
      font-weight: 800;
      line-height: .88;
      letter-spacing: -.082em;
      white-space: nowrap;
      transform: scaleX(1.045);
      transform-origin: left bottom;
    }
    .project-list { width: 100%; }
    .project-link {
      min-height: 126px;
      grid-template-columns: minmax(0, 1fr) 310px;
      gap: clamp(22px, 2.6vw, 48px);
    }
    .project-name {
      max-width: none;
      font-family: "Inter Local", "Noto Sans KR", Arial, sans-serif;
      font-size: clamp(22px, 2vw, 38px);
      font-weight: 650;
      line-height: 1.03;
      letter-spacing: -.07em;
      white-space: nowrap;
      word-break: keep-all;
    }
    .project-meta {
      grid-template-columns: minmax(130px, 1fr) minmax(148px, auto);
      font-family: "Inter Local", "Noto Sans KR", Arial, sans-serif;
      font-size: 13px;
    }
    .project-meta > span:last-child {
      text-align: right;
    }
    .project-preview {
      z-index: 10;
      width: min(60vw, 920px);
      margin-top: -560px;
      background: #fff;
      isolation: isolate;
      box-shadow: 0 18px 65px rgba(0, 0, 0, .28);
    }
    .project-preview img { background: #fff; }
    @media (max-width: 820px) {
      .studio-header img { width: 76px; height: auto; }
      .etri-hero-title {
        right: 18px;
        width: calc(100% - 36px);
        font-size: clamp(19px, 5.45vw, 45px);
        letter-spacing: -.09em;
        transform: scaleX(1.02);
      }
      .project-link { min-height: auto; grid-template-columns: 1fr; gap: 18px; }
      .project-name {
        font-size: clamp(15px, 3.95vw, 28px);
        letter-spacing: -.075em;
      }
      .project-meta { grid-template-columns: 1fr auto; }
    }
"""


def replace_once(text: str, pattern: str, replacement: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"Expected one match for: {pattern[:80]}")
    return updated


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8").lstrip("\ufeff")
    html = html.replace('<html lang="fr">', '<html lang="ko">', 1)
    html = replace_once(html, r'<meta name="description"[^>]+>', '<meta name="description" content="한국전자통신연구원 의료·헬스케어 인공지능 IP거래 기술목록">')
    html = replace_once(html, r'<title>.*?</title>', '<title>ETRI IP거래 기술목록</title>')
    html = replace_once(
        html,
        r'<header class="studio-header".*?</header>',
        '''<header class="studio-header" aria-label="ETRI IP거래 기술목록">
      <img src="assets/etri-logo.png" alt="ETRI 한국전자통신연구원">
      <p>ETRI IP거래<br>기술목록</p>
    </header>''',
        re.S,
    )
    html = replace_once(html, r'\s*<div class="showreel".*?</div>', '', re.S)
    html = replace_once(
        html,
        r'<p class="hero-wordmark"[^>]*>.*?</p>',
        '<h1 class="hero-wordmark etri-hero-title" id="hero-title">한국전자통신연구원 IP거래 기술 목록</h1>',
        re.S,
    )
    html = replace_once(
        html,
        r'\n\s*<div class="hero-copy">.*?</div>',
        '',
        re.S,
    )
    projects_start = html.index('      <section class="projects"')
    expertise_start = html.index('      <section class="section" id="expertise"', projects_start)
    html = html[:projects_start] + PROJECTS + html[expertise_start:]

    expertise_start = html.index('      <section class="section" id="expertise"')
    main_end = html.index('    </main>', expertise_start)
    html = html[:expertise_start] + '    </main>' + html[main_end + len('    </main>'):]

    html = html.replace('      const showreel = document.querySelector(\'.showreel\');\n', '', 1)
    html = html.replace('      const mediaButton = document.querySelector(\'.media-pill\');\n', '', 1)
    html = replace_once(html, r'\s*mediaButton\.addEventListener\(\'click\', \(\) => \{.*?\n      \}\);', '', re.S)
    html = html.replace('<div class="custom-cursor" aria-hidden="true">Lecture</div>', '<div class="custom-cursor" aria-hidden="true">SMK 보기</div>', 1)
    html = html.replace('  </style>', OVERRIDES + '  </style>', 1)

    OUTPUT.write_text(html, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
