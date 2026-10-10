import Mathlib.Order.Interval.Set.OrdConnectedComponent
import Mathlib.Tactic

/-! Canonical finite interval components of a marked support. -/

namespace MathCompression.ParityMix

variable {I : Type*} [LinearOrder I]

noncomputable def supportComponent (S : Finset I) (i : I) : Finset I := by
  classical
  exact S.filter (fun j => j ∈ Set.ordConnectedComponent (S : Set I) i)

@[simp] theorem mem_supportComponent (S : Finset I) (i j : I) :
    j ∈ supportComponent S i ↔ j ∈ Set.ordConnectedComponent (S : Set I) i := by
  classical
  simp only [supportComponent, Finset.mem_filter]
  exact ⟨And.right, fun h => ⟨Set.ordConnectedComponent_subset h, h⟩⟩

@[simp] theorem coe_supportComponent (S : Finset I) (i : I) :
    (supportComponent S i : Set I) = Set.ordConnectedComponent (S : Set I) i := by
  ext j
  exact mem_supportComponent S i j

noncomputable def supportComponents (S : Finset I) : Finset (Finset I) :=
  S.image (supportComponent S)

theorem supportComponent_subset (S : Finset I) (i : I) : supportComponent S i ⊆ S := by
  intro j hj
  exact Set.ordConnectedComponent_subset ((mem_supportComponent S i j).mp hj)

theorem supportComponent_nonempty (S : Finset I) {i : I} (hi : i ∈ S) :
    (supportComponent S i).Nonempty := by
  exact ⟨i, (mem_supportComponent S i i).mpr (Set.self_mem_ordConnectedComponent.mpr hi)⟩

theorem supportComponent_ordConnected (S : Finset I) (i : I) :
    Set.OrdConnected (supportComponent S i : Set I) := by
  rw [coe_supportComponent]
  infer_instance

/-- A point common to two canonical components identifies them. -/
theorem supportComponent_eq_of_overlap (S : Finset I) {i j x : I}
    (hi : x ∈ supportComponent S i) (hj : x ∈ supportComponent S j) :
    supportComponent S i = supportComponent S j := by
  apply Finset.coe_injective
  rw [coe_supportComponent, coe_supportComponent]
  have hix := (mem_supportComponent S i x).mp hi
  have hxj := Set.mem_ordConnectedComponent_comm.mp ((mem_supportComponent S j x).mp hj)
  exact Set.ordConnectedComponent_eq (Set.mem_ordConnectedComponent_trans hix hxj)

/-- The actual finite support is the union of its canonical components. -/
theorem supportComponents_cover (S : Finset I) :
    (supportComponents S).biUnion id = S := by
  classical
  ext i
  constructor
  · intro hi
    obtain ⟨C, hC, hiC⟩ := Finset.mem_biUnion.mp hi
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.mp hC
    exact supportComponent_subset S j hiC
  · intro hi
    apply Finset.mem_biUnion.mpr
    refine ⟨supportComponent S i, Finset.mem_image.mpr ⟨i, hi, rfl⟩, ?_⟩
    exact (mem_supportComponent S i i).mpr (Set.self_mem_ordConnectedComponent.mpr hi)

/-- Distinct canonical components are disjoint, with no graph premise. -/
theorem supportComponents_disjoint (S : Finset I) :
    Pairwise fun C D : supportComponents S => Disjoint (C : Finset I) (D : Finset I) := by
  intro C D hCD
  apply Finset.disjoint_left.mpr
  intro x hxC hxD
  obtain ⟨i, hi, hCi⟩ := Finset.mem_image.mp C.property
  obtain ⟨j, hj, hDj⟩ := Finset.mem_image.mp D.property
  apply hCD
  apply Subtype.ext
  rw [← hCi, ← hDj]
  apply supportComponent_eq_of_overlap S
  · rwa [hCi]
  · rwa [hDj]

theorem component_index_nonempty (S : Finset I) (C : supportComponents S) :
    (C : Finset I).Nonempty := by
  obtain ⟨i, hi, hCi⟩ := Finset.mem_image.mp C.property
  rw [← hCi]
  exact supportComponent_nonempty S hi

theorem component_index_ordConnected (S : Finset I) (C : supportComponents S) :
    Set.OrdConnected (C : Set I) := by
  obtain ⟨i, hi, hCi⟩ := Finset.mem_image.mp C.property
  rw [← hCi]
  exact supportComponent_ordConnected S i

#print axioms supportComponent_eq_of_overlap
#print axioms supportComponents_cover
#print axioms supportComponents_disjoint
#print axioms component_index_nonempty
#print axioms component_index_ordConnected

/-- The canonical component containing a point of a component is that
component itself. -/
theorem supportComponent_eq_component (S : Finset I) (C : supportComponents S)
    {i : I} (hi : i ∈ (C : Finset I)) : supportComponent S i = C := by
  obtain ⟨j, hj, hCj⟩ := Finset.mem_image.mp C.property
  have hiS : i ∈ S := by
    apply supportComponent_subset S j
    rwa [hCj]
  rw [← hCj]
  apply supportComponent_eq_of_overlap S
  · exact (mem_supportComponent S i i).mpr (Set.self_mem_ordConnectedComponent.mpr hiS)
  · rwa [hCj]

def pathAdjacent {n : ℕ} (S : Finset (Fin n)) (i j : S) : Prop :=
  (i : Fin n).val + 1 = (j : Fin n).val ∨ (j : Fin n).val + 1 = (i : Fin n).val

/-- Every two points in a finite integer interval are joined by actual
successor steps lying in the interval. -/
theorem interval_forward_path {n : ℕ} (S : Finset (Fin n))
    (hS : Set.OrdConnected (S : Set (Fin n))) (i j : S)
    (hij : (i : Fin n).val ≤ (j : Fin n).val) :
    Relation.ReflTransGen (pathAdjacent S) i j := by
  have hwalk : ∀ k : ℕ, (i : Fin n).val ≤ k →
      ∀ hk : k < n, ∀ hm : (⟨k, hk⟩ : Fin n) ∈ S,
        Relation.ReflTransGen (pathAdjacent S) i ⟨⟨k, hk⟩, hm⟩ := by
    intro k hik
    induction k, hik using Nat.le_induction with
    | base =>
      intro hk hm
      have he : (⟨⟨(i : Fin n).val, hk⟩, hm⟩ : S) = i := by
        apply Subtype.ext
        apply Fin.ext
        rfl
      rw [he]
    | succ k hik ih =>
      intro hk hm
      have hkn : k < n := by omega
      have hmem : (⟨k, hkn⟩ : Fin n) ∈ S :=
        hS.out i.property hm ⟨hik, by change k ≤ k + 1; omega⟩
      apply (ih hkn hmem).tail
      exact Or.inl rfl
  simpa using hwalk (j : Fin n).val hij (j : Fin n).isLt j.property

theorem interval_path {n : ℕ} (S : Finset (Fin n))
    (hS : Set.OrdConnected (S : Set (Fin n))) (i j : S) :
    Relation.ReflTransGen (pathAdjacent S) i j := by
  rcases le_total (i : Fin n).val (j : Fin n).val with hij | hji
  · exact interval_forward_path S hS i j hij
  · have hrev := interval_forward_path S hS j i hji
    clear hji
    induction hrev with
    | refl => exact .refl
    | @tail a b hab habstep ih =>
      exact ih.head (Or.symm habstep)

/-- Markers from distinct canonical components are separated by more
than one step on the marker path. -/
theorem components_separated {n : ℕ} (S : Finset (Fin n))
    (C D : supportComponents S) (hCD : C ≠ D)
    (i j : Fin n) (hi : i ∈ (C : Finset (Fin n))) (hj : j ∈ (D : Finset (Fin n))) :
    i.val + 1 < j.val ∨ j.val + 1 < i.val := by
  by_contra hsep
  have hiS : i ∈ S := by
    rw [← supportComponents_cover S]
    exact Finset.mem_biUnion.mpr ⟨C, C.property, hi⟩
  have hjS : j ∈ S := by
    rw [← supportComponents_cover S]
    exact Finset.mem_biUnion.mpr ⟨D, D.property, hj⟩
  have hbetween : Set.uIcc i j ⊆ (S : Set (Fin n)) := by
    intro k hk
    have hvals : (i.val ≤ k.val ∧ k.val ≤ j.val) ∨
        (j.val ≤ k.val ∧ k.val ≤ i.val) := by
      exact (Set.mem_uIcc.mp hk).imp (fun h => ⟨h.1, h.2⟩) (fun h => ⟨h.1, h.2⟩)
    have he : k = i ∨ k = j := by
      have hv : k.val = i.val ∨ k.val = j.val := by omega
      exact hv.imp Fin.ext Fin.ext
    rcases he with rfl | rfl
    · exact hiS
    · exact hjS
  have hc : supportComponent S i = supportComponent S j := by
    apply Finset.coe_injective
    rw [coe_supportComponent, coe_supportComponent]
    exact Set.ordConnectedComponent_eq hbetween
  rw [supportComponent_eq_component S C hi, supportComponent_eq_component S D hj] at hc
  exact hCD (Subtype.ext hc)

#print axioms supportComponent_eq_component
#print axioms interval_forward_path
#print axioms interval_path
#print axioms components_separated

end MathCompression.ParityMix
