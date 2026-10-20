import sys
from pathlib import Path

import pymupdf

from graphask.ingest.clean import extract_pdf

pdf = Path(sys.argv[1])
doc = pymupdf.open(pdf)
print(f"Pages: {len(doc)}")
for i in range(min(2, len(doc))):
    print(f"\n  page {i + 1}")
    print(doc[i].get_text()[:1500])

sys.path.insert(0, "src")

pages = extract_pdf(sys.argv[1])
print(f"Pages: {len(pages)}")
for i in (0, 1):
    print(f"\n  page {i + 1}: {len(pages[i])} blocks")
    for n, block in enumerate(pages[i][:12]):
        print(f"[{n}] {block[:150]!r}")
