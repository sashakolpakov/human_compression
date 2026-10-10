# Quadratic translations: admitted formal scope

[CharacteristicTwoTranslations.lean](CharacteristicTwoTranslations.lean)
proves the equal-label power relation as equality of actual linear
equivalences on the entire ambient vector space over any field of
characteristic two, for every integer exponent. The form may be degenerate
and the vector space need not have finite dimension. The unit-vector and
polar-form hypotheses are explicit. Translation composition, exponent two,
covariance and the required normalization are proved, not assumed in the
final theorem.

The [independent proof review](../phase151_source_relators_root_review.md)
checks the complete implementation and its written consumer. The
[frozen author scope](../phase140_source_relators_scope.md) lists all twenty
audited declarations. The [fresh public build](CharacteristicTwoTranslations.check.json)
uses only subsets of `propext` and `Quot.sound`. Two missing pinned Mathlib
objects were freshly built in a private overlay; the compiler and remaining
cached compiled dependencies remain trusted.

Finite-field parameter choice, the retained orthogonal-group generation
and intersection theorem, and polytope correspondence are separate
obligations. This is not a full formal proof of the source conjecture or
of the finite-existence families derived in the written manuscript.
