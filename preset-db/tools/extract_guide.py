"""Extract the Spooky2 User's Guide text layer, one file per page range.

The guide is born-digital (Quartz/PDFContext), so the text layer is present and
complete. It is NOT the whole story: multi-column bodies interleave and images
carry no text at all, so this output is a companion for cross-checking while the
vision pass does the real reading.

Usage: python extract_guide.py [--dpi 150] [--range 1-244]
Writes into preset-db/docs/.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB_ROOT = os.path.dirname(HERE)
PROJECT = os.path.dirname(DB_ROOT)
PDF = os.path.join(PROJECT, "Spooky2_Users_Guide_20250124.pdf")
DOCS = os.path.join(DB_ROOT, "docs")
PAGES_DIR = os.path.join(DOCS, "pages")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--range", dest="rng", default="1-244")
    ap.add_argument("--text", action="store_true", help="only write the text layer")
    args = ap.parse_args()

    lo, hi = (int(x) for x in args.rng.split("-"))
    os.makedirs(DOCS, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    try:
        import pypdf
    except ImportError:
        raise SystemExit("pypdf is required: pip install pypdf")

    reader = pypdf.PdfReader(PDF)
    total = len(reader.pages)
    hi = min(hi, total)

    out = io.StringIO()
    out.write(f"# Spooky2 User's Guide - text layer ({lo}-{hi} of {total})\n\n")
    for i in range(lo - 1, hi):
        text = reader.pages[i].extract_text() or ""
        out.write(f"\n\n<!-- ===== page {i + 1} ===== -->\n\n{text}\n")
    text_path = os.path.join(DOCS, "guide_text.md")
    with open(text_path, "w", encoding="utf-8") as fh:
        fh.write(out.getvalue())
    print(f"text layer -> {text_path}  ({len(out.getvalue()):,} chars)")

    if args.text:
        return 0

    cmd = ["pdftoppm", "-f", str(lo), "-l", str(hi), "-r", str(args.dpi), "-png", PDF,
           os.path.join(PAGES_DIR, "pg")]
    subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    made = sorted(f for f in os.listdir(PAGES_DIR) if f.endswith(".png"))
    print(f"rendered {len(made)} page images at {args.dpi} dpi -> {PAGES_DIR}")
    if made:
        size = os.path.getsize(os.path.join(PAGES_DIR, made[0]))
        print(f"  ~{size / 1024:.0f} KB each, approx {(size * 0 + 2900):,} image tokens per page")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())