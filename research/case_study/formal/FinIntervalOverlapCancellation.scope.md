# Finite-marker interval cancellation: admitted formal scope

[FinIntervalOverlapCancellation.lean](FinIntervalOverlapCancellation.lean)
transports the [interval theorem](IntervalOverlapCancellation.scope.md)
to subsets of `Fin n`. It proves convexity preservation and an exact
disjointness equivalence under `Fin.val`, then applies the unchanged core
theorem with the same weights and sums. The case n=0 is included.

The [independent proof review](../phase155_interval_overlap_root_review.md)
and [author scope](../phase154_fin_interval_scope.md) cover all three new
declarations. The [fresh public compilation](FinIntervalOverlapCancellation.check.json)
imports a freshly compiled core and reports only standard axioms. The
installed compiler and cached standard-package objects remain trusted.

This is a representation adapter, counted as a separate scoped Lean
module rather than another research result. It adds no group application,
source coverage, conjecture solution or compression factor.
