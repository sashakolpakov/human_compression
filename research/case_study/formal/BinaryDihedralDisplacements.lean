import Mathlib.Tactic
import Mathlib.GroupTheory.Subgroup.Centralizer

/-! Algebra of involutory displacements, including the finite presentation's
period adapter. This file does not formalize the full polytope construction. -/
namespace HumanCompression.BinaryDihedral
variable {G : Type*} [Group G] (x y : G)
def displacement (k : ℤ) : G := y ^ k * x ^ k

lemma inverse_of_square_one (a : G) (h : a * a = 1) : a⁻¹ = a := by
  calc
    a⁻¹ = a⁻¹ * (a * a) := by rw [h, mul_one]
    _ = a := by group

lemma displacement_reverse
    (h : ∀ k : ℤ, displacement x y k * displacement x y k = 1) (k : ℤ) :
    y ^ k * x ^ k = x ^ (-k) * y ^ (-k) := by
  have hh := inverse_of_square_one (displacement x y k) (h k)
  simpa only [displacement, mul_inv_rev, ← zpow_neg] using hh.symm

lemma reversed_displacement
    (h : ∀ k : ℤ, displacement x y k * displacement x y k = 1) (k : ℤ) :
    x ^ k * y ^ k = y ^ (-k) * x ^ (-k) := by
  calc
    x ^ k * y ^ k = x ^ k * (y ^ k * x ^ k) * x ^ (-k) := by group
    _ = x ^ k * (x ^ (-k) * y ^ (-k)) * x ^ (-k) := by rw [displacement_reverse x y h k]
    _ = y ^ (-k) * x ^ (-k) := by group

lemma displacement_product
    (h : ∀ k : ℤ, displacement x y k * displacement x y k = 1) (i j : ℤ) :
    displacement x y i * displacement x y j = x ^ (-i) * y ^ (j-i) * x ^ j := by
  change (y ^ i * x ^ i) * (y ^ j * x ^ j) = _
  rw [displacement_reverse x y h i]
  group

theorem displacements_commute
    (h : ∀ k : ℤ, displacement x y k * displacement x y k = 1) (i j : ℤ) :
    displacement x y i * displacement x y j = displacement x y j * displacement x y i := by
  rw [displacement_product x y h i j, displacement_product x y h j i]
  calc
    x ^ (-i) * y ^ (j-i) * x ^ j =
        x ^ (-j) * (x ^ (j-i) * y ^ (j-i)) * x ^ j := by group
    _ = x ^ (-j) * (y ^ (-(j-i)) * x ^ (-(j-i))) * x ^ j := by
      rw [reversed_displacement x y h (j-i)]
    _ = x ^ (-j) * y ^ (i-j) * x ^ i := by group

theorem displacement_conjugation (k : ℤ) :
    x⁻¹ * displacement x y k * x =
      (displacement x y 1)⁻¹ * displacement x y (k+1) := by
  simp only [displacement]
  group

theorem displacement_closure_commutative
    (h : ∀ k : ℤ, displacement x y k * displacement x y k = 1) :
    IsMulCommutative (Subgroup.closure (Set.range (displacement x y))) := by
  apply Subgroup.isMulCommutative_closure
  rintro a ⟨i, rfl⟩ b ⟨j, rfl⟩
  exact displacements_commute x y h i j

theorem finite_period_involutions (n : ℕ) (hn : 0 < n)
    (hx : x ^ n = 1) (hy : y ^ n = 1)
    (h : ∀ k : ℕ, 0 < k → k < n →
      displacement x y (k : ℤ) * displacement x y (k : ℤ) = 1) :
    ∀ k : ℤ, displacement x y k * displacement x y k = 1 := by
  intro k
  have hnz : (n : ℤ) ≠ 0 := by omega
  have hnonneg := Int.emod_nonneg k hnz
  have hnpos : (0 : ℤ) < (n : ℤ) := by exact_mod_cast hn
  have hlt := Int.emod_lt_of_pos k hnpos
  have heq : ((k % (n : ℤ)).toNat : ℤ) = k % (n : ℤ) :=
    Int.toNat_of_nonneg hnonneg
  have hd : displacement x y k =
      displacement x y ((k % (n : ℤ)).toNat : ℤ) := by
    simp only [displacement, heq]
    rw [zpow_eq_zpow_emod' k hy, zpow_eq_zpow_emod' k hx]
  rw [hd]
  by_cases hz : (k % (n : ℤ)).toNat = 0
  · simp [hz, displacement]
  · apply h
    · omega
    · omega

theorem finite_displacement_closure_commutative (n : ℕ) (hn : 0 < n)
    (hx : x ^ n = 1) (hy : y ^ n = 1)
    (h : ∀ k : ℕ, 0 < k → k < n →
      displacement x y (k : ℤ) * displacement x y (k : ℤ) = 1) :
    IsMulCommutative (Subgroup.closure (Set.range (displacement x y))) :=
  displacement_closure_commutative x y (finite_period_involutions x y n hn hx hy h)

#print axioms displacements_commute
#print axioms displacement_conjugation
#print axioms displacement_closure_commutative
#print axioms finite_period_involutions
#print axioms finite_displacement_closure_commutative
end HumanCompression.BinaryDihedral
