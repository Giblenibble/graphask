import sys
from pathlib import Path

import pymupdf

pdf = next(Path("data/raw/arxiv").glob(f"{sys.argv[1]}*.pdf"))
terms = [t.lower() for t in sys.argv[2:]]
with pymupdf.open(pdf) as doc:
    for n, page in enumerate(doc, start=1):
        text = " ".join(page.get_text().replace("-\n", "").split())
        low = text.lower()
        for term in terms:
            start = 0
            while (i := low.find(term, start)) != -1:
                print(f"[page {n}] term: ... {text[max(0, i - 200): i + 300]}...\n")
                start = i + len(term)
