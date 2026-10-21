import Mathlib.GroupTheory.Commutator.Basic
import Mathlib.Tactic

/-!
Exact bidirectional local relation adapter for the universal label-four
presentation. This file does not assume or formalize the Biss--Dasgupta
identification of their presented group with a unitriangular matrix group.
-/

open scoped commutatorElement

namespace MathCompression.LabelFourRelations

variable {G : Type*} [Group G]

/-- For involutory generators, the adjacent commutator is the product square. -/
theorem commutator_eq_square (a b : G) (ha : a * a = 1) (hb : b * b = 1) :
    ⁅a, b⁆ = (a * b) ^ 2 := by
  have hai := inv_eq_of_mul_eq_one_right ha
  have hbi := inv_eq_of_mul_eq_one_right hb
  simp [commutatorElement_def, hai, hbi, pow_two, mul_assoc]

/-- Both nested adjacent commutators are the inverse fourth power. -/
theorem nested_commutators (a b : G) (ha : a * a = 1) (hb : b * b = 1) :
    ⁅a, ⁅a, b⁆⁆ = ((a * b) ^ 4)⁻¹ ∧ ⁅b, ⁅a, b⁆⁆ = ((a * b) ^ 4)⁻¹ := by
  have hai := inv_eq_of_mul_eq_one_right ha
  have hbi := inv_eq_of_mul_eq_one_right hb
  have hca : a * (a * b) * a⁻¹ = (a * b)⁻¹ := by
    calc
      a * (a * b) * a⁻¹ = (a * a) * b * a⁻¹ := by group
      _ = b * a⁻¹ := by rw [ha]; simp
      _ = (a * b)⁻¹ := by simp [hbi]
  have hcb : b * (a * b) * b⁻¹ = (a * b)⁻¹ := by
    calc
      b * (a * b) * b⁻¹ = b * a := by group
      _ = (a * b)⁻¹ := by simp [hai, hbi]
  have calc_nested (x : G) (hx : x * (a * b) * x⁻¹ = (a * b)⁻¹) :
      ⁅x, ⁅a, b⁆⁆ = ((a * b) ^ 4)⁻¹ := by
    rw [commutator_eq_square a b ha hb, commutatorElement_def]
    calc
      x * (a * b) ^ 2 * x⁻¹ * ((a * b) ^ 2)⁻¹ =
          (x * (a * b) * x⁻¹) ^ 2 * ((a * b) ^ 2)⁻¹ := by simp only [pow_succ, pow_zero]; group
      _ = _ := by rw [hx]; simp only [pow_succ, pow_zero]; group
  exact ⟨calc_nested a hca, calc_nested b hcb⟩

/-- The adjacent Biss--Dasgupta relations at m=2 are equivalent to the
fourth-power relation, in every ambient group. -/
theorem adjacent_relations_iff (a b : G) (ha : a * a = 1) (hb : b * b = 1) :
    (⁅a, ⁅a, b⁆⁆ = 1 ∧ ⁅b, ⁅a, b⁆⁆ = 1) ↔ (a * b) ^ 4 = 1 := by
  rw [(nested_commutators a b ha hb).1, (nested_commutators a b ha hb).2]
  simp

/-- Two elements of square one commute exactly when their reversed product
has square one. Identity elements are allowed. -/
theorem commutator_iff_reversed_square (u v : G)
    (hu : u * u = 1) (hv : v * v = 1) :
    ⁅u, v⁆ = 1 ↔ (v * u) ^ 2 = 1 := by
  have hui := inv_eq_of_mul_eq_one_right hu
  have hvi := inv_eq_of_mul_eq_one_right hv
  rw [commutatorElement_eq_one_iff_mul_comm, pow_two, mul_eq_one_iff_eq_inv,
    mul_inv_rev, hui, hvi]
  exact eq_comm

/-- The cross-commutator relation is precisely the source k=2 relator
once the adjacent fourth powers and generator involutions hold. -/
theorem cross_relation_iff (a b c : G)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hab : (a * b) ^ 4 = 1) (hbc : (b * c) ^ 4 = 1) :
    ⁅⁅a, b⁆, ⁅b, c⁆⁆ = 1 ↔ ((b * c) ^ 2 * (a * b) ^ 2) ^ 2 = 1 := by
  rw [commutator_eq_square a b ha hb, commutator_eq_square b c hb hc]
  apply commutator_iff_reversed_square
  · calc (a * b) ^ 2 * (a * b) ^ 2 = (a * b) ^ 4 := by rw [← pow_add]
         _ = 1 := hab
  · calc (b * c) ^ 2 * (b * c) ^ 2 = (b * c) ^ 4 := by rw [← pow_add]
         _ = 1 := hbc

/-- Nonadjacent commutation already supplies the source k=1 relator. -/
theorem first_power_relation (a b c : G)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hac : Commute a c) : ((b * c) * (a * b)) ^ 2 = 1 := by
  have hbi := inv_eq_of_mul_eq_one_right hb
  have hac2 : (a * c) ^ 2 = 1 := by
    rw [hac.mul_pow, pow_two, pow_two, ha, hc, one_mul]
  have hword : (b * c) * (a * b) = b * (a * c) * b⁻¹ := by
    calc
      (b * c) * (a * b) = b * (c * a) * b := by group
      _ = b * (a * c) * b⁻¹ := by rw [hac.eq, hbi]
  rw [hword]
  calc (b * (a * c) * b⁻¹) ^ 2 = b * (a * c) ^ 2 * b⁻¹ := by simp only [pow_succ, pow_zero]; group
       _ = 1 := by rw [hac2]; group

/-- The source k=3 relator follows from the two fourth powers and distant
commutation; it is not a further presentation relation. -/
theorem third_power_relation (a b c : G)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hac : Commute a c)
    (hab : (a * b) ^ 4 = 1) (hbc : (b * c) ^ 4 = 1) :
    ((b * c) ^ 3 * (a * b) ^ 3) ^ 2 = 1 := by
  have cube_inv (x : G) (hx : x ^ 4 = 1) : x ^ 3 = x⁻¹ := by
    apply eq_inv_iff_mul_eq_one.mpr
    calc x ^ 3 * x = x ^ 4 := by simp only [pow_succ, pow_zero]
         _ = 1 := hx
  have hac2 : (a * c) ^ 2 = 1 := by
    rw [hac.mul_pow, pow_two, pow_two, ha, hc, one_mul]
  have habbc : (a * b) * (b * c) = a * c := by
    calc (a * b) * (b * c) = a * (b * b) * c := by group
         _ = a * c := by rw [hb]; simp
  rw [cube_inv _ hbc, cube_inv _ hab, ← mul_inv_rev, habbc, inv_pow, hac2, inv_one]

/-- Exact bidirectional adapter for a consecutive triple, under the common
involution and distant-commutation relations of both presentations. -/
theorem label_four_relations_iff (a b c : G)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hac : Commute a c) :
    ((a * b) ^ 4 = 1 ∧ (b * c) ^ 4 = 1 ∧
      ∀ k : ℕ, 1 ≤ k → k ≤ 3 → ((b * c) ^ k * (a * b) ^ k) ^ 2 = 1) ↔
    ((⁅a, ⁅a, b⁆⁆ = 1 ∧ ⁅b, ⁅a, b⁆⁆ = 1) ∧
      (⁅b, ⁅b, c⁆⁆ = 1 ∧ ⁅c, ⁅b, c⁆⁆ = 1) ∧
      ⁅⁅a, b⁆, ⁅b, c⁆⁆ = 1) := by
  constructor
  · rintro ⟨hab, hbc, hrel⟩
    exact ⟨(adjacent_relations_iff a b ha hb).mpr hab,
      (adjacent_relations_iff b c hb hc).mpr hbc,
      (cross_relation_iff a b c ha hb hc hab hbc).mpr (hrel 2 (by decide) (by decide))⟩
  · rintro ⟨hab', hbc', hcross⟩
    have hab := (adjacent_relations_iff a b ha hb).mp hab'
    have hbc := (adjacent_relations_iff b c hb hc).mp hbc'
    refine ⟨hab, hbc, ?_⟩
    intro k hk₁ hk₃
    interval_cases k
    · simpa using first_power_relation a b c ha hb hc hac
    · exact (cross_relation_iff a b c ha hb hc hab hbc).mp hcross
    · exact third_power_relation a b c ha hb hc hac hab hbc

#print axioms commutator_eq_square
#print axioms nested_commutators
#print axioms adjacent_relations_iff
#print axioms commutator_iff_reversed_square
#print axioms cross_relation_iff
#print axioms first_power_relation
#print axioms third_power_relation
#print axioms label_four_relations_iff

end MathCompression.LabelFourRelations
