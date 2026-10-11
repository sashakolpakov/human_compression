import Mathlib.Algebra.Group.Subgroup.Ker

/- Generic restriction-image criterion. The permutation restriction map,
supported saturation and string end induction are written application steps. -/
namespace RestrictionKernelCriterion

variable {G H : Type*} [Group G] [Group H]

theorem mem_of_same_image (f : G →* H) (P Q : Subgroup G)
    (hPQ : P ≤ Q) (hker : Q ⊓ f.ker ≤ P)
    {q p : G} (hq : q ∈ Q) (hp : p ∈ P) (himage : f q = f p) : q ∈ P := by
  have hz : q * p⁻¹ ∈ P := by
    apply hker
    refine ⟨Q.mul_mem hq (Q.inv_mem (hPQ hp)), ?_⟩
    change f (q * p⁻¹) = 1
    simp [himage]
  have h := P.mul_mem hz hp
  simpa [mul_assoc] using h

theorem saturation_intersection_iff (f : G →* H) (P Q : Subgroup G)
    (hPQ : P ≤ Q) :
    Q ⊓ (P.map f).comap f = P ↔ Q ⊓ f.ker ≤ P := by
  constructor
  · intro heq q hq
    have h : q ∈ Q ⊓ (P.map f).comap f := by
      refine ⟨hq.1, ?_⟩
      change f q ∈ P.map f
      have hz : f q = 1 := hq.2
      rw [hz]
      exact (P.map f).one_mem
    rw [heq] at h
    exact h
  · intro hker
    apply le_antisymm
    · intro q hq
      obtain ⟨p, hp, heq⟩ := Subgroup.mem_map.mp hq.2
      exact mem_of_same_image f P Q hPQ hker hq.1 hp heq.symm
    · intro p hp
      exact ⟨hPQ hp, Subgroup.mem_map_of_mem f hp⟩

theorem kernel_stability_iff (f : G →* H) (P Q : Subgroup G)
    (hPQ : P ≤ Q) :
    Q ⊓ (P.map f).comap f = P ↔ Q ⊓ f.ker = P ⊓ f.ker := by
  rw [saturation_intersection_iff f P Q hPQ]
  constructor
  · intro h
    apply le_antisymm
    · intro q hq
      exact ⟨h hq, hq.2⟩
    · intro q hq
      exact ⟨hPQ hq.1, hq.2⟩
  · intro h q hq
    rw [h] at hq
    exact hq.1

#print axioms mem_of_same_image
#print axioms saturation_intersection_iff
#print axioms kernel_stability_iff
end RestrictionKernelCriterion
