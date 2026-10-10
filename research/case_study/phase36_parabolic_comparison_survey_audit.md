# Written review of the bounded-product parabolic comparison theorem

Reviewer: `survey_audit`. Date: 2026-10-10. Result: **PASS after the explicit index-set clarification in §2**. The companion JSON binds the final reviewed proof. This is a complete written mathematical review, with no new executable or formal-verification claim.

## Issue found and resolved

The exceptional case must be indexed by $E=I\setminus\{e\}$, rather than by equality of generated subgroups with $P_e$. Redundant markings may have $G_A=G_C=P_e$ for distinct index sets $A,C$, and their IP equality need not be tautological. For example, three copies of the same nonidentity generator of $C_2$ give $G_{\{1\}}=G_{\{2\}}=P_0$, but $G_{\{1\}\cap\{2\}}=1$.

The revised proof omits only the genuinely tautological indexed comparison $A=C=E$. In every other pair of proper index sets, at least one subgroup is contained in a protected parabolic. This fixes the proof while preserving the theorem's advertised scope of arbitrary indexed markings. It does not require independent or involutory generators.

## Both intersection-property directions

Since $B$ contains the identity and is inverse-closed, it is contained in $W=BB$. For a protected element $b$, membership of its image in an image marked subgroup lifts exactly: use the exceptional-membership hypothesis if the index set is $E$, and injectivity on $W$ with a protected lift otherwise. This argument does not assume IP in either group.

For every nonexceptional indexed pair, one entire subgroup lies in $B$. Its elements provide unique lifts of the image intersection, so the actual subgroup intersection and the generated intersection subgroup can be compared by the same injective restriction. Consequently both directions of the IP equivalence follow. Pairs involving the entire marking, and the single indexed pair $E,E$, are indeed tautological.

The separate intersection statement (C) is stronger than an IP rewrite: a common element of several image parabolics lifts through one protected parabolic, and each remaining membership follows from (M). This is an exact bijection of the actual intersections, even if neither marking satisfies IP.

## Product and coset checks

For products of two protected parabolics, lifting a factorization produces an element of $W$, where injectivity compares it with the given protected element. If the first factor is exceptional, the correct tested word is $g b^{-1}$ with $b$ in the second, protected factor. If the second factor is exceptional, it is $a^{-1}g$ with $a$ in the first, protected factor. Both words lie in $W$, and the exact exceptional-membership assumption proves the required equivalence in each orientation.

The anchored extension criterion (H) is equivalent to typed coset Helly for an arbitrary subgroup family. Necessity follows by applying Helly to the base parabolics and one additional coset. Sufficiency normalizes all but one member of a pairwise incident family using the induction hypothesis, then represents the remaining coset inside any chosen base parabolic. No subgroup-intersection formula is used in this induction.

With only one exceptional type, a base flag of at least two types has a protected anchor. Candidate representatives and common witnesses lift uniquely through that anchor, by (P) and (C). For right cosets, the final equality is exactly
\[
P_i g=P_i k\quad\Longleftrightarrow\quad gk^{-1}\in P_i.
\]
Both representatives lie in the same protected subgroup, so the last word lies in $B$ and (M) preserves its membership. Thus the premise and conclusion of (H) have the same truth values upstairs and downstairs. This proves both Helly directions without assuming either IP property.

## Quantifiers and application

The type set is finite; the groups and the exceptional subgroup need not be. The proof uses element witnesses and bijections, so it does not substitute finite cardinality arguments in the infinite case. Finiteness of the protected parabolics is used only when presenting the hypotheses as a finite certificate. The exceptional-membership hypothesis still concerns membership in the entire image subgroup, as the note explicitly requires.

For integral matrices the entry-difference bound $2C<n$ proves injectivity on the full product set. The bounded-test specialization is valid only with its stated necessity for every candidate word and every relevant modulus, together with a sufficient integral witness for every passing test. Those are the actual hypotheses supplied by the retained tensor certificate. Testing necessity alone or enumerating only selected words would not suffice.

The many-quotient consequence is also valid: all quotients compare to the same integral group, so no map between unrelated moduli is needed. The frozen tensor data supply $C=2$, $D=4$ and the exact bounded membership witnesses. The resulting comparison reaches the integral tensor marking as well as all indicated finite reductions. Arithmetic identification of the parameter and the marked local groups remain separate retained steps.

I previously authored the retained tensor model and reviewed/discussed its specific geometric transport. This review checks the parent's general theorem and both equivalences; it is not an independent discovery claim for the shared mechanism. No historical priority, general membership algorithm, complexity bound or complete formalization follows from this review.
