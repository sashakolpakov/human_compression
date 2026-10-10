import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
Two group-theoretic steps used in the first-excess classification.
The first lifts one intersection through a homomorphism when common
images lift in the intended subgroup and the kernel contributes nothing
extra. The second applies this to a two-element kernel whose distinguished
element occurs in a marked parabolic precisely on a principal support.

No central extension construction, seed group, uniform parameter census,
or canonical-quotient theorem is formalized by this module.
-/

namespace MathCompression.PrincipalKernelIntersections

variable {G Q : Type*} [Group G] [Group Q]

theorem intersection_eq_of_image_and_kernel
    (A B C : Subgroup G) (f : G →* Q)
    (hCA : C ≤ A) (hCB : C ≤ B)
    (himage : ∀ x : G, x ∈ A → x ∈ B →
      ∃ y : G, y ∈ C ∧ f y = f x)
    (hkernel : ∀ x : G, x ∈ A → x ∈ B → f x = 1 → x ∈ C) :
    A ⊓ B = C := by
  apply le_antisymm
  · intro x hx
    obtain ⟨y, hy, heq⟩ := himage x hx.1 hx.2
    have hA : x * y⁻¹ ∈ A := A.mul_mem hx.1 (A.inv_mem (hCA hy))
    have hB : x * y⁻¹ ∈ B := B.mul_mem hx.2 (B.inv_mem (hCB hy))
    have hf : f (x * y⁻¹) = 1 := by simp [map_mul, map_inv, heq]
    have hC : x * y⁻¹ ∈ C := hkernel _ hA hB hf
    have hmul : (x * y⁻¹) * y ∈ C := C.mul_mem hC hy
    simpa only [inv_mul_cancel_right] using hmul
  · intro x hx
    exact ⟨hCA hx, hCB hx⟩

theorem intersection_property_of_principal_kernel
    {I : Type*} (P : Set I → Subgroup G) (f : G →* Q)
    (z : G) (J : Set I)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f)
    (hkernel : ∀ x : G, f x = 1 → x = 1 ∨ x = z)
    (hsupport : ∀ S : Set I, z ∈ P S ↔ J ⊆ S) :
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
    rcases hkernel x hfx with hx | hx
    · simpa only [hx] using (P (S ∩ T)).one_mem
    · subst x
      apply (hsupport _).mpr
      exact Set.subset_inter ((hsupport S).mp hxS) ((hsupport T).mp hxT)

#print axioms intersection_eq_of_image_and_kernel
#print axioms intersection_property_of_principal_kernel

end MathCompression.PrincipalKernelIntersections
