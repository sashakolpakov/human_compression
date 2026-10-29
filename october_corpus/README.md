# October corpus

[Human Compression](../README.md) · [November corpus](../november_corpus/README.md) · [Current programme](README.rst) · [Reproduction](REPRODUCING.md)

This corpus studies finite groups, polytopes and incidence geometry through
publications by Dimitri Leemans and collaborators. It asks whether a few
reusable mathematical ideas, developed with a strong language model and
agents, can recover decades of published results in shorter, complete papers.
Sources, borrowed results and contributions made here receive separate
attribution.

This is the corpus README carried forward from the original project overview.
Its navigation points to the published corpus files. The [detailed programme](README.rst)
and [source register](audit/corpus/latest.json) retain their recorded counts;
the [manuscript accounting audit](audit/corpus/proposals/manuscript-accounting/README.rst)
explains the correction from source components to manuscripts used below.

## Current position

The accessible corpus contains **105 manuscripts**: 104 mathematical manuscripts
and one editorial. **101 of the 104 mathematical manuscripts have complete
reviewed treatments**: 93 principal-result recoveries and eight complete
treatments following principal refutations. **F004, F009 and L026 remain.**
The editorial has no mathematical result to recover.

These manuscripts have 106 registered source components. L063 and L064 are
the main article and its supplementary appendix, counted together as one
manuscript. The accounting audit preserves both source IDs and all their
results. Its catalogue correction is published as a proposal; existing
catalogue pointers remain unchanged while computations bound to them finish.

Of the recoveries, **53 have published measurements** and forty await
measurement. The current [measurement overview](audit/overview/latest.json)
contains nineteen whole-topic comparisons and 53 individual conditional
comparisons. These measurement counts are distinct from the intake counts.
The stopping point for the current intake is completion of the remaining
three mathematical originals.

The [latest archived intake results](research/proof_collection/updates/curated_cp11216_job23_gen27neg68_20261029/README.rst)
contain F009's accepted checkpoint 11,216 and all 21 required historical
payloads, 38 further F004 exclusions in job 23, and the Fi22 ledger with
27 generation and 68 additional nongeneration certificates. The intersection
property for the generating markings follows separately from the cited
theorem. The archive also preserves the later F009 proposal at 11,262 and
its earlier failed verifier run. All seven archive integrity checks passed.
These finite results add no completed manuscript or compression measurement.

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

## Results carried forward from the original README

The descriptions below preserve the original README's named results and
their qualifications. Links to earlier proof notes use a fixed Git commit;
the [archive register](audit/archive_markdown.json) records those documents.
The current programme above gives the later source treatments and measurements.

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

The [two graph examples](research/graphs/diameter_eight/README.rst) provide
independent proofs and standalone checks for graphs of diameter eight,
together with a counting reduction for the unfinished graph census.
Both checks passed from an isolated copy of the package.

The [common commutant example](research/groups/common_commutant/README.rst)
uses one matrix to exclude every completion of a specified group prefix.
Its standalone checker verifies the finite tables and witness; the original
group correspondence remains an explicit premise. A further reviewed theory
describes affine witness spaces for general commutation constraints.

The [marked matrix obstruction certificates](research/groups/marked_obstructions/README.rst)
check supplied witnesses for all 694 tuples in one F004 candidate family
using only Python's standard library. The original-group correspondence
and the classification used by 129 cases remain explicit premises;
F004 remains unfinished.

The [shared matrix certificates](research/groups/shared_obstructions/README.rst)
check 16,352 supplied obstructions across five F004 families, using one matrix
table. Their portable arithmetic check passed from an isolated copy. That
package retains 62 unresolved positions and explicitly states the imported
group, frame, orbit and classification premises; it adds no completed manuscript
or compression measurement.

The [complete census for these five families](research/groups/marked_census/README.rst)
now classifies all 16,414 original positions: 14 valid markings and 16,400
obstructions. Its independent reproduction passed from an isolated copy in
52 seconds, using about 104 MB of memory. The package includes the proofs,
compact certificate data and a standard library checker. Other F004 families
remain to be completed.

The [involution centralizer bound](research/groups/involution_centralizers/README.rst)
has a complete TeX proof and independent agent review. A subgroup of the
specified equal-determinant group containing a Klein four and avoiding its
central involution has order at most 1,320. This gives a compact obstruction
criterion for rank-five markings under an explicit centralizer identification.
It adds no completed census or manuscript.

The [packed conjugacy-key example](research/onan/packed_keys/README.rst) builds
the new permutation kernel from source and runs its eighteen kernel checks
and ten I/O checks. These small tests are separate from the unfinished O'Nan census.

The [permutation certificate kernel](research/onan/generation_certificates/README.rst)
checks supplied cycles, transitivity trees and invariant sets. Its corrected
25-test suite passed after a fresh compilation and review of the execution.
The production adapter and group census require further checks.

The [nonfree O'Nan orbit certificate](research/onan/nonfree_orbits/README.rst)
conditionally excludes all 1,776 nonfree rows in the retained endpoint index.
Its standalone check passed from an isolated copy; named-group, model and
exact-orbit premises remain explicit. This partial L026 result adds no completed original.

The [Fi22 involution geometry](research/fi22/involution_geometry/README.rst)
derives products, stabilizers and orbit weights from commuting edges and
triangle pairs. Its conditional written proof has an independent review;
the model correspondence and census computations remain to be acquired.

Start with [the instructions for the new directory layout](REPRODUCING.md),
then the [detailed reproduction guide](docs/REPRODUCING.rst) and the selected
paper's guide. Keep generated builds and scratch outputs outside the checkout.
The migration preserves all previously tracked corpus files and their history;
it adds no mathematical result, reviewed original or compression measurement.
