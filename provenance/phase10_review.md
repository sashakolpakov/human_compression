# Phase-ten review record

10 October 2026. This phase adds a common Suzuki rank/counting derivation,
a uniform partial hypertope result, an explicit finite unitary certificate
and the sixteenth Lean module. Earlier frozen proofs and reports retain
their bytes. [Original-file hashes](phase10_original_files.json) identify
the exported artifacts and the one relative-link portability edit.

## Suzuki rank and counting

Root read all twelve pages of the primary L074 author manuscript and wrote
the [marked-field derivation](../research/case_study/phase10_suzuki_marked_fields.md).
An independent agent reviewed the complete argument and the source match.
The review covered unique normalization, canonical subfield position,
generation, all rank-three intersections, the higher-rank obstruction,
proper almost-simple extensions, Frobenius/duality freeness and the exact
all-parameter equivalence with the source's nested counting formula. No
gap was found in that internal review.

Both principal L074 counting theorems are rederived. The L085 rank/existence
theorem is matched through its exact primary restatement in L074; the
original 2006 article body is unavailable, so the registry retains component
coverage for L085. The L074 manuscript date, 27 September 2011, differs from
the 2010 journal year and is recorded separately. Classical Suzuki subgroup,
centralizer, automorphism, ovoid and field structure remain explicit inputs.

Root's exact Python run and an independent fresh rerun agree except for
timestamp: 49 odd-degree formula comparisons and complete coordinate orbits
at q=8,32,512. Root and the independent reviewer also freshly ran the GAP
matrix checker: 42 normalized triples, 2,688 subgroup intersections and
42 diagonal-conjugation duality checks at q=8. Parsed reports agree.
The independent audit binds the final source and both execution records.
The written proofs supply the all-parameter claims; the computations are
finite diagnostics. The [intake](../research/case_study/phase10_suzuki_marked_intake.json)
records targets, source hashes, retained structure and reproduction commands.

## Uniform small-factor cyclic TPP

Root and another agent reviewed the full
[cyclic-subgroup proof](../research/case_study/phase10_cyclic_tpp.md).
Root also read the retained marked metacyclic restatement, multiplication
formulas and exact marked nonmetacyclic classification in the primary
isobicyclic source, including Theorem 4.1 and its proof on pages 15–16.
The argument constructs the involutory factor swap from an action on the
oriented edges of a complete bipartite graph; it does not infer the marking
from an abstract group classification alone.

The result proves cyclic TPP for every triple in a finite 2-group with a
factor of order at most four. Consequently the hypertope order bound holds
whenever a distinguished pair product has order at most eight. The
minimal-counterexample reductions preserve this subclass. The unrestricted
conjecture, including the next minimum-factor-eight boundary, remains open.
The marked isobicyclic classification is retained, not re-proved here.

Root freshly ran the frozen coordinate checker. Its
[separate report](../research/case_study/phase10_cyclic_tpp_root_check.json)
is byte-for-byte identical to the author report: 48 models, 48,336 relevant
elements, 386,688 swap equations and 1,966,080 associativity equations.
Only the n≤8 models exhaust every associativity triple; larger models use
generator-local equations. The computation is not a census of all 2-groups
through the largest model order. The older independent written-review
record correctly says that reviewer did not rerun the checker; root's
later execution is a separate record.

## PSU4(5) by explicit matrices

The original permutation certificate and its independent bitmask checker
are preserved. Root reviewed the stronger
[natural-matrix certificate](../research/case_study/phase10_unitary_matrix_certificate.md)
and its checker, then freshly ran it. An independent agent also reran it.
Four explicit matrices over GF(25) have determinant one and preserve the
specified Hermitian form. Their isotropic-plane image has order
14,742,000,000. Scalars act trivially, so unitary containment and the
standard projective-unitary order formula identify the image as PSU4(5).
This route requires neither ATLAS input nor simple-group recognition.

The type is {4,26,10}; all 16 generated subset groups and all 256 ordered
intersection equalities pass. Root's [execution record](../research/case_study/phase10_unitary_matrix_root_check.json)
binds the unchanged checker, matrix witness and fresh log. Combined with
the earlier reviewed upper bound, the finite existence certificate gives
maximum rank four at q=5. Uniform rank-four existence for other odd q≥5
and publication priority remain unverified here.

## Formal rank obstruction

Root reviewed the statement and proof of
[InvolutionCentralizers.lean](../research/case_study/formal/InvolutionCentralizers.lean).
In any center-free group, if the nonidentity involutions commuting with a
given nonidentity involution commute with one another, every generating
string of nonidentity involutions has length at most three. The proof uses
actual subgroup closure for generation. It requires neither finiteness,
generator distinctness nor the intersection property. The second theorem
expresses trivial center as `Subgroup.center G = ⊥`.

The agent freshly compiled the public source through the portable runner
using the pinned Lean/mathlib dependencies. Both theorems report only
`propext`, `Classical.choice` and `Quot.sound`, with no admitted lemmas.
The private successful report is preserved separately; all fifteen older
saved report hashes are unchanged. The sixteen saved reports match their
sources. Only this new module was freshly compiled in this phase.
Suzuki-specific structure and rank-three existence remain outside Lean.

## Measurement and coverage

The registry now has eight works whose identified principal results are
rederived. The new principal entry is L074. This counts precise theorem
coverage; it is neither eight whole-paper reductions nor a numerical ratio.
The existing conditional ratio 127/38≈3.34 for the two matched L066 formulas
is unchanged. No result receives the separate infinity marker.

The [tree measurement scope audit](../research/case_study/phase10_measurement_scope.md)
identifies exact 1998/2002 targets and shared dependencies. The complete
2002 source is available; missing 1998 proof spans prevent a cross-paper
numerator. The exported scope note changes only its relative link to the
root measurement policy. No unavailable source length is estimated and
no third-party full text is distributed.
