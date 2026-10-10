import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.GroupTheory.Subgroup.Center
import Mathlib.Tactic

namespace HumanCompression.StringCentralizerBridge
variable {G : Type*} [Group G]

/-- A generated subgroup transfers commutation from its marked generators. -/
theorem commute_of_generators {ι : Type*} (rho : ι → G)
    (generates : Subgroup.closure (Set.range rho) = ⊤)
    (z : G) (hz : ∀ i, Commute z (rho i)) : ∀ g, Commute z g := by
  intro g
  have hg : g ∈ Subgroup.closure (Set.range rho) := by rw [generates]; trivial
  induction hg using Subgroup.closure_induction with
  | mem x hx => obtain ⟨i, rfl⟩ := hx; exact hz i
  | one => exact Commute.one_right z
  | mul x y hx hy hcx hcy => exact hcx.mul_right hcy
  | inv x hx hcx => exact hcx.inv_right

/-- No IP hypothesis is needed: a central first edge would centralize its endpoint. -/
theorem first_pair_noncommuting
    (center_free : ∀ z : G, (∀ g : G, Commute z g) → z = 1)
    {n : ℕ} (hn : 2 ≤ n) (rho : Fin n → G)
    (nonidentity : ∀ i, rho i ≠ 1)
    (string_commutations : ∀ i j : Fin n, i.val + 1 < j.val → Commute (rho i) (rho j))
    (generates : Subgroup.closure (Set.range rho) = ⊤) :
    ¬ Commute (rho ⟨0, by omega⟩) (rho ⟨1, by omega⟩) := by
  intro h01
  apply nonidentity ⟨0, by omega⟩
  apply center_free
  apply commute_of_generators rho generates
  intro j
  by_cases h0 : j.val = 0
  · have hj : j = ⟨0, by omega⟩ := Fin.ext h0
    simpa only [hj] using (Commute.refl (rho ⟨0, by omega⟩))
  by_cases h1 : j.val = 1
  · have hj : j = ⟨1, by omega⟩ := Fin.ext h1
    simpa only [hj] using h01
  · exact string_commutations _ j (by simp only; omega)

/-- An actual string marking has rank at most four when every noncommuting
involution pair has at most one nonidentity element in its common centralizer. -/
theorem string_rank_le_four
    (center_free : ∀ z : G, (∀ g : G, Commute z g) → z = 1)
    (pair_centralizer : ∀ a b x y : G,
      a * a = 1 → b * b = 1 → ¬ Commute a b →
      x ≠ 1 → y ≠ 1 →
      Commute a x → Commute b x → Commute a y → Commute b y → x = y)
    {n : ℕ} (rho : Fin n → G)
    (nonidentity : ∀ i, rho i ≠ 1)
    (involutions : ∀ i, rho i * rho i = 1)
    (distinct : Function.Injective rho)
    (string_commutations : ∀ i j : Fin n, i.val + 1 < j.val → Commute (rho i) (rho j))
    (generates : Subgroup.closure (Set.range rho) = ⊤) : n ≤ 4 := by
  by_contra h
  have hn : 5 ≤ n := by omega
  let i0 : Fin n := ⟨0, by omega⟩
  let i1 : Fin n := ⟨1, by omega⟩
  let i3 : Fin n := ⟨3, by omega⟩
  let i4 : Fin n := ⟨4, by omega⟩
  have h01 : ¬ Commute (rho i0) (rho i1) :=
    first_pair_noncommuting center_free (by omega) rho nonidentity string_commutations generates
  have h34 := pair_centralizer (rho i0) (rho i1) (rho i3) (rho i4)
    (involutions i0) (involutions i1) h01 (nonidentity i3) (nonidentity i4)
    (string_commutations i0 i3 (by dsimp [i0,i3]; omega))
    (string_commutations i1 i3 (by dsimp [i1,i3]; omega))
    (string_commutations i0 i4 (by dsimp [i0,i4]; omega))
    (string_commutations i1 i4 (by dsimp [i1,i4]; omega))
  have heq := congrArg Fin.val (distinct h34)
  dsimp [i3,i4] at heq
  omega

#print axioms commute_of_generators
#print axioms first_pair_noncommuting
#print axioms string_rank_le_four
end HumanCompression.StringCentralizerBridge
