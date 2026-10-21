Exploratory history and validation boundary
===========================================
The first C++ exploratory pass stopped at its coset-disjointness assertion:
for an odd-order SL rotation it had omitted the scalar negatives in H0.
That failure was preserved in the private explore_stdout.txt. Both scalar
signs are included in the final program, and the actual-group GAP oracle
independently reconstructs the same graphs. The failure was caught before
any author freeze or scientific claim.

The optional GAP probe uses its native finite fields and actual generated
matrix groups, rather than importing the C++ arithmetic. It reconstructs
the selected examples and all seven q7 cases. The q9 row took82.777s,
including its actual SL2(729) order calculation. All twelve current graphs
agree. A thirteenth q4 empty example is retained as an additional diagnostic.
The same author executed both implementations; no distinct human review is
claimed. Pynauty was used only to discover permutations and to compare the
two implementations' unlabeled graph outputs. The required final graph
certificate verifies all actual generators and proves fullness by elementary
refinement and exact subgroup closure (or the explicit28-dimensional flip
kernel and336 quotient), without an automorphism backend.

The unchanged accepted predecessor computations were not rerun. No new
source download, census outside this original, Lean or measurement was made.
