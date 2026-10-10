import LabelEightFiniteCertificate

/-! Alphabet closure and finite-alphabet versions of the checked reductions. -/

namespace MathCompression.LabelEightCriticalPairs

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def Bounded (bound : ℕ) (u : Word) : Prop := ∀ a ∈ u, a < bound

theorem bounded_append (bound : ℕ) (u v : Word) :
    Bounded bound (u ++ v) ↔ Bounded bound u ∧ Bounded bound v := by
  simp only [Bounded, List.forall_mem_append]

def ruleClosureCheck (d bound : ℕ) : Bool :=
  (List.range bound).all fun a =>
    (List.range (a + 1)).all fun b => (rule d a b).all fun c => decide (c < bound)

def RulesClosed (d bound : ℕ) : Prop :=
  ∀ a b, a < bound → b ≤ a → Bounded bound (rule d a b)

theorem ruleClosureCheck_sound (d bound : ℕ) (h : ruleClosureCheck d bound = true) :
    RulesClosed d bound := by
  unfold ruleClosureCheck at h
  simp only [List.all_eq_true, List.mem_range, decide_eq_true_eq] at h
  intro a b ha hb
  exact h a ha b (by omega)

theorem rank14_rules_closed : RulesClosed 14 63 := by
  apply ruleClosureCheck_sound
  decide

theorem rank3_rules_closed : RulesClosed 3 8 := by
  apply ruleClosureCheck_sound
  decide

theorem step_preserves_alphabet (d bound : ℕ) (hr : RulesClosed d bound)
    {u v : Word} (h : Step d u v) (hu : Bounded bound u) : Bounded bound v := by
  cases h with
  | apply pre post a b hab =>
    have hp := (bounded_append bound pre (a :: b :: post)).mp hu
    have ha : a < bound := hp.2 a (by simp)
    have hpost : Bounded bound post := by
      intro c hc
      exact hp.2 c (by simp [hc])
    rw [List.append_assoc]
    apply (bounded_append bound pre (rule d a b ++ post)).mpr
    exact ⟨hp.1, (bounded_append bound (rule d a b) post).mpr ⟨hr a b ha hab, hpost⟩⟩

/-- Both endpoints lie in the finite alphabet and the step is a literal
presentation rewrite. Restricting every edge also restricts intermediates. -/
def AlphabetStep (d bound : ℕ) (u v : Word) : Prop :=
  Bounded bound u ∧ Step d u v ∧ Bounded bound v

theorem reachable_restrict (d bound : ℕ) (hr : RulesClosed d bound)
    {u v : Word} (h : Relation.ReflTransGen (Step d) u v) (hu : Bounded bound u) :
    Relation.ReflTransGen (AlphabetStep d bound) u v ∧ Bounded bound v := by
  induction h with
  | refl => exact ⟨.refl, hu⟩
  | @tail b c hbc hstep ih =>
    have hc := step_preserves_alphabet d bound hr hstep ih.2
    exact ⟨ih.1.tail ⟨ih.2, hstep, hc⟩, hc⟩

theorem rank14_critical_pairs_join_in_alphabet (a b c : ℕ) (ha : a < 63)
    (hb : b ≤ a) (hc : c ≤ b) :
    ∃ t, Relation.ReflTransGen (AlphabetStep 14 63) (leftBranch 14 a b c) t ∧
      Relation.ReflTransGen (AlphabetStep 14 63) (rightBranch 14 a b c) t := by
  obtain ⟨t, hl, hr⟩ := rank14_critical_pairs_join a b c ha hb hc
  have hlb : Bounded 63 (leftBranch 14 a b c) := by
    unfold leftBranch
    apply (bounded_append _ _ _).mpr
    refine ⟨rank14_rules_closed a b ha hb, ?_⟩
    simpa only [Bounded, List.mem_singleton, forall_eq] using (show c < 63 by omega)
  have hrb : Bounded 63 (rightBranch 14 a b c) := by
    intro e he
    simp only [rightBranch, List.mem_cons] at he
    rcases he with he | he
    · simpa only [he] using ha
    · exact rank14_rules_closed b c (by omega) hc e he
  exact ⟨t, (reachable_restrict 14 63 rank14_rules_closed hl hlb).1,
    (reachable_restrict 14 63 rank14_rules_closed hr hrb).1⟩

theorem sourceWord_bounded (k : ℕ) : Bounded 8 (sourceWord k) := by
  intro a ha
  simp only [sourceWord, sourceInner, List.mem_append, List.mem_flatten,
    List.mem_replicate] at ha
  rcases ha with (⟨l, hl, ha⟩ | ⟨l, hl, ha⟩) | (⟨l, hl, ha⟩ | ⟨l, hl, ha⟩)
  all_goals rcases hl with ⟨_, rfl⟩
  all_goals simp_all
  all_goals omega

theorem rank3_source_word_reduces_in_alphabet (k : ℕ) (hk : k < 8) :
    Relation.ReflTransGen (AlphabetStep 3 8) (sourceWord k) [] :=
  (reachable_restrict 3 8 rank3_rules_closed (rank3_source_word_reduces k hk)
    (sourceWord_bounded k)).1

#print axioms rank14_rules_closed
#print axioms rank3_rules_closed
#print axioms step_preserves_alphabet
#print axioms reachable_restrict
#print axioms rank14_critical_pairs_join_in_alphabet
#print axioms sourceWord_bounded
#print axioms rank3_source_word_reduces_in_alphabet

end MathCompression.LabelEightCriticalPairs
