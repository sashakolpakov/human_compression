import PrincipalKernelIntersections

/-!
Actual intersection transport for nested kernel supports. The explicit
three-valued profile is K on the larger support, L on the smaller support,
and the trivial subgroup elsewhere. No finite group, centrality, elementary
abelian kernel, extension construction, or classification is assumed here.
-/

namespace MathCompression.NestedKernelIntersections

open MathCompression.PrincipalKernelIntersections

variable {G Q I A : Type*} [Group G] [Group Q]

/-- An arbitrary family of totally nested supports suffices. Its index type
need not be finite or linearly ordered; nestedness is supplied explicitly.
The kernel membership profile is an assumption, not inferred from image IP. -/
theorem intersection_property_of_chain_kernel
    (P : Set I → Subgroup G) (f : G →* Q)
    (levels : A → Subgroup G) (support : A → Set I)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f)
    (hnested : ∀ i j : A, support i ⊆ support j ∨ support j ⊆ support i)
    (hprofile : ∀ (S : Set I) (x : G), f x = 1 →
      (x ∈ P S ↔ ∃ i : A, x ∈ levels i ∧ support i ⊆ S)) :
    ∀ S T : Set I, P S ⊓ P T = P (S ∩ T) := by
  intro S T
  apply intersection_eq_of_image_and_kernel (P S) (P T) (P (S ∩ T)) f
  · exact hmono _ _ Set.inter_subset_left
  · exact hmono _ _ Set.inter_subset_right
  · intro x hxS hxT
    have hximage : f x ∈ (P S).map f ⊓ (P T).map f := by
      constructor
      · exact Subgroup.mem_map.mpr ⟨x, hxS, rfl⟩
      · exact Subgroup.mem_map.mpr ⟨x, hxT, rfl⟩
    rw [himages] at hximage
    exact Subgroup.mem_map.mp hximage
  · intro x hxS hxT hfx
    obtain ⟨i, hi, hiS⟩ := (hprofile S x hfx).mp hxS
    obtain ⟨j, hj, hjT⟩ := (hprofile T x hfx).mp hxT
    apply (hprofile (S ∩ T) x hfx).mpr
    rcases hnested i j with hij | hji
    · exact ⟨i, hi, Set.subset_inter hiS (hij.trans hjT)⟩
    · exact ⟨j, hj, Set.subset_inter (hji.trans hiS) hjT⟩

noncomputable def nestedKernel
    (L K : Subgroup G) (E T S : Set I) : Subgroup G := by
  classical
  exact if T ⊆ S then K else if E ⊆ S then L else ⊥

theorem mem_nestedKernel
    (L K : Subgroup G) (E T S : Set I) (hLK : L ≤ K) (x : G) :
    x ∈ nestedKernel L K E T S ↔
      x = 1 ∨ (x ∈ L ∧ E ⊆ S) ∨ (x ∈ K ∧ T ⊆ S) := by
  classical
  unfold nestedKernel
  by_cases hT : T ⊆ S
  · rw [if_pos hT]
    constructor
    · intro hx
      exact Or.inr (Or.inr ⟨hx, hT⟩)
    · intro hx
      rcases hx with rfl | hx | hx
      · exact K.one_mem
      · exact hLK hx.1
      · exact hx.1
  · rw [if_neg hT]
    by_cases hE : E ⊆ S
    · rw [if_pos hE]
      constructor
      · intro hx
        exact Or.inr (Or.inl ⟨hx, hE⟩)
      · intro hx
        rcases hx with rfl | hx | hx
        · exact L.one_mem
        · exact hx.1
        · exact False.elim (hT hx.2)
    · rw [if_neg hE]
      constructor
      · intro hx
        exact Or.inl (Subgroup.mem_bot.mp hx)
      · intro hx
        rcases hx with hx | hx | hx
        · exact Subgroup.mem_bot.mpr hx
        · exact False.elim (hE hx.2)
        · exact False.elim (hT hx.2)

theorem nestedKernel_mono
    (L K : Subgroup G) (E T : Set I) (hLK : L ≤ K)
    {S U : Set I} (hSU : S ⊆ U) :
    nestedKernel L K E T S ≤ nestedKernel L K E T U := by
  intro x hx
  rw [mem_nestedKernel L K E T S hLK] at hx
  apply (mem_nestedKernel L K E T U hLK x).mpr
  rcases hx with hx | hx | hx
  · exact Or.inl hx
  · exact Or.inr (Or.inl ⟨hx.1, hx.2.trans hSU⟩)
  · exact Or.inr (Or.inr ⟨hx.1, hx.2.trans hSU⟩)

/-- The explicit K/L/trivial profile has exact meets. -/
theorem nestedKernel_meet
    (L K : Subgroup G) (E T S U : Set I)
    (hLK : L ≤ K) (hET : E ⊆ T) :
    nestedKernel L K E T S ⊓ nestedKernel L K E T U =
      nestedKernel L K E T (S ∩ U) := by
  apply le_antisymm
  · intro x hx
    have hxS := (mem_nestedKernel L K E T S hLK x).mp hx.1
    have hxU := (mem_nestedKernel L K E T U hLK x).mp hx.2
    apply (mem_nestedKernel L K E T (S ∩ U) hLK x).mpr
    rcases hxS with hxS | hxS | hxS
    · exact Or.inl hxS
    · rcases hxU with hxU | hxU | hxU
      · exact Or.inl hxU
      · exact Or.inr (Or.inl ⟨hxS.1, Set.subset_inter hxS.2 hxU.2⟩)
      · exact Or.inr (Or.inl ⟨hxS.1,
          Set.subset_inter hxS.2 (hET.trans hxU.2)⟩)
    · rcases hxU with hxU | hxU | hxU
      · exact Or.inl hxU
      · exact Or.inr (Or.inl ⟨hxU.1,
          Set.subset_inter (hET.trans hxS.2) hxU.2⟩)
      · exact Or.inr (Or.inr ⟨hxS.1, Set.subset_inter hxS.2 hxU.2⟩)
  · intro x hx
    exact ⟨nestedKernel_mono L K E T hLK Set.inter_subset_left hx,
      nestedKernel_mono L K E T hLK Set.inter_subset_right hx⟩

/-- Exact image IP and the explicit nested kernel profile imply actual IP.
No assertion about parabolic kernels is deduced from image IP alone. -/
theorem intersection_property_of_nested_kernel
    (P : Set I → Subgroup G) (f : G →* Q)
    (L K : Subgroup G) (E T : Set I)
    (hLK : L ≤ K) (hET : E ⊆ T)
    (hmono : ∀ S U : Set I, S ⊆ U → P S ≤ P U)
    (himages : ∀ S U : Set I,
      (P S).map f ⊓ (P U).map f = (P (S ∩ U)).map f)
    (hprofile : ∀ S : Set I,
      P S ⊓ f.ker = nestedKernel L K E T S) :
    ∀ S U : Set I, P S ⊓ P U = P (S ∩ U) := by
  intro S U
  apply intersection_eq_of_image_and_kernel (P S) (P U) (P (S ∩ U)) f
  · exact hmono _ _ Set.inter_subset_left
  · exact hmono _ _ Set.inter_subset_right
  · intro x hxS hxU
    have hximage : f x ∈ (P S).map f ⊓ (P U).map f := by
      constructor
      · exact Subgroup.mem_map.mpr ⟨x, hxS, rfl⟩
      · exact Subgroup.mem_map.mpr ⟨x, hxU, rfl⟩
    rw [himages] at hximage
    exact Subgroup.mem_map.mp hximage
  · intro x hxS hxU hfx
    have hxker : x ∈ f.ker := hfx
    have hxKS : x ∈ nestedKernel L K E T S := by
      rw [← hprofile S]
      exact ⟨hxS, hxker⟩
    have hxKU : x ∈ nestedKernel L K E T U := by
      rw [← hprofile U]
      exact ⟨hxU, hxker⟩
    have hxmeet : x ∈ nestedKernel L K E T (S ∩ U) := by
      rw [← nestedKernel_meet L K E T S U hLK hET]
      exact ⟨hxKS, hxKU⟩
    rw [← hprofile (S ∩ U)] at hxmeet
    exact hxmeet.1

#print axioms intersection_property_of_chain_kernel
#print axioms mem_nestedKernel
#print axioms nestedKernel_mono
#print axioms nestedKernel_meet
#print axioms intersection_property_of_nested_kernel

end MathCompression.NestedKernelIntersections
