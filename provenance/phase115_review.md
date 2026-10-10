# Admission of the label-eleven counterexample

10 October 2026. The complete [matrix and quotient manuscript](../research/case_study/phase212_n11_obstruction.md)
and [universal-presentation manuscript](../research/case_study/phase214_universal_bounds.md)
are admitted together, following the frozen
[independent review](../research/case_study/phase215_review.md).

The accepted conclusion is that Li–Zhang's arXiv v1 Conjecture 3.7 is
false: label 11 is impossible in every rank d≥5 with all its additional
relations. The proof identifies the universal rank-five group, exhibits
a signed intersection witness, and excludes every quotient retaining
the required adjacent order. A failed natural representation alone would
not have sufficed.

The root read both complete written proofs, the complete C++ upper-bound
checker, the exact matrix and independent binary-field programs, all nine
Lean declarations, and the independent review. The reviewer separately
checked the primary PDF, including its displayed ranges, and reran both
final frozen packages. It also checked arbitrary relabelling and rejected
omitted relators, a corrupted edge, and a valid one-point quotient action
that does not prove an upper bound.

## Fresh public execution

The two components were copied byte for byte, followed by all 54 exported
review artifacts. Fresh runs from the public directory passed:

- [Upper certificate](../research/case_study/phase217_public_upper/report.json):
  the three finite index bounds and both author rejection controls.
- [Matrix and Lean certificate](../research/case_study/phase217_public_matrices/report.json):
  signed memberships, exact orders, simplicity, independent small-field
  arithmetic, nine standard-axiom declarations and five rejection controls.
- [Combined public wrapper](../research/case_study/phase217_combined_replay/report.json):
  the unchanged components and 40 bound artifacts, with a fresh execution
  of both checks.

The wrapper also passes [three interface controls](../research/case_study/phase217_wrapper_controls.json).
It rejects the original output path if it is a dangling symlink, addressing
the nonmathematical issue recorded for the frozen phase212 driver. Existing
output and altered manifests are rejected. Frozen author files were preserved.

## Scope and accounting

The three frozen component manifests are
[phase212](../research/case_study/phase212_export.json),
[phase214](../research/case_study/phase214_manifest.json), and
[phase215](../research/case_study/phase215_manifest.json).
Their exact publication copies and the new root files are recorded in
[the export manifest](../research/case_study/phase217_export.json).

GAP remains trusted for large finite-group orders, simplicity and signed
membership. The coset upper bound has a separate portable C++ deduction
checker and written soundness proof. The compiler and cached pinned
dependencies remain in the Lean trust boundary. The canonical
[SimpleQuotientObstruction.lean](../research/case_study/formal/SimpleQuotientObstruction.lean)
is identical to the reviewed author source; its nine declarations do not
formalize the concrete groups or the entire counterexample. It is the
76th scoped canonical Lean file.

The [question update](../research/case_study/phase217_question_update.json)
moves the existing F014 entry from partial positive cases to a complete
negative answer for the specified version. There are still eleven question
entries: nine complete answers, one ambiguous formulation, and one broader
question with family results. The 20 principal source records and 43
records with recovered results do not increase. No source-compression
credit or numerical factor follows from this conjecture result.

The compressed certificate tables occupy approximately 14 MB and are
essential parts of the computational proof. They cannot be omitted from
a future account of its proof resources. No matched source/replacement
measurement is supplied here.

The journal edition was published in 2026, but the complete published
conjecture wording has not been obtained. No claim of continuing openness,
historical priority, or an unchanged journal formulation is made. The
mathematical conclusion concerns the precise primary preprint statement.
