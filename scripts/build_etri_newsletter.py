from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "ETRI" / "newsletter"
ASSET_DIR = OUTPUT_DIR / "assets"
SOURCE_DIR = OUTPUT_DIR / "source-assets"
PUBLIC_BASE = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/"

TECHNOLOGIES = [
    {
        "number": "01",
        "title": "미래 건강 예측을 위한\n의료지능 딥러닝 엔진 기술",
        "keyword": "DEEP LEARNING ENGINE",
        "source": ROOT / "ETRI" / "assets" / "tech-01" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-01.html",
        "base": "#20D5E5",
        "deep": "#087A9C",
    },
    {
        "number": "02",
        "title": "미래 건강상태 및 예후 예측\n헬스케어 인공지능 기술",
        "keyword": "PROGNOSIS AI",
        "source": ROOT / "ETRI" / "assets" / "tech-02" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-02.html",
        "base": "#37C8F1",
        "deep": "#2363B4",
    },
    {
        "number": "03",
        "title": "개인 맞춤형 건강 관리 계획\n인공지능 헬스케어 기술",
        "keyword": "PERSONALIZED CARE",
        "source": ROOT / "ETRI" / "assets" / "tech-03" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-03.html",
        "base": "#2FDCC6",
        "deep": "#087B8F",
    },
    {
        "number": "04",
        "title": "미래 건강 상태 맞춤형 예측 및\n최적 관리 인공지능 기술",
        "keyword": "OPTIMAL HEALTH",
        "source": ROOT / "ETRI" / "assets" / "tech-04" / "representative.png",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-04.html",
        "base": "#6CB8ED",
        "deep": "#4149A5",
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("C:/Windows/Fonts/NotoSansKR-VF.ttf"),
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("A Korean font was not found")


def cover(source: Path, size: tuple[int, int], focus_x: float = 0.5) -> Image.Image:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
    )
    max_left = image.width - size[0]
    left = round(max_left * focus_x)
    top = (image.height - size[1]) // 2
    return image.crop((left, top, left + size[0], top + size[1]))


def vertical_gradient(size: tuple[int, int], top: str, bottom: str) -> Image.Image:
    start = tuple(int(top[i : i + 2], 16) for i in (1, 3, 5))
    end = tuple(int(bottom[i : i + 2], 16) for i in (1, 3, 5))
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for y in range(size[1]):
        ratio = y / max(1, size[1] - 1)
        color = tuple(round(start[index] * (1 - ratio) + end[index] * ratio) for index in range(3))
        draw.line((0, y, size[0], y), fill=color)
    return image


def build_hero() -> Path:
    source = SOURCE_DIR / "medical-ai-hero.png"
    if not source.exists():
        raise FileNotFoundError(source)

    canvas = cover(source, (600, 420), focus_x=0.42).convert("RGBA")
    shade = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for x in range(430):
        alpha = max(0, round(205 * (1 - x / 430)))
        shade_draw.line((x, 0, x, 420), fill=(5, 16, 43, alpha))
    shade_draw.rectangle((0, 0, 600, 420), outline=(63, 228, 243, 80), width=2)
    canvas = Image.alpha_composite(canvas, shade)
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((34, 31, 202, 62), radius=3, fill="#1DD7E8")
    draw.text((47, 35), "ETRI 보유 유망기술", font=font(14, True), fill="#071530")
    draw.text((34, 92), "의료·헬스케어", font=font(37, True), fill="white")
    draw.text((34, 144), "AI 기술이전", font=font(48, True), fill="#43E4F2")
    draw.rectangle((35, 218, 293, 220), fill="#37DDEA")
    draw.text((34, 240), "미래 건강을 예측하고", font=font(18, True), fill="white")
    draw.text((34, 269), "개인별 최적 관리를 설계하는 기술", font=font(18, True), fill="white")

    tags = ["건강 예측", "예후 분석", "맞춤 계획", "최적 관리"]
    x = 34
    for tag in tags:
        width = draw.textbbox((0, 0), tag, font=font(12, True))[2] + 24
        draw.rounded_rectangle((x, 325, x + width, 355), radius=15, fill=(11, 42, 80, 220), outline="#47DDEB")
        draw.text((x + 12, 330), tag, font=font(12, True), fill="#BFF9FF")
        x += width + 8
    draw.text((35, 382), "Electronics and Telecommunications Research Institute", font=font(10), fill="#9CB8D2")

    path = ASSET_DIR / "newsletter-hero.png"
    canvas.convert("RGB").save(path, quality=94, optimize=True)
    return path


def build_card(technology: dict[str, str | Path]) -> Path:
    width, height = 280, 190
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((8, 17, 274, 187), radius=11, fill=(0, 0, 0, 105))
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))

    canvas = Image.new("RGBA", (width, height), (8, 22, 54, 255))
    canvas = Image.alpha_composite(canvas, shadow)

    card = vertical_gradient((264, 168), str(technology["base"]), str(technology["deep"])).convert("RGBA")
    card_mask = Image.new("L", card.size, 0)
    mask_draw = ImageDraw.Draw(card_mask)
    mask_draw.rounded_rectangle((0, 12, 264, 168), radius=10, fill=255)
    mask_draw.polygon([(0, 12), (0, 4), (86, 4), (101, 16), (264, 16), (264, 42), (0, 42)], fill=255)
    canvas.paste(card, (8, 10), card_mask)

    visual = cover(Path(technology["source"]), (112, 168), focus_x=0.5)
    visual = ImageEnhance.Color(visual).enhance(0.6)
    visual = ImageEnhance.Contrast(visual).enhance(1.1).convert("RGBA")
    visual.putalpha(vertical_alpha((112, 168), 30, 205))
    canvas.alpha_composite(visual, (160, 10))

    gloss = Image.new("RGBA", (264, 168), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    gloss_draw.polygon([(0, 0), (264, 0), (264, 34), (0, 86)], fill=(255, 255, 255, 24))
    canvas.alpha_composite(gloss, (8, 10))

    draw = ImageDraw.Draw(canvas)
    draw.text((22, 25), str(technology["number"]), font=font(15, True), fill="#071630")
    draw.text((54, 27), str(technology["keyword"]), font=font(9, True), fill="#0B4565")

    y = 64
    for line in str(technology["title"]).splitlines():
        draw.text((22, y), line, font=font(15, True), fill="white", stroke_width=1, stroke_fill=(0, 51, 80, 90))
        y += 25

    draw.rounded_rectangle((21, 132, 143, 161), radius=14, fill="#081936")
    draw.text((38, 137), "SMK 자세히 보기  →", font=font(10, True), fill="#B9FAFF")
    draw.line((8, 177, 272, 177), fill=(72, 231, 242, 180), width=1)

    path = ASSET_DIR / f"tech-{technology['number']}-folder.png"
    canvas.convert("RGB").save(path, quality=92, optimize=True)
    return path


def vertical_alpha(size: tuple[int, int], left: int, right: int) -> Image.Image:
    alpha = Image.new("L", size)
    draw = ImageDraw.Draw(alpha)
    for x in range(size[0]):
        value = round(left + (right - left) * x / max(1, size[0] - 1))
        draw.line((x, 0, x, size[1]), fill=value)
    return alpha


def build_assets() -> list[Path]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for technology in TECHNOLOGIES:
        if not Path(technology["source"]).exists():
            raise FileNotFoundError(technology["source"])
    return [build_hero(), *(build_card(technology) for technology in TECHNOLOGIES)]


def image_tag(filename: str, width: int, height: int, alt: str) -> str:
    return (
        f'<img src="{PUBLIC_BASE}assets/{filename}" width="{width}" height="{height}" alt="{alt}" '
        f'style="display:block; width:100%; max-width:{width}px; height:auto; margin:0; padding:0; border:0; outline:none; text-decoration:none;">'
    )


def card_cell(technology: dict[str, str | Path], side: str) -> str:
    card = image_tag(
        f"tech-{technology['number']}-folder.png",
        280,
        190,
        f"{str(technology['title']).replace(chr(10), ' ')} — SMK 자세히 보기",
    )
    padding = "0 5px 10px 15px" if side == "left" else "0 15px 10px 5px"
    return f'''<td width="300" valign="top" style="width:50%; padding:{padding};">
                    <a data-tech-card="{technology['number']}" href="{technology['url']}" target="_blank" rel="noopener noreferrer" style="display:block; text-decoration:none;">{card}</a>
                  </td>'''


def build_html() -> Path:
    hero = image_tag("newsletter-hero.png", 600, 420, "ETRI 의료·헬스케어 AI 기술이전 안내")
    rows = []
    for index in range(0, 4, 2):
        rows.append(
            "                <tr>\n                  "
            + card_cell(TECHNOLOGIES[index], "left")
            + "\n                  "
            + card_cell(TECHNOLOGIES[index + 1], "right")
            + "\n                </tr>"
        )

    html = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ETRI 의료·헬스케어 AI 기술이전 안내</title>
  </head>
  <body style="margin:0; padding:0; background:#e8edf3;">
    <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:transparent;">미래 건강 예측부터 개인 맞춤형 관리까지, ETRI 의료 AI 기술 4종을 확인하세요.</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; margin:0; border-collapse:collapse; background:#e8edf3;">
      <tr>
        <td align="center" style="padding:24px 0;">
          <table data-design-reference="kist-connect-2026" role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%; max-width:600px; margin:0; border-collapse:collapse; background:#081636;">
            <tr><td style="padding:0;">{hero}</td></tr>
            <tr>
              <td style="padding:25px 30px 22px 30px; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; background:#081636; color:#ffffff;">
                <div style="color:#39ddea; font-size:11px; line-height:1.4; letter-spacing:2px; font-weight:700;">ETRI TECHNOLOGY PORTFOLIO</div>
                <div style="padding-top:7px; font-size:24px; line-height:1.35; font-weight:700;">사업화 가능 기술 4선</div>
                <div style="padding-top:8px; color:#a9bfd4; font-size:13px; line-height:1.7;">관심 기술 카드를 선택하면 상세 SMK로 이동합니다.</div>
              </td>
            </tr>
            <tr>
              <td style="padding:0; background:#081636;">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%; max-width:600px; border-collapse:collapse;">
{chr(10).join(rows)}
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding:22px 30px 25px 30px; background:#102750; border-top:1px solid #28466e; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#ffffff;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; border-collapse:collapse;">
                  <tr>
                    <td align="center" valign="middle">
                      <div style="color:#42e0ec; font-size:11px; letter-spacing:1px; font-weight:700;">TECH TRANSFER CONSULTING</div>
                      <div style="padding-top:5px; font-size:19px; line-height:1.45; font-weight:700;">기술이전·사업화 상담</div>
                    </td>
                  </tr>
                  <tr>
                    <td align="center" valign="middle" style="padding-top:12px; font-size:13px; line-height:1.8;">
                      <a href="mailto:yhj@daraebiz.com" style="color:#ffffff; text-decoration:none; font-weight:700;">yhj@daraebiz.com</a><br>
                      <a href="tel:042-716-7084" style="color:#42e0ec; text-decoration:none; font-weight:700;">042-716-7084</a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td align="center" style="padding:15px 20px 17px 20px; background:#061129; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#718ba7; font-size:10px; line-height:1.6;">다래전략사업화센터 대전지사 · ETRI 보유기술 사업화 협력 안내</td>
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
