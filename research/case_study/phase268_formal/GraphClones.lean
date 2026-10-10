import Mathlib.Logic.Relation

namespace GraphClones

variable {V F : Type*}

def adj (R : V → V → Prop) (x y : V × F) : Prop := R x.1 y.1

theorem lift_fixed_fiber (R : V → V → Prop) (a : F) {v w : V}
    (h : Relation.ReflTransGen R v w) :
    Relation.ReflTransGen (adj R) (v, a) (w, a) := by
  induction h with
  | refl => exact .refl
  | tail _ step ih => exact ih.tail step

theorem same_fiber_reachable (R : V → V → Prop) (hR : ∀ {v w}, R v w → R w v)
    (v : V) (h : ∃ w, R v w) (a b : F) :
    Relation.ReflTransGen (adj R) (v, a) (v, b) := by
  obtain ⟨w, hw⟩ := h
  have first : adj R (v, a) (w, b) := hw
  have second : adj R (w, b) (v, b) := hR hw
  exact (Relation.ReflTransGen.single first).trans (.single second)

theorem lift_reachability (R : V → V → Prop) (hR : ∀ {v w}, R v w → R w v)
    (hN : ∀ v, ∃ w, R v w) (x y : V × F)
    (h : Relation.ReflTransGen R x.1 y.1) :
    Relation.ReflTransGen (adj R) x y := by
  exact (same_fiber_reachable R hR x.1 (hN x.1) x.2 y.2).trans
    (lift_fixed_fiber R y.2 h)

theorem preserves_connectedness (R : V → V → Prop) (hR : ∀ {v w}, R v w → R w v)
    (hN : ∀ v, ∃ w, R v w)
    (h : ∀ v w, Relation.ReflTransGen R v w) :
    ∀ x y : V × F, Relation.ReflTransGen (adj R) x y := by
  intro x y
  exact lift_reachability R hR hN x y (h x.1 y.1)

#print axioms lift_fixed_fiber
#print axioms same_fiber_reachable
#print axioms lift_reachability
#print axioms preserves_connectedness
end GraphClones
