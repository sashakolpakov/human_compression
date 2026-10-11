import Mathlib.GroupTheory.SemidirectProduct
import Mathlib.Tactic

/-! The actual coordinate automorphism used for the paired signed markings.
Multiplicative notation is used for the abelian module. The source graph
identification and full marked-module intersection proof remain written. -/
namespace CocycleShear
variable {V Q : Type*} [CommGroup V] [Group Q]
variable (φ : Q →* MulAut V)

def IsCocycle (c : Q → V) : Prop :=
  ∀ g h, c (g * h) = c g * φ g (c h)

theorem cocycle_one (c : Q → V) (hc : IsCocycle φ c) : c 1 = 1 := by
  have h := hc 1 1
  simp only [one_mul, map_one, MulAut.one_apply] at h
  exact (mul_eq_left.mp h.symm)

/-- The coordinate shear, including an explicit inverse. -/
def shear (c : Q → V) (hc : IsCocycle φ c) : (V ⋊[φ] Q) ≃* (V ⋊[φ] Q) where
  toFun x := ⟨x.left * c x.right, x.right⟩
  invFun x := ⟨x.left * (c x.right)⁻¹, x.right⟩
  left_inv x := by ext <;> simp
  right_inv x := by ext <;> simp
  map_mul' x y := by
    apply SemidirectProduct.ext
    · change (x.left * φ x.right y.left) * c (x.right * y.right) =
        (x.left * c x.right) * φ x.right (y.left * c y.right)
      rw [hc, map_mul]
      ac_rfl
    · rfl

theorem shear_fixes_kernel (c : Q → V) (hc : IsCocycle φ c) (v : V) :
    shear φ c hc (SemidirectProduct.inl v) = SemidirectProduct.inl v := by
  apply SemidirectProduct.ext
  · change v * c 1 = v
    rw [cocycle_one φ c hc, mul_one]
  · rfl

theorem shear_involution (c : Q → V) (hc : IsCocycle φ c)
    (hexp : ∀ v : V, v * v = 1) (x : V ⋊[φ] Q) :
    shear φ c hc (shear φ c hc x) = x := by
  apply SemidirectProduct.ext
  · change (x.left * c x.right) * c x.right = x.left
    rw [mul_assoc, hexp, mul_one]
  · rfl

/-- A homomorphism with invariant values times a coboundary is a cocycle. -/
theorem invariant_hom_coboundary (b : Q →* V)
    (hb : ∀ g h, φ g (b h) = b h) (a : V) :
    IsCocycle φ (fun g => b g * a * φ g a⁻¹) := by
  intro g h
  simp only [map_mul, map_inv, MulAut.mul_apply, hb]
  simp [mul_assoc, mul_left_comm, mul_comm]

variable {G H : Type*} [Group G] [Group H]

theorem transport_marked_intersection (f : G ≃* H)
    (S R C : Set G)
    (h : Subgroup.closure S ⊓ Subgroup.closure R = Subgroup.closure C) :
    Subgroup.closure (f '' S) ⊓ Subgroup.closure (f '' R) =
      Subgroup.closure (f '' C) := by
  have h' := congrArg (Subgroup.map f.toMonoidHom) h
  rw [Subgroup.map_inf _ _ _ f.injective,
    MonoidHom.map_closure, MonoidHom.map_closure, MonoidHom.map_closure] at h'
  exact h'

end CocycleShear
#print axioms CocycleShear.cocycle_one
#print axioms CocycleShear.shear
#print axioms CocycleShear.shear_fixes_kernel
#print axioms CocycleShear.shear_involution
#print axioms CocycleShear.invariant_hom_coboundary
#print axioms CocycleShear.transport_marked_intersection
