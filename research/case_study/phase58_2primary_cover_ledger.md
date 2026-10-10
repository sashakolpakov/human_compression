# Phase58 source, proof, and diagnostic ledger

Status at freeze: author proof and exact finite certificates; independent review is pending. No public edit or Lean component is part of this package.

| Item | Scope | Basis |
|---|---|---|
| Input P | β≥5, ε1,ε2=±1, Table 2 Γ2, type {8,2^β,8} | Cunningham–Pellicer Theorem 4.8; tightness, exact presentation/order/IP retained |
| Smallest regular R | all those parameters; order 128q and nonpoly | Manuscript §2, full written coordinate/fiber proof |
| Raw facet/cofacet covers | all parameters; cyclic-four kernels, each locally noninjective at one end | §§3–4, exact normal closure and common quotient |
| Same reduced S | all parameters; order 256q; globally minimal cover over P | §4 independent-central-relator presentation, with §3 prime-degree argument |
| Shared interval | all parameters; H order 1024q, kernel C4×C2, unique maximal admissible C2² | §5 full invariant-subgroup and IP proof |
| Eight checks | β=5,6, all four signs | Standalone check.g; finite cross-check only |
| Complete double/quartic census | only β=5, ε1=ε2=+1, full R of order 8192 | §6 exact universal module-extension bounds plus standalone extension_check.g |
| Geometric transport | marked regular rotation/string-C recognition; smallest regular maniplex property | Retained standard background, not imported target multiplicity |
| Attribution | mix with facet/cofacet trivial extensions | Cunningham's earlier finite example; phase49 odd-prime work is contextual, no target-proof import |

The primary author PDF is https://arxiv.org/pdf/2009.04566 (v1, 9 September 2020; internal header 11 September 2020). Published bibliographic identification is *Journal of Algebraic Combinatorics* 54 (2021), 837–878, DOI 10.1007/s10801-021-01023-z. The actual inspected mathematical version is the author PDF, not an asserted byte-identical publisher PDF. The Table 2 Γ2 row and Theorem 4.8 were reopened on 10 October 2026; previously bound web extractions contain those same primary statements. The exact source dependencies also include Table 1 local constructions, Lemma 4.6, and Corollary 4.5 through retained Theorem 4.8. This package does not reprove their classification content.

The all-parameter obstruction is a positive theorem about these constructed covers, not evidence that the general question has a negative answer. In the finite sample all 29 quartic covers tested exhaustively have the good double quotient; higher degree or odd-order extensions are outside the search. Covers are marked and rank preserving. No equivalence under arbitrary rank permutations is claimed. Historical novelty has not been established by this package.
