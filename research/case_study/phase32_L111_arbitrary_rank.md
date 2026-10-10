# L111 Theorem 4.1 at arbitrary rank: direct truncation proof

Date: 2026-10-10. Private extension of [the frozen finite-rank adapter](phase32_L111_theory.md). No edits to that note or its finite evidence.

## 1. Quantifiers and exact scope

The primary author-indexed version of Lefèvre-Percsy, Percsy and Leemans, [*New geometries for finite groups and polytopes*](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes), p.586, defines a flag as a pairwise incident set without imposing finiteness, and requires every flag to lie in a chamber. Its strong connectivity condition includes all truncations of rank at least two, in every residue. Theorem 4.1 explicitly allows infinite rank. Its rank-two residues can therefore be residues of infinite complementary flags.

We adopt those quantifiers literally: the type set \(I\) is an arbitrary **set** with at least three elements; a flag may be infinite; every such flag extends to an \(I\)-chamber; every flag residue is considered, including the empty flag. A truncation can retain any subset of types with at least two elements. Connectivity means connectivity by finite paths. Object sets may also be infinite.

The source access remains selected primary indexed passages, not a complete primary body or PDF. The exact target is the single numbered Theorem 4.1. Other statements, application tables and the entire-paper scope remain unclaimed. In particular we do not assert the converse direction of the source's hypothesis-conversion Lemma 4.1.

## 2. Statement and the parts that need no rank bound

Use assumptions G and E and definition (2) of \(U\Gamma\) from the finite note. For every higher flag \(F\) of cotype \(\{0,1\}\), let \(X_F\) be its graph residue. Write
\[
 \mathcal O:\quad D(X_F)\text{ is connected for every such }F. \tag{1}
\]
Here \(D\) denotes the bipartite double. Equivalently every \(X_F\) is connected and has an odd cycle.

**Theorem.** At arbitrary rank as above, \(U\Gamma\) is a geometry. It has the exact rank-two residue classes described in §6 of the finite note, and
\[
 \begin{split}
 U\Gamma\text{ is residually connected}
 &\iff\Gamma\text{ is residually connected and }\mathcal O,\\
 U\Gamma\text{ is strongly connected}
 &\iff\Gamma\text{ is strongly connected and }\mathcal O.
 \end{split}\tag{2}
\]
Every given type-preserving automorphism action has the same kernel and chamber orbits after applying \(U\). Conditions G and E persist at each disjoint pair of types.

The chamber proof and maps (3)–(6) in the finite note use neither induction nor the cardinality of a flag. A flag still contains zero, one or two objects of the selected types, even if its higher part is infinite. In the two-object case, E applies separately to every higher object, so the associated original flag extends by the stated chamber axiom. The resulting chamber bijection is valid for infinite chambers.

For the same reason, all three residue models hold for every flag. The connectivity equivalence for a remaining rank at least three uses finite paths and the availability of one remaining higher type; it requires no finite-rank induction. The rank-two case is the elementary bipartite-double criterion. The original edge-only residues have two endpoints joined to every remaining higher object, so are connected whenever their remaining rank is at least two. This proves the first equivalence in (2), with exactly the residue case split in §4 of the finite note.

The proofs for actions, disjoint-pair preservation and equality of all residue classes also use only these formulas. They remain unchanged at arbitrary rank. What requires a new argument is the **second** equivalence in (2); we must not assume that residual connectivity implies strong connectivity at infinite rank.

## 3. A global two-type truncation lemma

The following arguments apply to any geometry \(R\) with at least three types, satisfying G and E at types0 and1. They do not require a finite type set.

First observe that all truncations of rank at least two are connected if and only if all two-type truncations are connected. For the nontrivial direction, fix two retained types \(i,j\). Their truncation is connected. Any object of any further retained type lies in a chamber and hence meets an object of type \(i\); thus it belongs to the same connected component. This argument concerns arbitrary retained subsets, not just finite truncations.

**Forward lemma.** If every two-type truncation of \(R\) is connected, and at least one graph residue \(X_F\) has an odd cycle, then every two-type truncation of \(UR\) is connected.

Pairs of types outside0 and1 are unchanged. Each new truncation on \(\{0,j\}\) or \(\{1,j\}\), with \(j\notin\{0,1\}\), is a copy of the old truncation on \(\{0,j\}\). The remaining pair is \(D(X)\), where \(X\) is the full old vertex–edge graph. The old \(\{0,1\}\) truncation is connected, so \(X\) is connected. It contains the odd cycle from \(X_F\). Hence \(D(X)\) is connected.

**Reverse lemma.** Suppose \(UR\) is strongly connected, in the all-residues sense. Then every two-type truncation of \(R\) is connected.

The pairs outside0 and1 and the pairs \(\{0,j\}\) are obtained directly from the unchanged or copied truncations. Projection from the connected graph \(D(X)\) proves that \(X\) is connected, giving the old \(\{0,1\}\) truncation.

It remains to connect the old truncation on \(\{1,j\}\). Fix \(j\notin\{0,1\}\). If two old edges \(e,f\) share a vertex \(p\), the copied-vertex residue isomorphism gives
\[
 (UR)_{(p,0)}\cong R_p. \tag{3}
\]
Strong connectivity of \(UR\) makes the \(\{1,j\}\) truncation of the left-hand residue connected, and therefore supplies an old \(\{1,j\}\)-path between \(e\) and \(f\) in \(R_p\).

Any two old edges can be joined by a finite sequence of edges with consecutive edges sharing a vertex, since \(X\) is connected and has no isolated vertices. Concatenate the corresponding paths just constructed. Every old type-\(j\) object is incident with an edge, by chamber extension. Thus all objects of the old \(\{1,j\}\) truncation lie in one component. This completes the reverse lemma. Notice its explicit use of a residue of \(UR\); connectivity of its global pair truncations alone was not silently substituted for strong connectivity.

## 4. Apply the lemma to every residue

Assume first that \(\Gamma\) is strongly connected and \(\mathcal O\) holds. Let \(Q\) be any flag of \(U\Gamma\), possibly infinite.

If \(Q\) contains a copied vertex, its residue is an original flag residue by the local isomorphism, possibly with a type renamed. Every truncation of rank at least two is therefore connected.

If \(Q\) contains no copied vertex, it is a higher flag \(F\), and its residue is \(U(R)\) for \(R=\operatorname{Res}_\Gamma(F)\). If \(R\) has rank two, \(\mathcal O\) gives connectivity directly. If its rank is at least three, choose a chamber of \(R\) and remove its two selected lower objects. This produces a higher flag \(F'\) in \(R\), potentially infinite, such that \(F\cup F'\) has cotype \(\{0,1\}\) in \(\Gamma\). Condition \(\mathcal O\) gives an odd cycle in that graph residue. All two-type truncations of \(R\) are connected by strong connectivity of \(\Gamma\). The forward lemma therefore applies. This proves strong connectivity of every new residue, including the empty-flag residue.

Conversely, suppose \(U\Gamma\) is strongly connected. Its rank-two residues over higher flags are the graphs \(D(X_F)\), so \(\mathcal O\) holds. Let \(F\) now be any original flag whose residue has rank at least two.

- If \(F\) contains a vertex, the local model (4) or (5) in the finite note identifies its residue with a new flag residue. If it also contains an edge, the second copied vertex represents that edge. All its truncations are connected.
- If \(F\) contains neither a vertex nor an edge, its new residue is \(U(R)\) for \(R=\operatorname{Res}_\Gamma(F)\). Strong connectivity passes to that new residue because a flag in a residue adjoins to \(F\) to give a flag of the whole geometry. At remaining rank two, projection of \(D(X_F)\) gives connectedness of the original graph. At remaining rank at least three, the reverse lemma proves all two-type truncations of \(R\) connected.
- If \(F\) contains an edge \(e=\{p,q\}\) but no vertex, every remaining higher object meets both endpoints. Truncations of types \(\{0,j\}\) are consequently complete bipartite graphs with nonempty parts. Truncations on two remaining higher types are unchanged upon adjoining \(p\) to \(F\); the latter residue has already been identified with a new flag residue and has connected two-type truncations. There is no remaining type1.

These cases exhaust all flags. The first observation in §3 promotes the pair-truncation conclusions to all truncations, proving strong connectivity of \(\Gamma\). This completes the second equivalence in (2).

## 5. The source's alternative local-graph hypotheses

The source also allows a formulation using local graph residues, an endpoint-containment condition, and a converse condition triggered by two common endpoints. The direction needed to apply our theorem can be verified without assuming its asserted equivalence lemma.

Assume that every residue of cotype \(\{0,1\}\) is a simple graph, that every vertex incident with an edge \(e\) is incident with every higher object incident with \(e\), and that two distinct vertices common to an edge \(e\) and a higher object \(x\) force \(eIx\).

Choose a chamber containing an edge \(e\), and let \(H\) be its higher part. Endpoint containment puts **every global endpoint of \(e\)** in the residue of \(H\). Since that residue is a graph, \(e\) has exactly two global endpoints. If two edges \(e,e'\) share those endpoints, then for every \(x\in H\) the converse condition gives \(e'Ix\). They are two edges with the same endpoints in the graph residue of \(H\), so simplicity gives \(e=e'\). Every vertex lies on an edge by chamber extension. The two endpoint conditions now give E in both directions. Thus G and E follow, and the theorem applies to this alternative source input as well.

This proves the required implication from the alternative hypotheses. It does not assert the unnecessary converse, or remove the source's convention excluding a graph reduced to one edge.

## 6. Reusable theory and limitations

The finite-rank positive case in the earlier note is exactly a specialization of the existing monodromy recognition theorem: every relevant shadow has full \(C_2\)-monodromy. At arbitrary rank we instead use the direct proof above. The frozen general-cover theorem assumes finite rank; it is not imported as an arbitrary-rank theorem here. In particular, residual connectivity alone at infinite rank is not used to infer that a selected graph truncation is connected.

The whole of Theorem 4.1, including arbitrary rank and both source input formulations, is now recovered by explicit formulas and path arguments. This remains a **single-theorem component** of L111. No complete-primary-access status, full-principal-paper credit, claim about §6, or numerical compression ratio follows. The finite checker attached to the earlier note tests its concrete maps and boundary cases only; it supplies no experimental verification of infinite rank.
