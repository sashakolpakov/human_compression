# Cover literature: completed bounded comparison, with access gaps preserved

10 October 2026. This is an attribution and source-status note, not a mathematical admission, a complete literature census, or a historical-priority certificate. It preserves phase72/82 and the frozen phase90/92 theorem packages. No public files were changed. Primary full texts are excluded from export.

The two requested access gaps remain material. A fresh ordinary check did not obtain the complete Monson–Pellicer–Williams 2014 paper or Pellicer’s 2025 chapters 4/5 and Appendix C. The new comparison nevertheless identifies an older universal-amalgamation attribution that the presentation of phase90/92 should make explicit. The exact repository calculations can be described and checked without calling the underlying amalgamation or mix principles new.

## What was actually accessible

| Target | Fresh access and reading | Result |
|---|---|---|
| Monson–Pellicer–Williams, *Mixing and monodromy of abstract polytopes*, Trans. AMS 366 (2014), 2651–2681 | Publisher metadata/abstract and Williams’s author publication entry; direct AMS article and PDF requests returned 403. The author link points to AMS. | Complete statements and proofs remain unread. Citations to individual results in other primary papers are explicitly indirect evidence. |
| Pellicer, *Abstract Chiral Polytopes*, chapter 4, pp. 208–262 | Publisher chapter metadata and summary. | No chapter proof text obtained. |
| Same book, chapter 5, pp. 263–341 | Publisher chapter metadata and summary. | No chapter proof text obtained. |
| Same book, Appendix C, pp. 459–465 | Publisher metadata and access page. | None of its problem statements obtained. |
| Same book, detailed contents | Search extraction of the publisher frontmatter, not a complete local PDF or a visual PDF reading. | It identifies §4.3, *Quotients and Covers*, beginning p. 236; §4.4, *Mixing*, p. 244; §5.2, *Tight Chiral Polytopes*, p. 274; §5.4, *Chiral Amalgamations*, p. 309. These are the precise outstanding comparisons. |

The book remains listed with online publication 23 March 2025 and print publication 3 April 2025. Its chapter pages expose an access requirement; this audit neither purchased access nor used credentials or a bypass. The AMS electronic publication date remains 4 November 2013. Dates do not establish that any question is currently open. [AMS record](https://doi.org/10.1090/S0002-9947-2013-05954-5), [author publication list](https://williams.alaska.edu/publications), [chapter 4](https://doi.org/10.1017/9781108695046.005), [chapter 5](https://doi.org/10.1017/9781108695046.006), [Appendix C](https://doi.org/10.1017/9781108695046.010).

Fresh arXiv metadata still displays only v1 for Cunningham–Hubard 2506.19334 and Cunningham–Pellicer 2009.04566. The earlier phase72 full reading of the 21-page mix paper remains inherited evidence; it was not repeated here. The source version is not silently upgraded to an unacquired journal version. [Mix version record](https://arxiv.org/abs/2506.19334), [tight-family version record](https://arxiv.org/abs/2009.04566).

## Universal amalgamation was already part of the theory

A fresh selected reading of Cunningham–Pellicer’s 2016 author version, §4.1 on PDF pp. 17–19 and its reference [69], confirms that a universal regular amalgamation with prescribed facets and vertex-figures is an established construction whenever such a regular amalgamation exists. That source attributes the result to Schulte, *Amalgamation of regular incidence-polytopes* (1988). The original 1988 publisher abstract and metadata were checked, but its full proof was not acquired. This is a precise attribution through a primary survey, not a claim to have independently collated the original proof or theorem numbering. [2016 author source](https://arxiv.org/pdf/1608.07993v1), [1988 original record](https://doi.org/10.1112/plms/s3-56.2.303).

There is also directly read, related primary construction material: Monson–Schulte, arXiv:1109.1337v2, §5, pp. 18–22, including Lemmas 5.1–5.4, Theorem 5.5 and the following discussion. It uses amalgamated groups and normal forms to assemble alternating regular facets, then discusses adjoining a closing relation and checking intersection and embedding conditions. Its local configuration is different from the two opposite ends used here; Theorem 5.5 is not a direct theorem giving our rank-four completion kernel. The fresh reading is selected proof reading, not the full 28-page paper. The arXiv record lists v2 on 26 January 2012, whereas the served PDF prints 22 July 2021 on its title page; the latter is not treated as a new submitted version. [Checked author version](https://arxiv.org/pdf/1109.1337v2), [submission record](https://arxiv.org/abs/1109.1337).

For the exact relationship, write A=G012, B=G123 and C=G12. The marked group

```text
W=(A *_C B)/<<[r0,r3]>>
```

contains every local defining relation and the remaining outer string commutation. Any marked cover of G whose two end projections are injective receives the canonical epimorphism from W. When one such polytopal cover exists, the standard quotient/recognition argument makes W polytopal. In geometric language it realizes the universal regular amalgamation of these exact local types. This elementary universal property is part of the established framework and should be attributed accordingly.

What phase90 explicitly proves in addition is the relationship with its separately defined complement presentation U: a bipartite coset graph with translated commuting-square cells identifies the nonfree factor of U with ker(W→G), fixes the marked defects, and gives a finite-group-class separation criterion. Its proof uses classical Bass–Serre theory, maximal-tree presentations, van Kampen and string C-group recognition. Calling that an explicit repository derivation is justified; calling it historically new is not justified by this audit.

## Exact comparison of the repository results

| Repository statement | Existing method or input that must retain attribution | Additional calculation or argument in the frozen repository |
|---|---|---|
| Phase49 odd-prime Γ1 covers Q and Q′ | Source family construction and chirality results; old facet-cover mix criterion; Cunningham’s finite example and two-extension strategy | All valid Γ1 parameters, exact normal closure and degree, distinct characters and the complete stated interval under their common cover. Phase72/82 already separates these costs. |
| Phase90 Theorem 1 | Amalgamated products, their tree, fundamental groups of cell complexes | Exact U≅F_t*ker(W→G), explicit square/path conventions and defect e_i=i_B⁻¹i_A. |
| Phase90 Theorem 2 | Finite products, normal cores and recursive intersection recognition | Equivalence between locally faithful finite covers with kernel in a subgroup/product-closed finite class and separation of all defects in finite quotients; no coprimality restriction. |
| Phase90 Corollary 3 | Universal regular amalgamation and quotient machinery | Exact admissible-normal-subgroup description over the specified G, using ker(W→G)∩BA. |
| Phase92 Theorem 1 and action | Γ2 source presentation; earlier uniform reduction to the fixed coset action; free-product normal forms | Explicit reversible U≅F15*(C2×C2), defect X, and complete marked action. |
| Phase92 Theorems 2–3 | Standard affine/semidirect construction, local recognition, the preceding universal framework | Exact V4 completion kernel and action, actual W≅H identification, and the resulting two-object classification in the class with injective ends. |

The last classification has one minimal member, of degree two, and one larger member, of degree four. It does **not** prove two minimal covers. It classifies every regular polytopal marked cover of G with both end projections injective, even if the cover was not assumed finite. It does not classify end-enlarging covers. The source parameter range is every Γ2 sign pair and q=2^β, β≥5, conditional on the frozen source and transport inputs.

The general mix criteria checked in phase72/82 prove polytopality of suitable mixes. They do not, simply by applying those criteria, compute the kernel of this exact universal completion or rule out additional locally faithful quotients. Conversely, without reading the two missing works, this audit cannot exclude a previously published theorem or calculation that subsumes those results. The ledger therefore uses “not supplied by the checked criterion” rather than “absent from the literature.”

## Relation to the stated questions

Cunningham’s checked eight-page author manuscript, §4, gives two distinct minimal covers for one odd-prime example and proposes analogous multiplicity for the five tight families. Phase49 settles the specified Γ1 family part of that older proposal with the declared retained inputs. Phase92 does not settle the Γ2 multiplicity part: it shows that any second minimal regular cover must enlarge at least one local end. The degree-four locally faithful cover is not a second minimal cover because it covers the degree-two one. This is a useful constraint on further proof search, not an unrestricted uniqueness result. [Checked author manuscript](https://gabrielcunningham.com/WhichChiralPolytopes.pdf).

Likewise, the 2016 author source’s Problems 5 and 6 concern unrestricted minimal regular polytopal covers. The local restriction in phase92 prevents treating its unique local minimum as a resolution of Problem 5. The current status of those broader questions is not certified here, particularly while the 2025 book’s relevant chapters and problem appendix remain unread. This audit does not add an open-conjecture-solved or novelty marker.

## Next proof branch

The most directly relevant remaining source target is a second minimal cover for the Γ2 family in Cunningham’s proposal. The new universal result says exactly where to search: allow one local end to enlarge while preserving a map onto the specified source end. A concrete branch is to choose an explicit finite regular cover A′→A of the facet group, compatible with the medial marking, form the completion from A′ and B, and prove a polytopal quotient over G with a minimal descendant distinct from the known double cover. The necessary obligations are a complete local presentation, exact medial compatibility, intersection recognition, and a kernel/quotient argument proving that the descendant does not factor onto the known double cover. No such A′ or descendant has been established by this note.

In parallel, the existing phase90 Γ3/Γ4 source interfaces permit a separate parameter proof of their defect laws or completion kernels. A successful proof must handle their growing coset complexes; the finite probes are not a uniform certificate. Neither branch depends on repeatedly retrying inaccessible book pages. Obtaining a legitimate complete copy of the missing literature would improve priority/status comparison, but the mathematical proof work can proceed under explicit attribution and scope.

## Frozen evidence and export boundary

The accompanying sources JSON records successful metadata/excerpt access, failed retrievals and exact newly read local ranges. Its SHA-bound local inputs include phase49/72/82/90/92/96 and the actually used primary extractions. The comparison ledger separates mathematical scope from historical status. The manifest exports only this report, the two JSON ledgers and itself. No source PDF, source transcription, browser full text, credentials or private access material is exported. No mathematical program or Lean theorem was rerun for this literature note.
