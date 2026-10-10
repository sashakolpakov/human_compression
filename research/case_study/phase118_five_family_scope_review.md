# Independent review of the five-family synthesis and attribution

10 October 2026. **PASS for the exact author-source scope, presentation conversion, synthesis and bounded attribution. No [O] approval, historical-priority finding or current-openness certification.** No required correction to the frozen phase113 package was found.

The reviewed manifest is `phase113_five_family_priority_manifest.json`, SHA256 `fca2b96e47bbd74c2f6667166b6c0ed424b4e2fd67ebfc3cebe6b0417b005ba6`; the complete report has SHA256 `7f4d710069c389569a0b17864422e2c5582f3519edbac65da87dff7b0a6d6831`. I read the report, coverage map, source ledger and query record in full and verified all 26 original bindings, including the manifest itself. The source PDFs, extracts, source-page images and browser captures remain private and are excluded from this review's export allowlist.

Phase113 accurately records that phase112 was pending when it was drafted. That frozen historical statement is preserved. The separate phase112 review is now **PASS without required correction**, at manifest SHA256 `7e3036ad90298161c223e73a13b0576526360ef887b836268628faa5b6c6069e`. It independently assessed the complete phase109 uniform proof and recomputed the two finite constructions. This additive state update does not turn phase113 into another construction replay and does not settle its priority gate.

## Exact target and source rows

I reread Example 3.5, the complete §4 and the references in the bound July 25, 2023 author PDF of Cunningham's *Chiral polytopes whose smallest regular cover is a polytope* (printed pages 6–8 for §4 and references). The definite assertion supported by the final conjectural sentence is multiplicity: every member of the five specified families should have at least two distinct minimal regular polytopal covers. The preceding example has two degree-three covers, but the sentence does not impose that degree or that exact construction on every family. Phase113 uses the narrower defensible interpretation. [Checked author source](https://gabrielcunningham.com/WhichChiralPolytopes.pdf).

I freshly rendered and visually inspected the original Table 4 on page 40 of Cunningham–Pellicer's arXiv:2009.04566v1. It has three regular-facet rows followed by exactly these five chiral-facet rows:

| Row | Ordered type | Complete parameter contract | Reviewed proof |
|---|---|---|---|
| 4 | {2m,m^α,2m} | m odd prime, α≥2, 1≤k≤m−1 | phase49/59/67 |
| 5 | {8,2^β,8} | β≥5, both independent signs | phase109/112 |
| 6 | {2^(β−1),2^β,2^(β−1)} | β≥5, both independent signs | phase109/112 |
| 7 | {8,2^β,2^(β−1)} | β≥5, both independent signs | phase109/112 |
| 8 | {2^(β−1),2^β,8} | β≥5, both independent signs, exchanged on duality | phase109/112 |

The source text immediately before Theorem 5.14 identifies the last two rows as a dual pair, and obtains eleven atomic families by also adjoining the duals of the first three regular-facet rows. Hence the five-row proposal is not a claim about all eleven rows or every tight chiral polytope. Theorem 4.7's equal-parameter condition is necessary for Γ1 to have the stated source-polytope contract; it is not an omitted valid unequal-parameter subfamily. The α=2, m=3 and β=5 endpoints are included. The source contains no m=2, k=0 or β<5 case within these five contracts. [Checked classification author version](https://arxiv.org/pdf/2009.04566v1).

The exact table comparison is against the author edition. The later paper references the journal edition's Table 4 and a different proposition number. Neither phase113 nor this review claims an unperformed collation of the complete publisher editions. That edition boundary remains visible in any admission wording.

## Presentation conversion and duality

I independently checked both directions of the algebra in phase113. From (ab)^2=1 one has b^-1=a b a and b=a^-1 b^-1 a^-1. Thus ba²=a²b^(1+e) gives

`b^-1 a = a³ b^(1+e)`.

The inverse of 1+e modulo q is 1−e because e²≡0 mod q. Reordering the same conjugation relation gives b^-1a^-2=a^-2b^(-1+e), and consequently

`b a^-1 = a^-3 b^(-1+e)`.

Conversely, multiplying the first displayed equality by a^-1 on the left, and using a^-1b^-1=ba, recovers ba²=a²b^(1+e). The second rewrite introduces no additional constraint. This holds for e=k m^(α−1), α≥2, and for e=ε2^(β−2), β≥5, since the required square divisibility holds in both entire ranges.

Putting u=c^-1, v=b^-1 converts the right relation to exactly the same left relation. Inverting the resulting two equalities yields the two Table 4 right words, in the reversed order displayed in phase113. The Γ3 words already agree literally. Powers and rotation-square relations are unchanged. Thus the presentation identification uses the actual marks and relations; matching types or abstract group orders alone is not doing the work.

Under marked duality `(a,b,c)→(c^-1,b^-1,a^-1)`, the two end parameters are exchanged without changing either sign. The right Γ3 pair inverts to the left pair in reverse order; the Γ2-type end relation also converts exactly as above. Therefore every sign pair in the dual mixed row is obtained from the reversed pair in Γ4. All four sign pairs remain covered. This does not assert that every sign choice is a different isomorphism class or that unequal-sign Γ2/Γ3 members are individually self-dual. The five ordered-type rows represent four families up to rank reversal, with Γ4 and its dual forming the one mixed pair. The proposal and the distinct-cover results use rank-preserving isomorphisms.

## Synthesis after the independent mathematical review

The now separately accepted phase109/112 proof, together with phase49/59/67, covers all five author-source rows at every valid parameter. For Γ1 the two exhibited covers are themselves globally minimal, each of degree m over the smallest regular maniplex. Their different kernel actions distinguish the rank-preserving covers even though they are dual.

For each two-primary row, phase109 constructs covers of degrees 3^34 and 5^34. Maximal admissible normal-kernel descent gives globally minimal quotients of degrees 3^d and 5^e, with 1≤d,e≤34. Different positive prime-power degrees imply distinct covers. The exact exponents and quotient kernels are not selected, and the large constructed covers are not proved minimal. Phase113 preserves this important difference.

The family-specific join-density statements are also present in their bound proofs: phase49 uses the two independent axes in its common Cp² cover, and phase109 uses the coprime indices of the two universal kernels. Neither conclusion propagates automatically upward along Theorem 5.14's atomic quotient map. In particular the synthesis establishes no statement for every non-atomic tight chiral polytope, and no arbitrary-polytope multiplicity theorem.

The separate 2016 author *Open problems on k-orbit polytopes*, Problem 5, was reread with the surrounding covering discussion on page 8. It allows arbitrary polytopes and asks about unique minimal regular polytopal covers with nonpolytopal monodromy. The five-family result does not decide that broader problem. Historical conjectural wording in either source is not evidence of current openness. [Checked problem source](https://arxiv.org/pdf/1608.07993v1).

## Attribution and later literature comparison

I read the entire §6 of the bound Cunningham–Hubard 2025v1 PDF, including all statements, proofs, examples and its three concluding problems. The characterization in Theorem 6.3 and Corollary 6.6 genuinely supplies the general local-polytopality and variance-intersection framework. Proposition 6.5 supplies the facet-cover shortcut; its application to Γ1 was already independently explained in phase82. Corollary 6.17 recovers the chiral smallest-cover criterion. These are attributed background results rather than new principles of the family synthesis. [Checked mix paper](https://arxiv.org/pdf/2506.19334v1).

The displayed §6 results do not themselves provide the two fixed affine witnesses, verify their intersections, prove the exact marked quotient from every source member, or distinguish their minimal descendants. The fixed affine facet has bounded order for each of the two fields, so it cannot cover source facets of arbitrarily large order in Γ3/Γ4. Thus Proposition 6.5 is not an automatic all-parameter substitution for the phase109 construction. This statement does not rule out a different construction or a different deduction from the literature. The new derivation's remaining obligations are concrete construction and transport obligations inside an established mix/cover framework.

I also reread the relevant earlier phase82 comparison and the exact Γ1 source/result interfaces. The older finite example, prime-degree minimality argument, mix/fiber-product method, quotient criterion and source chirality orders remain credited to their sources. The retained classifications, tightness, orders and IP are substantial assumptions; neither phase113 nor phase109 compresses those away by asserting them without cost.

The author records sixteen dated queries and corresponding private response captures. I checked the query inventory and bound capture/source records, but did **not** repeat that entire search or claim that a negative query result proves absence. Independently reopening the two arXiv abstract records showed only the cited v1 submissions, September 9, 2020 and June 24, 2025. The author publication page also still lists the 2024 cover paper. These are limited observations of the accessed records, not an exhaustive bibliography or an openness certificate. [Classification record](https://arxiv.org/abs/2009.04566), [mix submission record](https://arxiv.org/abs/2506.19334), [author list](https://gabrielcunningham.com/math).

The discrepant date in the mix paper's HTML rendering is not treated as a new submitted version. This review freshly checked the abstract submission history; phase113's more specific HTML-date observation remains its dated author record. It does not change the proof comparison, which uses the exact bound PDF.

The report's unread-material list is material and correctly limits its conclusion. In particular the relevant full 2025 book chapters and Appendix C, the complete 2014 mixing/monodromy paper, full publisher-edition collation and complete comparison with other abelian-cover methods remain uncompleted in this audit. I did not acquire or read those texts here, and did not repeat failed access attempts. The report does not claim to exclude an encompassing result in them. Its references to unread papers do not serve as evidence that their methods fail to subsume this work.

## Admission boundary

The safe affirmative statement is now: **the independently reviewed family proofs establish the multiplicity assertion for all five rows in the checked author-source proposal, using the retained classifications and standard cover theory. Historical priority and current openness remain unverified.** The qualifier about exact source edition remains necessary until publisher collation is completed.

No [O] marker is cleared. This audit adds no source to a compression assembly, no compression ratio, no whole-family Lean component and no claim of first discovery. Phase113's old pending-review language remains frozen; this additive review supplies the explicit phase112 update. All original files are unchanged, and no public file was edited. Root admission and publication are separate.
