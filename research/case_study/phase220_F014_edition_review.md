# F014: edition, literature status, and significance

Audit date: 10 October 2026. This is a bounded source audit, separate from the accepted mathematical proof and its independent computational review.

The result established by the project is a computer-assisted disproof of **Conjecture 3.7 in Mingchao Li and Wei-Juan Zhang, arXiv:2505.09505v1 (14 May 2025), page 11**. Its label is (n=11), in every rank (d\geq5). The proof identifies the rank-five universal group for the displayed relations as (C_2\times\operatorname{Sp}_4(32)), and excludes the intersection property in every quotient retaining the prescribed adjacent orders. The proof and computational evidence are in the frozen phase212, phase214, and phase215 packages. This audit does not repeat or enlarge that proof.

## Editions actually inspected

| Edition or source | Evidence available | Conclusion |
|---|---|---|
| [arXiv:2505.09505v1](https://arxiv.org/abs/2505.09505v1), 14 May 2025 | Complete 12-page PDF; Conjecture 3.7 on printed page 11 | The conjecture has the quantifiers and local relations used in the accepted disproof. |
| [Current arXiv record](https://arxiv.org/abs/2505.09505), checked 10 October 2026 | Fresh submission-history page | Only v1 is listed. No later arXiv edition was identified. |
| [Journal of Algebra 695 (2026), 1–13](https://doi.org/10.1016/j.jalgebra.2026.01.041) | Publisher preview, Crossref metadata, and publisher API metadata | The journal edition exists. Its accessible introduction differs from v1. Its final conjecture section was not obtained. |

The journal preview credits Cunningham–Mixer for earlier rank-three existence and reformulates Problem 1.1 around an explicit presentation and a precisely determined, relatively small group order. This establishes an introductory revision. It does **not** establish whether Conjecture 3.7 was retained, renumbered, altered, or removed. The preview stops early in Section 3; absence of the conjecture from that preview is not evidence of removal. The public claim should continue to identify the preprint edition exactly.

## Access and search limits

The legitimate routes checked were the publisher article and PDF endpoints, the Crossref-listed publisher text-mining endpoint, the current arXiv version history, the authors' institutional and ORCID discovery routes, and repository discovery through OpenAlex. The publisher PDF endpoint returned HTTP 403. The public publisher API supplied bibliographic metadata only. OpenAlex listed the journal article as closed and identified no repository full text. The relevant institutional profile and ORCID record supplied no manuscript or personal-homepage link. None of these observations implies that an accessible copy exists nowhere.

Targeted searches used the title, DOI, arXiv identifier, conjecture number, label 11, several notations for the symplectic group, its order, and correction/refutation terms. No primary later source giving this exact obstruction or universal-group identification was located. OpenAlex reported zero indexed citations to its journal record, a database observation with no implication of completeness. The later primary preprint *Testing chirality on hypertopes* was screened for a relevant citation; none was found. The machine-readable ledger records the actual queries and the limited conclusions.

**Novelty and current published-conjecture status remain unverified.** No priority claim, exhaustive literature claim, or claim that a currently open journal conjecture has been settled follows from this search. Obtaining the complete journal edition and inspecting its final Section 3 would settle the edition question. It would not by itself settle priority.

## Mathematical significance

The obstruction addresses an existence assertion over all quotients satisfying specified relations. A failed matrix construction alone would not answer that assertion. The universal-group upper bound, matching signed matrix image, and quotient argument together exclude every candidate at (n=11,d=5); the parabolic argument excludes all larger ranks with the same label. This is a substantive negative result within regular-polytope and string-C-group construction: the proposed local rank-three relations cannot always be assembled into the conjectured higher-rank objects.

That assessment is a mathematical judgment about the proved statement, not evidence of historical novelty or wider influence. It does not refute Li–Zhang's rank-three construction, their explicit rank-three group order, or unrestricted existence of regular polytopes of the same Schläfli type without the additional relations. It does not classify every remaining parameter pair. A conjecture disproof is not a replacement of the whole source paper and earns no whole-manuscript compression credit.

For historical context, the complete primary [Cunningham–Mixer paper](https://cdm.ucalgary.ca/article/download/62785/46842/179298), *Contributions to Discrete Mathematics* 12(2) (2017), 187–214, Theorem 5.1 on page 201, already establishes internally self-dual regular polyhedra of type \(\{p,p\}\) for every \(p\geq3\), and externally self-dual examples for \(p\geq4\). This concerns rank three and imposes no Li–Zhang triple-power presentation. The journal's more specific construction problem therefore must be distinguished from unrestricted existence.

## Recommended public wording

> We give a computer-assisted disproof of Conjecture 3.7 in Li–Zhang's May 2025 preprint: for label 11, no quotient satisfying the stated relations can define the proposed regular polytope in rank at least five. The exact 2026 journal conjecture text and priority of this obstruction have not been verified.

The direct authors of F014 are Mingchao Li and Wei-Juan Zhang. The project should attribute the conjecture to them, preserve the earlier results just identified, and describe its own contribution as the universal-group and quotient obstruction. No conclusion about the quality or motives of a research group follows from this result.
