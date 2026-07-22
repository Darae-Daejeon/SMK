from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "ETRI" / "newsletter"
ASSET_DIR = OUTPUT_DIR / "assets"
SOURCE_DIR = OUTPUT_DIR / "source-assets"
PUBLIC_BASE = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/"

WIDTH = 1200
HEIGHT = 2860
HERO_HEIGHT = 1000
TECH_HEIGHT = 360
CONTACT_MAIN_HEIGHT = 260
CONTACT_PHONE_HEIGHT = 160

TECHNOLOGIES = [
    {
        "number": "01",
        "label": "MEDICAL INTELLIGENCE",
        "title": "미래 건강 예측을 위한 의료지능 딥러닝 엔진 기술",
        "description": "의료 데이터를 분석해 개인의 미래 건강 위험을 예측하는 딥러닝 엔진",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-01.html",
    },
    {
        "number": "02",
        "label": "PROGNOSIS PREDICTION",
        "title": "미래 건강상태 및 예후 예측을 위한 헬스케어 인공지능 기술",
        "description": "불확실성을 반영해 미래 건강 상태와 예후를 확률 기반으로 예측",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-02.html",
    },
    {
        "number": "03",
        "label": "PERSONALIZED HEALTHCARE",
        "title": "개인 맞춤형 건강 관리 프로그램을 계획하는 인공지능 헬스케어 기술",
        "description": "개인의 상태와 목표에 맞춘 건강 관리 프로그램을 자동 계획",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-03.html",
    },
    {
        "number": "04",
        "label": "OPTIMAL HEALTH MANAGEMENT",
        "title": "미래 건강 상태의 맞춤형 예측 및 최적 관리를 위한 인공지능 기술",
        "description": "개인별 미래 건강 상태를 예측하고 최적의 관리 전략을 제안",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-04.html",
    },
]


def korean_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/Hancom Gothic Bold.ttf" if bold else "C:/Windows/Fonts/Hancom Gothic Regular.ttf"),
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    raise FileNotFoundError("Korean font not found")


def english_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf")
    return ImageFont.truetype(str(path), size)


def cover(source: Path, size: tuple[int, int], focus_x: float = 0.5) -> Image.Image:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = round((image.width - size[0]) * focus_x)
    top = (image.height - size[1]) // 2
    return image.crop((left, top, left + size[0], top + size[1]))


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def gradient_background() -> Image.Image:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#061A2B")
    draw = ImageDraw.Draw(canvas)
    top = (4, 26, 44)
    bottom = (7, 57, 70)
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        color = tuple(round(top[index] * (1 - ratio) + bottom[index] * ratio) for index in range(3))
        draw.line((0, y, WIDTH, y), fill=color)
    for x in range(0, WIDTH, 12):
        draw.line((x, 0, x, HEIGHT), fill=(14, 74, 87), width=1)
    draw.ellipse((-320, 180, 1240, 2920), fill=(8, 55, 69), outline=(18, 105, 119), width=3)
    draw.ellipse((-200, 300, 1110, 2740), outline=(22, 119, 132), width=2)
    return canvas


def draw_hero(canvas: Image.Image) -> None:
    hero_source = SOURCE_DIR / "medical-ai-hero.png"
    hero = cover(hero_source, (WIDTH, 850), focus_x=0.38).convert("RGBA")
    shade = Image.new("RGBA", hero.size, (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for x in range(900):
        alpha = max(0, round(220 * (1 - x / 900)))
        shade_draw.line((x, 0, x, 850), fill=(2, 16, 34, alpha))
    shade_draw.rectangle((0, 0, WIDTH, 850), fill=(3, 17, 34, 35))
    hero = Image.alpha_composite(hero, shade)
    canvas.paste(hero.convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 850), outline=(29, 161, 181), width=2)
    nav_font = korean_font(24, True)
    draw.text((70, 54), "AI·SW    의료AI    디지털헬스케어    맞춤형 건강관리", font=nav_font, fill="#CFEAF0")

    draw.text((68, 144), "2026", font=english_font(60, True), fill="white")
    draw.text((68, 220), "ETRI", font=english_font(112, True), fill="white", stroke_width=2, stroke_fill="#13384A")
    draw.text((68, 326), "MEDICAL AI", font=english_font(92, True), fill="#45DCEA")
    draw.text((68, 416), "TECH SERIES", font=english_font(92, True), fill="white")

    draw.rounded_rectangle((72, 555, 485, 627), radius=36, fill="#F2FBFC", outline="#19B8CA", width=5)
    draw.text((118, 571), "ETRI 유망기술 4선", font=korean_font(31, True), fill="#087A91")
    draw.text((71, 686), "미래 건강을 예측하고", font=korean_font(39, True), fill="white")
    draw.text((71, 742), "개인별 최적 관리를 설계하는 의료 AI", font=korean_font(39, True), fill="white")

    draw.rectangle((0, 850, WIDTH, HERO_HEIGHT), fill="#071D35")
    draw.rounded_rectangle((362, 894, 838, 968), radius=37, fill="#0A3149", outline="#38D3E1", width=4)
    draw.ellipse((392, 919, 414, 941), fill="#42E5EF")
    label = "의료·헬스케어 AI 분야"
    bbox = draw.textbbox((0, 0), label, font=korean_font(36, True))
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2 + 14, 907), label, font=korean_font(36, True), fill="white")


def draw_technology(canvas: Image.Image, technology: dict[str, str], index: int) -> None:
    y = HERO_HEIGHT + index * TECH_HEIGHT
    draw = ImageDraw.Draw(canvas)
    panel_top = y + 36
    panel_bottom = y + 324

    shadow = Image.new("RGBA", (WIDTH, TECH_HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((70, 48, 1130, 330), radius=24, fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(shadow, (0, y), shadow)

    fill = "#F1F7F8" if index % 2 == 0 else "#E5F1F3"
    draw.rounded_rectangle((66, panel_top, 1134, panel_bottom), radius=22, fill=fill, outline="#66C9D4", width=3)
    draw.rectangle((66, panel_top, 82, panel_bottom), fill="#13AEC2")

    draw.text((105, panel_top + 82), technology["number"], font=english_font(66, True), fill="#0A263E")
    draw.text((286, panel_top + 34), technology["label"], font=english_font(18, True), fill="#16869A")

    title_font = korean_font(34, True)
    title_lines = wrap_lines(draw, technology["title"], title_font, 590)
    title_y = panel_top + 70
    for line in title_lines[:2]:
        draw.text((286, title_y), line, font=title_font, fill="#071D3C")
        title_y += 48

    description_font = korean_font(23)
    description_lines = wrap_lines(draw, technology["description"], description_font, 590)
    description_y = panel_top + 200
    for line in description_lines[:2]:
        draw.text((287, description_y), line, font=description_font, fill="#405B69")
        description_y += 38

    draw.rounded_rectangle((920, panel_top + 91, 1092, panel_top + 191), radius=18, fill="#072642")
    draw.text((958, panel_top + 113), "SMK", font=english_font(25, True), fill="white")
    draw.text((944, panel_top + 151), "자세히 보기", font=korean_font(20, True), fill="#4CE1EB")


def draw_contact(canvas: Image.Image) -> None:
    y = HERO_HEIGHT + len(TECHNOLOGIES) * TECH_HEIGHT
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, y, WIDTH, HEIGHT), fill="#06233A")
    draw.line((70, y + 20, 1130, y + 20), fill="#38D8E5", width=3)

    draw.rounded_rectangle((260, y + 62, 940, y + 210), radius=74, fill="#F5FCFD", outline="#11AFC2", width=7)
    draw.text((354, y + 91), "기술이전 상담 바로가기", font=korean_font(42, True), fill="#078CA3")
    draw.ellipse((842, y + 91, 904, y + 153), fill="#10AFC2")
    draw.text((860, y + 93), ">", font=english_font(42, True), fill="white")

    phone_y = y + CONTACT_MAIN_HEIGHT
    draw.rounded_rectangle((86, phone_y + 28, 1114, phone_y + 124), radius=18, fill="#0A314A", outline="#61CDDA", width=4)
    draw.text((142, phone_y + 55), "CONTACT", font=english_font(25, True), fill="#46E2EC")
    draw.text((378, phone_y + 50), "yhj@daraebiz.com", font=english_font(27, True), fill="white")
    draw.text((794, phone_y + 50), "042-716-7084", font=english_font(27, True), fill="white")


def build_poster() -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    canvas = gradient_background()
    draw_hero(canvas)
    for index, technology in enumerate(TECHNOLOGIES):
        draw_technology(canvas, technology, index)
    draw_contact(canvas)

    poster_path = OUTPUT_DIR / "etri-medical-ai-newsletter-poster.png"
    canvas.save(poster_path, quality=96, optimize=True)

    slices = [
        ("poster-hero.png", 0, HERO_HEIGHT),
        *[
            (f"poster-tech-{index + 1:02d}.png", HERO_HEIGHT + index * TECH_HEIGHT, HERO_HEIGHT + (index + 1) * TECH_HEIGHT)
            for index in range(4)
        ],
        ("poster-contact-main.png", HERO_HEIGHT + 4 * TECH_HEIGHT, HERO_HEIGHT + 4 * TECH_HEIGHT + CONTACT_MAIN_HEIGHT),
        ("poster-contact-phone.png", HEIGHT - CONTACT_PHONE_HEIGHT, HEIGHT),
    ]
    for filename, top, bottom in slices:
        canvas.crop((0, top, WIDTH, bottom)).save(ASSET_DIR / filename, quality=96, optimize=True)
    return poster_path


def image_tag(filename: str, height: int, alt: str) -> str:
    return (
        f'<img src="{PUBLIC_BASE}assets/{filename}" width="600" height="{height}" alt="{alt}" '
        'style="display:block; width:100%; max-width:600px; height:auto; margin:0; padding:0; border:0; outline:none; text-decoration:none;">'
    )


def linked_image(href: str, filename: str, height: int, alt: str) -> str:
    return (
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" style="display:block; text-decoration:none;">'
        f'{image_tag(filename, height, alt)}</a>'
    )


def build_html() -> Path:
    technology_rows = []
    for technology in TECHNOLOGIES:
        number = technology["number"]
        technology_rows.append(
            f'            <tr><td style="padding:0;">{linked_image(technology["url"], f"poster-tech-{number}.png", 180, technology["title"] + " — SMK 자세히 보기")}</td></tr>'
        )

    html = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ETRI 의료·헬스케어 AI 기술이전 안내</title>
  </head>
  <body style="margin:0; padding:0; background:#DDE5EA;">
    <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:transparent;">ETRI 의료·헬스케어 AI 유망기술 4선과 기술이전 상담 안내</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; margin:0; border-collapse:collapse; background:#DDE5EA;">
      <tr>
        <td align="center" style="padding:24px 0;">
          <table data-design-reference="etri-tech-series-poster-2026" role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%; max-width:600px; margin:0; border-collapse:collapse; background:#06233A;">
            <tr><td style="padding:0;">{image_tag("poster-hero.png", 500, "2026 ETRI 의료 AI TECH SERIES")}</td></tr>
{chr(10).join(technology_rows)}
            <tr><td style="padding:0;">{linked_image("mailto:yhj@daraebiz.com", "poster-contact-main.png", 130, "기술이전 상담 이메일 보내기")}</td></tr>
            <tr><td style="padding:0;">{linked_image("tel:042-716-7084", "poster-contact-phone.png", 80, "기술이전 상담 전화하기")}</td></tr>
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
    poster_path = build_poster()
    html_path = build_html()
    print(f"generated {poster_path} and {html_path}")
