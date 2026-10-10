# Even subsets of a polygon and an equal-label presentation

The complete positive rank-three results of Li–Zhang's 2025 preprint
follow from the polygon construction already in the shared theory, with
an explicit identification and presentation proof:

$$
\text{C.Polygon}+\text{this application}
\quad\Longrightarrow\quad
\text{F014, Theorems 1.3, 3.4 and Corollaries 3.5–3.6}.
$$

Read the [complete application, five pages](research/case_study/phase232_application.pdf),
[Markdown](research/case_study/phase229_equal_label_application.md),
[independent review](research/case_study/phase232_review.md) and
[exact source contract](research/case_study/phase232_contract.json).

For every n≥3, the group is the even-coordinate subspace of F₂ⁿ acted on
by the dihedral symmetries of an n-cycle. The explicit marking gives a
self-dual regular polyhedron of type {n,n}, with exactly n2ⁿ flags.
The application proves the exact universal presentation for every n;
a quotient with the right order alone would not establish that assertion.

| Annotation | Attribution and contribution |
|---|---|
| **[B]** | Montero–Ivić Weiss's 2020 polygon construction already supplies existence, order and self-duality. The retained proof is [C.Polygon](research/case_study/phase150_module_C_manuscript.md). |
| **[B]** | Li–Zhang supply the presentation and its commuting-displacement argument; the standard polytope correspondence is due to McMullen–Schulte. |
| **[I], [R]** | The application identifies both constructions and the source's matrices, proves the complete normality and order argument, and recovers all four named principal statements. |
| **[C]** | A consistent left action repairs the source's printed multiplication convention. The n=2 endpoint of Corollary 3.6 is proved separately. That source quantifies prime p; the replacement also holds for integer p≥2. |
| **[L], [V]** | Five general Lean declarations check the algebraic core and its finite-period adapter. Independent GAP permutations check the declared samples and two negative controls. |

The full group, geometric identification and universal presentation theorem
remain written proofs; they are not completely formalized in Lean.
See the [formal scope](research/case_study/formal/BinaryDihedralDisplacements.scope.md).

This adds one recovered principal-source contract, bringing the total to
**21 of 161 indexed works**. It adds no conjecture answer: the separate
[negative answer to the higher-rank conjecture](LABEL_ELEVEN_OBSTRUCTION.md)
keeps its own evidence and credit. Nor is the positive existence theorem
claimed as new work.

The five-page application and twelve-page source use different layouts.
No matched compression ratio follows from those counts. A topic comparison
must also include its complete chosen umbrella once and every required
application argument, as specified in the [complexity protocol](TOPIC_COMPLEXITY.md).
