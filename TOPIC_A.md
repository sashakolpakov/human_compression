# Topic A: Two-group polytopes and hypertopes

The first complete pair of papers is available and independently reviewed:

| Paper | Complete text | Results supplied |
|---|---|---|
| **U_A: Supported extensions and finite two-group quotients** | [PDF, 15 pages](research/case_study/phase228_umbrella.pdf); [Markdown](research/case_study/phase207_topic_A_umbrella.md) | Supported extensions, exact kernel profiles and intersections, geometric transfer, the forest quotient, finite exhaustive quotients, affine square groups and dihedral attachments |
| **A₁: Prescribed rank, type and two-power order** | [PDF, 4 pages](research/case_study/phase228_application.pdf); [Markdown](research/case_study/phase207_L032_application.md) | Hou–Feng–Leemans, L032 Theorem 1.2, for every stated parameter, plus the necessary order bound attributed to Conder |

The exact recovery is

$$
U_A+A_1\quad\Longrightarrow\quad
\text{L032, Theorem 1.2 and the attributed Proposition 2.2}.
$$

For all d≥3, n≥5 and kᵢ≥2 with Σkᵢ≤n−1, A₁ constructs a regular
polytope of rank d, type {2^k₁,…,2^k₍d−1₎} and exactly 2^n flags.
It checks the actual local quotient maps, full generation, intersections,
string commutation and order. It does not classify every realizing group
or identify its construction with the source's particular presentation.

The [independent review](research/case_study/phase228_topic_A_review.md)
and [24-clause contract](research/case_study/phase228_source_contract.json)
cover both complete papers. They rework already established project proofs;
they add no new historical theorem or principal-source credit.
L032 was already among the twenty recovered principal contracts.
The [provenance ledger](research/case_study/phase207_umbrella_provenance.json)
identifies every reused proof passage and local addition.

The full U_A is charged once for this topic. The 15+4 pages are the actual
reviewed renderings; the historical edition has eight pages. These use
different source layouts and are not a matched compression ratio.
U_A supports more than this first application, so its acquisition cost
has not yet been compared with a finished application collection.
Another topic pays its own full umbrella independently.
See the [cost record](research/case_study/phase228_cost_scope.json).

Fresh Lean replay checks 34 inherited declarations about the supported
construction and its consequences. The forest argument, affine construction
and complete geometric application remain written proofs; neither whole
paper is formalized in Lean. See the [replay instructions](research/case_study/phase228_replay.md).

Five further applications remain to be reworked from the [existing proof
material](MODULE_A.md): L035's eight rank-three families, F013's canonical
quotient, F016's section and extension constructions, N009's order-1024
census, and L034's prescribed hypertopes. The independent review identifies
their additional obligations. They are not counted as completed
standalone papers merely because their proofs occur in the earlier compilation.
