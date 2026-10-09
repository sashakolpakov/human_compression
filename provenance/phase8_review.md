# Phase-eight review record

10 October 2026. This phase completes the proposed PSL4 maximum-rank proof
and extends the older Suzuki construction analysis. The previous phase's
record remains historical: its unresolved rank-six boundary is superseded
by the new direct rank-six proof. Publication priority remains unverified.

## Maximum rank and the general form obstruction

The root read the complete [rank-six proof](../research/case_study/phase8_psl4_rank6.md)
and the earlier endpoint classifications it invokes. A separate agent
independently reviewed every new case and the structural corollary. Both
reviews found no gap. The new argument uses both middle generators' actual
commutations with three endpoints; it does not treat a rank-five parabolic
as if it generated the entire rank-six group.

In the reducible mixed-sign cases, every three-endpoint subset contains an
adjacent pair that commutes on one summand and has an invertible additive
commutator on the other. This forces both off-diagonal intertwining blocks
to vanish. The review checked all three sign patterns, their nonzero
determinant factors and their validity in every odd characteristic. It also
checked the tensor intertwiners, simultaneous splitting, larger Jordan
blocks and each pair of square-zero ranks.

The resulting theorem excludes rank six. Together with the frozen rank-five
proof, the earlier upper bound six and the retained published rank-four
construction, it supplies a complete proposed proof of maximum rank four
for every odd q. The same proof gives the stated bilinear-form alternative
for finite irreducible projective string actions in dimension four; the
noncommuting-adjacent-generator hypothesis remains explicit.

The drafting agent and separate reviewer ran the new symbolic checker.
Root then freshly reproduced all 33 identities and 12 distinguishing-pair
witnesses from the public files. The [root report](../research/case_study/phase8_psl4_rank6_root_check.json)
is separate from the two earlier executions. Root verified the artifact,
proof-dependency and formal-source hashes in the
[intake](../research/case_study/phase8_psl4_intake.json).

`IntertwinerSeparation.lean` was freshly compiled through the portable runner
with the pinned Lean and mathlib environment. Both general ring theorems
report no axioms. The formal implication requires the commuting pair and a
right inverse for the other additive commutator; the concrete normal forms,
their determinants, exhaustive coverage and complete group theorem remain
outside Lean. Earlier saved reports were not replaced.

## The older construction families

Root read all of [the pure-subfield and mixed-center proof](../research/case_study/phase8_suzuki_subfields.md).
The independent reviewer additionally inspected the primary page images
containing the RWPRI definition, intersection conventions and Constructions
10/11. Both reviews passed. A retained-input clarification explicitly added
the normalizer-of-center fact used to place the mixed parabolic in a Borel.

For the canonical pure-subfield family, the exact criterion is bottom
exponent greater than one. The repeated-prime boundary supplies the stated
rank-four example omitted from the literal construction list. The review
distinguishes that list from a possible enlargement by truncations.

For the mixed parabolic, the proof classifies its relevant overgroups by
scalar subspaces. The negative RWPRI conclusion uses only the prescribed
pairwise mixed-intersection types and holds for every such embedding. It
does not assert nonexistence of bare intersections or failure of flag
transitivity.

The drafting agent and independent reviewer executed the exact finite
checker. It verifies 49,152 matrix identities and nine strict intermediate
groups. Root reviewed the proof and artifact bindings, without claiming a
third execution of this finite computation. All artifact and prior-input
hashes in [the intake](../research/case_study/phase8_suzuki_subfields_intake.json)
match the distributed files. No full-text source is distributed.

## Status and limits

The dated [literature audit](../research/case_study/phase8_psl4_status_audit.md)
records what was actually searched and read. A negative bounded search does
not establish publication priority. Internal agent agreement is not external
peer review, and the new general theorems do not imply a reduction of dozens
of whole papers. The measurement rules retain these distinctions.
