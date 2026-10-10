# Supported-kernel consequences: admitted formal scope

[SupportedKernelConsequences.lean](SupportedKernelConsequences.lean) has a complete
[independent statement and proof review](../phase135_supported_kernel_consequences_review.md).

Order, local recognition, separator factorization and the lower-central
consequence follow from the actual construction hypotheses. The final
statements discharge the helper kernel-profile premises using the proved
construction. Infinite Nat.card values use Lean's zero convention; the
finite specialization is the ordinary group-order formula. Boolean
deletions, typed Helly and source applications are outside this module.

The unchanged [author scope](../phase129_supported_kernel_consequences_scope.md)
lists every hypothesis, theorem and retained input. Its pending-review label
records an earlier checkpoint; the root review supplies the subsequent
admission. The [public compilation](SupportedKernelConsequences.check.json) records a fresh
pinned compiler run. The compiler and cached dependencies are trusted;
two missing Mathlib modules were rebuilt in a private overlay.

Only standard axioms are reported. This component does not constitute a
complete formalization of U, Module A or an open conjecture, and adds no
known-source compression credit.
