import Mathlib.Data.List.Shortlex
import Mathlib.Tactic

/-!
A well-founded, two-sided compatible block order on finite alphabets.
At each letter, blocks separated by that letter are compared in shortlex order;
the block entries use the order already constructed on higher letters.
-/

namespace MathCompression.TriangularWordTermination

abbrev Word := List ℕ

def lastMap {α : Type*} (f : α → α) : List α → List α
  | [] => []
  | [a] => [f a]
  | a :: b :: t => a :: lastMap f (b :: t)

@[simp] theorem lastMap_length {α : Type*} (f : α → α) (u : List α) :
    (lastMap f u).length = u.length := by
  induction u with
  | nil => rfl
  | cons a t ih => cases t <;> simp_all [lastMap]

theorem shortlex_head {α : Type*} {r : α → α → Prop} {f : α → α}
    (hf : ∀ a b, r a b → r (f a) (f b)) {u v : List α}
    (h : List.Shortlex r u v) :
    List.Shortlex r (u.modifyHead f) (v.modifyHead f) := by
  rcases List.shortlex_def.mp h with hlt | ⟨hlen, hlex⟩
  · exact List.Shortlex.of_length_lt (by simpa using hlt)
  · clear h
    apply List.Shortlex.of_lex (by simpa using hlen)
    cases hlex with
    | nil => simp at hlen
    | cons h => exact .cons h
    | rel h => exact .rel (hf _ _ h)

theorem lex_last {α : Type*} {r : α → α → Prop} {f : α → α}
    (hf : ∀ a b, r a b → r (f a) (f b)) {u v : List α}
    (hlen : u.length = v.length) (h : List.Lex r u v) :
    List.Lex r (lastMap f u) (lastMap f v) := by
  induction h with
  | nil => simp at hlen
  | @cons a u v h ih =>
    cases u with
    | nil => cases v <;> simp_all
    | cons b u =>
      cases v with
      | nil => simp at hlen
      | cons c v => exact .cons (ih (by simpa using hlen))
  | @rel a u b v h =>
    cases u with
    | nil =>
      cases v with
      | nil => exact .rel (hf _ _ h)
      | cons c v => simp at hlen
    | cons c u =>
      cases v with
      | nil => simp at hlen
      | cons e v => exact .rel h

theorem shortlex_last {α : Type*} {r : α → α → Prop} {f : α → α}
    (hf : ∀ a b, r a b → r (f a) (f b)) {u v : List α}
    (h : List.Shortlex r u v) :
    List.Shortlex r (lastMap f u) (lastMap f v) := by
  rcases List.shortlex_def.mp h with h | ⟨hlen, hlex⟩
  · exact List.Shortlex.of_length_lt (by simpa using h)
  · exact List.Shortlex.of_lex (by simpa using hlen) (lex_last hf hlen hlex)

theorem shortlex_cons {α : Type*} {r : α → α → Prop} {u v : List α}
    (h : List.Shortlex r u v) (a : α) : List.Shortlex r (a :: u) (a :: v) := by
  rcases List.shortlex_def.mp h with h | ⟨hlen, hlex⟩
  · exact List.Shortlex.of_length_lt (by simpa using h)
  · exact List.Shortlex.of_lex (by simpa using hlen) (.cons hlex)

theorem lex_snoc {α : Type*} {r : α → α → Prop} {u v : List α}
    (hlen : u.length = v.length) (h : List.Lex r u v) (a : α) :
    List.Lex r (u ++ [a]) (v ++ [a]) := by
  induction h with
  | nil => simp at hlen
  | cons h ih => exact .cons (ih (by simpa using hlen))
  | rel h => exact .rel h

theorem shortlex_snoc {α : Type*} {r : α → α → Prop} {u v : List α}
    (h : List.Shortlex r u v) (a : α) :
    List.Shortlex r (u ++ [a]) (v ++ [a]) := by
  rcases List.shortlex_def.mp h with h | ⟨hlen, hlex⟩
  · exact List.Shortlex.of_length_lt (by simpa using h)
  · exact List.Shortlex.of_lex (by simpa using hlen) (lex_snoc hlen hlex a)

def blocks (k : ℕ) : Word → List Word
  | [] => [[]]
  | a :: u => if a = k then [] :: blocks k u else (blocks k u).modifyHead (a :: ·)

theorem blocks_ne_nil (k : ℕ) (u : Word) : blocks k u ≠ [] := by
  induction u with
  | nil => simp [blocks]
  | cons a u ih =>
    simp only [blocks]
    split
    · simp
    · cases h : blocks k u <;> simp_all

theorem lastMap_cons {α : Type*} (f : α → α) (a : α) {u : List α} (h : u ≠ []) :
    lastMap f (a :: u) = a :: lastMap f u := by cases u <;> simp_all [lastMap]

theorem head_append {α : Type*} (f : α → α) {u : List α} (h : u ≠ []) (v : List α) :
    (u ++ v).modifyHead f = u.modifyHead f ++ v := by cases u <;> simp_all

theorem head_last_commute {α : Type*} (f g : α → α)
    (hfg : ∀ a, f (g a) = g (f a)) (u : List α) :
    (lastMap g u).modifyHead f = lastMap g (u.modifyHead f) := by
  cases u with
  | nil => rfl
  | cons a u => cases u <;> simp [lastMap, hfg]

theorem blocks_snoc (k : ℕ) (u : Word) (a : ℕ) :
    blocks k (u ++ [a]) =
      if a = k then blocks k u ++ [[]]
      else lastMap (fun w => w ++ [a]) (blocks k u) := by
  induction u with
  | nil => simp [blocks, lastMap]
  | cons b u ih =>
    simp only [List.cons_append, blocks, ih]
    by_cases hb : b = k <;> by_cases ha : a = k
    · simp [hb, ha]
    · simp [hb, ha, lastMap_cons _ _ (blocks_ne_nil k u)]
    · simp [hb, ha, head_append _ (blocks_ne_nil k u)]
    · simp only [hb, ha, if_false]
      exact head_last_commute _ _ (by intro; rfl) _

def BlockOrder (k : ℕ) : ℕ → Word → Word → Prop
  | 0 => fun _ _ => False
  | n + 1 => InvImage (List.Shortlex (BlockOrder (k + 1) n)) (blocks k)

theorem blockOrder_wf (k n : ℕ) : WellFounded (BlockOrder k n) := by
  induction n generalizing k with
  | zero => exact ⟨fun _ => .intro _ (by intro _ h; cases h)⟩
  | succ n ih => exact InvImage.wf (blocks k) (List.Shortlex.wf (ih (k + 1)))

theorem blockOrder_cons {k n : ℕ} {u v : Word} (h : BlockOrder k n u v) (a : ℕ) :
    BlockOrder k n (a :: u) (a :: v) := by
  induction n generalizing k u v a with
  | zero => exact h.elim
  | succ n ih =>
    change List.Shortlex (BlockOrder (k + 1) n) (blocks k (a :: u)) (blocks k (a :: v))
    change List.Shortlex (BlockOrder (k + 1) n) (blocks k u) (blocks k v) at h
    simp only [blocks]
    split
    · exact shortlex_cons h []
    · exact shortlex_head (fun _ _ h => ih h a) h

theorem blockOrder_snoc {k n : ℕ} {u v : Word} (h : BlockOrder k n u v) (a : ℕ) :
    BlockOrder k n (u ++ [a]) (v ++ [a]) := by
  induction n generalizing k u v a with
  | zero => exact h.elim
  | succ n ih =>
    change List.Shortlex (BlockOrder (k + 1) n) (blocks k (u ++ [a])) (blocks k (v ++ [a]))
    change List.Shortlex (BlockOrder (k + 1) n) (blocks k u) (blocks k v) at h
    rw [blocks_snoc, blocks_snoc]
    split
    · exact shortlex_snoc h []
    · exact shortlex_last (fun _ _ h => ih h a) h

theorem blockOrder_context {k n : ℕ} {u v : Word} (h : BlockOrder k n u v)
    (pre post : Word) : BlockOrder k n (pre ++ u ++ post) (pre ++ v ++ post) := by
  have hleft : BlockOrder k n (pre ++ u) (pre ++ v) := by
    induction pre with
    | nil => exact h
    | cons a pre ih => exact blockOrder_cons ih a
  induction post using List.reverseRecOn with
  | nil => simpa using hleft
  | append_singleton post a ih => simpa only [List.append_assoc] using blockOrder_snoc ih a

theorem blocks_of_no_separator {k : ℕ} {u : Word} (h : ∀ a ∈ u, a ≠ k) :
    blocks k u = [u] := by
  induction u with
  | nil => rfl
  | cons a u ih =>
    have ha : a ≠ k := h a (by simp)
    have hu : ∀ b ∈ u, b ≠ k := fun b hb => h b (by simp [hb])
    simp [blocks, ha, ih hu]

theorem blockOrder_lift {k n : ℕ} {u v : Word}
    (hu : ∀ a ∈ u, a ≠ k) (hv : ∀ a ∈ v, a ≠ k)
    (h : BlockOrder (k + 1) n u v) : BlockOrder k (n + 1) u v := by
  change List.Shortlex (BlockOrder (k + 1) n) (blocks k u) (blocks k v)
  rw [blocks_of_no_separator hu, blocks_of_no_separator hv, List.shortlex_singleton_iff]
  exact h

/-- Every letter in the active interval is strictly greater than the empty word. -/
theorem nil_lt_letter {k n a : ℕ} (hka : k ≤ a) (han : a < k + n) :
    BlockOrder k n [] [a] := by
  induction n generalizing k with
  | zero => omega
  | succ n ih =>
    by_cases hak : a = k
    · subst a
      change List.Shortlex (BlockOrder (k + 1) n) (blocks k []) (blocks k [k])
      apply List.Shortlex.of_length_lt
      simp [blocks]
    · apply blockOrder_lift (by simp) (by simpa using hak)
      exact ih (by omega) (by omega)

/-- Replacing a square by any word on strictly higher letters decreases the order. -/
theorem square_decreases {k n a : ℕ} {tail : Word}
    (hka : k ≤ a) (han : a < k + n) (htail : ∀ c ∈ tail, a < c) :
    BlockOrder k n tail [a, a] := by
  induction n generalizing k with
  | zero => omega
  | succ n ih =>
    have ht : ∀ c ∈ tail, c ≠ k := by intro c hc; have := htail c hc; omega
    by_cases hak : a = k
    · subst a
      change List.Shortlex (BlockOrder (k + 1) n) (blocks k tail) (blocks k [k, k])
      rw [blocks_of_no_separator ht]
      apply List.Shortlex.of_length_lt
      simp [blocks]
    · apply blockOrder_lift ht (by simpa using hak)
      exact ih (by omega) (by omega)

/-- Moving the smaller letter left decreases its preceding higher-letter block;
the new correction word lies entirely after that first strict decrease. -/
theorem swap_decreases {k n a b : ℕ} {tail : Word}
    (hkb : k ≤ b) (hba : b < a) (han : a < k + n)
    (htail : ∀ c ∈ tail, a < c) :
    BlockOrder k n (b :: a :: tail) [a, b] := by
  induction n generalizing k with
  | zero => omega
  | succ n ih =>
    have hak : a ≠ k := by omega
    have ht : ∀ c ∈ tail, c ≠ k := by intro c hc; have := htail c hc; omega
    by_cases hbk : b = k
    · subst b
      have hat : ∀ c ∈ a :: tail, c ≠ k := by simp_all
      change List.Shortlex (BlockOrder (k + 1) n)
        (blocks k (k :: a :: tail)) (blocks k [a, k])
      have hleft : blocks k (k :: a :: tail) = [[], a :: tail] := by
        rw [blocks, if_pos rfl, blocks_of_no_separator hat]
      have hright : blocks k [a, k] = [[a], []] := by simp [blocks, hak]
      rw [hleft, hright]
      apply List.Shortlex.of_lex (by simp)
      exact .rel (nil_lt_letter (by omega) (by omega))
    · apply blockOrder_lift (by simp_all) (by simp_all)
      exact ih (by omega) (by omega)

/-- A reusable triangular rewriting interface.  Higher tails need not satisfy a
length bound, and no confluence or pre-existing termination hypothesis occurs. -/
inductive TriangularStep (bound : ℕ) : Word → Word → Prop
  | square (pre post tail : Word) (a : ℕ) (ha : a < bound)
      (htail : ∀ c ∈ tail, a < c) :
      TriangularStep bound (pre ++ [a, a] ++ post) (pre ++ tail ++ post)
  | swap (pre post tail : Word) (a b : ℕ) (ha : a < bound) (hba : b < a)
      (htail : ∀ c ∈ tail, a < c) :
      TriangularStep bound (pre ++ [a, b] ++ post) (pre ++ b :: a :: tail ++ post)

theorem triangular_step_decreases {bound : ℕ} {u v : Word}
    (h : TriangularStep bound u v) : BlockOrder 0 bound v u := by
  cases h with
  | square pre post tail a ha ht =>
    exact blockOrder_context (square_decreases (Nat.zero_le _) (by simpa using ha) ht) pre post
  | swap pre post tail a b ha hba ht =>
    exact blockOrder_context (swap_decreases (Nat.zero_le _) hba (by simpa using ha) ht) pre post

theorem triangular_termination (bound : ℕ) :
    WellFounded (fun v u => TriangularStep bound u v) :=
  (blockOrder_wf 0 bound).mono fun _ _ h => triangular_step_decreases h

#print axioms blockOrder_wf
#print axioms blockOrder_context
#print axioms square_decreases
#print axioms swap_decreases
#print axioms triangular_termination

end MathCompression.TriangularWordTermination
