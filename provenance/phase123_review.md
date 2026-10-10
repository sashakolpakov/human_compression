# Formal verification of the projective matrix core

10 October 2026. Admission after the independent phase241 review of six
actual matrix theorems supporting Topic E. This adds one canonical Lean
file and no principal-source or conjecture credit.

The frozen phase237 author manifest has SHA256
`2095e96025bb4978babe7ee2e64d23267c8d0a3452c8a815a2bebe0cdb3ef98f`.
The independent phase241 manifest has SHA256
`29d4770c0e12a5a64e6a685f9c02662875dc2a11fd51a2ea7cc3ff7b022182cd`.
All twenty exports and both manifests are preserved byte for byte.
The canonical ProjectiveDihedralMatrices source has SHA256
`98a746e4b34c5dcf3da4c4bf575d8a2517dfa59d2a4a4b44e869c044335df78f`.

The independent reviewer read the complete source, scope and runner,
recompiled all six declarations and checked their mathematical hypotheses.
Root read the review and its separate finite-field checker before this
admission. The result proves centralizer descriptions in the actual
semisimple and unipotent matrix normal forms, with entrywise lemmas and
the trace-zero representative and determinant calculation. It is more
formal coverage of the existing written argument, not a new mathematical
classification or a historical priority claim.

## Fresh public execution

The [formal replay](../research/case_study/phase244_public_replay/report.json)
passes under Lean 4.32.2. All six reports use only propext,
Classical.choice and Quot.sound. Root separately checks all nine pinned
package revisions and clean source trees. Precompiled dependency objects
remain part of the trust boundary.

Both versions with deliberately changed hypotheses fail elaboration.
As the reviewer notes, replacing an inequality by its complementary
equality is an excluded-case test, not a logical weakening. The fresh
[independent matrix computation](../research/case_study/phase244_independent_matrices.json)
also checks actual counterexamples over F₅ and F₂, so the interpretation
does not rest on compiler failure alone. Its diagnostic enumeration
covers 52,224 semisimple configurations and 16,656 unipotent configurations
over F₃, F₅ and F₇. Lean supplies the general theorem; bounded field tests
do not replace it.

The canonical report records the fresh successful output. Generated
sources for the two deliberately false test assertions are retained in
the replay directory with nonzero exit codes; they are not members of
the canonical verified library.

## Remaining formal boundary

Conjugacy over an algebraic closure, transport under a basis change,
passage to PGL and descent of the representative to the original field
remain written. So do the retained classical classifications, universal
finite-group calculations and geometric applications. Neither the full
centralizer-descent theorem nor either complete polytope classification
is yet a Lean theorem.

The canonical file count rises 83→84: 83 use no native-evaluation axioms;
the one earlier transfer file retains its four recorded native axioms.
The 23 principal-source contracts and eleven question entries do not change.
