# Bounded source-status audit: abelian covers, L003 and L111

Audit date: 10 October 2026. Private source-access and comparison record. No frozen mathematical artifact or public registry is changed. This pass does **not** establish priority or the absence of a published correction.

## 1. N015: exact theorem comparison is still blocked

Wei-Juan Zhang, *Abelian covers of regular hypertopes*, Journal of Algebra **650** (2024), 123–144, DOI [10.1016/j.jalgebra.2024.03.017](https://doi.org/10.1016/j.jalgebra.2024.03.017). The [publisher page](https://www.sciencedirect.com/science/article/pii/S0021869324001534) gives the issue date 15 July 2024. Publisher-deposited Crossref metadata independently confirms the title, author, volume and pages; its publication date has month precision only. An exact first-online day was not verified.

The publisher abstract, introduction and section previews were read again. They establish prior work on abelian group covers producing regular hypertopes, with rank-five through rank-seven examples. The introduction expressly permits diagrams beyond its Y-shaped illustrations. Section 5 cites Theorems 4.1 and 4.4 as the construction inputs; the preview does not expose their complete statements or proofs. Thus the rank of the displayed applications does **not** bound the general method's scope.

The full body was not obtained. The [ResearchGate record](https://www.researchgate.net/publication/379578350_Abelian_covers_of_regular_hypertopes) explicitly offers a full-text request rather than a manuscript. No request was sent. The publisher PDF route failed. The two text-mining URLs deposited at Crossref returned rate-limit or invalid-view responses; an explicit full-view request returned an authentication error. No API key or institutional access was available or sought. Exact-title, DOI, theorem-number, author and institution searches did not reveal a primary manuscript. The author's public ORCID record, identified through the publisher metadata, has no researcher URLs. OpenAlex reports only a closed publisher location; that is a discovery aid, not proof that no manuscript exists elsewhere.

Consequently, **a full reading and exact main-theorem match have not been completed**. This access limitation must remain visible in any priority statement.

## 2. What must be compared to the new even-parameter construction

The current private [even-parameter note](phase33_L003_even_family.md) constructs rank-four examples for every even source parameter (s=2m\ge2). Its Coxeter diagram is fixed; the changing quantity is a toroidal residue parameter, with that residue's group order (48m^2=12s^2). Three maximal parabolics inject into the parameter-two base. A unimodular translation minor identifies the growing fourth residue. The full group maps to the base with an abelian kernel of translation functions.

These features make N015 directly relevant. They do not identify the two constructions. In particular, a permutation-voltage action over a fixed set of states is not, by terminology alone, the same object as a regular graph cover with geometric elements given by connected shadow components.

An exact match needs the following source information:

| Required part of N015 | Comparison obligation |
|---|---|
| Covering definition and ambient group construction in §4 | Determine whether it includes integral permutation-voltage lifts with a fixed Coxeter diagram. |
| Complete Theorems 4.1 and 4.4 | Match every rank, kernel, relator and local-injectivity hypothesis. |
| Intersection-property argument | Check whether injectivity on all but one maximal marked parabolic is sufficient there, or whether additional conditions occur. |
| Flag-transitivity argument | Compare actual typed coset completion, separately from subgroup intersection. |
| Parameter/order conclusion | Distinguish a growing toroidal relation parameter from a changing edge label, and compare exact local groups rather than numerical group orders alone. |

Until these obligations are met, the comparison is **undetermined**. The basic use of abelian covers to construct hypertopes is established prior art; no broad novelty claim is justified. Conversely, the inaccessible theorems cannot be cited as already proving this specific parameter family.

## 3. L003 Problem 9.2 and the accessible follow-up

The cached [2018 author manuscript](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf) was reread at the end of §8, Table 8 and Problem 9.2. The displayed question concerns an infinite family with ordered parameters (((3,0),(2,0),(1,1),(s,0))), for integer (s\ge2). Its surrounding discussion mentions finite examples, while the table is about finite universal objects. These scopes are distinct.

The later [Fernandes–Leemans–Piedade–Weiss manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/301629/3/FLPWrev.pdf) was reread at Theorem 4.3 and §5. Its theorem realizes a different ordered toroidal family; §5 corrects residue identifications in the earlier table's second and third rows. These passages do not supply the proposed varying-(s) family. They also reinforce the need to prove the exact marked residue types, rather than assume the defining parameters cannot collapse.

Exact-title/problem-number/parameter searches found no primary passage explicitly settling Problem 9.2. This is only a bounded negative result. In particular, the unread N015 theorems remain a material comparison gap. The new even-parameter statement should retain its precise scope: infinitely many finite examples with varying exact even parameter, with odd parameters, universal-group identification and current priority outside that theorem.

## 4. L111: correction search and version boundary

The [indexed author-uploaded L111 text](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes) was checked again at Theorem 6.1, Theorem 6.2 and Corollary 6.1. The same disputed assertions remain in those indexed passages. Their statements and the hypotheses used by the two counterexamples are documented in the frozen [section 6 ledger](phase32_L111_section6_ledger.json).

Bounded searches combined the title, DOI, authors, theorem/corollary number, and correction/erratum terms. The current [author publication list](https://leemans.dimitri.web.ulb.be/papersbyyear.html) was also inspected. No explicit correction to these two assertions was located. Publisher-deposited Crossref metadata has no linked update in its returned `relation` or `update-to` fields. Neither observation proves that no correction, alternative formulation or prior counterexample exists.

The final journal PDF has still not been compared byte-for-byte or visually with the indexed author text. The indexed first-page typography includes an apparent template year, so its metadata alone cannot certify final-version identity. The journal citation is independently supported by the author's publication list and DOI metadata. The proper present claim is therefore a counterexample to the **accessed indexed primary statements**, with final-version and correction-priority status unverified.

The mathematical boundaries remain separate. The disconnected example defeats the unrestricted symmetry converse by the full-group orders 128 and 512; it does not challenge the corrected connected-color-kernel sequence. The thin regular odd square tori meet the explicitly permitted weak geometric (I_{01}) condition and refute local-to-global bipartiteness. They leave Theorem 6.2's explicit global-bipartition assumption intact. No assertion about all connected extensions splitting is added here.

## 5. Recorded limits

The companion JSON binds the local source files, publisher metadata, query families and working comparison target. No third-party article body is exported, no author was contacted, and no new theorem or whole-paper coverage is credited by this audit. The absence of a search hit is not a proof of openness or novelty.
