import LabelEightCriticalPairs

/-!
Uniform triangularity and alphabet closure of the literal label-eight table.
These lemmas do not assume termination or confluence of the rewrite relation.
-/

namespace MathCompression.LabelEightCriticalPairs

/-- A nonempty square tail itself forces the input to be an x-letter. -/
theorem square_tail_triangular {d a c : ℕ} (hd : 3 ≤ d)
    (hc : c ∈ rule d a a) :
    a < c ∧ c < 5 * d - 7 := by
  simp only [rule, ↓reduceIte] at hc
  unfold decode at hc
  split_ifs at hc <;> simp_all [w]
  all_goals omega

set_option maxHeartbeats 2000000 in
theorem correction_triangular {d a b c : ℕ} (hd : 3 ≤ d)
    (ha : a < 5 * d - 7) (hba : b < a) (hc : c ∈ correction d a b) :
    a < c ∧ c < 5 * d - 7 := by
  unfold correction at hc
  split at hc
  all_goals try { simp at hc }
  all_goals unfold decode at *
  all_goals split_ifs at * <;> simp_all [x, y, z, w] <;> omega

/-- Every oriented rule stays in the alphabet and introduces no smaller letter. -/
theorem rule_mem_bounds {d a b c : ℕ} (hd : 3 ≤ d)
    (ha : a < 5 * d - 7) (hba : b ≤ a) (hc : c ∈ rule d a b) :
    b ≤ c ∧ c < 5 * d - 7 := by
  by_cases hab : a = b
  · subst b
    obtain ⟨hac, hc⟩ := square_tail_triangular hd hc
    exact ⟨hac.le, hc⟩
  · have hlt : b < a := lt_of_le_of_ne hba (Ne.symm hab)
    simp only [rule, if_neg hab, List.mem_cons] at hc
    rcases hc with rfl | rfl | hc
    · exact ⟨le_rfl, lt_of_lt_of_le hlt ha.le⟩
    · exact ⟨hba, ha⟩
    · obtain ⟨hac, hc⟩ := correction_triangular hd ha hlt hc
      exact ⟨hba.trans hac.le, hc⟩

/-- Actual contextual rewrite steps preserve any allowed lower alphabet cutoff. -/
theorem uniform_step_preserves_range {d lo : ℕ} {u v : Word} (hd : 3 ≤ d)
    (h : Step d u v) (hu : ∀ c ∈ u, lo ≤ c ∧ c < 5 * d - 7) :
    ∀ c ∈ v, lo ≤ c ∧ c < 5 * d - 7 := by
  cases h with
  | apply pre post a b hba =>
    have ha := hu a (by simp)
    have hb := hu b (by simp)
    intro c hc
    simp only [List.mem_append] at hc
    rcases hc with (hc | hc) | hc
    · exact hu c (by simp [hc])
    · obtain ⟨hbc, hbound⟩ := rule_mem_bounds hd ha.2 hba hc
      exact ⟨hb.1.trans hbc, hbound⟩
    · exact hu c (by simp [hc])

theorem uniform_reachable_preserves_range {d lo : ℕ} {u v : Word} (hd : 3 ≤ d)
    (h : Relation.ReflTransGen (Step d) u v)
    (hu : ∀ c ∈ u, lo ≤ c ∧ c < 5 * d - 7) :
    ∀ c ∈ v, lo ≤ c ∧ c < 5 * d - 7 := by
  induction h with
  | refl => exact hu
  | tail h hstep ih => exact uniform_step_preserves_range hd hstep ih

#print axioms square_tail_triangular
#print axioms correction_triangular
#print axioms rule_mem_bounds
#print axioms uniform_step_preserves_range
#print axioms uniform_reachable_preserves_range

end MathCompression.LabelEightCriticalPairs
