import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.ZMod.Basic

/-! Exact algebra for the constant quadruple in the four-family theorem.
The field-subgroup classification and the passage to regular maniplexes
are written arguments, not conclusions of this file. -/
namespace HumanCompression.FourProjectiveMarks

abbrev Mat2 (F : Type*) := Matrix (Fin 2) (Fin 2) F

section Ring
variable {F : Type*} [CommRing F]

def r0 : Mat2 F := !![0, 1; 1, 0]
def r1 : Mat2 F := !![1, 0; 1, -1]
def r2 : Mat2 F := !![-1, 0; 0, 1]
def r3 : Mat2 F := !![1, -2; 2, -1]
def lower (t : F) : Mat2 F := !![1, 0; t, 1]

theorem square_relations :
    (r0 : Mat2 F)^2 = 1 ∧ r1^2 = (1 : Mat2 F) ∧
    r2^2 = (1 : Mat2 F) ∧ r3^2 = (-3 : F) • (1 : Mat2 F) := by
  repeat' constructor
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [r0, r1, r2, r3, pow_two, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem distant_anticommutation :
    (r0 : Mat2 F) * r2 = -(r2 * r0) ∧
    (r0 : Mat2 F) * r3 = -(r3 * r0) ∧
    (r1 : Mat2 F) * r3 = -(r3 * r1) := by
  repeat' constructor
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [r0, r1, r2, r3, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem determinants :
    (r0 : Mat2 F).det = -1 ∧ (r1 : Mat2 F).det = -1 ∧
    (r2 : Mat2 F).det = -1 ∧ (r3 : Mat2 F).det = 3 := by
  simp [r0, r1, r2, r3, Matrix.det_fin_two]
  ring

theorem adjacent_products :
    (r1 : Mat2 F) * r2 = -lower (1 : F) ∧
    ((r0 : Mat2 F) * r1)^3 = -(1 : Mat2 F) := by
  constructor
  all_goals
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [r0, r1, r2, lower, pow_succ, Matrix.mul_apply, Fin.sum_univ_two]

theorem lower_mul (x y : F) : lower x * lower y = lower (x+y) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [lower, Matrix.mul_apply, Fin.sum_univ_two]

theorem lower_one_pow (n : ℕ) : (lower (1 : F))^n = lower (n : F) := by
  induction n with
  | zero => ext i j; fin_cases i <;> fin_cases j <;> simp [lower]
  | succ n ih => rw [pow_succ, ih, lower_mul]; simp

theorem lower_scalar_iff (t : F) :
    (∃ c : F, lower t = c • (1 : Mat2 F)) ↔ t = 0 := by
  constructor
  · rintro ⟨c, h⟩
    simpa [lower] using congrArg (fun M : Mat2 F => M 1 0) h
  · intro h
    refine ⟨1, ?_⟩
    ext i j
    fin_cases i <;> fin_cases j <;> simp [lower, h]

end Ring

section Field
variable {F : Type*} [Field F]

theorem nonscalar_marks (h2 : (2 : F) ≠ 0) :
    (∀ c : F, r0 ≠ c • (1 : Mat2 F)) ∧
    (∀ c : F, r1 ≠ c • (1 : Mat2 F)) ∧
    (∀ c : F, r2 ≠ c • (1 : Mat2 F)) ∧
    (∀ c : F, r3 ≠ c • (1 : Mat2 F)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 0 1) h
    simp [r0] at hh
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 1 0) h
    simp [r1] at hh
  · intro c h
    have h00 := congrArg (fun M : Mat2 F => M 0 0) h
    have h11 := congrArg (fun M : Mat2 F => M 1 1) h
    simp [r2] at h00 h11
    apply h2
    linear_combination -h00 + h11
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 1 0) h
    exact h2 (by simpa [r3] using hh)

theorem pairwise_not_proportional (h2 : (2 : F) ≠ 0) :
    (∀ c : F, r1 ≠ c • (r0 : Mat2 F)) ∧
    (∀ c : F, r2 ≠ c • (r0 : Mat2 F)) ∧
    (∀ c : F, r3 ≠ c • (r0 : Mat2 F)) ∧
    (∀ c : F, r1 ≠ c • (r2 : Mat2 F)) ∧
    (∀ c : F, r3 ≠ c • (r1 : Mat2 F)) ∧
    (∀ c : F, r3 ≠ c • (r2 : Mat2 F)) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 0 0) h
    simp [r0, r1] at hh
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 0 0) h
    simp [r0, r2] at hh
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 0 0) h
    simp [r0, r3] at hh
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 1 0) h
    simp [r1, r2] at hh
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 0 1) h
    have hz : -(2 : F) = 0 := by simpa [r1, r3] using hh
    exact h2 (neg_eq_zero.mp hz)
  · intro c h
    have hh := congrArg (fun M : Mat2 F => M 1 0) h
    exact h2 (by simpa [r2, r3] using hh)

end Field

theorem lower_projective_period (p n : ℕ) :
    (∃ c : ZMod p, (lower (1 : ZMod p))^n = c • (1 : Mat2 (ZMod p))) ↔ p ∣ n := by
  rw [lower_one_pow, lower_scalar_iff, ZMod.natCast_eq_zero_iff]

theorem prime_field_lower_exhaustion (p : ℕ) [NeZero p] (t : ZMod p) :
    ∃ n : ℕ, n < p ∧ (lower (1 : ZMod p))^n = lower t := by
  refine ⟨t.val, t.val_lt, ?_⟩
  rw [lower_one_pow, ZMod.natCast_zmod_val]

#print axioms square_relations
#print axioms distant_anticommutation
#print axioms determinants
#print axioms adjacent_products
#print axioms lower_mul
#print axioms lower_one_pow
#print axioms lower_scalar_iff
#print axioms nonscalar_marks
#print axioms pairwise_not_proportional
#print axioms lower_projective_period
#print axioms prime_field_lower_exhaustion
end HumanCompression.FourProjectiveMarks
