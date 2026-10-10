# Complete coprime fiber-product generation in Lean

10 October 2026. The new [written theorem](../research/case_study/phase115_coprime_pullback_theorem.md)
and [Lean module](../research/case_study/formal/CoprimePullback.lean) prove
that a compatible subgroup with surjective coordinate projections is the
whole fiber product when the two kernel cardinalities are coprime. The
paired-generator corollary proves the generation hypotheses explicitly.
The kernels need not be abelian. This is classical group theory, with no
historical-priority claim.

The [independent review](../research/case_study/phase126_coprime_pullback_review.md)
read the exact proof, declarations, wrapper and the relevant mathlib power
lemmas. Its [frozen manifest](../research/case_study/phase126_coprime_pullback_manifest.json)
binds six review files and four author inputs. Its SHA-256 is
`461261ef721157963ffa4645f548d88e775f08e8ff68d9bc7f106efc47f535e9`.
All ten input/export bindings were verified before copying three author
files, six review files and the manifest; the existing dependency manifest
already matched exactly.

Root then compiled the exported source with the public generic runner.
The [fresh report](../research/case_study/phase128_coprime_pullback_public_build.json)
records successful compilation of all three substantive declarations in
6.57 seconds. Each uses only `propext`, `Classical.choice` and `Quot.sound`.
The report also supplies the saved `CoprimePullback.check.json`. The Lake
roots and public runner selection now include this module.

The [fresh public controls](../research/case_study/phase128_coprime_pullback_public_controls.json)
pass six wrong-input/no-clobber cases, two independent positive examples
and three counterexamples to weakened hypotheses. They check the exact
published wrapper, including a dangling output symlink. These finite
examples are scope checks, not substitutes for the general Lean proof.

There are now 44 scoped Lean certificates: 43 without native-evaluation
axioms and the earlier transfer certificate with four explicitly recorded
native-evaluation axioms. The usual compiler and compiled-dependency trust
boundary remains explicit.

The [scope note](../research/case_study/formal/CoprimePullback.scope.md)
explains the slight extension from finite kernel orders in the written
theorem to `Nat.card` in Lean. This addition does not prove a new source
conjecture, certify a complete cover construction, or finish U or A's
formalization. No compression factor changes.
