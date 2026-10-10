# Scope of CosetUpperCertificate.lean

The thirteen selected declarations establish soundness of an inductive coset-deduction system and executable trace checker, surjectivity onto actual cosets from complete proved transitions, finite-index bounds in the actual presented group, and the cardinality bound from a finite facet. The group and subgroup are not assumed finite in the index theorem; finiteness of the coset space is a conclusion.

Tree edges require literal representative-word identities. Relator deductions require membership in the stated relator set and previously proved paths. The universal group is Mathlib's quotient of the free group by the normal closure of generator squares and the supplied relators. A proposed finite action is not an upper-bound premise.

The file provides general theorems. Concrete certificates live in the two companion files. The frozen C++ scanner is not itself formalized or identified with this checker. The [independent review](../phase226_coset_review.md) examines these interfaces. The [fresh public report](../phase225_public_replay/report.json) and [compiler record](CosetUpperCertificate.check.json) bind all selected standard-axiom reports. Cached dependencies, the compiler and Lean's kernel remain trusted execution components.
