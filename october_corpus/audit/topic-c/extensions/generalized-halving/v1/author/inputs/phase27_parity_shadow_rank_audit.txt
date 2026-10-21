# Independent audit of the parity-shadow obstruction

The [complete repaired theorem](phase27_parity_theory.md) passes independent mathematical review, including its exact residual-connectivity criterion and its lattice-polytope application. The firm rank-four example is a counterexample to the residual-connectivity assertion for the literal Construction 3.6 in the inspected [arXiv:2405.19050v1](https://arxiv.org/abs/2405.19050v1). The conclusion under challenge is Proposition 3.13 and the corresponding clause of Theorem A / Theorem 3.18. This finding is restricted to that source version. It is not a counterexample to the thin, flag-transitive regular-hypertope specialization.

## Source and hypothesis checks

I independently read the definitions in §2.1, the standing B1/B2 assumptions and Figure 2, Construction 3.6, Lemmas 3.9–3.12, Proposition 3.13, and the statements of Theorems A and 3.18. I also visually checked Figure 2 on printed p.6. The definition of incidence geometry requires every maximal flag to be a chamber. It does not silently impose thinness, flag transitivity, or firmness. The example nevertheless satisfies firmness. Its diagram has type 0 adjacent only to type 1, as required.

The nonbipartite graph in the hypotheses is the *underlying vertex-edge graph*, not the bipartite incidence graph between vertex and edge objects. Here that graph is $K_{2,2,2,2}$ and contains triangles.

The live [arXiv record](https://arxiv.org/abs/2405.19050), checked on 10 October 2026, lists only v1, dated 29 May 2024. The [publisher record](https://link.springer.com/article/10.1007/s00493-024-00134-y) gives a revision dated 24 November 2024 and a version of record dated 16 January 2025. Its body was not accessible in this review. Consequently I do **not** identify the inspected v1 text with the revised journal theorem. The separate [version audit](phase27_halving_version_status.md) records that access boundary. Bounded exact-title and correction searches found no relevant erratum; this is not a priority or exhaustive literature conclusion.

## Direct mathematical verification

Partition eight vertices into four two-element parts $A,B,C,D$. Type 0 consists of the vertices and type 1 of the 24 edges between different parts. Each of types 2 and 3 consists of four distinct objects, indexed by the unions of three parts. All pairs of objects of types 2 and 3 are incident. Incidence of a vertex or edge with a higher object is containment in its shadow. Same-type distinct objects are not incident.

B1 holds because the graph is simple. B2 is precisely the definition of edge–higher incidence. Any two higher shadows have either two or three whole parts in common. Thus they contain an edge; and every common vertex lies on such an edge. Every flag therefore extends to a chamber: if it already contains an edge, choose an endpoint when needed and choose the missing containing higher objects; otherwise first choose an edge in the common shadow, through the specified vertex when present. The same argument covers a flag with no higher objects.

All panels have at least two completions. For a panel missing a higher type, its specified edge belongs to exactly two higher objects of that type. For a panel missing type 0, its edge has two endpoints. For a panel missing type 1, the common higher shadow has two or three parts, and its specified vertex has respectively two or four neighbours there. These give exactly 336 panels of size two and 24 of size four. In particular the example is firm and nonthin.

For residual connectedness, all rank-two residue types can be checked directly:

* A residue on types $\{0,1\}$ is the vertex-edge incidence geometry of $K_{2,2}$ or $K_{2,2,2}$, both connected.
* Residues on types $\{0,2\}$, $\{0,3\}$, and $\{2,3\}$ are complete bipartite incidence graphs. Hence the first two pairs do not add edges at type 0 in the Buekenhout diagram.
* In a residue on types $\{1,2\}$, fix a vertex $v$ and a type-3 shadow $T$ containing it. One type-2 object has the same shadow $T$ and is incident to every eligible edge through $v$. Every other eligible type-2 object is incident to at least one such edge. The residue is connected. The $\{1,3\}$ case is symmetric.

The residues of rank three are also connected. At a vertex, the remaining higher types form a complete bipartite graph and every incident edge attaches to it. At an edge, both endpoints and all higher objects form a connected complete multipartite graph. At a higher object, the vertex-edge truncation is a connected $K_{2,2,2}$ geometry and every object of the other higher type attaches to it. Finally the whole geometry is connected by its vertex-edge truncation. This covers every flag of corank at least two.

Every individual higher shadow is $K_{2,2,2}$, so its even-walk partition has just one class, the whole shadow. Construction 3.6 therefore leaves each higher object unsplit. The new types 0 and 1 are two copies of the eight original vertices; a cross-type pair is incident exactly when its parts differ. Each higher object is incident to both copies of the vertices in its shadow, and the two higher types remain completely incident.

Take a type-2 object omitting $A$ and a type-3 object omitting $B$. Their common original graph is $K_{2,2}$ on $C\cup D$. Their new residue has the two disjoint components

$$C\times\{0\}\ \cup\ D\times\{1\},\qquad
  D\times\{0\}\ \cup\ C\times\{1\},$$

each a $K_{2,2}$. Thus the transformed geometry is not residually connected. The same obstruction occurs for all twelve ordered unequal choices of omitted parts. It remains a geometry: any common vertex can be paired with a vertex in a different common part, and any such pair extends by containing higher objects.

This identifies the exact failed inference. The intersection of the chosen individual even-walk classes is all of $C\cup D$. It is **not** one even-walk class of the common graph $K_{2,2}$. Lemma 3.11 consequently does not supply a partitioned neighbourhood graph of the kind to which Lemma 3.4 applies. Connectedness of the original common graph does not repair this parity-class mismatch.

The example is also not flag-transitive. Whether the type-2 and type-3 members of a chamber have equal vertex shadows is invariant under every type-preserving automorphism. Chambers of both kinds exist. No assertion here refutes the regular-hypertope specialization, nor does it prove that specialization by another argument.

## Independent executable check

The new [checker](phase27_parity_shadow_rank_check.py) imports none of the author's code. It uses bitset incidence matrices and recursively enumerates every typed flag. It computes even-walk classes from length-two reachability and constructs the transformed incidence relation from those classes, rather than assuming that the higher objects are unsplit. It checks every flag extension, every rank-at-least-two residue, every B2 instance, the rank-two digon pairs, and all twelve common-shadow parity partitions.

The saved [report](phase27_parity_shadow_rank_check.json) records 801 original flags, 192 chambers, the panel distribution above, no original disconnected residue, and exactly twelve disconnected transformed residues, each with component sizes $[4,4]$. It also confirms that every flag of the transformed incidence system extends. This finite exhaustive check supports the preceding direct proof; it is not a finite-to-uniform argument or a Lean certificate.

Reproduce with:

```sh
python3 phase27_parity_shadow_rank_check.py --output /tmp/phase27-independent.json
```

## Complete repaired theorem and source reduction

I independently reviewed all nine sections of [phase27_parity_theory.md](phase27_parity_theory.md). The proof introduces the condition PC: for every higher-object flag, an intersection of nonbipartite individual shadows must remain nonbipartite. The following points are material to the approval.

1. **The truncation lemma has a proof.** Finite-rank induction on object residues first gives chamber-gallery connectivity. Restricting a gallery to at least two types then gives a connected truncation. This is valid for every residue and does not presume that a truncation is itself a residue. It is precisely what is required in the necessity argument for a higher flag that does not contain all higher types.
2. **The component lemma uses connected common shadows.** A selected component over a bipartite shadow restricts to one of the two components over each connected subshadow. Incidence of two selected components makes their restrictions agree over the connected pairwise shadow, hence also over the total flag shadow. Nonbipartite individual shadows impose no fiber restriction. This proves that the intersection always contains an edge, and proves exactly when it is connected.
3. **Geometry, residual connectivity and residue identification are separate.** Chamber extension works before PC is imposed. Under PC, the connected vertex truncation of a higher-flag residue connects every other object by chamber extension. Residues whose flags already contain a lifted vertex are identified directly with original residues. Conversely, failure of PC gives a disconnected truncation forbidden by the first lemma. In the stronger residue-transport statement, PC on the enlarged flags ensures that restricting individual components is bijective; compatibility of two such restrictions uses their connected common graph.
4. **Thinness and group conclusions respect the changed types.** A panel missing a new vertex type corresponds to an original panel missing the edge type. Panels missing a higher type correspond to the original panels of that type, while original panels missing the vertex type already have two completions by B1/B2. Natural automorphisms act faithfully because their action on vertices and higher objects determines the edges. In the bipartite case the correct acting group is the color-preserving subgroup, not the whole original group.
5. **The regular-marking bridge retains actual geometry.** Residue transitivity gives the local vertex graph on cosets of $Q_J$ in $U_J$. Its bipartiteness is equivalent to exclusion of $a$ from $H_J$ by the two-color character. The higher-flag condition becomes the coatom intersection condition for the upward family $\mathcal F$; finiteness of the type set then makes it equivalent to closure under all intersections. No assertion that a general C-group coset system is a geometry is used. Under PC the new thin, connected chamber geometry identifies the actual adjacent-chamber involutions and the full automorphism group.
6. **The Montero–Weiss adapter matches its stated target.** I reread [arXiv:2001.11082v1](https://arxiv.org/abs/2001.11082v1), §3, including Theorem 3.1, Proposition 3.2 and Corollary 3.3. I also checked the Piedade–Tranchida introduction's explicit interpretation of the nondegenerate hypothesis as a lattice face poset. In a lattice polytope an edge is the join of its distinct endpoints, giving B1 and B2. Higher faces of a flag form a chain, so their common shadow is the smallest one and PC follows. The new proof therefore recovers the C-group, actual flag-transitive coset geometry, regularity, full type-preserving automorphism group, and halved diagram conclusions for this source hypothesis. It does not retain the alternating semiregular-polytope flag-transitivity argument it replaces.

The final additions also pass. A thin infinite polygon has a bi-infinite path as its vertex graph; the selected double-cover component remains a bi-infinite path, retaining infinite endpoint order. For the all-$m$ counterexample family, the direct residue case split is exhaustive. I independently obtained $48m^2$ chambers and $162m^2+64m+25$ flags: there are 25 higher-only flags, $64m$ flags containing a vertex and no edge, and $6m^2\cdot27$ containing an edge. The panel multiplicities are $72m^2$ of size two, $24m$ of size $m$, and $12m$ of size $2m$, with coinciding sizes aggregated. These are written derivations; the independent executable here checks only $m=2$.

This is principal **construction** coverage of the cited Montero–Weiss §3 target, with the ordinary regular-polytope/hypertope and coset correspondences retained. It is not whole-paper coverage: the generalized-cube groups, exact orders, locally spherical examples and hyperbolic applications in §4 have not been rederived by this note. Nor does the proof establish that B1+B2 alone force PC for every regular leaf hypertope. The exact new conditional statement and the inspected broad source defect must remain separate.

All primary full texts and the source-page image remain private. No messages were sent to the paper's authors. Frozen phase26 files are unchanged.
