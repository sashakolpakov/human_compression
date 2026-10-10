# Quadratic relations and interval cancellation in Lean

Four new scoped modules have complete independent proof reviews and fresh
pinned compilations. The
[source-relator review](../research/case_study/phase151_source_relators_root_review.md)
covers the all-integer ambient quadratic relation and the bidirectional
label-four relation equivalence. The
[interval review](../research/case_study/phase155_interval_overlap_root_review.md)
covers interval-overlap cancellation and its finite-marker adapter.

Root read all four implementations, their scope notes and written
interfaces. Fresh dedicated builds passed, as did all 23 input-mutation
and occupied-path controls. The interval core and adapter also passed
isolated portable replays. All four exported sources then compiled with
the public generic runner; the adapter imports the newly compiled core.
The 34 audited declarations use only standard axioms. The compiler and
remaining cached package objects are trusted, with two missing Mathlib
objects freshly built for the quadratic module.

There are now **51 scoped Lean components**: 50 without native-evaluation
axioms and one historical supplement with four recorded such axioms.
The adapter is a representation bridge, not a separate research result.
Old saved reports and frozen author packages are unchanged. The
[export record](../research/case_study/phase155_question_formal_public_export.json)
binds the new public artifacts.

This admission adds no source coverage, resolved-conjecture count,
priority claim or compression factor. Finite-field selection, retained
presentation and generation theorems, the parity-mixing group consumer,
and the complete polytope conclusions remain outside these four proofs.
