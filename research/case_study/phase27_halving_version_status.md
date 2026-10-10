# Halving paper: bounded version and correction audit

Checked 10 October 2026. This is a source-status supplement, not a novelty assessment or a full-paper review. Frozen phase26 files are unchanged.

**The current public arXiv text is exactly the v1 already studied. The journal theorem has not been checked from its full body.** The live [arXiv record](https://arxiv.org/abs/2405.19050) lists only v1, dated 29 May 2024. A fresh download through the unversioned PDF address is byte-identical to the cached v1: SHA256 `c904311dec0e33fb27242a0553cca245d4e1fea1411e2e3519159f6cac0b8516`.

The [publisher record](https://link.springer.com/article/10.1007/s00493-024-00134-y) identifies *Combinatorica* 45, article 10 (2025), with revision on 24 November 2024 and version of record on 16 January 2025. Its body is subscription content; the PDF endpoint redirects to the preview. The [ULB deposit](https://difusion.ulb.ac.be/vufind/Record/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/398629/Holdings) labels its available file `2405.19050v1-3.pdf` as a preprint. The [MPI bibliography](https://www.mis.mpg.de/stochastic-topology-applications/publications) links the DOI and arXiv. Neither supplied an independently accessible journal body in this audit.

Exact-title, DOI, and author-plus-halving correction searches located no relevant correction or erratum. The publisher landing page and [author bibliography](https://capiedade.github.io/Publications.html) showed none. This bounded negative result does not establish that no correction exists or that the observation is new. Unrelated corrections by either author were excluded.

## Exact v1 scope

The following comparison uses the byte-bound v1, not inferred journal numbering:

| Target | Printed v1 location | Assumptions relevant here |
|---|---|---|
| Construction 3.6 | p.8 | Residually connected geometry; B1 and B2; nonbipartite vertex-edge graph. Higher elements are copied once per even-walk class of their individual graph shadow. |
| Lemma 3.11 | p.9 | Claims the residue at a higher-type flag is a partitioned neighbourhood graph using the intersection of the chosen individual classes. |
| Proposition 3.13 | p.10 | Claims residual connectedness is preserved in the preceding construction. No thinness or flag-transitivity assumption is added. |
| Theorem 3.18 | pp.11–12 | Collects the construction under the same geometric assumptions; residual connectedness is an unconditional conclusion, whereas the automorphism conclusion is conditional. |

The firm example in [phase27_parity_shadow_check.py](phase27_parity_shadow_check.py) uses the graph $K_{2,2,2,2}$ and two higher types, each indexed by the three-part subsets. Incidence below a higher object is containment in its three-part shadow; every pair of different higher types is incident. Its individual higher shadows contain triangles. Two distinct such objects have a common shadow $K_{2,2}$. Construction 3.6 therefore leaves both objects unsplit, while their transformed residue is the disconnected bipartite double cover of $K_{2,2}$, with two components of four vertices each.

The geometric checks and source comparison concern the literal current v1 claim, specifically the residual-connectedness conclusion. Firmness does not remove this example: its original panels have sizes two or four. It is not a thin regular hypertope, so it does not by itself refute the more specialized Theorem 4.4. This supplement does not assert that the counterexample persists in the inaccessible journal body. The separate mathematical audit and any proposed repair must retain that boundary.

## Evidence and limits

The [JSON record](phase27_halving_version_status.json) binds the saved current primary pages, the fresh PDF, the exact queries, and the scope of reading. Source files remain private. The counterexample checker is owned and reviewed separately; its evolving bytes are not silently frozen by this status note. No message was sent to the authors, no institutional login was attempted, and no whole-paper coverage is assigned.
