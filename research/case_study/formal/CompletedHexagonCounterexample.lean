import Mathlib.Tactic

/-!
The completed graph in Díaz Ramos--Molinier--Viruel, arXiv:2511.02410v2,
Example 5.1. A base hexagon carries alternating colors zero and one; a
color-two tip completes each hexagon edge to a triangle.

The explicit type-preserving reflection has order two. Consequently the
type-preserving automorphism group cannot be C3, as printed in the source.
This file does not count the entire automorphism group or formalize the
general representation construction.
-/

namespace MathCompression.CompletedHexagonCounterexample

abbrev Index := ZMod 6
abbrev Vertex := Index ⊕ Index

def adjacent : Vertex → Vertex → Prop
  | .inl i, .inl j => j = i + 1 ∨ i = j + 1
  | .inl i, .inr j => i = j ∨ i = j + 1
  | .inr i, .inl j => j = i ∨ j = i + 1
  | .inr _, .inr _ => False

instance (v w : Vertex) : Decidable (adjacent v w) := by
  cases v <;> cases w <;> unfold adjacent <;> infer_instance

def color : Vertex → ℕ
  | .inl i => i.val % 2
  | .inr _ => 2

def reflect : Vertex → Vertex
  | .inl i => .inl (-i)
  | .inr i => .inr (-i - 1)

theorem reflect_involutive : Function.Involutive reflect := by
  show ∀ v, reflect (reflect v) = v
  decide

def reflection : Equiv.Perm Vertex :=
  ⟨reflect, reflect, reflect_involutive, reflect_involutive⟩

theorem reflection_preserves_adjacency (v w : Vertex) :
    adjacent (reflection v) (reflection w) ↔ adjacent v w := by
  revert v w
  decide

theorem reflection_preserves_color (v : Vertex) :
    color (reflection v) = color v := by
  revert v
  decide

theorem reflection_ne_one : reflection ≠ 1 := by
  intro h
  have he := congrArg (fun f : Equiv.Perm Vertex => f (.inl 1)) h
  have hn : reflection (.inl 1) ≠ (1 : Equiv.Perm Vertex) (.inl 1) := by decide
  exact hn he

theorem reflection_square : reflection * reflection = 1 := by
  ext v
  exact reflect_involutive v

theorem reflection_order : orderOf reflection = 2 := by
  apply orderOf_eq_prime
  · simpa [pow_two] using reflection_square
  · exact reflection_ne_one

theorem cyclic_three_has_no_nontrivial_involution
    (g : Multiplicative (ZMod 3)) (h : g * g = 1) : g = 1 := by
  revert g
  decide

#print axioms reflection_preserves_adjacency
#print axioms reflection_preserves_color
#print axioms reflection_order
#print axioms cyclic_three_has_no_nontrivial_involution

end MathCompression.CompletedHexagonCounterexample
