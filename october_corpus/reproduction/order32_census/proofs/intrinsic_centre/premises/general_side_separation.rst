Universal side separation at the extremal defect budget
======================================================

Root proposed this strengthening while the separate degree-five diagnostic
was being frozen. The proof below is independently verified and written by
/root/readme_final_check,23 October2026. It uses the independent-set and
disjoint-neighborhood lemmas of Navigation's earlier defect notes, cited
below. These are elementary graph arguments applied in this project; no
historical-priority, new source-intake, Lean or completed-census claim is made.
The earlier frozen degree-five kit remains byte-identical and its diagnostic
remains UNRUN. No number of current applications is asserted here.

1. An abstract graph lemma
-------------------------

Theorem. Let k>=5 be an integer. Let X be a finite simple graph with at
most k edges, and let L,R,M partition its vertices. Suppose:

(a) every path from L to R has length at least4; and
(b) d_X(u)+d_X(v)>=k for every edge uv whose endpoints are both in M.

Then no connected component of X meets both L and R.

No triangle-free assumption is needed for this abstract statement. In the
regular-graph application below, triangle-freeness establishes hypothesis(b).
Degrees in(b) are full degrees in X, not degrees in a chosen path.

Proof. Assume a component meets both sides and choose a shortest path between
the SETS L and R. Denote it x_0,x_1,...,x_t with x_0 in L and x_t in R.
It is simple. Every internal vertex is in M: an internal vertex in either
side gives a shorter path between the sets. By(a),t>=4.

First suppose t>=5. The internal edge x_2x_3 has both endpoints in M.
Let S_23 be the set of all edges incident with x_2 or x_3. Since X is
simple, their common incident edge is precisely x_2x_3, so

               |S_23|=d_X(x_2)+d_X(x_3)-1>=k-1.

The distinct path edges x_0x_1 and x_4x_5 are outside S_23. Hence X has
at least(k-1)+2=k+1 edges, a contradiction. This excludes every t>=5;
there is no need to enumerate possible longer paths up to the edge budget.

It remains that t=4. The edges x_1x_2 and x_2x_3 are M--M edges. For the
first, the incident-edge union S_12 has size at least k-1. The outer path
edge x_3x_4 is outside S_12. The total edge budget therefore forces

             E(X)=S_12 disjoint-union {x_3x_4}.              (1)

In particular X has exactly k edges and d_X(x_1)+d_X(x_2)=k. Applying
the same count to x_2x_3 and the other outer edge gives

             E(X)=S_23 disjoint-union {x_0x_1}.              (2)

Remove the two distinct outer edges x_0x_1 and x_3x_4. Every remaining
edge must meet {x_1,x_2} by(1), and {x_2,x_3} by(2). If such an edge
does not meet x_2, it must be x_1x_3. That chord gives an L--R path of
length3, contrary to(a). Thus every one of the k-2 remaining edges is
incident with x_2.

Simplicity implies that these k-2 edges form a star with k-2 distinct
neighbors. Two are x_1 and x_3. The center cannot also be adjacent to
x_0 or x_4: either edge gives a path between the sides of length3.
Consequently the star has k-4 additional neighbors outside the original
path. Since k>=5, at least one such neighbor y exists. All edges of X
have already been described: the two outer path edges and this star.
Therefore

                       d_X(x_2)=k-2,  d_X(y)=1.              (3)

The vertex y is in neither side. If y were in L, the path
y,x_2,x_3,x_4 would have length3 between the sides. If y were in R,
use x_0,x_1,x_2,y. Hence y is in M, as is x_2. Their edge has degree
sum(k-2)+1=k-1, contradicting(b). This proves the theorem.

The proof covers disconnected X and isolated vertices: the edge budget is
global, while the chosen path lies in one component. No extra edge in
another component can escape either of the two tight incidence counts.
It also does not assume that X is a forest or has a prescribed degree
sequence. The chord exclusion follows from(a), so an additional triangle-free
assumption on X would be redundant.

2. The degree-four boundary
--------------------------

The abstract threshold cannot be lowered to k=4. Take the five-vertex path
x_0--x_1--x_2--x_3--x_4, let L={x_0},R={x_4}, and let M contain the
three internal vertices. There are exactly four edges, the side distance
is4, and both M--M edges have degree sum2+2=4. Nevertheless the component
meets both sides. In the proof, k-4 is then zero, so the leaf y in(3)
does not exist. This is an abstract counterexample only; it does not
assert realizability as a defect graph of a specified regular target.

3. Application to all degrees k>=5
---------------------------------

Corollary. Let G be a finite simple triangle-free k-regular graph on
6k+2 vertices, where k>=5, containing an eight-edge geodesic
p_0,...,p_8. Put

       A=N_G(p_0), B=N_G(p_4), C=N_G(p_8), I=A union B union C,
       J=V(G)\I, F=G[J], J'=J\{p_0,p_4,p_8}.

Let L be the vertices of J' meeting A, let R be those meeting C, and
let M consist of those meeting neither. Then no component of F meets
both L and R.

Proof. Each neighborhood is independent by triangle-freeness. The three
centers have pairwise geodesic distances4,4,8. A common vertex of two
neighborhoods gives a shorter center-to-center path of length2, and an
edge between two neighborhoods gives one of length3. Thus I is independent
of size3k; its complement has size3k+2. The standard degree identity gives

                   2|E(F)|=k|J|-k|I|=2k,

so F has exactly k edges. The three centers are isolated in F. The sets
L and R are disjoint because a common vertex gives a root walk of length4.
A path in F from l in L to r in R, together with one A-neighbor of l
and one C-neighbor of r, gives a root walk with four additional edges.
It follows that every such F-path has length at least4.

For v in M, every neighbor in I lies in B, so there are k-d_F(v) such
neighbors. If u,v in M are adjacent in F, their B-neighborhoods are
disjoint, since a common neighbor would be a triangle. Their combined
size is at most k, giving d_F(u)+d_F(v)>=k. Add the three isolated
centers to M for purposes of the abstract partition; no edge meets them,
so this does not introduce an additional degree condition. All hypotheses
of the theorem now hold with X=F. This proves the corollary.

No primality assumption on k is needed. No assumption that G is bipartite,
or that F is acyclic, has been introduced. This is a necessary structural
condition, not a sufficient construction or a class-counting formula.

4. Current literal diagnostic and provenance
-------------------------------------------

For degree5 and the retained order32 seed, this corollary strengthens the
same written proof premise of ../check_separation.py. That frozen checker
still examines only known edges and forced side memberships of the fixed
accepted7727 partial records. A known defect path between forced sides
cannot disappear in a completion. Lack of a known path remains UNPAID;
the checker does not infer a completed partition from missing partial edges.

The degree-five Source kit is pinned by ../source_handoff.json,7950 bytes,
SHA60880588e50dd04455696d44c99b633c44a6d62a52421258b1fcfec4d83b41f7.
Its written argument is8992 bytes,
SHAed0c93d02b583c5e2482c7d808b5605342a5342f63a1dc4d1e2af8ade30025b1;
its checker is10789 bytes,
SHAae634c1628985e535064a89fcc9b9454e0553488f68eb93622c4b618b1d611f2.
Those files remain unchanged. This general-degree supplement contains no
worker or executable test and does not claim any current family is excluded.

Navigation's ../../ARGUMENT.rst,Sections2 and4,16836 bytes,
SHA688c4e4bc3f3ada4a213af977aeb9fab6246cb64441ed25178381f42725664d1,
supplies the independent-set identity and geodesic-neighborhood construction.
Navigation's ../../two_sided_middle_vertices/ARGUMENT.rst,Section1,
15185 bytes,SHAaa92690f46561d5e79a8306f4be8149d081dc6d9e0fb739a719b0d46b619c9e2,
supplies the side definitions and disjoint-B-neighborhood degree inequality.
Root supplied the strengthened two-tight-incidence-unions proof idea; this
author independently checked every case and supplied this complete derivation.
There is no claim that these standard methods or this theorem are novel in
the literature. No Source, state, frontier history, accepted census, reservation,
Original count, measurement or Lean record is modified by this supplement.
