import Mathlib.Algebra.Group.Subgroup.Map

/-!+A kernel-checked intersection step for endpoint changes in marked groups.

The whole C-group recognition criterion and the geometric Helly condition are
not formalized here.  The theorem isolates its mixed-subgroup case: the two
subgroups lie in distinct automorphic copies of one maximal parabolic, whose
intersection is fixed pointwise by the automorphism.
-/

namespace EndpointDoubling

variable {G : Type*} [Group G]

/-- A fixed-point intersection controls every mixed pair of subgroups. -/
theorem mixed_intersection_of_fixed_overlap (φ : G ≃* G)
    (P R A B : Subgroup G) (hA : A ≤ P) (hB : B ≤ P)
    (hPR : P ⊓ P.map φ.toMonoidHom = R)
    (hfix : ∀ x ∈ R, φ x = x) :
    A ⊓ B.map φ.toMonoidHom = (A ⊓ B) ⊓ R := by
  apply le_antisymm
  · intro x hx
    rcases hx.2 with ⟨b, hb, hbx⟩
    have hxR : x ∈ R := by
      rw [← hPR]
      exact ⟨hA hx.1, ⟨b, hB hb, hbx⟩⟩
    have hbeq : b = x := φ.injective (hbx.trans (hfix x hxR).symm)
    exact ⟨⟨hx.1, hbeq ▸ hb⟩, hxR⟩
  · intro x hx
    exact ⟨hx.1.1, ⟨x, hx.1.2, hfix x hx.2⟩⟩

/-- In a marked-family application, two known restrictions to the overlap
and their meet identify the expected common marked subgroup. -/
theorem mixed_intersection_identified (φ : G ≃* G)
    (P R A B A₀ B₀ C : Subgroup G) (hA : A ≤ P) (hB : B ≤ P)
    (hPR : P ⊓ P.map φ.toMonoidHom = R)
    (hfix : ∀ x ∈ R, φ x = x)
    (hAR : A ⊓ R = A₀) (hBR : B ⊓ R = B₀) (hC : A₀ ⊓ B₀ = C) :
    A ⊓ B.map φ.toMonoidHom = C := by
  rw [mixed_intersection_of_fixed_overlap φ P R A B hA hB hPR hfix]
  rw [← hC, ← hAR, ← hBR]
  exact le_antisymm
    (fun _ h => ⟨⟨h.1.1, h.2⟩, ⟨h.1.2, h.2⟩⟩)
    (fun _ h => ⟨⟨h.1.1, h.2.1⟩, h.1.2⟩)

#print axioms mixed_intersection_of_fixed_overlap
#print axioms mixed_intersection_identified

end EndpointDoubling
