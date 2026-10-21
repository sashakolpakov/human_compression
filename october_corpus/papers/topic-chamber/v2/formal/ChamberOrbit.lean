import Mathlib.Logic.Relation
import Mathlib.GroupTheory.GroupAction.Defs

/-!
Generic chamber-orbit arguments.  This file does not define a coset geometry,
prove residual connectedness implies chamber connectedness, or instantiate
the hypotheses for Problem 9.3.  Those are separate mathematical arguments.
The action here is a left action; a right-action convention is equivalent
after replacing each acting element by its inverse.
-/

namespace LeemansChamberOrbit

variable {G X I : Type*} [Group G] [MulAction G X]

/-- Membership in the orbit of a chosen base chamber. -/
def InBaseOrbit (c x : X) : Prop := ∃ g : G, g • c = x

/-- A predicate preserved in both directions across edges is preserved by
undirected reachability, including reflexive paths. -/
theorem predicate_iff_of_path (R : X → X → Prop) (P : X → Prop)
    (hedge : ∀ x y, R x y → (P x ↔ P y))
    {x y : X} (hpath : Relation.EqvGen R x y) : P x ↔ P y := by
  induction hpath with
  | rel x y h => exact hedge x y h
  | refl x => exact Iff.rfl
  | symm x y _ ih => exact ih.symm
  | trans x y z _ _ hxy hyz => exact hxy.trans hyz

/-- If the base orbit is closed under a symmetric chamber adjacency and
every chamber is connected to the base, every chamber lies in that orbit. -/
theorem all_in_base_orbit_of_closed (R : X → X → Prop) (c : X)
    (hsymm : ∀ x y, R x y → R y x)
    (hconn : ∀ x, Relation.EqvGen R c x)
    (hclosed : ∀ x y, R x y → InBaseOrbit (G := G) c x →
      InBaseOrbit (G := G) c y) :
    ∀ x, InBaseOrbit (G := G) c x := by
  intro x
  have hedge : ∀ a b, R a b →
      (InBaseOrbit (G := G) c a ↔ InBaseOrbit (G := G) c b) := by
    intro a b hab
    exact ⟨hclosed a b hab, hclosed b a (hsymm a b hab)⟩
  have hc : InBaseOrbit (G := G) c c := ⟨1, one_smul G c⟩
  exact (predicate_iff_of_path R (InBaseOrbit (G := G) c) hedge (hconn x)).mp hc

/-- The usual two-point formulation of action transitivity follows from
membership of every point in a single base orbit. -/
theorem transitive_of_all_in_base_orbit (c : X)
    (hall : ∀ x, InBaseOrbit (G := G) c x) :
    ∀ x y : X, ∃ g : G, g • x = y := by
  intro x y
  obtain ⟨g, hg⟩ := hall x
  obtain ⟨h, hh⟩ := hall y
  refine ⟨h * g⁻¹, ?_⟩
  rw [← hg, mul_smul]
  simpa using hh

/-- It suffices to test orbit closure at the base when adjacency is
equivariant.  No freeness or faithfulness assumption is needed. -/
theorem orbit_closed_of_base_neighbors (R : X → X → Prop) (c : X)
    (hequiv : ∀ (g : G) x y, R x y → R (g • x) (g • y))
    (hbase : ∀ y, R c y → InBaseOrbit (G := G) c y) :
    ∀ x y, R x y → InBaseOrbit (G := G) c x →
      InBaseOrbit (G := G) c y := by
  intro x y hxy hx
  obtain ⟨g, hg⟩ := hx
  have hback : R c (g⁻¹ • y) := by
    have h := hequiv g⁻¹ x y hxy
    simpa [← hg] using h
  obtain ⟨k, hk⟩ := hbase (g⁻¹ • y) hback
  refine ⟨g * k, ?_⟩
  rw [mul_smul, hk]
  simp

/-- A unique base neighbor of each panel type, supplied by an element of
the acting group, forces transitivity on a connected chamber graph.

Only uniqueness at the base is required: equivariance transports it to the
base orbit, and connectivity then proves that this is the entire chamber set.
Adjacency irreflexivity is not needed for this abstract implication. -/
theorem transitive_of_unique_panel_mates (Adj : I → X → X → Prop)
    (c : X) (r : I → G)
    (hsymm : ∀ i x y, Adj i x y → Adj i y x)
    (hequiv : ∀ (g : G) i x y, Adj i x y → Adj i (g • x) (g • y))
    (hmate : ∀ i, Adj i c (r i • c))
    (hunique : ∀ i x y, Adj i c x → Adj i c y → x = y)
    (hconn : ∀ x, Relation.EqvGen (fun a b => ∃ i, Adj i a b) c x) :
    ∀ x y : X, ∃ g : G, g • x = y := by
  let R : X → X → Prop := fun a b => ∃ i, Adj i a b
  have hRsymm : ∀ x y, R x y → R y x := by
    intro x y h
    obtain ⟨i, hi⟩ := h
    exact ⟨i, hsymm i x y hi⟩
  have hRequiv : ∀ (g : G) x y, R x y → R (g • x) (g • y) := by
    intro g x y h
    obtain ⟨i, hi⟩ := h
    exact ⟨i, hequiv g i x y hi⟩
  have hbase : ∀ y, R c y → InBaseOrbit (G := G) c y := by
    intro y h
    obtain ⟨i, hi⟩ := h
    exact ⟨r i, (hunique i y (r i • c) hi (hmate i)).symm⟩
  have hall : ∀ x, InBaseOrbit (G := G) c x :=
    all_in_base_orbit_of_closed R c hRsymm hconn
      (orbit_closed_of_base_neighbors R c hRequiv hbase)
  exact transitive_of_all_in_base_orbit c hall

#print axioms all_in_base_orbit_of_closed
#print axioms orbit_closed_of_base_neighbors
#print axioms transitive_of_unique_panel_mates

end LeemansChamberOrbit
