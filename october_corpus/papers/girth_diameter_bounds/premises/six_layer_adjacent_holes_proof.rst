Adjacent missing cells at six-layer mass twenty-one
==================================================

Status: corrected handwritten exclusion, pending independent adoption.

This edition preserves and corrects the frozen proposal
six_layer_equality_adjacent_holes.rst, SHA256
ef946affeb8e452d3e00acded66b43e42c5a47fed0de9e698e7e89b966f93214.
The distinct reader found the permitted L--C23 alternative in the U=2,
V=1 case. That alternative is now treated explicitly by the degree
deficit at C31. The original proposal is retained unchanged; no solver
result is used in this correction.

Let a simple quartic graph of girth at least five have six consecutive
nonsingleton BFS layers of total size21. Choose adjacent centres on a
geodesic through these layers, in local layers2 and3. Their two-ball grid
cannot have seven occupied cells and two adjacent missing cells.

This is only an equality21 restriction. Cases with five or six occupied
cells are not excluded here. No six-layer22 or order94 exclusion is claimed.
No solver, graph enumeration or scientific replay is a premise or was run
to prepare this argument.

Framework and fixed geodesic endpoints
-------------------------------------

We use the elementary grid framework in
six_layer_twenty_equality_exclusion.rst, SHA256
d80cc0af013665beecd6fbfbdb02d530b399319c17b4824d6de0b5e061ca0d69,
accepted by six_layer_twenty_one_acceptance.json, SHA256
1befdd15630d78611b38c904e86322d0a2234e483f78e1995b048b123e040121.

Write u,v for the centres at2,3; their other neighbors are A1,A2,A3
and B1,B2,B3. The chosen geodesic supplies

  L -- A1 -- u -- v -- B1 -- R
  0     1    2    3     4    5.

Thus L and R really are private second neighbors, not just vertices
whose placement is optional. Their distances from the opposite centre
are at least3 by the original BFS indices. Up to interchanging the
two sides, adjacent missing cells are11,12. The private vertices are
L,U at A1, R at B1, and V at B2. The seven grid vertices are

  13,21,22,23,31,32,33,

where ij denotes Cij with parents Ai,Bj. The two-ball union has19
vertices; call the two extras X,Y. Each extra is outside this union.
All centre and parent vertices are already saturated. We have

  A2,A3 in {2,3}; B3 in {2,3}; B2 in {2,3,4};
  U in {0,1,2}; V in {1,2,3,4,5};
  C13 at1 or2; C21,C31 at3 or4.

An edge changes the original layer index by at most1. Any interior
vertex has all four neighbors inside the six-layer interval. Boundary
vertices may have further neighbors outside; we never require their
internal degrees to be four.

After omitting the two prescribed parent edges, each grid vertex needs
two extra incidences. Grid components are paths on at most three vertices,
with two distinct nongrid endpoints. A vertex other than the actual common
parent cannot meet two grid vertices sharing a row or column. Private
vertices cannot meet a grid vertex with their own parent. The grid-edge
possibilities, before further full-degree or girth restrictions, are

  13:21,22,31,32;   21:13,32,33;   22:13,31,33;
  23:31,32;        31:13,22,23;   32:13,21,23;   33:21,22.

Every three-vertex grid path contains C13. In particular the only
middle pairs at C13 are {21,32} and {22,31}. This follows directly
from the table and the requirement of distinct rows and columns along
such a path. These are literal adjacency possibilities, not a graph search.

Nonsingleton boundary layers now leave exactly six placements of the
extras: both interior; one interior and one at0; one interior and one
at5; both at0; both at5; or one at each boundary. We treat all six.

Both extras interior
--------------------

Necessarily U is at0 and V at5. Hence B1,B2 are at4, all grid columns1,2
start at3, and only column3 grid vertices can supplement A1 in layer1.

An extra at1 could meet at most one of L,U, at most one column3 grid
vertex, and the other extra. Its degree would be at most3. Thus neither
extra is at1. An extra at2 has no boundary neighbor, so degree4 would
force adjacency to the other extra and three grid vertices. The latter
use all three rows, including the unique row1 vertex C13.

If C13 were at1, its two additional neighbors would have to be both
extras, necessarily at2. They could not be adjacent, by a triangle
through C13, contrary to the preceding degree requirement. If C23 or
C33 were at1, it could meet at most one of L,U and no other grid vertex.
It therefore needs an extra at2. That extra would meet both this column3
vertex and C13, contrary to the common-parent rule. Layer1 is a singleton.

One extra at0 and one interior
------------------------------

Call them X at0 and Y interior. V must be at5, so again B1,B2 are at4
and grid columns1,2 start at3.

If U is at0, Y cannot be at1: only X, at most one of L,U and at most
one column3 grid vertex are available. At2 or3, Y could meet only grid
vertices, at most three. Thus Y is at4. C13 cannot be at1, where only
X could supply an extra edge. At2 it has no nongrid neighbor, so is a
grid middle. Both endpoints of its three-vertex path have index3 and
can meet only Y outside the grid. This repeats the exterior endpoint
of a grid path, giving a quadrangle.

If U is at2, its degree forces U-Y and two grid neighbors. The edge
U-Y forbids Y from meeting row1 grid vertices or L, through A1.
At1, Y could therefore meet only U,X and at most one column3 grid
vertex. At2 or3 it could meet U and at most two grid vertices. Index4
is too far from U. All possibilities have deficient degree.

If U is at1, its three additional neighbors must be X,Y and a
column3 grid vertex. Thus Y is at1 or2. At1, Y cannot meet X (triangle
through U) or L (quadrangle through U,A1), and can meet at most one
grid vertex. At2 it can meet U and at most two grid vertices, since
row1 is forbidden by U-Y. Again its degree is deficient.

One extra at5 and one interior
------------------------------

Call them X at5 and Y interior. Both L,U are at0. If Y were at1,
degree4 would require V, one left private vertex and two grid vertices
in columns2,3. Its edge to the left private forbids row1, and its edge
to V forbids column2. Only one grid column would remain. At2 or3,
degree4 would require V and three grid vertices, but the Y-V edge
forbids column2. Consequently Y is at4.

V cannot be at1: besides its parent it could meet at most one left
private and one column3 grid vertex. At2 it could meet at most two
grid vertices. Hence V is at3,4 or5.

First suppose B2 has index at least3. The only layer1 candidates
besides A1 are column3 grid vertices. C13 can have at most one extra
neighbor, in column2. A vertex Ci3 with i=2 or3 would have to meet
one left private and Cj2 in the other row. Cj2 must be at2. It cannot
meet V with its own parent, Y at4 or either boundary. Nor can it have
a second grid neighbor: the remaining row1 choice C13 repeats column3,
and the alternative Ci1 repeats row i along the path. Degree is deficient.

It remains that B2=2, so V=3. V's degree forces Y and two grid
neighbors, one each in columns1,3. C13 is not at1, since it still has
at most one extra neighbor. Any other grid vertex at1 must meet a
left private and a grid vertex in the other column2/3. If that other
vertex were C13, the edge to the left private would give a quadrangle
through A1. Thus, up to swapping rows2,3, the nonsingleton layer1 forces

  C23 -- C32, with their other extra edges to different L,U.

These two vertices are full, and A2,A3,B2,B3 all have index2. In
particular C21,C31=3 and C13=2. C22 has no nongrid neighbor: V shares
B2; Y-V forbids Y-C22; the right boundary is too far; each of L,U
already meets C23 or C32, sharing one of C22's parents. Its only
possible grid middle pair is therefore {C13,C31}.

C13's exterior endpoint must be V. The other endpoint C31 cannot
also meet V, by a quadrangle through the three-vertex path, so meets
Y. V's second grid neighbor must then be C21. The remaining extra
edge of C21 is forced to C33: C13 would give a triangle through V,
and C32 is full. C33 cannot meet a left boundary from its index at
least2, cannot meet V with its existing column3 neighbor C13, and
cannot meet the full C22. Its remaining neighbor must be Y, forcing
C33=3. But Y now meets C31,C33 with the common parent A3. Contradiction.

Both extras at0
----------------

V is at5 and B1,B2 are at4. U cannot be at2, since it could meet at
most two grid vertices and no other available nongrid vertex. Thus U
is at0 or1. Consider a grid component containing a column1/2 vertex,
which has index at least3.

If both exterior endpoints were on the left, the grid endpoint
indices would be1, except possibly one at2 attached to the single
interior U. A path of at most three vertices could not then contain
index3: its middle is adjacent to an index1 endpoint, and its endpoints
are at most2. If its exterior endpoints were on opposite sides,
their grid indices would have to be2,4, with a middle at3. Such a
three-vertex path contains C13; that vertex can only be its left
endpoint at2, but cannot attach to U with its own parent A1.

Thus both exterior endpoints must be R,V, and their grid endpoints
have index4. A three-vertex path is impossible because it contains
C13 at most2. An isolated column1/2 vertex cannot meet both R,V,
one of whose parents it shares. For a two-vertex path with endpoints
R,V, neither grid vertex can have column1 or2: at the near endpoint
that gives a triangle, and at the other a quadrangle through B1 or
B2. Both would have column3, impossible for a grid edge. This excludes
every component containing a column1/2 vertex, a contradiction.

Both extras at5
----------------

U is at0. At1, V could meet at most one of L,U and one column3 grid
vertex; at2 or3 it could meet only grid vertices, at most two. Hence
V is at4 or5, and B2 has index at least3. The layer1 deficit argument
in the preceding interior-extra case with B2>=3 applies verbatim:
C13 lacks two extra neighbors, and any other column3 vertex at1
would force a column2 neighbor at2 with deficient degree. No interior
extra is now present to add an edge. Layer1 is a singleton.

One extra at each boundary
--------------------------

Write X at0 and Y at5. First take U=0. The only possible interior
private V has index1 or4: at2 or3 it could meet at most two grid
vertices and no nongrid vertex. If V=5, C13 at1 has only X available,
whereas at2 it would be a middle with both grid endpoints at3 and
no nongrid endpoint available.

If V=1, degree4 forces V-X, an edge to one of L,U, and one column3
grid edge. The edge to a left private forbids V-C13. If C13=2, a
middle path has a column1 endpoint at3 with no nongrid neighbor.
If C13=1, it must meet X and a column2 grid vertex E at1 or2. E has
no exterior neighbor: the left privates give quadrangles through
A1,C13, X gives a triangle, and V shares B2. Thus E must be a grid
middle, forcing E=2 and a column1 endpoint at3, again with no exterior
neighbor. If V=4, B2>=3. At C13=2 a column2 endpoint at2 or3 has no
exterior neighbor. At C13=1, the edge X-C13 and a column2 neighbor
E=2 are forced; E must be a middle, but its column1 endpoint at3
cannot attach to V because V-B2-E-endpoint-V is a quadrangle.
This excludes U=0.

V=5 also excludes either interior choice of U: at2 U has at most
two grid neighbors; at1 it has only X and at most one column3 grid
neighbor besides its parent. We may therefore take U=1 or2 and V
interior. The following short branches exhaust these placements.

U at1, with U and V nonadjacent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

U must meet X and two grid vertices in columns2,3 and distinct rows.
Swap rows2,3 so these are C22,C33. V cannot be at2 or3, where it
would have at most two grid neighbors. If V=1, its full degree forces
edges to L,X and one column3 grid vertex. Now neither X nor V can
meet C13, by quadrangles through U,A1 and L,A1 respectively. C13
must be a middle with a column1 endpoint at3 and no exterior neighbor.

If V=4, B2=3 because U-C22 requires C22=2. C13 has no nongrid
neighbor and must be a middle. The pair {21,32} fails because C32
cannot use U, already adjacent to C22 with the same column, or any
other nongrid endpoint. Thus the path is C22-C13-C31, with C31-V.
C33's remaining neighbor must be C21: C22 is full and every nongrid
choice is forbidden or too far. Hence C33=2,C21=3. C21 cannot meet
V, already meeting C31 in the same column. Its possible further grid
neighbor C32 would repeat row3 along C33-C21-C32, while C13 is full.
Its degree is deficient.

U at1, with U and V adjacent
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The U-V edge forbids U-column2 and V-row1 edges. Degree4 forces
U-X and one column3 grid neighbor; name it C23. If V=1, it cannot
meet L (quadrangle through U,A1), X (triangle through U), or more
than one grid vertex, so has deficient degree. Thus V=2. Its two
grid neighbors must be C21,C33: they are the only distinct-row/column
pair in columns1,3 avoiding U's neighbor C23.

C21=3. Its remaining edge is C13: C33 gives a triangle through V,
and C32 gives a quadrangle through V,B2. Thus C13=2. C13 has no
nongrid neighbor; its other grid neighbor must be C32, since C22
repeats row2 and C31 repeats column1 of C21. The path endpoint C32
cannot meet U,V or L, and can reach the boundary only at1 via X.
Thus C32=1 and A3=B2=2.

C23's remaining edge must be C31, since C32 is full. This forces
C23=2,C31=3. C31 cannot meet U by support, V with its existing
column1 neighbor C21, or any boundary. Its remaining grid edge is
C22. But C22 is at2 or3 from its adjacency to C31 and its parent
B2=2. It has no nongrid neighbor, and cannot meet C33 because that
repeats row3 of C31; C13 is full. Contradiction.

U at2
~~~~~~

U has no boundary neighbor. Its degree forces U-V and two grid
neighbors. The U-V edge forbids U-column2 and V-row1 edges. Swap
rows2,3 so U's grid neighbors are C21,C33. V has index1,2 or3.

If V=1, degree4 forces V-X and V-C23; L is forbidden through U,A1,
and C33 would give a triangle through U. C33 cannot meet L through
U,A1 or X through U,V, and cannot reach the right boundary. Its
remaining grid edge is C22. For C23's remaining extra edge, U is
already full, and C32
would give a quadrangle through V,B2. The boundary choice X would
give a triangle through V, and the right boundary is too far.
Its remaining possibilities are therefore L at C23=1, or C31.

If L--C23 is present, then C23=1 and A2=B3=2. Now C31 has index3
or4. It cannot meet C22, since C22 already meets C33 with the same
parent A3; it cannot meet C23 by layer support. U is full, V at1 and
L,X at0 are too far, and R has its own parent B1. At index3, only
C13 could supply an extra neighbor. At index4, C13 is too far and
only Y=5 could do so. In either case C31 lacks its required two
extra neighbors. The permitted five-cycle L--A1--U--V--C23--L is
not itself called contradictory.

Otherwise C23--C31 is forced, so C23=2,C31=3. C31 cannot meet U
(quadrangle through V,C23), V or a boundary. Its other grid choices
fail: C13 repeats column3 of C23, and C22 already meets C33 in the
same row as C31. Again its degree is deficient.

Finally V=2 or3. Its degree forces two grid neighbors in addition
to U, hence precisely C23,C31. There are no other available pairs
avoiding U's grid neighbors. Consider C13.

If C13=1, it must meet X and a column2 grid vertex E. E cannot
meet a nongrid vertex: L gives a quadrangle through A1,C13, X a
triangle, and U,V are forbidden by B2 and U-V. E must be the middle
of a three-vertex path, with its other endpoint in column1. The
choice E=C22 would have endpoint C31 and form V-B2-C22-C31-V.
Thus the path is C13-C32-C21, with indices1,2,3, and it is full.

For V=3, C23 has no remaining grid neighbor: C31 gives a triangle
through V and C32 is full. Its extra edge must therefore reach a
boundary. Since it is adjacent to V=3, only index4 and a right
boundary neighbor are possible. But C23=4 would require B3=3,
whereas C13=1 requires B3=2. For V=2, C31=3 and must have remaining
grid neighbor C22. C33 must also meet C22: C21 is full, L is
forbidden through U,A1, X through its column3 neighbor C13, and
the right boundary is too far. This gives two neighbors C31,C33
of C22 with common parent A3. Thus C13 cannot be at1.

If C13=2, it has no nongrid neighbor and is a middle with pair
{21,32} or {22,31}. Its column2 endpoint E has no nongrid neighbor
except X, necessarily at E=1; L is forbidden through A1,C13,
U,V by B2 and U-V, and the right boundary is too far. In particular
B2=2. When V=2, every vertex other than B1 has index different
from4: all grid vertices are at most3 (use U,V=2 and B2=2), all
other parents are at most3, and nongrid vertices are at0,2 or5.
This contradicts the nonsingleton layer4.

For V=3, if E=C32, then A3=2,C31=3. C31 needs C22 as its remaining
neighbor, since C13 is full and C23 gives a triangle through V.
C22 is at2 or3, has no nongrid neighbor, and cannot meet C33 with
the same row as C31; C13 is full. If E=C22, C21=3 instead needs
C32 as its remaining neighbor, since C13 is full and C33 gives a
triangle through U. C32 is at2 or3, has no nongrid neighbor, and
cannot meet C23 with the same row as C21; C13 is full. Both cases
are contradictory. This exhausts the last placement.

Conclusion and retained scope
-----------------------------

All placements of the two extras, and all remaining private-vertex
indices within them, are excluded. Seven occupied cells with adjacent
holes are therefore impossible at six-layer mass21, subject to review
of this proof. Together with the separate eight-cell and disjoint-hole
lemmas, this would leave only m=5,6 at equality21. Those cases remain
unresolved here. In particular the accepted global bound stays21 until
the other cases have their own proofs; no source, branch or enumeration
credit is acquired by this proposal. The existing Moore, adjacent-ball
and BFS source attribution is retained. No novelty or Lean claim is made.
