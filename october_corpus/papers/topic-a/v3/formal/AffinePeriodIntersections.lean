import QuotientIntersectionCriterion

/-!
Preservation of a subgroup intersection on passing to a smaller period kernel.
The ambient group and both subgroups are actual Lean groups/subgroups. This is
not an affine-coordinate, Schreier-presentation, lattice-index, or polytope proof.
The application must supply normal period subgroups, their containment, and the
faithfulness of the two distinguished subgroups under the point quotient.
-/
namespace MathCompression.AffinePeriodIntersections

open scoped Pointwise
open MathCompression.QuotientIntersectionCriterion

variable {G : Type*} [Group G]

/-- If a coarse period quotient preserves the intersection and both ends are
faithful under the point quotient, every smaller normal period does so too. -/
theorem quotient_inf_of_smaller_period (A B L M N : Subgroup G)
    [M.Normal] [N.Normal] (hMN : M ≤ N) (hNL : N ≤ L)
    (hA : L ⊓ A = ⊥) (hB : L ⊓ B = ⊥)
    (hN : A.map (QuotientGroup.mk' N) ⊓ B.map (QuotientGroup.mk' N) =
      (A ⊓ B).map (QuotientGroup.mk' N)) :
    A.map (QuotientGroup.mk' M) ⊓ B.map (QuotientGroup.mk' M) =
      (A ⊓ B).map (QuotientGroup.mk' M) := by
  have coarse := (quotient_inf_iff_trivial_defect A B L N hNL hA hB).mp hN
  apply (quotient_inf_iff_trivial_defect A B L M (hMN.trans hNL) hA hB).mpr
  apply Set.Subset.antisymm
  · intro x hx
    have hxN : x ∈ (N : Set G) ∩ ((L : Set G) ∩ ((A : Set G) * (B : Set G))) :=
      ⟨hMN hx.1, hx.2⟩
    rwa [coarse] at hxN
  · intro x hx
    have heq : x = 1 := Set.mem_singleton_iff.mp hx
    subst x
    refine ⟨M.one_mem, L.one_mem, ?_⟩
    simpa using Set.mul_mem_mul A.one_mem B.one_mem

/-- The same fixed test applies simultaneously to an arbitrary indexed family;
there is no finiteness assumption on the family or on the ambient group. -/
theorem quotient_family_of_one_period {I : Type*} (A B L N : Subgroup G)
    [N.Normal] (M : I → Subgroup G) [∀ i, (M i).Normal]
    (hMN : ∀ i, M i ≤ N) (hNL : N ≤ L)
    (hA : L ⊓ A = ⊥) (hB : L ⊓ B = ⊥)
    (hN : A.map (QuotientGroup.mk' N) ⊓ B.map (QuotientGroup.mk' N) =
      (A ⊓ B).map (QuotientGroup.mk' N)) :
    ∀ i, A.map (QuotientGroup.mk' (M i)) ⊓ B.map (QuotientGroup.mk' (M i)) =
      (A ⊓ B).map (QuotientGroup.mk' (M i)) := by
  intro i
  exact quotient_inf_of_smaller_period A B L (M i) N (hMN i) hNL hA hB hN

#print axioms quotient_inf_of_smaller_period
#print axioms quotient_family_of_one_period

end MathCompression.AffinePeriodIntersections
