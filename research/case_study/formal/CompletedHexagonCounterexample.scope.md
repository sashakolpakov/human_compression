# Completed-hexagon reflection: formal scope

[CompletedHexagonCounterexample.lean](CompletedHexagonCounterexample.lean)
defines a twelve-vertex graph: a hexagon with one third-coloured tip on
each edge. Base vertices are indexed by ZMod6 and have alternating colours;
the tip on {i,i+1} has colour two. The explicit permutation sends a base
index i to −i and a tip index i to −i−1.

The file proves that this permutation preserves adjacency and colours,
is nonidentity and has order two. It also proves that an element of the
cyclic group of order three whose square is one is the identity. These
statements obstruct the printed type-preserving group C3 in F010,
Example5.1. The source-to-model identification and the conclusion about
isomorphic groups are stated in the written application; a general graph
automorphism-group equivalence is not constructed here.

All four named reports in the [fresh public compile](CompletedHexagonCounterexample.check.json)
use only `propext`, `Classical.choice` and `Quot.sound`. The finite cases
are evaluated by ordinary `decide`, without a native-evaluation axiom.
Lean 4.32.2 and the recorded package revisions are checked by the runner;
compiled dependency objects remain trusted.

The [independent review](../phase188_F010_independent_review.md) and
[root admission](../phase193_root_admission.md) separate this certificate
from the GAP/GRAPE computation of full group orders and the written
all-group representation theorem. Neither the three universal constructions
nor the recursive symmetric-group family is fully formalized by this file.
