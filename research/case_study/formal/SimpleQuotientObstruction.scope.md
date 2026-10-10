# Simple-factor obstructions under quotients

The [Lean source](SimpleQuotientObstruction.lean) contains nine printed
declarations. The [fresh public replay](../phase217_public_matrices/report.json)
compiled the identical source with Lean4.32.2 and the pinned mathlib
dependencies. Only propext, Classical.choice and Quot.sound occur.

The principal theorem is
`surviving_adjacent_product_separates_simple_factor`. For a noncommutative
simple group S, any homomorphism from C×S that retains a nontrivial
product of two equally signed generators, whose common sign squares to
one, separates their S-coordinates. This follows by proving that its
restriction to S is injective and that every kernel element has trivial
S-coordinate. The separate `intersection_witness_survives` theorem
then preserves an actual witness under such a map.

The remaining declarations prove centerlessness, nontriviality and
injectivity of the simple-factor restriction, the kernel and fiber
steps, and triviality of a character killed on a subgroup whose index
is coprime to the codomain order. The index-three/binary specialization
provides an alternative sign argument.

These are general mathematical theorems, with the hypotheses stated
explicitly. The file does not define Sp₄(32), certify its order or
simplicity, identify the source presentation, or instantiate the
geometric counterexample. Those are separate written and computational
parts of the [complete argument](../phase212_n11_obstruction.md).
No finite group assertion is introduced as a Lean axiom.

The canonical source is byte-identical to the independently reviewed
`phase212_formal/SimpleQuotientObstruction.lean`. The compiler and cached
objects from the pinned dependency checkouts remain trusted.
