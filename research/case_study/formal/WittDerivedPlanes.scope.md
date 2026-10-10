# Three explicit maps to the projective plane of order four

[WittDerivedPlanes.lean](WittDerivedPlanes.lean) defines three finite
incidence tables, explicit point and line permutations, and the coordinate
incidence relation on PG(2,4). For each table it proves that both maps are
bijective and that incidence is equivalent to the literal GF(4) dot-product
equation. The nine printed declarations include the resulting incidence
isomorphisms.

The field arithmetic is imported from the unchanged
[DeletedLineFourResidue.lean](DeletedLineFourResidue.lean). A fresh
[public replay](../phase208_public_replay/report.json) regenerates the
Lean file from the computed witness, checks exact byte equality, and
compiles it with Lean 4.32.2 and the recorded mathlib revision. Its
[compiler report](WittDerivedPlanes.check.json) uses only standard axioms.
Changing an incidence equation or interchanging two point images is
rejected by the compiler.

The bridge from the original Witt block systems to the three displayed
derivatives is checked in GAP and independently in Python. It is **not**
proved in this Lean file. Neither the full design automorphism groups,
the uniform residue theorem nor the higher-rank classification is
formalized here. Their written proofs, borrowed inputs and independent
review are linked from the [admission](../phase208_root_admission.md).
