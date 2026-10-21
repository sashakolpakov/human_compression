import LabelEightTriangular
import TriangularWordTermination

/-!
All-rank termination for the actual label-eight rewrite table.  The order is
constructed in `TriangularWordTermination`; the strict table inequalities and
alphabet closure are proved in `LabelEightTriangular`.
-/

namespace MathCompression.LabelEightCriticalPairs

open MathCompression.TriangularWordTermination

theorem uniform_step_refines_triangular {d : ℕ} {u v : Word} (hd : 3 ≤ d)
    (h : Step d u v) (hu : ∀ c ∈ u, c < 5 * d - 7) :
    TriangularStep (5 * d - 7) u v := by
  cases h with
  | apply pre post a b hba =>
    have ha : a < 5 * d - 7 := hu a (by simp)
    by_cases hab : a = b
    · subst b
      have ht : ∀ c ∈ rule d a a, a < c :=
        fun c hc => (square_tail_triangular hd hc).1
      simpa only [List.append_assoc, List.cons_append, List.nil_append] using
        TriangularStep.square pre post (rule d a a) a ha ht
    · have hlt : b < a := lt_of_le_of_ne hba (Ne.symm hab)
      have ht : ∀ c ∈ correction d a b, a < c :=
        fun c hc => (correction_triangular hd ha hlt hc).1
      simpa only [rule, if_neg hab, List.append_assoc, List.cons_append, List.nil_append] using
        TriangularStep.swap pre post (correction d a b) a b ha hlt ht

theorem uniform_step_decreases {d : ℕ} {u v : Word} (hd : 3 ≤ d)
    (h : Step d u v) (hu : ∀ c ∈ u, c < 5 * d - 7) :
    BlockOrder 0 (5 * d - 7) v u :=
  triangular_step_decreases (uniform_step_refines_triangular hd h hu)

/-- Every word in the actual finite alphabet is accessible for the reverse of
the rewrite relation, so no infinite sequence of forward rewrites starts there. -/
theorem uniform_step_accessible {d : ℕ} (hd : 3 ≤ d) (u : Word)
    (hu : ∀ c ∈ u, c < 5 * d - 7) : Acc (fun v u => Step d u v) u := by
  revert hu
  refine (blockOrder_wf 0 (5 * d - 7)).induction
    (C := fun u => (∀ c ∈ u, c < 5 * d - 7) → Acc (fun v u => Step d u v) u) u ?_
  intro u ih hu
  refine Acc.intro u ?_
  intro v hstep
  apply ih v (uniform_step_decreases hd hstep hu)
  intro c hc
  exact (uniform_step_preserves_range hd hstep (fun a ha => ⟨Nat.zero_le a, hu a ha⟩) c hc).2

theorem uniform_bounded_step_wf {d : ℕ} (hd : 3 ≤ d) :
    WellFounded (fun v u : {u : Word // ∀ c ∈ u, c < 5 * d - 7} =>
      Step d u.val v.val) := by
  apply (InvImage.wf Subtype.val (blockOrder_wf 0 (5 * d - 7))).mono
  intro v u h
  exact uniform_step_decreases hd h u.property

/-- Accessibility supplies some sufficient fuel for the literal leftmost
collector.  No numerical fuel estimate is assumed or claimed. -/
theorem collector_terminates_of_accessible {d : ℕ} {u : Word}
    (h : Acc (fun v u => Step d u v) u) :
    ∃ fuel, next d (collect d fuel u) = none := by
  induction h with
  | intro u _ ih =>
    cases hn : next d u with
    | none => exact ⟨0, by simpa [collect] using hn⟩
    | some v =>
      obtain ⟨fuel, hfuel⟩ := ih v (next_sound d u v hn)
      exact ⟨fuel + 1, by simpa [collect, hn] using hfuel⟩

theorem uniform_collector_terminates {d : ℕ} (hd : 3 ≤ d) (u : Word)
    (hu : ∀ c ∈ u, c < 5 * d - 7) :
    ∃ fuel, next d (collect d fuel u) = none :=
  collector_terminates_of_accessible (uniform_step_accessible hd u hu)

#print axioms uniform_step_refines_triangular
#print axioms uniform_step_decreases
#print axioms uniform_step_accessible
#print axioms uniform_bounded_step_wf
#print axioms collector_terminates_of_accessible
#print axioms uniform_collector_terminates

end MathCompression.LabelEightCriticalPairs
