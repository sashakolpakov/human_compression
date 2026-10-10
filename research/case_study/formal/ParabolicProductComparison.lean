import OneExceptionalParabolic

/-!
Typed-coset Helly comparison from injectivity on products of protected
parabolics and exact membership in one exceptional parabolic. Neither the
groups nor the type set need be finite. No global surjectivity is assumed.
This module does not encode the marked-subgroup IP equivalence or any geometry.
-/
namespace MathCompression.ParabolicProductComparison

open MathCompression.ParabolicQuotientTransport

variable {G H I : Type*} [Group G] [Group H]

def Protected (P : I → Subgroup G) (e : I) (x : G) : Prop :=
  ∃ i, i ≠ e ∧ x ∈ P i

def Footprint (P : I → Subgroup G) (e : I) (x : G) : Prop :=
  ∃ a, Protected P e a ∧ ∃ b, Protected P e b ∧ x = a * b

def ProductMember (A B : Subgroup G) (x : G) : Prop :=
  ∃ a ∈ A, ∃ b ∈ B, x = a * b

theorem protected_footprint (P : I → Subgroup G) (e : I) {x : G}
    (hx : Protected P e x) : Footprint P e x := by
  obtain ⟨i, hie, hxi⟩ := hx
  exact ⟨x, ⟨i, hie, hxi⟩, 1, ⟨i, hie, (P i).one_mem⟩, by simp⟩

theorem protected_inv (P : I → Subgroup G) (e : I) {x : G}
    (hx : Protected P e x) : Protected P e x⁻¹ := by
  obtain ⟨i, hie, hxi⟩ := hx
  exact ⟨i, hie, (P i).inv_mem hxi⟩

theorem member_image_iff (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x})
    (hexc : ∀ w, Footprint P e w →
      (f w ∈ (P e).map f ↔ w ∈ P e))
    {x : G} (hx : Protected P e x) (i : I) :
    f x ∈ (P i).map f ↔ x ∈ P i := by
  classical
  by_cases hie : i = e
  · subst i
    exact hexc x (protected_footprint P e hx)
  constructor
  · intro hh
    obtain ⟨a, ha, hfa⟩ := Subgroup.mem_map.mp hh
    have hax : a = x := hinj
      (protected_footprint P e ⟨i, hie, ha⟩)
      (protected_footprint P e hx) hfa
    exact hax ▸ ha
  · intro hxi
    exact Subgroup.mem_map.mpr ⟨x, hxi, rfl⟩

theorem protected_injective (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x}) :
    ∀ i, i ≠ e → Set.InjOn f (P i) := by
  intro i hie a ha b hb hh
  exact hinj (protected_footprint P e ⟨i, hie, ha⟩)
    (protected_footprint P e ⟨i, hie, hb⟩) hh

theorem image_meet (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x})
    (hexc : ∀ w, Footprint P e w →
      (f w ∈ (P e).map f ↔ w ∈ P e)) (i j : I) :
    (P i ⊓ P j).map f = (P i).map f ⊓ (P j).map f := by
  classical
  by_cases hij : i = j
  · subst j
    simp
  ext y
  constructor
  · intro hy
    obtain ⟨x, hx, hfx⟩ := Subgroup.mem_map.mp hy
    exact ⟨Subgroup.mem_map.mpr ⟨x, hx.1, hfx⟩,
      Subgroup.mem_map.mpr ⟨x, hx.2, hfx⟩⟩
  · intro hy
    by_cases hie : i = e
    · have hje : j ≠ e := fun hh => hij (hie.trans hh.symm)
      obtain ⟨x, hxj, hfx⟩ := Subgroup.mem_map.mp hy.2
      have hxi : x ∈ P i :=
        (member_image_iff P e f hinj hexc ⟨j, hje, hxj⟩ i).mp (hfx.symm ▸ hy.1)
      exact Subgroup.mem_map.mpr ⟨x, ⟨hxi, hxj⟩, hfx⟩
    · obtain ⟨x, hxi, hfx⟩ := Subgroup.mem_map.mp hy.1
      have hxj : x ∈ P j :=
        (member_image_iff P e f hinj hexc ⟨i, hie, hxi⟩ j).mp (hfx.symm ▸ hy.2)
      exact Subgroup.mem_map.mpr ⟨x, ⟨hxi, hxj⟩, hfx⟩

theorem product_comparison (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x})
    (hexc : ∀ w, Footprint P e w →
      (f w ∈ (P e).map f ↔ w ∈ P e))
    {g : G} (hg : Protected P e g) (i j : I) (hij : i ≠ j) :
    ProductMember ((P i).map f) ((P j).map f) (f g) ↔
      ProductMember (P i) (P j) g := by
  classical
  constructor
  · rintro ⟨aa, haa, bb, hbb, hprod⟩
    obtain ⟨a, ha, hfa⟩ := Subgroup.mem_map.mp haa
    obtain ⟨b, hb, hfb⟩ := Subgroup.mem_map.mp hbb
    have heq : f g = f a * f b := by simpa [hfa, hfb] using hprod
    by_cases hie : i = e
    · subst i
      have hje : j ≠ e := Ne.symm hij
      have hfoot : Footprint P e (g * b⁻¹) :=
        ⟨g, hg, b⁻¹, protected_inv P e ⟨j, hje, hb⟩, rfl⟩
      have hm : f (g * b⁻¹) ∈ (P e).map f := by
        have hh : f (g * b⁻¹) = f a := by simp [map_mul, map_inv, heq, mul_assoc]
        rw [hh]
        exact Subgroup.mem_map.mpr ⟨a, ha, rfl⟩
      exact ⟨g * b⁻¹, (hexc _ hfoot).mp hm, b, hb, by simp [mul_assoc]⟩
    by_cases hje : j = e
    · subst j
      have hfoot : Footprint P e (a⁻¹ * g) :=
        ⟨a⁻¹, protected_inv P e ⟨i, hie, ha⟩, g, hg, rfl⟩
      have hm : f (a⁻¹ * g) ∈ (P e).map f := by
        have hh : f (a⁻¹ * g) = f b := by simp [map_mul, map_inv, heq]
        rw [hh]
        exact Subgroup.mem_map.mpr ⟨b, hb, rfl⟩
      exact ⟨a, ha, a⁻¹ * g, (hexc _ hfoot).mp hm, by simp⟩
    have heq' : g = a * b := hinj (protected_footprint P e hg)
      ⟨a, ⟨i, hie, ha⟩, b, ⟨j, hje, hb⟩, rfl⟩ (by simpa using heq)
    exact ⟨a, ha, b, hb, heq'⟩
  · rintro ⟨a, ha, b, hb, hprod⟩
    exact ⟨f a, Subgroup.mem_map.mpr ⟨a, ha, rfl⟩,
      f b, Subgroup.mem_map.mpr ⟨b, hb, rfl⟩, by simp [hprod]⟩

theorem coset_pair_iff_product (A B : Subgroup G) (g h : G) :
    (∃ x, x * g⁻¹ ∈ A ∧ x * h⁻¹ ∈ B) ↔
      ProductMember A B (g * h⁻¹) := by
  constructor
  · rintro ⟨x, hxg, hxh⟩
    refine ⟨(x * g⁻¹)⁻¹, A.inv_mem hxg, x * h⁻¹, hxh, ?_⟩
    group
  · rintro ⟨a, ha, b, hb, heq⟩
    refine ⟨a⁻¹ * g, ?_, ?_⟩
    · simpa [mul_assoc] using A.inv_mem ha
    · have hh : a⁻¹ * g * h⁻¹ = b := by
        calc
          a⁻¹ * g * h⁻¹ = a⁻¹ * (g * h⁻¹) := by group
          _ = a⁻¹ * (a * b) := by rw [heq]
          _ = b := by group
      simpa [hh] using hb

/- The descent proof uses a single protected anchor and choice of representatives;
it does not induct on the number of types. -/
theorem typed_helly_descent (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x})
    (hexc : ∀ w, Footprint P e w →
      (f w ∈ (P e).map f ↔ w ∈ P e))
    (hup : TypedCosetHelly P) :
    TypedCosetHelly (fun i => (P i).map f) := by
  classical
  intro S g hpair
  by_cases hanchor : ∃ k ∈ S, k ≠ e
  · obtain ⟨k, hk, hke⟩ := hanchor
    have hlifts : ∀ i : I, ∃ a : G, a ∈ P k ∧
        (i ∈ S → f a * g k * (g i)⁻¹ ∈ (P i).map f) := by
      intro i
      by_cases hi : i ∈ S
      · obtain ⟨x, hxi, hxk⟩ := hpair i hi k hk
        obtain ⟨a, ha, hfa⟩ := Subgroup.mem_map.mp hxk
        refine ⟨a, ha, ?_⟩
        intro _
        simpa [hfa, mul_assoc] using hxi
      · exact ⟨1, (P k).one_mem, fun hh => False.elim (hi hh)⟩
    choose a hak hai using hlifts
    have hsource : ∀ i ∈ S, ∀ j ∈ S, ∃ x : G,
        x * (a i)⁻¹ ∈ P i ∧ x * (a j)⁻¹ ∈ P j := by
      intro i hi j hj
      by_cases hij : i = j
      · subst j
        exact ⟨a i, by simp, by simp⟩
      have htarget : ∃ x : H, x * (f (a i))⁻¹ ∈ (P i).map f ∧
          x * (f (a j))⁻¹ ∈ (P j).map f := by
        obtain ⟨x, hxi, hxj⟩ := hpair i hi j hj
        refine ⟨x * (g k)⁻¹, ?_, ?_⟩
        · have hh := same_right_coset_difference ((P i).map f)
            x (f (a i) * g k) (g i) hxi (hai i hi)
          simpa [mul_assoc] using hh
        · have hh := same_right_coset_difference ((P j).map f)
            x (f (a j) * g k) (g j) hxj (hai j hj)
          simpa [mul_assoc] using hh
      have hprod := (coset_pair_iff_product ((P i).map f) ((P j).map f)
        (f (a i)) (f (a j))).mp htarget
      have hprod' : ProductMember (P i) (P j) (a i * (a j)⁻¹) :=
        (product_comparison P e f hinj hexc
          ⟨k, hke, (P k).mul_mem (hak i) ((P k).inv_mem (hak j))⟩ i j hij).mp
          (by simpa using hprod)
      exact (coset_pair_iff_product (P i) (P j) (a i) (a j)).mpr hprod'
    obtain ⟨u, hu⟩ := hup S a hsource
    refine ⟨f u * g k, ?_⟩
    intro i hi
    have hleft : f u * (f (a i))⁻¹ ∈ (P i).map f :=
      Subgroup.mem_map.mpr ⟨u * (a i)⁻¹, hu i hi, by simp⟩
    have hh := ((P i).map f).mul_mem hleft (hai i hi)
    simpa [mul_assoc] using hh
  · refine ⟨g e, ?_⟩
    intro i hi
    have hie : i = e := by
      by_contra hh
      exact hanchor ⟨i, hi, hh⟩
    subst i
    simp

/-- Exact typed-coset Helly equivalence, including infinite selected families.
Only the exceptional parabolic may have a noninjective image map. -/
theorem typed_helly_iff (P : I → Subgroup G) (e : I) (f : G →* H)
    (hinj : Set.InjOn f {x | Footprint P e x})
    (hexc : ∀ w, Footprint P e w →
      (f w ∈ (P e).map f ↔ w ∈ P e)) :
    TypedCosetHelly P ↔ TypedCosetHelly (fun i => (P i).map f) := by
  constructor
  · exact typed_helly_descent P e f hinj hexc
  · exact MathCompression.OneExceptionalParabolic.typed_helly_transport
      P f e (protected_injective P e f hinj) (image_meet P e f hinj hexc)

#print axioms member_image_iff
#print axioms image_meet
#print axioms product_comparison
#print axioms coset_pair_iff_product
#print axioms typed_helly_descent
#print axioms typed_helly_iff
end MathCompression.ParabolicProductComparison
