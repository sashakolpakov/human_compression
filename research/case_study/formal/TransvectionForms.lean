import Mathlib.Data.Matrix.Basis

/-!
An elementary matrix certificate for the no-bilinear-form argument.
Exact invariance under the elementary transvections already forces the
form to vanish in dimension at least three, in every characteristic.
The projective-similarity multiplier reduction remains a written input.
-/

namespace MathCompression

open Matrix

variable {R : Type*} [Ring R]
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem form_entry_zero_of_transvection_invariance
    (B : Matrix ι ι R) (i j b : ι) (hbj : b ≠ j)
    (h : (1 + Matrix.single i j (1 : R))ᵀ * B *
      (1 + Matrix.single i j (1 : R)) = B) :
    B i b = 0 := by
  have he := congrArg (fun M : Matrix ι ι R => M j b) h
  have hh : B j b + B i b = B j b := by
    simpa only [transpose_add, transpose_one, transpose_single,
      add_mul, mul_add, one_mul, mul_one, Matrix.add_apply,
      mul_single_apply_of_ne _ _ _ _ _ hbj, single_mul_apply_same,
      one_mul, add_zero] using he
  exact add_left_cancel (hh.trans (add_zero _).symm)

theorem form_zero_of_transvection_invariance
    (third : ∀ i b : ι, ∃ j, j ≠ i ∧ j ≠ b)
    (B : Matrix ι ι R)
    (h : ∀ i j : ι, i ≠ j →
      (1 + Matrix.single i j (1 : R))ᵀ * B *
        (1 + Matrix.single i j (1 : R)) = B) : B = 0 := by
  ext i b
  obtain ⟨j, hji, hjb⟩ := third i b
  exact form_entry_zero_of_transvection_invariance B i j b hjb.symm
    (h i j hji.symm)

theorem form_four_zero_of_transvection_invariance
    (B : Matrix (Fin 4) (Fin 4) R)
    (h : ∀ i j : Fin 4, i ≠ j →
      (1 + Matrix.single i j (1 : R))ᵀ * B *
        (1 + Matrix.single i j (1 : R)) = B) : B = 0 := by
  apply form_zero_of_transvection_invariance (B := B) _ h
  decide

#print axioms form_entry_zero_of_transvection_invariance
#print axioms form_zero_of_transvection_invariance
#print axioms form_four_zero_of_transvection_invariance

end MathCompression
