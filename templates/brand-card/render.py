#!/usr/bin/env python3
"""ideavoll marka kartı (4:5 Instagram post) üretici.

JSON kart tanımını HTML şablonuna doldurur ve Chrome headless ile
1080x1350 PNG'ye render eder. Metin/logo tarayıcıda çizildiği için
Türkçe karakterler ve marka renkleri birebir doğru çıkar.

Kullanım:
    python3 render.py cards/sabah_kosusu.json [-o cikti.png]
"""

import argparse
import base64
import io
import json
import logging
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("brand-card")

TEMPLATE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEMPLATE_DIR.parents[1]
CHROME = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
CANVAS = (1080, 1350)
SCALE = 2

ICONS = {
    "plus": "M12 5v14M5 12h14",
    "pin": (
        "M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"
        "M12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"
    ),
    "users": (
        "M16 20v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"
        "M9 10a4 4 0 1 0 0-8 4 4 0 0 0 0 8"
        "M22 20v-2a4 4 0 0 0-3-3.9M16 2.1a4 4 0 0 1 0 7.8"
    ),
    "compass": (
        "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"
        "M15.9 8.1l-2.1 5.8-5.8 2.1 2.1-5.8 5.8-2.1z"
    ),
    "calendar": (
        "M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6"
        "a2 2 0 0 0-2-2zM3 10h18M16 2v4M8 2v4"
    ),
    "heart": (
        "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0"
        "-7.8 7.8l1.1 1L12 21l7.7-7.6 1.1-1a5.5 5.5 0 0 0 0-7.8z"
    ),
    "bolt": "M13 2L3 14h8l-1 8 10-12h-8l1-8z",
}

ICON_TINTS = {
    "blue": ("rgba(3, 112, 251, 0.12)", "#0370FB"),
    "orange": ("rgba(253, 114, 1, 0.14)", "#FD7201"),
    "violet": ("rgba(109, 76, 255, 0.13)", "#6D4CFF"),
}


def encode_image(path: Path, max_width: int, quality: int = 88) -> str:
    """Görseli küçültüp base64 data URI'ye çevirir."""
    with Image.open(path) as source:
        image = source.convert("RGB")
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, "JPEG", quality=quality)
    payload = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{payload}"


def encode_logo(path: Path, size: int = 200) -> str:
    """Logoyu saydamlığı koruyarak base64 PNG'ye çevirir."""
    with Image.open(path) as source:
        image = source.convert("RGBA").resize(
            (size, size), Image.LANCZOS
        )
        buffer = io.BytesIO()
        image.save(buffer, "PNG")
    payload = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{payload}"


def build_feature(feature: dict) -> str:
    """Tek bir ikon+başlık+açıklama satırının HTML'ini üretir."""
    tint, stroke = ICON_TINTS.get(
        feature.get("tint", "blue"), ICON_TINTS["blue"]
    )
    path = ICONS.get(feature.get("icon", "plus"), ICONS["plus"])
    svg = (
        f'<svg viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
        f'stroke-width="2.1" stroke-linecap="round" '
        f'stroke-linejoin="round"><path d="{path}"/></svg>'
    )
    return (
        '<div class="feature">'
        f'<div class="feature-icon" style="background:{tint}">{svg}'
        "</div><div><div class=\"feature-title\">"
        f'{feature["title"]}</div>'
        f'<div class="feature-body">{feature["body"]}</div>'
        "</div></div>"
    )


def resolve(path_value: str) -> Path:
    """Kart JSON'undaki yolu proje köküne göre çözer."""
    path = Path(path_value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def build_html(card: dict) -> str:
    """Kart tanımını doldurulmuş HTML'e dönüştürür."""
    template = (TEMPLATE_DIR / "template.html").read_text("utf-8")
    features = "".join(build_feature(f) for f in card["features"])

    photo_block = ""
    if card.get("photo"):
        src = encode_image(resolve(card["photo"]), 1300)
        photo_block = f'<img class="photo" src="{src}" alt="">'

    device_block = ""
    if card.get("device_screenshot"):
        src = encode_image(resolve(card["device_screenshot"]), 820)
        device_block = f'<div class="device"><img src="{src}"></div>'

    logo = encode_logo(resolve(card.get("logo", "brand/logo.png")))
    replacements = {
        "{{THEME}}": card.get("theme", "light"),
        "{{LOGO_SRC}}": logo,
        "{{HEADLINE}}": card["headline"],
        "{{LEDE}}": card["lede"],
        "{{FEATURES}}": features,
        "{{CTA}}": card.get("cta", "Etkinlik Oluştur"),
        "{{TAG}}": card.get("tag", ""),
        "{{PHOTO_BLOCK}}": photo_block,
        "{{DEVICE_BLOCK}}": device_block,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def shoot(html: str, output: Path) -> None:
    """HTML'i Chrome headless ile render edip PNG olarak kaydeder."""
    with tempfile.TemporaryDirectory() as workdir:
        page = Path(workdir) / "card.html"
        page.write_text(html, "utf-8")
        raw = Path(workdir) / "raw.png"
        command = [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            f"--force-device-scale-factor={SCALE}",
            f"--window-size={CANVAS[0]},{CANVAS[1]}",
            f"--screenshot={raw}",
            page.as_uri(),
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=120
        )
        if not raw.exists():
            logger.error("Chrome çıktısı: %s", result.stderr[-800:])
            raise RuntimeError("Chrome ekran görüntüsü üretemedi.")
        with Image.open(raw) as shot:
            shot.convert("RGB").resize(CANVAS, Image.LANCZOS).save(
                output, "PNG"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", help="Kart tanımı (JSON)")
    parser.add_argument("-o", "--output", help="Çıktı PNG yolu")
    args = parser.parse_args()

    card_path = Path(args.card)
    card = json.loads(card_path.read_text("utf-8"))
    output = Path(args.output) if args.output else card_path.with_suffix(
        ".png"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    shoot(build_html(card), output)
    logger.info("Kart üretildi: %s (%dx%d)", output, *CANVAS)


if __name__ == "__main__":
    main()
