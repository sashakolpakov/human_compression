# Coprime fiber-product generation

This module proves the complete theorem and paired-generator corollary in
[the written argument](../phase115_coprime_pullback_theorem.md).
The [independent review](../phase126_coprime_pullback_review.md) checks the
mathematical and formal statements, fresh compilation and wrapper controls.

For group homomorphisms `f : A →* D` and `g : B →* D`, the actual subgroup
`fiberProduct f g` consists of the pairs `(a,b)` with `f a = g b`.
Neither homomorphism is assumed surjective onto `D`.

- `snd_kernel_mem` proves that a subgroup contained in the fiber product,
  surjective onto `B`, contains its entire pure second kernel when the two
  kernel cardinalities are coprime.
- `eq_fiberProduct_of_coprime` also assumes surjectivity onto `A` and
  proves equality with the whole fiber product.
- `closure_paired_generators` assumes compatible paired generators whose
  coordinate families generate both groups and proves that the pairs
  generate the entire fiber product.

The written theorem assumes finite kernels. The formal statement uses
`Nat.card` and also covers the case of one infinite kernel: coprimality
then forces the other kernel to be trivial. No kernel is assumed abelian;
the power argument takes place in individual cyclic subgroups.

All three declarations use only `propext`, `Classical.choice` and
`Quot.sound`. There are no unproved placeholders or native-evaluation
axioms. Compilation trusts the installed Lean compiler and compiled
dependencies; their pinned source revisions and tracked-file cleanliness
are checked, but their build objects are not independently rebuilt.

This is a classical algebraic step used by the cover constructions. It
does not formalize their particular quotient maps, local-parabolic
applications, intersection properties, presentation recognition or
geometric conclusions. It makes no historical-priority or new-conjecture
claim, and does not complete the formalization of U or Module A.
