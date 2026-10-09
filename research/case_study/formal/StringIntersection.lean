import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
Local intersection obstruction used in the written PSL4 rank-eight exclusion.
The displayed intersection hypothesis states that the two adjacent parabolics
intersect only in 1 and the middle involution. No representation classification
or rank bound is assumed or formalized here.
-/
namespace LeemansString

variable {G : Type*} [Group G]

theorem central_alternating_pair_forces_commutation
    (a b c : G) (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hbne : b ≠ 1) (hac : Commute a c) (hprod : Commute (a * c) b)
    (hip : ∀ x : G,
      x ∈ Subgroup.closure ({a, b} : Set G) →
      x ∈ Subgroup.closure ({b, c} : Set G) → x = 1 ∨ x = b) :
    Commute a b := by
  have hca : c * (a * c) = a := by
    calc
      c * (a * c) = (c * a) * c := by group
      _ = (a * c) * c := by rw [hac.eq]
      _ = a := by rw [mul_assoc, hc, mul_one]
  have haca : (a * c) * a = c := by
    calc
      (a * c) * a = a * (c * a) := by group
      _ = a * (a * c) := by rw [hac.eq]
      _ = c := by rw [← mul_assoc, ha, one_mul]
  have hconj : a * b * a = c * b * c := by
    calc
      a * b * a = (c * (a * c)) * b * a := by rw [hca]
      _ = c * ((a * c) * b) * a := by group
      _ = c * (b * (a * c)) * a := by rw [hprod.eq]
      _ = c * b * ((a * c) * a) := by group
      _ = c * b * c := by rw [haca]
  have hsq : (b * a) ^ 2 = (b * c) ^ 2 := by
    calc
      (b * a) ^ 2 = b * (a * b * a) := by simp only [pow_two, mul_assoc]
      _ = b * (c * b * c) := by rw [hconj]
      _ = (b * c) ^ 2 := by simp only [pow_two, mul_assoc]
  have hleft : (b * a) ^ 2 ∈ Subgroup.closure ({a, b} : Set G) := by
    apply Subgroup.pow_mem
    apply Subgroup.mul_mem
    · exact Subgroup.subset_closure (by simp)
    · exact Subgroup.subset_closure (by simp)
  have hright : (b * a) ^ 2 ∈ Subgroup.closure ({b, c} : Set G) := by
    rw [hsq]
    apply Subgroup.pow_mem
    apply Subgroup.mul_mem
    · exact Subgroup.subset_closure (by simp)
    · exact Subgroup.subset_closure (by simp)
  rcases hip ((b * a) ^ 2) hleft hright with hq | hq
  · have hai : a = a⁻¹ := (eq_inv_iff_mul_eq_one).2 ha
    have hbi : b = b⁻¹ := (eq_inv_iff_mul_eq_one).2 hb
    have hba : b * a = (b * a)⁻¹ :=
      (eq_inv_iff_mul_eq_one).2 (by simpa [pow_two] using hq)
    change a * b = b * a
    simpa only [mul_inv_rev, ← hai, ← hbi] using hba.symm
  · have h1 : b * (a * b * a) = b * 1 := by
      simpa [pow_two, mul_assoc] using hq
    have h2 : a * b * a = 1 := mul_left_cancel h1
    have h3 : a * b = a := by
      calc
        a * b = (a * b * a) * a := by rw [mul_assoc, ha, mul_one]
        _ = a := by rw [h2, one_mul]
    have h4 : b = 1 := mul_left_cancel (show a * b = a * 1 by simpa using h3)
    exact (hbne h4).elim

#print axioms central_alternating_pair_forces_commutation

end LeemansString
