import Mathlib.Tactic

/-!
A marked-isomorphism obstruction over the complete bipartite incidence graph.
This formalizes the factor obstruction and universal coset intersections; it does
not import or assume a classification of graph automorphism groups.
-/

namespace MathCompression.RankTwoMarkedCounterexample

abbrev C4 := Multiplicative (ZMod 4)
abbrev V4 := Multiplicative (ZMod 2) × Multiplicative (ZMod 2)
abbrev G := C4 × V4

def leftFactor : Subgroup G where
  carrier := {g | g.2 = 1}
  one_mem' := rfl
  mul_mem' := by intro a b ha hb; simp_all
  inv_mem' := by intro a ha; simp_all

def rightFactor : Subgroup G where
  carrier := {g | g.1 = 1}
  one_mem' := rfl
  mul_mem' := by intro a b ha hb; simp_all
  inv_mem' := by intro a ha; simp_all

def quarterTurn : G := (Multiplicative.ofAdd (1 : ZMod 4), 1)

theorem klein_square (v : V4) : v * v = 1 := by
  revert v
  decide

theorem quarterTurn_square_ne_one : quarterTurn * quarterTurn ≠ 1 := by decide

theorem quarterTurn_in_left : quarterTurn ∈ leftFactor := rfl

theorem no_marked_swap (f : G ≃* G) :
    ¬ (∀ g ∈ leftFactor, f g ∈ rightFactor) := by
  intro h
  have hf : (f quarterTurn).1 = 1 := h quarterTurn quarterTurn_in_left
  have hsq : f quarterTurn * f quarterTurn = 1 := by
    apply Prod.ext
    · simpa using congrArg (fun x : C4 => x * x) hf
    · exact klein_square _
  apply quarterTurn_square_ne_one
  apply f.injective
  simpa using hsq

/-- The two factor stabilizers have trivial intersection. -/
theorem factor_intersection : leftFactor ⊓ rightFactor = ⊥ := by
  ext g
  change (g.2 = 1 ∧ g.1 = 1) ↔ g = 1
  constructor
  · intro h; exact Prod.ext h.2 h.1
  · intro h; simp [h]

/-- Every left coset of the first factor meets every left coset of the second.
The witnesses exhibit the complete bipartite incidence relation explicitly. -/
theorem every_factor_coset_pair_meets (g h : G) :
    ∃ a ∈ leftFactor, ∃ b ∈ rightFactor, g * a = h * b := by
  refine ⟨(g.1⁻¹ * h.1, 1), rfl, (1, h.2⁻¹ * g.2), rfl, ?_⟩
  apply Prod.ext <;> simp

theorem factor_sizes : Fintype.card C4 = 4 ∧ Fintype.card V4 = 4 := by decide

#print axioms no_marked_swap
#print axioms factor_intersection
#print axioms every_factor_coset_pair_meets
#print axioms factor_sizes

end MathCompression.RankTwoMarkedCounterexample
