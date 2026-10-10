# Independent reading review: uniform label-eight triangularity

Reviewed source: `formal/LabelEightTriangular.lean`, SHA-256 `89be51e09e7465668e5c8390b3f5f5ceff009a14f4f19f2318d30950c0b82f64`.
Its literal rewrite-table dependency is `formal/LabelEightCriticalPairs.lean`, SHA-256 `22dce0b70cba3f4a9c9e3608bda7ee829e7d3d7352ec96d887e2a2b3a07a092d`.
Review date: 2026-10-10. Reviewer: the separate phase172 termination agent; the phase174 source was authored by the root agent. This is a semantic reading review, not a claim that the reviewer independently recompiled the file.

The reviewer read the complete source and the frozen imported table. The following five statements agree with the table and have the stated scope.

1. `square_tail_triangular` says that for rank `d >= 3`, every letter in the actual square replacement `rule d a a` is strictly higher than `a` and below `5*d-7`. There is no input-bound hypothesis. This is justified because a nonempty square replacement forces `decode d a` to have kind 1, namely an x-letter, whose replacement is the corresponding w-letter. The proof unfolds the actual definition and closes the resulting natural-number inequalities; it does not assume the conclusion.
2. `correction_triangular` assumes `b < a < 5*d-7` and proves the same strict upper-triangularity for every member of `correction d a b`. The case split is over the imported table, including all nonempty branches involving r-, x-, and y-letters. Natural subtraction in the index offsets is addressed by the arithmetic proof under `d >= 3`.
3. `rule_mem_bounds` combines the strict tail facts with the two retained letters in a swap. Its lower bound is `b <= c`, as required for the whole replacement, rather than the stronger and false claim that the retained letters also exceed `a`.
4. `uniform_step_preserves_range` handles the actual contextual `Step`, using the source-word bound to bound both input letters. Context letters retain their original bounds, and replacement letters use the previous lemma. The lower cutoff `lo` is arbitrary.
5. `uniform_reachable_preserves_range` extends that result along the actual reflexive transitive closure by induction. It does not assume normalization, sufficient fuel, or confluence.

These are the precise local arithmetic and closure hypotheses needed by a separate termination proof. The file itself does not prove termination, local confluence, confluence, existence or uniqueness of normal forms, a group-order formula, the intersection property, or the complete polytope construction. A root-run fresh compiler check supplies the build evidence separately. No whole-conjecture or historical-priority claim follows from this file.
