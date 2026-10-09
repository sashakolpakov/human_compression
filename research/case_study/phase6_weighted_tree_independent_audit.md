# Independent internal review: weighted-tree truncations

Date: 2026-10-10. Reviewer: the recent-conjectures agent, separate from the authoring root agent. This is an internal mathematical and implementation review, not external peer review or a literature-priority determination.

**Result:** no gap found in the stated model-level theorem or the finite checker. The exact Cara 2003 full-paper comparison is still unavailable; the reviewed note explicitly retains that limitation.

## Written proof

I read the complete [weighted-tree note](phase6_weighted_tree.md), including the following potentially delicate steps.

1. Pairwise coset incidence fixes all four Boolean atom sizes for a pair of cuts. Rooted tree cuts form a laminar family, and subtracting maximal selected children identifies equal-size atoms for an arbitrary flag. The bijections on these atoms assemble into a single permutation. Thus flag transitivity is proved rather than assumed. Weighted forest components also give the claimed subgroup intersections and residue factors.
2. Truncation keeps each retained edge's bipartition unchanged. Contracting omitted edges and assigning component sizes therefore preserves the actual parabolics and incidence, not just the diagram. Expansion of each positive weight gives the converse model construction. No unproved uniqueness of weighted parameters up to abstract isomorphism is claimed.
3. The subset-action primitivity argument handles equal blocks, unequal blocks and the exceptional pair (1,1). The potential unordered-block overgroup exists only for equal block sizes. In a positive weighted tree at most one edge bisects a component's total weight. This justifies the passage from the single-edge action test to residual weak primitivity in all higher residues.
4. For the adjacent-edge rank-two residue, disjoint a- and c-subsets of an (a+b+c)-set have binomial common-neighbor counts. An interior weight b>1 produces a genuine four-cycle, while b=1 permits at most one common neighbor on either side. The incidence graph is not a complete bipartite digon. Nonadjacent edge types do give digons. This proves the stated rank-two intersection criterion.
5. Branching gives the explicit weighted-claw obstruction to full shadow intersection. Two same-type subsets with overlap one below their size have a nontrivial proper common shadow. The three possible witness types are each excluded; a multi-element flag cannot repair this because each of its elements would have to be incident to both query elements.
6. For a path with internal weights one, retained subset ranks are consecutive. Every nonempty shadow is bounded by the union of lower query sets and the intersection of upper query sets; the boundary sets lie in the retained ranks whenever they are nonempty/proper. A singleton shadow has a one-element witness. Otherwise the two boundaries give a flag incident to the whole query family. Residues and joins are handled in the written proof. Rank-one exceptions are stated separately.

The proof distinguishes subgroup intersection, rank-two geometric intersection and the full residual shadow condition. It does not replace one of these by another without proof.

## Checker audit and independent execution

I read every function of [the checker](phase6_weighted_tree_check.py). It imports neither the proof nor any table or prior report. The checks use actual symmetric-group permutations for flag orbits, invariant-equivalence closure for subset-action primitivity, explicit incidence bitsets for common neighbors, and exhaustive searches over actual witness flags for the small full-shadow tests. These provide independent checks of the formulas. NetworkX is used to list nonisomorphic unlabelled trees; the script then tests weight compositions. The direct shadow sweep covers the required element-plus-flag queries, while the written Boolean theorem is stronger and covers arbitrary finite query families.

I executed a byte-identical copy in a disposable directory using Python with NetworkX 3.6.1. It exited successfully in about 4.3 seconds. The generated report was exactly equal as parsed JSON to the historical report, which was not modified. The [independent run record](phase6_weighted_tree_independent_run.json) preserves the observed result.

| Check | Observed count |
|---|---:|
| Direct subset-action tests | 28 |
| Weighted models / flag-orbit equalities | 89 |
| Flags | 57,630 |
| Residual primitivity checks | 741 |
| Rank-two models | 84 |
| Common-neighbor pairs | 216,590 |
| Full-shadow models / queries | 33 / 117,970 |
| Weighted-claw obstructions | 35 |
| Consecutive-rank shadow queries | 2,354,462 |
| Contraction models | 942 |

Scope remains finite: weighted models have total mass at most six, direct full-shadow models at most five, rank-two triples at most nine, claws at most eight, consecutive-rank models at most six, and unweighted contraction trees at most seven vertices. The all-parameter result depends on the written proof, not extrapolation from these checks. The finite sweep also does not replace the written residue-join argument.

## Formal scope

I read [ConsecutiveShadow.lean](formal/ConsecutiveShadow.lean), especially `exists_witness_in_consecutive_ranks`. Its hypotheses retain a nonempty shadow and a consecutive interval of proper Boolean ranks, and its conclusion provides the bounded witness within that interval. It imports the earlier Boolean-shadow theorem. I did not rerun Lean in this review; the root agent's separate saved compilation report records its successful compilation. The Lean theorem does not formalize the tree realization, primitivity classification, branching obstruction or residue joins.

## Reviewed hashes

| Artifact | SHA-256 |
|---|---|
| phase6_weighted_tree.md | `4b12222c91fd38df0e17575cd0765e649bb945ddcd83cb4da26e4d6bac81fd48` |
| phase6_weighted_tree_check.py | `1a7f52853fe1b3d196e1a04b4062f6ae43931018360bf80bd20f38fd2b409e36` |
| phase6_weighted_tree_check.json | `7b49414be782424832033efb7685c2c72d55c6aecbcadd89c7ff71a3dd2a835f` |
| phase6_weighted_tree_independent_run.json | `ac8aa5b2964c466dc2244358d5624c7e628c82154c07fee5b8d8bd55b2b82344` |

No source proof, checker or historical certificate was edited by this review.
