Independent hand review of the side-boundary decomposition
=========================================================

Reviewer /root/readme_final_check. Verdict: qualified mathematical Source
PASS, no supported blocker in ARGUMENT.rst12005B,
d856896125338bc1684d9a7c89ab5128ecbaf7d164682c29466e7aaa5f04b778.
The author is Navigation. Root proposed the port/decomposition direction.
This reviewer authored the cited general-degree side-separation proof from
Root's argument and Navigation's earlier independent-set premises; that
related ancestry is explicit. This is an independent review of the NEW
decomposition, not an independently authored replacement of those old legs.

All checks here are Source reading and hand mathematics. No graph/example,
family, state, snapshot, frontier, incidence library, solver, enumerator,
checker, native/compiler, project/helper, guard or process function ran.
There is no acquired library count, current-H applicability, speedup,
upper-coverage return, new Original/Lean/measurement or frontier credit.

1. Seed, side definitions and incidence bound
-------------------------------------------

The exact25-edge seed fixes N(0)=A={1..5}, N(20)=B={21..25},
N(10)=C={11..15}, with the displayed eight-edge root path. A completion
with root distance at least8 therefore makes this path geodesic. Its
three centers have pairwise distances4,4,8. Triangle-freeness makes each
neighborhood independent; an overlap or edge between neighborhoods would
give a center path of length2 or3, contradicting a geodesic subpath.
Thus I=A union B union C is independent of size15. The regular-degree
identity gives |E(G[J])|=5(32-30)/2=5. The saturated centers are isolated
in F. The old defect host, without forest/bipartite assumptions, is retained.

For L, every one of the20 A-incidences beyond the saturated root lands in
L. Its vertices have total degree5|L|. The required edge9--21 consumes a
further incidence at L (9 meets1 in A and21 is in B). Consequently
5|L|>=21, so |L|>=5. This does not assume L independent or ignore internal
edges: all incidences outside A only make the inequality stronger.
The symmetric19--25 argument proves |R|>=5.

L and R are disjoint, since a vertex meeting both A and C would give a
root walk of length4. Their union with M is the14-vertex active J set.
The known four S_L vertices lie in L and four S_R in R, so M is a subset
of U and |M|<=4. Writing |L|=4+x, |R|=4+y gives x,y>=1 and x+y+m=6.
For m0..4 there are respectively5,4,3,2,1 ordered choices:15 SIZE types.
Initial Sym(U) is transitive on partitions of each such size. This is
not an orbit count for completed graphs or for an arbitrary later H.

2. Exact edge ownership and all size bounds
------------------------------------------

The four disjoint vertex blocks are X_L={0} union A union L,
X_R={10} union C union R, P=B union M, and {20}. No edge joins the
two interiors: I-independence excludes A--C; side definitions exclude
A--R and C--L; an L--R edge yields a root path of length5; the roots
are already saturated by their prescribed neighborhoods. The center20
has exactly B as its neighbors. Every remaining edge therefore has
exactly one owner: internal P or20--P in Z, otherwise the unique side
piece meeting its endpoint in X_L or X_R. Removing internal-P edges from
both sides avoids double ownership. This proves the claimed partition.

Sizes follow directly, with no estimate from a graph count:

  |X_L|=10+x, |X_R|=10+y lie between11 and15;
  |P|=5+m<=9;
  |X_L union P|=15+x+m=21-y<=20;
  |X_R union P|=21-x<=20; |P union{20}|=6+m<=10.

The converse is correctly limited by ALL final predicates. Piece degrees
alone do not preserve root distance, connectedness, exact girth4 or exact
diameter8. Requiring each L vertex to meet A, each R vertex to meet C,
and M to meet neither recovers the intended complete side definitions.
Every true labelled completion supplies exactly its own partition/pieces.
No hidden source-family forbidden-pair/canonical-history constraint was
added: the acquired family contract has none.

3. Port restriction and defect-component condition
-------------------------------------------------

A B vertex meeting L and R would give the root path
0--a--l--b--r--c--10 of length6. Hence it meets at most one side.
Its four noncentral neighbors all belong to L,R,M. If it meets no side,
they must be four DISTINCT M vertices. Since m<=4, this means m=4 and
adjacency to all M. Thus when m<4 every B vertex belongs to exactly one
side-neighbor class, with21 left and25 right by their forced seed edges.
The initial interchangeability of22..24 is correctly not treated as a
free quotient factor.

The earlier side-separation theorem applies to the FULL defect graph F.
Its hypotheses are root side-distance>=4 in F and the disjoint B-neighbor
inequality d_F(u)+d_F(v)>=5 on each M--M edge. The cited proof establishes
them for these targets, without assuming F is a forest. For the proposed
gluing test, only F connectivity on M is merged: B and the centers are
not defect connectors. Every side F component touching M transfers its
side flag to that boundary component; central M--M edges merge components.
Components with no M cannot connect to the other side and are harmless.
This proves the stated component-flag check, provided actual F-connectivity
and flags are retained rather than only degrees or full-G connectivity.

4. Library and current-family coverage
-------------------------------------

A boundary-pointwise side isomorphism extends by identity on the opposite
interior and Z. It agrees on P, and the exact edge ownership proves that
the extended map is a graph isomorphism. Root/side/requirement colors must
be respected as stated. Full side graphs are essential; equal degree
deficits or boundary distances alone do not give that isomorphism.

Conversely every actual target provides eligible side pieces and a central
graph, so COMPLETE pointwise-boundary libraries and EVERY compatible gluing
give class coverage. Relabelling ports independently would break the common
interface; simultaneous transport of both sides and Z is necessary.
No division by2, row factorial, or port factorial is justified without an
explicit action/transport and correct stabilizers.

The ordinary isomorphism lemma is not, by itself, a bijection of a fixed
literal H family. The author's Section6 supplies the necessary stronger
interface: an actual seed embedding/root orientation, all H edges forced,
every consistent full L/R/M split, and either H-preserving transports or
checked GLOBAL class-coverage transport. In particular missing partial
incidences never establish M. Initial Sym(U) normalization and row sorting
must not be copied into an arbitrary H without this qualification. The
held note already makes these limitations; no correction is requested.

Any upper-coverage certificate still needs complete libraries/child cases,
an acyclic reuse proof, every glue's final decision, and actual ordinary
isomorphisms to accepted positives. A deficit-only cache key, circular reuse,
partial library, expected count or unvisited glue cannot supply those facts.
No current H or reserved debt is shown closed by this note.

5. Native symmetry statements and attribution
---------------------------------------------

The pinned girthDiamGraph.c createCanonicalFormEncodedGraph at234--262
sets defaultptn=false and exactly three classes: unordered original roots,
remaining original vertices and the two auxiliaries. It does not individualize
the seed row or U cells. The stated seed permutations are consequently
recognized when their partial graphs are rooted-isomorphic; adding only
those canonical relations would not be a new equivalence reduction.

The pinned search function backtrack at524--526 checks visited keys only
at a saturated current vertex and the stated level range. The terminal
entry sets level1=level2=0 and partialLevel999999. addToVisitedGraphs at
235--260 caps admission at65536; at the cap it returns false and continues
search (including already-seen keys, not merely unseen keys). The note's
weaker statement about unseen keys is true. Tree freeing and separate
regular-leaf cache/isolated first-use normalization corroborate its limited
reuse/performance claims. This is a check of those textual statements, not
a new audit of the whole native algorithm's completeness or runtime.

The order80 defect-forest leg has different girth10 hypotheses and is only
an analogy here. Neither forest structure nor its free-action factor is
imported into order32. Navigation's prior row-multiset proof explicitly
allows equal completed rows; its nonfree stabilizers and H-preservation
qualification remain. Root/Nav/earlier source-author contributions are
retained. No literature priority or novelty claim has been assessed.

Scope boundary
--------------

PASS applies to the held d8568961 note and its explicitly conditional
mathematical/library interface. It does not certify an implementation,
current-family seed map, actual library size, finite-incidence addendum,
bounded runtime/controls, accepted upper coverage or source-paper completion.
No enumeration, graph test, project function or scientific payload read was
performed. The separate proposed small-side incidence libraries were not
treated as acquired input or silently added to this reviewed edition.
