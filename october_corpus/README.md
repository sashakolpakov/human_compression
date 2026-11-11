# October corpus

[Human Compression](../README.md) · [November corpus](../november_corpus/README.md) · [Detailed programme](README.rst) · [Reproduction](REPRODUCING.md)

This corpus studies finite groups, polytopes and incidence geometry through
publications by Dimitri Leemans and collaborators. It asks whether reusable
mathematical ideas can recover published results in shorter, complete papers.
Sources, borrowed results and contributions made here receive separate attribution.

## Corpus and progress

The corpus contains **102 manuscripts: 101 mathematical manuscripts and one
editorial**. All **101 mathematical manuscripts have complete reviewed
treatments**: 93 principal-result recoveries and eight treatments following
principal refutations. **Intake is complete.**

| Measure | Count |
|---|---:|
| Mathematical manuscripts | 101 |
| Complete reviewed treatments | 101 |
| Principal-result recoveries | 93 |
| Treatments following principal refutations | 8 |
| Pending mathematical treatments | 0 |
| Measured applications | 53 |
| Recoveries awaiting measurement | 40 |
| Measured topics | 19 |
| Editorials | 1 |

The manuscripts have 103 source components. L063 and its L064 supplementary
appendix form one manuscript. The [source catalogue](audit/corpus/catalogue.json)
retains their separate identities. The [intake status](INTAKE_STATUS.json)
and [source register](audit/corpus/latest.json) give the current counts.

The next stage is measurement of the forty completed, unmeasured recoveries.
Refutation treatments and the editorial receive no ordinary recovery
compression factor. Existing measurements cover 53 applications across 19 topics.

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
| Two-group polytopes and hypertopes | [Topic A](papers/topic-a/v5/PUBLICATION.rst) |
| Forest coordinates and primitive coset geometries | [Topic B](audit/topic-b/v4/README.rst) |
| Halving and Petrial operations | [Topic C](papers/topic-c/extensions/livingstone/v1/PUBLICATION.rst) |
| Marked actions, field orbits and geometry enumeration | [Topic D](papers/topic-d/v2/README.rst) |
| Projective centralizers, polytopes and maniplexes | [Topic E](papers/topic-e/v3/README.rst) |

The [measurement overview](audit/overview/README.md) lists all nineteen
whole-topic comparisons and the 53 measured applications. Read the
[measurement policy](audit/measurement_policy/v1/README.rst) before interpreting
those factors. Required common material, local arguments,
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

## Selected results

The [equal-label polygon application](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/EQUAL_LABEL_POLYGONS.md)
recovers Li–Zhang’s complete stated rank-three results from the earlier polygon
construction and an exact presentation proof. The
[common projective-line proof](papers/topic-e/v3/README.rst) recovers two more
principal classifications. Its [maniplex application](papers/topic-e/v3/projective-maniplexes.pdf)
recovers the full specified PSL₂ maniplex contract, including the required
source corrections. The
[odd-kernel application](papers/topic-f/v3/README.rst) recovers L014’s three main
theorems through characters and a cyclotomic module, with an explicit
source correction and the retained tightness classification. The
[mixed-prime application](papers/topic-affine/v2/README.rst) completes L012’s
stated classifications and constructions using affine periods and supported
extensions, with its source-sign correction and full retained costs explicit.

The [primitive-square result](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/PRIMITIVE_SQUARES.md)
has a complete independent arithmetic review, fresh exceptional-case checks
and six additional Lean declarations for its polynomial arguments.

The [Hermitian-unital result](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/HERMITIAN_UNITALS.md)
includes its complete independent review and thirteen Lean declarations for
explicit unitary transport, a reusable part of the connectivity proof.

The [triangle-geometry theory and application](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/TRIANGLE_GEOMETRIES.md)
recover the complete corrected principal L009 classification in two papers
of five and eight pages in that edition. Their retained classifications,
geometric proofs and required programs remain explicit. Four Lean declarations
verify the determinant and orbit interface. The later
[Topic G guide](papers/topic-g/v2/README.rst) describes the expanded common theory
and applications.

### Answers to open questions

The earlier [question ledger](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/CONJECTURE_RESULTS.md)
records exact statements, the extent of each proof, checks of later literature
and uncertainty about priority. These results are assessed separately from
compression of previously proved results. The
[attribution legend](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/ATTRIBUTION.md)
distinguishes earlier ideas, contributions made here, corrections, finite checks
and Lean proofs.

The [point-cloning counterexample](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/POINT_CLONING.md)
refutes the journal gonality-two experimental suggestion under its stated
definitions. It gives an infinite family, independent checks and four
axiom-free Lean path proofs.

The [four PGL maniplex families](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/PGL_MANIPLEX_FAMILIES.md)
answer the 2023 source conjecture in all four cases, with explicit prime
progressions, a complete written proof and independent review. Eleven Lean
declarations verify its matrix and unipotent algebra. A full Lean
formalization and historical priority remain unverified.

The [label-eleven obstruction](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/LABEL_ELEVEN_OBSTRUCTION.md)
gives a complete negative answer to Li–Zhang’s preprint Conjecture 3.7:
every rank d≥5 is excluded at that label. The full proof, independent review,
finite certificates and precise Lean coverage are recorded in the linked
note. The [coset certificates](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/COSET_CERTIFICATES.md)
add kernel-checked bounds through rank three; the larger computations remain
outside Lean. The source edition and historical-priority qualifications
remain part of the claim.

The [general theorem on minimal covers](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/MINIMAL_REGULAR_COVERS.md)
answers Cunningham–Pellicer’s unrestricted question: a polytope of finite rank
has a unique minimal regular polytopal cover exactly when its monodromy group
is a string C-group. The full written proof and independent review cover
arbitrary flag sets; five Lean declarations verify the stated algebraic
steps. The covers may be infinite. The recorded bounded literature audit
found no earlier complete resolution; historical priority remains unverified.

The [finite rank-four cover theorem](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/FINITE_RANK_FOUR_COVERS.md)
proves infinitely many finite minimal regular covers for every finite rank-four
polytope with non-C monodromy. It has a complete seven-page proof, independent
review and five scoped Lean declarations. The
[interval theorem](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/INTERVAL_MINIMAL_COVERS.md)
extends it to every ambient rank containing a non-C four-mark interval;
the remaining finite higher-rank cases are open in those notes.

The [surface construction](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/INFINITE_MINIMAL_COVERS.md)
gives infinitely many finite minimal regular covers throughout four specified
families, by an argument valid for every odd prime. The
[square-torus application](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/SQUARE_TORUS_COVERS.md)
proves infinitely many finite minimal covers for every odd square-torus pyramid,
with controlled prime-power kernels for every permitted prime. The
arbitrary-polytope finite version is unresolved in these notes.

The [locally faithful cover criterion](https://github.com/sashakolpakov/human_compression/blob/3b067cc2eba4ac2f2f91248448727639d8ac7c5a/LOCALLY_FAITHFUL_COVERS.md)
gives an exact homology test for abelian covers preserving both end subgroups.
Its Tomotope application classifies that restricted class and excludes every
nontrivial odd-prime-power kernel. Three Lean declarations check its quotient
interfaces; the general finite question remains outside that result.

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


Start with the [reproduction guide](REPRODUCING.md) and the selected paper's
guide. Keep generated builds and scratch outputs outside the checkout.
