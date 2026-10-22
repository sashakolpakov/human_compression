Cyclic defects: two exclusions and an explicit counterexample
=============================================================

Author: /root/readme_navigation_audit, 22 October 2026.

This note continues the separately reviewed five-defect reduction. It is
written mathematics, with an independently specified example and a proposed
finite checker. The checker has NOT been invoked. No current census family,
payload, checkpoint, accepted Source or gate is changed. The example is not
claimed to represent a new ordinary class or a class from the source list.
No historical novelty, conjecture, Lean or completed-census credit is claimed.

1. The three middle neighborhoods
----------------------------------

Retain a connected triangle-free 5-regular graph G of order32, with a
geodesic p_0,...,p_8. Put A=N(p_0), B=N(p_4), C=N(p_8). The previous
argument proves that I=A union B union C is independent, with each block
of size5, and its complement J has17 vertices and exactly five internal
edges F. Write f(v)=deg_F(v), including zero degrees.

Remove p_0,p_4,p_8 from J, leaving a14-point set J'. Let L consist of
the vertices of J' meeting A, R those meeting C, and M all remaining
vertices. A vertex in L intersect R would give a root path of length4,
so these three sets partition J'. No B vertex can meet both L and R:
such neighbors, with an A and a C neighbor, give a root walk of length6.
Let B_L and B_R denote the B vertices meeting L and R, respectively.
They are disjoint and both nonempty: p_3 meets p_2 in L, and p_5 meets
p_6 in R.

There are20 edges from A to L. Indeed each A vertex has its center
neighbor p_0 and four others, all in L. A member of L can have neighbors
only in A, B and J. Therefore

            5|L|=20+|E(B,L)|+sum_{v in L} f(v).          (1)

The B term is positive, so |L|>=5. Symmetrically |R|>=5, and consequently
|M|<=4.

An F-path of length at most3 from L to R is impossible. Appending the
two-edge routes from its ends to p_0 and p_8 would give a root walk of
length at most7. In particular no connected F component of diameter at
most3 can meet both L and R.

For an F edge uv with u,v in M, their I-neighbors all lie in B, with
respective sizes5-f(u),5-f(v). These sets must be disjoint, since a
common neighbor gives a triangle. As |B|=5, this proves

                     f(u)+f(v)>=5.                     (2)

2. A uniform obstruction on one side
------------------------------------

Lemma. Suppose no F edge meets R, and every M vertex of positive
F-degree has an F neighbor in L. Then G cannot satisfy the assumptions.

Proof. Let T be the M vertices of positive F-degree, and t=|T|. A
vertex b in B_R cannot be adjacent to a member v of T: choose its
F neighbor l in L, an A neighbor a of l, an R neighbor r of b, and
a C neighbor c of r. The walk

                      p_0,a,l,v,b,r,c,p_8

has length7, contrary to the root distance. On the other hand every
v in M\T has all five of its neighbors in B, because it meets neither
A nor C and has no F edge. Thus each b in B_R is adjacent to all
|M|-t vertices in M\T and to none in T. It already has p_4 as a
neighbor and has no L neighbor. It therefore has exactly

                         a=4-|M|+t

neighbors in R. This number lies between0 and4. Put b_R=|B_R|;
then1<=b_R<=4, since B_L is nonempty and disjoint from B_R.
Counting at R, which has no F incidence, gives

                       5(|R|-4)=a b_R.                 (3)

Its left side is positive, because |R|>=5. Hence a is one of1,2,3,4.
Neither factor on the right of (3) is divisible by5, a contradiction.

Corollary. Suppose F is connected, has diameter at most3, and every
vertex v of positive F-degree has some F neighbor w satisfying
f(v)+f(w)<=4. Then F is impossible.

Proof. Its small diameter prevents F from meeting both L and R, so
interchange the two ends if necessary to ensure that no F edge meets R.
If a positive-degree vertex v in M had no F neighbor in L, all of its
F neighbors would lie in M. Choosing the asserted neighbor w would
contradict (2). Thus every positive-degree M vertex has an F neighbor
in L, and the lemma applies.

This is a sufficient obstruction, not a classification of all defects.
The proof uses no source graph count, bipartiteness hypothesis, generator
claim or current-family geometry.

3. Which cyclic shape can remain
---------------------------------

Proposition. The five-edge graph F is neither a five-cycle nor a
four-cycle with one pendant edge. If F contains a cycle, it is a
four-cycle disjoint from a single edge.

Proof. In a five-cycle every vertex has degree2, every edge has degree
sum4, and the diameter is2. The corollary excludes it.

For a four-cycle with a pendant edge, the attachment vertex has degree3;
the pendant vertex has degree1; and the other three cycle vertices have
degree2. The attachment vertex and its leaf have each other as a
neighbor of degree sum4. Each other cycle vertex has a cycle neighbor
of degree2, again giving sum4. Its diameter is3, so the corollary
excludes this graph too.

Finally F is triangle-free and has only five edges. A cycle has length
four or five. A five-cycle uses every edge. Given a four-cycle, the
fifth edge is either disjoint from it or pendant on it, unless both
endpoints lie on the cycle. In the latter case it would be a diagonal,
creating a triangle. The two exclusions leave precisely C4 disjoint
union K2.

The same corollary also excludes the five-edge tree with two adjacent
degree-three vertices, each carrying two leaves. Its diameter is3,
and each vertex has a neighbor of degree sum4. This is a further
substantive negative condition; it is not used in the example below.

4. An explicit nonbipartite example with a cyclic defect
--------------------------------------------------------

The companion example.json gives the complete adjacency lists on0..31.
Here is a readable description of the same graph. All sets in this
display are disjoint:

  X={0,6,7};       A_1={1,2};       A_2={3,4,5};
  P={8,9};        Q={26,27};
  B_L={21,22};    B_R={23,24,25};
  Z={20,28,29,30};
  C_1={11,12};    C_2={13,14,15};   Y={10,16,17,18}.

The two remaining vertices are19 and31. Insert all edges between each
of the following listed pairs of sets, and no unlisted edges:

  X--(A_1 union A_2);  A_1--P;  A_2--Q;  P--Q;
  Z--(B_L union B_R);  Y--(C_1 union C_2);
  {19}--C_1;  {31}--C_2.

Add the six edges

              8--22, 9--21, 19--24, 19--25,
                       31--23, 19--31.

The groups A=A_1 union A_2, B=B_L union B_R, C=C_1 union C_2 are
the neighborhoods of0,20,10 respectively. Thus

                I={1..5,11..15,21..25}

is exactly the independent set used by the retained seed reduction.
The induced graph on J has edges

                 8--26, 8--27, 9--26, 9--27, 19--31,

and is C4 disjoint union K2. All25 original seed edges are present,
including9--21 and19--25. The original eight-edge root path is

                   0,1,9,21,20,25,19,11,10.             (4)

Degree proof. Each X vertex has five A neighbors. Each A_1 vertex
has three X and two P neighbors; each A_2 vertex has three X and two
Q neighbors. Each P vertex has two A_1, two Q and its one B_L neighbor.
Each Q vertex has three A_2 and two P neighbors. Each B vertex has
four Z neighbors and one neighbor among P,{19},{31}. Each Z vertex
has five B neighbors. Each C_1 vertex has four Y neighbors and19;
each C_2 vertex has four Y neighbors and31. Each Y vertex has five
C neighbors. Vertex19 has neighbors11,12,24,25,31, and31 has
neighbors13,14,15,19,23. Every vertex therefore has degree five.

Girth proof. The graph has no edge inside I. Its J edges are precisely
the displayed C4 and single edge, so they contain no triangle. Every
remaining possible triangle would use one I vertex and an F edge
between two of its neighbors. But P vertices have I-neighbors in
A_1 union B_L, Q vertices have theirs in A_2, and these sets are
disjoint. The I-neighbors of19 are11,12,24,25, whereas those of31
are13,14,15,23, again disjoint. No triangle exists. The cycle
0,1,6,2,0 has length four, proving girth exactly four. The cycle
0,1,8,26,3,0 has length five, so the graph is nonbipartite.

Connectivity and diameter upper bound. Every vertex is at distance
at most three from some B vertex. On the left, P is distance one,
Q and A_1 at most two, and A_2 and X at most three. On the right,
19,31 are distance one, C at most two, and Y at most three.
Vertices of Z have distance one, and B itself has distance zero.
Every two B vertices have distance at most two through20. Hence
every two vertices of G have distance at most3+2+3=8; this proves
connectivity as well.

Diameter lower bound. Deleting Z separates the component containing0
and B_L from the component containing10 and B_R. From0, reaching
B_L requires at least three edges: its first step is into A, and
no A vertex is adjacent to B_L. The path0,1,9,21 attains three.
From10 the analogous minimum distance to B_R is three, attained by
10,11,19,25. The only way into Z is through B. Thus any path from0
to10 must take at least four edges before its first Z vertex and
at least four after its last Z vertex. Its length is at least eight.
Path (4) attains eight, so the diameter is exactly eight.

Consequently neither a forest restriction nor a star restriction on F
can be used to close the remaining target families. This example does
not assert membership of any accepted unfinished family or source
class list; such membership would require its own actual comparison.

5. Proposed finite check, awaiting Root inspection and grant
------------------------------------------------------------

check_example.py is a short standard-library checker for this one literal
artifact. It imports no project, graph library, GAP or solver. It checks
strict finite labels, five distinct symmetric neighbors per vertex, all
25 seed edges, connectedness, exact girth by edge-deletion distances,
all-pairs diameter, the eight-edge root geodesic, both displayed cycles,
the literal independent set and every induced defect edge/component.
It performs no isomorphism reduction, external class comparison, current
family lookup, native search, census transition or automatic continuation.

Its proposed explicit command is PY -E -B -S check_example.py
--input ABSOLUTE_EXAMPLE_PATH --input-sha256 ACTUAL_SHA
--out FRESH_ABSOLUTE_RESULT_JSON, inside Root's unchanged512MiB/150s
guard. No call or fit claim is supplied here. A successful later check
would certify this one independently specified graph only. Mathematical
review of the two exclusion proofs remains a separate human proof duty.

Attribution
-----------

The girth-diameter census problem and original numerical results retain
the source authors' credit. The old seed, exact family contract and
already reviewed independent-set reduction are borrowed here. Degree
counts, disjoint neighborhoods, divisibility and ordinary finite BFS
are standard arguments. This note supplies the two cyclic exclusions,
their common sufficient obstruction and an explicit counterpattern to
stronger exclusions. It makes no claim of historical priority.
