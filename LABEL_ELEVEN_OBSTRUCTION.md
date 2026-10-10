# The equal-label conjecture fails at eleven

**There is no regular d-polytope of exact type {11,...,11} satisfying
the additional relations in Li–Zhang's Conjecture 3.7 when d≥5.**
This is a negative answer to the full existence assertion in
[arXiv:2505.09505v1](https://arxiv.org/html/2505.09505v1), not just a
failure of one proposed construction.

The [complete manuscript](research/case_study/phase212_n11_obstruction.md)
and [universal-group proof](research/case_study/phase214_universal_bounds.md)
give the argument in detail. The
[edition and literature audit](research/case_study/phase220_F014_edition_review.md)
confirms that arXiv still lists only v1. The journal introduction was
revised, but its complete conjecture section has not been obtained.
The journal formulation and historical priority remain unverified.

## The proof

At rank five and label eleven, the literal universal presentation is

\[
U_5\cong C_2\times\operatorname{Sp}_4(32),
\qquad |U_5|=2,249,598,645,043,200.
\]

An explicit reflection belongs to both end parabolics, with the same
binary sign, but its projection is outside the middle parabolic.
Simplicity of Sp₄(32) implies that every quotient retaining adjacent
order eleven preserves this obstruction. Thus no such quotient is a
string C-group. Every higher-rank example would contain the forbidden
rank-five parabolic.

| Step | Certificate and scope |
|---|---|
| **[I] [V]** Universal upper bound | Three finite coset certificates, verified by a separate C++ program using only spanning-tree definitions and deductions from literal relators. A valid one-point permutation action is rejected as insufficient to prove an upper bound. |
| **[I] [V]** Matching group and signed witness | Exact matrices over F₃₂, faithful projective actions, GAP group orders and simplicity, and two signed subgroup-membership checks. Independent Python arithmetic verifies the relators and the small quotient excluding middle membership. |
| **[I] [L]** Every possible quotient is excluded | Nine Lean declarations prove the general simple-factor and intersection arguments. The concrete large groups and the full geometric theorem are not formalized. |
| **[B]** Retained mathematics | The characteristic-two quadratic symmetry construction, the earlier local translation identity, and the standard string C-group correspondence. The manuscript identifies their roles. |

The [independent review](research/case_study/phase215_review.md) checks
the source statement, full written argument, literal presentations,
deduction checker, matrix interfaces and Lean hypotheses. The
[publication record](provenance/phase115_review.md) binds that review
and fresh runs from the public files.

The [earlier positive label families](EQUAL_LABEL_POLYTOPES.md) remain
valid. F014 now has a complete negative answer for the bound source
version; it is one question in the ledger, not an additional question
for every excluded rank. No historical-priority marker or compression
factor is assigned.

## Reproduction

Both output directories must be new. The upper certificate requires
Python and a C++17 compiler; it does not require GAP or the original
coset enumerator.

```sh
python3 -B -O research/case_study/phase214_check.py --out /tmp/NEW-upper
python3 -B -O research/case_study/phase212_check.py --out /tmp/NEW-matrices --gap GAP --lean LEAN --packages PACKAGES
```

The second command requires GAP 4.15.1, Lean 4.32.2 and the pinned
mathlib packages. It checks the signed witness, compiles the nine
general declarations, and rejects five altered mathematical claims.
The finite-group backend, compiler and cached dependency objects remain
part of the stated trust boundary.
