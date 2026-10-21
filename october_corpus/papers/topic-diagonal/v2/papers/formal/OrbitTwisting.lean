import Mathlib.GroupTheory.OrderOfElement
import Mathlib.Tactic

/-! Algebraic parts of the finite-rank twisting proof.
The geometric Helly hypothesis and the standard Coxeter parabolic theorem
are written inputs, not claimed to be formalized here. -/
namespace OrbitTwisting

variable {G : Type*} [Group G]

def coset (P : Subgroup G) (g : G) : Set G := {x | g⁻¹ * x ∈ P}
def product (H P : Subgroup G) : Set G := {g | ∃ h ∈ H, h⁻¹ * g ∈ P}

theorem product_iff_meets (H P : Subgroup G) (g : G) :
    g ∈ product H P ↔ ∃ h ∈ H, h ∈ coset P g := by
  constructor
  · rintro ⟨h, hh, hp⟩
    refine ⟨h, hh, ?_⟩
    change g⁻¹ * h ∈ P
    simpa using P.inv_mem hp
  · rintro ⟨h, hh, hp⟩
    refine ⟨h, hh, ?_⟩
    change g⁻¹ * h ∈ P at hp
    simpa using P.inv_mem hp

theorem product_intersection_of_helly (H K P : Subgroup G)
    (helly : ∀ g : G,
      (∃ h ∈ H, h ∈ coset P g) →
      (∃ k ∈ K, k ∈ coset P g) →
      ∃ w, w ∈ H ∧ w ∈ K ∧ w ∈ coset P g) :
    product H P ∩ product K P = product (H ⊓ K) P := by
  ext g
  constructor
  · rintro ⟨hh, hk⟩
    obtain ⟨w, wh, wk, wp⟩ := helly g
      ((product_iff_meets H P g).mp hh) ((product_iff_meets K P g).mp hk)
    exact (product_iff_meets (H ⊓ K) P g).mpr ⟨w, ⟨wh, wk⟩, wp⟩
  · intro hg
    obtain ⟨w, whk, wp⟩ := (product_iff_meets (H ⊓ K) P g).mp hg
    exact ⟨(product_iff_meets H P g).mpr ⟨w, whk.1, wp⟩,
      (product_iff_meets K P g).mpr ⟨w, whk.2, wp⟩⟩

variable {L : Type*} {X : L → Type*} {J : Type*}

def support (f : J → (l : L) → Set (X l)) (removed : Set L) (j : J) :
    Set (Sigma X) := {x | x.1 ∉ removed ∧ x.2 ∈ f j x.1}

theorem support_intersection (f : J → (l : L) → Set (X l))
    (R S : Set L) (i j k : J)
    (orbit_inter : ∀ l, f k l = f i l ∩ f j l) :
    support f (R ∪ S) k = support f R i ∩ support f S j := by
  ext x
  simp only [support, Set.mem_setOf_eq, Set.mem_union, not_or, Set.mem_inter_iff,
    orbit_inter]
  tauto

theorem complement_union (I M N : Set L) :
    (I \ M) ∪ (I \ N) = I \ (M ∩ N) := by
  ext x
  simp only [Set.mem_union, Set.mem_sdiff, Set.mem_inter_iff]
  tauto

theorem orbital_square (a b : G) : (a * b) ^ 2 = a * (b * a * b) := by
  simp only [pow_two, mul_assoc]

theorem doubled_order_of_projection {H : Type*} [Group H]
    (f : G →* H) (g : G) (h : orderOf (f g) = 2) :
    orderOf g = 2 * orderOf (g ^ 2) := by
  have hd : 2 ∣ orderOf g := h ▸ orderOf_map_dvd f g
  rw [orderOf_pow_of_dvd (by decide : (2 : ℕ) ≠ 0) hd]
  exact (Nat.mul_div_cancel' hd).symm

theorem mixed_exact_order {H : Type*} [Group H]
    (f : G →* H) (a b : G) (ha : f a = 1) (hb : orderOf (f b) = 2) :
    orderOf (a * b) = 2 * orderOf (a * (b * a * b)) := by
  have h : orderOf (f (a * b)) = 2 := by simpa [ha] using hb
  simpa only [orbital_square] using doubled_order_of_projection f (a * b) h

theorem mixed_infinite_order {H : Type*} [Group H]
    (f : G →* H) (a b : G) (ha : f a = 1) (hb : orderOf (f b) = 2)
    (hinf : orderOf (a * (b * a * b)) = 0) : orderOf (a * b) = 0 := by
  rw [mixed_exact_order f a b ha hb, hinf, mul_zero]

end OrbitTwisting

#print axioms OrbitTwisting.product_iff_meets
#print axioms OrbitTwisting.product_intersection_of_helly
#print axioms OrbitTwisting.support_intersection
#print axioms OrbitTwisting.complement_union
#print axioms OrbitTwisting.orbital_square
#print axioms OrbitTwisting.doubled_order_of_projection
#print axioms OrbitTwisting.mixed_exact_order
#print axioms OrbitTwisting.mixed_infinite_order
