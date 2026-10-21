import SupportedKernelGeneration
import Mathlib.GroupTheory.Index
import Mathlib.GroupTheory.Nilpotent

/-!
Cardinality, local recognition, separator factorization and lower-central
consequences of the actual supported-kernel construction. This module imports
the independently reviewed core; it derives the profiles used in its final
statements rather than assuming them. Lower-central index n means gamma_(n+1).
-/

namespace MathCompression.SupportedKernelGeneration

variable {I J B : Type*} [DecidableEq I] [Fintype J] [DecidableEq J] [Group B]
variable {E : J → Type*} [∀ j, Group (E j)]

def baseProjection (r : I → B × (∀ j, E j)) (L : Finset I) :
    marked r L →* B :=
  (MonoidHom.fst B (∀ j, E j)).comp (marked r L).subtype

omit [DecidableEq I] [Fintype J] [DecidableEq J] in
theorem baseProjection_range (r : I → B × (∀ j, E j)) (L : Finset I) :
    (baseProjection r L).range = marked (fun i => (r i).1) L := by
  change (baseProjection r L).range =
    marked (fun i => (MonoidHom.fst B (∀ j, E j)) (r i)) L
  rw [← marked_map r (MonoidHom.fst B (∀ j, E j)) L]
  ext x
  constructor
  · rintro ⟨w, rfl⟩
    exact ⟨w.val, w.property, rfl⟩
  · rintro ⟨w, hw, rfl⟩
    exact ⟨⟨w, hw⟩, rfl⟩

omit [Fintype J] [DecidableEq J] in
noncomputable def kernelCoordinatesEquiv
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (q : ∀ j, E j →* B) (L : Finset I)
    (hprofile : ∀ y : ∀ j, E j, (1, y) ∈ marked r L ↔
      (∀ j, q j (y j) = 1) ∧ (∀ j, ¬ scope j ⊆ L → y j = 1)) :
    (baseProjection r L).ker ≃ (∀ j : {j // scope j ⊆ L}, (q j.val).ker) := by
  let expand : (∀ j : {j // scope j ⊆ L}, (q j.val).ker) → (∀ j, E j) :=
    fun y j => if hj : scope j ⊆ L then (y ⟨j, hj⟩).val else 1
  have facts (w : (baseProjection r L).ker) :
      (∀ j, q j (w.val.val.2 j) = 1) ∧
        (∀ j, ¬ scope j ⊆ L → w.val.val.2 j = 1) := by
    apply (hprofile w.val.val.2).mp
    have hbase : w.val.val.1 = 1 := w.property
    have he : (1, w.val.val.2) = w.val.val := by
      apply Prod.ext
      · exact hbase.symm
      · rfl
    rw [he]
    exact w.val.property
  refine {
    toFun := fun w j => ⟨w.val.val.2 j.val, (facts w).1 j.val⟩
    invFun := fun y => ⟨⟨(1, expand y), ?_⟩, rfl⟩
    left_inv := ?_
    right_inv := ?_
  }
  · apply (hprofile (expand y)).mpr
    constructor
    · intro j
      by_cases hj : scope j ⊆ L
      · simp only [expand, dif_pos hj]
        exact (y ⟨j, hj⟩).property
      · simp [expand, hj]
    · intro j hj
      simp [expand, hj]
  · intro w
    apply Subtype.ext
    apply Subtype.ext
    apply Prod.ext
    · exact w.property.symm
    · funext j
      by_cases hj : scope j ⊆ L
      · simp [expand, hj]
      · simpa [expand, hj] using ((facts w).2 j hj).symm
  · intro y
    funext j
    apply Subtype.ext
    simp [expand, j.property]

/-- The finite order formula, with Nat.card's valid general convention.
The kernel profile used in its proof is the conclusion of the construction
theorem, not an additional hypothesis of this statement. -/
theorem parabolic_cardinality
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (L : Finset I) :
    Nat.card (marked r L) =
      Nat.card (marked (fun i => (r i).1) L) *
        ∏ j : {j // scope j ⊆ L}, Nat.card (q j.val).ker := by
  have hker : Nat.card (baseProjection r L).ker =
      ∏ j : {j // scope j ⊆ L}, Nat.card (q j.val).ker := by
    rw [Nat.card_congr (kernelCoordinatesEquiv r scope q L
      (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj L))]
    exact Nat.card_pi
  calc
    Nat.card (marked r L) =
        Nat.card (baseProjection r L).ker * Nat.card (baseProjection r L).range := by
      rw [← (baseProjection r L).ker.card_mul_index, Subgroup.index_ker]
    _ = _ := by rw [hker, baseProjection_range]; exact Nat.mul_comm _ _

#print axioms baseProjection_range
#print axioms kernelCoordinatesEquiv
#print axioms parabolic_cardinality

/-- Antichain supports retain the whole local group, with no finite-order
or cardinality comparison. Both injectivity and surjectivity are proved. -/
theorem local_projection_bijective
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hanti : ∀ j s, scope j ⊆ scope s → j = s)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (s : J) :
    Function.Bijective ((coordinate s).comp (marked r (scope s)).subtype) := by
  have hscope : Function.Injective scope := by
    intro j t he
    apply hanti j t
    rw [he]
  constructor
  · apply (injective_iff_map_eq_one _).mpr
    intro w hw
    change w.val.2 s = 1 at hw
    have hc := marked_compatibility r q p hcompatible (scope s) s w.property
    have hf := marked_base_fixed r (p s) (scope s) (hfix s) w.property
    have hbase : w.val.1 = 1 := by
      calc
        w.val.1 = p s w.val.1 := hf.symm
        _ = q s (w.val.2 s) := hc.symm
        _ = 1 := by rw [hw, map_one]
    have hpure : (1, w.val.2) = w.val := by
      apply Prod.ext
      · exact hbase.symm
      · rfl
    have hmem : (1, w.val.2) ∈ marked r (scope s) := by
      rw [hpure]
      exact w.property
    have hp := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      (scope s) w.val.2).mp hmem
    apply Subtype.ext
    apply Prod.ext
    · exact hbase
    · funext j
      by_cases hjs : j = s
      · subst j
        exact hw
      · apply hp.2 j
        intro hsub
        exact hjs (hanti j s hsub)
  · intro x
    have hmap : (marked r (scope s)).map (coordinate s) = ⊤ := by
      rw [marked_map]
      exact hgen s
    have hx : x ∈ (marked r (scope s)).map (coordinate s) := by
      rw [hmap]
      trivial
    obtain ⟨w, hw, he⟩ := hx
    exact ⟨⟨w, hw⟩, he⟩

#print axioms local_projection_bijective


/-- A base separator lifts whenever no surviving support straddles it.
The factorization is proved for each parabolic union and requires neither
commutativity of the local kernels nor normality of the two parabolics. -/
theorem separator_factorization
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (L M : Finset I)
    (hbase : ∀ z ∈ marked (fun i => (r i).1) (L ∪ M),
      ∃ a ∈ marked (fun i => (r i).1) L,
      ∃ b ∈ marked (fun i => (r i).1) M, z = a * b)
    (hsides : ∀ j, scope j ⊆ L ∪ M → scope j ⊆ L ∨ scope j ⊆ M) :
    ∀ x ∈ marked r (L ∪ M),
      ∃ a ∈ marked r L, ∃ b ∈ marked r M, x = a * b := by
  intro x hx
  have hproject : x.1 ∈ marked (fun i => (r i).1) (L ∪ M) := by
    rw [← baseProjection_range r (L ∪ M)]
    exact ⟨⟨x, hx⟩, rfl⟩
  obtain ⟨a₀, ha₀, b₀, hb₀, hab₀⟩ := hbase x.1 hproject
  rw [← baseProjection_range r L] at ha₀
  rw [← baseProjection_range r M] at hb₀
  obtain ⟨a, ha⟩ := ha₀
  obtain ⟨b, hb⟩ := hb₀
  change a.val.1 = a₀ at ha
  change b.val.1 = b₀ at hb
  let n := x * (a.val * b.val)⁻¹
  have hnmem : n ∈ marked r (L ∪ M) := by
    apply (marked r (L ∪ M)).mul_mem hx
    apply (marked r (L ∪ M)).inv_mem
    exact (marked r (L ∪ M)).mul_mem
      (marked_mono r Finset.subset_union_left a.property)
      (marked_mono r Finset.subset_union_right b.property)
  have hnbase : n.1 = 1 := by
    dsimp [n]
    rw [hab₀, ha, hb]
    exact mul_inv_cancel _
  have hnpure : (1, n.2) = n := Prod.ext hnbase.symm rfl
  have hnprofile := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
    (L ∪ M) n.2).mp (hnpure ▸ hnmem)
  let yL : ∀ j, E j := fun j => if scope j ⊆ L then n.2 j else 1
  let yM : ∀ j, E j := fun j => if scope j ⊆ L then 1 else n.2 j
  have hyL : (1, yL) ∈ marked r L := by
    apply (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj L yL).mpr
    constructor
    · intro j
      by_cases hj : scope j ⊆ L
      · simpa [yL, hj] using hnprofile.1 j
      · simp [yL, hj]
    · intro j hj
      simp [yL, hj]
  have hyM : (1, yM) ∈ marked r M := by
    apply (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj M yM).mpr
    constructor
    · intro j
      by_cases hj : scope j ⊆ L
      · simp [yM, hj]
      · simpa [yM, hj] using hnprofile.1 j
    · intro j hj
      by_cases hjL : scope j ⊆ L
      · simp [yM, hjL]
      · simp only [yM, if_neg hjL]
        apply hnprofile.2 j
        intro hu
        exact (hsides j hu).elim hjL hj
  have hsplit : (1, yL) * (1, yM) = n := by
    apply Prod.ext
    · simpa using hnbase.symm
    · funext j
      by_cases hj : scope j ⊆ L <;> simp [yL, yM, hj]
  have hconj : a.val⁻¹ * (1, yM) * a.val ∈ marked r M := by
    have hm := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      M yM).mp hyM
    have hc : a.val⁻¹ * (1, yM) * a.val =
        (1, fun j => (a.val.2 j)⁻¹ * yM j * a.val.2 j) := by
      apply Prod.ext
      · simp
      · rfl
    rw [hc]
    apply (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj M _).mpr
    constructor
    · intro j
      simp [map_mul, map_inv, hm.1 j]
    · intro j hj
      simp [hm.2 j hj]
  refine ⟨(1, yL) * a.val, (marked r L).mul_mem hyL a.property,
    (a.val⁻¹ * (1, yM) * a.val) * b.val,
    (marked r M).mul_mem hconj b.property, ?_⟩
  calc
    x = n * (a.val * b.val) := by dsimp [n]; group
    _ = ((1, yL) * (1, yM)) * (a.val * b.val) := by rw [hsplit]
    _ = _ := by group

#print axioms separator_factorization


/-- If every local kernel lies in the indicated lower-central term, the
same support induction isolates it in the lower-central term of its actual
support parabolic. Mathlib index n denotes the usual term gamma_(n+1). -/
theorem pure_kernel_mem_lowerCentralSeries
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (n : ℕ) (hlocal : ∀ j, (q j).ker ≤ (⊤ : Subgroup (E j)).lowerCentralSeries n)
    (s : J) (x : E s) (hx : q s x = 1) :
    (1, Pi.mulSingle s x) ∈ (marked r (scope s)).lowerCentralSeries n := by
  let P : J → Subgroup (∀ j, E j) :=
    fun j => ((marked r (scope j)).lowerCentralSeries n).comap kernelEmbedding
  let R : J → J → Prop := fun j i => scope j ⊆ scope i ∧ j ≠ i
  have hrank : ∀ j i, R j i → (scope j).card < (scope i).card := by
    intro j i hji
    apply Finset.card_lt_card
    apply Finset.ssubset_iff_subset_ne.mpr
    exact ⟨hji.1, fun he => hji.2 (hscope he)⟩
  have hmono : ∀ j i, R j i → P j ≤ P i := by
    intro j i hji y hy
    exact Subgroup.lowerCentralSeries_mono n (marked_mono r hji.1) hy
  have hwitness : ∀ i (x : E i), x ∈ (q i).ker →
      ∃ y : ∀ j, E j, y ∈ P i ∧ y i = x ∧
        (∀ j, y j ∈ (q j).ker) ∧
        (∀ j, j ≠ i → ¬ R j i → y j = 1) := by
    intro i x hx
    have hmap : ((marked r (scope i)).lowerCentralSeries n).map (coordinate i) =
        (⊤ : Subgroup (E i)).lowerCentralSeries n := by
      rw [Subgroup.map_lowerCentralSeries, marked_map]
      change (marked (fun k => (r k).2 i) (scope i)).lowerCentralSeries n = _
      rw [hgen i]
    have hxm : x ∈ ((marked r (scope i)).lowerCentralSeries n).map (coordinate i) := by
      rw [hmap]
      exact hlocal i hx
    obtain ⟨w, hwc, hwx⟩ := hxm
    have hw := (marked r (scope i)).lowerCentralSeries_le_self n hwc
    change w.2 i = x at hwx
    have hc := marked_compatibility r q p hcompatible (scope i) i hw
    have hf := marked_base_fixed r (p i) (scope i) (hfix i) hw
    have hbase : w.1 = 1 := by
      calc
        w.1 = p i w.1 := hf.symm
        _ = q i (w.2 i) := hc.symm
        _ = 1 := by rw [hwx]; exact hx
    have he : (1, w.2) = w := Prod.ext hbase.symm rfl
    have hp := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      (scope i) w.2).mp (he ▸ hw)
    refine ⟨w.2, ?_, hwx, hp.1, ?_⟩
    · change (1, w.2) ∈ (marked r (scope i)).lowerCentralSeries n
      rwa [he]
    · intro j hji hnot
      apply hp.2 j
      intro hsub
      exact hnot ⟨hsub, hji⟩
  exact triangular_isolation P (fun j => (q j).ker)
    (fun j => (scope j).card) R hrank hmono hwitness s x hx

/-- The lower-central term of every actual parabolic is exactly its base
kernel, if the corresponding base term vanishes and each local kernel lies
in its local term. This includes U.SK.Central with n=c-1, and requires only
kernel inclusion in the local term, rather than equality. -/
theorem lowerCentralSeries_eq_kernel
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (n : ℕ) (hlocal : ∀ j, (q j).ker ≤ (⊤ : Subgroup (E j)).lowerCentralSeries n)
    (hbase : (⊤ : Subgroup B).lowerCentralSeries n = ⊥)
    (L : Finset I) :
    (marked r L).lowerCentralSeries n =
      marked r L ⊓ (MonoidHom.fst B (∀ j, E j)).ker := by
  apply le_antisymm
  · intro w hw
    refine ⟨(marked r L).lowerCentralSeries_le_self n hw, ?_⟩
    have hm : w.1 ∈ ((marked r L).lowerCentralSeries n).map
        (MonoidHom.fst B (∀ j, E j)) := ⟨w, hw, rfl⟩
    rw [Subgroup.map_lowerCentralSeries] at hm
    have ht := Subgroup.lowerCentralSeries_mono n
      (show (marked r L).map (MonoidHom.fst B (∀ j, E j)) ≤ ⊤ from le_top) hm
    change w.1 ∈ (⊤ : Subgroup B).lowerCentralSeries n at ht
    rw [hbase] at ht
    exact ht
  · intro w hw
    have he : (1, w.2) = w := Prod.ext hw.2.symm rfl
    have hp := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      L w.2).mp (he ▸ hw.1)
    let P : Subgroup (∀ j, E j) :=
      ((marked r L).lowerCentralSeries n).comap kernelEmbedding
    have hP : w.2 ∈ P := by
      apply Subgroup.pi_mem_of_mulSingle_mem w.2
      intro j
      by_cases hj : scope j ⊆ L
      · exact Subgroup.lowerCentralSeries_mono n (marked_mono r hj)
          (pure_kernel_mem_lowerCentralSeries r scope hscope q p hout hcompatible hfix
            hgen hinj n hlocal j (w.2 j) (hp.1 j))
      · have hz := hp.2 j hj
        simp [hz]
    change (1, w.2) ∈ (marked r L).lowerCentralSeries n at hP
    rwa [he] at hP

#print axioms pure_kernel_mem_lowerCentralSeries
#print axioms lowerCentralSeries_eq_kernel

end MathCompression.SupportedKernelGeneration
