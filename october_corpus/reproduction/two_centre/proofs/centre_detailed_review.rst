Independent written mathematical review
========================================

Reviewed frozen edition
-----------------------
The proof is centre_decomposition.tex, 18,534 bytes, SHA256
25987bb9eb742cbc1b8e779408dec9823a99e3a4704e3eadb4f3d6735aa73a3d.
The scope is NONBIPARTITE, simple, connected, quintic graphs on 32 vertices,
of girth four and diameter eight, with the retained fixed geodesic setup.
The twenty-four-row classification, positive side-column incidences and
its radius-four proof are imported from 522af65b. The strict H16 proof is
1588351c. The empty/singleton and all-isolated centre facts are imported
from 76a5c09c, independently reviewed at 026a34a5. The new argument is not
asserted for the bipartite residual-star stratum.

Verdict: supported written mathematical theory, with no substantive gap.
No represented Source, graph, state, gzip, TeX or control was executed.

The centre
----------
The diameter-eight endpoints imply that any vertex within three of one
endpoint has distance at least five to the other. This excludes endpoint
rows, side vertices, side ports and every middle vertex with a side
neighbor. The only possible additional centres are therefore B0 and the
neutral leaves in a middle-edge row. X consists of midpoint false twins.

For a no-middle-edge row with B0, a B0 vertex y meets all middle vertices
and the midpoint. When each side has a middle neighbor, all side ports
are at distance at most two. On a five-vertex edgeless side the support
of middle/port incidences has at least two vertices: the total deficit
is five and every single deficit is at most four. Every four-element
endpoint row meets this support. A side vertex outside the support meets
all endpoint rows, including a row through a middle-supported vertex.
These observations give distance at most four to every vertex and the
endpoint. In an internally edged side j=2 or 3, all middle support is on
one edge endpoint and port support on the other; the three isolates
meet every endpoint row. The same bound follows. The only exception is
j=1: y has neighborhood X plus u on the opposite side. Each X vertex
is distance four from the empty-middle side endpoint and u is at least
five away. Thus y has eccentricity five and is excluded.

For a neutral middle leaf v, its neighborhood is u plus B minus a.
Hence u has distance one, a distance two, the other ports distance one,
and X and the other neutral leaves distance two. The side-star leaves
are at distance two. When there are at least two such leaves every
four-subset row contains one. With only one star leaf, a row omitting
it contains all four other side vertices and in particular an a-neighbor,
so it is still within four. A side vertex with neither port nor residual
support sees all five rows, one of them already within three. The
opposite six-side or five-side radius argument applies because all its
ports meet v and its possible positive middle vertex is within two.
This treats the r=3 case, rather than assuming at least two star leaves.
The full centre is the independent union X and these neutral leaves.
Their neighborhoods differ by a versus u, so they are two distinct
full-graph false-twin classes.

The component table
-------------------
Deleting the centre leaves each endpoint joined to its five endpoint
rows and every side vertex joined to at least one such row. Remaining
ports have positive side arity, and each remaining middle vertex has a
side neighbor. The exceptional noncentral B0 at j=1 has only the one
remaining middle neighbor and stays in that side. There is no cross
edge in the retained port tables. Thus there are exactly two connected
components. The sizes follow by adding endpoint + five rows + side
vertices + remaining side ports + remaining middle vertices.

I independently obtained: q2 (14,16); q3 no-middle (17-d,12+d);
q3 middle (13,16); q4 middle with opposite side edge (14,14);
q4 middle with opposite middle edge (13,16); Q1 (13,16), Q2 (14,15),
Q3 (13,14), Q4 (13,16), Q5 (14,14), Q6 (13,14), Q7 (13,16);
side-edge j1 (14,14), and j2/j3 (14,13). Every component is at most16.
The listed centre types have at most five vertices and two twin classes.
The table does not create disjoint ordinary classes merely because its
rows differ. The retained all-isolated strata have centres X of sizes
2,3,4 and also satisfy the stated small-component property.

A complete ordinary invariant
-----------------------------
An ordinary isomorphism preserves eccentricity and therefore the centre.
It preserves equality of FULL open neighborhoods and hence the centre
twin classes. Record their sizes and the between-class adjacency bit.
Every outside vertex meets all or none of each twin class, so its
one/two-bit boundary color is exact. Complete colored canonical codes
for the two connected components, sorted as a pair, reconstruct all
remaining edges and all edges to the centre. This proves the converse,
not just invariance. Class size order is forced when unequal; when
equal there are only two global coordinate choices. The same swap must
be applied to BOTH components. Minimizing each component under its own
swap would lose an alignment invariant and is explicitly forbidden.
No assertion is made that a proposed colored-GI implementation already
fits any runtime envelope. An implementation still needs full witnesses.

The enlarged right-half domain
------------------------------
A zero side-column has d+beta=5, beta<=3, hence d>=2. K1,3 and P3+K2
have only one candidate; the matching has none. The two candidates in
P4 are adjacent and would have to belong to every port row if both
were zero, contradicting independent port rows. Thus there is at most
one zero. Its degree is three with two incident ports or degree two
with all three incident ports. Deleting it gives exactly the q2 degree3
or degree2 incidence type, including both possible placements of the
remaining side edge in the degree2 case. The other six side columns
are positive. All ports meet a positive column, and the exceptional
column meets ports; hence the half is connected.

The original endpoint remains eligible after dropping positivity. Every
eligible alternative endpoint is among the thirteen intrinsic degree5
vertices; its five neighbors avoid the ports and give a seven-vertex
side with three edges by the unchanged degree count. With at most48
side maps there are at most624 candidate tuples. Exhausting these roots
and side maps, retaining complete reconstruction/witnesses, gives the
ordinary unrooted half invariant. The exceptional zero vertex must not
be added as an artificial invariant color.

For strict/zero disjointness, use a zero presentation p,A,S,u. The vertex
u meets ports and cannot be a strict root. A side vertex touching a port
or u fails the required no-port-neighbor condition. An unported side
edge cannot have both endpoints unported: their row-incidence sum would
exceed the five independent rows. Any remaining unported side isolate
is a false twin of p and still leaves u zero. A candidate old row a has
new neighbors p plus four of the six ordinary side vertices; the two
omitted side vertices can meet this new neighbor set only across the
single remaining side edge, so at least one remains a zero column.
All thirteen degree5 vertices are covered. Therefore no zero half has
a strict presentation. This establishes disjointness of ordinary half
classes, rather than just of marked inputs.

The complete nonbipartite two-twin-centre stratum
-----------------------------------------------
The retained empty case is impossible. The singleton case has centre2,
all-isolated q2/q3 have centre3/4, and all-isolated q4 is impossible.
The new centre table leaves exactly the q2 nonisolated rows in addition
to the singleton case. After deleting the two-centre class, orders14/16
and port counts2/3 distinguish the two half roles intrinsically. The14
half is one of the six retained forms. The16 half is exactly the enlarged
nonnegative-column domain. Conversely these half pairs are feasible by
the retained singleton/q2 construction and radius proofs. Every port is
joined to both centre vertices, leaving no port matching or centre-label
choice. Ordinary isomorphisms are therefore exactly products of the two
half isomorphisms. This proves the six-times-extended-H16 identity.
It does not numerically evaluate the enlarged domain, assert all strata
disjoint, or pay any pending Native family or whole manuscript.
