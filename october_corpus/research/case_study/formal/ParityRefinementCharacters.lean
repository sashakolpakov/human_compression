import ParityOverlapGrid

/-! Derived row and column character equations for actual support refinements. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration
open scoped BigOperators

variable {I C T E G A : Type*} [DecidableEq I] [Fintype C] [Fintype T]
  [DecidableEq C] [DecidableEq T] [Group E] [Group G] [CommGroup A]

theorem refined_character_equality (e : I → E) (g : I → G)
    (coarse : C → Finset I) (fine : T → Finset I)
    (hcE : Pairwise fun c d => ∀ i ∈ coarse c, ∀ j ∈ coarse d, Commute (e i) (e j))
    (hcG : Pairwise fun c d => ∀ i ∈ coarse c, ∀ j ∈ coarse d, Commute (g i) (g j))
    (hfE : Pairwise fun c d => ∀ i ∈ fine c, ∀ j ∈ fine d, Commute (e i) (e j))
    (hfG : Pairwise fun c d => ∀ i ∈ fine c, ∀ j ∈ fine d, Commute (g i) (g j))
    (hd : Pairwise fun c d => Disjoint (coarse c) (coarse d))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (ε : E →* A) (δ : G →* A)
    (hlocal : ∀ c, ∀ u : marked e (coarse c), ∀ v : marked g (coarse c),
      ((u : E), (v : G)) ∈ marked (fun i => (e i, g i)) (coarse c) ↔ ε u = δ v)
    (parent : T → C) (hsub : ∀ t, fine t ⊆ coarse (parent t))
    (x : ∀ t, marked e (fine t)) (y : ∀ t, marked g (fine t))
    (hm : (componentAssembly e fine hfE x, componentAssembly g fine hfG y) ∈
      marked (fun i => (e i, g i)) (Finset.univ.biUnion coarse)) :
    ∀ c, (∏ t, if c = parent t then ε (x t) else 1) =
      ∏ t, if c = parent t then δ (y t) else 1 := by
  have hU : ∀ t, fine t ⊆ Finset.univ.biUnion coarse := by
    intro t i hi
    exact Finset.mem_biUnion.mpr ⟨parent t, Finset.mem_univ _, hsub t hi⟩
  have hx := componentAssembly_mem_super e fine hfE _ hU x
  have hy := componentAssembly_mem_super g fine hfG _ hU y
  have hp := (mixed_membership_coordinates e g coarse hcE hcG hd hipE hipG ε δ hlocal
    ⟨_, hx⟩ ⟨_, hy⟩).mp hm
  intro c
  exact (component_coordinate_refinement e coarse fine hcE hfE hd hipE parent hsub ε c x hx).symm.trans
    ((hp c).trans (component_coordinate_refinement g coarse fine hcG hfG hd hipG parent hsub δ c y hy))

omit [DecidableEq I] [DecidableEq T] in
theorem row_filtered_product (f : C × T → A) (c : C) :
    (∏ p, if c = p.1 then f p else 1) = ∏ t, f (c, t) := by
  rw [Fintype.prod_prod_type, Finset.prod_comm]
  simp

omit [DecidableEq I] [DecidableEq C] in
theorem column_filtered_product (f : C × T → A) (t : T) :
    (∏ p, if t = p.2 then f p else 1) = ∏ c, f (c, t) := by
  rw [Fintype.prod_prod_type]
  simp

omit [DecidableEq I] [Fintype C] [DecidableEq C] [DecidableEq T] in
/-- An equality of character products yields the exact additive defect
sum required by the interval-overlap theorem. -/
theorem character_defect_sum (a b : T → A) (hab : (∏ t, a t) = ∏ t, b t) :
    (∑ t, Additive.ofMul (a t * (b t)⁻¹)) = 0 := by
  change Additive.ofMul (∏ t, a t * (b t)⁻¹) = Additive.ofMul 1
  congr 1
  rw [Finset.prod_mul_distrib, Finset.prod_inv_distrib, hab, mul_inv_cancel]

#print axioms refined_character_equality
#print axioms row_filtered_product
#print axioms column_filtered_product
#print axioms character_defect_sum

end MathCompression.ParityMix
