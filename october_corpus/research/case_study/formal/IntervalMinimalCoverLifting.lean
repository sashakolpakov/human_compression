import Mathlib.Order.Minimal
import Mathlib.Order.Hom.Basic

/-!
The order argument in interval lifting.  Larger kernels correspond to smaller
covers.  The extension theorem, restriction preserving the intersection
property, finite descent and the group/polytope correspondence are written
inputs; this file does not assert them under renamed predicates.
-/
namespace MathCompression.IntervalMinimalCoverLifting

variable {A B : Type*} [PartialOrder A] [PartialOrder B]

/-- An increasing restriction of kernels cannot enlarge a maximal admissible
local kernel while remaining locally admissible. -/
theorem restriction_retains_maximal
    (f : A →o B) (Q : B → Prop) {r m : A} {q : B}
    (hq : Maximal Q q) (hrq : f r = q) (hrm : r ≤ m)
    (hm : Q (f m)) : f m = q := by
  have hle : q ≤ f m := hrq ▸ f.monotone hrm
  exact le_antisymm (hq.2 hm hle) hle

/-- Local maximal kernels lift to global maximal kernels when exact extension,
descent, and admissible restriction are supplied explicitly. -/
theorem exists_maximal_with_prescribed_restriction
    (f : A →o B) (P : A → Prop) (Q : B → Prop)
    (hextend : ∀ q, Maximal Q q → ∃ r, P r ∧ f r = q)
    (hdescend : ∀ r, P r → ∃ m, r ≤ m ∧ Maximal P m)
    (hrestrict : ∀ m, P m → Q (f m))
    {q : B} (hq : Maximal Q q) : ∃ m, Maximal P m ∧ f m = q := by
  obtain ⟨r, hr, hrq⟩ := hextend q hq
  obtain ⟨m, hrm, hm⟩ := hdescend r hr
  exact ⟨m, hm, restriction_retains_maximal f Q hq hrq hrm
    (hrestrict m hm.1)⟩

omit [PartialOrder A] [PartialOrder B] in
/-- Different prescribed restrictions force different global kernels. -/
theorem distinct_of_distinct_restrictions
    (f : A → B) {m₁ m₂ : A} {q₁ q₂ : B}
    (h₁ : f m₁ = q₁) (h₂ : f m₂ = q₂) (hneq : q₁ ≠ q₂) : m₁ ≠ m₂ := by
  intro heq
  apply hneq
  exact h₁.symm.trans ((congrArg f heq).trans h₂)

#print axioms restriction_retains_maximal
#print axioms exists_maximal_with_prescribed_restriction
#print axioms distinct_of_distinct_restrictions

end MathCompression.IntervalMinimalCoverLifting
