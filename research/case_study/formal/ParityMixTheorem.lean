import ParityMixIntersections

/-!
The source-hypothesis theorem for the actual marked parity mix. This proves
full intersection property and its intrinsic version in the generated
subgroup. The interval profiles, component decompositions, refinement
identities and interval cancellation are derived, not assumed.
-/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {n : ℕ} {E G A : Type*} [Group E] [Group G] [CommGroup A]

/-- The actual paired marking has the full intersection property under
the source hypotheses. Two-primary E suffices; no additional finiteness,
common-quotient, mixed-profile, or mixed-IP hypothesis is needed. -/
theorem marked_parity_mix_intersection (e : Fin n → E) (g : Fin n → G)
    (hE : IsPGroup 2 E) (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* A) (δ : G →* A) (t : A) (ht : t ≠ 1)
    (hε : ∀ i, ε (e i) = t) (hδ : ∀ i, δ (g i) = t)
    (hodd : ∀ i j, i.val + 1 = j.val → Odd (orderOf (g i * g j)))
    (hstringE : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (e i) (e j))
    (hstringG : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (g i) (g j))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (S T : Finset (Fin n)) :
    marked (fun i => (e i, g i)) S ⊓ marked (fun i => (e i, g i)) T =
      marked (fun i => (e i, g i)) (S ∩ T) := by
  classical
  have hlocal := interval_support_profile e g hE he hg ε δ t ht hε hδ hodd
  have h := parity_overlap_intersection e g ε δ hipE hipG hlocal
    (fun C : supportComponents S => (C : Finset (Fin n)))
    (fun D : supportComponents T => (D : Finset (Fin n)))
    (component_index_ordConnected S) (component_index_ordConnected T)
    (supportComponents_disjoint S) (supportComponents_disjoint T)
    (component_string_comm e S hstringE) (component_string_comm g S hstringG)
    (component_string_comm e T hstringE) (component_string_comm g T hstringG)
  rw [component_subtype_cover S, component_subtype_cover T] at h
  exact h

/-- The literal generators viewed inside their actual generated subgroup. -/
def mixedMarker (e : Fin n → E) (g : Fin n → G) (i : Fin n) : mix e g :=
  ⟨(e i, g i), pair_mem_mix e g i⟩

/-- The intrinsic marker family generates the mix; generation is part
of the construction, not a conclusion about the ambient direct product. -/
theorem mixedMarker_generation (e : Fin n → E) (g : Fin n → G) :
    Subgroup.closure (Set.range (mixedMarker e g)) = ⊤ := by
  apply Subgroup.map_injective (mix e g).subtype_injective
  rw [MonoidHom.map_closure, ← Set.range_comp]
  change mix e g = _
  rw [← MonoidHom.range_eq_map, Subgroup.range_subtype]

/-- The ambient intersection equality is transported to the actual
mixed group through its injective subtype map. -/
theorem intrinsic_parity_mix_intersection (e : Fin n → E) (g : Fin n → G)
    (hE : IsPGroup 2 E) (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* A) (δ : G →* A) (t : A) (ht : t ≠ 1)
    (hε : ∀ i, ε (e i) = t) (hδ : ∀ i, δ (g i) = t)
    (hodd : ∀ i j, i.val + 1 = j.val → Odd (orderOf (g i * g j)))
    (hstringE : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (e i) (e j))
    (hstringG : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (g i) (g j))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (S T : Finset (Fin n)) :
    marked (mixedMarker e g) S ⊓ marked (mixedMarker e g) T =
      marked (mixedMarker e g) (S ∩ T) := by
  apply Subgroup.map_injective (mix e g).subtype_injective
  rw [Subgroup.map_inf _ _ _ (mix e g).subtype_injective, marked_map, marked_map, marked_map]
  exact marked_parity_mix_intersection e g hE he hg ε δ t ht hε hδ hodd
    hstringE hstringG hipE hipG S T

/-- The actual mixed generators are nonidentity involutions when the
input generators square to one and a genuine character distinguishes them. -/
theorem mixedMarker_involutions (e : Fin n → E) (g : Fin n → G)
    (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* A) (t : A) (ht : t ≠ 1) (hε : ∀ i, ε (e i) = t) (i : Fin n) :
    mixedMarker e g i * mixedMarker e g i = 1 ∧ mixedMarker e g i ≠ 1 := by
  constructor
  · apply Subtype.ext
    exact Prod.ext (he i) (hg i)
  · intro hi
    have hei : e i = 1 := congrArg (fun z : mix e g => z.val.1) hi
    have hv := hε i
    rw [hei, map_one] at hv
    exact ht hv.symm

/-- Distant commutation holds inside the actual mixed group. -/
theorem mixedMarker_string (e : Fin n → E) (g : Fin n → G)
    (hstringE : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (e i) (e j))
    (hstringG : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (g i) (g j))
    (i j : Fin n) (hij : i.val + 1 < j.val ∨ j.val + 1 < i.val) :
    Commute (mixedMarker e g i) (mixedMarker e g j) := by
  apply Subtype.ext
  exact Prod.ext (hstringE i j hij).eq (hstringG i j hij).eq

#print axioms marked_parity_mix_intersection
#print axioms mixedMarker_generation
#print axioms intrinsic_parity_mix_intersection
#print axioms mixedMarker_involutions
#print axioms mixedMarker_string

end MathCompression.ParityMix
