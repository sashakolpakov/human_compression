# Scope of `ParabolicProductComparison.lean`

This is a partial formal certificate for the written parabolic-product comparison theorem in `phase36_parabolic_comparison.md`. It proves the complete typed-coset Helly equivalence, including its membership, product and image-intersection ingredients. It does **not** formalize the separate full marked-subgroup intersection-property equivalence, the matrix arithmetic certificate, any local toroidal-group identification, or the resulting hypertope assertions.

## Exact interface

Let `P : I → Subgroup G`, let `e : I` be a distinguished type, and let `f : G →* H` be a group homomorphism. Set

\[
B=\bigcup_{i\ne e}P_i,\qquad W=BB.
\]

`Protected P e x` means `x ∈ B`, and `Footprint P e x` means `x ∈ W`. The two assumptions of the final theorem are:

1. `f` is injective on the set `W`;
2. for each `w ∈ W`, `f w ∈ (P e).map f` if and only if `w ∈ P e`.

Under precisely these assumptions, `typed_helly_iff` proves

\[
\operatorname{TypedCosetHelly}(P)
\quad\Longleftrightarrow\quad
\operatorname{TypedCosetHelly}(i\mapsto f(P_i)).
\]

The imported definition quantifies over every selected set of types `S : Set I`, every family of group elements indexed by `I`, and all pairwise intersections of their right cosets. It requires one common point for the whole family. It is not a finite-flag surrogate.

There is no finiteness assumption on either group, the type set, the selected family, or any subgroup. There is no global surjectivity assumption on `f`, no involution marking, and no assumption on its kernel being central or abelian. Target parabolics are exactly the subgroup images. The presence of a distinguished type makes `I` nonempty; if there is no protected type, the selected families have at most one type and the theorem still applies.

## Proof components checked by Lean

* `member_image_iff` reflects membership in every parabolic for an element of `B`.
* `protected_injective` proves injectivity on each nonexceptional parabolic from the product-set assumption.
* `image_meet` proves `f(P_i ∩ P_j) = f(P_i) ∩ f(P_j)` for every pair of types, without assuming full marked IP.
* `product_comparison` reflects membership in `P_i P_j` for `i ≠ j` and an element of `B`. Its exceptional-factor cases use the exact exceptional-membership assumption on a product in `W`.
* `coset_pair_iff_product` identifies intersection of the right cosets `A g` and `B h` with membership of `g h⁻¹` in `A B`.
* `typed_helly_descent` chooses one protected anchor and simultaneously lifts normalized representatives for every selected type. The normalized pair differences lie in that protected subgroup. Product comparison makes the lifted source cosets pairwise incident; source Helly gives a common point whose image solves the original target family. This uses choice, not induction over a finite set.
* `typed_helly_iff` combines that descent with the previously formalized one-exceptional-parabolic lifting theorem, using the newly proved image-meet and protected-injectivity statements.

Thus the formal statement is somewhat more general than the finite-indexed formulation of the written comparison note. This extension concerns typed coset Helly only; it does not silently enlarge the unformalized marked-IP or geometry claims.

## Dependencies, execution and trust boundary

The module imports `OneExceptionalParabolic.lean`, which imports `ParabolicQuotientTransport.lean`. Both unchanged dependency sources were freshly compiled in a disposable stage before the final module. No historical compile report, frozen source, public runner or public manifest was edited. The exact source, runner, pinned package revisions, fresh dependency results and final result are bound in `phase36_parabolic_comparison_formal_run.json` and the formal package manifest.

The final warning-free compilation used Lean 4.32.2 with mathlib revision `905b95818eb32af7874a58b427f50c1711a5e96c`; all nine package revisions were independently checked against the existing dependency manifest. The source has no `sorry`, added axioms or `native_decide`. The six substantive printed theorem audits report only `propext`, `Classical.choice` and `Quot.sound`; `coset_pair_iff_product` uses `propext` alone. Ordinary Lean kernel and pinned-library trust remain.

The saved `ParabolicProductComparison.check.json` is the actual final compile report. This is a genuine abstract theorem proof, not an assumption of the numerical tensor certificate and not a proof of the entire geometric construction.
