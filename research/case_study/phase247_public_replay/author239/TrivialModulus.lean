import Mathlib.GroupTheory.OrderOfElement

/-! Elementary interfaces used in the uniform toroidal-pyramid proof.
The affine action, fixed finite group computation and surface theorem remain
written or separately computed. These statements do not assert those inputs.
-/
namespace MathCompression.PyramidKernelTransport

/-- A function supported at two distinct single coordinates is trivial. -/
theorem disjoint_single_coordinate_support {I V : Type*} [One V]
    (f : I → V) (a b : I) (hab : a ≠ b)
    (ha : ∀ i, i ≠ a → f i = 1) (hb : ∀ i, i ≠ b → f i = 1) :
    ∀ i, f i = 1 := by
  intro i
  by_cases hia : i = a
  · subst i
    exact hb a hab
  · exact ha i hia

/-- A coordinate in {0,1} which vanishes modulo n≥2 vanishes integrally. -/
theorem center_coordinate_zero (n t : ℕ) (hn : 1 ≤ n)
    (ht : t ≤ 1) (hmod : t % n = 0) : t = 0 := by
  have hlt : t < n := lt_of_le_of_lt ht (lt_of_lt_of_le (by decide : 1 < 2) hn)
  rwa [Nat.mod_eq_of_lt hlt] at hmod

variable {G E D : Type*} [Group G] [Group E] [Group D]

/-- Trivial kernel on a subgroup implies injectivity on that subgroup. -/
theorem injective_on_subgroup (rho : G →* E) (T : Subgroup G)
    (hker : ∀ x ∈ T, rho x = 1 → x = 1)
    {x y : G} (hx : x ∈ T) (hy : y ∈ T) (heq : rho x = rho y) : x = y := by
  have hk : rho (x * y⁻¹) = 1 := by simp [heq]
  have hid := hker (x * y⁻¹) (T.mul_mem hx (T.inv_mem hy)) hk
  exact mul_inv_eq_one.mp hid

/-- A fixed quotient can test the full intersection defect when the first
map is injective on the original intersection and bounds its image in J. -/
theorem transport_kernel_intersection
    (rho : G →* E) (pi : E →* D) (T C : Subgroup G) (J : Subgroup E)
    (hCT : C ≤ T)
    (hker : ∀ x ∈ T, rho x = 1 → x = 1)
    (himage : ∀ x ∈ T, rho x ∈ J)
    (hfixed : ∀ y ∈ J, pi y = 1 → y ∈ C.map rho) :
    ∀ x ∈ T, pi (rho x) = 1 → x ∈ C := by
  intro x hx hpx
  obtain ⟨c, hc, heq⟩ := hfixed (rho x) (himage x hx) hpx
  have hxc : x = c := injective_on_subgroup rho T hker hx (hCT hc) heq.symm
  simpa [hxc] using hc

#print axioms disjoint_single_coordinate_support
#print axioms center_coordinate_zero
#print axioms injective_on_subgroup
#print axioms transport_kernel_intersection

end MathCompression.PyramidKernelTransport
