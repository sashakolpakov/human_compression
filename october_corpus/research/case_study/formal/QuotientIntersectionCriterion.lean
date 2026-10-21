import Mathlib.GroupTheory.QuotientGroup.Basic
import Mathlib.Algebra.Group.Pointwise.Set.Basic

/-!
An exact downward intersection criterion. The products in the conclusions are
products of subsets, not subgroup joins. No finiteness, centrality, or global
surjectivity is assumed. Polytope recognition and the cover-poset consequences
are not part of this algebraic certificate.
-/

namespace MathCompression.QuotientIntersectionCriterion

open scoped Pointwise

variable {H G : Type*} [Group H] [Group G]

/-- The image of an intersection equals the intersection of the images exactly
when every kernel element in AB factors through the two restricted kernels. -/
theorem image_inf_iff_kernel_product (f : H →* G) (A B : Subgroup H) :
    A.map f ⊓ B.map f = (A ⊓ B).map f ↔
      (f.ker : Set H) ∩ ((A : Set H) * (B : Set H)) =
        ((f.ker ⊓ A : Subgroup H) : Set H) *
          ((f.ker ⊓ B : Subgroup H) : Set H) := by
  constructor
  · intro hi
    apply Set.Subset.antisymm
    · rintro m ⟨hm, hp⟩
      obtain ⟨a, ha, b, hb, rfl⟩ := Set.mem_mul.mp hp
      have hab : f a * f b = 1 := by simpa using hm
      have hai : f a = f b⁻¹ := by
        rw [map_inv]
        exact eq_inv_of_mul_eq_one_left hab
      have hfi : f a ∈ (A ⊓ B).map f := by
        rw [← hi]
        exact ⟨⟨a, ha, rfl⟩, ⟨b⁻¹, B.inv_mem hb, hai.symm⟩⟩
      obtain ⟨c, hc, hfc⟩ := hfi
      apply Set.mem_mul.mpr
      refine ⟨a * c⁻¹, ⟨?_, A.mul_mem ha (A.inv_mem hc.1)⟩,
        c * b, ⟨?_, B.mul_mem hc.2 hb⟩, ?_⟩
      · change f (a * c⁻¹) = 1
        simp [hfc]
      · change f (c * b) = 1
        simpa [hfc] using hab
      · simp [mul_assoc]
    · intro m hm
      obtain ⟨a, ha, b, hb, rfl⟩ := Set.mem_mul.mp hm
      exact ⟨f.ker.mul_mem ha.1 hb.1, Set.mul_mem_mul ha.2 hb.2⟩
  · intro hk
    apply le_antisymm
    · intro y hy
      obtain ⟨a, ha, hfa⟩ := hy.1
      obtain ⟨b, hb, hfb⟩ := hy.2
      have hd : a * b⁻¹ ∈ (f.ker : Set H) ∩ ((A : Set H) * (B : Set H)) := by
        refine ⟨?_, Set.mul_mem_mul ha (B.inv_mem hb)⟩
        change f (a * b⁻¹) = 1
        simp [hfa, hfb]
      rw [hk] at hd
      obtain ⟨u, hu, v, hv, huv⟩ := Set.mem_mul.mp hd
      have heq : u⁻¹ * a = v * b := by
        calc
          u⁻¹ * a = u⁻¹ * ((a * b⁻¹) * b) := by simp
          _ = u⁻¹ * ((u * v) * b) := by rw [huv]
          _ = v * b := by simp [mul_assoc]
      refine ⟨u⁻¹ * a, ⟨A.mul_mem (A.inv_mem hu.2) ha, ?_⟩, ?_⟩
      · rw [heq]
        exact B.mul_mem hv.2 hb
      · have hu1 : f u = 1 := hu.1
        simp [hu1, hfa]
    · intro y hy
      obtain ⟨c, hc, rfl⟩ := hy
      exact ⟨⟨c, hc.1, rfl⟩, ⟨c, hc.2, rfl⟩⟩

/-- Exact specialization to an actual quotient, with M an arbitrary normal
subgroup. Neither restricted kernel is assumed trivial. -/
theorem quotient_inf_iff_kernel_product (A B M : Subgroup H) [M.Normal] :
    A.map (QuotientGroup.mk' M) ⊓ B.map (QuotientGroup.mk' M) =
        (A ⊓ B).map (QuotientGroup.mk' M) ↔
      (M : Set H) ∩ ((A : Set H) * (B : Set H)) =
        ((M ⊓ A : Subgroup H) : Set H) * ((M ⊓ B : Subgroup H) : Set H) := by
  simpa only [QuotientGroup.ker_mk'] using
    image_inf_iff_kernel_product (QuotientGroup.mk' M) A B

/-- If the kernel lies in a subgroup L that meets both ends trivially, the
only test is whether the kernel meets the defect set L ∩ AB trivially. -/
theorem image_inf_iff_trivial_defect (f : H →* G) (A B L : Subgroup H)
    (hker : f.ker ≤ L) (hA : L ⊓ A = ⊥) (hB : L ⊓ B = ⊥) :
    A.map f ⊓ B.map f = (A ⊓ B).map f ↔
      (f.ker : Set H) ∩ ((L : Set H) ∩ ((A : Set H) * (B : Set H))) = {1} := by
  have hkA : f.ker ⊓ A = ⊥ := by
    apply le_antisymm
    · intro x hx
      rw [← hA]
      exact ⟨hker hx.1, hx.2⟩
    · exact bot_le
  have hkB : f.ker ⊓ B = ⊥ := by
    apply le_antisymm
    · intro x hx
      rw [← hB]
      exact ⟨hker hx.1, hx.2⟩
    · exact bot_le
  have hs : (f.ker : Set H) ∩ ((L : Set H) ∩ ((A : Set H) * (B : Set H))) =
      (f.ker : Set H) ∩ ((A : Set H) * (B : Set H)) := by
    apply Set.Subset.antisymm
    · exact fun _ hx => ⟨hx.1, hx.2.2⟩
    · exact fun _ hx => ⟨hx.1, hker hx.1, hx.2⟩
  rw [image_inf_iff_kernel_product, hkA, hkB, hs]
  simp only [Subgroup.coe_bot, Set.singleton_mul_singleton, mul_one]

/-- The actual intermediate-quotient formulation of the defect criterion.
Normality of L is not needed for this algebraic statement; normality of M is
needed only to form H/M. -/
theorem quotient_inf_iff_trivial_defect (A B L M : Subgroup H) [M.Normal]
    (hML : M ≤ L) (hA : L ⊓ A = ⊥) (hB : L ⊓ B = ⊥) :
    A.map (QuotientGroup.mk' M) ⊓ B.map (QuotientGroup.mk' M) =
        (A ⊓ B).map (QuotientGroup.mk' M) ↔
      (M : Set H) ∩ ((L : Set H) ∩ ((A : Set H) * (B : Set H))) = {1} := by
  have hk : (QuotientGroup.mk' M).ker ≤ L := by
    simpa only [QuotientGroup.ker_mk'] using hML
  simpa only [QuotientGroup.ker_mk'] using
    image_inf_iff_trivial_defect (QuotientGroup.mk' M) A B L hk hA hB

#print axioms image_inf_iff_kernel_product
#print axioms quotient_inf_iff_kernel_product
#print axioms image_inf_iff_trivial_defect
#print axioms quotient_inf_iff_trivial_defect

end MathCompression.QuotientIntersectionCriterion
