The eight-cell case at six-layer mass twenty-one
================================================

Status: proposed elementary restriction, pending independent review.

Let G be a simple quartic graph of girth at least five. Suppose six
consecutive original BFS layers are nonsingleton and contain exactly
21 vertices. Choose adjacent geodesic centres u in local layer2 and v
in local layer3. Their radius-two balls cannot have eight common second
neighbors. In the notation below, m<=7.

This excludes only the eight-cell case at equality21. It does not prove
a six-layer lower bound22: the cases m=5,6,7 are still unresolved here.
It is independent of any solver outcome.

Inherited local structure
-------------------------

Use the notation and proved local structure of
six_layer_twenty_equality_exclusion.rst, final SHA256
d80cc0af013665beecd6fbfbdb02d530b399319c17b4824d6de0b5e061ca0d69,
and its root acceptance six_layer_twenty_one_acceptance.json, SHA256
1befdd15630d78611b38c904e86322d0a2234e483f78e1995b048b123e040121.

The other neighbors of u and v are A1,A2,A3 and B1,B2,B3, respectively,
where A1 is in layer1 and B1 in layer4. A grid vertex Cij is adjacent
to Ai and Bj. Its row and column parents are already saturated. When
counting additional edges, omit the two prescribed parent edges at
each grid vertex. The grid-induced components are paths on at most
three vertices. Each such path has exactly two additional incidences
to distinct nongrid endpoints. A third vertex other than the common
parent cannot meet two grid vertices sharing a row or column.

For m=8, only cell11 is missing. There is one private U with parent A1
and one private V with parent B1. The two-ball union has18 vertices;
there are exactly three further vertices in the six-layer interval.
Within the union, only U can lie in layer0 and only V in layer5.
At least one extra vertex must therefore lie at each end. There are
two possibilities: all three extras lie at the boundaries, two on one
side and one on the other; or exactly one extra lies at each boundary
and the third is interior. In the latter case U,V must themselves be
at the boundaries. In the former, the private vertex on the enlarged
side may initially be interior; this is treated separately below.

Boundary-only extras, with the private vertex at the enlarged end
---------------------------------------------------------------

First suppose all three extras are at the boundaries and both U,V are
at their respective boundaries. Up to reversing support, there are
three nongrid vertices at the left and two at the right. No grid path
can have its exterior endpoints at opposite ends: its grid endpoints
would have indices1 and4, whereas the path has at most two edges.

C12 and C13 must belong to left paths, since they meet A1 in layer1;
C21 and C31 to right paths, since they meet B1 in layer4. The two
vertices in each pair are in different grid paths by their shared
parent. At the two-vertex right end, neither C21 nor C31 can meet V,
because of its common parent B1. Only the extra right vertex is
available, and it cannot meet both. Thus at least one of C21,C31 is
the middle of a three-vertex grid path, and the other belongs to a
path of at least two vertices. Right paths require at least five
grid vertices.

At the three-vertex left end, C12,C13 cannot meet U. If neither is an
isolated grid vertex, their distinct paths need at least four vertices.
If one is isolated, its two exterior neighbors are both extra left
vertices. Neither of these can meet the other C1j, by a quadrangle
through A1. The other C1j must then be a middle vertex, requiring a
three-vertex path. The same lower bound four results. Thus at least
nine grid vertices would be required, contradicting m=8.

One extra interior vertex
-------------------------

Suppose one extra X is interior. Exactly one extra lies at each end;
write Y at the left and Z at the right. Now U must lie in layer0 and
V in layer5. If X is in layer2 or3, its only available neighbors are
grid vertices: the parent vertices are saturated and the four other
nongrid vertices lie at indices0 and5. It can meet at most three grid
vertices, by distinct rows and columns, contradicting degree4.

By support reversal it remains to consider X in layer1. Grid column1
has index at least3, so X can meet at most two grid vertices, in
columns2 and3. Its only other possible neighbors are U and Y. Full
degree therefore forces adjacency to both U,Y and two grid vertices.
Neither grid neighbor is in row1, since X-U-A1-C1j-X would be a
quadrangle.

Consequently a row1 grid vertex, if it is an endpoint of its grid
path, can attach only to Y and must lie in layer1. It cannot be an
isolated grid vertex, which would need two distinct exterior endpoints.
At most one of C12,C13 can attach to Y. Their distinct paths therefore
contain at least five grid vertices. Similarly, an endpoint among
C21,C31 can attach only to Z and lies in layer4: V shares its parent,
and X in layer1 is too far. Their distinct paths also require at least
five grid vertices.

The left and right required paths are disjoint. If a row1 and a column1
vertex were both endpoints of the same path, their indices1 and4 would
be too far apart. If the row1 vertex were the middle, its index is at
most2 and the column1 endpoint would be at4, again impossible. If the
column1 vertex were the middle, its index is at least3 and the row1
endpoint would be at1. A path on at most three vertices has only one
middle. Thus at least ten grid vertices would be required.

Boundary extras with an interior private vertex
-----------------------------------------------

Up to reversal, both extra X,Y lie in layer0, the third extra Z is in
layer5, V lies in layer5, and U is interior. Its parent A1 has index1,
so U has index1 or2. At index2 it cannot meet any boundary vertex.
Besides its parent it could meet only grid vertices, at most two
because row1 is forbidden. This gives degree at most3. Hence U is
in layer1.

For row1 grid vertices, the only possible exterior endpoints are now
X,Y: U shares their parent, and the right side is too far. If neither
C12,C13 is isolated, their distinct paths use at least four vertices.
If one is isolated, it uses both X,Y; the other cannot meet either and
must be a middle vertex, again requiring four in total. Their endpoint
indices are1, and their possible middle indices are at most2.

The two column1 grid vertices cannot meet U at index1. An endpoint
among them must meet Z, hence has index4; a middle has index at least3.
As in the two-vertex-end argument, their paths use at least five grid
vertices. The same endpoint/middle support argument in the preceding
section shows that none of these right paths can be one of the left
paths. Thus at least nine grid vertices would be needed. This excludes
the last boundary assignment and completes the m=8 exclusion.

Conditional arithmetic only
--------------------------

If a complete six-layer22 theorem were proved, replacing21 by22 in
the accepted disjoint packing gives no-singleton lower95, singleton
sets (4) and (18) lower95, and the pair (4,18) lower94. These are
literal integer substitutions, not an existence or exclusion claim
for the still-open equality21 cases. No graph/profile search, source
credit or enumeration-boundary change is asserted here.
