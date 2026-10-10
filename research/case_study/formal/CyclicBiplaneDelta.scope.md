# A literal counterexample to the unrestricted connectivity implication

[CyclicBiplaneDelta.lean](CyclicBiplaneDelta.lean) uses points and line
labels in Z/11Z and the difference set {1,3,4,5,9}. It defines incidence,
the primal and dual proper-triangle neighbor relations, the source's
singleton-intersection rule for flag–line incidence, and the actual
residue at the flag (1,0).

The six printed declarations prove thickness and pairwise collinearity,
line intersection sizes, connectivity of both neighbor graphs, absence
of flag–line incidences, the four-point residue set and disconnection of
that residue. This refutes the unrestricted forward implication in L092
Lemma 3(1). It does not refute the principal theorem's hypothesis of a
partial linear space: the counterexample has two lines through every
pair of distinct points.

The [fresh compiler report](CyclicBiplaneDelta.check.json) and
[public replay](../phase208_public_replay/report.json) record Lean 4.32.2,
the pinned mathlib revision and standard axioms only. Altering the
difference set or replacing the singleton intersection by a pair is
rejected. The design itself is classical; this certificate concerns its
application to the printed statement, without a historical-priority claim.

See the [written correction](../phase186_biplane_delta_correction.md)
and [independent review](../phase199_L092_review.md). The certificate does
not formalize the separate uniform construction or its classification.
