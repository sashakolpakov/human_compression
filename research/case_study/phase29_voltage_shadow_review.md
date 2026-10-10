# Independent written review of the graph-cover theorem

Review date: 10 October 2026. This is an internal mathematical review, not external peer review or a publication-priority determination. The accompanying JSON binds the exact reviewed `phase28_voltage_shadow_theory.md` bytes.

I read the full note, §§1–9. No mathematical gap was found in the stated hypotheses and conclusions. In particular:

- All shadow graphs are connected by the finite-rank connected-truncation argument and contain an edge by chamber extension. Those facts are required for transporting intersections to a common fiber.
- With voltage multiplication on the right, component fibers are left cosets gH. Pairwise component intersections can be transported to the same chosen base vertex along a path in the connected common shadow.
- A nonempty fiber intersection is g(⋂H_i). Its common-shadow components correspond to left cosets of H_F inside ⋂H_i. Normality is unnecessary; h⁻¹h'∈H_F is the correct relation.
- Typed coset Helly is exactly the flag-extension obstruction in both constructions. Lower-object flags extend using unique edge lifting and the stated base B1/B2 conditions.
- The vertex/edge residue identifications are valid. For the bipartite compression, the remaining lower type can be relabeled; panels missing an original vertex already have two completions by B1.
- Residual-connectivity necessity correctly uses connected two-type truncations of every residue. A disconnected lower truncation alone would not imply that the full residue graph is disconnected.
- The group-action section states liftability explicitly. In the nonbipartite-base/bipartite-cover case, the deck action must exchange colors, since otherwise the base would inherit a bipartition. The color-preserving lift group therefore surjects onto the given base group and has the claimed chamber action.
- The parity specialization is restricted to the canonical all-edges-odd cover. It does not incorrectly infer bipartiteness from monodromy in an arbitrary double cover.

This review does not claim a fresh execution of the phase28 finite checker or an independent reading of the cited primary voltage-graph paper. Its written proof is self-contained for the covering fact used here. The separate new Lean module `formal/Phase29CosetMonodromy.lean` checks only the algebraic common-fiber/subgroup obstruction, with the narrower boundary in its scope file. That formal companion is new proof development, not a claim that the whole graph-cover theorem has been formalized.
