import ParabolicProductComparison

/-!
Full marked-subgroup IP comparison under the frozen product-comparison
hypotheses. The source and image markings are connected by the actual
subgroup-closure/map identity. Redundant markings are allowed: exceptional
cases are identified by index sets, never by equality of generated subgroups.
No geometry, numerical certificate, finiteness or involution condition is
encoded here.
-/
namespace MathCompression.ParabolicMarkedComparison

open MathCompression.ParabolicProductComparison
open MathCompression.ParabolicQuotientTransport

variable {G H I : Type*} [Group G] [Group H]

def MaximalFamily (P : Set I → Subgroup G) (i : I) : Subgroup G :=
  P ({i}ᶜ)

def FullIntersection (P : Set I → Subgroup G) : Prop :=
  ∀ S T : Set I, P S ⊓ P T = P (S ∩ T)

theorem protected_of_omitted (P : Set I → Subgroup G) (e : I)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    {S : Set I} {x : G} (hx : x ∈ P S)
    (homit : ∃ i, i ≠ e ∧ i ∉ S) : Protected (MaximalFamily P) e x := by
  obtain ⟨i, hie, his⟩ := homit
  refine ⟨i, hie, hmono S ({i}ᶜ) ?_ hx⟩
  intro j hj
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
  rintro rfl
  exact his hj

/-- Reflection of membership in every proper indexed subgroup on the protected
union. The exceptional case is S={e}ᶜ, not P(S)=P({e}ᶜ). -/
theorem proper_member_image_iff (P : Set I → Subgroup G) (e : I) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily P) e x})
    (hexc : ∀ w, Footprint (MaximalFamily P) e w →
      (f w ∈ (P ({e}ᶜ)).map f ↔ w ∈ P ({e}ᶜ)))
    {S : Set I} (hS : S ≠ Set.univ) {x : G}
    (hx : Protected (MaximalFamily P) e x) :
    f x ∈ (P S).map f ↔ x ∈ P S := by
  classical
  by_cases homit : ∃ i, i ≠ e ∧ i ∉ S
  · constructor
    · intro hh
      obtain ⟨a, ha, hfa⟩ := Subgroup.mem_map.mp hh
      have hax : a = x := hinj
        (protected_footprint _ _ (protected_of_omitted P e hmono ha homit))
        (protected_footprint _ _ hx) hfa
      exact hax ▸ ha
    · intro hxi
      exact Subgroup.mem_map.mpr ⟨x, hxi, rfl⟩
  · have hSE := MathCompression.OneExceptionalParabolic.exceptional_subset e S hS homit
    rw [hSE]
    exact hexc x (protected_footprint _ _ hx)

private theorem image_meet_protected_left
    (P : Set I → Subgroup G) (e : I) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily P) e x})
    (hexc : ∀ w, Footprint (MaximalFamily P) e w →
      (f w ∈ (P ({e}ᶜ)).map f ↔ w ∈ P ({e}ᶜ)))
    (S T : Set I) (hT : T ≠ Set.univ)
    (homit : ∃ i, i ≠ e ∧ i ∉ S) :
    (P S ⊓ P T).map f = (P S).map f ⊓ (P T).map f := by
  ext y
  constructor
  · intro hy
    obtain ⟨x, hx, hfx⟩ := Subgroup.mem_map.mp hy
    exact ⟨Subgroup.mem_map.mpr ⟨x, hx.1, hfx⟩,
      Subgroup.mem_map.mpr ⟨x, hx.2, hfx⟩⟩
  · intro hy
    obtain ⟨x, hxS, hfx⟩ := Subgroup.mem_map.mp hy.1
    have hxT : x ∈ P T :=
      (proper_member_image_iff P e f hmono hinj hexc hT
        (protected_of_omitted P e hmono hxS homit)).mp (hfx.symm ▸ hy.2)
    exact Subgroup.mem_map.mpr ⟨x, ⟨hxS, hxT⟩, hfx⟩

/-- All actual source-subgroup pair intersections have exact images. This
does not assume that the source or target marking already satisfies IP. -/
theorem all_image_meets (P : Set I → Subgroup G) (e : I) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily P) e x})
    (hexc : ∀ w, Footprint (MaximalFamily P) e w →
      (f w ∈ (P ({e}ᶜ)).map f ↔ w ∈ P ({e}ᶜ))) :
    ∀ S T : Set I, (P S ⊓ P T).map f = (P S).map f ⊓ (P T).map f := by
  classical
  intro S T
  by_cases hS : S = Set.univ
  · subst S
    have hle := hmono T Set.univ (Set.subset_univ T)
    rw [inf_eq_right.mpr hle, inf_eq_right.mpr (Subgroup.map_mono hle)]
  by_cases hT : T = Set.univ
  · subst T
    have hle := hmono S Set.univ (Set.subset_univ S)
    rw [inf_eq_left.mpr hle, inf_eq_left.mpr (Subgroup.map_mono hle)]
  by_cases hpS : ∃ i, i ≠ e ∧ i ∉ S
  · exact image_meet_protected_left P e f hmono hinj hexc S T hT hpS
  by_cases hpT : ∃ i, i ≠ e ∧ i ∉ T
  · simpa [inf_comm] using
      image_meet_protected_left P e f hmono hinj hexc T S hS hpT
  have hSE := MathCompression.OneExceptionalParabolic.exceptional_subset e S hS hpS
  have hTE := MathCompression.OneExceptionalParabolic.exceptional_subset e T hT hpT
  have hST : S = T := hSE.trans hTE.symm
  simp [hST]

/-- Full IP is equivalent upstairs and on the exact subgroup images. The
family is monotone and fills its source group; no injective marking is assumed. -/
theorem full_intersection_iff (P : Set I → Subgroup G) (e : I) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily P) e x})
    (hexc : ∀ w, Footprint (MaximalFamily P) e w →
      (f w ∈ (P ({e}ᶜ)).map f ↔ w ∈ P ({e}ᶜ))) :
    FullIntersection P ↔ FullIntersection (fun S => (P S).map f) := by
  constructor
  · intro hup S T
    rw [← all_image_meets P e f hmono hinj hexc S T, hup S T]
  · intro hdown
    exact MathCompression.OneExceptionalParabolic.marked_intersection_transport
      P f e hmono htop
      (protected_injective (MaximalFamily P) e f hinj) hdown

/-- The two equivalences are supplied separately; neither is inferred from
the other. -/
theorem full_comparison (P : Set I → Subgroup G) (e : I) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily P) e x})
    (hexc : ∀ w, Footprint (MaximalFamily P) e w →
      (f w ∈ (P ({e}ᶜ)).map f ↔ w ∈ P ({e}ᶜ))) :
    (FullIntersection P ↔ FullIntersection (fun S => (P S).map f)) ∧
      (TypedCosetHelly (MaximalFamily P) ↔
        TypedCosetHelly (fun i => (MaximalFamily P i).map f)) := by
  exact ⟨full_intersection_iff P e f hmono htop hinj hexc,
    typed_helly_iff (MaximalFamily P) e f hinj hexc⟩

def MarkedSubgroup (r : I → G) (S : Set I) : Subgroup G :=
  Subgroup.closure (r '' S)

theorem marked_monotone (r : I → G) :
    ∀ S T : Set I, S ⊆ T → MarkedSubgroup r S ≤ MarkedSubgroup r T := by
  intro S T hST
  exact Subgroup.closure_mono (Set.image_mono hST)

/-- This is the actual source/image marking bridge, not an assumed matching
between arbitrary subgroup families. -/
theorem marked_map (r : I → G) (f : G →* H) (S : Set I) :
    (MarkedSubgroup r S).map f = MarkedSubgroup (fun i => f (r i)) S := by
  unfold MarkedSubgroup
  rw [MonoidHom.map_closure, Set.image_image]

/-- Both IP and typed Helly compare for the subgroups generated by an actual
marking and its elementwise image. Surjectivity is unnecessary for this theorem. -/
theorem marking_comparison (r : I → G) (e : I) (f : G →* H)
    (hgen : MarkedSubgroup r Set.univ = ⊤)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily (MarkedSubgroup r)) e x})
    (hexc : ∀ w, Footprint (MaximalFamily (MarkedSubgroup r)) e w →
      (f w ∈ (MarkedSubgroup r ({e}ᶜ)).map f ↔ w ∈ MarkedSubgroup r ({e}ᶜ))) :
    (FullIntersection (MarkedSubgroup r) ↔
      FullIntersection (MarkedSubgroup (fun i => f (r i)))) ∧
    (TypedCosetHelly (MaximalFamily (MarkedSubgroup r)) ↔
      TypedCosetHelly (MaximalFamily (MarkedSubgroup (fun i => f (r i))))) := by
  have hh := full_comparison (MarkedSubgroup r) e f (marked_monotone r) hgen hinj hexc
  have hfamilies : (fun S => (MarkedSubgroup r S).map f) =
      MarkedSubgroup (fun i => f (r i)) := by
    funext S
    exact marked_map r f S
  have hparabolics : (fun i => (MaximalFamily (MarkedSubgroup r) i).map f) =
      MaximalFamily (MarkedSubgroup (fun i => f (r i))) := by
    funext i
    exact marked_map r f ({i}ᶜ)
  rw [hfamilies, hparabolics] at hh
  exact hh

/-- When the homomorphism is onto, the image marking generates the full
target group as well. This adds the quotient hypothesis of the written theorem. -/
theorem quotient_marking_comparison (r : I → G) (e : I) (f : G →* H)
    (hgen : MarkedSubgroup r Set.univ = ⊤) (hsurj : Function.Surjective f)
    (hinj : Set.InjOn f {x | Footprint (MaximalFamily (MarkedSubgroup r)) e x})
    (hexc : ∀ w, Footprint (MaximalFamily (MarkedSubgroup r)) e w →
      (f w ∈ (MarkedSubgroup r ({e}ᶜ)).map f ↔ w ∈ MarkedSubgroup r ({e}ᶜ))) :
    MarkedSubgroup (fun i => f (r i)) Set.univ = ⊤ ∧
    (FullIntersection (MarkedSubgroup r) ↔
      FullIntersection (MarkedSubgroup (fun i => f (r i)))) ∧
    (TypedCosetHelly (MaximalFamily (MarkedSubgroup r)) ↔
      TypedCosetHelly (MaximalFamily (MarkedSubgroup (fun i => f (r i))))) := by
  refine ⟨?_, marking_comparison r e f hgen hinj hexc⟩
  rw [← marked_map r f Set.univ, hgen, Subgroup.map_top_of_surjective f hsurj]

#print axioms proper_member_image_iff
#print axioms all_image_meets
#print axioms full_intersection_iff
#print axioms full_comparison
#print axioms marked_map
#print axioms marking_comparison
#print axioms quotient_marking_comparison
end MathCompression.ParabolicMarkedComparison
