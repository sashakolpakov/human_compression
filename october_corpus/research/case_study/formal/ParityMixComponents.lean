import ParityMix
import SupportedKernelGeneration
import Mathlib.GroupTheory.NoncommPiCoprod
import Mathlib.GroupTheory.Subgroup.Centralizer

/-!
Actual component decompositions of marked subgroups. No intersection
property of the mixed marking is assumed. Mutable phase146 development.
-/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {I C G : Type*} [DecidableEq I] [Fintype C] [DecidableEq C] [Group G]

omit [DecidableEq I] in
@[simp] theorem marked_empty (r : I → G) : marked r ∅ = ⊥ := by
  simp [marked]

omit [Fintype C] [DecidableEq C] in
/-- Taking the generated subgroup commutes with a finite union of supports. -/
theorem marked_component_sup (r : I → G) (scope : C → Finset I) (cs : Finset C) :
    (⨆ c ∈ cs, marked r (scope c)) = marked r (cs.biUnion scope) := by
  apply le_antisymm
  · apply iSup_le
    intro c
    apply iSup_le
    intro hc
    apply marked_mono r
    intro i hi
    exact Finset.mem_biUnion.mpr ⟨c, hc, hi⟩
  · apply (Subgroup.closure_le _).mpr
    rintro x ⟨i, hi, rfl⟩
    obtain ⟨c, hc, hic⟩ := Finset.mem_biUnion.mp hi
    exact Subgroup.mem_iSup_of_mem c (Subgroup.mem_iSup_of_mem hc
      (Subgroup.subset_closure ⟨i, hic, rfl⟩))

/-- Disjoint support sets yield independent component subgroups when the
original marking has IP. The conclusion is independence from the union
of all other components, not only pairwise trivial intersections. -/
theorem marked_components_independent (r : I → G) (scope : C → Finset I)
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M)) :
    iSupIndep (fun c => marked r (scope c)) := by
  apply iSupIndep_def.mpr
  intro c
  have hothers : (⨆ d, ⨆ (_ : d ≠ c), marked r (scope d)) ≤
      marked r ((Finset.univ.erase c).biUnion scope) := by
    apply iSup_le
    intro d
    apply iSup_le
    intro hdc
    apply marked_mono r
    intro i hi
    exact Finset.mem_biUnion.mpr ⟨d, Finset.mem_erase.mpr ⟨hdc, Finset.mem_univ d⟩, hi⟩
  have hempty : scope c ∩ (Finset.univ.erase c).biUnion scope = ∅ := by
    apply Finset.eq_empty_iff_forall_notMem.mpr
    intro i hi
    obtain ⟨hic, hio⟩ := Finset.mem_inter.mp hi
    obtain ⟨d, hd, hid⟩ := Finset.mem_biUnion.mp hio
    exact Finset.disjoint_left.mp (hdisj (Finset.mem_erase.mp hd).1.symm) hic hid
  apply Disjoint.mono_right hothers
  rw [disjoint_iff, hip, hempty, marked_empty]

omit [DecidableEq I] in
/-- Commutation of the actual markers on two supports extends to their
entire generated subgroups. -/
theorem marked_commute (r : I → G) (L M : Finset I)
    (hcomm : ∀ i ∈ L, ∀ j ∈ M, Commute (r i) (r j)) :
    ∀ x y, x ∈ marked r L → y ∈ marked r M → Commute x y := by
  have hcentral : marked r L ≤ Subgroup.centralizer (r '' (M : Set I)) := by
    apply (Subgroup.closure_le _).mpr
    rintro x ⟨i, hi, rfl⟩ y ⟨j, hj, rfl⟩
    exact (hcomm i hi j hj).eq.symm
  have hcentral' : marked r L ≤ Subgroup.centralizer (marked r M : Set G) := by
    simpa only [marked, Subgroup.centralizer_closure] using hcentral
  intro x y hx hy
  exact (hcentral' hx y hy).symm

/-- The actual assembly map from commuting component subgroups. -/
def componentAssembly (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d =>
      ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j)) :
    (∀ c, marked r (scope c)) →* G :=
  Subgroup.noncommPiCoprod (fun c d hcd => marked_commute r (scope c) (scope d) (hcomm hcd))

omit [DecidableEq C] in
theorem componentAssembly_range (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d =>
      ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j)) :
    (componentAssembly r scope hcomm).range = marked r (Finset.univ.biUnion scope) := by
  unfold componentAssembly
  rw [Subgroup.noncommPiCoprod_range]
  simpa using marked_component_sup r scope Finset.univ

theorem componentAssembly_injective (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d =>
      ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M)) :
    Function.Injective (componentAssembly r scope hcomm) :=
  Subgroup.injective_noncommPiCoprod_of_iSupIndep
    (marked_components_independent r scope hdisj hip)

#print axioms marked_component_sup
#print axioms marked_components_independent
#print axioms marked_commute
#print axioms componentAssembly_range
#print axioms componentAssembly_injective

variable {K : Type*} [Group K]

/-- The actual homomorphism induced on a marked parabolic. -/
def mapMarked (r : I → G) (f : G →* K) (S : Finset I) :
    marked r S →* marked (fun i => f (r i)) S :=
  (f.comp (marked r S).subtype).codRestrict _ (by
    intro x
    rw [← marked_map r f S]
    exact ⟨x, x.property, rfl⟩)

omit [DecidableEq I] [DecidableEq C] in
/-- Assembly commutes with a genuine group homomorphism, including the
coordinate projections used by the mixed group. -/
theorem componentAssembly_map (r : I → G) (f : G →* K) (scope : C → Finset I)
    (hcomm : Pairwise fun c d =>
      ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hcomm' : Pairwise fun c d =>
      ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (f (r i)) (f (r j)))
    (x : ∀ c, marked r (scope c)) :
    f (componentAssembly r scope hcomm x) =
      componentAssembly (fun i => f (r i)) scope hcomm'
        (fun c => mapMarked r f (scope c) (x c)) := by
  simp only [componentAssembly, Subgroup.noncommPiCoprod_apply, Finset.map_noncommProd]
  rfl

#print axioms componentAssembly_map

end MathCompression.ParityMix
