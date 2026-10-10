import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.GroupTheory.GroupAction.Basic

namespace HumanCompression.DeterminantFibers

variable {K n : Type*} [Field K] [Fintype n] [DecidableEq n]

/-- Two invertible row frames of equal determinant differ by one unique
right multiplication of determinant one. This is an actual matrix statement. -/
theorem determinant_fiber_torsor (A B : Matrix n n K)
    (hA : IsUnit A.det) (hdet : A.det = B.det) :
    ∃! C : Matrix n n K, C.det = 1 ∧ A * C = B := by
  refine ⟨A⁻¹ * B, ⟨?_, A.mul_nonsing_inv_cancel_left B hA⟩, ?_⟩
  · rw [Matrix.det_mul, ← hdet]
    exact A.det_nonsing_inv_mul_det hA
  · intro C hC
    calc
      C = A⁻¹ * (A * C) := (A.nonsing_inv_mul_cancel_left C hA).symm
      _ = A⁻¹ * B := by rw [hC.2]

/-- Determinants of row frames under the literal semilinear action. -/
theorem semilinear_determinant (σ : K ≃+* K) (A M : Matrix n n K) :
    (A.map σ * M).det = σ A.det * M.det := by
  have hm : σ A.det = (A.map σ).det := σ.map_det A
  rw [Matrix.det_mul, ← hm]

/-- A semilinear move followed by determinant-one transport reaches exactly
its determinant fiber. This holds for every square matrix size. -/
theorem semilinear_fiber_transport (σ : K ≃+* K) (A M B : Matrix n n K)
    (hC : IsUnit (A.map σ * M).det) :
    (∃ C : Matrix n n K, C.det = 1 ∧ (A.map σ * M) * C = B) ↔
      B.det = σ A.det * M.det := by
  constructor
  · rintro ⟨C, hCdet, hCB⟩
    rw [← hCB, Matrix.det_mul, hCdet, mul_one, semilinear_determinant]
  · intro hdet
    have heq : (A.map σ * M).det = B.det := by
      rw [semilinear_determinant, ← hdet]
    obtain ⟨C, hCprop, _⟩ := determinant_fiber_torsor (A.map σ * M) B hC heq
    exact ⟨C, hCprop⟩

/-- Saturating each fiber reduces an actual subgroup orbit to its image under
an arbitrary signature map. No faithfulness or freeness is silently assumed. -/
theorem orbit_saturation {G X Y : Type*} [Group G] [MulAction G X]
    (H : Subgroup G) (f : X → Y)
    (hfiber : ∀ u v, f u = f v → ∃ h ∈ H, h • u = v) (x y : X) :
    (∃ h ∈ H, h • x = y) ↔ (∃ h ∈ H, f (h • x) = f y) := by
  constructor
  · rintro ⟨h, hh, hxy⟩
    exact ⟨h, hh, congrArg f hxy⟩
  · rintro ⟨h, hh, hxy⟩
    obtain ⟨k, hk, hky⟩ := hfiber (h • x) y hxy
    refine ⟨k * h, H.mul_mem hk hh, ?_⟩
    simpa only [mul_smul] using hky

#print axioms determinant_fiber_torsor
#print axioms semilinear_determinant
#print axioms semilinear_fiber_transport
#print axioms orbit_saturation
end HumanCompression.DeterminantFibers
