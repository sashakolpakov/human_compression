# Supported-kernel construction: admitted formal scope

The complete source [SupportedKernelGeneration.lean](SupportedKernelGeneration.lean)
has an [independent statement and proof review](../phase133_supported_kernel_review.md).
It formalizes the structural part of U.SK in
[Marked groups, kernels and intersections](../phase123_umbrella_manuscript_v2.md).

The conclusion includes generation of the full simultaneous fiber product,
both directions of the kernel profile for every generated parabolic, and
the full marked intersection property. The profile is proved from local
generation, compatibility, base fixation, distinct supports and proper
parabolic injectivity. It is not assumed. Kernels may be nonabelian and
groups may be infinite.

The exact hypotheses and translation from the written theorem are listed
in the unchanged [author scope](../phase129_supported_kernel_scope.md).
Its pending-review label records the author checkpoint; the independent
root review above supplies the subsequent admission at this stated scope.

The finite order formula, the four separate U.SK corollaries, application
bindings and geometric conclusions are not part of this module. No complete
formalization of U, Module A or a source paper follows. This adds no new
conjecture-resolution or historical-priority claim.

The local dependencies `CoordinateKernels` and `LiftCertificate` were
recompiled. All ten new printed declarations use only the standard axioms
`propext`, `Classical.choice` and `Quot.sound`. The installed compiler and
compiled pinned external dependencies remain trusted; they were not rebuilt
in full. The [saved report](SupportedKernelGeneration.check.json) records
the fresh public-run compilation.
