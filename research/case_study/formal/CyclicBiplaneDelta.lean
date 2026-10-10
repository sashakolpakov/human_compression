import Mathlib.Tactic

/-! A literal 11-point cyclic counterexample to the unrestricted implication
in L092 Lemma 3(1). Both proper-triangle neighbour graphs are connected,
but the Construction 3 residue at (1,D) is four isolated point objects. -/

namespace MathCompression.CyclicBiplaneDelta

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

abbrev Point := ZMod 11
def D : Finset Point := {1, 3, 4, 5, 9}
def incident (x a : Point) : Prop := x - a ∈ D
instance (x a : Point) : Decidable (incident x a) := inferInstanceAs (Decidable (_ ∈ _))

def near (p x y : Point) : Prop :=
  p ≠ x ∧ p ≠ y ∧ x ≠ y ∧
  (∃ a, incident p a ∧ incident x a) ∧
  (∃ a, incident p a ∧ incident y a) ∧
  (∃ a, incident x a ∧ incident y a) ∧
  ¬ ∃ a, incident p a ∧ incident x a ∧ incident y a
instance (p x y : Point) : Decidable (near p x y) := by unfold near; infer_instance

def dualNear (p x y : Point) : Prop :=
  p ≠ x ∧ p ≠ y ∧ x ≠ y ∧
  (∃ a, incident a p ∧ incident a x) ∧
  (∃ a, incident a p ∧ incident a y) ∧
  (∃ a, incident a x ∧ incident a y) ∧
  ¬ ∃ a, incident a p ∧ incident a x ∧ incident a y
instance (p x y : Point) : Decidable (dualNear p x y) := by unfold dualNear; infer_instance

theorem thick_and_pairwise_collinear :
    (∀ a : Point, (Finset.univ.filter (fun x => incident x a)).card = 5) ∧
    (∀ x : Point, (Finset.univ.filter (fun a => incident x a)).card = 5) ∧
    (∀ x y : Point, ∃ a, incident x a ∧ incident y a) := by decide

theorem intersection_sizes : ∀ a b : Point,
    (Finset.univ.filter (fun x => incident x a ∧ incident x b)).card =
      if a = b then 5 else 2 := by decide

theorem primal_distance_two : ∀ p x y : Point, x ≠ p → y ≠ p →
    x = y ∨ near p x y ∨ ∃ z, near p x z ∧ near p z y := by decide

theorem dual_distance_two : ∀ p x y : Point, x ≠ p → y ≠ p →
    x = y ∨ dualNear p x y ∨ ∃ z, dualNear p x z ∧ dualNear p z y := by decide

private theorem reachable_of_two {α : Type*} {R : α → α → Prop} {x y : α}
    (h : x = y ∨ R x y ∨ ∃ z, R x z ∧ R z y) : Relation.ReflTransGen R x y := by
  rcases h with h | h | ⟨z, h₁, h₂⟩
  · subst y; exact .refl
  · exact .single h
  · exact (Relation.ReflTransGen.single h₁).trans (.single h₂)

theorem both_delta_connected :
    (∀ p x y : Point, x ≠ p → y ≠ p → Relation.ReflTransGen (near p) x y) ∧
    (∀ p x y : Point, x ≠ p → y ≠ p → Relation.ReflTransGen (dualNear p) x y) := by
  constructor
  · intro p x y hx hy
    exact reachable_of_two (primal_distance_two p x y hx hy)
  · intro p x y hx hy
    exact reachable_of_two (dual_distance_two p x y hx hy)

/-- This is the source's singleton-intersection condition, literally. -/
def flagLine (p a b : Point) : Prop := ∀ x, incident x a ∧ incident x b ↔ x = p
instance (p a b : Point) : Decidable (flagLine p a b) := by unfold flagLine; infer_instance

theorem no_flag_line : ∀ p a b : Point, ¬ flagLine p a b := by decide
theorem residue_point_set : ∀ x : Point,
    incident x 0 ∧ x ≠ 1 ↔ x ∈ ({3,4,5,9} : Finset Point) := by decide

abbrev ResiduePoint := {x : Point // incident x 0 ∧ x ≠ 1}
abbrev ResidueLine := {b : Point // flagLine 1 0 b}
abbrev ResidueVertex := ResiduePoint ⊕ ResidueLine

def residueAdj : ResidueVertex → ResidueVertex → Prop
  | .inl x, .inr b => ¬ incident x.val b.val
  | .inr b, .inl x => ¬ incident x.val b.val
  | _, _ => False

theorem no_residue_edge (u v : ResidueVertex) : ¬ residueAdj u v := by
  cases u with
  | inl x =>
    cases v with
    | inl y => exact id
    | inr b => exact False.elim (no_flag_line 1 0 b.val b.property)
  | inr b => exact False.elim (no_flag_line 1 0 b.val b.property)

def three : ResidueVertex := .inl ⟨3, by decide⟩
def four : ResidueVertex := .inl ⟨4, by decide⟩

theorem residue_not_connected :
    ¬ ∀ u v : ResidueVertex, Relation.ReflTransGen residueAdj u v := by
  intro h
  have heq : ∀ u v, Relation.ReflTransGen residueAdj u v → u = v := by
    intro u v huv
    induction huv with
    | refl => rfl
    | tail _ edge _ => exact False.elim (no_residue_edge _ _ edge)
  have hn : three ≠ four := by decide
  exact hn (heq three four (h three four))

#print axioms thick_and_pairwise_collinear
#print axioms intersection_sizes
#print axioms both_delta_connected
#print axioms no_flag_line
#print axioms residue_point_set
#print axioms residue_not_connected

end MathCompression.CyclicBiplaneDelta
