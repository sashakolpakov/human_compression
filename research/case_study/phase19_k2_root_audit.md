# Root review: complete excess-two classification

10 October 2026. **PASS for the stated ordered-marking theorem.** This is an
internal mathematical review, not external peer review or a priority claim.
The accompanying JSON binds the exact proof and fresh executions.

The reviewed category is finite two-groups with d>=3 ordered involutory
path generators, actual intersection property, no adjacent product of
order two, and order 2^(2d+1). The count is of marked isomorphism classes.

## Mathematical review

1. The retained forest quotient identifies K=gamma3 and gives |K|=4 and
   K intersect G_S=gamma3(G_S). Strict decrease of the nontrivial lower
   central terms bounds the class by four directly. Central K is exactly
   the previously classified class-at-most-three contribution.
2. For noncentral cyclic K, an order-four beta would force generators of
   K into two distinct edge parabolics. Actual IP excludes this. Exactly
   one edge alpha generates K; only the two incident beta words may be
   nontrivial, and each is its square. The endpoint count gives 4d-8.
3. For noncentral elementary-abelian K, all alpha words are fixed by G.
   A nonfixed beta has full triple support. A moving marker puts K into
   an interval of length at most four. Two nonfixed beta words would
   occupy adjacent triples; the exact class-four commutator identities
   would make every marker centralize K. Therefore exactly one beta is
   nonfixed. Only its middle marker moves it, and an optional nontrivial
   alpha lies on one of its two edges. This gives 5d-12.
4. Existence is constructive. The affine seed (Z/4)^2 semidirect D8 has
   order 128 and the required noncentral V4 kernel. The cyclic seed is
   D32. Central attachments and fiber products with the retained edge
   and triple covers realize the optional parameters. The marked words
   isolate each auxiliary kernel before the central identifications;
   hence the diagonal generators fill the asserted fiber products.
5. The parabolic kernels have exact principal or nested profiles. Lifting
   a common quotient image and correcting by the common kernel proves
   actual IP. This is not an inference from quotient IP alone. The new
   NestedKernelIntersections Lean module certifies that abstract adapter;
   establishing the profiles for these constructions remains written.
6. The marked presentations have at most 4|C_d| elements by collection
   modulo K, and the constructed groups attain that order. This proves
   uniqueness for each parameter choice, not just existence. Parameters
   are marked words and cannot be identified by a marked isomorphism.

Adding the class-three contribution gives
`a_2(d)=(25d^2-107d+122)/2`. The four displayed adjacent-order type
counts sum to the same polynomial. Neither interpolation nor a finite
group catalogue is an input to the all-rank proof.

## Fresh execution

The root reran the independent NQ census from the frozen script. It
enumerates all 207 normal subgroups of the universal rank-three
class-four quotient, tests all 23 eligible order-128 quotients, constructs
184 parabolics and checks all 1,472 pairwise meets. Exactly 13 markings
pass: six central, four noncentral cyclic and three noncentral V4.
The actual distinguished generators are transported through the NQ map.
Candidate selection does not use the proposed alpha/beta classification.

The root also reran the separate standard-library affine seed checker:
128 elements; lower-central orders 128,16,4,2,1; eight parabolic kernel
and order checks; all 64 subgroup meets. Both executions passed. The
author's additional ranks-four/five group diagnostics and primary-source
census comparison are retained saved records, not claimed as root reruns.

## Boundary

The full necessity, construction and uniqueness arguments remain written
mathematics. The bounded census and partial Lean certificate do not
constitute an end-to-end formal proof. The older small-order counts agree
in their matched numerical scopes; their individual presentations and
publication priority have not been established here. This result receives
no infinity marker or matched proof-length ratio.
