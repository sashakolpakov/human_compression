import Mathlib.GroupTheory.PresentedGroup
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Tactic

namespace MathCompression.Phase32Voltage

variable {A Q : Type*}
abbrev Letter (A : Type*) := A × Bool

def word {H : Type*} [Group H] (f : A → H) : List (Letter A) → H
  | [] => 1
  | (a, positive) :: w => (if positive then f a else (f a)⁻¹) * word f w

def step (forward backward : A → Q → Q) (v : A → Q → ℤ)
    (l : Letter A) (i : Q) : Q × ℤ :=
  if l.2 then (forward l.1 i, v l.1 i)
  else (backward l.1 i, -v l.1 (backward l.1 i))

def walk (forward backward : A → Q → Q) (v : A → Q → ℤ) :
    List (Letter A) → Q → Q × ℤ
  | [], i => (i, 0)
  | l :: w, i =>
    let a := step forward backward v l i
    let b := walk forward backward v w a.1
    (b.1, a.2 + b.2)

def affine (forward backward : A → Q → Q) (v : A → Q → ℤ)
    (h : ∀ a i, backward a (forward a i) = i ∧ forward a (backward a i) = i)
    (a : A) : Equiv.Perm (Q × ℤ) where
  toFun u := (forward a u.1, u.2 + v a u.1)
  invFun u := (backward a u.1, u.2 - v a (backward a u.1))
  left_inv := by
    rintro ⟨i, n⟩
    simp only [h]
    congr 1
    omega
  right_inv := by
    rintro ⟨i, n⟩
    simp only [h, sub_add_cancel]

def generator (forward backward : A → Q → Q) (v : A → Q → ℤ)
    (h : ∀ a i, backward a (forward a i) = i ∧ forward a (backward a i) = i)
    (a : A) : (Equiv.Perm (Q × ℤ))ᵐᵒᵖ :=
  MulOpposite.op (affine forward backward v h a)

theorem word_action (forward backward : A → Q → Q) (v : A → Q → ℤ)
    (h : ∀ a i, backward a (forward a i) = i ∧ forward a (backward a i) = i)
    (w : List (Letter A)) (i : Q) (n : ℤ) :
    MulOpposite.unop (word (generator forward backward v h) w) (i, n) =
      ((walk forward backward v w i).1, n + (walk forward backward v w i).2) := by
  induction w generalizing i n with
  | nil => simp [word, walk]
  | cons l w ih =>
    rcases l with ⟨a, positive⟩
    cases positive <;>
      simp [word, generator, affine, step, walk, MulOpposite.unop_mul,
        Equiv.Perm.mul_apply, ih, sub_eq_add_neg, add_assoc]

theorem lift_word {H : Type*} [Group H] (f : A → H) (w : List (Letter A)) :
    FreeGroup.lift f (word FreeGroup.of w) = word f w := by
  induction w with
  | nil => simp [word]
  | cons l w ih =>
    rcases l with ⟨a, positive⟩
    cases positive <;> simp [word, ih]

def relSet {I : Type*} (relations : I → List (Letter A)) : Set (FreeGroup A) :=
  Set.range (fun i => word FreeGroup.of (relations i))

theorem infinite_of_voltage_witness {I : Type*}
    (forward backward : A → Q → Q) (v : A → Q → ℤ)
    (h : ∀ a i, backward a (forward a i) = i ∧ forward a (backward a i) = i)
    (relations : I → List (Letter A))
    (hr : ∀ j i, walk forward backward v (relations j) i = (i, 0))
    (w : List (Letter A)) (q : Q)
    (hw : walk forward backward v w q = (q, -1)) :
    Infinite (PresentedGroup (relSet relations)) := by
  let f := generator forward backward v h
  have valid : ∀ r ∈ relSet relations, FreeGroup.lift f r = 1 := by
    intro r hrmem
    obtain ⟨j, rfl⟩ := hrmem
    rw [lift_word]
    apply MulOpposite.unop_injective
    apply Equiv.ext
    rintro ⟨i, n⟩
    change MulOpposite.unop (word f (relations j)) (i, n) = (i, n)
    simpa only [hr, Prod.fst, Prod.snd, add_zero] using
      word_action forward backward v h (relations j) i n
  let hom := PresentedGroup.toGroup valid
  let g : PresentedGroup (relSet relations) :=
    PresentedGroup.mk _ (word FreeGroup.of w)
  have hg : hom g = word f w := by
    change FreeGroup.lift f (word FreeGroup.of w) = word f w
    exact lift_word f w
  have hg_action (n : ℤ) : MulOpposite.unop (hom g) (q, n) = (q, n - 1) := by
    rw [hg]
    simpa only [hw, Prod.fst, Prod.snd, sub_eq_add_neg] using
      word_action forward backward v h w q n
  have hp (n : ℕ) : MulOpposite.unop (hom (g ^ n)) (q, 0) = (q, -(n : ℤ)) := by
    induction n with
    | zero => simp
    | succ n ih =>
      rw [pow_succ, map_mul, MulOpposite.unop_mul, Equiv.Perm.mul_apply, ih, hg_action]
      simp only [Nat.cast_add, Nat.cast_one]
      congr 1
      omega
  apply Infinite.of_injective (fun n : ℕ => g ^ n)
  intro m n heq
  have hh := congrArg (fun u => (MulOpposite.unop (hom u) (q, 0)).2) heq
  simpa only [hp, Prod.snd, neg_inj, Nat.cast_inj] using hh

#print axioms infinite_of_voltage_witness
end MathCompression.Phase32Voltage
