# Seed questions (GraphAsk)

Types: single, multi, cross-corpus, unanswerable. Answer locations use PDF page numbers (1-based, as printed by pymupdf), not the numbers printed on the paper.

## Q1 (single)
**Question:** What layer-wise propagation rule does the GCN paper derive, and what is it an approximation of?
**Answer location:** 1609.02907, Introduction (also Section 2)

## Q2 (single)
**Question:** How does GAT compute how much a node attends to each neighbor, and what does multi-head attention add?
**Answer location:** 1710.10903, Section 2.1

## Q3 (single)
**Question:** Which aggregator functions does GraphSAGE propose?
**Answer location:** 1706.02216, Section 3.3

## Q4 (single or multi, see note)
**Question:** Why can GIN distinguish graph structures that GCN and GraphSAGE cannot?
**Answer location:** 1810.00826, Section 5.2
**Note:** the answer is located inside the GIN paper alone, so labelled as single unless supporting passages are found in other papers. TODO.

## Q5 (single)
**Question:** Compared to GCN-style models, how does GraphSAGE handle nodes that weren't seen during training?
**Answer location:** 1706.02216, page 2 (transductive vs inductive contrast)

## Q6 (multi)
**Question:** How do the MPNN and GIN papers each formalize a single GNN layer?
**Answer location:** 1704.01212, Section 2; 1810.00826, Section TODO

## Q7 (cross-corpus)
**Question:** Which papers study theoretical properties of GNNs (expressiveness, generality and convergence), and what does each analyze?
**Answer location:** 1704.01212, Section 2; 1810.00826, section TODO

## Q8 (cross-corpus)
**Question:** Which papers use GNNs to solve a specific real-world problem, and what is the problem in each?
**Required:** 2405.06553 (property valuation), 2310.19763 (neural PDE solvers), 2511.15246 (wireless power allocation, quantum GNN), 2207.06221 (recommender systems)
**Acceptable:** 1704.01212 (framework, applied to quantum chemistry)

## Q9 (unanswerable, hard-negative)
**Question:** What test accuracy does GraphGPS report on ogbn-arxiv?
**Answer location:** none
**Near misses:** 2410.05499 p.8 (GPS on other benchmarks), 2505.11346 p.7 (ZINC12K)
**TODO:** confirm the GraphGPS excerpt on 2411.00835 p.5 has no ogbn result.

## Q10 (unanswerable)
**Question:** What training speedup does GraphSAINT report over GraphSAGE?
**Answer location:** none
**Near miss:** 2411.00835 p.12(bibliography entry only)

## Q11 (unanswerable, clean)
**Question:** What accuracy does NAGphormer report on the Cora dataset?
**Answer location:** none (zero mentions in the corpus)

## Q12 (single)
**Question:** By how much does GAT improve over the author's best GraphSAGE result on the PPI dataset?
**Answer location:** 1710.10903, page 8 (20.5% over GraphSAGE, 3.9% over Const-GAT)

## Q13 (single)
**Question:** On which molecular dataset does the MIMO graph convolutions paper evaluate GraphGPS?
**Answer location:** 2505.11346, page 7 (ZINC12K)