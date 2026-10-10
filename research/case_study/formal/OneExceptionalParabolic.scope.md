# Scope of OneExceptionalParabolic.lean

This new module imports the frozen `ParabolicQuotientTransport` module and
weakens injectivity from every maximal parabolic to every maximal parabolic
except one specified type. It does not alter the earlier module.

Four exported theorems are kernel-checked:

- `typed_helly_transport` lifts arbitrary typed right-coset Helly when exact
  pair-intersection images hold and all but one family subgroup are injective.
  A family with a nonexceptional type uses that subgroup as an anchor; a family
  contained in the exceptional singleton is settled directly.
- `exceptional_subset` says that a proper subset omitting no nonexceptional
  type equals the complement of the exceptional singleton.
- `marked_intersection_transport` lifts the full subgroup intersection property
  from exact images for a monotone subset-indexed family with full subset top.
  It treats full subsets, injectively protected subsets, and the sole remaining
  equal-subset case separately.
- `marked_quotient_transport` combines that IP theorem with typed Helly for the
  maximal parabolics. Image-meet equalities for the latter are derived from IP.

All type sets, selected families and groups may be infinite. The homomorphism
need not be onto the ambient target group, since every target subgroup in the
statements is its exact image. There is no finite, central-kernel, involution,
or geometric assumption hidden in these statements. The module formalizes no
particular finite group, presentation, toroidal residue or hypertope family.

The saved successful Lean 4.32.2 report uses the same package checkout recorded
by the earlier pinned phase32 build. Every exported result reports only
`propext`, `Classical.choice`, and `Quot.sound`; no unproved placeholder or native
evaluation axiom occurs. An initial local compile failed because `protected`
was used as a local identifier; the compiled source uses `hprotected`. No
mathematical assumption or proof was changed to address that parser error.

Reproduction uses the ordinary pinned verification runner, with the frozen
`ParabolicQuotientTransport.lean` compiled first. No additional mathlib overlay
is required. The portable public runner may record a separate fresh compile
without replacing the historical private report.
