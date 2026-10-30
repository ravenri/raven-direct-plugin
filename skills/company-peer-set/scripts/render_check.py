#!/usr/bin/env python3
"""Converts the finished Word document to PDF and a contact sheet of page images for a visual check.

Usage: python render_check.py Peer_Set.docx
Prints the page count and writes <name>_sheet.png beside the document. View the sheet to confirm the
tables fit, nothing splits badly, and the page count is sensible.
"""
import glob
import os
import subprocess
import sys
import tempfile
from PIL import Image

src = os.path.abspath(sys.argv[1])
base = os.path.splitext(src)[0]
tmp = tempfile.mkdtemp()
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src], capture_output=True)
pdf = os.path.join(tmp, os.path.basename(base) + ".pdf")
subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, os.path.join(tmp, "pg")], check=True)
pages = sorted(glob.glob(os.path.join(tmp, "pg-*.png")))
ims = [Image.open(p) for p in pages]
w, h = ims[0].size
rows = (len(ims) + 1) // 2
sheet = Image.new("RGB", (w * 2, h * rows), "white")
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 2) * w, (i // 2) * h))
out = base + "_sheet.png"
sheet.save(out)
print(f"{len(ims)} pages. Contact sheet: {out}")
