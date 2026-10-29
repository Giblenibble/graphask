import sys
from pathlib import Path

import pymupdf

terms = [t.lower() for t in sys.argv[1:]]
counts = dict.fromkeys(terms, 0)
for pdf in sorted(Path("data/raw/arxiv").glob("*.pdf")):
    with pymupdf.open(pdf) as doc:
        raw = " ".join(page.get_text() for page in doc)
    text = " ".join(raw.replace("-\n", "").split()).lower()
    for t in terms:
        counts[t] += text.count(t)

for t, c in counts.items():
    print(f"{c:4d}  {t}    {'<- usable' if c == 0 else ''}")
