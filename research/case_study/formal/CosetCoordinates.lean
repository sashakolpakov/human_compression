import RankThreeFactorization

/-!
An arbitrary family of cosets meeting a distinguished coset has a common
point when the distinguished subgroup covers every tuple of coset coordinates.
The coordinate map is a map of sets; no subgroup is assumed normal.
-/

namespace CosetCoordinates

open RankThreeFactorization

variable {G I : Type*} [Group G]

/-- Surjectivity of the map from K to the product of its coset-coordinate
sets. Each coordinate is represented by an element of K. -/
def CoversCoordinates (K : Subgroup G) (H : I → Subgroup G) : Prop :=
  ∀ k : I → G, (∀ i, k i ∈ K) →
    ∃ v ∈ K, ∀ i, (k i)⁻¹ * v ∈ H i

/-- All-rank attachment lemma, also valid for infinite index types.
Pairwise incidence among the H-cosets is not required by this lemma. -/
theorem common_point_of_coordinates (K : Subgroup G) (H : I → Subgroup G)
    (hcover : CoversCoordinates K H) (a : G) (x : I → G)
    (hmeet : ∀ i, ∃ u, InCoset K a u ∧ InCoset (H i) (x i) u) :
    ∃ z, InCoset K a z ∧ ∀ i, InCoset (H i) (x i) z := by
  classical
  choose u huK huH using hmeet
  obtain ⟨v, hvK, hvH⟩ := hcover (fun i => a⁻¹ * u i) huK
  refine ⟨a * v, ?_, ?_⟩
  · simpa [InCoset] using hvK
  · intro i
    change (x i)⁻¹ * (a * v) ∈ H i
    have h := (H i).mul_mem (huH i) (hvH i)
    have heq : ((x i)⁻¹ * u i) * ((a⁻¹ * u i)⁻¹ * v) =
        (x i)⁻¹ * (a * v) := by group
    exact heq ▸ h

/-- The coordinate hypothesis is necessary as well as sufficient for this
attachment property. This does not assert Helly for the H-family alone. -/
theorem coordinates_of_common_point (K : Subgroup G) (H : I → Subgroup G)
    (hpoint : ∀ x : I → G,
      (∀ i, ∃ u, u ∈ K ∧ InCoset (H i) (x i) u) →
      ∃ z ∈ K, ∀ i, InCoset (H i) (x i) z) :
    CoversCoordinates K H := by
  intro k hk
  apply hpoint k
  intro i
  refine ⟨k i, hk i, ?_⟩
  simp [InCoset]

end CosetCoordinates

#print axioms CosetCoordinates.common_point_of_coordinates
#print axioms CosetCoordinates.coordinates_of_common_point
