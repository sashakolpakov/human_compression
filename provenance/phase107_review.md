# General triangular rewriting and label-eight termination

The two new Lean modules prove a reusable termination theorem and its
actual label-eight application for every rank d >= 3. They include
existence of sufficient fuel for the implemented collector. The root
read both complete proofs and their scope, then freshly compiled all
four local dependencies from the public tree using the generic runner.

The [independent review](../research/case_study/phase178_termination_root_review.md),
[fresh build](../research/case_study/phase178_termination_public_build.json),
[author scope](../research/case_study/phase172_termination_scope.md) and
[exact export record](../research/case_study/phase178_termination_export.json)
bind eleven new and eight retained printed declarations. Every reported
axiom is standard. The pinned upstream Shortlex object was rebuilt in a
private overlay; other compiled dependencies remain trusted inputs.

There are now 69 scoped Lean components. This admission proves no numerical
fuel bound, all-rank confluence, group order, IP or complete polytope
theorem. No source or conjecture count changes.
