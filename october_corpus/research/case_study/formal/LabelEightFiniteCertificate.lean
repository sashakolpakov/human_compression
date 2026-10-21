import LabelEightCriticalPairs

/-!
Kernel-checked finite joinability for all descending triples on the actual
63-letter rank-fourteen alphabet, plus the eight rank-three source words.
This does not assert the separate uniform support-compression theorem.
-/

namespace MathCompression.LabelEightCriticalPairs

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def rowCheck (d fuel a : ℕ) : Bool :=
  (List.range (a + 1)).all fun b =>
    (List.range (b + 1)).all fun c => criticalCheck d fuel a b c

def allCritical (d bound fuel : ℕ) : Bool :=
  (List.range bound).all (rowCheck d fuel)

theorem allCritical_sound (d bound fuel : ℕ) (h : allCritical d bound fuel = true)
    (a b c : ℕ) (ha : a < bound) (hb : b ≤ a) (hc : c ≤ b) :
    ∃ t, Relation.ReflTransGen (Step d) (leftBranch d a b c) t ∧
      Relation.ReflTransGen (Step d) (rightBranch d a b c) t := by
  unfold allCritical rowCheck at h
  simp only [List.all_eq_true, List.mem_range] at h
  exact criticalCheck_sound d fuel a b c (h a ha b (by omega) c (by omega))

/-- The complete check is divided into rows so that kernel reduction
keeps a bounded working set. Every row is proved by ordinary `decide`. -/
theorem checkedRow0 : rowCheck 14 32 0 = true := by decide
theorem checkedRow1 : rowCheck 14 32 1 = true := by decide
theorem checkedRow2 : rowCheck 14 32 2 = true := by decide
theorem checkedRow3 : rowCheck 14 32 3 = true := by decide
theorem checkedRow4 : rowCheck 14 32 4 = true := by decide
theorem checkedRow5 : rowCheck 14 32 5 = true := by decide
theorem checkedRow6 : rowCheck 14 32 6 = true := by decide
theorem checkedRow7 : rowCheck 14 32 7 = true := by decide
theorem checkedRow8 : rowCheck 14 32 8 = true := by decide
theorem checkedRow9 : rowCheck 14 32 9 = true := by decide
theorem checkedRow10 : rowCheck 14 32 10 = true := by decide
theorem checkedRow11 : rowCheck 14 32 11 = true := by decide
theorem checkedRow12 : rowCheck 14 32 12 = true := by decide
theorem checkedRow13 : rowCheck 14 32 13 = true := by decide
theorem checkedRow14 : rowCheck 14 32 14 = true := by decide
theorem checkedRow15 : rowCheck 14 32 15 = true := by decide
theorem checkedRow16 : rowCheck 14 32 16 = true := by decide
theorem checkedRow17 : rowCheck 14 32 17 = true := by decide
theorem checkedRow18 : rowCheck 14 32 18 = true := by decide
theorem checkedRow19 : rowCheck 14 32 19 = true := by decide
theorem checkedRow20 : rowCheck 14 32 20 = true := by decide
theorem checkedRow21 : rowCheck 14 32 21 = true := by decide
theorem checkedRow22 : rowCheck 14 32 22 = true := by decide
theorem checkedRow23 : rowCheck 14 32 23 = true := by decide
theorem checkedRow24 : rowCheck 14 32 24 = true := by decide
theorem checkedRow25 : rowCheck 14 32 25 = true := by decide
theorem checkedRow26 : rowCheck 14 32 26 = true := by decide
theorem checkedRow27 : rowCheck 14 32 27 = true := by decide
theorem checkedRow28 : rowCheck 14 32 28 = true := by decide
theorem checkedRow29 : rowCheck 14 32 29 = true := by decide
theorem checkedRow30 : rowCheck 14 32 30 = true := by decide
theorem checkedRow31 : rowCheck 14 32 31 = true := by decide
theorem checkedRow32 : rowCheck 14 32 32 = true := by decide
theorem checkedRow33 : rowCheck 14 32 33 = true := by decide
theorem checkedRow34 : rowCheck 14 32 34 = true := by decide
theorem checkedRow35 : rowCheck 14 32 35 = true := by decide
theorem checkedRow36 : rowCheck 14 32 36 = true := by decide
theorem checkedRow37 : rowCheck 14 32 37 = true := by decide
theorem checkedRow38 : rowCheck 14 32 38 = true := by decide
theorem checkedRow39 : rowCheck 14 32 39 = true := by decide
theorem checkedRow40 : rowCheck 14 32 40 = true := by decide
theorem checkedRow41 : rowCheck 14 32 41 = true := by decide
theorem checkedRow42 : rowCheck 14 32 42 = true := by decide
theorem checkedRow43 : rowCheck 14 32 43 = true := by decide
theorem checkedRow44 : rowCheck 14 32 44 = true := by decide
theorem checkedRow45 : rowCheck 14 32 45 = true := by decide
theorem checkedRow46 : rowCheck 14 32 46 = true := by decide
theorem checkedRow47 : rowCheck 14 32 47 = true := by decide
theorem checkedRow48 : rowCheck 14 32 48 = true := by decide
theorem checkedRow49 : rowCheck 14 32 49 = true := by decide
theorem checkedRow50 : rowCheck 14 32 50 = true := by decide
theorem checkedRow51 : rowCheck 14 32 51 = true := by decide
theorem checkedRow52 : rowCheck 14 32 52 = true := by decide
theorem checkedRow53 : rowCheck 14 32 53 = true := by decide
theorem checkedRow54 : rowCheck 14 32 54 = true := by decide
theorem checkedRow55 : rowCheck 14 32 55 = true := by decide
theorem checkedRow56 : rowCheck 14 32 56 = true := by decide
theorem checkedRow57 : rowCheck 14 32 57 = true := by decide
theorem checkedRow58 : rowCheck 14 32 58 = true := by decide
theorem checkedRow59 : rowCheck 14 32 59 = true := by decide
theorem checkedRow60 : rowCheck 14 32 60 = true := by decide
theorem checkedRow61 : rowCheck 14 32 61 = true := by decide
theorem checkedRow62 : rowCheck 14 32 62 = true := by decide

theorem allCritical14_verified : allCritical 14 63 32 = true := by
  simp only [allCritical, List.range_succ, List.range_zero, List.all_append,
    List.all_cons, List.all_nil, checkedRow0, checkedRow1, checkedRow2, checkedRow3, checkedRow4, checkedRow5, checkedRow6, checkedRow7, checkedRow8, checkedRow9, checkedRow10, checkedRow11, checkedRow12, checkedRow13, checkedRow14, checkedRow15, checkedRow16, checkedRow17, checkedRow18, checkedRow19, checkedRow20, checkedRow21, checkedRow22, checkedRow23, checkedRow24, checkedRow25, checkedRow26, checkedRow27, checkedRow28, checkedRow29, checkedRow30, checkedRow31, checkedRow32, checkedRow33, checkedRow34, checkedRow35, checkedRow36, checkedRow37, checkedRow38, checkedRow39, checkedRow40, checkedRow41, checkedRow42, checkedRow43, checkedRow44, checkedRow45, checkedRow46, checkedRow47, checkedRow48, checkedRow49, checkedRow50, checkedRow51, checkedRow52, checkedRow53, checkedRow54, checkedRow55, checkedRow56, checkedRow57, checkedRow58, checkedRow59, checkedRow60, checkedRow61, checkedRow62, Bool.true_and]

/-- The actual two one-step reducts of every descending triple join by
literal presentation rewrites. No confluence or group structure is assumed. -/
theorem rank14_critical_pairs_join (a b c : ℕ) (ha : a < 63)
    (hb : b ≤ a) (hc : c ≤ b) :
    ∃ t, Relation.ReflTransGen (Step 14) (leftBranch 14 a b c) t ∧
      Relation.ReflTransGen (Step 14) (rightBranch 14 a b c) t :=
  allCritical_sound 14 63 32 allCritical14_verified a b c ha hb hc

def sourceInner (k : ℕ) : Word :=
  (List.replicate k [1, 2]).flatten ++ (List.replicate k [0, 1]).flatten

def sourceWord (k : ℕ) : Word := sourceInner k ++ sourceInner k

def allSourceWords : Bool :=
  (List.range 8).all fun k => collect 3 256 (sourceWord k) == []

theorem allSourceWords_verified : allSourceWords = true := by
  decide

/-- Each actual label-eight consecutive-triple word reduces to the empty
word using the rank-three presentation rules. -/
theorem rank3_source_word_reduces (k : ℕ) (hk : k < 8) :
    Relation.ReflTransGen (Step 3) (sourceWord k) [] := by
  have hall := allSourceWords_verified
  unfold allSourceWords at hall
  have h := List.all_eq_true.mp hall k (List.mem_range.mpr hk)
  have he : collect 3 256 (sourceWord k) = [] := by
    simpa only [beq_iff_eq] using h
  simpa only [he] using collect_reachable 3 256 (sourceWord k)

#print axioms allCritical_sound
#print axioms allCritical14_verified
#print axioms rank14_critical_pairs_join
#print axioms allSourceWords_verified
#print axioms rank3_source_word_reduces

end MathCompression.LabelEightCriticalPairs
