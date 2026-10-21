import Mathlib.Algebra.Group.Subgroup.Ker

namespace LocallyFaithfulIntersection

variable {U H G : Type*} [Group U] [Group H] [Group G]

/-- The quotient intersection is controlled by discrepancies between the unique
    lifts in the two end groups. The topological computation of those
    discrepancies is deliberately outside this theorem. -/
theorem quotient_intersection_iff
    (A B C : Subgroup U) (hCA : C ≤ A) (hCB : C ≤ B)
    (f : U →* G) (q : U →* H) (p : H →* G)
    (hf : p.comp q = f)
    (hA : Set.InjOn f A) :
    A.map q ⊓ B.map q = C.map q ↔
      ∀ a ∈ A, ∀ b ∈ B, f a = f b →
        f a ∉ C.map f → q (a * b⁻¹) ≠ 1 := by
  constructor
  · intro heq a ha b hb hab hout hkill
    have hqab : q a = q b := by
      have ht : q a * (q b)⁻¹ = 1 := by simpa using hkill
      exact mul_inv_eq_one.mp ht
    have hai : q a ∈ A.map q ⊓ B.map q := by
      constructor
      · exact ⟨a, ha, rfl⟩
      · exact ⟨b, hb, hqab.symm⟩
    rw [heq] at hai
    obtain ⟨c, hc, hqc⟩ := hai
    have hfc : f c = f a := by
      have ht := congrArg p hqc
      simpa only [← hf, MonoidHom.comp_apply] using ht
    exact hout ⟨c, hc, hfc⟩
  · intro hsep
    apply le_antisymm
    · intro x hx
      obtain ⟨a, ha, hqa⟩ := hx.1
      obtain ⟨b, hb, hqb⟩ := hx.2
      have hqab : q a = q b := hqa.trans hqb.symm
      have hfab : f a = f b := by
        have ht := congrArg p hqab
        simpa only [← hf, MonoidHom.comp_apply] using ht
      have hfa : f a ∈ C.map f := by
        by_contra hout
        apply hsep a ha b hb hfab hout
        simp [map_mul, map_inv, hqab]
      obtain ⟨c, hc, hfc⟩ := hfa
      have hca : c = a := hA (hCA hc) ha hfc
      exact ⟨a, hca ▸ hc, hqa⟩
    · intro x hx
      obtain ⟨c, hc, hqc⟩ := hx
      exact ⟨⟨c, hCA hc, hqc⟩, ⟨c, hCB hc, hqc⟩⟩

/-- Faithfulness of the map to the base group prevents a quotient over the base
    from killing any nonidentity element of an end group. -/
theorem quotient_faithful_on_end
    (A : Subgroup U) (f : U →* G) (q : U →* H) (p : H →* G)
    (hf : p.comp q = f) (hA : Set.InjOn f A) : Set.InjOn q A := by
  intro a ha b hb hab
  apply hA ha hb
  have ht := congrArg p hab
  simpa only [← hf, MonoidHom.comp_apply] using ht

/-- In a quotient diagram, imposed relations persist exactly in the quotient
    direction: the first kernel is contained in the composite kernel. -/
theorem quotient_kernel_containment (q : U →* H) (p : H →* G) :
    q.ker ≤ (p.comp q).ker := by
  intro x hx
  change p (q x) = 1
  change q x = 1 at hx
  rw [hx, map_one]

#print axioms quotient_intersection_iff
#print axioms quotient_faithful_on_end
#print axioms quotient_kernel_containment
end LocallyFaithfulIntersection
