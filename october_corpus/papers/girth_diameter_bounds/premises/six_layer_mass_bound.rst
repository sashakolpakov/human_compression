Twenty vertices in six nonsingleton distance layers
===================================================

Proposed elementary local lemma and packing consequence, pending distinct
review. The stronger target twenty-two is NOT proved here. The present
twenty bound uses full local degree compatibility, repairing the gap in
the earlier adjacent-ball suggestion. It reduces the existing twelve
necessary singleton-position sets to five, without excluding all F009
graphs of order at most94.

Local theorem
-------------

Let G be connected, simple, four-regular and of girth at least five. Any
six consecutive BFS layers from a fixed root, each containing at least
two vertices, contain at least twenty vertices in total.

Number the six layers locally L0,...,L5. Take six consecutive vertices
of a root-shortest path through them, and denote its adjacent middle
vertices by u in L2 and v in L3. Write A={A1,A2,A3} for the other three
neighbors of u, and B={B1,B2,B3} for the other three neighbors of v,
with A1 in L1 and B1 in L4 on the chosen geodesic.

Both radius-two balls have seventeen vertices and are contained in the
six layers. Their intersection contains u,v,A,B. Every additional common
vertex is a unique Cij adjacent to Ai and Bj. It cannot have two A-parents
or two B-parents, by quadrangle-freeness. No A--B edge exists, since that
would make a quadrangle through u,v. Thus there are m occupied cells in
a3-by-3 grid and

  |B2(u) union B2(v)| = 26-m.                                  (1)

For each missing grid cell in row i there is one private second neighbor
of u, adjacent to Ai; for each missing cell in column j there is one
private second neighbor of v, adjacent to Bj. All these private vertices
are distinct within and across the two sides. This follows from the
seventeen-vertex ball counts; a vertex on both sides would be an occupied
grid cell. There are 9-m private vertices on each side.

Cell11 is missing: a common neighbor of A1 in L1 and B1 in L4 is impossible
because an edge changes BFS index by at most one. Hence m<=8. If m<=6,
the union (1) already has at least twenty vertices. To exclude a total
of at most nineteen, only m=7,8 need consideration.

Eight occupied cells
~~~~~~~~~~~~~~~~~~~~

The union has eighteen vertices and only one private vertex on each side.
Its only possible vertex in L0 is the private u-side vertex. Indeed A is
in layers1..3, B in layers2..4, and every grid vertex is adjacent to a B
vertex of index at least2. Symmetrically its only possible vertex in L5
is the private v-side vertex. Since L0 and L5 each have at least two
vertices, at least two additional vertices outside the union are needed,
one in each layer. This gives at least twenty vertices.

Seven occupied cells
~~~~~~~~~~~~~~~~~~~~~

Here the union has nineteen vertices. If the six layers had total at most
nineteen, they would equal this union. Both private u-side vertices must
lie in L0, and both private v-side vertices in L5. Hence every row
containing a missing cell has its A-parent in L1; every column containing
a missing cell has its B-parent in L4. Every intersection of those rows
and columns must then be missing. With only two missing cells, they must
share a row or a column. The following argument uses only full degrees
and adjacent-layer support, not an assumption that reversed layers form
a BFS partition. It is therefore symmetric under exchanging u,v and
reversing the six indices; take the missing cells to be11 and12.

Thus A1 is in L1, B1,B2 in L4, and the private vertices U1,U2 adjacent
to A1 are the entire L0. The other A-vertices are in layers at least2,
because they have grid children adjacent to B1/B2. B3 also has index at
least2, as it is adjacent to v in L3. Consequently the only possible
L1 vertices besides A1 are C13,C23,C33. Since L1 is nonsingleton, one of
these Ck3 must lie in L1. It already has its two grid parents Ak,B3.
Its only possible additional neighbors in the nineteen-vertex union
are U1,U2, for the following reasons:

* Every A/B vertex and u/v already has all four neighbors in the two-ball
  union, so none can supply a new incidence.
* The other vertices in column3 share B3 with Ck3, so adjacency to them
  would make a triangle.
* All grid vertices in columns1,2 lie in layers at least3, since B1,B2
  are in L4. They cannot be adjacent to Ck3 in L1.
* The private v-side vertices lie in L5.

For k=1, neither U-vertex is possible because it shares parent A1 with
C13, making a triangle. For k=2 or3, at most one is possible: joining
both makes a quadrangle through their common neighbor A1. Thus Ck3 has
degree at most three, contradicting degree four. These categories exhaust
the union. Notice that this argument allows the extra Ui--Ck3 edge that
invalidated the earlier claim that L1 must be a singleton; it is precisely
that vertex's remaining degree which now gives the obstruction. No forward
neighbor for an arbitrary original layer vertex was assumed. This proves
the theorem in the column case as well as the row case.

What remains of the stronger twenty-two target
----------------------------------------------

The proof does not rule out total twenty or twenty-one. By (1), the
remaining possibilities for (occupied cells, vertices outside the union)
are

  total20: (6,0), (7,1), (8,2);
  total21: (5,0), (6,1), (7,2), (8,3).

These pairs are not feasible graph claims. Each still requires compatible
BFS placement, all interior degrees four and no triangles/quadrangles.
The earlier fixed nineteen-vertex layer assignment is incomplete, so it
is not a counterexample to twenty or twenty-two. In particular the proof
above must not be extended by silently treating all grid-layer assignments
as the one illustrated in that earlier discussion. A universal bound22
still needs an argument covering the remaining configurations, or an
actual completed local counterexample. No such classification or search
was performed here.

Packing consequence for the existing F009 problem
--------------------------------------------------

For r consecutive nonsingleton original layers define

  P6(r)=max {17a+20b+2(r-5a-6b): a,b>=0 integers,5a+6b<=r}.     (2)

Partitioning into a five-layer blocks, b six-layer blocks and the remaining
single layers proves this bound. Five-layer mass17 is the previously
acquired Moore bound; six-layer mass20 is the theorem above. This does
not assert simultaneous realizability or sharpness of any partition.
For r=0,...,17 the exact values are

  0,2,4,6,8,17,20,22,24,26,34,37,40,42,44,51,54,57.

Reuse the accepted disjoint cap/section ball supports from
singleton_free_section_bounds.rst and boundary_radius_four.rst, replacing
their weaker P by P6. With the acquired cap minimum20, define

  E6(h)=max(20,
            26+P6(h-5) if h>=5,
            32+P6(h-6) if h>=6,
            36+P6(h-7) if h>=7).

For consecutive singletons h layers apart, put F6(4)=17, F6(5)=18,
and, for h>=6,

  F6(h)=max(22+P6(h-6),
            28+P6(h-7) if h>=7,
            32+P6(h-8) if h>=8,
            36+P6(h-9) if h>=9).

Every middle interval to which P6 is applied contains no singleton by
the definition of consecutive/first/last singletons. The same exact
partition for their full set s1<...<sk gives

  |G|>=E6(s1)+E6(22-sk)+sum_j F6(s[j+1]-s[j])+k-2.            (3)

No ball support or boundary overlap has changed; only the lower bound
for the disjoint whole middle layers is strengthened.

Literal substitution into the twelve remaining necessary sets yields

  set       bound           set          bound
  (4)        92             (4,8)          95
  (8)        95             (4,9)          94
  (9)        95             (4,18)         93
  (13)       95             (13,18)        94
  (14)       95             (14,18)        95
  (18)       92
  (19)       95.

Thus only (4),(18),(4,9),(4,18),(13,18) survive this necessary test at
total order at most94. Previously excluded sets cannot reappear because
P6 dominates the earlier P and all formulas are monotone. The tiny integer
calculation used only (2) and these twelve fixed substitutions, not graph
states, scalar-profile variables or a solver.

With no internal singleton, the first/last three layers each have mass
at least17, and the seventeen middle layers give

  |G| >= 17+P6(17)+17 = 91.

This improves the earlier89 but does NOT exclude order94. Likewise the
five surviving position sets remain unresolved. Neither the twenty-two
claim nor full F009 source completion is acquired by this note.

Exact premises, attribution and scope
-------------------------------------

Root proposed the adjacent-radius-two grid route and the stronger
twenty-two target. The present degree-completion repair and its twenty
bound are by finite_recoveries. The radius-two/Moore and earlier packing
arguments are reused with their retained attribution; no historical
novelty claim is made. Paths below are relative to computation/f009.

* layer_profile_inequalities.tex,4971B,SHA256
  292a51e062e5200192decd73b5f3ccd14374e3d05bc015f83b40425ca80ba337.
* singleton_free_section_bounds.rst,8760B,SHA256
  652124e2d4a862ab68911977a773ee249559427364350ce19236f97fa730371f.
* singleton_free_section_acceptance.json,9390B,SHA256
  fab32a5b8e98b33e361b8c894ce1ed2fd1ae9a7ad90ec436594e520627aff829.
* boundary_radius_four.rst,11672B,SHA256
  8f9a2fbbeb527720b78d92593415283b5daeb4e0bbdda607894789271b4c2b68.
* boundary_radius_four_acceptance.json,6448B,SHA256
  9e18b21897516cc0632c55bbf6e210eec964b1399cd8df7abb3f15b8a265f0e6.
* singleton_cap_twenty_bound.rst,11536B,SHA256
  7be002e562fb751e1e059b5c94471c2a80ae8526a44b2fe429e49f86e60886b5.
* singleton_cap_twenty_acceptance.json,2694B,SHA256
  5fb6edbd66754ad5de14e1147606d4bc26e66a296d6fe58f9eea1c91bd4a3280.

No scientific process, graph/profile enumeration, solver, build, new
executable, source registration or CURRENT edit was performed. Frozen
earlier proofs and failed/incomplete computational evidence are preserved.
