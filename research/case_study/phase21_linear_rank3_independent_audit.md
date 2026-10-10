# Independent review of the linear rank-three construction

10 October 2026. Internal mathematical review by the survey/source-audit agent, separately from the construction's author. Verdict: **PASS — no mathematical gap found in the full written argument**, conditional on its explicitly retained classical group inputs. This is neither external peer review nor a publication-priority determination.

Reviewed proof: `phase21_linear_rank3.md`, SHA256 `d9e4b7abc1ee7d28aede897a55fcbef39aa1504254eee025cadbe2fc7aea955a`.

## Full argument checked

1. **Matrices and projective scope.** The endpoint A squares to the primitive nonsquare scalar nu; C anticommutes with it; B is an involutory reflection. The corrected Av=(0,1,nu,0) excludes ordinary commutation with B, and the unequal 3+1 eigenspace dimensions exclude anticommutation. Determinants nu^2,-1,1 generate exactly the order-two subgroup in the determinant quotient, including q congruent to 3 modulo 4. The proof claims linear SL4 containment before passing projectively, so no scalar-lifting step is silently presumed.

2. **Both rank-one projections.** The opposite unipotents have distinct fixed lines and nontrivial order p. Trace-square differences 128nu and 128/nu generate the full field in every odd characteristic. This excludes conjugate proper subfield groups, including PGL subfield groups; ordinary traces would not suffice for that projective argument. The A4/S4/A5 exceptions are separated correctly: p>=7 by element orders, p=5 by trace field or equality with the whole target at q=5, and p=3 by trace field with the sole q=9 case checked explicitly. For q=9, a primitive w satisfies w^2=sw+1 with s=+/-1; one displayed trace-square is 2 and gives projective order four, excluding A5. The trace field excludes A4 and S4. The central lift from PSL2 to SL2 uses perfection at q>=5, with no unsupported complement assertion.

3. **Independent factors.** Goursat is applied only after quotienting both centers to the simple PSL2 factors. An automorphism graph would force the same Frobenius power in the two word equations; their difference implies nu^(p^k+1)=1. The elementary bound p^k+1<q-1 holds also at q=5 and q=9. Perfection then removes the possible central correlation in the linear subdirect product. The exceptional abstract isomorphism PSL2(9)=A6 does not invalidate the stated full automorphism group.

4. **Nonzero and full radical.** If the additive kernel vanished, the unique lift of the central element (-I,I) would centralize U and split the four-dimensional space into two invariant two-dimensional eigenspaces. A unipotent on this split space has no block of length three, contradicting the exact nilpotent-square calculation. Once the kernel is nonzero, the double root-difference identity extracts a complete F-line from one nonzero matrix entry without assuming initial F-linearity. Independent left/right Weyl actions yield all matrix units. The action factors through the diagonal image because the radical is abelian, and subtracting radical blocks then gives the actual standard Levi subgroup.

5. **Generation and intersection.** The conjugate Q(s) and its root commutator provide x43; the following three elementary commutators give the missing roots. Their denominators require only odd characteristic and nu nonzero. All twelve root groups generate SL4 by elimination. The product bc has exact order 2p, including p=3. The retained elementary same-marking rank-three proof was reread in phase20 Section 6: both rotation/rotation and mixed rotation/reflection cases produce a cyclic normal subgroup, so the absence of such a subgroup gives actual IP for this marking. This is stronger than merely citing an existence-only intersection theorem and is justified here.

6. **Final rank set.** The new argument covers q>=5. The q=3 rank-three statement is explicitly retained from the 2025 published PGL theorem. The phase16 rank-four construction states all odd q>=3, and supplies the q=3 parameter h=1; the separate phase9 upper bound excludes higher rank. Nonabelian almost-simple groups cannot have rank one or two. Thus the stated diagonal-family rank set {3,4} has the displayed dependency chain; no conclusion for field/graph extensions follows.

## Primary inputs actually inspected

The Dickson list was reread in the cached primary Leemans–Moerenhout–O'Reilly-Regueiro paper, Proposition 2.3, extraction `sources/psl2_chiral2017.txt`, lines 206–220. The cited Guralnick–Zieve author PDF was independently opened online: [Appendix, printed p. 42](https://websites.umich.edu/~zieve/papers/gz.pdf), immediately before Lemma A.5, explicitly gives Aut(PSL2(q))=PΓL2(q). Only those relevant appendix paragraphs were read, not the full monodromy paper. Simplicity, perfection, Dickson and elementary generation remain retained classical inputs rather than independently formalized theorems.

The prior [2025 linear intake](phase20_linear_rank3_intake.md) establishes that the q congruent to 3 modulo 4 existence cases are published input. This review neither repeats a full current-status search nor establishes novelty for q congruent to 1 modulo 4.

## Exact-check scope

The author symbolic checker was read in full and freshly executed from a temporary copy. All **34 exact identities** passed, including the q=9 polynomial reductions; the new report matches the saved author report after excluding its timestamp. The run is recorded in `phase21_linear_rank3_independent_symbolic_run.json`. These identities are in the localized rational polynomial ring, with exceptional small-characteristic issues separately handled in the written argument.

The six-field GAP checker and saved log were read, but **not rerun in this review**. Their stated scope is q=5,7,9,13,17,25, 48 marked subgroup closures and 384 meets; this corroborates rather than proves the all-field theorem. The order sandwich and determinant containment in that script correctly identify the projective target without a recognition oracle. No new Lean verification is claimed.
