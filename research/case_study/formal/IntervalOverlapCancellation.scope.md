# Interval-overlap cancellation: admitted formal scope

[IntervalOverlapCancellation.lean](IntervalOverlapCancellation.lean)
proves that weights in any additive commutative monoid on overlaps of two
internally disjoint finite interval families vanish if all row and column
sums vanish. The intervals are finite order-convex subsets of the natural
numbers. A leaf in every nonempty supported subgraph is derived from the
earliest right endpoint. Neither acyclicity nor additive cancellation is
assumed. Empty intervals and families are permitted.

The [independent complete proof review](../phase155_interval_overlap_root_review.md),
[frozen author scope](../phase149_interval_overlap_scope.md) and
[fresh public compilation](IntervalOverlapCancellation.check.json) record
the three theorems and their hypotheses. Only standard axioms are reported.
The pinned compiler and cached standard-package objects remain trusted.

The group application must construct the weights and prove the sum
identities. This module does not prove the mixed-group intersection
property or a polytope theorem, and carries no historical-novelty claim.
