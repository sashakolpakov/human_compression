# Human Compression

[Public repository](https://github.com/sashakolpakov/human_compression)

Can a few reusable mathematical ideas, developed with a strong language model
and agents, recover decades of published results in shorter, complete papers?
We test that question on finite groups, polytopes and incidence geometry,
with clear attribution, precise statements of the results recovered and checked proofs.

## The current product

A **module is a mathematical topic containing several of our papers**.
Topic A has an umbrella theory U_A and application papers A₁, A₂, …,
corresponding to historical manuscripts LA₁, LA₂, …. Topic B has its own U_B
and B₁, B₂, …, matched to LB₁, LB₂, ….

The umbrellas may share mathematics. Each topic's independent complexity
comparison charges its **full umbrella once**, then all its complete
application papers, required appendices and mathematical programs.
Topic B pays for all of U_B even when it overlaps U_A. A separate account
of reuse over time may discount proofs already paid for, under explicit
conditions.

Read the [manuscript programme](MANUSCRIPT_PROGRAM.md),
[topic complexity protocol](TOPIC_COMPLEXITY.md),
[dependency pilot](DEPENDENCY_PILOT.md) and
[proof library](PROOF_LIBRARY.md).

## Work available for reuse

The existing A–D documents each combine several sources in one reviewed
manuscript. They must be **reworked into families of papers on each topic**.
Their proofs, records of the source results and certificates remain
usable. [Topic A now has a complete umbrella and first application](TOPIC_A.md),
independently reviewed and rendered at 15 and 4 pages. The remaining
application families are unfinished.

| Mathematical topic | Reviewed material and restructuring status |
|---|---|
| Two-group polytopes and hypertopes | [Complete U_A and first application](TOPIC_A.md); [remaining source material](MODULE_A.md) |
| Forest coordinates and primitive coset geometries | [B source material](MODULE_B.md) |
| Halving and Petrial operations on regular geometries | [C source material](MODULE_C.md) |
| Marked actions, field orbits and geometry enumeration | [D source material](MODULE_D.md) |
| Projective centralizers and regular polytopes | [Complete U_E and two applications](PROJECTIVE_LINE_POLYTOPES.md): 7 + 3 + 2 pages |

The [existing umbrella manuscript](UMBRELLA.md) supplies proved components
for choosing and completing each topic's umbrella. The
[current work index](CURRENT_REPORT.md) also lists later applications and
results that recover only part of a source paper. The
[source registry](PAPER_MAP.md) records the papers studied and the results
recovered. These totals do not measure completion of the new application papers.

Earlier combined compilations, edition measurements, status reports and
the coarse complexity plot are isolated in the [historical archive](archive/README.md).
Their measurements apply to those earlier versions. The first
[measurement of a complete topic](TOPIC_E_MEASUREMENT.md) is now available:
the two projective-line applications give conditional factors of 1.62× and
2.38×, but their full umbrella has not yet paid for itself. The designated
total written factor is 0.835×; other topics remain to be measured.

The [equal-label polygon application](EQUAL_LABEL_POLYGONS.md) recovers
Li–Zhang’s complete stated rank-three results from the earlier polygon
construction and an exact presentation proof. The
[common projective-line proof](PROJECTIVE_LINE_POLYTOPES.md) recovers two more
principal classifications. In total, **25 of the 161 indexed works** have
their specified main results recovered. The
[odd-kernel application](ODD_KERNEL_POLYHEDRA.md) adds L014’s three main
theorems through characters and a cyclotomic module, with an explicit
source correction and the retained tightness classification. The
[mixed-prime application](MIXED_PRIME_POLYHEDRA.md) completes L012’s
stated classifications and constructions using affine periods and supported
extensions, with its source-sign correction and full retained costs explicit.
This count is distinct from the number of completed new topic papers.

## Proof and attribution

Each application must derive the historical main results it promises to recover,
including substantial local arguments and exceptional cases. Borrowed
ideas and earlier theorems used here keep their attribution. The
[annotation legend](ATTRIBUTION.md) distinguishes reuse, repository
contributions, corrections, finite checks and Lean proofs, with their
hypotheses and limits stated.
A Lean proof of one supporting lemma does not verify a whole manuscript.

[Open-question results](CONJECTURE_RESULTS.md) have a separate ledger,
including exact statements, the extent of each proof, checks of later
literature and uncertainty about priority. These results are assessed
separately from compression of previously proved results.

The [label-eleven obstruction](LABEL_ELEVEN_OBSTRUCTION.md) gives a
complete negative answer to Li–Zhang’s preprint Conjecture 3.7: every
rank d≥5 is excluded at that label. The full proof, independent review,
finite certificates and precise Lean coverage are included. The
[new coset certificates](COSET_CERTIFICATES.md) add kernel-checked bounds
through rank three; the larger computations remain outside Lean.
The [edition audit](research/case_study/phase220_F014_edition_review.md)
records the remaining limits on journal-version and priority claims.

The [general theorem on minimal covers](MINIMAL_REGULAR_COVERS.md)
answers Cunningham–Pellicer’s unrestricted question: a polytope of finite
rank has a unique minimal regular polytopal cover exactly when its
monodromy group is a string C-group. The full written proof and
independent review cover arbitrary flag sets; five new Lean declarations
verify the stated algebraic steps. The covers may be infinite. A
[bounded literature audit](research/case_study/phase227_priority_audit.md)
found no earlier complete resolution; historical priority remains unverified.

The [surface construction](INFINITE_MINIMAL_COVERS.md) gives the stronger
conclusion of infinitely many **finite** minimal regular covers throughout
four specified families, by an argument valid for every odd prime. A
[new uniform application](SQUARE_TORUS_COVERS.md) proves infinitely many
finite minimal covers for every odd square-torus pyramid, with controlled
prime-power kernels for every permitted prime. The arbitrary-polytope
finite version remains unresolved.

The study of costs as proofs are developed and reused draws on
[GKM](https://github.com/sashakolpakov/gkm). The proposed sawtooth pattern
must appear in measured proof costs and valid dependencies. Node counts,
paper counts and a few favorable checkpoints do not establish that pattern.

See [reproduction instructions](REPRODUCING.md) and the
[Lean statements and limitations](research/case_study/formal/README.md).

```sh
python3 scripts/verify_snapshot.py
python3 scripts/smoke_check.py --quick
```

Primary publications are referenced through their
[citations and checksums](research/case_study/sources/README.md).
[Provenance](provenance/README.md) preserves frozen artifacts and reviews.
