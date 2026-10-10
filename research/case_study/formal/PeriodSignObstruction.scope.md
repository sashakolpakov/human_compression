# Formal scope: period-word sign obstruction

The canonical source is byte-identical to the frozen phase250 proof.
Its three declarations in `HumanCompression.PeriodSignObstruction` are:

- `literal_word_conjugacy`: the actual two source period words are conjugate inverses under the stated involution hypotheses.
- `equal_period_signs_collapse`: equal period signs, together with the explicit commutation hypothesis, force the additional rotation relation, for every natural parameter.
- `source_period_sign_obstruction`: specialization of that general argument to the literal words in arXiv:2001.02945v2, Lemma 4.5.

Fresh public compilation uses Lean 4.32.2 and the pinned clean dependency
source trees. Only standard axioms are reported; there is no native
evaluation axiom or proof placeholder. Cached dependency objects remain
trusted. The exact report is `PeriodSignObstruction.check.json`.

The positive affine constructions, abstract-kernel computations, full
classification, Burnside theorem, Lucchini theorem and catalogue
completeness are not formalized by these declarations. Their written and
computational scope is stated in the accepted phase254 review and the
phase259 admission. No additional question credit is attached to this
supporting formal component.
