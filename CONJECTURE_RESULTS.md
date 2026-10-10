# Answers to source questions

Question solving has its own record, separate from compression of known
published results. The current catalogue contains **eleven entries: eight
recorded answer claims under their precise scope, and three qualified
results**. This is an inventory of existing proofs and evidence, not a
fresh mathematical audit of every entry. None has completed historical
priority clearance.

| Source question | Recorded conclusion | Qualification |
|---|---|---|
| L043, Conjecture 6.1 | The specified field expression is a nonzero square for all stated odd primes and odd extension degrees greater than one. | No full Lean proof; a separate detailed arithmetic audit was not located in this inventory pass. |
| L043, Conjecture 6.2 | For the stated coprime odd degrees, the two middle parabolics intersect in their common cyclic subgroup. | Lean covers field and entrywise intersection components; the source matrix and geometric applications remain written. |
| L025, Conjecture 3.2 | The source Suzuki graphs have girth five and exactly q−1 pentagons through each edge. | Dedicated mathematical audit; Lean verifies the matrix membership component. |
| L092, Conjecture 1 | The specified unital geometry has the asserted firmness, connectivity and flag transitivity. | Inherited internal-review claims; a separate detailed mathematical audit was not located. Lean covers a connectivity lemma. |
| L102, §5.1.2 | The stated affine semilinear case forces a Desarguesian spread and gives the specified existence and uniqueness conclusion. | Both local primitivity assumptions are essential to the stated answer; written proof and dedicated descent audit. |
| L007, §7 | The omitted even-exponent cases have non-tight chiral polyhedra of the required orders. | Written construction and dedicated audit; Lean verifies conditional transfer. |
| L052, Problem 9.3 | The requested counterexample cannot occur for the standard parabolic coset construction. | The standard construction is part of the scope; Lean verifies orbit propagation. |
| L052, Problem 9.4 | A rank-three standard parabolic coset system is residually connected, precluding the requested simultaneous failure. | Dedicated written audit; the complete result is not formalized. |
| L003, Problem 9.2 | Finite examples exist for the specified toroidal family; the exact universal groups are infinite for all s≥6. | Answers a stated finite-existence interpretation, not every reading of the problem. Lean proves infinitude of the three exact presentations, with the geometric identification remaining written. |
| N016 / F005, minimal-cover questions | Each of the five specified chiral-facet families has at least two distinct minimal regular polytopal covers. | The general arbitrary-polytope conjecture remains unresolved. Complete written and computational arguments have scoped Lean components. |
| F014, Conjecture 3.7 | In every rank, finite examples satisfy all specified relations at labels 4 and n, 2n, 4n for n=3 or the stated powers-of-two ±1 families. | [Complete scope and proofs](EQUAL_LABEL_POLYTOPES.md). The all-label conjecture remains unresolved. Universal presentations are identified only at labels 3 and 4; no complete Lean proof. |

The [detailed catalogue](research/case_study/phase124_question_results.md)
and [structured ledger](research/case_study/phase124_question_results.json)
give exact parameter ranges, original authors and source statements,
retained published inputs, proof files, review records, computational
evidence and the missing Lean arguments. The
[five-family cover page](COVER_FIVE_FAMILIES.md) describes the latest
reviewed family result in more detail.

The original ten-entry catalogue remains frozen. The
[F014 admission](research/case_study/phase131_equal_label_admission.json)
and [independent review](research/case_study/phase131_equal_label_root_review.md)
add the eleventh entry, a partial question result with explicitly retained
theorems. A broader reconciliation of older recorded claims is in progress.

No entire source-level geometric answer in this table is formalized end
to end. Exact presented-group infinitude in the toroidal entry is a
complete Lean theorem; its interpretation as the source geometry is a
separate written argument. Mathematical review, finite computation,
formal proof and evidence about current openness are recorded separately.

The wider census of all 161 indexed works remains in progress. It must
also include questions already answered in later literature and papers
whose full texts remain unavailable. No new compression factor is assigned
by this catalogue.

The [publication record](provenance/phase90_review.md) distinguishes the
frozen private evidence hashes from five existing public versions with
documented navigation, path or documentation changes.
