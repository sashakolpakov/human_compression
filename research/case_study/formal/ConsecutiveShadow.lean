import BooleanShadow

/-!
The bounded witness remains inside every consecutive interval of proper
Boolean ranks. The query is an arbitrary finite family, not necessarily a
flag. Tree realization, branching obstructions and residue joins are not
formalized by this module.
-/

namespace BooleanShadow

variable {α : Type*} [DecidableEq α] [Fintype α]

omit [Fintype α] in
theorem lower_rank_bound {U : Finset (Finset α)} {k lo : ℕ}
    (hU : ∀ X ∈ U, lo ≤ X.card) (hne : lower U k ≠ ∅) :
    lo ≤ (lower U k).card := by
  obtain ⟨a, ha⟩ := Finset.nonempty_iff_ne_empty.mpr hne
  obtain ⟨X, hX, hlt, _⟩ := mem_lower.mp ha
  exact (hU X hX).trans (Finset.card_le_card (smaller_subset_lower hX hlt))

theorem upper_rank_bound {U : Finset (Finset α)} {k hi : ℕ}
    (hU : ∀ X ∈ U, X.card ≤ hi) (hne : upper U k ≠ Finset.univ) :
    (upper U k).card ≤ hi := by
  classical
  by_cases hs : ∃ X ∈ U, k < X.card
  · obtain ⟨X, hX, hlt⟩ := hs
    exact (Finset.card_le_card (upper_subset_larger hX hlt)).trans (hU X hX)
  · have heq : upper U k = Finset.univ := by
      ext a
      simp only [mem_upper, Finset.mem_univ, iff_true]
      intro X hX hlt
      exact False.elim (hs ⟨X, hX, hlt⟩)
    exact False.elim (hne heq)

/-- Every nonempty shadow in consecutive proper ranks has a witness of
at most two vertices, both still in the retained ranks. -/
theorem exists_witness_in_consecutive_ranks
    {U : Finset (Finset α)} {lo hi k : ℕ}
    (hlo : 0 < lo) (hhi : hi < (Finset.univ : Finset α).card)
    (hkl : lo ≤ k) (hkh : k ≤ hi)
    (hU : ∀ X ∈ U, lo ≤ X.card ∧ X.card ≤ hi)
    (hne : ∃ Y, Shadow U k Y) :
    ∃ C, Witness U k C ∧ ∀ X ∈ C, lo ≤ X.card ∧ X.card ≤ hi := by
  classical
  have hk0 : 0 < k := by omega
  have hktop : k < (Finset.univ : Finset α).card := by omega
  obtain ⟨Y₀, hY₀⟩ := hne
  have hsingleton (hunique : ∀ Y, Shadow U k Y → Y = Y₀) :
      ∃ C, Witness U k C ∧ ∀ X ∈ C, lo ≤ X.card ∧ X.card ≤ hi := by
    refine ⟨{Y₀}, singleton_witness hk0 hktop hY₀ hunique, ?_⟩
    intro X hX
    have heq := Finset.mem_singleton.mp hX
    simpa only [heq, hY₀.1] using And.intro hkl hkh
  by_cases heq : ∃ X ∈ U, X.card = k
  · obtain ⟨X, hX, hXcard⟩ := heq
    apply hsingleton
    intro Y hY
    exact (shadow_eq_of_same_rank_member hX hXcard hY).trans
      (shadow_eq_of_same_rank_member hX hXcard hY₀).symm
  · have hno : ∀ X ∈ U, X.card ≠ k := by
      intro X hX hcard
      exact heq ⟨X, hX, hcard⟩
    have hb := shadow_bounds hY₀
    have hYcard := hY₀.1
    have hLc := Finset.card_le_card hb.1
    have hVc := Finset.card_le_card hb.2
    by_cases hLeq : (lower U k).card = k
    · apply hsingleton
      intro Y hY
      have hYc := hY.1
      have hLY : lower U k = Y := Finset.eq_of_subset_of_card_le
        (shadow_bounds hY).1 (by omega)
      have hLY₀ : lower U k = Y₀ := Finset.eq_of_subset_of_card_le hb.1 (by omega)
      exact hLY.symm.trans hLY₀
    · by_cases hVeq : (upper U k).card = k
      · apply hsingleton
        intro Y hY
        have hYc := hY.1
        have hYV : Y = upper U k := Finset.eq_of_subset_of_card_le
          (shadow_bounds hY).2 (by omega)
        have hY₀V : Y₀ = upper U k := Finset.eq_of_subset_of_card_le hb.2 (by omega)
        exact hYV.trans hY₀V.symm
      · have hL : (lower U k).card < k := by omega
        have hV : k < (upper U k).card := by omega
        refine ⟨boundaryFlag (lower U k) (upper U k),
          boundaryFlag_witness hno ⟨Y₀, hY₀⟩ hL hV, ?_⟩
        intro X hX
        have hm := mem_boundaryFlag.mp hX
        rcases hm.1 with rfl | rfl
        · exact ⟨lower_rank_bound (fun X hX => (hU X hX).1) hm.2.1, by omega⟩
        · exact ⟨by omega, upper_rank_bound (fun X hX => (hU X hX).2) hm.2.2⟩

end BooleanShadow

#print axioms BooleanShadow.exists_witness_in_consecutive_ranks
