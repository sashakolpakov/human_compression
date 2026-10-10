# Phase 214: admitted component and external dependencies

The self-contained result of this package is Theorem 1 of
`phase214_universal_bounds.md`: the literal F014 presentation at label 11
has universal group orders at most 22,528, 2,147,481,600, and
2,249,598,645,043,200 at ranks 3, 4, and 5, respectively. The upper bounds use
the rank-two dihedral bound 22 and three independently replayable coset
deduction certificates. They do not borrow Li–Zhang's rank-three order
proof.

The manuscript's Proposition 3 is an explicitly conditional application.
It requires the separate phase212 matrix marking, its full simple image,
and the signed endpoint-intersection witness. Once those inputs are
accepted, the combined result identifies the rank-five universal group as
C2×Sp4(32) and excludes every quotient with exact adjacent order 11.
Consequently no rank d ≥ 5 regular polytope with label 11 can satisfy the
printed triple relations. The source target is Conjecture 3.7 in
arXiv:2505.09505v1; neither current openness nor publication priority nor
unchanged survival in the 2026 journal edition is asserted.

The checker is a computational certificate verifier, not a Lean theorem.
Its invariant is proved in Lemma 2. It accepts a proposed edge only as a
fresh spanning-tree definition, an original facet loop, or a forced
one-hole consequence of an exact displayed relator. ACE supplies the
candidate tables but is outside the verification trust boundary. The
standard library, compiler, runtime, hardware, and the stated written
invariant remain retained computational assumptions.

The general deduction principle and the usual dihedral presentation are
classical. The present work supplies the particular universal bounds,
the concrete certifying replay, and the application that closes the
alternative-quotient loophole. No source-level result is assigned new
authorship merely because it has been rechecked.

The portable command is:

```sh
python3 -B -O phase214_check.py --out /tmp/phase214-fresh-replay
```

It needs Python 3 and a C++17 compiler, requires a fresh output path, and
performs all three upper-bound checks and two negative controls. The
compressed table artifacts are part of the proof package; their byte
cost is recorded in `phase214_tables.json`, separately from the prose
and checker. No whole-source compression ratio or additional principal
source credit is claimed by this component. The joint conjecture result
is one question resolution, not several credits for its individual
ranks, certificates, and formal lemmas.

The earlier `phase214_tl_probe.py` and the short universal discovery probe
scripts are exploratory work, excluded from the freeze. In particular,
successful Temperley–Lieb relator tests were not mistaken for an
intersection-property proof. Only the listed certificate package is
offered for admission.
