A radius-four boundary ball and the three-singleton obstruction
==============================================================

Proposed proof-only refinement, pending independent review.  This note
uses the accepted cap, singleton-section and singleton-free packing
results.  It excludes a further structural stratum, not every F009
order-94 graph.  No graph enumeration or solver is used.

Local ball lemma
----------------

Let H be a finite connected simple graph of girth at least five, with
every vertex of even degree.  A specified vertex u has degree two;
every other vertex at distance at most four from u has degree four.
Suppose some vertex has distance at least five from u.  Then

  |B_4(u)| >= 19.                                               (1)

These hypotheses apply to an induced cap with boundary u and depth
at least five, and to either boundary of an induced two-boundary
section when the other boundary is at distance at least five.

Write its first five BFS layers as u,A,B,C,D.  The acquired parent
argument gives |A|=2, |B|=6 and B=P union Q, where each parent class
has three vertices.  Edges inside B form a matching of size m<=3.
Every C vertex has one or two B-parents, at most one from each class.
Thus, writing c=|C| and d=|D|,

  e(B,C)=18-2m,  c>=6,  d>=1,  |B_4(u)|=9+c+d.

If (1) fails, the only possibilities are c=6,d<=3; c=7,d<=2;
or c=8,d=1.  All C vertices have degree four and their non-B
neighbors are in C or D.  A D vertex cannot have two C-neighbors
sharing a B-parent, as that would give a quadrangle.  Consequently
the sets of B-parents of its C-neighbors are pairwise disjoint.

Recall two already acquired parent-label facts.  Double-parent C
vertices have distinct labels (i,j) for parents p_i,q_j.  When m=3,
the labels are off-diagonal and these vertices are independent.
A single-parent C vertex has at most two double-parent C-neighbors:
if its parent is p_i, their first coordinates must be distinct and
different from i, by triangles and quadrangles; similarly for q_i.

Case c=6
~~~~~~~~~

Here m=3 and all six vertices are double-parent.  They are independent,
so twelve edges go from C to D.  Their labels are exactly the six
off-diagonal pairs on {0,1,2}.  A D vertex can have at most three
such neighbors.  A three-neighbor set must use all first and all
second coordinates; the only possibilities are

  U={01,12,20},  V={10,02,21}.                                  (2)

Neither set can be used by two D vertices, because two common
C-neighbors would give a quadrangle.  With d<=3, at most
3+3+2=8 edges can go from C to D, contradicting twelve.
In fact the same argument gives d>=5 in this case.

Case c=7, m=2
~~~~~~~~~~~~~~

All seven C vertices are double-parent.  The accepted seven-label
calculation applies: after numbering the two B matching edges 00,11,
the labels are 01,10,02,20,12,21,22 and their only possible edges are

  22--01, 22--10, 02--21, 12--20.                               (3)

Hence e(C)<=4 and e(C,D)=28-14-2e(C)>=6.  Each D vertex has at most
three C-neighbors.  If d<=2, equality is necessary everywhere: d=2,
all four edges (3) occur, and both D vertices have three C-neighbors.
Vertex 22 has no D-neighbor and the other six each have one.  Each
D-neighbor triple must therefore be U or V in (2).  But U contains
the C edge 12--20, and V contains 02--21.  Either produces a triangle
through the common D-neighbor.  This is impossible.

Case c=7, m=3
~~~~~~~~~~~~~~

There are five double-parent vertices and two single-parent vertices
in C.  Doubles are independent; each single has at most two double
neighbors.  At most one edge joins the singles, so e(C)<=5.  Moreover
each D vertex has at most four C-neighbors.  Indeed five C-neighbors
would include at least three doubles, using at least eight distinct
B-parent incidences among only six vertices of B.  If it has four
C-neighbors, exactly two must be single and two double: three doubles
and one single would already require seven distinct B-parents.

Now e(C,D)=28-12-2e(C)=16-2e(C).  If e(C)<=3 this exceeds eight,
contradicting d<=2 and the four-parent bound.  If e(C)=4, both D
vertices must have four C-neighbors.  Each must contain both single
vertices in its neighbor set, which makes a quadrangle.

If e(C)=5, both singles are adjacent and each has two double
neighbors.  These four double neighbors are distinct: a double
adjacent to both singles would form a triangle.  Thus the singles
have no D-neighbors, four doubles have one each, and the fifth
double has two, for six C-to-D incidences.  Both D vertices must
therefore have three double-parent neighbors, whose labels form U
or V.  Equal triples at the two D vertices give a quadrangle;
distinct triples need all six off-diagonal labels, but only five
doubles exist.  This is again impossible.

Case c=8, d=1
~~~~~~~~~~~~~~

Let D={v}.  The cuts into v and from v to later layers are both
nonempty and even: H has even degrees, and a vertex at distance at
least five exists.  Since v has degree four, each cut has size two.
The induced layers u,A,B,C,v consequently form a section with both
boundary degrees two and every interior degree four.  The accepted
gap-four proof in singleton_pattern_bound.rst, section 2, requires
at least seventeen interior vertices, whereas 2+6+8=16.

This use of that proof is local: its argument assumes precisely the
two degree-two boundaries, their distance four, the intervening full
degrees, girth and the parent matching.  It does not require u to
have degree four in H or any properties of vertices outside this
induced section.  Thus it applies to the present section verbatim.
The cases exhaust a putative ball of size at most eighteen, proving (1).

Sharpness for this local statement
---------------------------------

The already independently checked twenty-vertex section has BFS
sizes (1,2,6,7,3,1), both boundary degrees two, and all other degrees
four.  It satisfies the local lemma and has |B_4(u)|=19.  Thus the
lemma cannot be strengthened to twenty under these hypotheses alone.
This is a fragment, not a completed quartic order-94 graph.

Improved section and cap packing
--------------------------------

Now let G satisfy the F009 hypotheses: simple connected quartic,
girth at least five, a root of eccentricity 22, and |G|<=94.  Use
the previously accepted notation

  P(r)=17*floor(r/5)+2*(r mod 5),  P(0)=0,

and old lower bounds E(h) for an end-cap order and F(h) for the
interior between consecutive singleton layers h steps apart.
They are defined in singleton_free_section_bounds.rst.  In particular
middle layers in these applications contain no singleton.

A degree-two radius-four boundary ball has at least nineteen
vertices by (1).  For a section of length h>=8, it is disjoint
from the at-least-fifteen-vertex radius-three ball at the other end.
Their original layer supports leave h-8 whole middle layers.
For h>=9, two radius-four balls are disjoint and leave h-9 such
layers.  Subtracting the two boundary vertices gives

  F*(h)=max(F(h),
            32+P(h-8) if h>=8,
            36+P(h-9) if h>=9).                               (4)

For an end cap of length h>=7, the boundary radius-four ball and
the regular radius-two ball at the far end are disjoint, of sizes
at least nineteen and seventeen.  Their original layer supports
leave h-7 whole middle layers.  Hence

  E*(h)=max(E(h), 36+P(h-7) if h>=7).                          (5)

The reverse ball need not be a union of original layers.  A vertex
within radius a of an endpoint of original index j has index at
least j-a; the corresponding upper support holds at the other end.
This is sufficient for all disjointness and whole-middle-layer
counts.  Distances from a singleton into its section/suffix equal
the original layer difference.  In a first cap the original root
and singleton are distance h apart; in the last cap any last-layer
vertex is distance h from its singleton.  Each regular far-end
radius-two ball is contained in the three original end layers.

Exact consequence for singleton positions
-----------------------------------------

The old proof restricts internal singleton indices to [4,19], gaps
at least four, and at most three singletons.  For their complete
nonempty ordered set s1<...<sk, the same exact partition now gives

  |G| >= E*(s1)+E*(22-sk)+sum(F*(s[j+1]-s[j]))+k-2.            (6)

Direct substitution in the same 214 index sets yields only fourteen
necessary possibilities, compared with the old sixty-six:

  one singleton     lower bound
       4                 91
       8                 94
       9                 94
      13                 94
      14                 94
      18                 91
      19                 92

  two singletons    lower bound
      (4,8)              94
      (4,9)              93
      (4,18)             93
      (4,19)             94
      (13,18)            93
      (14,18)            94
      (14,19)            94

There are no three-singleton possibilities.  For auditability, the
seventeen formerly surviving triples receive the following bounds:

  (4,8,13):96   (4,8,18):96   (4,9,13):96
  (4,9,14):95   (4,9,18):95   (4,9,19):96
  (4,10,18):95  (4,10,19):98  (4,12,18):95
  (4,13,18):95  (4,13,19):98  (4,14,18):96
  (4,14,19):96  (8,13,18):95  (9,13,18):96
  (9,14,18):96  (9,14,19):96.

All other triples were already excluded by the weaker bounds.  Thus
an order-at-most-94 target has AT MOST TWO internal singleton layers.
The fourteen position sets are necessary only; no realizability is
asserted.  Their count is not a count of graphs, enumerator roots or
newly acquired source cases.

The arithmetic used only combinations of at most three indices from
range(4,20), rejecting gaps below four, and formula (6).  For each k,
the old and new surviving counts were respectively (13,36,17) and
(7,7,0).  This is a literal integer table, not a graph/profile search.

Limits, attribution and exact inherited records
-----------------------------------------------

The no-internal-singleton stratum remains untouched: the previous
packing bound is still 89.  The surviving one/two-singleton strata
also remain unresolved.  The local ball bound is sharp, so further
progress needs compatibility beyond one boundary ball, a stronger
singleton-free interval theorem, or another structural argument.
No all-order-94 exclusion or accepted enumeration increment follows.

The new step is the radius-four ball argument and its application
to the already acquired packing formulas.  The parent-label facts,
seven-label adjacency list, gap-four section proof, Moore interval
bounds and their original attribution are reused; no priority claim
for elementary graph arguments is made.  Paths below are relative
to computation/f009; no accepted bytes have been modified.

* singleton_pattern_bound.rst: SHA256
  96dce96a87e04f0b062a2cce34ff059f4824b5329d645600e7cb9e256af846ca.
* singleton_pattern_review.json: 4444 bytes, SHA256
  cf5a9082e2750dd08fa176236f2a42482ff94c6c944311819cb401ec9baa9a41.
* singleton_free_section_bounds.rst: 8760 bytes, SHA256
  652124e2d4a862ab68911977a773ee249559427364350ce19236f97fa730371f.
* singleton_free_section_acceptance.json: 9390 bytes, SHA256
  fab32a5b8e98b33e361b8c894ce1ed2fd1ae9a7ad90ec436594e520627aff829.
* singleton_section_example.json: 2970 bytes, SHA256
  c6f370d7981ea0c44e6a9f0d9c6c09642782049ee5cfd1c1287b85ee466e4691.
* singleton_section_example_review.json: 1568 bytes, SHA256
  7551b617e476d408fcc66d2e7ba5b0424dead4948880d955516833d08a484f9e.

No production, solver, subgroup calculation, graph enumeration, build,
new intake, CURRENT edit or formal Lean verification was performed.
