import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-
Scoped formalization of the averaging and distance deductions.
The balanced incidence identity is an explicit premise: this file does not
formalize the group action, information sets, field models or C enumeration.
-/
namespace TransitiveCodeBounds
open scoped BigOperators

/-- Balanced incidence counts give a representative of bounded message weight. -/
theorem exists_information_bound {T : Type*} [Fintype T] [Nonempty T]
    (m : T → ℕ) (n k w : ℕ) (hn : 0 < n)
    (hbalance : (∑ t, n * m t) = Fintype.card T * (k * w)) :
    ∃ t, m t ≤ k * w / n := by
  have hex : ∃ t, n * m t ≤ k * w := by
    by_contra h
    push Not at h
    have hs : (∑ _t : T, k * w) < ∑ t : T, n * m t :=
      Finset.sum_lt_sum_of_nonempty Finset.univ_nonempty (fun t _ => h t)
    simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, hbalance] at hs
    exact (Nat.lt_irrefl _ hs)
  obtain ⟨t, ht⟩ := hex
  refine ⟨t, (Nat.le_div_iff_mul_le hn).2 ?_⟩
  simpa only [Nat.mul_comm] using ht

/-- A complete restricted enumeration proves the lower bound after averaging. -/
theorem distance_lower_bound {C : Type*} (z : C) (wt msg : C → ℕ)
    (n k D : ℕ)
    (hrep : ∀ c, c ≠ z → ∃ d, d ≠ z ∧ wt d = wt c ∧ msg d ≤ k * wt c / n)
    (henum : ∀ d, d ≠ z → msg d ≤ k * (D - 1) / n → D ≤ wt d) :
    ∀ c, c ≠ z → D ≤ wt c := by
  intro c hc
  by_contra h
  have hw : wt c ≤ D - 1 := by omega
  obtain ⟨d, hd, heq, hm⟩ := hrep c hc
  have hb : msg d ≤ k * (D - 1) / n :=
    hm.trans (Nat.div_le_div_right (Nat.mul_le_mul_left k hw))
  have hl := henum d hd hb
  omega

/-- An invariant proposed minimum set is exhaustive once every representative is. -/
theorem minimum_set_exhaustive {C : Type*} (S : Set C) (wt msg : C → ℕ)
    (n k D : ℕ)
    (hrep : ∀ c, wt c = D → ∃ d, wt d = D ∧ msg d ≤ k * D / n ∧ (d ∈ S → c ∈ S))
    (henum : ∀ d, wt d = D → msg d ≤ k * D / n → d ∈ S) :
    ∀ c, wt c = D → c ∈ S := by
  intro c hc
  obtain ⟨d, hd, hm, hback⟩ := hrep c hc
  exact hback (henum d hd hm)

#print axioms exists_information_bound
#print axioms distance_lower_bound
#print axioms minimum_set_exhaustive
end TransitiveCodeBounds
