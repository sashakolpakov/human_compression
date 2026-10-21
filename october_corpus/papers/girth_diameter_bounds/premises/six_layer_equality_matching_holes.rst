Two disjoint missing cells at six-layer mass twenty-one
=======================================================

Status: proposed elementary restriction, pending distinct proof review.

In a simple quartic graph of girth at least five, suppose six consecutive
nonsingleton BFS layers contain exactly21 vertices. For adjacent geodesic
centres in local layers2,3, their two radius-two balls cannot have seven
common second neighbors with the two missing grid cells disjoint.

This excludes one equality21 configuration. It does not exclude seven
occupied cells with adjacent holes, or the cases with five or six
occupied cells. In particular, no six-layer22 theorem is claimed.

The acquired local framework
----------------------------

Use six_layer_twenty_equality_exclusion.rst, SHA256
d80cc0af013665beecd6fbfbdb02d530b399319c17b4824d6de0b5e061ca0d69,
accepted by six_layer_twenty_one_acceptance.json, SHA256
1befdd15630d78611b38c904e86322d0a2234e483f78e1995b048b123e040121.
We repeat the precise facts needed here, rather than using any solver
result as a premise.

The centres are u in layer2 and v in layer3. Their other neighbors are
A1,A2,A3 and B1,B2,B3, with A1 in layer1 and B1 in layer4. Occupied grid
cell ij is a vertex Cij with parents Ai,Bj. Disjoint holes can be named
11,22. The seven grid vertices are

  C12,C13,C21,C23,C31,C32,C33.

There are private vertices L,U with respective parents A1,A2, and
R,V with parents B1,B2. The two-ball union has19 vertices. Call the two
additional vertices X,Y.

The cross cells C21,C31 force A2,A3 to have index at least2; the cross
cells C12,C13 force B2,B3 to have index at most3. Thus

  A2,A3,B2,B3 have indices2 or3.

Only L can be a layer0 vertex of the union: if U were there, its parent
A2 would have index1, contrary to C21. Similarly only R can lie in
layer5. Nonsingleton boundaries therefore force

  L,X in layer0; R,Y in layer5; U,V interior.

All centre and parent vertices already have degree4 in the displayed
union. Every grid vertex has exactly two additional neighbors besides
its two parents. The grid-induced components are paths on at most three
vertices, with exactly two additional incidences to distinct nongrid
endpoints. Parent edges are omitted in this incidence count, and the
already saturated parents cannot supply additional edges. A vertex
other than a common parent cannot meet two grid vertices sharing that
parent. A private vertex cannot meet a grid vertex with its own parent.

Throughout, an edge changes the original BFS index by at most one.
Support reversal interchanges u/v, A/B, U/V and local indices h/5-h;
it does not assert that the reversed layers are a BFS partition.

A useful middle-path restriction
--------------------------------

If a grid vertex is the middle of a grid path, its two grid neighbors
must have distinct rows and distinct columns, different from those of
the middle. Hence the only possible neighbor pairs for the particular
middle vertices C12 and C21 are respectively

  C12: {C21,C33} or {C23,C31};
  C21: {C12,C33} or {C13,C32}.                         (1)

Each endpoint of such a three-vertex grid path then requires a nongrid
neighbor. It cannot acquire a further grid neighbor, since a grid path
has at most three vertices. We will use (1) explicitly.

Case I: U and V both at the same near-boundary index
---------------------------------------------------

By reversal suppose both U,V have index1. Their parents A2,B2 then have
index2. C21 has index3 because its parents have indices2,4.

C21 cannot meet any nongrid vertex other than its prescribed parents:
U,V have index1, all boundary vertices have indices0,5, and parents are
saturated. It must therefore be a middle vertex of a three-vertex grid
path. Each of its two possible pairs in (1) includes a column2 endpoint,
either C12 or C32. That endpoint has index2 or3: it meets C21 at3 and
has parent B2 at2. No boundary vertex can meet it. V is forbidden by
the common parent B2. U is the only remaining possibility, and only
when the endpoint has index2. But U-A2-C21-endpoint-U would then be a
quadrangle. Thus neither pair in (1) is possible. This excludes both
U=V=1 and, by reversal, U=V=4, whether or not U,V are adjacent.

Case II: U at4, V at1
---------------------

Here U cannot meet row1 grid vertices, whose indices are at most2,
or row2 grid vertices, whose parent A2 it shares. It can meet at most
one grid vertex, in row3. Since V at1 is unavailable and its parent is
already prescribed, degree4 forces U to meet BOTH R,Y and one grid
vertex. Adjacency to R prohibits any column1 grid neighbor: such an
edge would form a quadrangle through R,B1. Similarly V must meet BOTH
L,X and one grid vertex, and cannot meet row1 grid vertices.

A row1 grid vertex, if it is a grid-path endpoint, can therefore meet
only X. U is too far, V is forbidden by its L adjacency, and L shares
the row1 parent. It must then have index1. C12 and C13 belong to
different grid paths; at most one can meet X. Neither can be isolated,
which would need two different exterior neighbors. Their paths require
at least five grid vertices: one middle path of length three vertices
and another path of at least two vertices, or two middle paths.

Likewise endpoints among C21,C31 can meet only Y and must have index4;
their two paths require at least five grid vertices. The left and right
paths cannot coincide. Two such endpoints would have indices1 and4,
too far for a path with at most two edges. A row1 middle has index at
most2 and cannot meet a column1 endpoint at4. A column1 middle has
index at least3 and cannot meet a row1 endpoint at1. There is only one
middle position in a three-vertex path. At least ten grid vertices
would be required, whereas there are seven.

Case III: U at1, V at4
---------------------

Now A2 has index2, B2 index3, C12 index2 and C21 index3.
The only possible additional nongrid neighbor of C12 is U: its own
parent B2 forbids V, its own parent A1 forbids L, and X,R,Y are too far.

Suppose C12 is a middle vertex. Each pair in (1) has a column1 endpoint,
C21 or C31, whose index must be3: it meets C12 at2 and B1 at4. That
endpoint's only possible nongrid neighbor is V at4. U and both left
vertices are too far; both right boundary vertices are also too far
from index3. But V-B2-C12-endpoint-V is a quadrangle. Hence C12 is not
a middle. It cannot be isolated, since only one nongrid neighbor is
available. It must be an endpoint adjacent to U.

By support reversal C21 must similarly be an endpoint adjacent to V.
The edge U-C12 prohibits U-L, by the quadrangle U-L-A1-C12-U.
U,V are too far to be adjacent. Thus the three additional neighbors
of U must be X and two grid vertices. Besides C12 the other grid
neighbor is necessarily C33: row2 is forbidden by U's parent; another
column2 vertex is forbidden by its common parent with C12; and C31
is too far from U at1. Symmetrically V must also meet C33. But a
vertex cannot be adjacent both to U at1 and V at4. Contradiction.

Reduction when a private vertex has index2 or3
----------------------------------------------

Suppose at least one of U,V has index2 or3. By reversal we may assume
it is U. None of the boundary vertices is adjacent to U by support.
U can meet at most two grid vertices (distinct rows other than its own
row2). Its full degree therefore forces the edge U-V and two grid
neighbors.

The edge U-V forbids U from meeting column2 grid vertices, through the
quadrangle with V,B2. Similarly V cannot meet row2 grid vertices,
through U,A2. Thus either private vertex can meet only

  C13,C31,C33,

and the only possible two-element grid-neighbor set is {C13,C31}.
The grid-neighbor sets of U,V are disjoint, by triangle-freeness.
V therefore cannot also have index2 or3: full degree would require
the same two neighbors. It is at index1 or4. The edge U-V leaves just
the two cases

  (U,V)=(2,1) or (3,4).

In both, U meets C13,C31. V has its parent and U already; its only
possible grid neighbor is C33. Thus V has either C33 and one boundary
neighbor, or both boundary neighbors at its end and no grid neighbor.
These alternatives are all retained below.

Case IV: U at2, V at1, with V adjacent to C33
--------------------------------------------

Here B2 is at2, C31 at3, and C33 at most2. C21 has index3 or4.
If C21 were at3, it could meet no nongrid vertex and would have one
of the two middle pairs in (1). Each pair includes a column2 endpoint,
C12 or C32, with index2 or3. No boundary is available at those indices.
V shares its parent B2, and U is forbidden by the quadrangle through
V,B2. Such an endpoint would have no external neighbor. Consequently
C21 is at4, forcing A2 to have index3.

C21 now has only Y and C32 as possible additional neighbors: U shares
its parent A2, R shares its parent B1, V and both left boundary vertices
are too far, and C12,C13,C33 have indices at most2. Thus both these
edges are forced, with C32 at3. C32 needs one more additional neighbor.
U,V are forbidden by B2, and no boundary is adjacent to index3.
Its only eligible grid neighbor besides C21 is C13: C23 would share
row2 with its existing neighbor C21. Hence C32-C13 is forced and
C13 is full, already having U as its other additional neighbor.

Consider C23, whose index is at least2 because A2 is at3. Its possible
additional neighbors have now been reduced to C12 and R. Indeed U
shares its parent A2; V is forbidden by the quadrangle through U,A2;
Y cannot meet both C21 and C23 with their common parent A2; both left
boundary vertices are too far. Of the potential grid neighbors, C32
is full and C31 is forbidden by U-A2-C23-C31-U; the remaining one
is C12. But C12 has index at most2 and R has index5, so C23 cannot
be adjacent to both. Its degree is at most3, a contradiction.

Case V: U at3, V at4, with V adjacent to C33
--------------------------------------------

B2 is at3, C12 and C13 at2, and C33 at least3. C12 has no available
nongrid neighbor: U is forbidden through V,B2, V and L share its
parents, and X,R,Y are too far. It must therefore be a grid middle.
The pair {C21,C33} is impossible, since C12-C33 would form the
quadrangle V-B2-C12-C33-V. Thus its pair is {C23,C31}.

C31 is at3 and has its prescribed external neighbor U. C23 is an
endpoint, with index at most3. It cannot meet U (common parent A2)
or V (quadrangle through U,A2), and the right boundary is too far.
It must have index1 and meet a left boundary vertex. L is forbidden
by L-A1-C12-C23-L, so C23-X is forced. Its two parents A2,B3 are
therefore both at2.

C21 is now at3. U shares its parent A2, V is forbidden through U,A2,
and every boundary vertex is too far. It is a grid middle. C12 already
has its two grid edges, so (1) forces the pair {C13,C32}. C32 must
have a nongrid neighbor. U is forbidden through V,B2 and V shares
its parent; no left boundary is available. It must be at4 and attach
to R or Y. R is forbidden by R-B1-C21-C32-R, so C32-Y is forced.
Its parent A3 consequently has index3.

Finally C33 has parents A3 at3 and B3 at2, and neighbor V at4, so
its index is3. Its possible further grid neighbors are only C12,C21,
both already full as grid middles. U would form a triangle with V,
and all boundary vertices are too far. It has degree at most3.

Case VI: V has both boundary neighbors and no grid neighbor
-----------------------------------------------------------

This treats both (U,V)=(2,1) and (3,4). In the former, V meets L,X;
in the latter it meets R,Y.

C12 has no nongrid neighbor. U is forbidden through V,B2, V and L
share its parents, and R,Y are too far. For (U,V)=(2,1), its only
remaining possibility X is forbidden by X-V-B2-C12-X. For (3,4),
C12 already has index2 from its parents A1 at1 and B2 at3, so X
is too far. Thus C12 must be a grid middle.

Each pair in (1) contains a column1 endpoint at index at least3,
so C12 must have index2 and that endpoint index3. The pair {C21,C33}
is impossible: C21 cannot meet U with its common parent A2, V has no
grid neighbor, and all boundary vertices are too far from index3.
Hence the grid path C23-C12-C31 is forced.

C31 has its prescribed external neighbor U. C23 must have index1:
it cannot meet U or V, cannot reach the right boundary from its index
at most3, and must therefore meet a left boundary vertex. The edge
to L would form L-A1-C12-C23-L, so C23-X is forced. Its parents
A2,B3 both have index2.

C21 is consequently at3. It has no nongrid neighbor, since U shares
its parent, V has no grid neighbor and all boundaries are too far.
C12 is already a full middle, so the path C13-C21-C32 is forced by
(1). C32 needs an external neighbor. U is forbidden through V,B2,
and V shares its parent. Its index is at least2 because it meets
C21 at3, so it cannot meet the left boundary. If V is at1, B2 is
at2 and C32 has index at most3, excluding the right boundary too.
If V is at4, a right neighbor would require C32 at4; Y is forbidden
by Y-V-B2-C32-Y and R by R-B1-C21-C32-R. No external neighbor exists.

Conclusion and scope
---------------------

Cases I--III exhaust both-private-extreme assignments. If a private
vertex is at2 or3, the reduction gives the two adjacent-index pairs,
with the remaining alternatives exhausted by IV--VI. Thus disjoint
holes11,22 are impossible at equality21.

Together with the separately accepted eight-cell exclusion, the still
unresolved equality21 cases have m=5 or6, or m=7 with the two missing
cells sharing a row or column. No contradiction for these cases is
asserted. No order94 exclusion or enumeration credit follows here.

Diagnostic and attribution
---------------------------

The once-run fixed diagnostic returned unverified UNSAT in0.604s;
request six_layer_matching_holes_request.json, SHA256
0a4d66cad9225235ec83d0109199f0fe52e3afd276186c21bf8dc3da412ffa50.
Its result and clean terminal receipt are retained in
six_layer_matching_holes_result/result.json and
six_layer_matching_holes_execution/receipt.json. The solver outcome
was guidance only; the complete handwritten contradictions above
are the mathematical argument. No new solver or enumeration was run.

The acquired adjacent-ball framework and prior Moore/cap/section
attribution remain unchanged. There is no historical novelty, Lean,
whole-graph existence, source-completion or accepted-root claim.

