# Two-coset intersection obstruction

This module formalizes the B-with-B obstruction in the written endpoint-halving criterion. It is a separate additive companion; no previously frozen proof, example, runner or certificate is changed.

For arbitrary subgroups H≤K≤U of any group and a group element a, assume every x∈U belongs to H or can be written a·h with h∈H. Then `subgroup_eq_iff_representative` proves

    K = H  ↔  (a∈K → a∈H).

`intersection_eq_iff_representative` specializes this to H≤A,B and A∩B≤U:

    A ∩ B = H  ↔  (a∈A → a∈B → a∈H).

`excess_witness_forces_representative` explicitly transports any x∈(A∩B)\H to the witness a∈(A∩B)\H. The proof multiplies x by h⁻¹ when x=a·h. This handles both a genuine index-two interval and a collapsed one. Finiteness, normality, disjointness of the two cosets and even a separate hypothesis a∈U are unnecessary.

In the written marking theorem, substitute H=H_(I∩J), A=H_I, B=H_J and U=U_(I∩J). The normality/index argument there supplies U=H∪aH. Old subgroup IP supplies the two bounds. The Lean equivalence then says precisely that the meet is correct if and only if simultaneous recovery of a by I and J implies its recovery by I∩J. The derivation of those marking-specific hypotheses, the set-family/principal-filter statement and the other subset cases remain in the written proof.

The three theorems were checked by the Lean kernel using only `propext` and `Quot.sound`. No `sorry`, `native_decide`, finite data evaluation, assumed numerical identity or classical-choice axiom appears in their printed axiom lists. The saved fresh compile report binds the source hash and pinned Lean version.

Reproduction in the private research workspace:

    python3 research/leemans/formal/verify_lean.py TwoCosetIntersection.lean

The existing runner reads its pinned local dependency checkout. Only the new module's build product and report are written; the `.olean` build product is not an exported original. This certificate proves the abstract interval step, not the complete C-group/geometry theorem, any finite marking verification or a classification.
