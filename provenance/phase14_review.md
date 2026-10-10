# Phase-fourteen review record

10 October 2026. This phase supplies a complete proposed cyclic-subgroup
TPP theorem for finite nilpotent groups and its consequence for the
published 2019 hypertope order conjecture. The [root review](../research/case_study/phase14_root_review.md)
and [bound record](../research/case_study/phase14_root_review.json) separate
written mathematical review, fresh computation and partial formalization.
The [first](../research/case_study/phase14_cyclic_tpp_audit.md) and
[second](../research/case_study/phase14_cyclic_tpp_independent_audit.md)
independent internal reviews also passed. These are internal reviews,
not external peer review.

The new proof uses two equivariant square maps and a marked-coordinate
obstruction. It removes the earlier finite census and marked-isobicyclic
classification dependencies. Lubotzky--Mann powerful-group structure and
elementary finite-p-group facts remain explicit inputs. The geometric
adapter retains actual flag transitivity, not only subgroup intersection.

The [dated status audit](../research/case_study/phase14_cyclic_tpp_status.md)
records 24 fresh searches and precise primary-source reading limits.
No later resolution was located, but the latest explicit open checkpoint
found remains the original 2019 conjecture. Current priority is unverified.
The living documentation therefore reports a complete proposed proof,
without assigning a verified-new-resolution infinity marker.

## Fresh Lean and finite checks

The eighteenth module, [marked square descent](../research/case_study/formal/MarkedSquareDescent.scope.md),
checks the finite commuting-action classification and abstract transport
obstruction. The public runner freshly compiled both
[BinaryFrattiniActions](../research/case_study/phase14_binary_frattini_public_compile.json)
and [MarkedSquareDescent](../research/case_study/phase14_marked_square_public_compile.json)
with the pinned Lean/mathlib setup, verifying dependency revisions and
tracked-file cleanliness. Both succeeded with no `sorryAx`. The complete
group and geometric arguments remain written proofs. All seventeen
earlier saved Lean reports are unchanged.

The [PSU4(7) witness](../research/case_study/phase14_unitary_q7.md) gives
type `{4,24,4}`. Root reviewed its matrix/order argument and reran the
original GAP checker in scratch space. The result matches the author
report except elapsed time: full order 1,165,572,172,800 and all 256
subgroup intersections pass. This is a fresh execution of the same
checker; no second finite-field backend is claimed. The retained upper
bound makes four the maximum rank at q=7. Uniform existence for
q congruent to three modulo four, q at least eleven, remains unresolved.

## Export and accounting

The [original-file manifest](phase14_original_files.json) records
byte-identical exports. Original draft/pending labels describe the
historical writing context; the bound reviews above record subsequent
internal review. Third-party full texts, superseded exploratory probes
and compiled Lean objects are excluded. Earlier original artifacts
remain unchanged.

The existing 127/38 approximately 3.34 matched-proof ratio and nine-work
principal-result ledger are unchanged. No whole-corpus ratio or complete
paper reduction is inferred from the conjecture proof. The detailed
introduction, paper registry and result table now state the stronger
theorem and the precise verification and priority boundaries.
