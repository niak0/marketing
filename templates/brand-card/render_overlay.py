#!/usr/bin/env python3
"""Video üstüne bindirilecek saydam metin katmanı üretici.

reel.html'in aksine bu tek bir durağan PNG üretir (alfa kanallı,
şeffaf zemin) — ffmpeg overlay ile bir AI videosunun üstüne
bindirilmek için. Marka fontu/rengiyle Chrome'da çizilir; metin
asla AI'a çizdirilmez.

Kullanım:
    python3 render_overlay.py "Yarın sabah,<br>sahilde." \
        -o ../../posts/<klasör>/overlay.png
"""

import argparse
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from render import CHROME, TEMPLATE_DIR, font_faces

CANVAS = (1080, 1920)
SCALE = 2


def build_html(headline: str) -> str:
    template = (TEMPLATE_DIR / "overlay_text.html").read_text("utf-8")
    return (
        template.replace("{{FONT_FACES}}", font_faces())
        .replace("{{HEADLINE}}", headline)
    )


def shoot(html: str, output: Path) -> None:
    with tempfile.TemporaryDirectory() as workdir:
        page = Path(workdir) / "overlay.html"
        page.write_text(html, "utf-8")
        raw = Path(workdir) / "raw.png"
        command = [
            CHROME,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            "--default-background-color=00000000",
            f"--force-device-scale-factor={SCALE}",
            f"--window-size={CANVAS[0]},{CANVAS[1]}",
            f"--screenshot={raw}",
            page.as_uri(),
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=120
        )
        if not raw.exists():
            raise RuntimeError(f"Chrome çıktısı: {result.stderr[-800:]}")
        with Image.open(raw) as shot:
            shot.convert("RGBA").resize(CANVAS, Image.LANCZOS).save(
                output, "PNG"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("headline", help="<br> ve <em> desteklenir")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    html = build_html(args.headline)
    shoot(html, output)
    print(f"Overlay hazır: {output}")


if __name__ == "__main__":
    main()
