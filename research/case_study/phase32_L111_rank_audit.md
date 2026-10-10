# Independent review of the L111 finite-rank adapter

10 October 2026. **PASS for the stated finite-rank Theorem 4.1 reduction.** This is internal review, not external peer review or a whole-paper claim.

The reviewed [proof](phase32_L111_theory.md) has SHA256 `75867219d30985bcdc6dda0372d6e1c19103054ec689b08f1c0bb9daff0db2a5`. I read every section and the full checker. A fresh execution reproduced the saved report byte for byte; the independent output is [phase32_L111_rank_run.json](phase32_L111_rank_run.json).

## Mathematical review

The exact chamber bijection uses the endpoint opposite the distinguished original vertex. Its inverse is unique because the graph is simple. All new flags extend: the cases of zero, one and two copied vertices require respectively an old higher flag, an old vertex flag, and an old edge flag. Endpoint incidence is used explicitly in the last case.

The copied-vertex residue is the original vertex residue with incident edges relabelled by their opposite endpoints. Restricting that map handles two copied vertices. Higher-only flags give the same construction on their old residue. In the reverse residual-connectivity implication, the old edge-only residue is an additional necessary case; its two endpoints meet every remaining object, so its graph is connected whenever its rank is at least two. No original residue is omitted.

For higher-only residues of rank at least three, the two copies of a vertex connect through a higher object. This is supplied by chamber extension even when the graph truncation itself is disconnected. Removing old edge-objects and subdividing endpoint adjacencies preserves connected components, because their higher incidences add no new component identifications. At rank two, the exact obstruction is the disconnected bipartite double of a bipartite graph.

Finite-rank gallery induction justifies the equivalence with the stated strong-connectivity convention. It is applied in every residue, and does not assume an infinite-rank induction. The diagram-class table is surjective as well as injective: each old complementary flag supplies the corresponding new flag. The automorphism assertion preserves the designated action, its kernel and chamber orbits; it correctly refrains from identifying full automorphism groups. Both incidence conditions persist at a disjoint pair, and the two literal replacement operations commute. Neither fact alone guarantees residual connectivity after a second replacement.

Finally, in the positive case, every common higher shadow is connected and contains a smaller odd-cycle shadow. Its parity monodromy is therefore all of C2. Thus the earlier cover theorem recovers the forward implication without replacing unsplit source objects by a different component-splitting construction.

## Primary-source and finite-evidence limits

I independently queried the [author-uploaded primary indexed text](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes) and read the full verbal Theorem 4.1 on printed p.590 and Construction 5.1 on pp.591–592, with their adjacent incidence discussion. The finite-rank target and its three conclusions match the adapter. I did not obtain a complete PDF or visually reconstruct the garbled diagrams. The source's stricter graph convention remains explicit; the broader one-edge diagnostic is not counted as satisfying it.

The fresh standard-library replay passed 316 graph/subset cases, 12,628 residue isomorphisms and 26,802 flag checks; it also reproduced the separate action and iteration examples. These are bounded diagnostics. The uniform theorem rests on the written proof above. No source application table, infinite-rank statement, Corollary 4.1 hypothesis conversion, full automorphism-group equality, or complete-paper reduction is credited.
