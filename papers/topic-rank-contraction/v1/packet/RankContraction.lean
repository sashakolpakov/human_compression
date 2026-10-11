import Mathlib.Algebra.Group.Subgroup.Ker
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Algebra.Group.Commute.Basic

/- Actual algebraic interfaces of the contraction proof. The string-C induction
and the classical-group applications are written, not formalized here. -/
namespace RankContraction
variable {G : Type*} [Group G]

theorem odd_recovery {a b c : G} (k : ℕ) (ha : a ^ 2 = 1)
    (hab : Commute a b) (hac : Commute a c)
    (hbc : (b * c) ^ (2 * k + 1) = 1) :
    ((a * b) * c) ^ (2 * k + 1) = a := by
  rw [mul_assoc, (hab.mul_right hac).mul_pow, hbc, mul_one]
  simp [pow_add, pow_mul, ha]

theorem recovered_mem {a b c : G} (H : Subgroup G) (k : ℕ)
    (ha : a ^ 2 = 1) (hab : Commute a b) (hac : Commute a c)
    (hbc : (b * c) ^ (2 * k + 1) = 1)
    (hm : a * b ∈ H) (hc : c ∈ H) : a ∈ H := by
  rw [← odd_recovery k ha hab hac hbc]
  exact H.pow_mem (H.mul_mem hm hc) _

theorem other_mark_mem {a b : G} (H : Subgroup G)
    (ha : a ∈ H) (hab : a * b ∈ H) : b ∈ H := by
  have h := H.mul_mem (H.inv_mem ha) hab
  simpa [mul_assoc] using h

theorem central_parity_obstruction {C : Type*} [Group C]
    (χ : G →* C) {a b c : G}
    (ha : χ a ≠ 1) (hab : χ (a * b) = 1) (hc : χ c = 1) :
    a ∉ Subgroup.closure ({a * b, c} : Set G) := by
  have hsub : Subgroup.closure ({a * b, c} : Set G) ≤ χ.ker := by
    apply (Subgroup.closure_le χ.ker).mpr
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact hab
    · exact hc
  intro hm
  exact ha (hsub hm)

#print axioms odd_recovery
#print axioms recovered_mem
#print axioms other_mark_mem
#print axioms central_parity_obstruction
end RankContraction
