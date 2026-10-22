Five defect edges for the remaining order-32 census
===================================================

Written mathematical analysis by /root/readme_navigation_audit, 22 October
2026. Distinct mathematical review is requested. This note changes no
Source, accepted boundary, census counter, reservation or proof record.
Only Source and closed mathematical or administrative text were read. No
frontier geometry, graph6 body, snapshot or target payload was decoded;
no project function, graph operation, solver, native program, resource
probe, process inspection, guard or state transition was invoked.

The contribution is an elementary structural reduction of the order-32
problem, parallel to the retained order-80 defect reduction. It also gives
a short independent proof of the order lower bound. Neither deduction
asserts a new historical theorem or acquires a complete class census.

1. The outstanding result is an exact class set
-----------------------------------------------

The source is Cambie, Goedgebeur, Jooken and Van den Eede, On the
order-diameter ratio of girth-diameter cages, the retained
arXiv:2511.21144v3 edition. Its degree-five, girth-four, diameter-eight
row records cage order 32 and 25,408 ordinary isomorphism classes. The
source's separate degree-three, girth-ten, diameter-eight row records
order 80 and five classes. The present task identifies their remaining
class-completeness obligations; final whole-manuscript assembly retains
its other independently checked premises.

The exact acquired order-32 contract is
rooted_census_split/family_coverage/family_contract.json. A family consists
of simple 5-regular supergraphs of its literal H on the same 32 labels,
with girth at least four and marked-root distance at least eight, followed
by selection for connectedness, girth exactly four and diameter exactly
eight. Roots are an unordered nonisolated pair. The contract adds no fixed
forbidden-pair list, canonical history or extra semantic constraint.
Strict operational fields and their historical verification are retained.

The acquired coverage invariant is the SET union of accepted ordinary
leaf classes and all unpaid semantic families. Raw occurrences and family
cardinalities cannot be added across overlapping families. A complete
census still requires every obligation closed by an accepted complete
return, coverage witness or sufficient empty-family proof; no reserved
debt; all exact final-property filters; ordinary isomorphism reduction;
and equality of the ENTIRE resulting class set with the retained reference.
Expected cardinality is not a stopping certificate.

Root reports the current accepted boundary as sequence 7605, with 3,899
nodes, 41 pending representatives, 201,549 selected raw occurrences and
zero reserved debt. These are supplied administrative facts, not a new
inspection of the mutable selector or a bound on remaining work.

2. An independent-set identity
------------------------------

Lemma. Let G be a k-regular graph on n vertices, and let I be an
independent set of size a. For J=V(G)\I,

                 |E(G[J])| = k(n-2a)/2.                 (1)

Proof. All ka incidences at I cross to J. The total degree sum in J is
k(n-a), so exactly k(n-a)-ka incidences remain for edges internal to J.
Each such edge has two incidences. This proves (1).

Lemma. If a triangle-free k-regular graph contains a geodesic
p_0,...,p_8, then

             A=N(p_0), B=N(p_4), C=N(p_8)

are disjoint independent sets, with no edge between any two of them.
Consequently their union I is independent and has size 3k.

Proof. Each neighborhood is independent because G has no triangle.
A geodesic has geodesic subpaths, so the three centers have pairwise
distances four, four and eight. Intersecting neighborhoods would give a
center-to-center path of length two. An edge between neighborhoods would
give one of length three. Both are impossible.

For k=5 and n=32, (1) gives exactly FIVE edges in G[J], where |I|=15
and |J|=17. This conclusion is valid for both bipartite and nonbipartite
targets. The five-edge graph is triangle-free, but it may contain a
four-cycle or a five-cycle. Requiring it to be a forest would lose coverage.

3. A short order exclusion, independent of enumeration
------------------------------------------------------

Proposition. If k is an odd prime, a connected triangle-free k-regular
graph of diameter at least eight has at least 6k+2 vertices. In particular
every connected triangle-free 5-regular graph of diameter eight has order
at least 32.

Proof. The preceding independent set I has size 3k. Degree counting into
its complement gives n>=6k. Suppose n=6k. Equality in that count forces
J to be independent too, so G is bipartite with parts I and J, each of
size 3k. The three centers p_0,p_4,p_8 belong to J and have neighborhoods
A,B,C respectively. Put J'=J\{p_0,p_4,p_8}.

Let L consist of the vertices of J' with a neighbor in A; let R consist
of those with a neighbor in C. They are disjoint: a vertex in both would
give a p_0--p_8 path of length four. Put M=J'\(L union R), and write
l=|L|, r=|R|, m=|M|. Each M vertex has all its k neighbors in B, hence
is adjacent to every member of B.

Each A vertex has its center neighbor p_0 and k-1 further neighbors,
all in L. Thus E(A,L) has k(k-1) edges. The geodesic vertex p_2 belongs
to L and is also adjacent to p_3 in B. Therefore L has at least one
incidence outside A, giving kl>k(k-1), or l>=k. Symmetrically r>=k.
Since l+r+m=3k-3, we have m<=k-3.

No member of B can have a neighbor in both L and R. Such neighbors,
together with an A neighbor at the L end and a C neighbor at the R end,
would give a p_0--p_8 walk of length six, contrary to distance eight.
Every B vertex already has its neighbor p_4 and all m neighbors in M.
Its remaining q=k-1-m neighbors therefore all lie in exactly one of
L or R, where 2<=q<=k-1. Partition B into B_L and B_R accordingly,
with sizes b_L,b_R. Both are nonempty, by p_2,p_3 and the symmetric
p_6,p_5 part of the geodesic, and b_L+b_R=k.

Degree counting at L gives

                   q b_L = kl-k(k-1)=k(l-k+1).            (2)

As k is prime and 1<q<k, (2) forces k to divide b_L. This contradicts
0<b_L<k. Thus n=6k is impossible. Finally k is odd, so the degree-sum
identity forces n even; n=6k+1 is impossible too. This proves the claim.

The argument uses elementary degree counts, the source's neighborhood
and geodesic method, and primality. It does not rely on the reported
25,408 classes or a completed generator run. It supplies no upper-bound
graph and no class-completeness proof. The source already has cage order
32; the proposition is a new local derivation here, not a priority claim.

4. Exact specialization to the already acquired seed
----------------------------------------------------

The held order32_inventory_distinct_review.rst describes the acquired
seed explicitly. It consists of two Moore edge trees, centered at 0--1
and 10--11, and the star centered at 20 with leaves 21..25. The joining
edges are 9--21 and 19--25. There are 25 edges on labels 0..25; labels
26..31 are isolated. The marked roots are 0 and 10, joined by the path

                  0,1,9,21,20,25,19,11,10.              (3)

This is the existing seed, not a proposed replacement for its acquired
coverage argument. Its specialization also follows directly from the
read createMooreTree Source branch for k=5,g=4,d=8.

The three centers 0,20,10 are already saturated. Thus their full target
neighborhoods, and hence I, are fixed seed sets:

        I = {1..5} union {11..15} union {21..25}.

In J, vertices 0,10,20 are saturated. Write

          S={6..9,16..19},       U={26..31}.

Only S union U can support an internal J edge. Within either four-point
S block, an edge would form a triangle through the common parent 1 or 11.
An edge between those blocks would give a root path of length five.
Therefore the complete necessary defect host is

                 (S cross U) union choose(U,2),          (4)

with 8*6+15=63 unordered pairs. Every target has exactly five edges F
in this host. Necessarily deg_F<=4 on 6..8,16..18, deg_F<=3 on 9,19,
and deg_F<=5 on U. Seed+F must remain triangle-free and retain root
distance at least eight. These are hereditary necessary conditions, not
a sufficient target test. No condition saying F is a star is imposed.

The seed has 25 crossing edges. The finished graph has 80 edges, of
which five are in F, leaving exactly 50 missing crossing edges. There
are only thirteen active I vertices: 2..5,12..15,22..24 each need four
neighbors; 21 and 25 each need three. The active J side is S union U,
of size fourteen. Its residual crossing demands are

  4-deg_F(j), j in {6..8,16..18};
  3-deg_F(j), j in {9,19};
  5-deg_F(j), j in U.

The initial S demand is 6*4+2*3=30 and the U demand is 6*5=30.
Their remaining crossing demand is therefore 60-2*5=50, equal to
11*4+2*3 on I.

The seed automorphisms fixing 0 and 10 individually fix path (3)
pointwise. Their effective action on the defect host is exactly
Sym({6,7,8}) cross Sym({16,17,18}) cross Sym(U), of order 25,920.
Each factor permutes indistinguishable pendant leaves or isolated seed
vertices and extends by the identity elsewhere. Conversely the fixed
path and seed adjacency force these cells and fix 9 and 19. This is
an exact available outer quotient, not a computed orbit count. When
using an arbitrary later family H, its additional edges can break
these symmetries and must be retained as well.

5. A complete finite neighborhood interface
--------------------------------------------

For fixed F, choose the full J-neighborhood T_i of each i in I. It must
have five distinct members, contain all already fixed neighbors, and
be an independent set in F. The two saturated rows 1 and 11 stay fixed.
The columns must satisfy

                  |{i in I : j in T_i}|=5-deg_F(j).

These finite conditions are necessary and sufficient for a simple
5-regular triangle-free graph containing seed+F. Indeed I is independent;
the only possible triangle either lies in F or uses one I vertex and
an F edge between two of its neighbors. The row-independence conditions
exclude exactly the latter triangles, and the row/column equations give
all degrees. No completeness of an external graph generator is needed
for this equivalence.

Connectivity, root distance, girth exactly four and diameter exactly eight
remain full final conditions. A row assignment meeting only the displayed
degree and triangle restrictions is not yet a target graph. A necessary
residual b-matching test is still useful for pruning but is not a complete
replacement for compatible row choices or final distance checks.

At the initial fixed-F interface, an ordinary four-neighbor row chooses
among at most choose(14,4)=1001 sets. A three-neighbor row already has
one neighbor in S and chooses among at most choose(13,3)=286 sets.
These are finite domain bounds before column capacity, triangle and
distance restrictions, not estimates of run time. They do not imply
that the complete cartesian search is small.

There is an exact reusable symmetry on these rows. Permute 2..5,
12..15 and 22..24 independently, fixing every other seed vertex. This
group K=Sym(4) cross Sym(4) cross Sym(3), of order 3456, preserves the
seed, every possible F, the roots and all final target conditions.
Within each cell, sort the COMPLETE crossing-neighbor lists in a fixed
lexicographic order. This retains exactly one edge-set representative
per K orbit: the product group acts by arbitrary row permutations within
the cells, and two assignments are equivalent exactly when each cell
has the same multiset of rows. A carrying permutation is obtained by
matching equal sorted rows, retaining all ties.

The ordering must be NONSTRICT. Equal rows create four-cycles, which
are permitted here. Consequently K is not generally free; 3456 is not
a uniform quotient of the number of labelled completions or a measured
speedup. Prefix pruning is justified only after the complete rows being
compared are fixed. Ordering incomplete rows is not licensed by this proof.
Earlier canonical searches may already exploit some of this symmetry.

6. Joining the current unfinished work without repeating it
----------------------------------------------------------

The most conservative application is per current semantic family H.
It needs an explicit checked embedding of this seed into H, including
the marked roots, or the corresponding transported sets I,S,U. No such
current-family witness is inferred from the scalar count 41. Keep all
edges of H: reject a candidate F unless it contains every H-edge internal
to J, and force every already present crossing edge into its row. The
five-edge and row equations then give an exact decomposition of the same
family, not a new global start and not a replay of closed native work.
Additional root/final filters remain the original ones.

For such a complete decomposition, every original target completion
supplies exactly its own F and its own row tuple. Conversely every row
tuple that contains H and passes every final filter is in that semantic
family. This proves the equality before quotienting. Quotient by the full
K is safe for the seed problem, but for an arbitrary fixed H it is safe
only under a subgroup that preserves H, or with a separately checked
transport that preserves the GLOBAL class union. Silently applying the
whole K while demanding fixed literal H can lose family coverage.

To use new negative or enumerative certificates for closure, the current
coverage verifier needs an explicit independently reviewed proof kind and
an accepted transition. The old native completed-return type is not a name
for these new certificates. A missed proposal, capped orbit list, partial
row search or unlaunched child leaves its obligation unpaid. Current aliases,
ordered prior leaves, historical retained inputs, debt and backend roles
are not rewritten. The five-edge decomposition alone closes no parent.

An outer fresh seed quotient is also mathematically possible, but it must
then genuinely cover all five-edge records and compatible row completions.
Using the existing pending families first is preferable for reuse: it
retains closed work as the acquired leg and narrows only the remaining
obligations. Which route is faster is unacquired.

7. Relation to order 80 and the actual next step
-----------------------------------------------

The acquired order80_defect_forest_reduction.rst already gives independent
set size38, complement42, exactly six defect edges in a156-pair host, then
43 missing crossing edges. The retained crossing-kernel proposition gives
its separate order262144 free action and exact rooted-tree normal form.
Those statements must be reused with their own girth-ten and seed premises;
they are not new results of this note. The order-32 row quotient differs:
its four-cycles are allowed, so equal rows and nontrivial stabilizers occur.
Neither quotient licenses multiplying an old canonical-search speedup.

Thus both remaining rows share one short independent-set identity and
the same outer-defect/inner-crossing architecture, with distinct exact
girth, degree, seed and symmetry interfaces. The actual class counts
still need complete certificates in those interfaces. A separate theorem
that all order-32 defects, or all order-80 non-star defects, are impossible
has not been proved here. No bipartiteness conclusion is assumed.

The next useful acquisition is to read each current order-32 parent's
literal seed embedding, fixed J edges, crossing rows and admissible symmetry
subgroup under an explicit later grant; measure the resulting constrained
five-edge and row domains; then choose a single reusable certificate
producer and a Saved checker that verifies full supplied data rather than
replaying a heuristic. Source review, small positive and negative controls,
genuine actual completion evidence and Root adoption remain unpaid.
For order80, reuse the already prepared defect/orbit/crossing interfaces
instead of starting another independent residual search.

Attribution
-----------

The cage problem, finite tables and original generator belong to the source
authors. The old seed embedding, chronological restore, exact-family set
coverage, closed-family transport and residual-degree certificates are
borrowed project legs with their original attribution. The independent-set
degree identity, finite group actions and degree divisibility are standard
elementary arguments. This note supplies their explicit order-32 join, a
complete written prime-degree exclusion and a finite row interface. It is
a proposed mathematical reduction awaiting distinct review, not a Lean
proof, executed certificate, new conjecture solution, measured compression
factor or completed original.
