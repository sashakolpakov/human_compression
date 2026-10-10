# Scope of Phase32VoltageTheory.lean

This module proves a generic infinitude criterion for a presented group. It is a group-theoretic theorem, not just a test of literal arrays.

The hypotheses are forward and inverse permutations of an arbitrary state type, integer voltages for arbitrary generator labels, a family of defining words, exact trivial action of every relator at every state, and one word fixing a specified state with voltage −1. It constructs bijections of `State × ℤ` and takes their opposite permutation group so that the multiplication convention agrees with right word traversal. The defining words factor through mathlib's `PresentedGroup.toGroup`.

The proof establishes the action formula for arbitrary integer heights and then proves that the n-th power of the witness sends the base pair to height −n. Consequently its powers in the presented group form an injective map from the natural numbers. The final theorem is `infinite_of_voltage_witness : Infinite (PresentedGroup (relSet relations))` under the stated hypotheses.

The kernel checks the full construction, relator factorization and injection argument. The reported axioms are only `propext`, `Classical.choice`, and `Quot.sound`. There are no unproved placeholders, `native_decide`, or evaluation axioms. Finite literal input hypotheses are supplied and separately kernel-checked by `Phase32L003Infinitude.lean`.

Reproduce both modules using [the portable runner](../phase32_L003_formal_check.py) and the pinned dependency manifest. The runner builds missing pinned mathlib modules into a fresh output directory without changing the installed checkout. The supplied output directory must not already exist.
