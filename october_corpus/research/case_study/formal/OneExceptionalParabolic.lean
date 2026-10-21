import ParabolicQuotientTransport

/-!
Quotient transport allowing one maximal parabolic on which the quotient need
not be injective. All other hypotheses concern the actual subgroup images.
The groups and type sets may be infinite. No geometric conclusion is encoded.
-/
namespace MathCompression.OneExceptionalParabolic

open MathCompression.ParabolicQuotientTransport

variable {G H I : Type*} [Group G] [Group H]

/-- A typed coset family of at least two types has a nonexceptional anchor.
Empty and singleton families require no injectivity. -/
theorem typed_helly_transport (P : I → Subgroup G) (f : G →* H) (e : I)
    (hinj : ∀ i, i ≠ e → Set.InjOn f (P i))
    (hmeet : ∀ i j, (P i ⊓ P j).map f = (P i).map f ⊓ (P j).map f)
    (hdown : TypedCosetHelly (fun i => (P i).map f)) :
    TypedCosetHelly P := by
  classical
  intro S g hpair
  by_cases hanchor : ∃ k ∈ S, k ≠ e
  · obtain ⟨k, hk, hke⟩ := hanchor
    have hpairdown : ∀ i ∈ S, ∀ j ∈ S, ∃ x : H,
        x * (f (g i))⁻¹ ∈ (P i).map f ∧ x * (f (g j))⁻¹ ∈ (P j).map f := by
      intro i hi j hj
      obtain ⟨x, hxi, hxj⟩ := hpair i hi j hj
      refine ⟨f x, ?_, ?_⟩
      · exact Subgroup.mem_map.mpr ⟨x * (g i)⁻¹, hxi, by simp⟩
      · exact Subgroup.mem_map.mpr ⟨x * (g j)⁻¹, hxj, by simp⟩
    obtain ⟨y, hy⟩ := hdown S (fun i => f (g i)) hpairdown
    obtain ⟨t, ht, hft⟩ := Subgroup.mem_map.mp (hy k hk)
    let x := t * g k
    have hfx : f x = y := by
      dsimp [x]
      rw [map_mul, hft]
      simp [mul_assoc]
    have hxk : x * (g k)⁻¹ ∈ P k := by simpa [x, mul_assoc] using ht
    refine ⟨x, ?_⟩
    intro i hi
    obtain ⟨a, hai, hak⟩ := hpair i hi k hk
    have hxak : x * a⁻¹ ∈ P k := same_right_coset_difference (P k) x a (g k) hxk hak
    have hfai : f a * (f (g i))⁻¹ ∈ (P i).map f :=
      Subgroup.mem_map.mpr ⟨a * (g i)⁻¹, hai, by simp⟩
    have hxaimage : f (x * a⁻¹) ∈ (P i).map f ⊓ (P k).map f := by
      constructor
      · simpa [map_mul, map_inv, hfx] using
          same_right_coset_difference ((P i).map f) y (f a) (f (g i)) (hy i hi) hfai
      · exact Subgroup.mem_map.mpr ⟨x * a⁻¹, hxak, rfl⟩
    rw [← hmeet i k] at hxaimage
    obtain ⟨c, hc, hfc⟩ := Subgroup.mem_map.mp hxaimage
    have hcx : c = x * a⁻¹ := hinj k hke hc.2 hxak hfc
    have hxai : x * a⁻¹ ∈ P i := hcx ▸ hc.1
    have hh := (P i).mul_mem hxai hai
    simpa [mul_assoc] using hh
  · refine ⟨g e, ?_⟩
    intro i hi
    have hie : i = e := by
      by_contra hh
      exact hanchor ⟨i, hi, hh⟩
    subst i
    simp

/-- A proper subset omitting no nonexceptional type is exactly the exceptional
maximal subset. This does not require a finite type set. -/
theorem exceptional_subset (e : I) (S : Set I) (hS : S ≠ Set.univ)
    (hno : ¬ ∃ i, i ≠ e ∧ i ∉ S) : S = ({e}ᶜ : Set I) := by
  classical
  have he : e ∉ S := by
    intro hes
    apply hS
    apply Set.eq_univ_of_forall
    intro i
    by_cases hie : i = e
    · simpa [hie] using hes
    · by_contra his
      exact hno ⟨i, hie, his⟩
  ext i
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
  constructor
  · intro hi hie
    subst i
    exact he hi
  · intro hie
    by_contra his
    exact hno ⟨i, hie, his⟩

private theorem meet_of_injective_left (P : Set I → Subgroup G) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f)
    (S T : Set I) (hinj : Set.InjOn f (P S)) : P S ⊓ P T = P (S ∩ T) := by
  apply le_antisymm
  · intro x hx
    have hfx : f x ∈ (P S).map f ⊓ (P T).map f :=
      ⟨Subgroup.mem_map.mpr ⟨x, hx.1, rfl⟩, Subgroup.mem_map.mpr ⟨x, hx.2, rfl⟩⟩
    rw [himages] at hfx
    obtain ⟨c, hc, hfc⟩ := Subgroup.mem_map.mp hfx
    have hcx : c = x := hinj (hmono _ _ Set.inter_subset_left hc) hx.1 hfc
    exact hcx ▸ hc
  · exact le_inf (hmono _ _ Set.inter_subset_left) (hmono _ _ Set.inter_subset_right)

/-- Image IP lifts when all but one maximal marked parabolic are injective.
The only unprotected proper subset is the exceptional maximal one; its meet
with itself is tautological. -/
theorem marked_intersection_transport (P : Set I → Subgroup G) (f : G →* H) (e : I)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : ∀ i : I, i ≠ e → Set.InjOn f (P ({i}ᶜ)))
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f) :
    ∀ S T : Set I, P S ⊓ P T = P (S ∩ T) := by
  classical
  have hprotected : ∀ S : Set I, (∃ i, i ≠ e ∧ i ∉ S) → Set.InjOn f (P S) := by
    intro S ⟨i, hie, hi⟩
    have hsub : S ⊆ ({i}ᶜ : Set I) := by
      intro j hj
      simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
      rintro rfl
      exact hi hj
    exact fun _ hx _ hy hh => hinj i hie (hmono _ _ hsub hx) (hmono _ _ hsub hy) hh
  intro S T
  by_cases hS : S = Set.univ
  · simp [hS, htop]
  by_cases hT : T = Set.univ
  · simp [hT, htop]
  by_cases hpS : ∃ i, i ≠ e ∧ i ∉ S
  · exact meet_of_injective_left P f hmono himages S T (hprotected S hpS)
  by_cases hpT : ∃ i, i ≠ e ∧ i ∉ T
  · simpa [inf_comm, Set.inter_comm] using
      meet_of_injective_left P f hmono himages T S (hprotected T hpT)
  have hST : S = T := (exceptional_subset e S hS hpS).trans (exceptional_subset e T hT hpT).symm
  simp [hST]

/-- Combined one-exceptional-maximal quotient transport. -/
theorem marked_quotient_transport (P : Set I → Subgroup G) (f : G →* H) (e : I)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : ∀ i : I, i ≠ e → Set.InjOn f (P ({i}ᶜ)))
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f)
    (hhelly : TypedCosetHelly (fun i : I => (P ({i}ᶜ)).map f)) :
    (∀ S T : Set I, P S ⊓ P T = P (S ∩ T)) ∧
      TypedCosetHelly (fun i : I => P ({i}ᶜ)) := by
  have hip := marked_intersection_transport P f e hmono htop hinj himages
  refine ⟨hip, typed_helly_transport (fun i : I => P ({i}ᶜ)) f e hinj ?_ hhelly⟩
  intro i j
  rw [hip]
  exact (himages _ _).symm

#print axioms typed_helly_transport
#print axioms exceptional_subset
#print axioms marked_intersection_transport
#print axioms marked_quotient_transport
end MathCompression.OneExceptionalParabolic
