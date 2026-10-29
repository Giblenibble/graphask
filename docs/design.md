# GraphAsk Design Doc

Status: draft, Phase 0. Last updated: 30-10-2026
Numeric targets below are provisional and are subject to change after measurement of baseline.

## 1. Problem

GraphAsk helps ML students and researchers get cited answers about graph neural networks (GNN) literature, so they can quickly compare methods, find limitations, and locate the source paper.

Users: students and researchers who read GNN papers. Planned early users are a university ML or graph lab and online graph-ML communities.

## 2. Goals

- Return answers grounded in the corpus, with citations to the source paper and page.
- Measurably improve retrieval over a vector-only baseline (hybrid search, reranking, chunking experiments), with every change measured on a fixed benchmark.
- Say "the corpus does not contain this" when it does not, instead of inventing an answer.
- Track latency and cost per query.

## 3. Non-goals

- No non-English papers.
- No multi-turn conversation memory.
- No paper recommendation.
- No fine-tuning of models.

## 4. Data

**Source:** arXiv, via the official API ('scripts/fetch_arxiv.py'). The script always include a list of seed papers by arXiv ID, then fills the rest from a keyword search in 'cs.LG'.

**Seed papers (always included):**
| arXiv ID | Paper |
|---|---|
| 1609.02907 | GCN |
| 1706.02216 | GraphSAGE |
| 1710.10903 | GAT |
| 1810.00826 | GIN |
| 1704.01212 | MPNN |

**Size:** the feasibility test uses 20 papers. Target corpus is 300 to 600 papers, post 2016 and foundational papers.

**Known corpus issue:** the keyword search pulls in papers that mention "message passing"  without being GNN papers (for example, a neural PDE solver write-up).The full corpus needs a relevance filter, such as requiring GNN terms in the title or abstract.

**Licensing:** arXiv papers carry varying licenses, so the repository contains only the fetch script and metadata. PDFs stay in 'data/', which is gitignored.

**Update strategy:** re-run the fetch script. Existing PDFs are skipped.

## 5. Architecture (draft)

```
fetch -> extract -> clean/filter -> chunk -> embed -> store -> retrieve (hybrid + rerank) -> generate -> cite
```

Storage: Postgres with pgvector, so one database holds vectors, metadata and full-text search for BM25.

## 6. PDF Extraction (findings from the feasibility test)

Extraction uses PyMuPDF with 'get_text("blocks")', so each paragraph or heading arrives as its own unit. Plain 'get_text()' was not good enough: it emits one line per row with no paragraph boundaries, so headings merged into body text and sentence-ending lines were never rejoined.

Implemented in 'src/graphask/ingest/clean.py':

- Unicode normalization (ligatures such as "fi" become "f i").
- Rejoining hyphen-split words at a line break.
- Joining the lines within a block.
- Dropping running headers and footers (text repeated across many pages).
- Dropping footnotes and copyright lines (heuristic).
- Dropping tiny figure-label fragments, while keeping headings.
- Splitting an "Abstract" heading from its body.

Tested on the MPNN paper. Two column order came out correct with the default block order. Do not use 'sort=True', which interleaves columns.

**Known gaps (Phase 1):** 

- Paragraphs split across columns or pages are not merged. A paragraph can be interrupted by a figure caption or a dropped footnote, so the merge rule must skip non-body blocks.
- The references section is still included. It adds noise chunks (for example, a bibliography entry for GraphSAINT is retrievable).Cut it at the "References" heading.
- Math symbols are somtimes garbled by font encoding.
- Tables are flattened, so a table row can lose its column headers.
- The filters were tuned on one paper and need testing on others, including a survey and a single-column paper.

## 7. Evaluation plan

**Benchmark:** 100 to 200 questions and answer pairs. A 13-question seed set exists in 'benchmark/seed-questions.md', with answer locations (paer and PDF page, as printed by PyMuPDF).

**Question types:**

- Single-paper lookups.
- Multi-paper questions, where the answer is stated in the sources and not just implied by comparing them.
- Cross-corpus list questions, graded against a **required** set of papers plus an **acceptable but optional** set.
- Unanswered questions, split into:
    - clean (the term never appears in the corpus), and
    - hard negatives (the corpus has related content but never the asked-for combination).

**Rules learned while building the seed set:**

- A question counts as unanswerable only after verifying it with the corpus search tools in 'scripts/' ('grep_corpus.py', 'grep_one.py', 'zero_hits.py'), including abbreviations and hyphenated names.
- Ground truth must be something a passage actually states. A comparison that can only be inferred by reading two papers side by side is not a ground truth. It can go in a separate "synthesis" set graded by hand.
- When a fact appears in several places, record all of them as valid, or recall@k will penalize correct retrievals.
- Phrase questions the way a user would, not in the papers' jargon. Keyword search fails on vocabulary mismatch (for example, "neighbor weighting" has zero matches with GAT and GCN papers, but can be retrieved using "normalization" and "attention"). Add paraphrased variants so the benchmark tests that gap.

**Retrieval metrics:** recall@k, MRR, nDCG@k. List questions use paper-level recall against the required set.

**Generation metrics:** faithfulness, answer correctness and abstentation accuracy on unanswerable questions. Hard negatives specifically test whether the system answers from a near match.

**Judge validation:** hand-check about 30 judged examples to confirm the LLM judge agrees with a human. Use a different or stronger model than the generator as judge.

## 8. Key technical decision (defaults, revisable)

| Decision | Default | Reason |
|---|---|---|
| Vector store | Postgres with pgvector | One database for vectors, metadata and BM25 |
| Embedding model | 'bge-small-en-v1.5' | Free, local, strong baseline |
| LLM | One provider behind an interface | Swap models without rewriting code |
| Judge model | Different from the generator | Reduces self-preference bias |
| PDF parsing | PyMuPDF blocks | Paragraph-level units, correct column order in testing |

## 9. Success targets (provisional)

- Recall@5 of at least 80% on the full benchmark.
- Faithfulness of at least 90%.
- p95 latency under 4 seconds.
- Abstains correctly on at least 90% of unanswerable questions.

Revise after the vector-only baseline is measured.

## 10. Risks and mitigation

| Risk | Mitigation |
|---|---|
| PDF Extraction errors hurt chunk quality | Block-based extraction, filters and tests on a variety of papers |
| Benchmark errors (wrong ground truth) | Verify every answer location by hand, use search tools for unanswerable questions |
| LLM Judge Bias | Different judge model, hand check 30 samples |
| Prompt injection through paper text | Treat retrieved text as data, add a gurad in the generation prompt |
| API Cost | Spending limit on the provider dashboard, semantic caching, cost logging |
| Corpus drifts off topic | Relevance filter on title and abstract |

## 11. Milestones

| Phase | Scope | Target |
|---|---|---|
| 0 | Setup, scoping, feasibility test, design doc | in progress |
| 1 | Ingestion: full fetch, extraction, chunking, embeddings, pgvector | TBD |
| 2 | Baseline RAG with citations, FastAPI endpoint, minimal UI | TBD |
| 3 | Evaluation harness and full benchmark | TBD |
| 4 | Retrieval experiments with an ablation table | TBD |
| 5 | Caching, observability, reliability, tests | TBD |
| 6 | Docker, Ci with an eval subset, deployment | TBD |
| 7 | Real users, write-up | TBD |

## 12. Open questions

- Exact relevance filter for the full corpus.
- Whether paragraph merging across pages should run before or after chunking.
- Whether to tag figure captions as a separate block type.
- Final size of the corpus (300 or 600).