# Human Compression

[Public repository](https://github.com/sashakolpakov/human_compression)

Can a few reusable mathematical ideas, developed with a strong language model
and agents, recover decades of published results in shorter, complete papers?
We test that question on finite groups, polytopes and incidence geometry,
with explicit attribution, source contracts and proof verification.

## The current product

A **module is a mathematical topic containing several of our papers**.
Topic A has an umbrella theory U_A and application papers A₁, A₂, …,
matched to historical manuscripts LA₁, LA₂, …. Topic B has its own U_B
and B₁, B₂, …, matched to LB₁, LB₂, ….

The umbrellas may share mathematics. Each topic's independent complexity
comparison charges its **full umbrella once**, then all its complete
application papers and required proof artifacts. Topic B pays for all of
U_B even when it overlaps U_A. A separate chronological library-reuse
account may discount already paid proofs under explicit conditions.

Read the [manuscript programme](MANUSCRIPT_PROGRAM.md),
[topic complexity protocol](TOPIC_COMPLEXITY.md),
[dependency pilot](DEPENDENCY_PILOT.md) and
[proof-library rules](PROOF_LIBRARY.md).

## Work available for reuse

The existing A–D manuscripts are **reviewed monolithic drafts to rework**
into topic families. Their proofs, source ledgers and certificates remain
usable. They are not already the requested A₁, A₂, … decomposition, and
renaming their sections would not establish that decomposition.

| Mathematical topic | Reviewed material and restructuring status |
|---|---|
| Two-group polytopes and hypertopes | [A source material](MODULE_A.md) |
| Forest coordinates and primitive coset geometries | [B source material](MODULE_B.md) |
| Halving and Petrial operations on regular geometries | [C source material](MODULE_C.md) |
| Marked actions, field orbits and geometry enumeration | [D source material](MODULE_D.md) |

The [existing umbrella manuscript](UMBRELLA.md) supplies proved components
for choosing and completing each topic's umbrella. The
[current work index](CURRENT_REPORT.md) also lists later applications and
partial source contracts. The [source registry](PAPER_MAP.md) records intake;
its coverage counts are not counts of completed topic papers.

Earlier combined compilations, edition measurements, status reports and
the coarse complexity plot are isolated in the [historical archive](archive/README.md).
Their measurements remain attached to their original artifacts. No historical
rate is presented here as a result for the new topic architecture.

## Proof and attribution

Each application must derive its declared historical principal results,
including substantial local arguments and exceptional cases. Borrowed
ideas and retained theorems keep their attribution. The
[annotation legend](ATTRIBUTION.md) distinguishes reuse, repository
contributions, corrections, finite checks and scoped Lean proofs.
A helper certificate does not verify a whole manuscript.

[Open-question results](CONJECTURE_RESULTS.md) have a separate ledger,
including exact statements, proof scope, later-literature checks and
uncertainty about priority. They do not inflate compression ratios for
previously proved results.

The proposed acquisition-and-reuse pattern draws on
[GKM](https://github.com/sashakolpakov/gkm). It must appear in measured
proof costs and valid dependencies. Node counts, paper counts and a few
favorable checkpoints do not establish that pattern.

See [reproduction instructions](REPRODUCING.md) and the
[formal certificate scopes](research/case_study/formal/README.md).

```sh
python3 scripts/verify_snapshot.py
python3 scripts/smoke_check.py --quick
```

Primary publications are referenced through their
[citations and checksums](research/case_study/sources/README.md).
[Provenance](provenance/README.md) preserves frozen artifacts and reviews.
