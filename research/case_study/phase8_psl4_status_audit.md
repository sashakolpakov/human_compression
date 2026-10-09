# PSL(4,q) maximum string C-group rank: bounded status and priority audit

**Audit date:** 10 October 2026 (Europe/Zurich). **Target:** L120, §5.7, Conjecture 2. **Author of this audit:** survey_audit agent. This is a source/status audit, not an additional review of the workspace proof.

## 1. Finding and permissible wording

No later explicit resolution of the assertion “the maximum string C-group rank of PSL(4,q) is four for every odd prime power q” was located in the bounded search recorded below. The last explicitly checked source stating this exact assertion as a conjecture is Dimitri Leemans's survey, arXiv:1910.08843v2, §5.7, Conjecture 2. Subsequent primary papers checked here establish other results: existence of some string C-group representation, ranks for PSp(4,q), constructions for orthogonal groups, or small generating sets of involutions. None of their checked statements resolves this conjecture.

This supports describing the workspace result as **a proposed proof of the named survey conjecture**. It does **not** establish that the problem remained open immediately before this work, that the proposed proof is the first, or that every relevant publication or unpublished result has been found. No author was contacted. The audit does not certify the mathematics of `phase8_psl4_rank6.md`; that file has its own proof and internal-review records.

The survey's adjacent **Problem 7** concerns the broader range PSL(4,q) ≤ G ≤ Aut(PSL(4,q)). A theorem just for PSL(4,q) does not settle that problem. Rank-four existence from the 2016 paper remains a published input to the maximum-rank conclusion.

## 2. Exact target and original source

### L120: the survey

- Dimitri Leemans, *String C-group representations of almost simple groups: a survey*, [arXiv v2](https://arxiv.org/html/1910.08843v2), dated 11 May 2020; published in Contemporary Mathematics 764 (2021), 157–178, [DOI 10.1090/conm/764/15335](https://doi.org/10.1090/conm/764/15335).
- Reading depth: §5.7, Theorem 5.8, Conjecture 2 and Problem 7, with the surrounding definitions and attribution.
- Theorem 5.8 records rank-four existence for odd q and nonexistence of string C-group representations for even q. Conjecture 2 asks for the odd-q upper bound of four. These are distinct assertions.

### L048: the 2016 construction paper

- Peter A. Brooksbank and Dimitri Leemans, *Polytopes of large rank for PSL(4,F_q)*, Journal of Algebra 452 (2016), 390–400, [DOI 10.1016/j.jalgebra.2015.11.051](https://doi.org/10.1016/j.jalgebra.2015.11.051).
- Primary records: [publisher](https://www.sciencedirect.com/science/article/pii/S0021869316000259), [Bucknell institutional record](https://digitalcommons.bucknell.edu/fac_journ/1204/), and [author-uploaded ResearchGate text](https://www.researchgate.net/publication/293026803_Polytopes_of_large_rank_for_PSL4Fq).
- Theorem 1.1 asserts odd-q rank-four existence. The indexed author manuscript has Theorem 5.1 for the construction at q ≥ 5 and Remark 5.2 concerning q = 3. Its §4 explains the six-dimensional orthogonal realization and gives the even-characteristic obstruction; Theorem 4.4 and Corollary 4.5 are not an odd-q upper bound.
- Access depth must be stated carefully. The web tool exposed extensive indexed author-manuscript text: §§1–5, page labels 1–9, Theorems 1.1, 4.4, 5.1 and 5.3, Corollaries 4.5 and 5.4, Proposition 5.5, Lemma 5.6, the concluding proof of Theorem 5.1, Remark 5.7, acknowledgments and references 1–23. The displayed manuscript is dated 26 November 2015; the upload is attributed to Brooksbank on 4 March 2020. This is substantially more than an abstract excerpt, but mathematical extraction is garbled in places, and the underlying PDF was not obtained or validated. A direct ResearchGate retrieval produced an error page. Earlier Bucknell PDF retrieval returned 403. Therefore this audit records **indexed manuscript sections, statements and proofs inspected**, not a validated full-text PDF or a complete proof audit. It does not change L048's historical access classification.

The isomorphism relevant to alternative searches is PSL(4,q) ≅ PΩ⁺(6,q). One must distinguish Ω⁺ from its projective quotient, especially when the former has nontrivial center, and distinguish them both from the full orthogonal group.

## 3. Subsequent primary literature checked

| Source | Reading depth and result relevant to this audit |
|---|---|
| Brooksbank, *On the ranks of string C-group representations for symplectic and orthogonal groups*, [arXiv:1912.05512](https://arxiv.org/html/1912.05512v1), Contemporary Mathematics 764 (2021), 31–41, [DOI](https://doi.org/10.1090/conm/764/15329) | Full cached manuscript available; introduction, Figure 2, Theorem 1.1, Lemma 4.1 and §5.2 inspected for this task. Figure 2 gives only rk(PSL(4,q)) ⊇ {3,4} for odd q. The exact {3,4,5} theorem concerns **PSp(4,q)**, with q = 3 excluded. The discussion of higher even-dimensional Ω groups does not assert an exact maximum. Thus neither this exact-rank theorem nor its dimension-five argument supplies the missing PSL(4,q) bound. |
| Leemans–Adrien Vandenschrick, *On simple groups that admit a string C-group representation*, Art of Discrete and Applied Mathematics 9 (2026), P1.07, [institutional record](https://repozitorij.upr.si/IzpisGradiva.php?id=22370&lang=eng), [DOI](https://doi.org/10.26493/2590-9770.1329.6f5), [author manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf) | All six cached manuscript pages read. Theorem 1.1 classifies nonabelian simple groups admitting **at least one** representation. §3 concerns PSL(4,2ⁿ) and PSU(4,2ⁿ), using the characteristic-two obstruction. No odd-q maximum-rank result is asserted. The publication record places first online publication in November 2025 and the issue in 2026; the cached manuscript retains placeholder publication fields. |
| *Unravelled abstract regular polytopes*, [arXiv:2105.01921v1](https://arxiv.org/html/2105.01921v1), published 2024, [DOI](https://doi.org/10.2140/iig.2024.21.139) | Introduction and relevant indexed passages searched/read. The inspected construction and cover results do not state the PSL(4,q) maximum. This is not a complete proof review of the paper. |
| Efimov–Nuzhin, *Generating sets of conjugate involutions of groups SL_n(q) for n = 4, 5, 7, 8 and odd q* (2021), [DOI](https://doi.org/10.21538/0134-4889-2021-27-1-62-69), [journal English abstract](https://www.trimm.uran.ru/sites/default/files/ALL_VOLUMES/Volume_27%2C_2021/Issue_1/Abstract/TrIMMUrORAN_2021_1_p62.pdf) | English abstract read; Russian proofs not read. The statement concerns five conjugate involutions with product one, including a small-field case. These conditions do not assert the string commutations or subgroup intersection property. This is a different invariant. |
| Nuzhin, *Tensor representations and generating sets of involutions of special linear groups* (2020), [DOI](https://doi.org/10.21538/0134-4889-2020-26-3-133-141), [journal English abstract](https://trimm.uran.ru/sites/default/files/ALL_VOLUMES/Volume_26%2C_2020/Issue_3/Abstract/TrIMMUrORAN_2020_3_p133.pdf) | English abstract and theorem summaries read. Results on representations and minimum involution generating sets with product one are not string C-group maximum-rank statements. Russian proofs not read. |
| Markovskaya, *On Generating Sets of Matrix Groups over Finite Fields* (2025), [primary full text](https://www.mathnet.ru/php/getFT.phtml?jrnid=jsfu&option_lang=eng&paperid=1290&what=fullt) | Introduction and main Theorems 1–2 read. The inspected result concerns three involutions, two commuting, in a group of matrices of determinant ±1, and a dimension threshold. The group and generation question differ from the projective PSL(4,q) maximum-rank target. |
| Nuzhin, *Generating Sets of Involutions of Almost Simple Groups and Their Applications*, [publisher](https://link.springer.com/article/10.1007/s10469-026-09809-5), published online 24 January 2026 | Publisher abstract and references read; subscription full text not read. The abstract describes minimum cardinality of generating involutions and rank-three applications, not the target maximum-rank theorem. Its unread full text remains an access limitation. |
| Gvozdev–Nuzhin, *The Groups G₂(2ᵐ) and ³D₄(2³ᵐ) as Automorphism Groups of Regular Polytopes of Ranks 3, 4, and 5*, [publisher](https://link.springer.com/article/10.1007/s10469-026-09844-2), published online 28 August 2026 | Publisher abstract and references read; subscription full text not read. The stated groups and existence results do not settle the target. |
| Anzanello–Fernandes–Spiga, *The maximal rank of a string group generated by involutions for alternating groups*, [arXiv:2505.09169](https://arxiv.org/abs/2505.09169), [institutional publication record](https://boa.unimib.it/handle/10281/597681), [DOI](https://doi.org/10.1515/jgth-2025-0080) | Primary abstract and metadata read. The exact maximum is for alternating groups; it cannot be transferred to this target merely because the vocabulary matches. |
| Chen–Rowley, 2025 finite irreducible Coxeter-group polytope paper, [Electronic Journal of Combinatorics 32(4), P4.18](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p18/pdf/) | Indexed introduction and references inspected. The introduction cites the 2016 PSL(4,q) work; such a retrospective citation is not evidence of a new PSL(4,q) upper bound. Main subject: finite irreducible Coxeter groups. |

These source scopes are intentionally different. “Abstract read,” “selected sections read,” “cached full manuscript read,” and “indexed text inspected” must not be merged into one full-text coverage count.

## 4. Author followups and discovery coverage

The [Leemans publication list](https://leemans.dimitri.web.ulb.be/papers.html) was inspected through its 2026 entries, including the Vandenschrick simple-group paper and the earlier characteristic-two orthogonal and rank-reduction papers. The [official Brooksbank faculty page](https://www.bucknell.edu/fac-staff/peter-brooksbank) leads to his [personal page](https://galois60.github.io/); selected recent papers and current news were inspected. This is not an assertion that either page exhausts all research, student theses or unpublished work. The latter page mixes a 2025 footer with 2026 news; a linked CV could not be retrieved through the web tool.

Leemans's [13 February 2026 slides](https://leandrovendramin.org/team/2026/leemans.pdf), *Constructing coset geometry with Magma*, were downloaded by the parent agent. The PDF has 101 pages implementing 65 numbered slides. Title and relevant string searches were checked here. No PSL(4,q) discussion was found. This is weak negative coverage only: a talk about another subject is not an update on the conjecture's status.

Three OpenAlex metadata responses were archived privately for discovery reproducibility:

1. The DOI record for the 2016 original, work W2268750035, reported 18 citations.
2. Its forward-citation query returned 18 records, including preprint/journal duplicates.
3. The survey preprint work W2981231823 returned 11 forward-citation records.

Those records supplied newer leads, which were checked against primary pages where possible. **The citation index is demonstrably incomplete:** the checked 2026 simple-group manuscript cites the 2016 paper, but did not appear in the returned 18 records. Thus even this bounded list is not a complete forward-citation census. OpenAlex metadata is not used as mathematical evidence.

The machine-readable companion records 41 representative executed searches, source reading depths, failed-access distinctions and hashes of the private cached artifacts. Searches included literal PSL(4,q), PSL_4 and PSL4 variants; orthogonal/PΩ⁺/Omega aliases; the conjecture and survey identifiers; 2020–2026 date terms; and the relevant author names. Mathematical typography was poorly normalized by the search engine, and some Omega queries returned irrelevant results. No automated all-language or all-thesis corpus search was performed.

## 5. Publication boundary

The appropriate public claim is narrow: the workspace contains a **proposed resolution of survey Conjecture 2**, with proof and review status stated separately; this bounded audit located no prior resolution. Do not promote that to “the first proof,” “known to be open as of October 2026,” a resolution of all almost-simple extensions, or a reconstruction of the 2016 existence proof.

The raw third-party PDFs, indexed text and metadata remain private source material. `sources/phase8_psl4_original_rg.html` is explicitly a **failed-retrieval error page**, not an article. This audit creates no new source-access or per-paper coverage classification in the central registry. Its original prose and companion metadata can be exported if the parent integrates them; cached source full texts should remain excluded under the repository's existing export practice.
