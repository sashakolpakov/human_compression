import ParityMixComponents

/-! The connected parity fiber attached to an actual marked parabolic. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration
open MathCompression.CoprimePullback

variable {I E G D : Type*} [Group E] [Group G] [Group D]

def localMarker (r : I → G) (S : Finset I) (i : S) : marked r S :=
  ⟨r i, Subgroup.subset_closure ⟨i, i.property, rfl⟩⟩

theorem localMarker_generation (r : I → G) (S : Finset I) :
    Subgroup.closure (Set.range (localMarker r S)) = ⊤ := by
  apply Subgroup.map_injective (marked r S).subtype_injective
  rw [MonoidHom.map_closure, ← Set.range_comp]
  have hr : Set.range ((marked r S).subtype ∘ localMarker r S) = r '' (S : Set I) := by
    ext x
    constructor
    · rintro ⟨i, rfl⟩
      exact ⟨i, i.property, rfl⟩
    · rintro ⟨i, hi, rfl⟩
      exact ⟨⟨i, hi⟩, rfl⟩
  rw [hr]
  change marked r S = _
  rw [← MonoidHom.range_eq_map, Subgroup.range_subtype]

/-- The local paired closure maps onto exactly the ambient marked
subgroup on that support, not an assumed abstract mix. -/
theorem local_mix_map (e : I → E) (g : I → G) (S : Finset I) :
    (mix (localMarker e S) (localMarker g S)).map
      ((marked e S).subtype.prodMap (marked g S).subtype) =
      marked (fun i => (e i, g i)) S := by
  unfold mix marked
  rw [MonoidHom.map_closure, ← Set.range_comp]
  congr 1
  ext x
  constructor
  · rintro ⟨i, rfl⟩
    exact ⟨i, i.property, rfl⟩
  · rintro ⟨i, hi, rfl⟩
    exact ⟨⟨i, hi⟩, rfl⟩

/-- Every connected support has the exact parity-fiber profile in the
original ambient product. The path, power, local generation and genuine
character hypotheses are discharged for the actual marked parabolics. -/
theorem connected_support_profile (e : I → E) (g : I → G)
    (hE : IsPGroup 2 E) (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* D) (δ : G →* D) (t : D) (ht : t ≠ 1)
    (hε : ∀ i, ε (e i) = t) (hδ : ∀ i, δ (g i) = t)
    (S : Finset I) (R : S → S → Prop)
    (hodd : ∀ i j, R i j → Odd (orderOf (g i * g j)))
    (i₀ : S) (hconn : ∀ i, Relation.ReflTransGen R i₀ i) (x : E × G) :
    x ∈ marked (fun i => (e i, g i)) S ↔
      x.1 ∈ marked e S ∧ x.2 ∈ marked g S ∧ ε x.1 = δ x.2 := by
  have helocal : ∀ i : S, localMarker e S i * localMarker e S i = 1 := by
    intro i
    apply Subtype.ext
    exact he i
  have hglocal : ∀ i : S, localMarker g S i * localMarker g S i = 1 := by
    intro i
    apply Subtype.ext
    exact hg i
  have hoddlocal : ∀ i j : S, R i j →
      Odd (orderOf (localMarker g S i * localMarker g S j)) := by
    intro i j hij
    rw [← Subgroup.orderOf_coe]
    exact hodd i j hij
  have hfiber := connected_parity_fiber (localMarker e S) (localMarker g S)
    (hE.to_subgroup (marked e S)) helocal hglocal
    (localMarker_generation e S) (localMarker_generation g S)
    (ε.comp (marked e S).subtype) (δ.comp (marked g S).subtype) t ht
    (fun i => hε i) (fun i => hδ i) R hoddlocal i₀ hconn
  rw [← local_mix_map e g S, hfiber]
  constructor
  · rintro ⟨⟨u, v⟩, huv, heq⟩
    cases heq
    exact ⟨u.property, v.property, huv⟩
  · rintro ⟨hx, hy, hpar⟩
    exact ⟨(⟨x.1, hx⟩, ⟨x.2, hy⟩), hpar, rfl⟩

#print axioms localMarker_generation
#print axioms local_mix_map
#print axioms connected_support_profile

end MathCompression.ParityMix
