# Root review of the exact quotient-intersection certificate

10 October 2026. **PASS for the complete algebraic criterion and all four
formal declarations.** This adds one scoped Lean component, bringing the
prepared repository to forty. It changes no admitted source contract or ratio.

The root read the complete 5,391-byte Lean source, author explanation, manifest
and dedicated compiler runner. The source hash is
`3c305f16801690ee314fe0a68e5f53fc239e0eadefd5b8f9c7609ae16f6bca39`.
All frozen author files were checked against their manifest before export.
Context documents are provenance only; the Lean module imports only mathlib.

The forward proof takes `ab` in the kernel and a common lift `c` of `f(a)`
to factor `ab = (ac⁻¹)(cb)` through the two restricted kernels. Conversely,
factoring `ab⁻¹ = uv` yields the common lift `u⁻¹a = vb`. Thus the displayed
equivalence concerns actual images and subset products, with no missing
surjectivity condition. The quotient theorems instantiate the actual quotient
homomorphism and its proved kernel identity. The local-injectivity corollaries
derive the two trivial restricted kernels from the stated containment in `L`.
No normality of `L` is used or needed.

The root freshly ran the author's dedicated runner under Lean 4.32.2. It
checked all nine pinned dependency revisions and tracked-file cleanliness;
the build took 5.71 seconds and reproduced the exact author axiom log. The
[root replay report](phase53_cover_kernel_root_replay.json) and
[log](phase53_cover_kernel_root_replay.log) preserve this execution.

After exporting the exact source, the root freshly compiled it again through
the public general runner, with a new scratch output directory. The
[saved public report](formal/QuotientIntersectionCriterion.check.json) records
exit zero, no diagnostics and the same four axiom reports. Only `propext`,
`Classical.choice` and `Quot.sound` occur, with `Classical.choice` absent from
the first theorem. The pinned package cache and compiler remain trusted inputs;
these runs do not rebuild all dependencies or audit the compiler.

The public runner and Lake root list include the new module. Its
[scope document](formal/QuotientIntersectionCriterion.scope.md) states the exact
conclusion and boundaries. Previous saved reports and frozen author history
remain unchanged. The forty-component count comprises thirty-nine reports
without native-evaluation axioms and the earlier transfer component with four
explicit native-evaluation axioms.

The conditional cover theory is a separate written result and finite
certificate. This formal admission does not include its geometric recognition,
mirror-stability, support classification, central complement count, or global
cover conjecture. No current-open-problem or historical-priority claim follows.
