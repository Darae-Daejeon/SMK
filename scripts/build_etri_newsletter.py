from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "ETRI" / "newsletter"
ASSET_DIR = OUTPUT_DIR / "assets"
SOURCE_DIR = OUTPUT_DIR / "source-assets"
PUBLIC_BASE = "https://darae-daejeon.github.io/SMK/ETRI/newsletter/"

TECHNOLOGIES = [
    {
        "number": "01",
        "label": "MEDICAL INTELLIGENCE",
        "title": "미래 건강 예측을 위한 의료지능 딥러닝 엔진 기술",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-01.html",
    },
    {
        "number": "02",
        "label": "PROGNOSIS PREDICTION",
        "title": "미래 건강상태 및 예후 예측을 위한 헬스케어 인공지능 기술",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-02.html",
    },
    {
        "number": "03",
        "label": "PERSONALIZED HEALTHCARE",
        "title": "개인 맞춤형 건강 관리 프로그램을 계획하는 인공지능 헬스케어 기술",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-03.html",
    },
    {
        "number": "04",
        "label": "OPTIMAL HEALTH MANAGEMENT",
        "title": "미래 건강 상태의 맞춤형 예측 및 최적 관리를 위한 인공지능 기술",
        "url": "https://darae-daejeon.github.io/SMK/ETRI/tech-04.html",
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf")
    if not path.exists():
        raise FileNotFoundError(path)
    return ImageFont.truetype(str(path), size)


def cover(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, round((image.width - size[0]) * 0.43))
    top = max(0, (image.height - size[1]) // 2)
    return image.crop((left, top, left + size[0], top + size[1]))


def build_hero() -> Path:
    source = SOURCE_DIR / "medical-ai-hero.png"
    if not source.exists():
        raise FileNotFoundError(source)

    canvas = cover(source, (1200, 760)).convert("RGBA")
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for x in range(900):
        alpha = max(0, round(228 * (1 - x / 900)))
        overlay_draw.line((x, 0, x, 760), fill=(2, 12, 35, alpha))
    overlay_draw.rectangle((0, 0, 1200, 760), fill=(2, 13, 38, 28))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((68, 62, 320, 116), fill="#42E3EC")
    draw.text((91, 73), "ETRI TECHNOLOGY", font=font(25, True), fill="#06142E")
    draw.text((67, 178), "의료 AI,", font=font(86, True), fill="white")
    draw.text((67, 292), "기업의 다음 서비스를", font=font(65, True), fill="#43E4EE")
    draw.text((67, 384), "만들다", font=font(65, True), fill="#43E4EE")
    draw.rectangle((70, 503, 524, 508), fill="#43E4EE")
    draw.text((68, 540), "예측부터 개인 맞춤형 건강 관리까지", font=font(31, True), fill="white")
    draw.text((68, 599), "사업화 가능한 ETRI 의료·헬스케어 AI 기술 4선", font=font(25), fill="#C3D7E9")

    path = ASSET_DIR / "newsletter-hero.png"
    canvas.convert("RGB").save(path, quality=96, optimize=True)
    return path


def image_tag(filename: str, width: int, height: int, alt: str) -> str:
    return (
        f'<img src="{PUBLIC_BASE}assets/{filename}" width="{width}" height="{height}" alt="{alt}" '
        f'style="display:block; width:100%; max-width:{width}px; height:auto; margin:0; padding:0; border:0; outline:none; text-decoration:none;">'
    )


def technology_row(technology: dict[str, str], index: int) -> str:
    background = "#FFFFFF" if index % 2 else "#F4F7FA"
    return f'''            <tr>
              <td data-tech-row="{technology['number']}" style="padding:0; background:{background}; border-bottom:1px solid #D8E0E8;">
                <a href="{technology['url']}" target="_blank" rel="noopener noreferrer" style="display:block; color:#071832; text-decoration:none;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; border-collapse:collapse;">
                    <tr>
                      <td class="tech-number" width="82" valign="middle" style="width:82px; padding:26px 0 25px 30px; color:#00AFC1; font-family:Arial,sans-serif; font-size:30px; line-height:1; font-weight:700;">{technology['number']}</td>
                      <td class="tech-copy" valign="middle" style="padding:24px 15px 23px 0; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif;">
                        <div style="color:#637589; font-family:Arial,sans-serif; font-size:10px; line-height:1.4; letter-spacing:1px; font-weight:700;">{technology['label']}</div>
                        <div style="padding-top:7px; color:#071832; font-size:17px; line-height:1.55; font-weight:700; word-break:keep-all;">{technology['title']}</div>
                      </td>
                      <td class="tech-action" width="92" align="right" valign="middle" style="width:92px; padding:24px 30px 23px 0; font-family:Arial,sans-serif;">
                        <span class="view-smk" style="display:inline-block; padding:10px 12px; background:#071832; color:#FFFFFF; font-size:10px; line-height:1; letter-spacing:.5px; font-weight:700; white-space:nowrap;">VIEW SMK</span>
                      </td>
                    </tr>
                  </table>
                </a>
              </td>
            </tr>'''


def build_html() -> Path:
    hero = image_tag("newsletter-hero.png", 600, 380, "ETRI 의료·헬스케어 AI 기술이전 안내")
    rows = "\n".join(technology_row(technology, index) for index, technology in enumerate(TECHNOLOGIES))

    html = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ETRI 의료·헬스케어 AI 기술이전 안내</title>
    <style>
      @media screen and (max-width:600px) {{
        .tech-number {{ width:48px !important; padding-left:16px !important; font-size:24px !important; }}
        .tech-copy {{ padding-right:7px !important; }}
        .tech-copy div:last-child {{ font-size:14px !important; line-height:1.5 !important; }}
        .tech-action {{ width:58px !important; padding-right:16px !important; }}
        .view-smk {{ padding:8px 7px !important; font-size:8px !important; }}
      }}
    </style>
  </head>
  <body style="margin:0; padding:0; background:#E9EEF3;">
    <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:transparent;">사업화 가능한 ETRI 의료·헬스케어 AI 기술 4선을 확인하세요.</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%; margin:0; border-collapse:collapse; background:#E9EEF3;">
      <tr>
        <td align="center" style="padding:24px 0;">
          <table data-design-reference="kist-editorial-2026" role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%; max-width:600px; margin:0; border-collapse:collapse; background:#FFFFFF;">
            <tr><td style="padding:0; background:#071832;">{hero}</td></tr>
            <tr>
              <td style="padding:30px 30px 26px 30px; background:#071832; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#FFFFFF;">
                <div style="color:#42E3EC; font-family:Arial,sans-serif; font-size:11px; line-height:1.4; letter-spacing:2px; font-weight:700;">SELECTED TECHNOLOGIES</div>
                <div style="padding-top:8px; font-size:25px; line-height:1.4; font-weight:700;">사업화 가능 기술 4선</div>
                <div style="padding-top:8px; color:#B8C7D8; font-size:13px; line-height:1.7;">기술명을 선택하면 상세 SMK로 이동합니다.</div>
              </td>
            </tr>
{rows}
            <tr>
              <td align="center" style="padding:31px 24px 33px 24px; background:#42E3EC; font-family:'Malgun Gothic','Apple SD Gothic Neo',Arial,sans-serif; color:#06152F;">
                <div style="font-family:Arial,sans-serif; font-size:10px; line-height:1.4; letter-spacing:2px; font-weight:700;">TECH TRANSFER CONTACT</div>
                <div style="padding-top:7px; font-size:22px; line-height:1.45; font-weight:700;">기술이전 상담</div>
                <div style="padding-top:13px; font-size:14px; line-height:1.8; font-weight:700;">
                  <a href="mailto:yhj@daraebiz.com" style="color:#06152F; text-decoration:none;">yhj@daraebiz.com</a><br>
                  <a href="tel:042-716-7084" style="color:#06152F; text-decoration:none;">042-716-7084</a>
                </div>
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
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    hero_path = build_hero()
    html_path = build_html()
    print(f"generated {hero_path} and {html_path}")
