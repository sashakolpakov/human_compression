# Scope of ParabolicQuotientTransport.lean

This module formalizes the algebraic quotient-transport step in the fixed-parameter L003 construction. It does not formalize its finite group, toroidal-map identifications or hypertope adapter.

`TypedCosetHelly P` means that every pairwise-intersecting family of right cosets, with at most one coset for each selected type, has a common point. Right-coset membership is written `x * g⁻¹ ∈ P i`. The definition quantifies over arbitrary subsets of an arbitrary type set; neither the groups nor the selected family must be finite.

The four kernel-checked results are:

- `same_right_coset_difference`: two elements in the same right coset have their quotient in its subgroup.
- `typed_helly_transport`: if a homomorphism is injective on every parabolic, maps their pair intersections to the exact intersections of their images, and the image family has typed Helly, then the original family has typed Helly. The empty selected family is treated explicitly.
- `marked_intersection_transport`: a monotone subgroup family indexed by generator subsets, with the full subset giving the whole group, inherits the full intersection property from its image if the map is injective on every maximal marked parabolic. A proper subset lies in a parabolic omitting one of its missing types. No finite-rank assumption is needed for this step.
- `marked_quotient_transport`: the combined subgroup-intersection and typed-Helly conclusion for the maximal parabolics of that family.

The homomorphism need not be globally surjective: the target parabolics are defined to be its exact subgroup images. The common point downstairs lifts because it belongs to one such coset. No centrality, finite kernel, involutory marking, or geometric regularity is assumed or concluded by these algebraic statements. The monotone marked-family and image-IP hypotheses remain explicit; the module does not infer them from names or from a finite computation.

The saved Lean 4.32.2 compile report is a successful execution of the unchanged private runner against the same pinned package checkout verified in `phase32_L003_formal_check.json`. The first theorem reports only `propext`; the other three report `propext`, `Classical.choice`, and `Quot.sound`. There are no unproved placeholders or native evaluation axioms. Root and a second agent separately read the complete statements/proofs without finding a gap; those reads are internal reviews, not external peer review.

Reproduction uses the project's pinned `formal/dependency_manifest.json` and ordinary Lean verification runner. This module imports only already compiled mathlib modules and requires no new dependency overlay. A separate fresh public compile may be recorded without replacing this historical report.
