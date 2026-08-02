#!/usr/bin/env python3
"""
98 seed gorselini (avatar/event/post/story) Higgsfield uzerinden uretir.

Veri kaynagi: prompts.json (parse_prompts.py ile docs/seed/01-IMAGE-PROMPTS.md
dosyasindan cikarildi). Model secimi:
  - avatarlar     -> text2image_soul_v2 (Higgsfield Soul 2.0), 0.12 kredi
  - event/post/st -> soul_location,                            0.12 kredi
Toplam ~98 x 0.12 = ~11.8 kredi (tekrar denemeler dahil onemsiz bir maliyet).

Kullanim:
  python3 generate_seed_images.py --party A --dry-run
  python3 generate_seed_images.py --party A
  python3 generate_seed_images.py --party B
  python3 generate_seed_images.py --party C
  python3 generate_seed_images.py --party all --force

Idempotent: hedef dosya zaten varsa atlanir (--force ile yeniden uretilir).
Ilerleme state.json'a yazilir; sureç kesilirse ayni komutla devam eder.
"""
import argparse
import json
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
PROMPTS_FILE = ROOT / "prompts.json"
STATE_FILE = ROOT / "state.json"
OUTPUT_ROOT = ROOT.parent.parent / "seed-images"

PARTY_FOLDERS = {
    "A": {"avatars", "events"},
    "B": {"posts"},
    "C": {"stories"},
    "all": {"avatars", "events", "posts", "stories"},
}

WORKERS = 6
WAIT_TIMEOUT = "5m"


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def submit_job(entry):
    cmd = [
        "higgsfield", "generate", "create", entry["model"],
        "--prompt", entry["prompt"],
        "--aspect_ratio", entry["aspect_ratio"],
        "--json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"submit failed: {result.stderr.strip()}")
    job_ids = json.loads(result.stdout)
    return job_ids[0]


def wait_job(job_id):
    cmd = [
        "higgsfield", "generate", "wait", job_id,
        "--timeout", WAIT_TIMEOUT, "--quiet", "--json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
    if result.returncode != 0:
        raise RuntimeError(f"wait failed: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    job = data[0] if isinstance(data, list) else data
    if job.get("status") != "completed":
        raise RuntimeError(f"job status={job.get('status')}")
    return job["result_url"]


def download_and_resize(url, out_path, width, height):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(".tmp.png")
    urllib.request.urlretrieve(url, tmp_path)
    img = Image.open(tmp_path).convert("RGB")

    src_w, src_h = img.size
    target_ratio = width / height
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    img = img.resize((width, height), Image.LANCZOS)
    img.save(out_path, "JPEG", quality=85)
    tmp_path.unlink(missing_ok=True)


def process_entry(entry, state, dry_run):
    entry_id = entry["id"]
    out_path = OUTPUT_ROOT / entry["folder"] / entry["filename"]

    if out_path.exists():
        return entry_id, "skipped (var)"

    if dry_run:
        return entry_id, (
            f"[dry-run] {entry['model']} {entry['aspect_ratio']} -> {out_path}"
        )

    try:
        record = state.get(entry_id, {})
        job_id = record.get("job_id")
        if not job_id:
            job_id = submit_job(entry)
            state[entry_id] = {"job_id": job_id, "status": "submitted"}
            save_state(state)

        result_url = wait_job(job_id)
        download_and_resize(result_url, out_path, entry["width"], entry["height"])

        state[entry_id] = {"job_id": job_id, "status": "done"}
        save_state(state)
        return entry_id, f"OK -> {out_path.relative_to(OUTPUT_ROOT.parent)}"
    except Exception as exc:
        state.setdefault(entry_id, {})["status"] = "failed"
        state[entry_id]["error"] = str(exc)
        save_state(state)
        return entry_id, f"HATA: {exc}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--party", choices=["A", "B", "C", "all"], default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    entries = json.loads(PROMPTS_FILE.read_text())
    folders = PARTY_FOLDERS[args.party]
    entries = [e for e in entries if e["folder"] in folders]
    if args.limit:
        entries = entries[: args.limit]

    if args.force:
        for e in entries:
            out_path = OUTPUT_ROOT / e["folder"] / e["filename"]
            out_path.unlink(missing_ok=True)

    state = load_state()

    print(f"Parti {args.party}: {len(entries)} gorsel islenecek "
          f"({'dry-run' if args.dry_run else 'CANLI'})")

    done = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(process_entry, e, state, args.dry_run): e
            for e in entries
        }
        for future in as_completed(futures):
            entry_id, msg = future.result()
            print(f"  {entry_id}: {msg}")
            if msg.startswith("HATA"):
                failed += 1
            else:
                done += 1

    print(f"\nBitti. {done} basarili/atlandi, {failed} hata.")
    if failed:
        print("Hatali olanlari tekrar denemek icin ayni komutu calistir "
              "(sadece basarisizlar yeniden gonderilir).")
        sys.exit(1)


if __name__ == "__main__":
    main()
