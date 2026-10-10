# Scope of `ParabolicMarkedComparison.lean`

This new module completes the abstract marked-subgroup intersection-property part of the comparison theorem in `phase36_parabolic_comparison.md`. It imports the frozen `ParabolicProductComparison.lean`, which supplies the separately proved typed-coset Helly equivalence. No earlier source or compile report is changed.

The final actual-marking theorem formally proves **both directions of both properties**, with a proved connection between the source-generated subgroups and the image-generated subgroups. It is not merely a theorem about independently specified subgroup families assumed to agree. The geometric applications and arithmetic verification of the hypotheses remain outside the certificate.

## Definitions and exact assumptions

For an indexed family of subgroups `P : Set I → Subgroup G`, write

\[
P_i=P(I\setminus\{i\}),\quad
B=\bigcup_{i\ne e}P_i,\quad W=BB,
\]

where `e : I` is a distinguished exceptional index. `FullIntersection P` means

\[
P(S)\cap P(T)=P(S\cap T)\qquad(S,T\subseteq I).
\]

The abstract `full_intersection_iff` assumes that `P` is monotone and `P(univ)=top`, and that the homomorphism `f : G →* H` satisfies exactly the frozen product-comparison hypotheses:

1. `f` is injective on `W`;
2. for every `w ∈ W`, membership of `f(w)` in `f(P_e)` is equivalent to membership of `w` in `P_e`.

It proves full intersection upstairs if and only if full intersection holds for the family `S ↦ f(P(S))`. No intersection-property hypothesis is built into either of the two comparison assumptions.

The type set, groups and subgroups may be infinite. There is no assumption that individual markers are involutions, nonidentity, distinct, independent, or irredundant. In particular, distinct index sets may generate the same subgroup. There is no central, abelian or finite-kernel hypothesis.

## Why the indexed exception is handled correctly

The proof does not skip an arbitrary subgroup just because it happens to equal the exceptional subgroup. A proper set `S` is protected unless it is exactly the **index set** `I \ {e}`: every other proper set omits a nonexceptional index and hence its subgroup lies in a protected maximal subgroup.

`proper_member_image_iff` therefore reflects membership of a protected element in every properly indexed subgroup. `all_image_meets` proves

\[
f(P(S)\cap P(T))=f(P(S))\cap f(P(T))
\]

for all pairs, before assuming IP. If either index set is full, monotonicity makes the meet tautological. Otherwise at least one side is protected unless **both index sets** equal `I \ {e}`. Only that last indexed pair is discharged as a self-intersection. This remains valid for redundant markings and even when a different indexed subgroup has the same underlying group as the exceptional one.

Source IP now implies image IP by applying `all_image_meets`. Image IP implies source IP by the already proved one-exceptional-parabolic transport, whose required injectivity is derived from injectivity on `W`. The new `full_comparison` pairs this result with the frozen typed-Helly equivalence; it does not infer either property from the other.

## Actual markings and target generation

`MarkedSubgroup r S` is defined literally as

\[
\operatorname{Subgroup.closure}(r(S)).
\]

The module proves its monotonicity and the exact identity

\[
f(\langle r_i:i\in S\rangle)
=\langle f(r_i):i\in S\rangle.
\]

Consequently `marking_comparison` gives both equivalences for an actual source marking and its elementwise image, assuming the source marking generates `G`. No surjectivity is required here: the image marking generates the image of `f`, which may be a proper subgroup of `H`.

The separate `quotient_marking_comparison` adds `Function.Surjective f`. Its first conclusion proves that the image marking generates **all of `H`**; its other conclusions give the IP and typed-Helly equivalences for those actual markings. This is the precise generated-quotient setting of the written comparison theorem. It holds without a finite-rank or minimum-three-types restriction.

The imported typed-Helly definition quantifies over every selected set of types and every pairwise intersecting family of right cosets in the relevant ambient group. It is not restricted to finite flags. The previous direct anchored proof supplies this stronger scope.

## Execution and trust

All four modules in the import chain were freshly compiled in order in a disposable stage: `ParabolicQuotientTransport`, `OneExceptionalParabolic`, `ParabolicProductComparison`, and finally `ParabolicMarkedComparison`. The last source was recompiled after fixing two elaboration details; the saved final report is warning-free and successful. No failed run or placeholder theorem is accepted as a certificate.

Lean version is 4.32.2, with mathlib revision `905b95818eb32af7874a58b427f50c1711a5e96c`. The exact original-source hashes, final reports, runner and verified package revisions are bound in `phase37_parabolic_marked_formal_run.json` and `phase37_parabolic_marked_formal_manifest.json`. All seven substantive printed theorem audits use only `propext`, `Classical.choice` and `Quot.sound`. There are no added axioms, `sorry`, or `native_decide` calls in the source. Ordinary kernel and pinned-library trust remain.

## Not certified here

The theorem assumes injectivity on the protected product set and the complete exceptional-membership test. It neither supplies an algorithm for those tasks nor replaces their proofs in a particular matrix model. The finite tensor computations, Fibonacci parameter orders, toroidal local presentations, thinness, residual connectedness and hypertope identifications remain separate written/executable results. This certificate adds no source-priority or manuscript-compression claim.
