import Mathlib.Algebra.Group.Subgroup.Lattice

/-!
The algebraic fiber kernel of the component/monodromy argument.

The common fiber is an intersection of left cosets. Choosing one of its
points rebases it to the coset of the intersection subgroup. Connectivity
is represented here ONLY by the explicit coset relation x⁻¹*y ∈ H. Graph
walks and the identification of their monodromy with H remain written.
-/

namespace Phase29CosetMonodromy

variable {G I : Type*} [Group G]

def CommonFiber (g : I → G) (S : I → Subgroup G) : Set G :=
  {x | ∀ i, (g i)⁻¹ * x ∈ S i}

def SameMonodromyClass (H : Subgroup G) (x y : G) : Prop :=
  x⁻¹ * y ∈ H

/-- A nonempty indexed intersection of left cosets is the left coset of
the intersection subgroup through any chosen common point. -/
theorem common_fiber_rebased (g : I → G) (S : I → Subgroup G) (z : G)
    (hz : z ∈ CommonFiber g S) (x : G) :
    x ∈ CommonFiber g S ↔ z⁻¹ * x ∈ ⨅ i, S i := by
  constructor
  · intro hx
    apply Subgroup.mem_iInf.mpr
    intro i
    have h := (S i).mul_mem ((S i).inv_mem (hz i)) (hx i)
    simpa [mul_assoc] using h
  · intro hx i
    have h := (S i).mul_mem (hz i) (Subgroup.mem_iInf.mp hx i)
    simpa [mul_assoc] using h

/-- Set equality form of the common-fiber rebasing theorem. -/
theorem common_fiber_eq_coset (g : I → G) (S : I → Subgroup G) (z : G)
    (hz : z ∈ CommonFiber g S) :
    CommonFiber g S = {x | z⁻¹ * x ∈ ⨅ i, S i} := by
  ext x
  exact common_fiber_rebased g S z hz x

/-- The relation used for the monodromy components is an equivalence
relation for an arbitrary subgroup, with no normality assumption. -/
theorem same_monodromy_class_equivalence (H : Subgroup G) :
    Equivalence (SameMonodromyClass H) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x
    change x⁻¹ * x ∈ H
    rw [inv_mul_cancel]
    exact H.one_mem
  · intro x y h
    have hinv := H.inv_mem h
    simpa [SameMonodromyClass] using hinv
  · intro x y z hxy hyz
    have h := H.mul_mem hxy hyz
    simpa [SameMonodromyClass, mul_assoc] using h

/-- The nonempty common fiber has a single H-class if and only if the
local monodromy subgroup equals the intersection of the shadow subgroups. -/
theorem common_fiber_one_class_iff (g : I → G) (S : I → Subgroup G)
    (H : Subgroup G) (hH : H ≤ ⨅ i, S i) (z : G)
    (hz : z ∈ CommonFiber g S) :
    (∀ x ∈ CommonFiber g S, ∀ y ∈ CommonFiber g S,
      SameMonodromyClass H x y) ↔ H = ⨅ i, S i := by
  constructor
  · intro hconnected
    apply le_antisymm hH
    intro k hk
    have hzk : z * k ∈ CommonFiber g S := by
      apply (common_fiber_rebased g S z hz (z * k)).2
      simpa using hk
    have h := hconnected z hz (z * k) hzk
    simpa [SameMonodromyClass] using h
  · intro heq x hx y hy
    have h := (common_fiber_rebased g S x hx y).1 hy
    change x⁻¹ * y ∈ H
    simpa [heq] using h

/-- An element of the subgroup-intersection outside the local monodromy
provides two explicit common fiber points in different classes. -/
theorem monodromy_defect_witness (g : I → G) (S : I → Subgroup G)
    (H : Subgroup G) (z k : G) (hz : z ∈ CommonFiber g S)
    (hk : k ∈ ⨅ i, S i) (hkH : k ∉ H) :
    z * k ∈ CommonFiber g S ∧ ¬ SameMonodromyClass H z (z * k) := by
  constructor
  · apply (common_fiber_rebased g S z hz (z * k)).2
    simpa using hk
  · intro h
    apply hkH
    simpa [SameMonodromyClass] using h

#print axioms common_fiber_rebased
#print axioms common_fiber_eq_coset
#print axioms same_monodromy_class_equivalence
#print axioms common_fiber_one_class_iff
#print axioms monodromy_defect_witness

end Phase29CosetMonodromy
