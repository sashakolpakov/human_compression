# Independent review of the tree-cut derivation

10 October 2026. **PASS for the written derivation and its stated scope.** This is an independent mathematical review, not a claim of external peer review or a complete Lean proof.

Reviewed proof SHA-256:

`0f5d0535f02d4f20cc9a59c7194e8fe666d4a7b6e7d449c85902693161db346f`

## Mathematical checks

* **Forest intersections:** intersections of component partitions give the components of the common edge set because a tree has a unique path between two vertices. The argument would fail for a general graph, so the tree hypothesis is essential and correctly retained.
* **Laminar incidence and flag transitivity:** the intersection cardinalities force exactly the original nesting/disjointness relations. Subtracting maximal selected subcontainers gives disjoint atoms of equal sizes in the original and proposed families. Independent bijections on these atoms combine into one permutation, for partial flags as well as chambers.
* **Primitivity and QPRI:** an element outside the unordered two-block stabilizer creates a cross-block transposition after conjugation of the within-block transpositions. Their support graph becomes connected, generating the full symmetric group. Unequal blocks therefore give a maximal stabilizer; equal blocks of size at least two give precisely the stated two-step subgroup chain. The N=2 exception is needed and is present. The leaf-cut argument in each product residue and the three-edge-path obstruction establish the RWPRI and RPRI claims.
* **Shadow-IP:** in the claw, no eligible vertex can witness the two-point shadow, including vertices of the target type. For the path, the union/intersection bounds yield either a point witness or the stated two-vertex flag; both vertices are incident with every member of the original query family. Empty and full shadows, omitted boundary sets, and rank-one factors are handled correctly. The join-of-intervals argument supplies the residue step; subgroup-IP is not substituted for shadow-IP.
* **Graph reconstruction:** unique maximal-clique ownership excludes multiple edges. A cycle of length at least four gives an induced cycle on its edge labels in the diagram. A triangle would force the same diagram edge into two maximal cliques. Reconstruction from clique vertices and leaf edges is therefore a tree and is inverse to its line graph, with the single-edge exception treated separately.

The exact 1998 definitions and foundational lemma were checked in the [author-uploaded full text](https://www.researchgate.net/publication/29655192_Some_properties_of_inductively_minimal_geometries) exposed by web search. Minimality uses the bound |G|≤(r+1)!, so the connected m-edge residue with group Sym(m+1) satisfies it exactly. QPRI is the unique-chain condition used by the proof. The retained 1997 classification and the already-known Cameron–Cara tree model remain explicit dependencies. The 2001 paper's complete text was not obtained; search fragments do not change that access limitation.

## Finite checker boundary

The existing PASS report and the checker source were inspected; its script hash matches:

`ac0a595730d46a2c3ff2bab69e2106b83d86bc5d9603a23157a91489e320aa55`

The report hash is:

`c2ae6ae0c8874e3fc8df85330ade35047c5378a0cf4f37a341f45de83cdf295b`

The report records 24 trees on 2–7 vertices, 52,116 partition meets, 262 exact generated subgroup closures, 7,060 group meets, 28,324 flag comparisons, and 1,519,962 Boolean shadow queries. Exact group and flag comparisons stop at six vertices. The explicit claw failure passes. NetworkX 3.6.1 supplies only the unlabelled tree list.

These checks support the finite implementation. The all-size primitivity, QPRI, reconstruction, and residue claims rely on the reviewed written proofs; they are not inferred from the finite counts. This review inspected the already completed run rather than repeating it.
