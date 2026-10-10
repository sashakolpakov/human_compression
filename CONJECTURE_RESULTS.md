# Answers to source questions

Question solving has its own record, separate from compression of known
published results. The current catalogue contains **twelve entries: eleven
recorded complete answers under their stated hypotheses and one answer to
an explicit interpretation of an ambiguously worded question**. Completeness
here concerns question coverage; Lean coverage and historical priority are
separate matters. This is an inventory of existing proofs and evidence, not a
new mathematical review of every entry. Historical priority has not been
verified for any of them.

| Source question | Recorded conclusion | Qualification |
|---|---|---|
| L043, Conjecture 6.1 | The specified field expression is a nonzero square for all stated odd primes and odd extension degrees greater than one. | [Complete arithmetic proof and detailed independent review](PRIMITIVE_SQUARES.md); six Lean declarations verify the polynomial steps, not the whole theorem. The exact bound source is the June 2016 author edition. |
| L043, Conjecture 6.2 | For the stated coprime odd degrees, the two middle parabolics intersect in their common cyclic subgroup. | Lean covers field and entrywise intersection components; the source matrix and geometric applications remain written. |
| L025, Conjecture 3.2 | The source Suzuki graphs have girth five and exactly q−1 pentagons through each edge. | Dedicated mathematical review; Lean verifies the matrix membership component. |
| L092, Conjecture 1 | The specified unital geometry has the asserted firmness, connectivity and flag transitivity. | Internal reviews are cited; this inventory did not locate a separate detailed mathematical review. Lean covers a connectivity lemma. |
| L102, §5.1.2 | The stated affine semilinear case forces a Desarguesian spread and gives the specified existence and uniqueness conclusion. | Both local primitivity assumptions are essential to the stated answer; written proof and dedicated review of the descent argument. |
| L007, §7 | The omitted even-exponent cases have non-tight chiral polyhedra of the required orders. | Written construction and dedicated review; Lean verifies conditional transfer. |
| L052, Problem 9.3 | The requested counterexample cannot occur for the standard parabolic coset construction. | The standard construction is part of the scope; Lean verifies orbit propagation. |
| L052, Problem 9.4 | A rank-three standard parabolic coset system is residually connected, precluding the requested simultaneous failure. | Dedicated written review; the complete result is not formalized. |
| L003, Problem 9.2 | Finite examples exist for every specified parameter s≥2; the exact universal groups are infinite for every s≥6. | [Source wording and both answers](TOROIDAL_QUESTION.md). Finite-existence is affirmative; universal finiteness is false. Lean proves infinitude of the exact presentations, with geometric identification remaining written. Full universal-group structure and priority remain unverified. |
| Cunningham–Pellicer, Problem 5; N016, §4 | Every abstract polytope of finite rank has a minimal regular polytopal cover; it is unique exactly when its distinguished monodromy group is a string C-group. | [Complete general proof and independent review](MINIMAL_REGULAR_COVERS.md). Covers may be infinite. Five new and six retained Lean declarations verify algebraic steps; the geometry and full theorem remain written. The [surface theorem](INFINITE_MINIMAL_COVERS.md) proves infinitely many finite covers in four families; the [square-torus application](SQUARE_TORUS_COVERS.md) adds every odd square-torus pyramid. The general finite version remains unresolved. |
| F014, Conjecture 3.7, arXiv v1 | **False at label 11 in every rank d≥5.** The universal rank-five presentation and a signed intersection witness exclude every quotient retaining exact adjacent order. | [Full proof and independent review](LABEL_ELEVEN_OBSTRUCTION.md). Nine general Lean declarations and [kernel-checked coset bounds through rank three](COSET_CERTIFICATES.md), alongside the separate larger certificates; no complete Lean proof. Published 2026 wording and historical priority are unverified. |
| L021, final conjecture of §5, May 2023 author edition | All four infinite rank-four PGL₂ families exist: the other end is S₄, A₅, PSL₂(p), or PGL₂(p), with explicit prime progressions. | [Complete proof and independent review](PGL_MANIPLEX_FAMILIES.md). Eleven Lean declarations verify actual matrix and unipotent algebra; the whole theorem remains written. A bounded later-literature search found no solution, but historical priority is unverified. |

The [detailed catalogue](research/case_study/phase124_question_results.md)
and [structured ledger](research/case_study/phase124_question_results.json)
give exact parameter ranges, original authors and source statements,
earlier published results used, proof files, review records, computational
evidence and the missing Lean arguments. The
[five-family cover page](COVER_FIVE_FAMILIES.md),
[surface construction](INFINITE_MINIMAL_COVERS.md) and
[square-torus application](SQUARE_TORUS_COVERS.md) distinguish the finite
family results and their successive extensions.

The original ten-entry catalogue remains frozen. The
[F014 admission](research/case_study/phase131_equal_label_admission.json)
and [independent review](research/case_study/phase131_equal_label_root_review.md)
added the eleventh entry as a partial answer. The
[new negative answer](LABEL_ELEVEN_OBSTRUCTION.md) supersedes its unresolved
status for the exact preprint conjecture; the frozen earlier positive
results retain their scope. The [general minimal-cover theorem](MINIMAL_REGULAR_COVERS.md)
also supersedes its earlier family-only status, without creating a new
question entry. A broader reconciliation of older recorded claims is in progress.

The [label-eight extension](research/case_study/phase168_label_eight_review.md)
expands that same F014 entry, with a separate Lean certificate for its
finite rewrite lemma. Later Lean proofs establish
[bounds on the table in every rank](research/case_study/phase174_label_eight_scope.md)
and [termination in every rank](research/case_study/phase172_termination_scope.md).
They do not establish confluence or formalize the resulting group theorem.
These developments and the later counterexample concern the same entry;
they do not create another entry in the conjecture count or establish
historical priority.

No complete geometric answer in this table is formalized in full.
Infinitude of the exact presented groups in the toroidal entry is a
complete Lean theorem; their interpretation as the source geometry is a
separate written argument. Mathematical review, finite computation,
formal proof and evidence about current openness are recorded separately.

The wider census of all 161 indexed works remains in progress. It must
also include questions already answered in later literature and papers
whose full texts remain unavailable. No new compression factor is assigned
by this catalogue.

The [publication record](provenance/phase90_review.md) distinguishes the
frozen private evidence hashes from five existing public versions with
documented navigation, path or documentation changes.

The census also records questions answered by later authors. In particular,
[L079 Conjecture 11](research/case_study/phase240_L079_status.md) was answered
by Connor, De Saedeleer and Leemans in 2015. It is not a new solution by
this project and is not added to the twelve repository-result entries.

The [four-family admission](research/case_study/phase262_L021_question_overlay.json)
adds the twelfth entry. Its complete affirmative answer, sources and
independent review are [recorded separately](PGL_MANIPLEX_FAMILIES.md).
It does not add a recovered historical principal contract or a ratio.

The [reviewed locally faithful criterion](LOCALLY_FAITHFUL_COVERS.md) adds
a general abelian existence test, a conditional multiplicity theorem and
a complete Tomotope classification within that class. The general finite
multiplicity question remains open, and the question count is unchanged.
