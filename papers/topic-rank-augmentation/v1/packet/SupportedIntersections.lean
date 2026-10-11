import Mathlib.Algebra.Group.Subgroup.Lattice

/- The actual subgroup factorization used in the three augmentation cases.
   The permutation description, transitivity, end C properties and source
   hypotheses remain written. No string intersection property is assumed.
-/
namespace SupportedIntersections
variable {G : Type*} [Group G]

/-- Once H=N*B and B is in K, only its supported factor needs to be tested. -/
theorem intersection_iff_supported_part
    (H N B K : Subgroup G) (hNH : N ≤ H) (hBH : B ≤ H) (hBK : B ≤ K)
    (hfactor : ∀ h ∈ H, ∃ n ∈ N, ∃ b ∈ B, h = n * b) :
    H ⊓ K = B ↔ N ⊓ K ≤ B := by
  constructor
  · intro heq x hx
    have h : x ∈ H ⊓ K := ⟨hNH hx.1, hx.2⟩
    rw [heq] at h
    exact h
  · intro hsmall
    apply le_antisymm
    · intro x hx
      obtain ⟨n, hn, b, hb, heq⟩ := hfactor x hx.1
      have hnK : n ∈ K := by
        have h := K.mul_mem hx.2 (K.inv_mem (hBK hb))
        simpa [heq, mul_assoc] using h
      rw [heq]
      exact B.mul_mem (hsmall ⟨hn, hnK⟩) hb
    · intro b hb
      exact ⟨hBH hb, hBK hb⟩

/-- For a complementary supported factor, the test is trivial intersection. -/
theorem intersection_iff_trivial_supported_part
    (H N B K : Subgroup G) (hNH : N ≤ H) (hBH : B ≤ H) (hBK : B ≤ K)
    (hfactor : ∀ h ∈ H, ∃ n ∈ N, ∃ b ∈ B, h = n * b)
    (hNB : N ⊓ B = ⊥) :
    H ⊓ K = B ↔ N ⊓ K = ⊥ := by
  rw [intersection_iff_supported_part H N B K hNH hBH hBK hfactor]
  constructor
  · intro h
    apply le_antisymm
    · intro n hn
      have hb : n ∈ N ⊓ B := ⟨hn.1, h hn⟩
      rw [hNB] at hb
      exact hb
    · exact bot_le
  · intro h
    rw [h]
    exact bot_le

#print axioms intersection_iff_supported_part
#print axioms intersection_iff_trivial_supported_part
end SupportedIntersections
