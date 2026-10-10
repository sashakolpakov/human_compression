# Partial Lean certificate for graded support lifting

[GradedSupport.lean](GradedSupport.lean) compiles against the pinned Lean
4.32.2 and Mathlib checkout recorded in
[dependency_manifest.json](dependency_manifest.json). The successful
[compiler report](GradedSupport.check.json) has exit code zero and no
`sorryAx`.

Three generic group-theoretic components are kernel checked:

* `common_image_trivial_of_split_kernel`: if two subgroups meet only in
  the identity and a homomorphism kernel factors through them, their
  images also meet only in the identity. The proof includes the exact
  noncommutative rearrangement used in the descending argument.
* `subgroup_product_injective`: actual trivial intersection makes the
  binary ordered multiplication map injective, without a commutativity
  assumption.
* `factorization_of_cardinality`: that injectivity, together with the
  explicitly stated finite cardinality equality and containment in a
  subgroup D, makes the product map onto D.

The first two theorems use only the standard `propext` axiom; the finite
cardinality theorem also uses standard `Classical.choice` and
`Quot.sound`. No additional axioms or unproved placeholders are introduced.

This is a partial certificate for
[the written graded-support proof](../phase15_graded_support.md).
It does not formalize lower-central Lie rings, the forest cut, graded
spanning, the quotient-index multiplication that supplies the displayed
cardinality equality, the descending induction, or the final cocycle and
polytope identification. The complete forest theorem is not claimed to
be formalized.
