import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic.Group

/-!
A factorization of one parabolic gives a rank-three typed Helly theorem.
The finite Suzuki matrices and subgroup maximality are not formalized here.
-/

namespace RankThreeFactorization

variable {G : Type*} [Group G]

/-- Membership in the left coset based at x. -/
def InCoset (H : Subgroup G) (x y : G) : Prop := x⁻¹ * y ∈ H

/-- If A is the product of its intersections with B and C, every B-coset
and C-coset meeting an A-coset have a common point in that A-coset.
No finiteness or pairwise B/C incidence assumption is needed. -/
theorem common_point_of_factorization (A B C : Subgroup G)
    (hfactor : ∀ x ∈ A, ∃ s ∈ A ⊓ B, ∃ t ∈ A ⊓ C, x = s * t)
    (a b c : G)
    (hAB : ∃ u, InCoset A a u ∧ InCoset B b u)
    (hAC : ∃ v, InCoset A a v ∧ InCoset C c v) :
    ∃ z, InCoset A a z ∧ InCoset B b z ∧ InCoset C c z := by
  obtain ⟨u, huA, huB⟩ := hAB
  obtain ⟨v, hvA, hvC⟩ := hAC
  have huv : u⁻¹ * v ∈ A := by
    have h := A.mul_mem (A.inv_mem huA) hvA
    have heq : (a⁻¹ * u)⁻¹ * (a⁻¹ * v) = u⁻¹ * v := by group
    exact heq ▸ h
  obtain ⟨s, hs, t, ht, hst⟩ := hfactor (u⁻¹ * v) huv
  have hright : u * s = v * t⁻¹ := by
    have heq : u * (u⁻¹ * v) * t⁻¹ = u * (s * t) * t⁻¹ :=
      congrArg (fun x => u * x * t⁻¹) hst
    simpa only [mul_assoc, mul_inv_cancel, inv_mul_cancel_left, mul_one,
      mul_inv_cancel_left] using heq.symm
  refine ⟨u * s, ?_, ?_, ?_⟩
  · change a⁻¹ * (u * s) ∈ A
    rw [← mul_assoc]
    exact A.mul_mem huA hs.1
  · change b⁻¹ * (u * s) ∈ B
    rw [← mul_assoc]
    exact B.mul_mem huB hs.2
  · rw [hright]
    change c⁻¹ * (v * t⁻¹) ∈ C
    rw [← mul_assoc]
    exact C.mul_mem hvC (C.inv_mem ht.2)

end RankThreeFactorization

#print axioms RankThreeFactorization.common_point_of_factorization
