One side has one of fifty-one unmarked incidence types
=====================================================

This guide gives the mathematical arguments behind the finite certificate.
The five-defect-edge and seed reductions are earlier project work, with
their source attribution in the `common argument <../common/ARGUMENT.rst>`_.
The contributions developed here are the side boundary, the complement
encoding, the cut parity deduction and the six-column catalogue. Detailed
authorship and review records accompany the retained notes. The proofs use
standard degree counting, finite multisets and finite group actions;
historical priority has not been established.

The exact earlier boundary and missing-hypergraph notes, and their
qualified mathematical reviews, are retained under ``provenance/``.
Those frozen documents include statements about their original preparation
time. The later finite verification is recorded separately. This guide
uses that verified catalogue without changing the old documents.

1. The target and its fixed seed
--------------------------------

Let G be a simple 5-regular triangle-free graph on 32 vertices. Its labelled
seed has roots 0 and 10 at distance at least 8 and the 25 edges

* 0--a for a=1,...,5, and 1--s for s=6,...,9;
* 9--21, and 20--b for b=21,...,25;
* 25--19, and 11--s for s=16,...,19;
* 10--c for c=11,...,15.

This is the retained seed normalization of a distance-eight geodesic:
choose its two endpoint neighborhoods and middle neighborhood, then the
four other neighbors of its first and penultimate vertices. Triangle
freeness and shorter root walks exclude overlaps among these seed parts.
Labels along the geodesic give the two displayed joining edges. This is
the existing seed interface, with its source attribution retained in the
common argument; it is not a newly asserted census-coverage return.

Thus 0,1,9,21,20,25,19,11,10 is a geodesic. Put

 A={1,...,5}, B={21,...,25}, C={11,...,15},
 I=A union B union C, J=V(G)\I, U={26,...,31}.

The common argument proves I independent: each neighborhood is independent
by triangle-freeness, and a common vertex or an edge between two such
neighborhoods would shorten a geodesic subpath between the three centres.
The regular degree identity

                 |E(G[J])|=5(32-2|I|)/2

therefore gives exactly five defect edges. The centres 0, 20, 10 already have
all five neighbors in I, so are isolated in G[J]. No forest or bipartite
assumption is made about G or its defect graph.

Among the 14 remaining J vertices define L to be those meeting A, R those
meeting C, and M those meeting neither. L and R are disjoint: a common
vertex would give a root walk of length 4. The seed puts {6,7,8,9} in L
and {16,17,18,19} in R. Write

 |L|=4+x, |R|=4+y, |M|=m, so x+y+m=6.

Each A vertex has four neighbors in L, besides root 0. These are 20 A--L
edges. The further forced edge 9--21 gives at least 21 degree incidences at
L, hence 5|L|>=21 and |L|>=5. Similarly |R|>=5 using 19--25. Thus x,y>=1,
m<=4, and every side has size between 5 and 9. M is a subset of U. These
are full-completion definitions: an absent partial edge does not prove M.

2. Missing neighbors encode the entire A--L incidence
-----------------------------------------------------

For each of the five labelled A vertices set E_a=L\N(a). If ell=|L|,
each E_a has size ell-4. Repeated sets are allowed. Let delta(v) be the
number of the five sets containing v, counting occurrences. Then

        d_A(v)=5-delta(v),  delta(v)<=4,
        remaining degree at v=delta(v),
        sum_v delta(v)=5(ell-4).

Indeed a is adjacent to v exactly when v is omitted from E_a. The bound
delta<=4 is exactly that every L vertex meets A. Conversely these
complements recover every incidence bit, give every A row degree 4, and
make every L column nonempty. This is a bijection on labelled data.

Forgetting the five A labels leaves a multiset of five hyperedges on L.
Incidence isomorphism under permutations of A and L is equivalent to
isomorphism of that multihypergraph under permutations of L. A carrying
column permutation preserves the multiset, and matching equal occurrences
supplies a row bijection. Equal rows are retained: four-cycles are allowed.
This unmarked quotient does not preserve the seed's distinguished row 1.

3. Local internal edges and residual port demands
-------------------------------------------------

For a pair of distinct L vertices {u,v}, adding uv creates a triangle
through A exactly when some a is adjacent to both. Its negation says
that {u,v} meets EVERY E_a. Let C_2 be the graph of such two-element
covering pairs. Then the internal L graph D must satisfy

          D subset C_2,  d_D(v)<=delta(v).

The remaining port demand is q(v)=delta(v)-d_D(v), into P=B union M.
For a proposed port set T_v of size q(v), the exact local triangle
conditions are: D triangle-free; T_u and T_v disjoint for every D edge;
and T_v independent in the supplied central graph on P. Together these
conditions give every side-interior vertex degree 5 and exclude every
triangle containing an interior vertex. The cases are triangles inside
L, through A, through a single port, or through two ports, respectively.

They do not determine port degrees or the opposite side. All required H
edges, the total defect budget, gluing compatibility, connectedness, root
distance, exact girth 4 and diameter 8 remain to be checked. A two-cover
pair is eligible only for the local triangle test, not for automatic
completion to a target.

4. Six five-column types and forty-five six-column types
-------------------------------------------------------

If ell=5, each complement is a singleton. Its positive column
multiplicities form a partition of 5 with all parts at most 4. The exact
six unmarked incidence types are

       (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1).

Zeros pad to five columns. Each partition is realized as a bare incidence
by assigning its singleton occurrences to the five A rows. Row and column
permutations identify precisely assignments with the same partition.
The partition 5 would give an empty A column and is forbidden.

A pair covers all singleton complements exactly when it contains the
whole support. Consequently C_2 consists of one edge for both (4,1) and (3,2);
it is empty for the other four types. That one edge is optional, with
seed/port restrictions still imposed. For example, using an edge at 9
when delta(9)=1 would leave no capacity for required 9--21.

If ell=6, each complement is a pair. The exact bare objects are loopless
multigraphs on six columns, with five edges, parallel edges allowed and
maximum degree 4. There are 15 possible unordered pairs. Their nonnegative
multiplicities sum to 5, giving C(19,5)=11628 raw multisets before filtering.

The `analytic count <COUNT.rst>`_ proves the following counts by Burnside's
formula and a classification of the forbidden multistars. The supplied
catalogue additionally gives all representatives and transporters:

                    raw multisets       11628
                    invalid degree        741
                    admissible          10887
                    S6 orbits              45

Its 45 representatives include degree budgets, the two-cover graph, orbit
size and stabilizer size. Every one of the 10,887 admissible raw multisets
has a literal six-vertex transporter to its representative. No predicted
orbit count is used to stop the computation.

The producer examines every raw multiset and caches complete S6 orbits.
The independent check path verifies canonicality once for each supplied
representative under all 720 vertex permutations. It then examines all
11628 raw cases, rejects precisely the invalid-degree ones, and checks
the ONE supplied transporter for every admissible case. Distinct minima
cannot represent the same orbit, so complete raw coverage proves the
partition and its multiplicities. The checker accepts any valid supplied
list order and carrying permutations; it does not replay the producer's
canonical-orbit cache search. Supplied canonical bytes are retained and
the emitted verified catalogue must equal them byte for byte.

5. Cut parity guarantees a small side
-------------------------------------

Suppose m=0. A B vertex already meets 20; its four other neighbors lie
in L union R. It cannot meet both sides, since
0--a--l--b--r--c--10 would be a root walk of length 6. Thus all four
neighbors are in just one side. Let B_L and B_R be these two classes.
They are both nonempty by 9--21 and 19--25. In particular

                         e(B,L)=4|B_L|.

The residual degree in L after A is 5x. With M empty and no L--R edge,
it is exactly twice the internal L edges plus B--L edges. Hence

                    5x-2e(G[L])=4|B_L|.

This forces x even. Likewise y is even. Since x,y>=1 and x+y=6,
only (2,4) or (4,2) remains. If m>0, x+y<=5 already forces one of x,y
at most 2. Therefore every target has a side of size 5 or 6.

The `nonempty middle set theorem <provenance/middle_nonempty_argument.rst>`_
now excludes m=0 entirely. To see its additional step, take the hypothetical
small side with six vertices. Every vertex has internal degree at most 2:
one A-neighbour forbids three of the five possible neighbours by triangles.
On an internal edge uv, disjoint A- and B_L-neighbourhoods force
d_D(u)+d_D(v)>=5-|B_L|. The cut equation leaves only
(e_D,|B_L|)=(1,2) or (3,1). A single edge has degree sum 2, below the
required 3. In the second case every edge endpoint must have degree 2,
forcing a nonempty triangle-free cycle with at least four edges, although
there are only three. Both cases are impossible. The
`review <provenance/middle_nonempty_review.rst>`_ records the retained
hypotheses and the full check.

After choosing a permitted orientation x<=y, the remaining necessary
size triples are contained in

 (1,4,1), (2,3,1), (1,3,2), (2,2,2), (1,2,3), (1,1,4).

These are not existence or class-count assertions. In the hypothetical m=0 case the
small side x=2 satisfies 10-2e_L=4|B_L|, so e_L is 1 or 3 and |B_L| is 2
or 1, respectively. The other side has 4 or 2 internal defect edges because
all five defect edges then lie in L or R.

6. Orientation and marked use
------------------------------

The initial seed has a root-exchanging permutation: swap 0 with 10, A
labels 1..5 with C labels 11..15, side labels 6..9 with 16..19, and 21
with 25; fix 20, 22, 23, 24 and U. This carries every listed seed edge in
Section 1 to another listed seed edge. Relabelling an ENTIRE completion
by this permutation therefore preserves its ordinary graph class and
places a chosen small side on the left of the initial seed interface.
It is not necessarily an automorphism of that completed graph.

An arbitrary later required graph H can break this exchange. For that
family keep both orientations or supply the checked transport to the
correspondingly relabelled family. An unordered root-pair convention alone
does not license dropping H's other edges.

Unmarked incidence types also forget the special A row 1, whose four
L neighbors are exactly {6,7,8,9}. Its missing set is therefore U intersect
L. Marked use must restore that hyperedge occurrence, the distinguished
vertex 9/port 21, all other seed and H information, internal D, and the
port sets. For column and row-occurrence permutations the required
incidence identity is

                       pi_L(E_a)=E'_{pi_A(a)}.

Equal occurrences still receive distinct A labels. A port permutation
must act simultaneously on both sides and the central graph. Every true
side gives a consistent marked lift of some unmarked representative;
enumerating all such lifts is complete, but no further quotient by a
factorial or group order is justified without its own action proof.

The resulting conclusion is precise: SIX plus FORTY-FIVE gives 51
unmarked incidence entry types for ONE side of every target, after the
allowed global orientation. It is not 51 graph types, and it does not say
that all 51 entries extend to targets. It supplies no complete side or port
library, no count of compatible glues, no closure of a current H family
or debt, and no upper proof for the 25,408-class census. Those remain
separate mathematical and certificate obligations.

The written arguments and actual finite verification give this incidence
result. They do not provide a Lean proof, a new Original disposition or
a measured manuscript compression ratio.
