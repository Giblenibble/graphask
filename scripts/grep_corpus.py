import sys
from pathlib import Path

import pymupdf

term = sys.argv[1].lower()
for pdf in sorted(Path("data/raw/arxiv").glob("*.pdf")):
    with pymupdf.open(pdf) as doc:
        pages = [" ".join(p.get_text().replace("-\n", "").split()) for p in doc]
    for n, text in enumerate(pages, start=1):
        low = text.lower()
        start = 0
        while (i := low.find(term, start)) != -1:
            print(f"{pdf.name} [page {n}]: ...{text[max(0, i - 150) : i + 250]} ...\n")
            start = i + len(term)
