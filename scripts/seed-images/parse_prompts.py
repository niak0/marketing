"""docs/seed/01-IMAGE-PROMPTS.md dosyasindan 98 prompt'u parse edip prompts.json uretir."""
import json
import re
from pathlib import Path

SRC = Path(
    "/Volumes/Okantosh/projects/ideavoll/lovable/docs/seed/01-IMAGE-PROMPTS.md"
)
OUT = Path(__file__).parent / "prompts.json"

STYLE_TAIL = (
    "shot on iPhone 15 Pro, natural available light, candid amateur "
    "photography, authentic imperfect composition, subtle sensor grain, "
    "true-to-life colors, no text, no lettering, no signage, no logos, "
    "no watermark"
)

CATEGORY_CONFIG = {
    "av": {
        "folder": "avatars",
        "aspect_ratio": "1:1",
        "model": "text2image_soul_v2",
        "size": (1024, 1024),
    },
    "ev": {
        "folder": "events",
        "aspect_ratio": "16:9",
        "model": "soul_location",
        "size": (1920, 1080),
    },
    "po": {
        "folder": "posts",
        "aspect_ratio": "1:1",
        "model": "soul_location",
        "size": (1440, 1440),
    },
    "st": {
        "folder": "stories",
        "aspect_ratio": "9:16",
        "model": "soul_location",
        "size": (1080, 1920),
    },
}

FILENAME_RE = re.compile(r"\*\*`([a-z0-9]+-\d+-[a-z-]+\.jpg)`\*\*")
CODEBLOCK_RE = re.compile(r"```\n(.*?)\n```", re.DOTALL)


def main():
    text = SRC.read_text()
    entries = []
    pos = 0
    for m in FILENAME_RE.finditer(text):
        filename = m.group(1)
        prefix = filename.split("-")[0]
        if prefix not in CATEGORY_CONFIG:
            continue
        block_match = CODEBLOCK_RE.search(text, m.end())
        if not block_match:
            raise ValueError(f"{filename} icin prompt bulunamadi")
        prompt = block_match.group(1).strip()
        cfg = CATEGORY_CONFIG[prefix]
        entries.append(
            {
                "id": filename.replace(".jpg", ""),
                "filename": filename,
                "folder": cfg["folder"],
                "model": cfg["model"],
                "aspect_ratio": cfg["aspect_ratio"],
                "width": cfg["size"][0],
                "height": cfg["size"][1],
                "prompt": f"{prompt}, {STYLE_TAIL}",
            }
        )

    by_folder = {}
    for e in entries:
        by_folder.setdefault(e["folder"], 0)
        by_folder[e["folder"]] += 1

    print(f"Toplam {len(entries)} prompt parse edildi:")
    for folder, count in by_folder.items():
        print(f"  {folder}: {count}")

    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=2))
    print(f"Yazildi: {OUT}")


if __name__ == "__main__":
    main()
