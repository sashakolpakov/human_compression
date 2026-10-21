import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic

/-!
The uniform normal-quotient leg for maximum irredundant length.
Theorems here prove the actual normalization and independence-preservation
steps in arbitrary groups. They do not formalize the cardinal bounds,
classification of primitive groups, simple subdirect products or geometries.
-/
namespace HumanCompression.IrredundantNormalization

variable {G I Q : Type*} [Group G] [Group Q]

def Independent (s : I → G) : Prop :=
  ∀ i, s i ∉ Subgroup.closure (s '' {j | j ≠ i})

def normalized (s w : I → G) (i : I) : G := s i * (w i)⁻¹

def base (s : I → G) (B : Set I) : Subgroup G :=
  Subgroup.closure (s '' B)

 theorem normalized_mem_kernel (s w : I → G) (f : G →* Q) (i : I)
    (h : f (w i) = f (s i)) : normalized s w i ∈ f.ker := by
  simp [normalized, MonoidHom.mem_ker, h]

 theorem base_le_omission (s : I → G) (B : Set I) {i : I} (hi : i ∉ B) :
    base s B ≤ Subgroup.closure (s '' {j | j ≠ i}) := by
  apply Subgroup.closure_mono
  apply Set.image_mono
  intro j hj hji
  subst j
  exact hi hj

 theorem normalized_mem_omission (s w : I → G) (B : Set I)
    (hw : ∀ j, w j ∈ base s B) {i j : I} (hi : i ∉ B) (hji : j ≠ i) :
    normalized s w j ∈ Subgroup.closure (s '' {k | k ≠ i}) := by
  exact Subgroup.mul_mem _ (Subgroup.subset_closure ⟨j, hji, rfl⟩)
    (Subgroup.inv_mem _ (base_le_omission s B hi (hw j)))

 theorem normalized_extra_not_mem (s w : I → G) (B : Set I)
    (hind : Independent s) (hw : ∀ j, w j ∈ base s B)
    {i : I} (hi : i ∉ B) :
    normalized s w i ∉ Subgroup.closure
      ((s '' B) ∪ (normalized s w '' {j | j ≠ i})) := by
  intro h
  have hle : Subgroup.closure ((s '' B) ∪ (normalized s w '' {j | j ≠ i})) ≤
      Subgroup.closure (s '' {j | j ≠ i}) := by
    apply (Subgroup.closure_le _).2
    intro x hx
    rcases hx with ⟨j, hj, rfl⟩ | ⟨j, hj, rfl⟩
    · exact base_le_omission s B hi (Subgroup.subset_closure ⟨j, hj, rfl⟩)
    · exact normalized_mem_omission s w B hw hi hj
  apply hind i
  have hmul := Subgroup.mul_mem _ (hle h) (base_le_omission s B hi (hw i))
  simpa [normalized, mul_assoc] using hmul

 theorem normalized_generates (s w : I → G) (B : Set I)
    (hw : ∀ j, w j ∈ base s B) :
    Subgroup.closure ((s '' B) ∪ Set.range (normalized s w)) =
      Subgroup.closure (Set.range s) := by
  apply le_antisymm
  · apply (Subgroup.closure_le _).2
    intro x hx
    have hb : base s B ≤ Subgroup.closure (Set.range s) := by
      apply Subgroup.closure_mono
      exact Set.image_subset_range _ _
    rcases hx with ⟨j, hj, rfl⟩ | ⟨j, rfl⟩
    · exact Subgroup.subset_closure ⟨j, rfl⟩
    · exact Subgroup.mul_mem _ (Subgroup.subset_closure ⟨j, rfl⟩)
        (Subgroup.inv_mem _ (hb (hw j)))
  · apply (Subgroup.closure_le _).2
    rintro x ⟨j, rfl⟩
    have hb : base s B ≤ Subgroup.closure ((s '' B) ∪ Set.range (normalized s w)) :=
      Subgroup.closure_mono Set.subset_union_left
    have hn : normalized s w j ∈
        Subgroup.closure ((s '' B) ∪ Set.range (normalized s w)) :=
      Subgroup.subset_closure (Or.inr ⟨j, rfl⟩)
    have hmul := Subgroup.mul_mem _ hn (hb (hw j))
    simpa [normalized, mul_assoc] using hmul

 theorem normalized_extra_not_mem_base_conjugates (s w : I → G) (B : Set I)
    (hind : Independent s) (hw : ∀ j, w j ∈ base s B)
    {i : I} (hi : i ∉ B) :
    normalized s w i ∉ Subgroup.closure
      {x | ∃ j, j ≠ i ∧ ∃ t ∈ base s B,
        x = t * normalized s w j * t⁻¹} := by
  intro h
  have hle : Subgroup.closure
      {x | ∃ j, j ≠ i ∧ ∃ t ∈ base s B,
        x = t * normalized s w j * t⁻¹} ≤
      Subgroup.closure (s '' {j | j ≠ i}) := by
    apply (Subgroup.closure_le _).2
    rintro x ⟨j, hji, t, ht, rfl⟩
    have hto := base_le_omission s B hi ht
    exact Subgroup.mul_mem _
      (Subgroup.mul_mem _ hto (normalized_mem_omission s w B hw hi hji))
      (Subgroup.inv_mem _ hto)
  apply hind i
  have hmul := Subgroup.mul_mem _ (hle h) (base_le_omission s B hi (hw i))
  simpa [normalized, mul_assoc] using hmul

 theorem abelian_kernel_conjugation_reduction (N T : Subgroup G)
    (hcomm : ∀ n ∈ N, ∀ v ∈ N, Commute n v)
    (hfactor : ∀ g : G, ∃ n ∈ N, ∃ t ∈ T, g = n * t)
    [N.Normal] {g v : G} (hv : v ∈ N) :
    ∃ t ∈ T, g * v * g⁻¹ = t * v * t⁻¹ := by
  obtain ⟨n, hn, t, ht, rfl⟩ := hfactor g
  refine ⟨t, ht, ?_⟩
  have htv : t * v * t⁻¹ ∈ N := (inferInstance : N.Normal).conj_mem v hv t
  have hc := (hcomm n hn (t * v * t⁻¹) htv).eq
  calc
    (n * t) * v * (n * t)⁻¹ = n * (t * v * t⁻¹) * n⁻¹ := by group
    _ = (t * v * t⁻¹) * n * n⁻¹ := by rw [hc]
    _ = t * v * t⁻¹ := by group


 theorem normalized_extra_not_mem_all_conjugates (s w : I → G) (B : Set I)
    (N : Subgroup G) [N.Normal]
    (hind : Independent s) (hw : ∀ j, w j ∈ base s B)
    (hnorm : ∀ j, normalized s w j ∈ N)
    (hcomm : ∀ n ∈ N, ∀ v ∈ N, Commute n v)
    (hfactor : ∀ g : G, ∃ n ∈ N, ∃ t ∈ base s B, g = n * t)
    {i : I} (hi : i ∉ B) :
    normalized s w i ∉ Subgroup.closure
      {x | ∃ j, j ≠ i ∧ ∃ g : G, x = g * normalized s w j * g⁻¹} := by
  intro h
  apply normalized_extra_not_mem_base_conjugates s w B hind hw hi
  have hs : {x | ∃ j, j ≠ i ∧ ∃ g : G, x = g * normalized s w j * g⁻¹} ⊆
      {x | ∃ j, j ≠ i ∧ ∃ t ∈ base s B, x = t * normalized s w j * t⁻¹} := by
    rintro x ⟨j, hji, g, rfl⟩
    obtain ⟨t, ht, heq⟩ := abelian_kernel_conjugation_reduction N (base s B)
      hcomm hfactor (g := g) (hnorm j)
    exact ⟨j, hji, t, ht, heq⟩
  exact Subgroup.closure_mono hs h

end HumanCompression.IrredundantNormalization

#print axioms HumanCompression.IrredundantNormalization.normalized_mem_kernel
#print axioms HumanCompression.IrredundantNormalization.base_le_omission
#print axioms HumanCompression.IrredundantNormalization.normalized_mem_omission
#print axioms HumanCompression.IrredundantNormalization.normalized_extra_not_mem
#print axioms HumanCompression.IrredundantNormalization.normalized_generates
#print axioms HumanCompression.IrredundantNormalization.normalized_extra_not_mem_base_conjugates
#print axioms HumanCompression.IrredundantNormalization.abelian_kernel_conjugation_reduction

#print axioms HumanCompression.IrredundantNormalization.normalized_extra_not_mem_all_conjugates
