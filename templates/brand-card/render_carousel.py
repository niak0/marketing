#!/usr/bin/env python3
"""ideavoll carousel (çok slaytlı Instagram postu) üretici.

Tek JSON'dan sıralı slayt PNG'leri üretir. Ortak alanlar (logo, tag)
slaytlara miras geçer; her slaytın `role` alanı düzeni belirler:
`hook` (kanca), `step` (adım), `cta` (kapanış).

Kullanım:
    python3 render_carousel.py cards/carousel_etkinlik.json \
        -o ../../posts/<klasör>/slayt.png
"""

import argparse
import json
import logging
from pathlib import Path

from render import FORMATS, build_html, shoot

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("carousel")

SWIPE = (
    '<div class="swipe"><span>{label}</span>'
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.4" stroke-linecap="round" '
    'stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    "</div>"
)

CTA_TAIL = (
    '<div class="cta"><svg viewBox="0 0 24 24" fill="none" '
    'stroke="#fff" stroke-width="2.4" stroke-linecap="round">'
    '<path d="M12 5v14M5 12h14"/></svg><span>{cta}</span></div>'
    '<div class="bottom"><span class="handle">ideavoll.com</span>'
    '<span class="handle">{tag}</span></div>'
)


def build_tail(slide: dict, is_last: bool) -> str:
    """Slaytın alt bölümünü (kaydır oku ya da CTA) üretir."""
    if slide.get("role") == "cta" or is_last:
        return CTA_TAIL.format(
            cta=slide.get("cta", "Etkinlik Oluştur"),
            tag=slide.get("tag", ""),
        )
    return SWIPE.format(label=slide.get("swipe", "kaydır"))


def slide_payload(
    shared: dict, slide: dict, index: int, total: int
) -> dict:
    """Ortak alanlarla slaytı birleştirip render girdisi üretir."""
    payload = {
        k: v for k, v in shared.items() if k not in {"slides"}
    }
    payload.update(slide)
    payload["counter"] = f"{index + 1}/{total}"
    payload["role"] = slide.get("role", "step")
    payload["tail"] = build_tail(slide, index == total - 1)
    payload.setdefault("step", str(index))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", help="Carousel tanımı (JSON)")
    parser.add_argument("-o", "--output", help="Çıktı PNG kalıbı")
    parser.add_argument(
        "-t", "--template", default="slide.html", help="Slayt şablonu"
    )
    args = parser.parse_args()

    card_path = Path(args.card)
    shared = json.loads(card_path.read_text("utf-8"))
    slides = shared.get("slides") or []
    if not slides:
        raise SystemExit("JSON içinde `slides` listesi yok.")

    base = Path(args.output) if args.output else card_path.with_suffix(
        ".png"
    )
    base.parent.mkdir(parents=True, exist_ok=True)
    canvas = FORMATS["feed"]

    for index, slide in enumerate(slides):
        payload = slide_payload(shared, slide, index, len(slides))
        target = base.with_name(f"{base.stem}_{index + 1}{base.suffix}")
        shoot(build_html(payload, args.template, "feed"), target, canvas)
        logger.info("slayt %d/%d -> %s", index + 1, len(slides), target)


if __name__ == "__main__":
    main()
