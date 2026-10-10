# Exact criterion for quotient intersections

10 October 2026. Root complete source review and two fresh compiler runs pass
for the frozen author module. The second run uses the public general runner.

For any group homomorphism `f : H →* G`, subgroups `A,B ≤ H`, and
`N = ker(f)`, the module proves the complete equivalence

    f(A) ∩ f(B) = f(A ∩ B)  iff  N ∩ AB = (N ∩ A)(N ∩ B).

Here every product is a product of subsets, not a subgroup join. The statement
has no finiteness, centrality, surjectivity or image-intersection hypothesis.
It also specializes to the actual quotient map `H → H/M` for any normal `M`.

If `N ≤ L` and `L ∩ A = L ∩ B = {1}`, write `D = L ∩ AB`. The other two
theorems prove the equivalent criterion `N ∩ D = {1}`, both for an arbitrary
homomorphism and for an actual quotient by normal `M ≤ L`. Normality of `L`
is unnecessary for these algebraic statements. In general `D` is a subset,
not a subgroup or a vector subspace.

The four declarations in namespace `MathCompression.QuotientIntersectionCriterion`
are `image_inf_iff_kernel_product`, `quotient_inf_iff_kernel_product`,
`image_inf_iff_trivial_defect`, and `quotient_inf_iff_trivial_defect`.
The proof constructs factorizations and common lifts explicitly; it does not
assume the desired equivalence as a premise. Only pinned mathlib is imported.

From the repository root, with the dependencies installed as described in the
[formal instructions](README.md), run:

```sh
python3 research/case_study/formal/verify_lean.py QuotientIntersectionCriterion.lean
```

The [saved public build](QuotientIntersectionCriterion.check.json) and
[root audit](../phase53_cover_kernel_root_audit.md) record fresh Lean 4.32.2
compilation, exact dependency revisions and all four axiom reports. The first
theorem uses `propext` and `Quot.sound`; the others also use `Classical.choice`.
No unproved placeholders or native-evaluation axioms occur. Existing compiled
dependency objects remain trusted inputs.

This certificate covers the algebraic intersection criterion only. Polytope
recognition, mirror invariance, cover minimality, module support classification,
central-kernel counting and source-specific finite computations remain outside
its scope. It supplies no new manuscript count, length ratio or conjecture
resolution. The author's frozen manifest retains its earlier pending-review
status; this scope and the root audit are additive review records.
