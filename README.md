# Human Compression

[Public repository](https://github.com/sashakolpakov/human_compression)

How much published mathematics can a small reusable theory and a strong
language model recover in substantially shorter, complete manuscripts?

This project studies a connected research literature in finite groups,
symmetric polytopes and incidence geometry. Its product is an **umbrella
theory U and a series of focused application manuscripts A, B, C, …**.
Each application manuscript groups mathematically similar source papers
and derives their principal results using U. It cites the umbrella
results without repeating their proofs. The intended application volume
is about 20–25 pages in ordinary academic style, with complete arguments.
A successful volume may replace a dozen papers or several years of work;
its actual source coverage and savings must be established.

Read the [manuscript programme](MANUSCRIPT_PROGRAM.md),
[current report](CURRENT_REPORT.md), [source registry](PAPER_MAP.md),
and [method and measurement rules](PROOF_LIBRARY.md).

## Current work

The active manuscripts have descriptive mathematical titles:

- **[Umbrella theory U: Marked groups, kernels and intersections](UMBRELLA.md).**
- **[Module A: Construction and classification of two-group polytopes](MODULE_A.md).**

**Complete drafts are available for review:** U has 28 statements with
proofs; A has 21 rendered pages. U develops
exact kernels, marked subgroup intersections, compatible extensions and
finite actions. Module A starts with five related papers on groups and
polytopes of two-power order, spanning 2018–2026. Its source-specific
classification and geometric arguments remain complete application proofs.
Additional sources enter only when their main results actually follow.
The [root review](research/case_study/phase127_modular_root_review.md)
records a complete proof reading and fresh reproduction checks. Full
formalization, final source admission and matched measurement remain pending.

The previous combined manuscripts are working source material. Their
proved lemmas, computations, source readings and certificates are being
reworked into U and the modules; their organization and size are not the
new project's product or benchmark. Historical records remain available
in [the research directory](research/case_study) and earlier commits.

The intake contains **161 indexed works**, with **102 complete texts
retrieved**, **39 named result/component rederivations**, and **17 records
covering all identified principal results**. These categories overlap.
They do not count completed modular manuscripts or a complete bibliography
of every collaborator. The existing working compilations now account for
thirteen distinct principal-result contracts.

A parallel track inventories every explicit conjecture, open question and
unresolved case in the intake, checks later work, and attacks related
questions through shared theory. The
[question-results catalogue](CONJECTURE_RESULTS.md) keeps recorded answers,
qualified cases and formalization gaps separate from compression credit.
The separately reviewed
[five-family cover result](COVER_FIVE_FAMILIES.md) establishes the stated
multiplicity assertion in the checked source proposal. Historical priority
and current openness remain unverified; the general conjecture is unresolved.

## What counts as compression

Each module names its sources, editions, main-result contracts and retained
inputs. It includes the complete application arguments. We report its
length conditional on U and the combined length with U charged once.
Repeated source memberships are counted once in a combined comparison.
Required proof appendices and computational certificates remain explicit.
Proof length, reproducibility cost and research/search effort are separate.

The method draws on [GKM](https://github.com/sashakolpakov/gkm): preserve
verified reusable components, pay for every application, and refactor when
new cases reveal shared structure. We track total cost, gross additions,
removals and marginal cost. A sawtooth pattern is a testable outcome,
not an assumed conclusion. Original source lengths are measured under
matched contracts and stated conventions. Expansion is reported as openly
as a large saving. Historical compilation measurements do not transfer
to U or a new module.

Established mathematics and original results remain attributed to their
authors. Our contributions are identified theorem by theorem. Claims
concern mathematical derivations, not the worth of their authors.

## Proofs and verification

The manuscripts use ordinary mathematical exposition at a level of detail
comparable to their source literature. Shared proofs occur once in U;
applications discharge their hypotheses and include exceptional cases.
Lean verification must match our actual written statements, including
assumptions and retained inputs. A certified helper does not certify an
entire application. Formal gaps and axioms remain visible.

Forty-four existing scoped Lean components and exact computational
certificates supply reusable verified material. They do not constitute
an end-to-end formalization of U, Module A or all conjecture claims.
See [reproduction instructions](REPRODUCING.md) and individual scope files.

```sh
python3 scripts/verify_snapshot.py
python3 scripts/smoke_check.py --quick
```

Primary papers and source-page images are not redistributed. Their
[citations and checksums](research/case_study/sources/README.md) remain
available. [Provenance](provenance/README.md) records frozen artifacts,
corrections and independent reviews.
