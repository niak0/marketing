#!/usr/bin/env python3
"""ideavoll animasyonlu Reel (9:16 mp4) üretici.

reel.html'deki CSS animasyonlarını kare kare yakalar ve ffmpeg ile
videoya çevirir. Her kare için şablona `--t` (kare zamanı) enjekte
edilir; animasyonlar duraklatıldığı ve gecikmeleri `calc(x - var(--t))`
olduğu için kare tam o ana sabitlenir.

Kullanım:
    python3 render_reel.py cards/reel_sabah_kosusu.json \
        -o ../../posts/<klasör>/reel.mp4 [--music yol.wav]
"""

import argparse
import logging
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from render import CHROME, build_html, json, resolve

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("reel")

CANVAS = (1080, 1920)
DURATION_MS = 6000
FPS = 24
WORKERS = 4


def frame_times() -> list[int]:
    step = 1000 / FPS
    count = int(DURATION_MS / step)
    return [round(index * step) for index in range(count)]


def shoot_frame(args: tuple[str, int, Path, Path]) -> Path:
    """Tek kareyi Chrome ile yakalar."""
    html, time_ms, workdir, target = args
    page = workdir / f"f{time_ms}.html"
    page.write_text(
        html.replace("--t: 0ms;", f"--t: {time_ms}ms;"), "utf-8"
    )
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
        f"--window-size={CANVAS[0]},{CANVAS[1]}",
        f"--screenshot={target}",
        page.as_uri(),
    ]
    subprocess.run(command, capture_output=True, timeout=180)
    if not target.exists():
        raise RuntimeError(f"Kare üretilemedi: {time_ms}ms")
    return target


def encode(frame_dir: Path, output: Path, music: Path | None) -> None:
    """Kareleri H.264 mp4'e çevirir, varsa müziği bindirir."""
    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS),
        "-i", str(frame_dir / "frame_%04d.png"),
    ]
    if music:
        command += ["-i", str(music), "-shortest", "-c:a", "aac",
                    "-b:a", "160k"]
    command += [
        "-c:v", "libx264", "-preset", "slow", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True, timeout=600)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", help="Reel tanımı (JSON)")
    parser.add_argument("-o", "--output", required=True, help="mp4 yolu")
    parser.add_argument("-t", "--template", default="reel.html")
    parser.add_argument("--music", help="Arka plan müziği (wav/mp3)")
    args = parser.parse_args()

    card = json.loads(Path(args.card).read_text("utf-8"))
    html = build_html(card, args.template, "story")
    times = frame_times()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        jobs = [
            (html, time_ms, workdir, workdir / f"frame_{i:04d}.png")
            for i, time_ms in enumerate(times)
        ]
        logger.info("%d kare üretiliyor (%d fps)...", len(jobs), FPS)
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            for done, _ in enumerate(pool.map(shoot_frame, jobs), 1):
                if done % 24 == 0:
                    logger.info("  %d/%d kare", done, len(jobs))

        music = resolve(args.music) if args.music else None
        encode(workdir, output, music)

    logger.info("Reel hazır: %s (%dx%d, %.1fs)", output, *CANVAS,
                DURATION_MS / 1000)


if __name__ == "__main__":
    main()
