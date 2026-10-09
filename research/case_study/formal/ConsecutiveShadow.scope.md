# Consecutive Boolean ranks: formal scope

`BooleanShadow.exists_witness_in_consecutive_ranks` proves the following.
For a finite universe, retain every subset size from `lo` through `hi`,
where `0 < lo` and `hi < |universe|`. Let `k` be a retained size and `U` any
finite family of retained subsets. If its common size-`k` shadow is nonempty,
there is a flag `C` of at most two retained subsets, incident with all of `U`,
whose size-`k` shadow is exactly the same.

The query family need not be a flag. The formal `Witness` predicate, imported
from [BooleanShadow.lean](BooleanShadow.lean), includes the cardinality bound,
properness of its members, pairwise comparability, incidence with the query,
and equality of all shadow elements. This module additionally proves that
each witness cardinality stays between `lo` and `hi`. Its two auxiliary lemmas
establish the necessary lower-union and upper-intersection rank bounds.

The successful fresh compiler report is
[ConsecutiveShadow.check.json](ConsecutiveShadow.check.json). Compilation also
freshly compiled its local BooleanShadow prerequisite. The previous saved
BooleanShadow report was preserved. Only `propext`, `Classical.choice`, and
`Quot.sound` occur in the printed axiom list; there is no `sorryAx`.

The weighted-tree identification, rank-two and branching obstructions,
symmetric-group primitivity, and passage to all residues are outside this
module. They are proved in the [written derivation](../phase6_weighted_tree.md).
No whole-paper or current-open-problem claim follows from this certificate.
