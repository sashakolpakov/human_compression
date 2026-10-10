import Mathlib.Tactic

/-!
Actual positive rewrite steps for the uniform label-eight presentation.
Finite joinability is checked by the kernel. The all-rank termination and
support-compression arguments are separate written results.
-/

namespace MathCompression.LabelEightCriticalPairs

abbrev Word := List ℕ

def decode (d a : ℕ) : ℕ × ℕ :=
  if a < d then (0, a)
  else if a < 2 * d - 1 then (1, a - d)
  else if a < 3 * d - 3 then (2, a - (2 * d - 1))
  else if a < 4 * d - 6 then (3, a - (3 * d - 3))
  else (4, a - (4 * d - 6))

def x (d i : ℕ) := d + i

def y (d i : ℕ) := 2 * d - 1 + i

def z (d i : ℕ) := 3 * d - 3 + i

def w (d i : ℕ) := 4 * d - 6 + i

def correction (d a b : ℕ) : Word :=
  match decode d a, decode d b with
  | (0, i), (0, j) => if i = j + 1 then [x d j, w d j] else []
  | (1, i), (0, j) =>
      if j = i ∨ j = i + 1 then [w d i]
      else if j = i + 2 then [y d i]
      else if j + 1 = i then [y d j, w d j, w d i]
      else []
  | (1, i), (1, j) =>
      if i = j + 1 then [w d j, w d i]
      else if i = j + 2 then [z d j]
      else []
  | (2, i), (0, j) =>
      if j + 1 = i then [z d j]
      else if j = i + 1 then [w d i, w d (i + 1)]
      else if j = i + 3 then [z d i]
      else []
  | _, _ => []

def rule (d a b : ℕ) : Word :=
  if a = b then
    if (decode d a).1 = 1 then [w d (decode d a).2] else []
  else b :: a :: correction d a b

/-- A literal contextual instance of one oriented presentation relation. -/
inductive Step (d : ℕ) : Word → Word → Prop
  | apply (pre post : Word) (a b : ℕ) (h : b ≤ a) :
      Step d (pre ++ a :: b :: post) (pre ++ rule d a b ++ post)

theorem Step.cons {d : ℕ} {u v : Word} (h : Step d u v) (a : ℕ) :
    Step d (a :: u) (a :: v) := by
  cases h with
  | apply pre post b c h =>
    simpa only [List.cons_append] using Step.apply (a :: pre) post b c h

/-- Choose the leftmost reducible pair, without assuming confluence. -/
def next (d : ℕ) : Word → Option Word
  | [] => none
  | [_] => none
  | a :: b :: rest =>
      if b ≤ a then some (rule d a b ++ rest)
      else (next d (b :: rest)).map (a :: ·)

theorem next_sound (d : ℕ) (u v : Word) (h : next d u = some v) : Step d u v := by
  induction u generalizing v with
  | nil => simp [next] at h
  | cons a tail ih =>
    cases tail with
    | nil => simp [next] at h
    | cons b rest =>
      by_cases hab : b ≤ a
      · simp only [next, if_pos hab, Option.some.injEq] at h
        subst v
        simpa using Step.apply [] rest a b hab
      · simp only [next, if_neg hab] at h
        cases hn : next d (b :: rest) with
        | none => simp [hn] at h
        | some t =>
          have hv : a :: t = v := by simpa [hn] using h
          subst v
          exact (ih t hn).cons a

/-- A bounded collector. Reachability does not require sufficient fuel. -/
def collect (d : ℕ) : ℕ → Word → Word
  | 0, u => u
  | fuel + 1, u =>
      match next d u with
      | none => u
      | some v => collect d fuel v

theorem collect_reachable (d fuel : ℕ) (u : Word) :
    Relation.ReflTransGen (Step d) u (collect d fuel u) := by
  induction fuel generalizing u with
  | zero => exact .refl
  | succ fuel ih =>
    cases hn : next d u with
    | none => simpa [collect, hn] using (Relation.ReflTransGen.refl : Relation.ReflTransGen (Step d) u u)
    | some v =>
      simpa [collect, hn] using (Relation.ReflTransGen.single (next_sound d u v hn)).trans (ih v)

def leftBranch (d a b c : ℕ) : Word := rule d a b ++ [c]

def rightBranch (d a b c : ℕ) : Word := a :: rule d b c

def criticalCheck (d fuel a b c : ℕ) : Bool :=
  collect d fuel (leftBranch d a b c) == collect d fuel (rightBranch d a b c)

theorem criticalCheck_sound (d fuel a b c : ℕ) (h : criticalCheck d fuel a b c = true) :
    ∃ t, Relation.ReflTransGen (Step d) (leftBranch d a b c) t ∧
      Relation.ReflTransGen (Step d) (rightBranch d a b c) t := by
  have he : collect d fuel (leftBranch d a b c) = collect d fuel (rightBranch d a b c) := by
    simpa only [criticalCheck, beq_iff_eq] using h
  refine ⟨collect d fuel (leftBranch d a b c), collect_reachable _ _ _, ?_⟩
  rw [he]
  exact collect_reachable _ _ _

#print axioms next_sound
#print axioms collect_reachable
#print axioms criticalCheck_sound

end MathCompression.LabelEightCriticalPairs
