from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "ETRI" / "newsletter"
ASSET_DIR = OUTPUT_DIR / "assets"
PUBLIC_BASE = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/"

TECHNOLOGIES = [
    {
        "number": "01",
        "title": "미래 건강 예측을 위한 의료지능 딥러닝 엔진 기술",
        "value": "의료 데이터를 분석해 개인의 미래 건강 위험을 예측",
        "field": "의료 데이터 분석 · 미래 건강 예측",
        "source": ROOT / "ETRI" / "assets" / "tech-01" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-01.html",
        "accent": "#00A6A6",
        "tint": "#DDF7F5",
    },
    {
        "number": "02",
        "title": "미래 건강상태 및 예후 예측을 위한 헬스케어 인공지능 기술",
        "value": "불확실성을 반영해 건강상태와 예후를 확률로 예측",
        "field": "확률 기반 예후 예측 · 의사결정 지원",
        "source": ROOT / "ETRI" / "assets" / "tech-02" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-02.html",
        "accent": "#2474C6",
        "tint": "#E3EFFB",
    },
    {
        "number": "03",
        "title": "개인 맞춤형 건강 관리 프로그램을 계획하는 인공지능 헬스케어 기술",
        "value": "개인의 상태와 목표에 맞춘 건강 관리 계획을 자동 수립",
        "field": "맞춤형 건강 관리 · 치료계획 최적화",
        "source": ROOT / "ETRI" / "assets" / "tech-03" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-03.html",
        "accent": "#6658C8",
        "tint": "#ECE9FC",
    },
    {
        "number": "04",
        "title": "미래 건강 상태의 맞춤형 예측 및 최적 관리를 위한 인공지능 기술",
        "value": "개인별 미래 건강상태를 예측하고 관리 전략을 최적화",
        "field": "맞춤형 예측 · 건강 관리 최적화",
        "source": ROOT / "ETRI" / "assets" / "tech-04" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-04.html",
        "accent": "#D46A42",
        "tint": "#FCEAE3",
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
    raise FileNotFoundError("Malgun Gothic or Arial font was not found")


def cover(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as image:
        converted = image.convert("RGB")
        scale = max(size[0] / converted.width, size[1] / converted.height)
        resized = converted.resize(
            (round(converted.width * scale), round(converted.height * scale)),
            Image.Resampling.LANCZOS,
        )
        left = (resized.width - size[0]) // 2
        top = (resized.height - size[1]) // 2
        return resized.crop((left, top, left + size[0], top + size[1]))


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    width: int,
) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def build_header() -> Path:
    canvas = Image.new("RGB", (600, 250), "#102A43")
    draw = ImageDraw.Draw(canvas)

    for x, y, radius, color in [
        (510, 30, 115, "#173D5C"),
        (565, 165, 90, "#0D666B"),
        (430, 220, 65, "#184E63"),
    ]:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    nodes = [(410, 55), (486, 92), (548, 60), (445, 150), (530, 188), (385, 205)]
    for index, start in enumerate(nodes):
        for end in nodes[index + 1 :]:
            if abs(start[0] - end[0]) + abs(start[1] - end[1]) < 150:
                draw.line((*start, *end), fill="#4EA8A8", width=2)
    for x, y in nodes:
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="#8EE3DC")
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill="white")

    draw.rounded_rectangle((32, 28, 176, 62), radius=17, fill="#00A6A6")
    draw.text((47, 36), "ETRI TECHNOLOGY", font=load_font(14, True), fill="white")
    draw.text((32, 85), "의료·헬스케어 AI", font=load_font(35, True), fill="white")
    draw.text((32, 135), "기업의 다음 서비스를 위한 기술 4선", font=load_font(22, True), fill="#8EE3DC")
    draw.text((32, 190), "예측  ·  예후  ·  맞춤형 계획  ·  최적 관리", font=load_font(15), fill="#D8E7F2")
    draw.text((514, 214), "ETRI", font=load_font(18, True), fill="white")

    path = ASSET_DIR / "newsletter-header.png"
    canvas.save(path, optimize=True)
    return path


def build_card(technology: dict[str, str | Path]) -> Path:
    canvas = Image.new("RGB", (600, 300), "#FFFFFF")
    draw = ImageDraw.Draw(canvas)
    accent = str(technology["accent"])
    tint = str(technology["tint"])

    visual = cover(Path(technology["source"]), (246, 300))
    visual = ImageEnhance.Contrast(visual).enhance(0.88)
    visual = ImageEnhance.Color(visual).enhance(0.72)
    canvas.paste(visual, (354, 0))
    overlay = Image.new("RGBA", (246, 300), (16, 42, 67, 28))
    canvas.paste(overlay, (354, 0), overlay)

    draw.rectangle((0, 0, 354, 300), fill="#FFFFFF")
    draw.rectangle((0, 0, 10, 300), fill=accent)
    draw.polygon([(314, 0), (354, 0), (354, 300), (334, 300)], fill=tint)
    draw.rounded_rectangle((30, 23, 91, 55), radius=16, fill=accent)
    draw.text((49, 30), str(technology["number"]), font=load_font(14, True), fill="white")

    title_font = load_font(21, True)
    title_lines = wrap_text(draw, str(technology["title"]), title_font, 274)
    y = 71
    for line in title_lines[:3]:
        draw.text((30, y), line, font=title_font, fill="#102A43")
        y += 32

    value_font = load_font(13)
    value_lines = wrap_text(draw, str(technology["value"]), value_font, 284)
    y = 177
    for line in value_lines[:2]:
        draw.text((30, y), line, font=value_font, fill="#40566B")
        y += 23

    draw.rounded_rectangle((30, 222, 295, 246), radius=12, fill=tint)
    draw.text((42, 226), str(technology["field"]), font=load_font(12, True), fill=accent)
    draw.rounded_rectangle((30, 258, 170, 288), radius=15, fill="#102A43")
    draw.text((49, 264), "SMK 자세히 보기  →", font=load_font(12, True), fill="white")

    path = ASSET_DIR / f"tech-{technology['number']}-card.png"
    canvas.save(path, optimize=True)
    return path


def build_assets() -> list[Path]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for technology in TECHNOLOGIES:
        source = Path(technology["source"])
        if not source.exists():
            raise FileNotFoundError(source)
    return [build_header(), *(build_card(technology) for technology in TECHNOLOGIES)]


def image_tag(filename: str, width: int, height: int, alt: str) -> str:
    src = f"{PUBLIC_BASE}assets/{filename}"
    return (
        f'<img src="{src}" width="{width}" height="{height}" alt="{alt}" '
        f'style="display:block; width:{width}px; max-width:100%; height:auto; margin:0; padding:0; border:0; outline:none; text-decoration:none;">'
    )


def build_html() -> Path:
    card_rows = []
    for technology in TECHNOLOGIES:
        card = image_tag(
            f"tech-{technology['number']}-card.png",
            600,
            300,
            f"{technology['title']} — SMK 자세히 보기",
        )
        card_rows.append(
            f'''              <tr>
                <td style="padding:0 0 14px 0;">
                  <a href="{technology['url']}" target="_blank" rel="noopener noreferrer" style="display:block; color:#102a43; text-decoration:none;">{card}</a>
                </td>
              </tr>'''
        )

    header = image_tag(
        "newsletter-header.png",
        600,
        250,
        "ETRI 의료·헬스케어 AI 기술이전 안내",
    )
    html = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ETRI 의료·헬스케어 AI 기술이전 안내</title>
  </head>
  <body style="margin:0; padding:0; background:#eef2f6;">
    <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:transparent;">미래 건강 예측부터 개인 맞춤형 관리까지, ETRI 의료 AI 기술 4종을 확인하세요.</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; margin:0; padding:0; border-collapse:collapse; background:#eef2f6;">
      <tr>
        <td align="center" style="padding:24px 0;">
          <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:600px; max-width:100%; margin:0; border-collapse:collapse; background:#ffffff;">
            <tr><td style="padding:0;">{header}</td></tr>
            <tr>
              <td style="padding:27px 32px 9px 32px; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#102a43;">
                <div style="font-size:20px; line-height:1.5; font-weight:700;">의료 AI 기술을 찾고 계신가요?</div>
                <div style="padding-top:10px; color:#506578; font-size:14px; line-height:1.75;">기업의 디지털 헬스케어 서비스 개발과 고도화에 활용 가능한 ETRI 기술 4종을 소개합니다. 관심 기술의 카드를 눌러 상세 SMK를 확인하세요.</div>
              </td>
            </tr>
            <tr>
              <td style="padding:20px 0 10px 0;">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:600px; max-width:100%; border-collapse:collapse;">
{chr(10).join(card_rows)}
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:30px 32px 32px 32px; background:#102a43; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#ffffff;">
                <div style="font-size:19px; line-height:1.5; font-weight:700;">기술이전·사업화 상담</div>
                <div style="padding-top:8px; color:#d8e7f2; font-size:13px; line-height:1.7;">보유 역량과 사업 방향을 바탕으로 적합한 기술 검토를 지원합니다.</div>
                <div style="padding-top:17px; font-size:15px; line-height:1.8;">
                  <a href="mailto:yhj@daraebiz.com" style="color:#8ee3dc; text-decoration:none; font-weight:700;">yhj@daraebiz.com</a>
                  <span style="color:#6e8da6;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                  <a href="tel:042-716-7084" style="color:#8ee3dc; text-decoration:none; font-weight:700;">042-716-7084</a>
                </div>
                <div style="padding-top:18px; color:#8aa2b5; font-size:11px; line-height:1.6;">다래전략사업화센터 대전지사 · ETRI 기술사업화 협력 안내</div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
'''
    output = OUTPUT_DIR / "etri-medical-ai-newsletter.html"
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    assets = build_assets()
    html_path = build_html()
    print(f"generated {len(assets)} images and {html_path}")
