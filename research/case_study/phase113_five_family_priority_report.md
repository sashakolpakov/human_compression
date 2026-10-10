# Five-family coverage and bounded priority audit

10 October 2026. This is an additive source and scope audit. It preserves the admitted odd-prime theorem and the frozen phase109 candidate. It is not a second mathematical verification of either construction. Phase109's independent phase112 review and root admission remain separate gates. **No [O] approval or historical-priority certification is supplied.**

## The exact older proposal

The checked primary is Gabe Cunningham's July 25, 2023 author PDF, *Chiral polytopes whose smallest regular cover is a polytope*, subsequently published in JCTA 204 (May 2024), 105839. Example 3.5 identifies the five chiral-facet/chiral-vertex families in reference [7, Table 4] as having nonpolytopal smallest regular covers. At the end of §4, after the finite {6,9,6} example, the author writes:

> We conjecture that the situation is similar with all of the chiral polytopes mentioned in Example 3.5.

The definite multiplicity assertion supported by that context is: **each polytope in those five families has at least two distinct minimal regular polytopal covers.** The displayed example uses two covers of degree three. The final sentence does not state a common degree for all five families, so the synthesis here asserts multiplicity rather than two degree-three covers or a prescribed construction for every family. [Author primary](https://gabrielcunningham.com/WhichChiralPolytopes.pdf), [publisher metadata and preview](https://www.sciencedirect.com/science/article/abs/pii/S0097316523001073).

This is narrower than the preceding broad suggestion about every polytope with a nonpolytopal smallest regular cover. It is also narrower than Cunningham–Pellicer's *Open problems on k-orbit polytopes*, Problem 5, which asks whether any polytope can have nonpolytopal monodromy and nevertheless a unique minimal regular polytopal cover. Neither of those general assertions is decided by the five-family construction. The source of Problem 5 was checked in its 2016 author version, printed page 8; no inference of current openness is drawn from that historical wording. [Primary version](https://arxiv.org/pdf/1608.07993v1).

## Editions and the five exact rows

Reference [7] in the 2023 cover manuscript is Cunningham–Pellicer, *Tight chiral polytopes*, J. Algebraic Combin. 54 (2021), 837–878. The complete classification edition available for this audit is arXiv:2009.04566v1, submitted September 9, 2020, with PDF date September 11. Its Table 2 is on printed page 23 and Table 4 on printed page 40. Both original page images have been visually checked; the rotated Table 4 extraction alone is insufficient for its formulas. The checked source has Theorems 4.7–4.10 and Proposition 4.2. The later cover paper cites a Proposition 11 in the journal edition; these numbers are not silently identified. The publisher article record confirms publication on February 22, 2021, but its full text and Table 4 were not acquired. A normal public table-page request was inaccessible in the browser. Thus the exact word/parameter collation below is against the checked author edition, while the bibliographic link to the 2023 proposal is explicit. [Author record](https://arxiv.org/abs/2009.04566), [publisher record](https://link.springer.com/article/10.1007/s10801-021-01023-z).

Table 4 has eight rows. Its first three have regular facets; its last five have chiral facets. The text preceding Theorem 5.14 says that the last two rows are a dual pair, and that adjoining the duals of the first three yields eleven atomic families in total. Consequently “five families” means exactly the five chiral-facet rows, not all eleven atomic families and not all tight chiral 4-polytopes.

In the following table m is an odd prime, α≥2, q=2^β with β≥5, and each ε_i is independently ±1.

| Table 4 row | Exact type | Parameters | Table 2/source theorem | Repository result |
|---|---|---|---|---|
| 4, first chiral-facet row | {2m,m^α,2m} | 1≤k≤m−1 | Γ1, Theorem 4.7, k1=k2=k | Admitted phase49/59/67: two distinct minimal covers, each degree m over the smallest regular maniplex |
| 5 | {8,2^β,8} | every β≥5; all four sign pairs | Γ2, Theorem 4.8 | Candidate109: regular covers of degrees 3^34 and 5^34 and distinct minimal descendants |
| 6 | {2^(β−1),2^β,2^(β−1)} | every β≥5; all four sign pairs | Γ3, Theorem 4.9 | Candidate109, same two coprime covering degrees |
| 7 | {8,2^β,2^(β−1)} | every β≥5; all four sign pairs | Γ4, Theorem 4.10 | Candidate109, same two coprime covering degrees |
| 8 | {2^(β−1),2^β,8} | every β≥5; all four sign pairs | dual Γ4 | Candidate109 by marked duality; signs exchanged |

There is no missing α=2, m=3 or β=5 boundary case in the stated contracts. There is no m=2, k=0 or β<5 parameter in these rows. Table 2 initially permits k1,k2 independently, but Theorem 4.7 proves k1=k2 necessary for the claimed tight chiral polytope; the one-parameter range is therefore the entire valid Γ1 family. This is a source restriction, not a repository omission. All odd-prime construction/classification hypotheses remain retained inputs.

## Word-level identification of Tables 2 and 4

Agreement of Schläfli type alone would not identify a marked polytope. The following algebra gives the needed conversion of presentations.

Write a,b,c for σ1,σ2,σ3. Suppose b^q=1, (ab)^2=1, and e²≡0 modulo q. The Table 2 relation

```text
b a² = a² b^(1+e)
```

is equivalent to the Table 4 pair

```text
b^(-1)a = a³ b^(1+e),
b a^(-1) = a^(-3) b^(-1+e).                         (1)
```

Indeed b^(-1)=a b a gives the first equation. Since (1+e)^(-1)≡1−e modulo q, the first defining relation also gives b^(-1)a^(-2)=a^(-2)b^(-1+e). Using b=a^(-1)b^(-1)a^(-1) yields the second equation. Conversely, multiply the first equation of (1) by a^(-1) on the left and use a^(-1)b^(-1)=ba to recover b a²=a² b^(1+e). Thus the extra second rewrite introduces no new constraint.

Applying the same argument to u=c^(-1),v=b^(-1), and inverting the resulting equations, converts

```text
c² b = b^(1+e)c²
```

to exactly the Table 4 pair

```text
c^(-1)b = b^(-1+e)c^(-3),
c b^(-1) = b^(1+e)c³.                               (2)
```

For Γ1 use q=m^α and e=k m^(α−1); for Γ2 and the relevant Γ4 end use q=2^β and e=ε q/4. In both cases e² is divisible by q throughout the stated range. The Γ3 two left and two right equations are already printed in the Table 4 form. Equations (1)–(2), the unchanged power and rotation-square relations, and Theorem 4.7's k1=k2 condition therefore identify every covered row as a marked presentation, not just an abstract group of the right order.

Duality reverses and inverts the rotation marks:

```text
(a,b,c) ↦ (c^(-1),b^(-1),a^(-1)).                   (3)
```

The right Γ3 equations become the two left Γ3 equations by inversion, in reversed order. The right Γ2 equation becomes the left Γ2 equation under (3), and vice versa, as also seen in (2). Therefore the two end parameters are exchanged without a sign change. For the Table 4 dual Γ4 row with labels (ε1,ε2), take the proved Γ4 row with labels (ε2,ε1) and dualize. As this map permutes the four sign pairs, none is omitted.

There are five **ordered-type rows**, but only four families up to rank reversal: Γ4 and dual Γ4 are one dual pair. Γ1 is self-dual in its one parameter, while Γ2 and Γ3 are closed under duality after exchanging ε1,ε2. This does not assert that all sign choices are mutually nonisomorphic; no isomorphism-count classification is needed. For β≥5, 2^(β−1)≥16 differs from 8, so the two mixed rows have different ordered types. Rank-preserving polytope isomorphisms do not identify them by merely reversing ranks. Within Γ1 the two minimal covers are dual to one another, but phase49 proves them distinct as rank-preserving polytopes, which is the convention required by the proposal.

## Precise synthesis and its proof boundary

Conditional on acceptance of the frozen phase109 theorem, the admitted Γ1 theorem plus phase109 cover every parameter and sign in the five rows of the checked author Table 4. The definite finite-family multiplicity assertion above follows. No new finite search is needed for this synthesis: the row identification is the written conversion (1)–(3), Γ1 has its already reviewed all-parameter proof, and phase109 supplies its own uniform source transport rather than parameter interpolation.

For Γ1, both distinct covers themselves have prime degree m and are proved globally minimal. For each 2-primary row, phase109 instead constructs two large finite covers H3,H5. Finite descent gives minimal quotients Q3,Q5 of respective degrees 3^d and 5^e, with 1≤d,e≤34, over the common smallest regular maniplex. Those positive coprime prime-power degrees prove distinctness. Neither the actual minimal exponents nor chosen quotient kernels are exhibited, and the large H3,H5 are not asserted minimal. The distinction is material and must remain in any public summary.

The separate family proofs also give finite admissible-kernel join-density. That is a stronger recorded conclusion for these particular families, not a theorem about all polytopes. Theorem 5.14's assertion that every tight chiral 4-polytope covers an atomic one does not supply upward inheritance of minimal-cover multiplicity or join-density. In particular no conclusion for every non-atomic tight chiral polytope follows merely by citing that classification.

The retained source constructions, exact orders, tightness, IP, chirality and geometric recognition are substantial. The synthesis does not reprove the atomic classification, add an admitted source to a compression assembly, or formalize either family construction in Lean.

## Bounded comparison with later primary literature

A fresh search on October 10, 2026 used sixteen recorded queries combining the exact proposal/title, tight families, minimal regular covers, chiral polytopes and 2025/2026. The primary arXiv records and Cunningham's author publication list were reopened. Search-engine dates and crawl labels were not interpreted as publication dates. Secondary hits were discovery aids only; no theorem-level conclusion is based on them.

The arXiv record for Cunningham–Hubard's *Polytopality criteria for the mix of polytopes and maniplexes* still displayed only v1, submitted June 24, 2025. Its HTML document date displayed August 24, 2026, while the bound PDF has June 25, 2025 on its title page; that HTML date is not evidence of a newly submitted version. The complete §6 of the bound primary PDF, including all theorems, proofs, examples and three concluding problems, was freshly read for this audit. The earlier phase72/82 whole-paper/selected-pass comparison remains separately bound. [Submission record](https://arxiv.org/abs/2506.19334), [primary version](https://arxiv.org/pdf/2506.19334v1).

Theorem 6.3 and Corollary 6.6 recognize when a specified mix is polytopal, through local polytopality and a variance-kernel intersection. Proposition 6.5 is the established facet-cover shortcut and already applies to the odd-prime construction, as phase72/82 explain. Corollary 6.17 includes the 2023 chiral smallest-cover criterion. The remaining §6 statements concern prescribed two-orbit classes, doubles, common local quotients and specified mixes; the concluding problems ask about admissible covers, preservation of a two-orbit class, and polytopality of a smallest regular cover. None of these displayed results supplies the five-family pair of distinct minimal covers or the fixed256 affine witnesses without additional construction and verification.

Phase109 can itself be regarded as a constructive specialization within this established mix/kernel framework: its new obligations are the uniform marked quotient preserving the defect, the two explicit finite affine groups, their local and full intersections, and generation of every source pullback. The bounded-order facet of Hbar cannot cover arbitrarily large Γ3/Γ4 source facets, so Proposition 6.5 is not an automatic all-parameter shortcut for that fixed construction. The general criterion remains credited to its authors; lack of the literal family calculation in §6 does not prove that no alternative deduction from the literature exists.

The live author publication list includes the 2024 smallest-cover paper and related cover/construction work, but is not an exhaustive or guaranteed current bibliography. The bounded search located no primary statement resolving this exact five-row multiplicity proposal. This is negative search evidence, not a proof of absence. [Author list](https://gabrielcunningham.com/math).

## Unread material and the priority gate

The following limits remain material:

* Daniel Pellicer's *Abstract Chiral Polytopes* was published online March 23, 2025. Publisher metadata/contents and references were refreshed, but the relevant full chapters 4–5 and Appendix C were not read. The references locate the 2024 smallest-cover paper on pages 240 and 243 and the tight classification on pages 284–285. A later solution or encompassing theorem in those sections has not been excluded. No repeated blocked chapter retrieval or alternate-access attempt was made. [Book record](https://www.cambridge.org/core/books/abstract-chiral-polytopes/BC35C376018672DE12A3B270315B759C), [references](https://www.cambridge.org/core/books/abs/abstract-chiral-polytopes/references/26F8682EA0F9E1FF79DF66FD37C23D90).
* Monson–Pellicer–Williams, *Mixing and monodromy of abstract polytopes* (2014), remains an unacquired complete text in this investigation; the earlier ordinary publisher retrieval failed. Its cited local results and metadata do not substitute for its complete comparison. No retrieval loop was repeated here. [Primary DOI](https://doi.org/10.1090/S0002-9947-2013-05954-5).
* Full publisher versions of the 2021 classification and 2024 cover paper have not been collated with the author versions. Their exact edition boundary and changed numbering remain explicit. The public 2021 Table 4 request failed through the browser; no access restriction was bypassed.
* Other covering-method papers, including Conder–Zhang's *Abelian covers of chiral polytopes* (2017) and Zhang's *Abelian covers of regular hypertopes* (2024), were identified through primary references or publisher summaries, but their complete methods were not compared here. They are not ruled out as prior-method antecedents. Their existence reinforces the need to avoid claiming novelty of the broad abelian-cover idea. No subsumption conclusion is drawn from an abstract alone.

Accordingly this audit certifies an exact **source-target/parameter synthesis**, at the frozen proof gate stated above, and a bounded literature comparison. It does not certify that the proposal was still open on October 10, 2026 or that the constructions are historically first. Even if phase112 accepts the mathematics, this audit does **not** clear an [O] marker. A safe description is: “The combined family proofs establish the multiplicity assertion for all five families in the checked author-source proposal, using retained classifications and standard cover theory; historical priority remains unverified.”

The machine-readable coverage map, source/read ledger and query record accompany this note. Private primary PDFs, extracts, page images and browser captures are excluded from export. No frozen theorem, annotation, public document, measurement or count was altered.
