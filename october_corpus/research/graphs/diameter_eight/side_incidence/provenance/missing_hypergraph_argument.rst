Hypergraphs of missing neighbors
================================

Root proposed the uniform encoding below and its small-side applications.
The proofs, exact reconstruction conditions and marked transport interface
are written by /root/readme_navigation_audit,23October2026. Navigation also
supplies the cut-parity exclusion in Section6. The earlier
defect, side-separation and boundary-gluing proofs remain attributed and
unchanged. Final is preparing a separate catalogue for the six-vertex
incidence problem; no catalogue or graph computation is executed here.
These are elementary finite encodings, with no historical novelty claim.

1. Setting and the uniform encoding
-----------------------------------

Use ../side_boundary_decomposition/ARGUMENT.rst,Sections1--3. The ambient
graph is triangle-free and5-regular on32vertices with the acquired rooted
seed. On its left side, A has five vertices and each a in A has precisely
four neighbors in L, besides its neighbor at the root0. Every vertex of
L has at least one neighbor in A. Write ell=|L|. The earlier proof gives
5<=ell<=9. Ports lie in P=B union M. The same statements hold on the right
with C,R and root10. No bipartiteness of the ambient graph is assumed.

For each a in A, define

                 E_a = L \ N(a).

These five subsets, initially labelled by the distinct vertices a, form
an (ell-4)-uniform multihypergraph H on L. Repeated hyperedges are allowed:
distinct A vertices may have the same four L neighbors, producing allowed
four-cycles. Let delta(v) count the hyperedges containing v, with multiplicity.

Theorem1. This is a bijection between A--L incidence graphs with every
A degree4 and every L vertex meeting A, and labelled five-edge uniform
multihypergraphs as above with delta(v)<=4. Moreover

             d_A(v)=5-delta(v),
             remaining degree at v after A edges =delta(v),
             sum over v of delta(v)=5(ell-4).                 (1)

Proof. Each of the five A vertices has four distinct L neighbors, so its
complement has size ell-4. A vertex v is adjacent to exactly the A vertices
whose complements omit v. This gives the first equation. Meeting A is
equivalent to5-delta(v)>=1, hence delta(v)<=4. Ambient degree5 gives the
second equation. Counting incidences in the five complements gives the
third. Conversely, define a--v exactly when v is not in E_a. Each A row
then has four neighbors and delta<=4 makes every L column nonempty. These
two constructions are inverse on labelled data.

After forgetting A labels, the five hyperedges are a multiset, not a set.
Incidence graphs modulo Sym(A) times Sym(L) correspond exactly to these
multihypergraphs modulo Sym(L). Indeed an incidence isomorphism carries
the complements accordingly. Conversely a vertex permutation carrying the
hyperedge multiset permits a bijection between equal hyperedge occurrences;
that bijection supplies the A permutation and hence an incidence isomorphism.
This unmarked statement does NOT preserve a distinguished seed A vertex.

2. The exact graph of eligible internal pairs
----------------------------------------------

Define C_2(H) on vertex set L: distinct u,v are adjacent exactly when the
two-element set {u,v} meets EVERY hyperedge E_a. Multiplicity is retained
in H although it does not change this particular hitting condition.

Theorem2. Adding the edge u--v creates no triangle containing an A vertex
if and only if uv is an edge of C_2(H).

Proof. Such a triangle exists exactly when some a is adjacent to both
u and v. By definition that is the assertion u,v are both outside E_a.
Its negation, for every a, is exactly {u,v} intersect E_a nonempty.

Consequently the internal graph D=G[L] satisfies

                D subset C_2(H),   d_D(v)<=delta(v).          (2)

Its remaining port demand is

                         q(v)=delta(v)-d_D(v).               (3)

The word eligible refers only to triangles with A. It does not say that
every subset of C_2(H) extends to a target graph.

Here is a complete local reconstruction interface. Include root0--A;
use the complement incidence from Theorem1; choose a simple graph D on L;
and choose each vertex's port-neighbor set T_v subset P of size q(v).
Require(2), require D triangle-free, and, for each uv in D, require
T_u intersect T_v empty. When the central graph Z[P] is supplied, also
require every T_v independent in Z[P]. These conditions are necessary and
sufficient for every interior vertex to have degree5 and for no triangle
to contain an interior vertex of this side piece.

For the degree assertion, root0 has its five A neighbors, each A has root0
and four L neighbors, and each L vertex has
5-delta(v)+d_D(v)+q(v)=5neighbors. For the triangle assertion, triangles
inside L are exactly those of D; triangles using A are excluded precisely
by Theorem2; triangles with two L vertices and one port are excluded by
disjoint port sets; and triangles with one L vertex and two ports are
excluded by independence in Z[P]. There are no A--A, A--P or0--L/0--P
edges. This exhausts all possibilities. Simplicity holds because all
neighbor collections are sets on disjoint parts and D is simple.

Full seed/family requirements, port degree compatibility, the total five
defect edges, the borrowed side-separation condition, connectedness, root
distance, exact girth4 and exact diameter8 remain additional conditions
when the two sides and Z are glued. The interface does not erase them.

3. Five L vertices: six incidence types
---------------------------------------

If ell=5, each hyperedge is a singleton. Equivalently the missing A sets
D_v={a:v in E_a} partition the five A vertices, permitting empty parts.
The multiset of positive delta values is therefore a partition of5 with
largest part at most4. There are exactly these six possibilities:

             (4,1), (3,2), (3,1,1), (2,2,1),
             (2,1,1,1), (1,1,1,1,1).

Zeros pad each to five columns. This is an exact count of UNMARKED
incidence types only; no cage count, port assignment or current-family
count is inferred. Each partition is realized by assigning its indicated
numbers of A labels to the singleton hyperedges. Permuting A labels and
L vertices shows that this assignment's incidence type depends only on
the partition, and every such permutation preserves the partition.

For distinct u,v, the pair meets all singleton hyperedges exactly when
the entire support lies in {u,v}. Since delta<=4 and the total is5,
both vertices then have positive delta. Thus C_2(H) is a single edge
for the types(4,1) AND(3,2), and is empty for the other four types. The
eligible edge is uniquely the pair of supported columns. Both two-part
types must be retained; excluding(3,2) would be incorrect.

Even that one edge is optional and subject to the seed and ports. For
example, the forced9--21 requires q(9)>=1. If delta(9)=1, selecting the
eligible edge incident with9 would give q(9)=0 and is therefore forbidden.
The unmarked six-type catalogue is not itself the marked side library.

4. Six L vertices: a multigraph with five edges
-----------------------------------------------

If ell=6, each E_a is an unordered pair. H is precisely a loopless
multigraph on six vertices with five edges, allowing parallel edges and
isolated vertices, and with maximum degree at most4. Its degree counts
all edge occurrences. There are15possible unordered pairs. Before the
degree restriction and before quotienting there are exactly

                        binomial(19,5)=11628

five-element multisets of those15pairs. This follows by writing their
fifteen multiplicities as nonnegative integers with sum5. It is a raw
finite input count, not a measured isomorphism-class count or runtime.

A complete unmarked catalogue may enumerate those multiplicity vectors,
reject exactly the ones with a degree above4, and for every remaining
multigraph choose the lexicographically least sorted edge multiset among
its6! vertex permutations. It must retain an explicit carrying permutation
for every raw admissible record, and one representative for every attained
key. Degree and multiplicity preservation justify the filters and action.
This procedure is finite and complete by construction, independently of
which canonical tie is selected. A Saved checker may accept ANY supplied
catalogue with valid representatives, explicit transports and complete raw
coverage; it need not trust a producer's choice of canonical representative.

Final owns the separate implementation of that Source kit. No enumerator
is authored or invoked by this note. No filtered class count is predicted.

5. Seed marks and lifts of catalogue transports
------------------------------------------------

In the acquired seed, a=1 is distinguished: N_L(1)=S_L={6,7,8,9}. Hence

                         E_1=U intersect L.                 (4)

The vertex9 is additionally distinguished by its required port21. The
other known seed or family H edges remain individually required too.
An unmarked catalogue quotients all five A vertices and all L labels;
it cannot silently be applied while leaving these distinctions fixed.

For ell=6, the distinguished missing pair in(4) is exactly the two U_L
vertices. The catalogue representative must later be supplied with a
distinguished hyperedge occurrence for A1, a bijection of its four-vertex
complement to S_L (including the chosen9), and a bijection of the marked
pair to the two actual U_L vertices. The other four hyperedge occurrences
are assigned to A2,...,A5. Identical occurrences still have distinct A
labels in this lift. The analogous marked lift applies for every ell.

More generally a transport certificate contains a permutation pi_L of
the ell columns and a permutation pi_A of the five row occurrences,
and verifies, for every a,

                       pi_L(E_a)=E'_{pi_A(a)}.                (5)

It also transports the seed colors, distinguished row/port, every required
H edge, internal D and all port-neighbor sets. A permutation of ports, if
used, must act simultaneously on both sides and Z. A certificate satisfying
only(5) proves unmarked incidence equivalence, not marked family equivalence.
Full current H must either be preserved or be carried by a separately
checked global class-coverage transport, as in the earlier boundary note.

Completeness of marked use follows by taking any actual side piece,
forming its labelled complements, transporting its unmarked type to a
catalogue representative, and carrying ALL its marks and port data along.
Thus enumerating every consistent marked lift loses no side piece. Reducing
those lifts further requires a proved orbit transversal under the stabilizer
of the retained marks, rather than a division by a group order.

A limited torsor statement is valid here. For two finite structured pieces
with the same fixed boundary identification, including all root/H marks,
let Iso_P(X,Y) consist of isomorphisms inducing that prescribed boundary
map. If nonempty, it is a torsor under Aut_P(X), the automorphisms of X
fixing its boundary pointwise and preserving all retained structure.
Indeed f and g in Iso_P give f^{-1}g in Aut_P(X), uniquely, and
g=f(f^{-1}g); composition is free and transitive. With different boundary
maps or dropped H marks this conclusion does not justify identifying
arbitrary glues. The statement describes exact transport choices, not a
classification of the unknown completed graphs.

6. Every target has a side of size five or six
----------------------------------------------

The earlier split parameters satisfy x,y>=1 and x+y+m=6, with
|L|=4+x and |R|=4+y. At the level of size equations alone, both sides
exceed6 exactly in the potential case x=y=3,m=0. The following degree
argument excludes that case in every target, without a finite search.

Lemma. If m=0, then x and y are even. Consequently their only possible
ordered size pairs are(2,4) and(4,2).

Proof. Each b in B already has its neighbor20 and four other neighbors.
When M is empty, all four lie in L union R. No b can meet both L and
R: that would give the root walk0,a,l,b,r,c,10 of length6, contradicting
root distance8. Thus partition B into B_L and B_R, according to which
side contains those four neighbors. Both parts are nonempty because of
the seed edges9--21 and19--25. In particular

                         e(B,L)=4|B_L|.                     (6)

The total residual degree in L after the A incidences is5x, by(1).
With M empty and no L--R edge, these incidences are precisely twice
the internal L edges and the B--L edges. Hence

                    5x-2e(G[L])=4|B_L|.                    (7)

The right side and the second term on the left are even, so x is even.
The symmetric argument gives y even. Now x+y=6 and x,y>=1 prove the
claim. In particular(1,5),(3,3),(5,1) cannot occur when m=0.

Corollary. Every actual target has a side with ell=5 or6.

Proof. If both sides were larger, the size equations would force the
excluded case x=y=3,m=0.

After orienting by x<=y where allowed, the necessary size possibilities
are therefore contained in the seven coarse types

 (2,4,0), (1,4,1), (2,3,1), (1,3,2),
 (2,2,2), (1,2,3), (1,1,4).

This is not an assertion that each type is realized, or an acquired
graph-orbit count. Without root exchange, retain the reversed types too.
For m=0 and the side x=2, the total five-defect-edge budget gives
e(G[L])<=5. Equation(7), with |B_L|>=1, then forces exactly
e(G[L])=1 or3, with |B_L|=2 or1 respectively. There are no M edges
or L--R edges, so the opposite side has4 or2 internal edges. These
are necessary library filters, not existence results.

For global unmarked graph coverage one may orient the seed so this small
side uses the left library, provided the root exchange transports the
entire seed and interface. An arbitrary fixed H need not admit that
exchange. Keep both orientations there, or supply the explicit checked
transport to the correspondingly relabelled family. The source contract's
unordered root pair does not permit forgetting H's other edges. The
initial25-edge seed does have an explicit exchanging automorphism:
swap0 with10, swap1,...,5 with11,...,15 respectively, swap6,...,9 with
16,...,19 respectively, swap21 with25, and fix20,22,23,24 and U.
Every listed seed edge is carried to a listed seed edge. Additional H
edges may break this automorphism and must still be retained.

The new leg is therefore a uniform finite incidence encoding, precise
internal-edge and port budgets, and a marked route to reuse small catalogues.
It proves no complete side library, full target upper bound, current-family
closure, census, Lean theorem, Original disposition or compression factor.
Existing accepted work and every Source/runtime/resource bound remain intact.
