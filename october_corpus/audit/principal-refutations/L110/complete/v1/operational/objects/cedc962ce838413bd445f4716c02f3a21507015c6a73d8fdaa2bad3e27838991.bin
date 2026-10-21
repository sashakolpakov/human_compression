# Scope of the coset-coordinate certificate

`CosetCoordinates.lean` imports the left-coset membership definition from
`RankThreeFactorization.lean` and proves two statements for any group and any
index type, with no finiteness or normality assumption.

* `common_point_of_coordinates`: assume that every tuple of coset coordinates
  represented in K has a simultaneous representative in K. Then any family
  of H_i-cosets each meeting one fixed K-coset has a common point in that
  K-coset. Pairwise incidence between the H_i-cosets is unnecessary.
* `coordinates_of_common_point`: the corresponding common-point property
  implies the coordinate-surjectivity hypothesis.

The first theorem uses `propext` and `Classical.choice`; the converse uses
only `propext`. The saved report records a fresh successful compiler run
against the pinned dependencies. No unfinished proof is accepted.

For the higher-rank Suzuki construction, the written proof establishes the
coordinate hypothesis using independent cyclic factors in a semidirect
product. This is a surjection of **sets of cosets**, not a group homomorphism:
the subgroups containing the common order-four complement need not be normal.
The Chinese-remainder instantiation, algebraic torus construction,
Lang–Steinberg descent, subfield Helly theorem, maximality, residual
connectedness and source-classification comparison remain outside this Lean
module. In particular, this certificate alone does not prove Helly for the
H_i family when the distinguished K-coset is absent.
