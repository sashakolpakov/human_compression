Two side pieces over a boundary of at most nine vertices
======================================================

Source-only mathematical note by /root/readme_navigation_audit,23October2026.
This reuses the existing five-defect-edge decomposition and Root/Final side-
separation theorem. It adds their explicit bounded port decomposition and
upper-coverage interface. No graph, solver, census, native, helper, resource,
guard or state operation has run. No historical novelty or measured speedup
is claimed. A distinct proof review and every actual certificate are owed.

1. Existing legs, retained exactly
---------------------------------

Use ../ARGUMENT.rst,Sections2,4--6, for the actual order32 seed, independent
set identity, defect host, exact row model and row-permutation normal form.
Use ../separation_of_sides/general_degree/ARGUMENT.rst for side separation.
The latter is Root's proposed argument, independently proved by Final; its
independent-set premises come from the earlier Navigation notes. The order80
defect-forest proof is the analogous earlier leg, with its own girth10
hypotheses. Order32 defects must NOT be assumed to be forests or stars.

In detail, G is a triangle-free5-regular graph on32 vertices containing the
acquired25-edge seed, whose roots0,10 have distance at least8. That seed
contains the path0,1,9,21,20,25,19,11,10, so this path is geodesic. Put

 A={1,...,5}, B={21,...,25}, C={11,...,15},
 I=A union B union C, J=V(G)\I,
 S_L={6,7,8,9}, S_R={16,17,18,19}, U={26,...,31}.

The existing proof gives I independent, F=G[J] with exactly5edges, the
centers0,10,20 isolated in F, and the defect host
(S_L union S_R) cross U, together with pairs inside U. Define L as the
vertices of J\{0,10,20} meeting A, R as those meeting C, and M as those
meeting neither. L,R,M are a partition, S_L subset L and S_R subset R.
These are FULL-completion side sets; absent partial edges do not prove M.
Every component of F meets at most one of L and R, by the borrowed theorem.

2. The small middle set
-----------------------

Lemma. |L|>=5, |R|>=5 and M subset U has size at most4.

Proof. Each a in A has one neighbor0 and four further neighbors. All20
further incidences go to L: I has no internal edges; the other two centers
cannot be adjacent to A; and the definition of L covers every remaining
neighbor. Vertex9 lies in L and has the prescribed neighbor21 in B. Thus
at least one incidence at L is not an A--L edge. Since L has total degree
5|L|, we obtain20<=5|L|-1 and hence |L|>=5. The symmetric argument uses
19--25 and gives |R|>=5. The set J\{0,10,20} has14vertices, so |M|<=4.
The four known S_L and four known S_R vertices are outside M, giving M⊂U.

Write x=|U intersect L|, y=|U intersect R| and m=|M|. Then

                x>=1, y>=1, m>=0, x+y+m=6.                 (1)

There are15ordered size triples in(1): for each m=0,...,4, there are5-m
choices of x. For the INITIAL seed, Sym(U) carries every partition of a
fixed size triple to a fixed consecutive-label partition. This is a proven
finite list of split SIZE TYPES, not a list of graph types or an acquired
orbit count. An arbitrary later family H need not retain all these
permutations; Section6 states the necessary qualification.

3. Exact gluing over at most nine ports
--------------------------------------

Theorem. Put P=B union M, X_L={0} union A union L and
X_R={10} union C union R. Then G has the following exact edge partition:

* a central graph Z on P union {20};
* a left piece on X_L union P with no edges internal to P;
* a right piece on X_R union P with no edges internal to P.

The interiors X_L,X_R are disjoint, there are no edges between them,
and20 has precisely its five neighbors B. Each side interior has11--15
vertices; |P|<=9; and each side piece INCLUDING its ports has at most20
vertices. Z has at most10vertices.

Proof. The definitions partition all32vertices into X_L,X_R,P,{20}.
There are no edges A--C or from A or C to B, since I is independent.
An edge A--R or C--L contradicts the definitions. Edges A--M and C--M
also contradict those definitions. An edge L--R would give the root walk
0,a,l,r,c,10 of length5 and is impossible. The two roots are saturated
by their seed neighborhoods. The center20 is saturated by B. This proves
the edge partition, including absence of every cross-interior edge.

Now |X_L|=6+|L|=10+x and |X_R|=10+y. Equation(1) gives11<=10+x<=15,
and similarly on the right. Also |P|=5+m<=9. The left piece size is
15+x+m=21-y<=20, and the right piece is21-x<=20. Finally |Z|=6+m<=10.
No forest or bipartite hypothesis was used.

Conversely, the union of three such pieces on these explicitly identified
vertex sets gives one unique labelled graph: central edges belong only to
Z, and every other edge belongs to its unique side piece. It is a target
completion exactly when it contains the required seed or family H, has
every vertex of degree5, is simple and triangle-free, is connected, and
has girth exactly4 and diameter exactly8 with the marked-root condition.
Thus all final distance, girth and connectivity predicates remain. Piece
degree feasibility alone is insufficient. Actual side definitions are
enforced by requiring every L vertex to meet A, every R vertex to meet C,
and M to meet neither. Each true completion supplies exactly its own
partition, central graph and pair of labelled side pieces.

Further necessary port condition. A vertex b in B cannot meet both L and
R, since0,a,l,b,r,c,10 would be a root walk of length6. Every b already
meets20 and has four remaining neighbors. If it meets neither side, these
four distinct neighbors all lie in M. Consequently that possibility occurs
only when m=4, and then b is adjacent to all M. This is an exact additional
boundary restriction. In particular m<4 partitions B into two sides, with
21 on the left and25 on the right. The three remaining B ports are
interchangeable in the initial seed, but this is not an extra free factor.

Retain also the borrowed side-separation condition on F. It can be tested
after gluing, or by merging the F-connectivity partitions on M contributed
by each side and Z: no resulting F component may carry both side flags.
The full graph need not be bipartite. Cycles in the five-edge F are retained.

4. An exact finite library normal form
--------------------------------------

Fix one split, central graph and the boundary labels. A side library stores
one FULL graph representative from each boundary-pointwise isomorphism
class of eligible side pieces. Its colors retain the interior root, its
A or C set, all seed/required-edge information, and the original interface.
The library cannot identify nonisomorphic interiors merely because their
degree deficits or boundary distance matrices coincide.

Lemma. Replacing a side piece by a boundary-pointwise isomorphic library
representative preserves the ordinary isomorphism class of the glued graph.

Proof. Extend the side isomorphism by the identity on the other side and
Z. Both maps agree on P; the exact edge partition in Section3 then proves
that this union is a graph isomorphism. All final graph predicates transfer.
Conversely every target graph supplies its actual side pieces, whose
library representatives give an isomorphic glued graph. This proves class
coverage, provided both libraries and every compatible pair are complete.

Boundary relabelling is also permitted, but it must act SIMULTANEOUSLY on
both libraries and Z and preserve the selected split, colors and requirements.
An explicit permutation proves each transport. Independently canonicalizing
the two boundaries can glue incompatible ports and is unsound. Root reversal
is a simultaneous transport of both sides and marks, not division by2.

The previous row-multiset normal form removes permutations of completed
rows2..5,12..15,22..24 where its hypotheses hold. Reuse that proof; equal
rows remain allowed. For additional library memoization, a state retains
the full colored partial side graph, remaining capacities, undecided
requirements and exact boundary data. A deficit vector alone is not a
state key. Reused states need an explicit full state isomorphism and an
already closed dependency; a circular reference proves no upper bound.

This changes the decomposition into reusable pieces of order at most20.
It does not assert that their finite libraries are small in practice, that
all pairs pass, or that library construction fits any given runtime cap.

5. Which symmetries the current native Source already uses
---------------------------------------------------------

The held graph5fe77d17 createCanonicalFormEncodedGraph uses densenauty
with three invariant color classes: the UNORDERED original root pair,
all other original vertices, and the two root auxiliaries. It therefore
recognizes root-preserving isomorphisms including the seed's S4×S4 row
permutations and S6 residual-label permutations whenever compared partial
graphs are isomorphic. It does not individualize these seed cells.

Searcha39438c3 uses that full partial key when currentVertex is saturated,
local numEdgesAfterTree>level1 and<=partialLevel. The current terminal entry
sets level1=level2=0 and partialLevel=999999. Its visited insertion cap is
65536; after the cap, unseen keys are searched without insertion. The table
is freed after each native call. Ordinary completed leaves have a separate
canonical cache. normalizedCurrentVertex and isolatedLexMin additionally
choose first-use labels among currently isolated vertices, accounting for
unused-label symmetry before general memo hits.

Hence merely adding an S4×S4 or S6 canonical key would not introduce a new
equivalence relation. The stated library leg instead moves a complete
bounded side problem outside repeated whole-graph traversals and permits
its verified reuse across compatible boundaries/families. Any actual gain
requires acquisition. No factorial speedup or raw-occurrence division is
deduced; stabilizers, cache limits and family overlaps must remain explicit.

6. Minimal family/coverage certificate interface
-----------------------------------------------

For a current semantic family H, retain its exact original record SHA,
marked roots and all H edges. Supply an explicit seed embedding into H,
with root orientation; missing such an embedding is an unpaid premise.
Enumerate every L/R/M split consistent with forced H side memberships;
do not classify a vertex as M merely because an edge is not yet present.
Force H edges into their actual central or side owner in Section3.

For fixed literal H use only permutations preserving H, or provide a
separately checked GLOBAL class-coverage transport to another retained
family. The full initial-seed S6 normalization and row sorting are not
automatically valid within every later H. Every explicit transport must
preserve roots, all mandatory edges and remaining interface predicates.

A possible NEW proof kind is F009_SIDE_BOUNDARY_UPPER_COVERAGE_V1. Its data
would contain the exact H/seed map, complete split/central cases, side-library
graphs with all child-choice coverage and transport permutations, an acyclic
reuse DAG, and every compatible glue's final decision. Each surviving target
glue carries an explicit ordinary isomorphism to a retained positive class;
each rejected glue cites a proved necessary condition or a verified final
predicate. All remaining child cases stay unpaid. No raw multiplicity or
expected25408 count substitutes for this complete coverage.

This is a precise proof obligation, not a new implemented verifier, native
return, method, control PASS or accepted frontier transition. The old
semantic family/set-union contract remains unchanged. Existing closed work
can be reused; only actual remaining families and reserved debts would need
new accepted coverage. Root alone may later acquire inputs, run bounded
controls/certificates and adopt a genuinely new proof kind. All current
resource, byte, provenance and literal-domain caps remain in force.
