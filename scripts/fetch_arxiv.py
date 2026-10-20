import json
import time
import urllib.request
from pathlib import Path

import arxiv


def fetch_file(url: str, dest: Path, attempts: int = 4) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "graphask-research-project"})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.write_bytes(resp.read())
                return
        except Exception as e:
            if attempt == attempts:
                raise
            wait = 10 * attempt
            print(f"    retry {attempt}/{attempts - 1} after error: {e} (waiting {wait}s)")
            time.sleep(wait)


OUT = Path("data/raw/arxiv")
OUT.mkdir(parents=True, exist_ok=True)

SEED_IDS = [
    "1609.02907",  # GCN
    "1706.02216",  # GraphSAGE
    "1710.10903",  # GAT
    "1810.00826",  # GIN
    "1704.01212",  # MPNN
]
QUERY = (
    '(abs:"graph neural network" OR abs:"graph convolutional" '
    'OR abs:"message passing") AND cat:cs.LG'
)
MAX_RESULTS = 20  # Raised to > 300 for feasibility

client = arxiv.Client(page_size=50, delay_seconds=3, num_retries=3)

results = list(client.results(arxiv.Search(id_list=SEED_IDS)))
seen = {r.get_short_id().split("v")[0] for r in results}
for r in client.results(arxiv.Search(query=QUERY, max_results=MAX_RESULTS)):
    if len(results) >= MAX_RESULTS:
        break
    base_id = r.get_short_id().split("v")[0]
    if base_id not in seen:
        results.append(r)
        seen.add(base_id)

metadata = []
for r in results:
    pid = r.get_short_id().replace("/", "_")
    pdf_path = OUT / f"{pid}.pdf"
    if not pdf_path.exists():
        try:
            fetch_file(r.pdf_url, pdf_path)
            time.sleep(3)
        except Exception as e:
            print(f"Failed {pid}: {e}")
            continue
    metadata.append(
        {
            "id": pid,
            "title": r.title,
            "author": [a.name for a in r.authors],
            "published": r.published.isoformat(),
            "abstract": r.summary,
            "pdf": str(pdf_path),
        }
    )

Path("data/raw/arxiv_metadata.json").write_text(json.dumps(metadata, indent=2))
print(f"Saved {len(metadata)} papers")
