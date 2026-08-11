#!/usr/bin/env python3
"""reel_overlay.html'in şeffaf zeminli kare dizisini üretir.

render_reel.py'nin aksine bir AI videosunun ÜSTÜNE bindirilmek için
saydam PNG kareler üretir (fotoğraf/kenburns katmanı yok, arka plan
alfa=0). Kareler ffmpeg overlay filtresine doğrudan image sequence
olarak beslenir.

Kullanım:
    python3 render_reel_overlay.py cards/reel_yoga_cta.json \
        -o ../../posts/<klasör>/cta_frames --duration-ms 5500
"""

import argparse
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from render import CHROME, build_html, json

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("reel-overlay")

CANVAS = (1080, 1920)
FPS = 24
WORKERS = 4


def frame_times(duration_ms: int) -> list[int]:
    step = 1000 / FPS
    count = int(duration_ms / step)
    return [round(index * step) for index in range(count)]


def shoot_frame(args: tuple[str, int, Path, Path]) -> Path:
    html, time_ms, workdir, target = args
    page = workdir / f"f{time_ms}.html"
    page.write_text(html.replace("--t: 0ms;", f"--t: {time_ms}ms;"), "utf-8")
    command = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-sandbox",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-sync",
        "--default-background-color=00000000",
        f"--window-size={CANVAS[0]},{CANVAS[1]}",
        f"--screenshot={target}",
        page.as_uri(),
    ]
    subprocess.run(command, capture_output=True, timeout=180)
    if not target.exists():
        raise RuntimeError(f"Kare üretilemedi: {time_ms}ms")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", help="Reel tanımı (JSON)")
    parser.add_argument("-o", "--output", required=True,
                         help="Kare dizini (frame_%%04d.png buraya yazılır)")
    parser.add_argument("-t", "--template", default="reel_overlay.html")
    parser.add_argument("--duration-ms", type=int, default=6000)
    args = parser.parse_args()

    card = json.loads(Path(args.card).read_text("utf-8"))
    html = build_html(card, args.template, "story")
    times = frame_times(args.duration_ms)

    workdir = Path(args.output).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    jobs = [
        (html, time_ms, workdir, workdir / f"frame_{i:04d}.png")
        for i, time_ms in enumerate(times)
    ]
    logger.info("%d kare üretiliyor (%d fps, şeffaf zemin)...",
                len(jobs), FPS)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for done, _ in enumerate(pool.map(shoot_frame, jobs), 1):
            if done % 24 == 0:
                logger.info("  %d/%d kare", done, len(jobs))

    logger.info("Kareler hazır: %s (%.1fs)", workdir, args.duration_ms / 1000)


if __name__ == "__main__":
    main()
