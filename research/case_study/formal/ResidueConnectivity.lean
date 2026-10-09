import Mathlib.Logic.Relation
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.GroupTheory.GroupAction.Defs

/-!
Undirected reachability from generating moves on a transitive group action.
The application to a Hermitian unital supplies the action, its transitivity,
and the generating unipotents geometrically; those identifications are not
asserted as formalized by this file.
-/

namespace LeemansConnectivity

variable {G X : Type*} [Group G] [MulAction G X]

/-- If moves by a generating set can be joined by graph paths, and the group
action is transitive, then any two vertices can be joined by a graph path.
Neither finiteness nor freeness of the action is required. -/
theorem connected_of_generating_moves (R : X → X → Prop) (S : Set G)
    (hgen : Subgroup.closure S = ⊤)
    (htrans : ∀ x y : X, ∃ g : G, g • x = y)
    (hstep : ∀ g ∈ S, ∀ x : X, Relation.EqvGen R x (g • x)) :
    ∀ x y : X, Relation.EqvGen R x y := by
  have hreach (g : G) : ∀ x : X, Relation.EqvGen R x (g • x) := by
    have hg : g ∈ Subgroup.closure S := by rw [hgen]; trivial
    refine Subgroup.closure_induction
      (p := fun g _ => ∀ x : X, Relation.EqvGen R x (g • x)) ?_ ?_ ?_ ?_ hg
    · intro a ha
      exact hstep a ha
    · intro x
      simpa using Relation.EqvGen.refl x
    · intro a b _ _ ha hb x
      simpa [mul_smul] using Relation.EqvGen.trans _ _ _ (hb x) (ha (b • x))
    · intro a _ ha x
      have h : Relation.EqvGen R (a⁻¹ • x) x := by
        simpa using ha (a⁻¹ • x)
      exact Relation.EqvGen.symm _ _ h
  intro x y
  obtain ⟨g, hg⟩ := htrans x y
  simpa [hg] using hreach g x

#print axioms connected_of_generating_moves

end LeemansConnectivity
