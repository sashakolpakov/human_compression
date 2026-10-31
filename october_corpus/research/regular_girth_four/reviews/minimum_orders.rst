Independent hand review: girth four and diameter 4r minima
=========================================================

Verdict: supported mathematical proof for integers k>=3 and r>=2.
No mathematical blocker was found. This review concerns the exact frozen
782f154c edition and its stated elementary graph domain. It supplies no
literature novelty, manuscript recovery, Lean or measurement claim.
No graph, Source, enumeration or TeX execution was performed.

The lower bound and prime obstruction
-------------------------------------

For a geodesic of length4r, every subsegment is geodesic. The r+1
neighborhoods N(p_4i) have sizek, are individually independent by
triangle-freeness, and are pairwise disjoint and anticomplete: a common
vertex or crossing edge would shorten a distance4|i-j| to2 or3. Thus their
union I is independent of size(r+1)k. Regularity bounds the crossing edges
by the capacity of its complement, giving n>=2(r+1)k. Equality uses every
complement degree across the cut, so the complement J is independent.

At equality a J vertex can meet only one or two consecutive I blocks;
meeting blocks two apart gives a forbidden length4 shortcut over a length8
geodesic subpath. A vertex meeting one block must meet all its k vertices.
Consequently X_i contains p_4i and is a full twin class, with size x_i>=1.
It has x_i<k, since otherwise X_i and I_i form a separate K_k,k component.
Each vertex of I_i has q_i=k-x_i in1..k-1 remaining neighbors.

An internal I_i vertex cannot meet both adjacent bridge classes: the
resulting length6 walk between z_(i-1) and z_(i+1) contradicts their
distance8. It therefore uses exactly one interface, and both sides are
nonempty by connectedness of the chain of types. For the first bridge,
b=|I_1^-| lies in1..k-1 and the exact incidence count is
k|F_0|=k*q_0+b*q_1. For primek, k divides neither b nor q_1, a contradiction.
The argument requires r>=2 so I_1 is internal. Since every primek>=3 is
odd, the degree sum forces even order, excluding the one-vertex increment
and proving the lower bound2k(r+1)+2. No classification of all equality
interfaces is claimed or needed.

The composite construction
--------------------------

Write k=pq with p,q>=2. Anchor size k-q=q(p-1)>=2 and port parts p and
k-p=p(q-1) are nonempty. Each bridge vertex has (k-p)+p=k neighbors,
and each interior port has k-q anchor plus q bridge neighbors.

On the left, crown incidence gives every row k-1 side neighbors and its
endpoint. Each side vertex gets k-1 rows and exactly one partition port;
each port has q side neighbors. On the right h=k-q+1 is in1..k-1, and the
specified cyclic incidence is simple and h-regular on both sides.
The q-1 groups of p ports each partition the k side vertices into q-sets,
so every right side vertex gains q-1 port neighbors and every port q side
neighbors. Its rows have q-1 endpoint-twin and h side neighbors. All named
vertices therefore have degreek, including the endpoints and anchors.

The two bipartition sizes are both (r+1)k, using the exact endpoint totalq,
two side sets of sizek, (r-1)(k-q) anchors and(r-2)q bridge vertices.
Every side vertex meets a port, every row meets a side, and all pieces
connect to the anchor chain. Bipartiteness excludes triangles; two anchor
members and two ports form an actual four-cycle. Each endpoint is exactly
four from every member of its adjacent anchor, and the remaining endpiece
vertices are within four. This verifies all hypotheses of the metric
argument, including r=2 when there are no interior bridges.

The plus-two construction and metric
------------------------------------

For every k>=3, anchor sizek-1>=2 and port parts k-2 and2 are nonempty.
A singleton interior bridge has 2+(k-2)=k neighbors. Every port has its
one endpiece/bridge neighbor and k-1 anchor neighbors.

On the left the omission multiset has k-1 copies of x and one of y.
Thus x has one row, the edge and k-2 ports; y has k-1 rows and the edge;
all other side vertices have k rows. No row contains both endpoints of
that side edge. On the right the omission counts are two for y, one for
each of the other k-2 leaves, and zero for f. Thus w has k-1 star edges
and its port; y has k-2 rows, its star edge and its port; every other leaf
has k-1 rows and the star edge; f has k rows. All row and endpoint degrees
also equal k. No row meets w, and no port meets both ends of a side edge,
so no triangle is introduced. Anchor/port four-cycles give girth exactly4.

The radius checks are valid at the smallest k=3: the k-2 remaining leaf
and the k-2 rows meeting y are still nonempty. The left row omitting y
is a length3 route from its anchor and gives a length4 route to its
endpoint and each other side vertex. On the right a row meeting y gives
length4 routes to f and its endpoint; rows omitting y meet another leaf
and have length4 routes through w. Every endpoint has distance exactly4
because any route must follow endpoint,row,side,port,anchor.

Deleting each full anchor class separates its left and right pieces.
Adjacent anchor classes have exact distance4; all named vertices of the
constructions are distinct except the specified piece boundaries. Hence
the two specified endpoints have distance4+4(r-2)+4=4r. The upper bounds
in the metric lemma cover same-endpiece pairs (<=8), opposite-endpiece
pairs (<=4r), remaining pairs (<=4r-4), and mixed pairs (<=4r-2).
No extra side edge joins different pieces. Counting the plus-two
construction gives (r+1)k row/port vertices and(r+1)k+2 remaining vertices.
Thus it attains the prime lower bound, while the composite construction
attains equality. This proves the stated minimum theorem with exact
girth and exact diameter, rather than merely triangle-freeness or a
diameter lower bound.

Ancillary quartic statement and scope
-------------------------------------

The cited diameter-eight precursor was also read. At k=4 equality forces
q=2, two anchor twins and two eleven-vertex components. Each has exactly
two intrinsic degree-two ports. Their two-subsets P,Q of a four-set force
all row omissions through beta, so their intersection size0,1,2 gives
three ordinary half classes. This size is the number of common port
neighbors and remains intrinsic under endpoint changes. The full graph
centre is exactly the two anchors, and deleting it recovers the two
components. There is no attachment alignment because all ports meet both
anchors. The six unordered pairs of three half classes therefore give
the quoted separate six-class consequence. This finite hand argument is
not an executed census, nor a proof of any other ordinary class count.

Optional wording clarifications, with no effect on the minimum proof:
state 'integers k and r' explicitly in the main theorem; say the minimum
triangle-free cycle order is8r in the k=2 aside (C_(8r+1) has the same
diameter); and make disjoint named pieces explicit if the metric lemma
is reused as a stand-alone abstract gluing statement. The actual
constructions already prescribe distinct named sets, so no application
gap results. Independent Root review/adoption is still required before
using the draft as an accepted pruning or intake theorem.
