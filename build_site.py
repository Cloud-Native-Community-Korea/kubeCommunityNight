#!/usr/bin/env python3
"""
Build the static web site (docs/) for the CNCK Kube Community Night decks.

For each event listed in events.config.json it converts the .pptx to per-slide
PNG images and writes the manifests the web viewer reads. Run locally or in CI.

Requirements: libreoffice (soffice) + poppler-utils (pdftoppm) + a Korean font.

    python3 build_site.py
"""
import glob
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
DPI = "144"  # ~1920px wide slides


def run(cmd):
    print("  $", " ".join(cmd))
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def render_event(ev):
    eid = str(ev["id"])
    pptx = os.path.join(ROOT, ev["pptx"])
    if not os.path.exists(pptx):
        print(f"  !! pptx not found: {pptx} — skipping event {eid}")
        return None

    outdir = os.path.join(DOCS, "events", eid)
    slides_dir = os.path.join(outdir, "slides")
    os.makedirs(slides_dir, exist_ok=True)
    for f in glob.glob(os.path.join(slides_dir, "*.png")):
        os.remove(f)

    # pptx -> pdf
    run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", outdir, pptx])
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")

    # pdf -> png (one per page)
    run(["pdftoppm", "-png", "-r", DPI, pdf, os.path.join(slides_dir, "slide")])
    os.remove(pdf)

    pages = sorted(glob.glob(os.path.join(slides_dir, "slide-*.png")))
    for i, p in enumerate(pages, 1):
        os.rename(p, os.path.join(slides_dir, f"{i:02d}.png"))

    # copy the pptx for download
    shutil.copy(pptx, os.path.join(outdir, os.path.basename(pptx)))

    meta = {
        "id": eid,
        "no": ev["no"],
        "title": ev["title"],
        "subtitle": ev.get("subtitle", ""),
        "date": ev["date"],
        "slideCount": len(pages),
        "pptx": os.path.basename(pptx),
    }
    with open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    print(f"  -> event {eid}: {len(pages)} slides")
    return meta


def main():
    with open(os.path.join(ROOT, "events.config.json"), encoding="utf-8") as fh:
        config = json.load(fh)

    manifest = []
    for ev in config:
        meta = render_event(ev)
        if meta:
            manifest.append(meta)

    manifest.sort(key=lambda m: m["no"], reverse=True)
    with open(os.path.join(DOCS, "events.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)

    if not manifest:
        print("No events built.", file=sys.stderr)
        sys.exit(1)
    print(f"Done. {len(manifest)} event(s) -> {DOCS}")


if __name__ == "__main__":
    main()
