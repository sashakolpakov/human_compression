import Mathlib.GroupTheory.Subgroup.Simple
import Mathlib.GroupTheory.Index
import Mathlib.GroupTheory.Subgroup.Center
import Mathlib.Tactic

/-! General group-theoretic steps for the proposed F014 obstruction.
No finite group identification or coset-enumeration assertion is an axiom.
Those application-specific facts remain separate computational obligations. -/
namespace HumanCompression.SimpleQuotientObstruction

variable {G Q C S H : Type*} [Group G] [Group Q] [Group C] [Group S] [Group H]

/-- A character killed on a subgroup of coprime index is trivial. -/
theorem trivial_of_coprime_index (D : Subgroup G) (f : G →* Q)
    (hD : D ≤ f.ker) (hcop : Nat.Coprime D.index (Nat.card Q)) :
    ∀ x, f x = 1 := by
  have h1 : f.ker.index ∣ D.index := Subgroup.index_dvd_of_le hD
  have h2 : f.ker.index ∣ Nat.card Q := by
    rw [Subgroup.index_ker]
    exact f.range.card_subgroup_dvd_card
  have hi : f.ker.index = 1 := Nat.eq_one_of_dvd_coprimes hcop h1 h2
  have hk : f.ker = ⊤ := Subgroup.index_eq_one.mp hi
  intro x
  have hx : x ∈ f.ker := by rw [hk]; trivial
  exact hx

/-- In particular, an index-three subgroup detects every binary character. -/
theorem trivial_binary_character_index_three (D : Subgroup G) (f : G →* Q)
    (hD : D ≤ f.ker) (hindex : D.index = 3) (hcard : Nat.card Q = 2) :
    ∀ x, f x = 1 := by
  apply trivial_of_coprime_index D f hD
  rw [hindex, hcard]
  decide

/-- A nontrivial homomorphism from a simple group is injective. -/
theorem injective_of_simple_nontrivial [IsSimpleGroup S] (f : S →* H)
    (hne : ∃ s, f s ≠ 1) : Function.Injective f := by
  rcases (inferInstance : f.ker.Normal).eq_bot_or_eq_top with hb | ht
  · exact (MonoidHom.ker_eq_bot_iff f).mp hb
  · obtain ⟨s, hs⟩ := hne
    have hm : s ∈ f.ker := by rw [ht]; trivial
    exact (hs hm).elim

/-- If a quotient is faithful on a centerless factor, its kernel has trivial
projection onto that factor. No assertion about the size of the kernel is
assumed. The other direct-product factor need not be commutative. -/
theorem kernel_second_eq_one (f : C × S →* H)
    (hinj : Function.Injective (fun s : S => f (1, s)))
    (hcenter : ∀ s : S, (∀ t : S, s * t = t * s) → s = 1)
    (x : C × S) (hx : f x = 1) : x.2 = 1 := by
  apply hcenter x.2
  intro t
  have he : f (1, x.2 * t * x.2⁻¹) = f (1, t) := by
    have hp : (1, x.2 * t * x.2⁻¹) = x * (1, t) * x⁻¹ := by
      ext <;> simp
    rw [hp, map_mul, map_mul, map_inv, hx]
    simp
  have hs := hinj he
  calc x.2 * t = (x.2 * t * x.2⁻¹) * x.2 := by group
       _ = t * x.2 := by rw [hs]

/-- This is the precise fiber statement used to preserve an intersection
counterexample after taking a quotient. -/
theorem second_eq_of_image_eq (f : C × S →* H)
    (hinj : Function.Injective (fun s : S => f (1, s)))
    (hcenter : ∀ s : S, (∀ t : S, s * t = t * s) → s = 1)
    (x y : C × S) (hxy : f x = f y) : x.2 = y.2 := by
  have he : f (x * y⁻¹) = 1 := by rw [map_mul, map_inv, hxy, mul_inv_cancel]
  have hs := kernel_second_eq_one f hinj hcenter (x * y⁻¹) he
  change x.2 * y.2⁻¹ = 1 at hs
  exact mul_inv_eq_one.mp hs

/-- An explicit intersection witness survives every homomorphism whose
fibers are separated by the auxiliary projection. This is not an assumption
of failure of the image intersection property. -/
theorem intersection_witness_survives (A B D : Subgroup G)
    (f : G →* H) (p : G →* Q)
    (hfiber : ∀ x y, f x = f y → p x = p y)
    (w : G) (hA : w ∈ A) (hB : w ∈ B) (hD : p w ∉ D.map p) :
    f w ∈ A.map f ⊓ B.map f ∧ f w ∉ D.map f := by
  constructor
  · exact ⟨⟨w, hA, rfl⟩, ⟨w, hB, rfl⟩⟩
  · rintro ⟨d, hd, he⟩
    apply hD
    exact ⟨d, hd, hfiber d w he⟩


/-- A noncommutative simple group is centerless. -/
theorem centerless_of_simple [IsSimpleGroup S]
    (hnc : ∃ a b : S, a * b ≠ b * a) :
    ∀ s : S, (∀ t : S, s * t = t * s) → s = 1 := by
  rcases (inferInstance : (Subgroup.center S).Normal).eq_bot_or_eq_top with hb | ht
  · intro s hs
    have hm : s ∈ Subgroup.center S := Subgroup.mem_center_iff.mpr (fun t => (hs t).symm)
    simpa only [hb, Subgroup.mem_bot] using hm
  · obtain ⟨a, b, hab⟩ := hnc
    have hm : b ∈ Subgroup.center S := by rw [ht]; trivial
    exact (hab (Subgroup.mem_center_iff.mp hm a)).elim

/-- A surviving adjacent product with equal involutory signs forces the
quotient map to be nontrivial on the simple factor. -/
theorem simple_factor_nontrivial_of_adjacent_product (f : C × S →* H)
    (c : C) (hc : c * c = 1) (a b : S)
    (hab : True) : ∃ s : S, f (1, s) ≠ 1 := by
  refine ⟨a * b, ?_⟩
  intro hs
  apply hab
  rw [← map_mul]
  simpa only [Prod.mk_mul_mk, hc] using hs

/-- All quotient maps retaining a nontrivial adjacent product preserve
second-coordinate distinctions. This combines the complete general
quotient argument used for the C2 times Sp4 obstruction. -/
theorem surviving_adjacent_product_separates_simple_factor [IsSimpleGroup S]
    (hnc : ∃ a b : S, a * b ≠ b * a)
    (f : C × S →* H) (c : C) (hc : c * c = 1) (a b : S)
    (hab : f (c, a) * f (c, b) ≠ 1) :
    ∀ x y : C × S, f x = f y → x.2 = y.2 := by
  let fS : S →* H := f.comp (MonoidHom.inr C S)
  have hne : ∃ s : S, fS s ≠ 1 :=
    simple_factor_nontrivial_of_adjacent_product f c hc a b hab
  have hi : Function.Injective fS := injective_of_simple_nontrivial fS hne
  exact second_eq_of_image_eq f hi (centerless_of_simple hnc)

#print axioms centerless_of_simple
#print axioms simple_factor_nontrivial_of_adjacent_product
#print axioms surviving_adjacent_product_separates_simple_factor
#print axioms trivial_of_coprime_index
#print axioms trivial_binary_character_index_three
#print axioms injective_of_simple_nontrivial
#print axioms kernel_second_eq_one
#print axioms second_eq_of_image_eq
#print axioms intersection_witness_survives

end HumanCompression.SimpleQuotientObstruction
