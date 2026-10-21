import Mathlib.LinearAlgebra.Span.Basic
import Mathlib.Tactic

/-! The nested spans used in the module proof, with no independence hypothesis.
This file does not identify a particular permutation orbit or generated group. -/
namespace PrefixSpans
variable {R V : Type*} [Semiring R] [AddCommMonoid V] [Module R V]

def prefixSpan (z : ℕ → V) (n : ℕ) : Submodule R V :=
  Submodule.span R (z '' Set.Iic n)

theorem monotone_prefix (z : ℕ → V) : Monotone (prefixSpan (R := R) z) := by
  intro m n h
  apply Submodule.span_mono
  exact Set.image_mono (Set.Iic_subset_Iic.mpr h)

theorem prefix_inf (z : ℕ → V) (m n : ℕ) :
    prefixSpan (R := R) z m ⊓ prefixSpan (R := R) z n = prefixSpan z (min m n) := by
  rcases le_total m n with h | h
  · rw [min_eq_left h, inf_eq_left.mpr (monotone_prefix z h)]
  · rw [min_eq_right h, inf_eq_right.mpr (monotone_prefix z h)]

def markedPrefix (z : ℕ → V) (active : Bool) (n : ℕ) : Submodule R V :=
  if active then prefixSpan z n else ⊥

theorem markedPrefix_inf (z : ℕ → V) (a b : Bool) (m n : ℕ) :
    markedPrefix (R := R) z a m ⊓ markedPrefix z b n =
      markedPrefix z (a && b) (min m n) := by
  cases a <;> cases b <;> simp [markedPrefix, prefix_inf]

end PrefixSpans
#print axioms PrefixSpans.monotone_prefix
#print axioms PrefixSpans.prefix_inf
#print axioms PrefixSpans.markedPrefix_inf
