# Locally faithful quotient intersections

Three declarations are freshly compiled under Lean 4.32.2 and the pinned
Mathlib dependencies. Their axiom reports contain only `propext`,
`Classical.choice` and `Quot.sound`.

- `quotient_intersection_iff` identifies intersection of actual subgroup
  images with separation of every lift discrepancy outside the shared image.
  It assumes injectivity of the base homomorphism on the first end.
- `quotient_faithful_on_end` shows that faithfulness over the base persists
  in an intermediate quotient over that base.
- `quotient_kernel_containment` gives containment of the first kernel in
  the composite kernel.

These are generic group statements. They do not assume or formalize
Bass–Serre theory, the identification of the geometric kernel, homology,
the integer matrix evaluation, GAP computations, or the general finite
minimal-cover conjecture. The written application supplies the relevant
hypotheses separately. The driver's actual C₂ counterexample demonstrates
that the injectivity premise cannot be omitted from the first equivalence.

The [independent review](../phase255_locally_faithful_review.md) and
[fresh public replay](../phase260_public_replay/report.json) state the
remaining proof and computational boundaries.
