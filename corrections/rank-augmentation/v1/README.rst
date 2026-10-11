A counterexample to the six-point case of rank augmentation
=========================================================

The `three-page proof <case_three.pdf>`_ gives an explicit rank-three string
C-marking of S18 whose prescribed rank augmentation fails the intersection
property. It disproves Theorem 4.1(3) in De Saedeleer, Leemans and Mulpas,
*A rank augmentation theorem for rank 3 string C-group representations of
the symmetric groups*, arXiv:2212.12563v1, 23 December 2022. The bound source
edition has nineteen pages; its theorem appears on physical pages 5–6.

The proof supplies all input hypotheses. Seventeen explicit conjugate
transpositions generate S18, and a dihedral intersection argument proves
the original C-property. The split transposition is an explicit word in
the other three output generators, contradicting the intersection property
for disjoint label sets. A separate GAP implementation verifies both group
orders, all 64 original intersection identities and the exact failed output
intersection. The new first end has order 48, its required middle has order
6, and its actual intersection with the other end has order 48.

The `Lean file <formal/RankAugmentationObstruction.lean>`_ proves thirteen
statements about the actual eighteen-point output permutations, culminating
in failure of the full intersection property for their generated subgroups.
Fresh compilation uses standard axioms only. The input C-property, S18
generation and source-hypothesis interpretation remain written proofs.
Both the author and the distinct reviewer read and compiled the formal
source; four damaged variants fail fresh typechecking.

Read the `TeX source <case_three.tex>`_, `independent findings
<independent_review/review.json>`_ and `current acceptance <admission.json>`_.
The frozen packets retain their submission-stage labels. The public paper
removes the private-review title date and updates the final review-status
paragraph; all mathematical statements and proofs are unchanged.

From the repository root, run the distinct GAP and Lean replay::

  python3 -B -O corrections/rank-augmentation/v1/independent_review/check.py \
    --written corrections/rank-augmentation/v1/written \
    --formal corrections/rank-augmentation/v1/formal --out /fresh/output

Use ``--gap``, ``--lean`` and ``--packages`` to select GAP 4.15.1,
Lean 4.32.2 and the pinned package checkouts. Compiled library dependencies
are trusted. No primary PDF is needed for this replay; its hash and exact
edition remain recorded for source comparison. The author written replay
additionally needs the private source through ``--study-root``.

This is a correction to one published theorem case. Cases (1) and (2),
the small-degree census and complete recovery of L020 remain separate.
It makes no claim about the different high-rank stability theorem, no
historical-priority claim, no open-conjecture credit and no compression
factor. L020 remains among the accessible originals awaiting full recovery.
