Excluding equality in the six-layer mass bound
=============================================

Status: proposed elementary theorem, pending distinct proof review.

Let G be simple, four-regular, and of girth at least five. Six consecutive
BFS layers, each nonsingleton, have total size at least TWENTY-ONE.
The stronger bound twenty-two is not proved. The conclusion below leaves
the no-singleton stratum and three singleton patterns possible at order94.

The acquired six_layer_mass_bound.rst already proves a lower bound of20.
We exclude equality by a finite handwritten case distinction. A separately
bounded solver diagnostic suggested one of the contradictions, but its
unverified UNSAT result is NOT a premise of this proof.

Common notation and elementary restrictions
------------------------------------------

Number the six original layers 0,...,5, locally. Take adjacent geodesic
centres u in layer2 and v in layer3, with other neighbors A1,A2,A3 and
B1,B2,B3 respectively, numbering so A1 is in layer1 and B1 in layer4.
The union of their seventeen-vertex radius-two balls consists of:

* u,v and the six A/B vertices;
* m common second neighbors Cij, with parents Ai,Bj;
* one private U-vertex at Ai for every missing cell ij;
* one private V-vertex at Bj for every missing cell ij.

All listed vertices are distinct, except that an occupied cell represents
one common vertex. A repeated pair of parents would make a quadrangle.
The union has 26-m vertices. Cell11 is missing because its parents have
layer difference three, so m<=8. With total20, only m=6,7,8 remain: the
number of vertices outside the union is respectively0,1,2. Every u,v,A,B
vertex already has degree4 in the displayed union. Thus none admits a
further edge. All grid vertices lie in layers1,...,4 and have precisely
two additional neighbors besides their two parents.

The following rules will be used explicitly throughout.

(i) A vertex OTHER THAN the common parent cannot be adjacent to two
    grid vertices with the same row or column: together with their
    common parent this gives a quadrangle. Parent vertices themselves
    are literal exceptions; they already have all four prescribed
    neighbors and cannot be used for any additional edge. A private vertex cannot be adjacent to a grid vertex
    sharing its own parent, because that gives a triangle.

(ii) In the graph induced by the grid vertices, each vertex has degree
     at most two and every component is a path on at most three vertices.
     Along a path of three vertices, both row and column labels are
     distinct, by triangles and quadrangles through a parent. A fourth
     vertex would have to repeat BOTH labels of the first, impossible.
     Cycles are excluded by girth or by containing such a four-vertex
     path. Omit the two prescribed parent edges at each grid vertex
     when counting additional incidences. Each grid path then has exactly
     two additional incidences to nongrid vertices. Their endpoints
     cannot be parent vertices, which are already saturated. These two
     incidences have different endpoints outside the path: a repeated endpoint gives a triangle, quadrangle, or,
     for a one-vertex path, a repeated edge.

(iii) Only private U-vertices can be in layer0 within the union; only
      private V-vertices can be in layer5. Every A is in layers1..3,
      every B in layers2..4. All other support claims below follow from
      the rule that an edge changes the original BFS index by at most1.

These arguments use support and full interior degrees only. Exchanging
u and v and reversing the six indices is therefore legitimate, without
assuming that reversed original layers themselves form a BFS partition.

Eight occupied cells
--------------------

The missing cell is11. The union has18 vertices, and contains at most
one vertex in either boundary layer: private U at A1, and private V at
B1. The two extra vertices must therefore be X in layer0 and Y in layer5.
Both boundary layers have exactly two vertices. Write U,X for the left
pair and V,Y for the right pair.

Every grid path has its two exterior incidences in these four vertices.
They cannot go to opposite ends: its endpoint grid vertices would then
have indices1 and4, although a grid path has at most two edges. Thus a
path attaches once to each of U,X, or once to each of V,Y. A left path
has every vertex in layers1..2; a right path has every vertex in layers3..4.

The grid vertices C12,C13 are adjacent to A1 in layer1, so are in left
paths. They cannot lie on the same grid path, by their common row and
rule(ii). Each such path has at least two vertices: a one-vertex path
would require adjacency to U, whose parent A1 they share. Similarly
C21,C31 force two different right paths of at least two vertices each.
There are only eight grid vertices. Hence these are exactly four paths
on two vertices. Both C12,C13 must attach to X, not U. This makes the
quadrangle A1-C12-X-C13-A1, a contradiction.

Seven occupied cells
---------------------

There are two missing cells and one extra vertex X. The missing cells
share a row or a column. To see this, at least one boundary layer contains
no X. If it is layer5, both private V vertices lie there. Every occupied
cell between A1 in layer1 and either corresponding B-parent in layer4
is forbidden. If the two holes use distinct columns, both holes must
therefore be in row1; otherwise they already share a column. Reverse the
support argument if the boundary without X is layer0.

By reversal take the missing cells as11,12. A1 has both private U
vertices; B1 and B2 each have one private V vertex.

First suppose X is in an interior layer. Both U vertices are in layer0
and both V vertices in layer5. Thus A1 is in layer1 and B1,B2 in layer4.
All grid vertices in columns1,2 have index at least3. A2,A3 have index
at least2. The only possible additional layer1 vertices are X or grid
vertices in column3. Such a grid vertex has no grid neighbor in layers
at most2, and at most one U-neighbor, because the U vertices share A1.
It cannot have degree4 without an X-neighbor. If X is in layer1, X
itself can have at most one U-neighbor and one column3 grid neighbor,
so has degree at most2. If X is in layer2, it can meet only grid vertices,
at most three by rule(i), so has degree at most3. If X is in layer3 or4,
it cannot rescue any layer1 grid vertex. All alternatives contradict
the full interior degrees or the nonsingleton first interior layer.

Next suppose X is in layer0. Both V vertices are in layer5, hence B1,B2
in layer4. At least one U is in layer0, hence A1 in layer1. C13 cannot
be in layer1: besides its two saturated parents it could meet only X;
the U vertices share its parent A1, the other column3 vertices share B3,
and columns1,2 start at index3. Therefore C13 is in layer2. Its other
two neighbors must be grid vertices, one in each of columns1,2 and
different rows, both necessarily in layer3. They form with C13 a full
three-vertex grid path. Each endpoint requires a nongrid neighbor by(ii).
At index3 it cannot meet X or the layer0 U, or either layer5 V. The
only remaining possibility is the other U, if that U is interior.
Both endpoints cannot meet the same U, by(ii). Contradiction.

Finally suppose X is in layer5. Both U vertices lie in layer0, so A1
is in layer1. At least one V lies in layer5; relabel columns1,2 so that
it is the B1-private vertex. If the other V also lies in layer5, the
column3 layer1 argument above already gives a degree deficit. Otherwise
write V for that interior B2-private vertex. Here B1 is in layer4,
A2,A3 have index at least2, and B3 has index at most3 because C13 meets A1.

V has at most two grid neighbors, in columns1 and3. Its remaining
possible neighbors are boundary vertices (all U in layer0 and the other
V and X in layer5). Full degree therefore puts V in layer1 or4.
It cannot be in layer1: grid column1 starts at index3, at most one grid
neighbor is available in column3, and at most one U-neighbor is possible.
Thus V is in layer4 and B2 has index at least3.

The only layer1 candidates other than A1 are C13,C23,C33. C13 can have
at most one additional neighbor (a column2 grid vertex), hence is not
in layer1. If Ci3 with i=2 or3 were in layer1, its two additional
neighbors would have to be a U and Cj2 in the other row. The latter
has index2. It cannot acquire a further grid neighbor: C13 would repeat
column3 along a three-vertex path, and Ci1 would repeat row i; the other
possibilities share its own row or column. It cannot meet a boundary
vertex from index2, or V, whose parent B2 it shares. Its degree is at
most3. Thus layer1 is a singleton, the final contradiction for m=7.

Six occupied cells: missing-cell classification
------------------------------------------------

The two-ball union is now the entire twenty-vertex interval. There are
three private U vertices and three private V vertices. Let R be the
rows whose A-parent is in layer1, and C the columns whose B-parent is
in layer4. At least two U vertices in layer0 have parents in R, and at
least two V vertices in layer5 have parents in C. Every cell in R x C
is missing. There are only three missing cells. Thus R and C cannot
both have two members. Classifying the three missing edges of this
bipartite row-column incidence gives, up to row/column relabeling and
reversal, precisely:

  star:        11,12,13;
  disjoint:    11,12,23;
  L-shape:     11,12,21.

For completeness, if R and C each have one member, both that row and
that column need at least two holes, giving the L-shape. If one has
two or three members and the other one member, their forced rectangle
uses two or three holes in a single row/column; the possible third hole
gives exactly the displayed star, disjoint shape or L-shape. Three
disjoint holes cannot supply two private boundary vertices on both sides.

The star
~~~~~~~~

Take holes11,12,13. All U vertices share parent A1 in layer1. At least
two B-parents, say B1,B2, are in layer4. Consequently A2,A3 have index
at least2, grid columns1,2 start at index3, and the only possible extra
layer1 vertices are grid C23,C33, the third U, or the B3-private V.

A column3 grid vertex in layer1 has no possible grid neighbor there
or in layer2 (other columns start at3); it cannot meet the B3-private
V, and can meet at most one U. Its degree is at most3. A U in layer1
cannot meet another U, can meet at most one column3 grid vertex, and
can meet at most the one B3-private V. Its degree is at most3. A B3-private
V in layer1 has no grid neighbor (its other possible columns start at3)
and at most one U-neighbor, so also has deficient degree. Thus layer1
would be a singleton. This excludes the star and its reversal.

The disjoint shape
~~~~~~~~~~~~~~~~~~~

Take holes11,12,23. The two row1 private vertices must be in layer0,
and the private vertices of columns1,2 in layer5. Indeed a second A
parent in layer1 or a different pair of B parents in layer4 would
require another missing cell. Thus A1 is in layer1, B1,B2 in layer4,
A2,A3 have index at least2, and B3 has index at most3. Write U for the
interior A2-private vertex and V for the interior B3-private vertex.
The grid is 13,21,22,31,32,33.

The layer1 candidates besides A1 are C13,C33,U,V. C13 can have at most
the one additional neighbor U; its two parents forbid the other private
vertices, and grid columns1,2 start at3. Hence it is not in layer1.
If U were in layer1, its other three neighbors would have to be one
left boundary private, one grid vertex in column3, and V: at most one
of each is possible. But the grid neighbor and V both have parent B3,
giving a quadrangle through U. If V were in layer1, its grid neighbors
in columns1,2 would be unavailable; at most one left private and U
could supplement its parent, again insufficient.

If C33 were in layer1, its two additional neighbors would have to be
U and one left boundary private. U is then in layer2. Once adjacent to
C33, U cannot have another grid neighbor: C13 shares B3 with C33;
C31,C32 share A3 with it; C21,C22 share U's own parent A2.
At index2 it cannot meet either boundary. Apart from its parent and
C33, only V is available, so its degree is at most3. All layer1
candidates are excluded.

The L-shape with two late B-parents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take holes11,12,21. A1 is necessarily in layer1 and B1 in layer4.
The only possibilities for (R,C) are ({1},{1}), ({1},{1,2}), and its
reversal ({1,2},{1}). First take ({1},{1,2}). The two A1-private vertices
are in layer0. B1,B2 are in layer4. The other private U has parent A2;
at least two of the three V vertices are in layer5. The remaining V
may have parent B1 OR B2; if interior it has index3 or4, since both
possible parents are in layer4. No choice of its parent is assumed.
The grid is

  13,22,23,31,32,33.

All grid columns1,2 start at3. The possible additional layer1 vertices
are C13,C23,C33,U. U in layer1 has at most one boundary-private neighbor
and one column3 grid neighbor besides its parent, so is impossible.
C13 in layer1 has at most U as an extra neighbor; C23 has at most one
left private, since U shares its parent A2. Neither has degree4.

C33 in layer1 would have to meet U and a left private. Then U is in
layer2, and cannot meet any other grid vertex, by repeated row/column
parents with C33 or its own parent A2. Neither boundary is adjacent to
index2. Apart from its parent and C33, only the possibly interior V
is available, giving degree at most3. This contradiction excludes
({1},{1,2}); reversal excludes ({1,2},{1}).

The L-shape with one parent at each extreme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It remains that R=C={1}. The two A1-private vertices lie in layer0,
the two B1-private vertices in layer5. Write U for the A2-private
vertex and V for the B2-private vertex; both are interior. Now

  A2,A3,B2,B3 lie in layers2 or3;
  C13 has index at most2; C31 has index at least3.

Each of U,V can meet at most one boundary private in total. It cannot
meet two at the same end, since those share a parent, and cannot meet
both ends, whose indices differ by5. Each can meet at most two grid
vertices: U must use distinct rows other than2, V distinct columns
other than2.

Suppose first that U,V are not adjacent. Degree4 forces each to meet
two grid vertices and one boundary private. The possible grid pair for
U is {13,31} or {13,32}; that for V is {31,13} or {31,23}. Because U
meets C13, its boundary attachment must be on the left and U has index1.
Because V meets C31, its attachment is on the right and V has index4.
Support therefore forces U's pair to be {13,32}, V's pair {31,23},
with A2 in layer2 and B2 in layer3.

C13's other extra neighbor is forced to be C31. It cannot use C32
(triangle through U), C22 (quadrangle through U,A2), a left private
(shared parent A1), or the distant right side. Thus C13 and C31 are
full. C22, whose index is2 or3, can meet neither boundary and shares
a parent with each of U,V. Its only remaining available grid neighbor
is C33, although it needs two. Contradiction.

Now suppose U,V are adjacent. A U-neighbor in grid column2 would give
a quadrangle through V,B2; similarly a V-neighbor in row2 would give
a quadrangle through U,A2. For either private vertex the possible grid
neighbors are therefore only {13,31,33}, with the sole possible two-set
{13,31}. The grid neighbor sets of U and V are disjoint, by triangles.
Each has at least one grid neighbor, since it can use at most one
boundary private in addition to its parent and the U--V edge.

If each has one grid neighbor, both require a boundary attachment.
Their adjacency forces these attachments to be at the same end: U,V
are both in layer1 or both in layer4. On the left their distinct grid
neighbors must be13 and33; the vertex using13 makes a quadrangle through
its boundary neighbor and A1. On the right the two choices must be31
and33, and the vertex using31 similarly makes a quadrangle through B1.

Otherwise, by reversal assume U has the two neighbors C13,C31. V has
the one grid neighbor C33 and a boundary attachment. There are two
support possibilities, with identical forced edges:

* If V attaches left, V is in layer1 and U in layer2. B2 is in layer2,
  C31 in layer3, and C33 at index at most2. The only possible additional
  layer4 vertex is C23, so nonsingleton layer4 forces C23 into layer4,
  and A2,B3 into layer3. C23 needs one right boundary neighbor and one
  grid neighbor. It cannot use C31 along with that boundary neighbor,
  since both have parent B1; hence its grid neighbor is C32. C32 is
  necessarily in layer3.

* If V attaches right, V is in layer4 and U in layer3. C13 is in layer2,
  B2 has index at least3, and C33 at least3. The only possible additional
  layer1 vertex is C23; it must be in layer1, forcing A2,B3 into layer2.
  C23 needs one left boundary neighbor and the grid neighbor C32.
  Hence C32 is in layer2 and B2 in layer3.

In either case C32's remaining extra neighbor must be C13. No boundary
is adjacent to its index2 or3; V shares its parent B2, and U would give
a quadrangle through V,B2. Its only other grid possibility is the already
used C23. Thus C13 is full with neighbors U,C32. C23 is full too.
C31 then requires C22 as its other extra neighbor: C13,C23 are full,
V would make a triangle through U, and all boundary choices violate
support or its parent B1. Finally C22 requires C33. Its index is2 or3;
it cannot meet a boundary or U,V, with which it shares parents, and
the alternatives C13,C31 are full/already used. But the edge C22--C33
makes the quadrangle V-B2-C22-C33-V. This exhausts the last case.

All equality cases are excluded. Six consecutive nonsingleton layers
therefore contain at least21 vertices.

Checked consequence for the retained order94 problem
----------------------------------------------------

Replace only the six-layer weight20 by21 in the accepted packing:

  P21(r)=max{17a+21b+2(r-5a-6b): a,b>=0, 5a+6b<=r}.

For r=0,...,17 its values are

  0,2,4,6,8,17,21,23,25,27,34,38,42,44,46,51,55,59.

Keep the same disjoint cap and section supports and replace P6 by P21
in E6,F6 from six_layer_mass_bound.rst. Direct integer substitution in
the five surviving patterns gives

  (4):93; (18):93; (4,9):95; (4,18):93; (13,18):95.

Thus (4,9) and (13,18) are excluded at order at most94. The only
nonempty singleton-index sets still possible under these necessary
bounds are (4), (18), (4,18). With no singleton the bound becomes

  17+P21(17)+17 = 93.

The five substitutions and the eighteen P21 values were evaluated by
literal integer maxima, not graph/profile search. Previously excluded
patterns cannot return because the strengthened weight is monotone.
This does not exclude order93 or94, prove twenty-two, or classify actual
graphs in the remaining strata. The accepted enumeration boundary2030
is not changed and no new root or original receives credit here.

Exact premises, diagnostic and attribution
------------------------------------------

This proof extends the acquired adjacent-ball argument and retains the
Moore/cap/section attribution in its predecessors. No priority or formal
Lean claim is made. The fixed L-shaped diagnostic ran once under the
unchanged small supervisor at60s/256MiB/1MiB output/1GiB reserve; it
returned unverified UNSAT in0.164s, with clean terminal receipt. The
last handwritten case above supplies an explicit independent argument;
the diagnostic's solver result grants no mathematical premise.

Direct files in computation/f009:

* six_layer_mass_bound.rst, SHA256
  f8b2dcf5cd63d52d111da09cbbd59fd389eedc8f25906b6453dd4ab3176fb944.
* six_layer_mass_acceptance.json (ROOT_ACCEPTED_F009_SIX_LAYER_MASS_TWENTY),
  SHA256 a11b029dbfb977ee7b522678f1b6f455b88d8b933350342ed576a5d6a5ce2e19.
* singleton_cap_twenty_acceptance.json, SHA256
  5fb6edbd66754ad5de14e1147606d4bc26e66a296d6fe58f9eea1c91bd4a3280.
* boundary_radius_four_acceptance.json, SHA256
  9e18b21897516cc0632c55bbf6e210eec964b1399cd8df7abb3f15b8a265f0e6.
* six_layer_l_shape_check.py and six_layer_l_shape_request.json
  (request SHA256 d8c878a840a5272651aa40598f365026ad5b24fb71ab743fb142133afd1a5716);
  six_layer_l_shape_result/result.json and six_layer_l_shape_execution/receipt.json.

The earlier proofs, the diagnostic and its outcome remain unmodified.
No further solver, enumeration, production call, build, CURRENT edit,
public-file edit or source registration was performed for this theorem.
