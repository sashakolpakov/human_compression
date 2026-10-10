import Mathlib.Algebra.Group.Subgroup.Basic

/-!
A two-coset interval certificate for the second difficult case of an
endpoint-halving intersection criterion. No finiteness, actual index-two
assumption, normality, or disjointness of the two cosets is required.
-/

namespace EndpointHalving

variable {G : Type*} [Group G]

/-- A subgroup inside a two-coset interval equals its lower endpoint exactly
when containing the chosen representative adds nothing to that endpoint. -/
theorem subgroup_eq_iff_representative (U H K : Subgroup G) (a : G)
    (hHK : H ≤ K) (hKU : K ≤ U)
    (hcover : ∀ x ∈ U, x ∈ H ∨ ∃ h ∈ H, x = a * h) :
    K = H ↔ (a ∈ K → a ∈ H) := by
  constructor
  · intro hEq ha
    simpa [hEq] using ha
  · intro ha
    apply le_antisymm
    · intro x hx
      rcases hcover x (hKU hx) with hxH | ⟨h, hh, hxh⟩
      · exact hxH
      · have haK : a ∈ K := by
          have hprod := K.mul_mem hx (K.inv_mem (hHK hh))
          simpa [hxh] using hprod
        rw [hxh]
        exact H.mul_mem (ha haK) hh
    · exact hHK

/-- The intersection version: the only possible excess is detected by the
chosen coset representative belonging to both subgroups. -/
theorem intersection_eq_iff_representative (U H A B : Subgroup G) (a : G)
    (hHA : H ≤ A) (hHB : H ≤ B) (hMeet : A ⊓ B ≤ U)
    (hcover : ∀ x ∈ U, x ∈ H ∨ ∃ h ∈ H, x = a * h) :
    A ⊓ B = H ↔ (a ∈ A → a ∈ B → a ∈ H) := by
  constructor
  · intro hEq ha hb
    have hmem : a ∈ A ⊓ B := ⟨ha, hb⟩
    simpa [hEq] using hmem
  · intro h
    apply (subgroup_eq_iff_representative U H (A ⊓ B) a
      (fun _ hx => ⟨hHA hx, hHB hx⟩) hMeet hcover).2
    intro ha
    exact h ha.1 ha.2

/-- Under the same hypotheses, any actual excess forces the representative
to belong to both subgroups and to lie outside the expected intersection. -/
theorem excess_witness_forces_representative (U H A B : Subgroup G) (a x : G)
    (hHA : H ≤ A) (hHB : H ≤ B) (hMeet : A ⊓ B ≤ U)
    (hcover : ∀ y ∈ U, y ∈ H ∨ ∃ h ∈ H, y = a * h)
    (hxA : x ∈ A) (hxB : x ∈ B) (hxH : x ∉ H) :
    a ∈ A ∧ a ∈ B ∧ a ∉ H := by
  rcases hcover x (hMeet ⟨hxA, hxB⟩) with h | ⟨h, hh, hxh⟩
  · exact False.elim (hxH h)
  · have haA : a ∈ A := by
      have hprod := A.mul_mem hxA (A.inv_mem (hHA hh))
      simpa [hxh] using hprod
    have haB : a ∈ B := by
      have hprod := B.mul_mem hxB (B.inv_mem (hHB hh))
      simpa [hxh] using hprod
    refine ⟨haA, haB, ?_⟩
    intro haH
    apply hxH
    rw [hxh]
    exact H.mul_mem haH hh

#print axioms subgroup_eq_iff_representative
#print axioms intersection_eq_iff_representative
#print axioms excess_witness_forces_representative

end EndpointHalving
