Separation of the two sides in the five-edge defect graph
=======================================================

Written by /root/readme_final_check,23 October2026, from Root's proposed
shortest-path argument, independently checked and expanded here. The defect
identity, fixed seed, side definitions and disjoint-neighborhood inequality
are borrowed from Navigation's earlier notes, cited precisely below. The
contribution is this short project derivation and its proposed literal
diagnostic, not a claim of historical priority or a completed graph census.
No checker, graph search, worker, helper, guard or state transition was
invoked while preparing this note. All finite diagnostic outcomes are UNRUN.

1. Setting and borrowed premises
-------------------------------

Let G be a simple5-regular graph on32 vertices with no triangle. Suppose
the literal seed retained by the rooted family contract is contained in G:

* 0--i for i=1,...,5 and10--i for i=11,...,15;
* 1--j for j=6,...,9 and11--j for j=16,...,19;
* 20--i for i=21,...,25, together with9--21 and19--25.

Assume d_G(0,10)>=8. The displayed seed contains the eight-edge path
0,1,9,21,20,25,19,11,10, so it is geodesic. The saturated centers0,20,10
have full neighborhoods A={1,...,5}, B={21,...,25}, C={11,...,15}.
These sets are disjoint, independent and have no edges between them:
within a neighborhood an edge makes a triangle, and an edge between two
neighborhoods shortens a subpath of the geodesic. Thus I=A union B union C
is independent of size15. Put J=V(G)\I and F=G[J]. Degree counting gives

                    2|E(F)|=5|J|-5|I|=10.                    (1)

Hence F has exactly five edges. The three centers are isolated in F.
Put J'=J\{0,10,20}. Let L be the vertices of J' meeting A, let R be
those meeting C, and let M meet neither. Here meeting means adjacency
in the FULL completion G, not merely in its partial literal record H.
L and R are disjoint, since a common vertex gives a root walk of length4.
Together L,R,M partition J'.

Every vertex v in M has all its I-neighbors in B and consequently has
5-d_F(v) neighbors in B. If uv is an edge of F with u,v in M, their
B-neighborhoods are disjoint by triangle-freeness. Since |B|=5,

                         d_F(u)+d_F(v)>=5.                   (2)

These are the independent-set identity and the disjoint-neighborhood
inequality in the borrowed two-sided-middle note, Section1, equations(1),(3).
The full graph G need not be bipartite. We impose no hypothesis that F is
a forest, a star, or free of four- or five-cycles.

2. The short-path restriction
----------------------------

For l in L choose a in A adjacent to l; for r in R choose c in C adjacent
to r. An F-path of length t from l to r supplies the root walk

                    0,a,l,...,r,c,10

of length t+4. A walk always contains a path no longer than itself.
Therefore every F-path between L and R has length at least4. This argument
does not require the auxiliary root walk to be simple.

3. An abstract five-edge lemma
-----------------------------

Lemma. Let X be a finite simple graph with at most five edges. Partition
its nonisolated vertices into sets L,R,M, permitting isolated vertices to
belong to any of the sets. Assume every L--R path has length at least4,
and assume d_X(u)+d_X(v)>=5 for every edge uv with u,v in M. Then no
connected component of X meets both L and R.

Proof. Suppose otherwise and choose a shortest path between the two SETS,
with endpoints x_0 in L and x_t in R. It is simple. No internal vertex
belongs to L or R: an internal L or R vertex would give a shorter path
between the sets. Thus all internal vertices belong to M. The distance
assumption gives t>=4, while the edge budget gives t<=5.

If t=5, the path uses all five edges of X. Every internal vertex has
degree2. The edge x_2x_3 is an M--M edge with degree sum4, a contradiction.
Extra isolated vertices or components do not change this count.

Suppose t=4. The path uses four edges. Its internal vertices x_1,x_2,x_3
are in M and each has degree at least2. With no fifth edge, either edge
x_1x_2 or x_2x_3 violates the degree-sum hypothesis. Thus a fifth edge
exists. To increase both sums d(x_1)+d(x_2) and d(x_2)+d(x_3) from4 to at
least5, this one edge must either be incident with x_2 or join x_1 to x_3.
An edge wholly elsewhere or incident with only one of x_1,x_3 cannot do so.
The chord x_1x_3 shortens the L--R path to length3 and is impossible.

The fifth edge therefore has form x_2y. Simplicity excludes a loop and
the two already present edges to x_1,x_3. The choices y=x_0 or y=x_4
would again shorten the L--R path to length3. Consequently y lies outside
the displayed path. If y were in L, then y,x_2,x_3,x_4 would be an L--R
path of length3. If y were in R, then x_0,x_1,x_2,y would be such a path.
Hence y is in M. Since all five edges are now accounted for, d(x_2)=3
and d(y)=1. Their M--M edge has degree sum4, the final contradiction.
This exhausts both possible path lengths and proves the lemma.

The abstract lemma needs no separate triangle-free assumption: geodesic
minimality already excludes the problematic chord. In the present graph
application, triangle-freeness was used to obtain(2). The proof does not
extend the five-edge budget to arbitrary k without a further argument.

4. Side separation in the target graph
--------------------------------------

Theorem. In the setting of Section1, no component of F meets both L and R.

Proof. Discard the three isolated centers or place them in M; their degree
is zero and they cannot affect an edge or path. Equations(1),(2) and
Section2 verify all hypotheses of the abstract lemma.

In particular every defect component is confined to L union M, to R union M,
or entirely to M. This is a necessary condition on a target completion, not
a sufficient characterization. It gives neither the existence nor the number
of completions, and it need not isolate every empty partial family.

5. Monotone literal certificate and proposed diagnostic
------------------------------------------------------

For an acquired literal graph H retaining the seed, put F_H=H[J]. Let L_H
be the vertices of J' with an H-neighbor in A, and define R_H similarly
using C. Every permitted completion has F_H subset F, L_H subset L and
R_H subset R. Thus a known F_H-path from L_H to R_H certifies that the
literal family is empty, by the theorem. It suffices to retain the literal
path, an A-neighbor of its left endpoint and a C-neighbor of its right
endpoint, together with the seed and family identity. Forced side sets are
monotone under extension; missing side adjacencies must never be inferred.

The Source-only checker proposed here authenticates the accepted7727 typed
snapshot, its acceptance chain, all51 pending node identities, each whole
original frontier file and each raw-line SHA/typed value join. It then examines
only the already known edges of those51 partial records. It supplies the full
component table and, when one exists, an explicit known L_H--R_H path. It
does not generate or enumerate completions, assume full L/R sets from H,
relabel families, infer class counts, or mutate any frontier. A family with
no such known path remains UNPAID by this diagnostic.

No number of matched or excluded current families has been acquired during
Source preparation. Even a later verified literal certificate is separate
from adoption: the existing native-return grammar has no new algebraic proof
transition. The history, pending counter, reservations and accepted class set
remain unchanged until a separately reviewed Root proof transition exists.
This artifact supplies no Original, measurement, Lean or complete-census credit.

6. Exact sources and attribution
-------------------------------

Navigation's common note, ../ARGUMENT.rst,16836 bytes, SHA
688c4e4bc3f3ada4a213af977aeb9fab6246cb64441ed25178381f42725664d1,
Sections2 and4 supplies the independent-set identity, fixed seed and defect
host. Navigation's ../two_sided_middle_vertices/ARGUMENT.rst,15185 bytes,
SHAaa92690f46561d5e79a8306f4be8149d081dc6d9e0fb739a719b0d46b619c9e2,
Section1 supplies the exact side definitions and(2). Its independent review
is ../two_sided_middle_vertices/independent_readme_review/review.json,
11328 bytes, SHA6b8750b01147f01de94de25e1f6e39b2e94bc12182c2a1fc0613929f291164f1.
The semantic contract is computation/f009/rooted_census_split/family_coverage/
family_contract.json,1404 bytes, SHA
2977a08362104cf74938049e7db121669d0282cc3e18e984d8d3cb8c4c733e8b.

The fixed closed7727 checkpoint/snapshot/acceptance identities are in scope.json
and the earlier persistence document c9ab9f24. They are immutable supplied
inputs for a future Root call, not a claim about the latest live checkpoint.
The path-counting lemma here is Root's proposed argument, independently verified
and written out by this reviewer using the cited standard graph facts. There
is no literature-priority claim and no new historical source intake.
