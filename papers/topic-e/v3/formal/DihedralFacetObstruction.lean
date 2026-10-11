import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic

/-! The abstract normalizer step in the common PSL2/PGL2 proof.
The projective matrix centralizer calculation and Dickson input are not axioms
of this file: they remain written application obligations. -/
namespace HumanCompression.DihedralFacetObstruction
variable {G Q : Type*} [Group G] [Group Q]

/-- An involution with an odd vanishing power is the identity. -/
theorem eq_one_of_square_and_odd_power (y : Q) (hy : y ^ 2 = 1)
    (n : ℕ) (hn : Odd n) (hp : y ^ n = 1) : y = 1 := by
  obtain ⟨k, hk⟩ := hn
  have hnk : n = 2 * k + 1 := by omega
  rw [hnk, pow_add, pow_mul, hy, one_pow, pow_one, one_mul] at hp
  exact hp

/-- If a homomorphism kills t, it also kills an involution s whenever ts has
an odd vanishing power. The target may be infinite. -/
theorem killed_by_odd_adjacent_product (f : G →* Q) (s t : G)
    (hs : s ^ 2 = 1) (ht : f t = 1) (n : ℕ) (hn : Odd n)
    (hp : (t * s) ^ n = 1) : f s = 1 := by
  refine eq_one_of_square_and_odd_power (f s) ?_ n hn ?_
  · simpa only [map_pow, map_one] using congrArg f hs
  · have hh := congrArg f hp
    simpa only [map_pow, map_mul, ht, one_mul, map_one] using hh

/-- The quotient version used in Lemma 2. -/
theorem mem_normal_facet (H : Subgroup G) [H.Normal] (s t : G)
    (hs : s ^ 2 = 1) (ht : t ∈ H) (n : ℕ) (hn : Odd n)
    (hp : (t * s) ^ n = 1) : s ∈ H := by
  have hh := killed_by_odd_adjacent_product (QuotientGroup.mk' H) s t hs
    ((QuotientGroup.eq_one_iff _).mpr ht) n hn hp
  exact (QuotientGroup.eq_one_iff _).mp hh

/-- Generation plus one normalizing element supplies normality; this theorem
thus assumes neither a normal facet nor its desired membership conclusion. -/
theorem mem_facet_of_normalizer (H : Subgroup G) (s t : G)
    (hg : Subgroup.closure ((H : Set G) ∪ {s}) = ⊤)
    (hN : s ∈ Subgroup.normalizer H) (hs : s ^ 2 = 1)
    (ht : t ∈ H) (n : ℕ) (hn : Odd n) (hp : (t * s) ^ n = 1) : s ∈ H := by
  have hle : Subgroup.closure ((H : Set G) ∪ {s}) ≤ Subgroup.normalizer H := by
    apply (Subgroup.closure_le _).2
    intro x hx
    rcases hx with hx | hx
    · exact H.le_normalizer hx
    · have hx1 : x = s := Set.mem_singleton_iff.mp hx
      change x ∈ Subgroup.normalizer H
      rw [hx1]
      exact hN
  have htop : Subgroup.normalizer (H : Set G) = ⊤ := by
    rw [hg] at hle
    exact top_le_iff.mp hle
  letI : H.Normal := Subgroup.normalizer_eq_top_iff.mp htop
  exact mem_normal_facet H s t hs ht n hn hp

/-- An independent fourth generator contradicts the normalizer condition. -/
theorem independent_facet_obstruction (H : Subgroup G) (s t : G)
    (hg : Subgroup.closure ((H : Set G) ∪ {s}) = ⊤)
    (hN : s ∈ Subgroup.normalizer H) (hs : s ^ 2 = 1)
    (ht : t ∈ H) (n : ℕ) (hn : Odd n) (hp : (t * s) ^ n = 1)
    (hind : s ∉ H) : False := by
  exact hind (mem_facet_of_normalizer H s t hg hN hs ht n hn hp)

#print axioms eq_one_of_square_and_odd_power
#print axioms killed_by_odd_adjacent_product
#print axioms mem_normal_facet
#print axioms mem_facet_of_normalizer
#print axioms independent_facet_obstruction
end HumanCompression.DihedralFacetObstruction
