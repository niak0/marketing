#!/usr/bin/env python3
"""Kart şablonunun kullandığı web fontlarını yerele indirir.

Google Fonts'tan woff2 dosyalarını çeker ve `fonts/` altına kaydeder.
Şablon bunları base64 olarak gömer — böylece Chrome render'ı ağa
bağımlı olmaz ve çıktı her seferinde aynı olur.

Kullanım:
    python3 fetch_fonts.py
"""

import logging
import re
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("fonts")

FONT_DIR = Path(__file__).resolve().parent / "fonts"

# Chrome UA -> Google Fonts woff2 döndürür (TTF yerine).
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

FAMILIES = {
    "bricolage": (
        "Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800"
    ),
    "archivo": "Archivo:wdth,wght@62..125,400..900",
    "space-grotesk": "Space+Grotesk:wght@400..700",
    "inter": "Inter:opsz,wght@14..32,400..700",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def latin_ext_urls(css: str) -> list[str]:
    """CSS'ten latin ve latin-ext subset'lerinin woff2 URL'lerini alır."""
    blocks = css.split("/*")
    wanted = []
    for block in blocks:
        if not block.startswith((" latin ", " latin-ext ")):
            continue
        found = re.findall(r"url\((https://[^)]+\.woff2)\)", block)
        wanted.extend(found)
    if not wanted:
        wanted = re.findall(r"url\((https://[^)]+\.woff2)\)", css)
    return wanted


def download_family(slug: str, spec: str) -> None:
    css_url = f"https://fonts.googleapis.com/css2?family={spec}&display=swap"
    css = fetch(css_url).decode("utf-8")
    urls = latin_ext_urls(css)
    if not urls:
        raise RuntimeError(f"{slug}: woff2 bağlantısı bulunamadı")

    for index, url in enumerate(urls):
        suffix = "" if index == 0 else f"-{index}"
        target = FONT_DIR / f"{slug}{suffix}.woff2"
        target.write_bytes(fetch(url))
        logger.info("  %s (%d KB)", target.name, target.stat().st_size // 1024)


def main() -> None:
    FONT_DIR.mkdir(exist_ok=True)
    for slug, spec in FAMILIES.items():
        logger.info("%s indiriliyor...", slug)
        download_family(slug, spec)
    logger.info("Fontlar hazır: %s", FONT_DIR)


if __name__ == "__main__":
    main()
