# Root review of the finite-rank neighbourhood adapter

10 October 2026. **PASS for the stated finite-rank theorem.** This is an
internal source, proof and code review, with a fresh execution of the finite
checker. It is not an external review or a whole-paper reduction.

Root independently retrieved the [primary author-uploaded indexed text](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes).
The retrieved passages include the connectivity definitions, graph
conventions, conditions B1/B2, the verbal conclusions of Theorem 4.1,
Construction 5.1 and the relevant residue and connectivity proofs in section
5. The complete primary PDF and all application tables remain unread.

The adapter uses exactly the endpoint incidence condition: an edge meets a
higher object if and only if both endpoints meet it. This is needed in both
directions of the copied-vertex residue isomorphism. Simplicity of the graph
is needed to identify the edge uniquely from the two copied vertices. A
chamber of the old geometry chooses an endpoint of an edge; orienting that
edge gives the two ordered copied vertices in the new chamber. The inverse
map recovers the chosen endpoint and its edge. Every new flag extends by
the three cases of zero, one or two copied vertices.

The three residue models cover every new flag. For the reverse connectivity
implication they are supplemented by an essential fourth observation:
an old flag with an edge but no vertex has the two endpoints incident with
every remaining higher object. Such a residue is connected whenever its
rank is at least two. There is therefore no unexamined class of original
residues in the reverse implication.

At remaining rank at least three, the two copies of a vertex are connected
through a higher object. Comparing connected components with the subdivided
original graph proves connectivity equivalence; it does not assume that the
vertex-edge truncation itself is connected. At rank two the new incidence
graph is precisely the bipartite double. It is connected exactly when the
original graph is connected and nonbipartite. Applying these facts to all
residues proves the claimed residual-connectivity equivalence. The separate
finite-rank gallery induction justifies the strong-connectivity equivalence
in the stated scope. No infinite-rank inference is taken from that induction.

The same literal maps prove the exact rank-two isomorphism classes and the
equivariance of chambers. Fixing all new objects fixes the original vertices
and higher objects, then all edges, so action kernels agree. This identifies
the given action and its chamber orbits, not the full automorphism groups.
The endpoint condition for a disjoint pair survives by applying the old
condition to the original vertex underlying either new copy. This also
justifies the claimed commutation of the two literal constructions.

In the positive finite-rank case, strong connectivity makes every common
higher shadow connected. Completing the higher flag to cotype {0,1} supplies
an odd cycle inside that shadow. Its parity monodromy is the full group C2,
so the common cover theorem's intersection and coset-completion conditions
hold. Each higher object then has just one lifted component, and the common
construction coincides with the older neighbourhood construction. The
identification is explicitly limited to this positive case.

Root read the standard-library checker and reran it unchanged in a new
scratch directory. The output is byte-identical to the saved report: 316
graph/subset inputs, 12,628 residue isomorphisms and 26,802 flags, alongside
16 named examples and three iterations. These finite checks corroborate the
written proof; they do not establish unbounded rank or object-set scope.
Some negative controls allow a one-edge residue beyond the source's graph
convention, as the adapter and intake explicitly disclose.

Credit is appropriate for a named component of L111, namely the finite-rank
conclusions of Theorem 4.1 under B1/B2. The hypothesis-conversion lemmas,
section 6 and application tables are not covered by this audit. It adds no
principal-paper reduction, matched-length ratio or new-resolution marker.
