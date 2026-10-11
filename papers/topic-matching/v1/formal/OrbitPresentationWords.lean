import Mathlib.Algebra.Group.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Tactic

/-!
Actual word equalities used in the complete parity presentation, and the
infinite-order matrix block for an omitted Coxeter pair.  No declaration
asserts completeness of a presentation or formalizes the retained extension
and geometric halving theorems.  The real Coxeter representation remains written.
-/
namespace OrbitPresentationWords

variable {G : Type*} [Group G]

theorem involution_inverse (a : G) (ha : a * a = 1) : a⁻¹ = a := by
  exact inv_eq_of_mul_eq_one_right ha

theorem orbital_rewrite (a w : G) (ha : a * a = 1) :
    a * w⁻¹ * a * w = (a * w * a)⁻¹ * w := by
  rw [mul_inv_rev, mul_inv_rev, involution_inverse a ha]
  simp only [mul_assoc]

theorem orbital_conjugate_inverse (a w : G) (ha : a * a = 1) :
    a * (a * w⁻¹ * a * w) * a = (a * w⁻¹ * a * w)⁻¹ := by
  have hi := involution_inverse a ha
  simp only [mul_inv_rev, hi, inv_inv]
  calc
    a * (a * w⁻¹ * a * w) * a = (a * a) * (w⁻¹ * a * w * a) := by group
    _ = w⁻¹ * (a * (w * a)) := by rw [ha, one_mul]; simp only [mul_assoc]

theorem even_word_rewrite (a w : G) :
    (a * w)^2 = (a * w * a) * w := by simp only [pow_two, mul_assoc]

theorem even_word_conjugate (a w : G) (ha : a * a = 1) :
    a * ((a * w * a) * w) * a = w * ((a * w * a) * w) * w⁻¹ := by
  have hi := involution_inverse a ha
  calc
    a * ((a * w * a) * w) * a = (a * a) * (w * a * w * a) := by group
    _ = w * a * w * a := by rw [ha, one_mul]
    _ = w * ((a * w * a) * w) * w⁻¹ := by group

def omittedBlock : Matrix (Fin 2) (Fin 2) ℚ := !![3, -2; 2, -1]

theorem omitted_block_power (n : ℕ) :
    omittedBlock ^ n = !![2 * (n : ℚ) + 1, -2 * (n : ℚ);
      2 * (n : ℚ), 1 - 2 * (n : ℚ)] := by
  induction n with
  | zero => ext i j; fin_cases i <;> fin_cases j <;> norm_num [omittedBlock]
  | succ n ih =>
    rw [pow_succ, ih]
    ext i j; fin_cases i <;> fin_cases j <;>
      simp [omittedBlock, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem omitted_block_no_positive_power (n : ℕ) (hn : 0 < n) :
    omittedBlock ^ n ≠ 1 := by
  intro h
  have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℚ => M 1 0) h
  rw [omitted_block_power] at he
  norm_num at he
  exact (Nat.ne_of_gt hn) (by exact_mod_cast he)

#print axioms involution_inverse
#print axioms orbital_rewrite
#print axioms orbital_conjugate_inverse
#print axioms even_word_rewrite
#print axioms even_word_conjugate
#print axioms omitted_block_power
#print axioms omitted_block_no_positive_power
end OrbitPresentationWords
