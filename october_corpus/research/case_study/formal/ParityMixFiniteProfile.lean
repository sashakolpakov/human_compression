import ParityMixProfile
import ParitySupportIntervals

/-! Source-hypothesis bindings for every actual finite support. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {n : ℕ} {E G D : Type*} [Group E] [Group G] [Group D]

/-- Both orientations of the marker-path adjacency have odd product
order; the reverse is the inverse product because markers are involutions. -/
theorem path_adjacent_odd (g : Fin n → G) (hg : ∀ i, g i * g i = 1)
    (hodd : ∀ i j, i.val + 1 = j.val → Odd (orderOf (g i * g j)))
    (S : Finset (Fin n)) (i j : S) (hij : pathAdjacent S i j) :
    Odd (orderOf (g i * g j)) := by
  rcases hij with hij | hji
  · exact hodd i j hij
  · have h := hodd j i hji
    have he : (g j * g i)⁻¹ = g i * g j := by
      rw [mul_inv_rev, inv_eq_of_mul_eq_one_right (hg i), inv_eq_of_mul_eq_one_right (hg j)]
    rw [← he, orderOf_inv]
    exact h

/-- Exact local profile for any order-connected support, including the
empty support. Its path hypothesis is proved from order-connectedness. -/
theorem interval_support_profile (e : Fin n → E) (g : Fin n → G)
    (hE : IsPGroup 2 E) (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* D) (δ : G →* D) (t : D) (ht : t ≠ 1)
    (hε : ∀ i, ε (e i) = t) (hδ : ∀ i, δ (g i) = t)
    (hodd : ∀ i j, i.val + 1 = j.val → Odd (orderOf (g i * g j)))
    (S : Finset (Fin n)) (hS : Set.OrdConnected (S : Set (Fin n))) (x : E × G) :
    x ∈ marked (fun i => (e i, g i)) S ↔
      x.1 ∈ marked e S ∧ x.2 ∈ marked g S ∧ ε x.1 = δ x.2 := by
  classical
  by_cases hne : S.Nonempty
  · let i₀ : S := ⟨hne.choose, hne.choose_spec⟩
    exact connected_support_profile e g hE he hg ε δ t ht hε hδ S (pathAdjacent S)
      (path_adjacent_odd g hg hodd S) i₀ (interval_path S hS i₀) x
  · have hzero : S = ∅ := Finset.not_nonempty_iff_eq_empty.mp hne
    subst S
    simp only [marked_empty, Subgroup.mem_bot]
    constructor
    · intro hx
      subst x
      simp
    · rintro ⟨hx, hy, _⟩
      exact Prod.ext hx hy

/-- The source string relations imply commutation across the actual
canonical support components. -/
theorem component_string_comm (r : Fin n → G) (S : Finset (Fin n))
    (hstring : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (r i) (r j)) :
    Pairwise fun C D : supportComponents S =>
      ∀ i ∈ (C : Finset (Fin n)), ∀ j ∈ (D : Finset (Fin n)), Commute (r i) (r j) := by
  intro C D hCD i hi j hj
  exact hstring i j (components_separated S C D hCD i j hi hj)

theorem component_subtype_cover (S : Finset (Fin n)) :
    Finset.univ.biUnion (fun C : supportComponents S => (C : Finset (Fin n))) = S := by
  classical
  calc
    Finset.univ.biUnion (fun C : supportComponents S => (C : Finset (Fin n))) =
        (supportComponents S).biUnion id := by
      ext i
      simp only [Finset.mem_biUnion, Finset.mem_univ, true_and, Subtype.exists,
        exists_prop, id_eq]
    _ = S := supportComponents_cover S

/-- The complete source parity profile on every support, using actual
canonical component coordinates and no mixed-IP premise. -/
theorem canonical_mixed_parity_profile (e : Fin n → E) (g : Fin n → G)
    (hE : IsPGroup 2 E) (he : ∀ i, e i * e i = 1) (hg : ∀ i, g i * g i = 1)
    (ε : E →* D) (δ : G →* D) (t : D) (ht : t ≠ 1)
    (hε : ∀ i, ε (e i) = t) (hδ : ∀ i, δ (g i) = t)
    (hodd : ∀ i j, i.val + 1 = j.val → Odd (orderOf (g i * g j)))
    (hstringE : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (e i) (e j))
    (hstringG : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val → Commute (g i) (g j))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (S : Finset (Fin n))
    (x : ∀ C : supportComponents S, marked e (C : Finset (Fin n)))
    (y : ∀ C : supportComponents S, marked g (C : Finset (Fin n))) :
    (componentAssembly e (fun C : supportComponents S => (C : Finset (Fin n)))
        (component_string_comm e S hstringE) x,
      componentAssembly g (fun C : supportComponents S => (C : Finset (Fin n)))
        (component_string_comm g S hstringG) y) ∈ marked (fun i => (e i, g i)) S ↔
      ∀ C, ε (x C) = δ (y C) := by
  classical
  have hprofile := mixed_component_profile e g _ (component_string_comm e S hstringE)
    (component_string_comm g S hstringG) (supportComponents_disjoint S) hipE hipG x y
  rw [component_subtype_cover S] at hprofile
  rw [hprofile]
  apply forall_congr'
  intro C
  rw [interval_support_profile e g hE he hg ε δ t ht hε hδ hodd C
    (component_index_ordConnected S C)]
  exact ⟨fun h => h.2.2, fun h => ⟨(x C).property, (y C).property, h⟩⟩

#print axioms path_adjacent_odd
#print axioms interval_support_profile
#print axioms component_string_comm
#print axioms component_subtype_cover
#print axioms canonical_mixed_parity_profile

end MathCompression.ParityMix
