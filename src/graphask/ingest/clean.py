import re
import unicodedata
from collections import Counter


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")  # normalize line endings
    text = unicodedata.normalize("NFKC", text)  # ligatures become plain letters
    text = re.sub(r"-\n(?=[a-z])", "", text)  # rejoin hyphenated words
    text = re.sub(r"\n+", " ", text)  # join broken lines
    return re.sub(r"[ \t]+", " ", text).strip()


def extract_blocks(page) -> list[str]:
    blocks = page.get_text("blocks")  # x0, x1, y0, y1, text, block no, block type
    return [clean_text(b[4]) for b in blocks if b[6] == 0 and b[4].strip()]


HEADING_RE = re.compile(r"^(\d+(\.\d+)*\.?|[A-Z]\.)\s+\S")
KNOWN_HEADINGS = {"abstract", "references", "acknowledgements", "conclusion", "conclusions"}
FOOTNOTE_RE = re.compile(r"^\d[A-Z][a-z]")


def is_heading(text: str) -> bool:
    return bool(HEADING_RE.match(text)) or text.lower() in KNOWN_HEADINGS


def filter_pages(pages: list[list[str]], min_len: int = 40) -> list[list[str]]:
    counts = Counter(b for blocks in pages for b in set(blocks))
    repeat_cut = max(2, len(pages) // 2)
    out = []
    for blocks in pages:
        kept = []
        for b in blocks:
            if counts[b] >= repeat_cut:
                continue
            if FOOTNOTE_RE.match(b) or b.startswith("Proceedings of"):
                continue
            if len(b) < min_len and not is_heading(b):
                continue
            m = re.match(r"^(Abstract)\s+(\S.{60,})$", b, re.S)
            if m:
                kept += [m.group(1), m.group(2)]
                continue
            kept.append(b)
        out.append(kept)
    return out


def extract_pdf(path) -> list[list[str]]:
    import pymupdf

    with pymupdf.open(path) as doc:
        pages = [extract_blocks(page) for page in doc]
    return filter_pages(pages)
