# October corpus

[Human Compression](../README.md) · [Current programme](README.rst) · [Reproduction](REPRODUCING.md)

This corpus studies finite groups, polytopes and incidence geometry through
publications by Dimitri Leemans and collaborators. It asks whether a few
reusable mathematical ideas, developed with a strong language model and
agents, can recover decades of published results in shorter, complete papers.
Sources, borrowed results and contributions made here receive separate
attribution.

This overview carries forward the original project README. Its navigation now
points to the published corpus files; the detailed [current programme](README.rst)
and [original register](audit/corpus/latest.json) record the exact dispositions.

## Current position

The accessible catalogue contains **106 original sources**: 105 mathematical
manuscripts and one editorial. **102 of the 105 mathematical originals have
complete reviewed treatments**: 93 principal-result recoveries and nine
complete treatments following principal refutations. **F004, F009 and L026
remain.** The editorial has no mathematical result to recover.

Of the recoveries, **53 have published measurements** and forty await
measurement. The current [measurement overview](audit/overview/latest.json)
contains nineteen whole-topic comparisons and 53 individual conditional
comparisons. These measurement counts are distinct from the intake counts.
The stopping point for the current intake is completion of the remaining
three mathematical originals.

## Common theories and applications

A module is a mathematical topic containing several of our papers. Topic A
has common theory U_A and application papers A₁, A₂, …, corresponding to
historical manuscripts LA₁, LA₂, …. Topic B has its own U_B and applications.
The common theories may share mathematics; each topic's independent
comparison charges its full common theory once.

The following are entry points into the published topic families, rather
than a complete list of the corpus's topics.

| Topic | Published guide |
|---|---|
| Two-group polytopes and hypertopes | [Topic A](papers/topic-a/v3/README.rst) |
| Forest coordinates and primitive coset geometries | [Topic B](papers/topic-b/v3/README.rst) |
| Halving and Petrial operations | [Topic C](papers/topic-c/v2/README.rst) |
| Marked actions, field orbits and geometry enumeration | [Topic D](papers/topic-d/v2/README.rst) |
| Projective centralizers, polytopes and maniplexes | [Topic E](papers/topic-e/v3/README.rst) |

The [six-page overview](audit/overview/v19/packet/reader.pdf),
[whole-topic graph](audit/overview/v19/packet/whole_topics.svg),
[first 27 individual comparisons](audit/overview/v19/packet/conditional_1.svg)
and [remaining 26 comparisons](audit/overview/v19/packet/conditional_2.svg)
show the measured results. Read the [measurement policy](audit/measurement_policy/v1/README.rst)
before interpreting those factors. Required common material, local arguments,
exceptional cases and retained inputs must remain visible. Software-inclusive
factors require an inventory on both sides.

The study of costs as proofs are developed and reused draws on
[GKM](https://github.com/sashakolpakov/gkm). A proposed sawtooth pattern must
be demonstrated by measured costs and valid dependencies. A few favorable
checkpoints do not establish it.

## Proof, attribution and open questions

Each application must derive the historical main results it promises to
recover, including substantial local arguments and exceptional cases. Earlier
theorems and constructions keep their attribution. Written proofs, finite
computations, independent reviews and Lean declarations have separately
stated scopes; none silently stands in for the others.

The [current programme](README.rst) links the complete treatments, corrections
and question results. The [answers directory](answers/) records answers to
open questions separately from recoveries of previously proved results; the
[corrections directory](corrections/) records specified source errors and their
replacements. A conjecture claim must identify its edition, hypotheses and
remaining qualifications. Neither a new answer nor a refutation receives an
ordinary compression factor without a comparison of equivalent results.

## Files and reproduction

| Directory | Contents |
|---|---|
| [papers/](papers/) | Mathematical manuscripts, application families and paper guides |
| [audit/](audit/) | Source contracts, registers, measurements, admissions and reviews |
| [answers/](answers/) | Results addressing open questions |
| [corrections/](corrections/) | Corrections to specified source claims |
| [data/](data/) | Retained data and certificates |
| [scripts/](scripts/) | Checkers, replay tools and paper builders |
| [research/](research/) | Earlier proof components and formal sources |
| [provenance/](provenance/) | Frozen artifacts and their recorded provenance |
| [archive/](archive/) | Earlier editions and historical material |

Start with [the instructions for the new directory layout](REPRODUCING.md),
then the [detailed reproduction guide](docs/REPRODUCING.rst) and the selected
paper's guide. Keep generated builds and scratch outputs outside the checkout.
The migration preserves all previously tracked corpus files and their history;
it adds no mathematical result, reviewed original or compression measurement.
