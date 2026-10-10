# Umbrella theory U: Marked groups, kernels and intersections

Read the [complete manuscript](research/case_study/phase123_umbrella_manuscript_v2.md).
This is the second author checkpoint, containing 28 statements and proofs.
It is the shared mathematical source for the application modules; those
papers cite its theorems and prove their application hypotheses.

The principal construction assembles local extensions over sets of
generators. Injectivity on every proper local parabolic allows an
induction to isolate each kernel, even when the supports overlap or are
nested and the kernels are nonabelian. This proves generation of the
whole compatible group and computes every parabolic kernel. The resulting
intersection property, deletion maps and factorization statements serve
several constructions in [Module A](MODULE_A.md).

Other sections treat quotient intersections, finite nilpotent quotients
and invariant subgroup ladders, comparison of marked quotients, coset
geometries, faithful actions, orbit decompositions, relative generation,
Frattini coordinates and amalgamated free products. Classical inputs are
identified explicitly. A fiber-product construction and an amalgamated
free product are distinct constructions with distinct hypotheses.

The [attribution and application ledger](research/case_study/phase123_umbrella_provenance_v2.md)
identifies reused arguments, reorganizations, new steps in this project,
retained mathematics and current Lean coverage. The
[exact contracts](research/case_study/phase123_umbrella_v2_contracts.json)
bind each complete statement and proof. Historical novelty has not been
established.

Root has read the complete U and A proofs. The
[review record](research/case_study/phase127_modular_root_review.md) states
what was checked and what remains. Full formalization, final source
admission and matched length measurement remain incomplete. The earlier
U checkpoint is preserved only for reproducible edit accounting.

The structural part of U.SK now has a
[Lean certificate](research/case_study/formal/SupportedKernelGeneration.lean):
it proves generation, every parabolic kernel profile and the full
intersection property from the actual local hypotheses. The
[independent review](research/case_study/phase133_supported_kernel_review.md)
checks its correspondence to the written argument. The separately reviewed
[consequences certificate](research/case_study/formal/SupportedKernelConsequences.scope.md)
now proves the order formula, local recognition, separator factorization
and lower-central consequence. A
[typed-Helly certificate](research/case_study/formal/SupportedKernelHelly.scope.md)
proves both the general marked transfer and its actual supported-kernel
application. Boolean deletions, full geometric recognition and source
application bindings remain separate formal tasks.

A [reviewed extension](MODULE_A_HYPERTOPES.md) proves typed-coset Helly
transfer when every parabolic kernel is a product of full coordinate
factors. Its geometric corollary requires involutory local markers.
The corrected proof is separate from the frozen U draft pending integration.
