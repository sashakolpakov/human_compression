import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.Data.Finset.Card

/-!
The abstract reconstruction used in the Livingstone-graph audit. This file
formalizes the reduction from invariant binary incidence to a diagonal orbit,
including the finite neighbour-count criterion. It contains no J1 data and
does not formalize either complete source polytope or the finite GAP run.
-/

namespace HumanCompression.EquivariantIncidence

variable {G X Y : Type*} [Group G] [MulAction G X] [MulAction G Y]

theorem reconstruction
    (R : X → Y → Prop) (x₀ : X) (y₀ : Y)
    (invariant : ∀ (g : G) (x : X) (y : Y), R x y → R (g • x) (g • y))
    (base : R x₀ y₀)
    (transitive : ∀ x : X, ∃ g : G, g • x₀ = x)
    (neighbours : ∀ y : Y, R x₀ y ↔
      ∃ h : G, h • x₀ = x₀ ∧ h • y₀ = y)
    (x : X) (y : Y) :
    R x y ↔ ∃ g : G, g • x₀ = x ∧ g • y₀ = y := by
  constructor
  · intro hxy
    obtain ⟨g, rfl⟩ := transitive x
    have hlocal : R x₀ (g⁻¹ • y) := by
      simpa using invariant g⁻¹ (g • x₀) y hxy
    obtain ⟨h, hx, hy⟩ := (neighbours _).mp hlocal
    refine ⟨g * h, ?_, ?_⟩
    · simp [mul_smul, hx]
    · rw [mul_smul, hy]
      simp
  · rintro ⟨g, rfl, rfl⟩
    exact invariant g x₀ y₀ base

noncomputable def localOrbit [Fintype Y] (x₀ : X) (y₀ : Y) : Finset Y := by
  classical
  exact Finset.univ.filter (fun y => ∃ h : G, h • x₀ = x₀ ∧ h • y₀ = y)

noncomputable def localNeighbours [Fintype Y] (R : X → Y → Prop) (x₀ : X) :
    Finset Y := by
  classical
  exact Finset.univ.filter (R x₀)

theorem localOrbit_subset [Fintype Y]
    (R : X → Y → Prop) (x₀ : X) (y₀ : Y)
    (invariant : ∀ (g : G) (x : X) (y : Y), R x y → R (g • x) (g • y))
    (base : R x₀ y₀) :
    localOrbit (G := G) x₀ y₀ ⊆ localNeighbours R x₀ := by
  classical
  intro y hy
  obtain ⟨h, hx, hy'⟩ : ∃ h : G, h • x₀ = x₀ ∧ h • y₀ = y := by
    simpa [localOrbit] using hy
  have h := invariant h x₀ y₀ base
  simpa [localNeighbours, hx, hy'] using h

theorem reconstruction_of_card [Fintype Y]
    (R : X → Y → Prop) (x₀ : X) (y₀ : Y)
    (invariant : ∀ (g : G) (x : X) (y : Y), R x y → R (g • x) (g • y))
    (base : R x₀ y₀)
    (transitive : ∀ x : X, ∃ g : G, g • x₀ = x)
    (cardinality : (localNeighbours R x₀).card = (localOrbit (G := G) x₀ y₀).card)
    (x : X) (y : Y) :
    R x y ↔ ∃ g : G, g • x₀ = x ∧ g • y₀ = y := by
  classical
  have heq : localOrbit (G := G) x₀ y₀ = localNeighbours R x₀ :=
    Finset.eq_of_subset_of_card_le (localOrbit_subset R x₀ y₀ invariant base)
      (Nat.le_of_eq cardinality)
  apply reconstruction R x₀ y₀ invariant base transitive
  intro z
  have hm : z ∈ localNeighbours R x₀ ↔ z ∈ localOrbit (G := G) x₀ y₀ := by rw [heq]
  simpa [localNeighbours, localOrbit] using hm

#print axioms reconstruction
#print axioms localOrbit_subset
#print axioms reconstruction_of_card

end HumanCompression.EquivariantIncidence
