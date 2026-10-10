import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Data.Nat.Prime.Basic

/-!
An algebraic obstruction to an isomorphism of marked covers: one marked
generator inverts a non-self-inverse kernel element, while the corresponding
generator in the other cover fixes every kernel element.

This certifies only the separation step. The existence and order of the
kernels, their actions, and polytope recognition are separate written inputs.
-/

namespace MathCompression.CoverCharacterSeparation

variable {H H' G : Type*} [Group H] [Group H'] [Group G]

/-- Different inversion/fixed actions obstruct a marked isomorphism over G. -/
theorem no_marked_cover_iso (π : H →* G) (π' : H' →* G)
    (a : H) (a' : H') (z : H)
    (hz : π z = 1) (hinv : a⁻¹ * z * a = z⁻¹) (hne : z ≠ z⁻¹)
    (hfixed : ∀ w, π' w = 1 → a'⁻¹ * w * a' = w) :
    ¬ ∃ e : H ≃* H', e a = a' ∧ π'.comp e.toMonoidHom = π := by
  rintro ⟨e, ha, hπ⟩
  have hz' : π' (e z) = 1 := by
    have he := congrArg (fun f : H →* G => f z) hπ
    simpa only [MonoidHom.comp_apply, MulEquiv.coe_toMonoidHom, hz] using he
  have hconj : a'⁻¹ * e z * a' = (e z)⁻¹ := by
    simpa only [map_mul, map_inv, ha] using congrArg e hinv
  have heq : e z = e (z⁻¹) := by
    rw [map_inv]
    exact (hfixed (e z) hz').symm.trans hconj
  exact hne (e.injective heq)

/-- An element of odd prime order cannot equal its inverse. -/
theorem ne_inv_of_odd_prime_order (z : H) (p : ℕ) (hp : Nat.Prime p)
    (hodd : p ≠ 2) (horder : orderOf z = p) : z ≠ z⁻¹ := by
  intro heq
  have hpow : z ^ 2 = 1 := by
    calc
      z ^ 2 = z * z := pow_two z
      _ = z * z⁻¹ := congrArg (fun w => z * w) heq
      _ = 1 := mul_inv_cancel z
  have hdvd : p ∣ 2 := by
    simpa only [horder] using orderOf_dvd_of_pow_eq_one hpow
  exact hodd ((Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp hdvd)

/-- Prime-order specialization of the marked-cover obstruction. -/
theorem no_marked_cover_iso_of_odd_prime_order
    (π : H →* G) (π' : H' →* G) (a : H) (a' : H') (z : H)
    (p : ℕ) (hp : Nat.Prime p) (hodd : p ≠ 2) (horder : orderOf z = p)
    (hz : π z = 1) (hinv : a⁻¹ * z * a = z⁻¹)
    (hfixed : ∀ w, π' w = 1 → a'⁻¹ * w * a' = w) :
    ¬ ∃ e : H ≃* H', e a = a' ∧ π'.comp e.toMonoidHom = π :=
  no_marked_cover_iso π π' a a' z hz hinv
    (ne_inv_of_odd_prime_order z p hp hodd horder) hfixed

#print axioms no_marked_cover_iso
#print axioms ne_inv_of_odd_prime_order
#print axioms no_marked_cover_iso_of_odd_prime_order

end MathCompression.CoverCharacterSeparation
