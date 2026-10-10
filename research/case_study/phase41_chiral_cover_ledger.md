# Chiral-cover source/dependency ledger

Date: 10 October 2026. Status: author-completed conditional adapter; independent/root review not yet claimed. No public registry or frozen package was edited.

## Exact target contract

Target: Gabe Cunningham, *Chiral polytopes whose smallest regular cover is a polytope*. Complete checked text: author PDF headed 25 July 2023, eight PDF pages (printed pages 1–8), ending with reference [14]. Publication independently confirmed by publisher and author webpage: JCTA Series A 204 (May 2024), 105839, DOI 10.1016/j.jcta.2023.105839. Publisher PDF unacquired. All embeddings below use compatible marked base sections.

| Source item | Exact conclusion/scope | Adapter location and proof cost | Status |
|---|---|---|---|
| Proposition 2.2, cited older result | Chiral P with regular facets OR regular vertex-figures has polytopal smallest regular cover | Lemma 3.1; rank induction using K and retained standard correspondence; target not assumed | Proved |
| Proposition 2.3 | For chiral P with both ends chiral, cover polytopal iff end intersection lies in medial subgroup | §3 after Lemma3.1; depth-two section regularity and recursive C+ criterion | Proved |
| Proposition 2.4 | Chirality subgroup is first-coordinate kernel of mirror mix | §2 equation(1), normal-subgroup product calculation | Proved |
| Theorem 3.1 | Arbitrary chiral P, sections K,L,M: cover polytopal iff X(K)∩X(L)≤X(M) | Theorem3.2; one K application after the proved local prerequisites | Proved |
| Remark 3.2 | Regular end makes criterion automatic | §3 consequence1 | Proved |
| Corollary 3.3 | If M regular, X(K)∩X(L) meets medial group trivially iff cover polytopal | §3 consequence2; this intersection already lies in the medial group | Proved, precise embedded scope |
| Corollary 3.4 | Rank4 criterion via absence of a nonidentity power of σ2 | §3 consequence3 | Proved, identity wording corrected |
| Example 3.5 | All five specified Table4 families with chiral ends have nonpolytopal smallest covers | §4 five-row parameter table; older existence/atomicity/chirality theorem retained openly; one obstruction per family | Conditional on stated older classification input; no finite sampling |
| Proposition 3.6 | Totally chiral ends: cover polytopal iff medial section totally chiral | §3 consequence4 | Proved |
| Corollary 3.7 | Chiral K with X(K)∩Γ0(K)=1 forces polytopal smallest cover for every chiral extension with facet K | §3 consequence5 | Proved; no extension-existence assertion |
| Example 3.8 | Chiral square torus maps in standard parameter convention satisfy preceding condition | §4 affine proof; square tessellation/torus model retained | Proved relative to standard geometric identification |
| §4 uniqueness implication | Polytopal smallest regular cover is unique minimal regular polytope cover | §5 universal factorization | Proved, infinite case allowed |
| §4 finite P | Literal presentation gives a chiral polytope with648 flags | §5 equations(4)(5), stock GAP exact bare-presentation computation | Checked, GAP dependency charged |
| §4 finite R | Mirror mix is smallest regular cover,1944 flags, nonpolytopal | §2 universality + §5 end intersection27>9 | Checked + proved universal property |
| §4 T and dual | Literal groups are trivial facet extension and its dual | §5 equations(6)(7), facet isomorphism, index2 facet subgroup, explicit dual map | Checked relative to standard two-facet interpretation |
| §4 Q,Q' | Both regular polytopes with5832 flags, distinct3-fold covers ofR and minimal regular covers ofP | §5 exact maps, IP, mirror maps, word(8), prime-index argument | Checked finite facts + full abstract minimality proof |
| §4 general likelihood | Every polytope with nonpolytopal smallest regular cover has multiple minimal polytopal covers | Not a theorem in source; K does not establish it | Unproved; not counted |
| §4 five-family conjecture | Analogous multiple minimal cover phenomenon for every Example3.5 polytope | Only the source's single finite instance is checked here | Unproved; not counted |

The claim is coverage of the author's proved source conclusions with specified retained inputs. It is not an unconditional replacement of older classifications or the full version of record, and no new formal-component count is warranted.

## Dependency inventory

| ID | Retained result/tool | Why needed | Boundary |
|---|---|---|---|
| G1 | Standard string C+ group↔oriented chiral/directly regular polytope correspondence, recursive intersection criterion, mirror regularity, marked covers | Converts the common group theorem and finite table into geometric conclusions | Substantial older geometric background; not proved here and not target imported |
| G2 | Facets-of-facets and vertex-figures-of-vertex-figures of chiral polytopes are directly regular (Schulte–Weiss Prop9 as cited by target) | Ensures local mirror covers in Theorem3.2 are polytopal | Does not assert target cover criterion |
| G3 | Standard square-tessellation quotient model of {4,4}(b,c) | Identifies the affine marked group in Example3.8 | Algebraic chirality obstruction is proved here; no new map classification |
| C1 | Cunningham–Pellicer2021 Table4 five chiral/chiral families, their atomicity and existence; published Prop11 / arXiv2020 Prop4.2 giving cyclic prime-order global chirality in the middle generator | All-parameter Example3.5 | This entire older input is retained; its completeness proof is not charged as newly proved or compressed |
| A1 | Exact GAP4.15.1 algorithms for finitely presented groups, permutation isomorphisms, subgroup intersections and marked homomorphisms | All finite orders, IP tests, maps and distinguishing word in source§4 | Computational proof with GAP trusted; no RAMP, SmallGroups, sampling, or Lean certificate |
| K | `formal/LiftCertificate.lean`, theorem `LeemansLift.intersection_of_image_and_kernel` | Existing certified common group theorem | Manuscript gives full elementary proof, so no proof-by-phase-link; geometry not formalized here |

All other mathematics used by the target adapter is proved in the manuscript. The target's own propositions are not listed as retained background. F005 is used only for the literature relation; none of its theorems is needed to prove Theorem3.2.

## Source acquisition and reading limits

- Main author PDF, https://gabrielcunningham.com/WhichChiralPolytopes.pdf: all eight pages read through the web tool's complete text extraction. The bound file `phase41_chiral_cover_source_web.txt` contains that extraction, including line/page markers. A normal shell download failed DNS; PDF screenshots also failed. Therefore there is no claimed local PDF-byte binding or visual page verification.
- Publisher, https://www.sciencedirect.com/science/article/abs/pii/S0097316523001073: primary indexed content checked for publication metadata, Theorem3.1 and acknowledgement of an earlier Cor3.3 error. A subsequent direct fetch returned403. No access escalation attempted. Author publication list https://gabrielcunningham.com/math independently agrees on2024 publication.
- Older classification, https://arxiv.org/pdf/2009.04566: selectively read Proposition4.2 and its proof, the neighboring arguments identifying embedded chirality groups, and Table4 with all five parameter rows. This was not a full43-page reread or verification of that classification. Selected primary web excerpts are bound separately in `phase41_chiral_cover_tight_excerpts_web.txt`. Screenshots failed; formula extraction is limited, so no new claims about the full table's literal presentations are made.
- F005, primary https://arxiv.org/abs/2506.19334 and existing cached `sources/mix_criteria2025.pdf/.txt`: inspected current primary metadata and read the relevant full Sections6.1,6.5,6.6, conclusions, and references. The printed text expressly makes the chiral result a Corollary6.17 specialization. Current arXiv record has v1 only and no journal reference.
- Hubard–Schulte2026, https://arxiv.org/html/2604.00185v1: inspected abstract and searched the primary full HTML for “minimal regular” and “cover”; neither matched. This was a bounded relevance check, not an independent review of that paper.
- Current web search phrases included “chiral minimal regular covers2025 2026” and “unique minimal regular cover chiral2025 2026”. No resolution of the source's two conjectures was located. This supports only the manuscript's bounded-search statement, not a theorem that no resolution exists.

## Corrections and exclusions

1. Restore mirror overbars lost by text extraction and keep embedded local groups explicit.
2. Read “no power” as “no nonidentity power”; otherwise identity gives an immediate contradiction.
3. Use the mathematically consistent cyclic rank-two base case, not the rank-one base line printed in the extraction.
4. A mix object is not assumed polytopal before IP is proved.
5. The degenerate one-cell square quotient is used only as a regular marked group, not asserted to be an abstract polytope.
6. The tight-family parameter table refers to the specific classified groups, not every polytope of the same type.
7. The publisher's Cor3.3 version history is acknowledged; unacquired version-of-record wording is not certified.
8. No quantitative source-length compression ratio, new criterion, complete classification, or conjecture resolution is claimed.
