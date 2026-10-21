import Mathlib.Algebra.Group.Subgroup.Finite
import Mathlib.Algebra.Group.Pi.Lemmas
import Mathlib.Tactic
import CoordinateKernels

/-!
Actual supported-kernel generation, parabolic kernel profiles and marked IP.
This is an author formalization awaiting independent statement/proof review.
No kernel-profile identity or isolated-word condition is an assumption.
-/

namespace MathCompression.SupportedKernelGeneration

variable {J : Type*} [Fintype J] [DecidableEq J]
variable {E : J → Type*} [∀ j, Group (E j)]

/-- A triangular witness can be corrected using already isolated smaller
coordinates. The factors E j and their subgroups N j need not be abelian. -/
theorem triangular_isolation
    (P : J → Subgroup (∀ j, E j)) (N : ∀ j, Subgroup (E j))
    (rank : J → ℕ) (R : J → J → Prop)
    (hrank : ∀ j i, R j i → rank j < rank i)
    (hmono : ∀ j i, R j i → P j ≤ P i)
    (hwitness : ∀ i (x : E i), x ∈ N i →
      ∃ y : ∀ j, E j, y ∈ P i ∧ y i = x ∧
        (∀ j, y j ∈ N j) ∧
        (∀ j, j ≠ i → ¬ R j i → y j = 1)) :
    ∀ i (x : E i), x ∈ N i → Pi.mulSingle i x ∈ P i := by
  have main : ∀ n : ℕ, ∀ i, rank i = n →
      ∀ x : E i, x ∈ N i → Pi.mulSingle i x ∈ P i := by
    intro n
    induction n using Nat.strong_induction_on with
    | h n ih =>
      intro i hi x hx
      obtain ⟨y, hy, hyi, hyN, hyzero⟩ := hwitness i x hx
      let z : ∀ j, E j := Function.update y i 1
      have hz : z ∈ P i := by
        apply Subgroup.pi_mem_of_mulSingle_mem z
        intro j
        by_cases hji : j = i
        · subst j
          simp [z]
        · by_cases hR : R j i
          · have hjlt : rank j < n := by simpa [hi] using hrank j i hR
            have hj := ih (rank j) hjlt j rfl (y j) (hyN j)
            apply hmono j i hR
            simpa [z, hji] using hj
          · have hjone := hyzero j hji hR
            simp [z, hji, hjone]
      have hm := (P i).mul_mem hy ((P i).inv_mem hz)
      have he : y * z⁻¹ = Pi.mulSingle i x := by
        funext j
        by_cases hji : j = i
        · subst j
          simp [z, hyi]
        · simp [z, hji]
      rwa [he] at hm
  intro i x hx
  exact main (rank i) i rfl x hx

#print axioms triangular_isolation

variable {I B : Type*} [DecidableEq I] [Group B]

def marked {G : Type*} [Group G] (r : I → G) (L : Finset I) : Subgroup G :=
  Subgroup.closure (r '' (L : Set I))

omit [DecidableEq I] in
theorem marked_mono {G : Type*} [Group G] (r : I → G)
    {L M : Finset I} (h : L ⊆ M) : marked r L ≤ marked r M :=
  Subgroup.closure_mono (Set.image_mono h)

omit [DecidableEq I] in
theorem marked_map {G K : Type*} [Group G] [Group K]
    (r : I → G) (f : G →* K) (L : Finset I) :
    (marked r L).map f = marked (fun i => f (r i)) L := by
  unfold marked
  rw [MonoidHom.map_closure, Set.image_image]

def coordinate (j : J) : (B × (∀ j, E j)) →* E j :=
  (Pi.evalMonoidHom E j).comp (MonoidHom.snd B (∀ j, E j))

def kernelEmbedding : (∀ j, E j) →* (B × (∀ j, E j)) where
  toFun x := (1, x)
  map_one' := rfl
  map_mul' _ _ := by simp

omit [Fintype J] [DecidableEq J] in
/-- A word on L has local support inside L intersect scope(j). This is
derived from its actual generators, not supplied as a kernel profile. -/
theorem coordinate_mem_marked_inter
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (L : Finset I) (j : J) {w : B × (∀ j, E j)}
    (hw : w ∈ marked r L) :
    w.2 j ∈ marked (fun i => (r i).2 j) (L ∩ scope j) := by
  have hle : marked r L ≤
      (marked (fun i => (r i).2 j) (L ∩ scope j)).comap (coordinate j) := by
    apply (Subgroup.closure_le _).mpr
    rintro x ⟨i, hi, rfl⟩
    change (r i).2 j ∈ marked (fun i => (r i).2 j) (L ∩ scope j)
    by_cases his : i ∈ scope j
    · apply Subgroup.subset_closure
      exact ⟨i, Finset.mem_inter.mpr ⟨hi, his⟩, rfl⟩
    · rw [hout j i his]
      exact (marked (fun i => (r i).2 j) (L ∩ scope j)).one_mem
  exact hle hw

omit [Fintype J] [DecidableEq J] [DecidableEq I] in
/-- Compatibility on the literal generators propagates to every actual
marked parabolic. -/
theorem marked_compatibility
    (r : I → B × (∀ j, E j)) (q : ∀ j, E j →* B) (p : J → B →* B)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (L : Finset I) (j : J) {w : B × (∀ j, E j)}
    (hw : w ∈ marked r L) :
    q j (w.2 j) = p j w.1 := by
  let f := (q j).comp (coordinate (B := B) j)
  let g := (p j).comp (MonoidHom.fst B (∀ j, E j))
  have hs : Set.EqOn f g (r '' (L : Set I)) := by
    rintro _ ⟨i, _, rfl⟩
    exact hcompatible j i
  exact MonoidHom.eqOn_closure hs hw

omit [Fintype J] [DecidableEq J] [DecidableEq I] in
/-- A genuine deletion fixes the base of a word on its retained support. -/
theorem marked_base_fixed
    (r : I → B × (∀ j, E j)) (p : B →* B) (L : Finset I)
    (hfix : ∀ i ∈ L, p (r i).1 = (r i).1)
    {w : B × (∀ j, E j)} (hw : w ∈ marked r L) :
    p w.1 = w.1 := by
  let f := p.comp (MonoidHom.fst B (∀ j, E j))
  let g := MonoidHom.fst B (∀ j, E j)
  have hs : Set.EqOn f g (r '' (L : Set I)) := by
    rintro _ ⟨i, hi, rfl⟩
    exact hfix i hi
  exact MonoidHom.eqOn_closure hs hw

#print axioms coordinate_mem_marked_inter
#print axioms marked_compatibility
#print axioms marked_base_fixed

omit [Fintype J] [DecidableEq J] in
/-- Local generation and proper-parabolic injectivity produce the actual
triangular witness required for isolation. No isolated-word condition is an input. -/
theorem local_kernel_witness
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (s : J) (x : E s) (hx : q s x = 1) :
    ∃ y : ∀ j, E j, (1, y) ∈ marked r (scope s) ∧ y s = x ∧
      (∀ j, q j (y j) = 1) ∧
      (∀ j, ¬ scope j ⊆ scope s → y j = 1) := by
  have hmap : (marked r (scope s)).map (coordinate s) = ⊤ := by
    rw [marked_map]
    exact hgen s
  have hxmap : x ∈ (marked r (scope s)).map (coordinate s) := by
    rw [hmap]
    trivial
  obtain ⟨w, hw, hwx⟩ := hxmap
  change w.2 s = x at hwx
  have hc := marked_compatibility r q p hcompatible (scope s) s hw
  have hf := marked_base_fixed r (p s) (scope s) (hfix s) hw
  have hbase : w.1 = 1 := by
    calc
      w.1 = p s w.1 := hf.symm
      _ = q s (w.2 s) := hc.symm
      _ = 1 := by rw [hwx]; exact hx
  refine ⟨w.2, ?_, hwx, ?_, ?_⟩
  · have he : (1, w.2) = w := by
      apply Prod.ext
      · exact hbase.symm
      · rfl
    rwa [he]
  · intro j
    have hj := marked_compatibility r q p hcompatible (scope s) j hw
    simpa [hbase] using hj
  · intro j hnot
    have hproper : scope s ∩ scope j ⊂ scope j := by
      apply Finset.ssubset_iff_subset_ne.mpr
      refine ⟨Finset.inter_subset_right, ?_⟩
      intro he
      apply hnot
      intro i hi
      have : i ∈ scope s ∩ scope j := by rw [he]; exact hi
      exact (Finset.mem_inter.mp this).1
    apply hinj j (scope s ∩ scope j) hproper
    · exact coordinate_mem_marked_inter r scope hout (scope s) j hw
    · have hj := marked_compatibility r q p hcompatible (scope s) j hw
      simpa [hbase] using hj

#print axioms local_kernel_witness

/-- The complete support induction: pure local kernels belong to the
actual subgroup generated on that support. -/
theorem pure_kernel_mem
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (s : J) (x : E s) (hx : q s x = 1) :
    (1, Pi.mulSingle s x) ∈ marked r (scope s) := by
  let P : J → Subgroup (∀ j, E j) :=
    fun j => (marked r (scope j)).comap kernelEmbedding
  let R : J → J → Prop := fun j i => scope j ⊆ scope i ∧ j ≠ i
  have hrank : ∀ j i, R j i → (scope j).card < (scope i).card := by
    intro j i hji
    apply Finset.card_lt_card
    apply Finset.ssubset_iff_subset_ne.mpr
    exact ⟨hji.1, fun he => hji.2 (hscope he)⟩
  have hmono : ∀ j i, R j i → P j ≤ P i := by
    intro j i hji y hy
    exact marked_mono r hji.1 hy
  have hwitness : ∀ i (x : E i), x ∈ (q i).ker →
      ∃ y : ∀ j, E j, y ∈ P i ∧ y i = x ∧
        (∀ j, y j ∈ (q j).ker) ∧
        (∀ j, j ≠ i → ¬ R j i → y j = 1) := by
    intro i x hx
    obtain ⟨y, hy, hyi, hyN, hyzero⟩ :=
      local_kernel_witness r scope q p hout hcompatible hfix hgen hinj i x hx
    refine ⟨y, hy, hyi, hyN, ?_⟩
    intro j hji hnot
    apply hyzero j
    intro hsub
    exact hnot ⟨hsub, hji⟩
  exact triangular_isolation P (fun j => (q j).ker)
    (fun j => (scope j).card) R hrank hmono hwitness s x hx

/-- Both directions of the actual parabolic kernel profile. The profile
is concluded from the construction; it is not an input. -/
theorem kernel_profile
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (L : Finset I) (y : ∀ j, E j) :
    (1, y) ∈ marked r L ↔
      (∀ j, q j (y j) = 1) ∧ (∀ j, ¬ scope j ⊆ L → y j = 1) := by
  constructor
  · intro hy
    have hyN : ∀ j, q j (y j) = 1 := by
      intro j
      have hj := marked_compatibility r q p hcompatible L j hy
      simpa using hj
    refine ⟨hyN, ?_⟩
    intro j hnot
    have hproper : L ∩ scope j ⊂ scope j := by
      apply Finset.ssubset_iff_subset_ne.mpr
      refine ⟨Finset.inter_subset_right, ?_⟩
      intro he
      apply hnot
      intro i hi
      have : i ∈ L ∩ scope j := by rw [he]; exact hi
      exact (Finset.mem_inter.mp this).1
    exact hinj j (L ∩ scope j) hproper
      (y j) (coordinate_mem_marked_inter r scope hout L j hy) (hyN j)
  · rintro ⟨hyN, hyzero⟩
    let P : Subgroup (∀ j, E j) := (marked r L).comap kernelEmbedding
    change y ∈ P
    apply Subgroup.pi_mem_of_mulSingle_mem y
    intro j
    by_cases hj : scope j ⊆ L
    · exact marked_mono r hj
        (pure_kernel_mem r scope hscope q p hout hcompatible hfix hgen hinj j (y j) (hyN j))
    · have hyj := hyzero j hj
      simp [hyj]

def simultaneousFiber (q : ∀ j, E j →* B) (p : J → B →* B) :
    Subgroup (B × (∀ j, E j)) where
  carrier := {w | ∀ j, q j (w.2 j) = p j w.1}
  one_mem' := by simp
  mul_mem' := by
    intro x y hx hy j
    change q j (x.2 j * y.2 j) = p j (x.1 * y.1)
    simpa only [map_mul] using congrArg₂ (· * ·) (hx j) (hy j)
  inv_mem' := by
    intro x hx j
    change q j (x.2 j)⁻¹ = p j x.1⁻¹
    simpa only [map_inv] using congrArg Inv.inv (hx j)

/-- The marked tuples generate the full simultaneous fiber product,
with every kernel profile already proved above. -/
theorem generated_eq_fiber [Fintype I]
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (hbase : marked (fun i => (r i).1) Finset.univ = ⊤) :
    marked r Finset.univ = simultaneousFiber q p := by
  have hle : marked r Finset.univ ≤ simultaneousFiber q p := by
    intro w hw j
    exact marked_compatibility r q p hcompatible Finset.univ j hw
  apply le_antisymm hle
  intro x hx
  have hmap : (marked r Finset.univ).map (MonoidHom.fst B (∀ j, E j)) = ⊤ := by
    rw [marked_map]
    exact hbase
  have hxmap : x.1 ∈ (marked r Finset.univ).map (MonoidHom.fst B (∀ j, E j)) := by
    rw [hmap]
    trivial
  obtain ⟨w, hw, hwx⟩ := hxmap
  change w.1 = x.1 at hwx
  let z := x * w⁻¹
  have hzFiber : z ∈ simultaneousFiber q p :=
    (simultaneousFiber q p).mul_mem hx ((simultaneousFiber q p).inv_mem (hle hw))
  have hzbase : z.1 = 1 := by simp [z, hwx]
  have hzN : ∀ j, q j (z.2 j) = 1 := by
    intro j
    have hj := hzFiber j
    simpa [hzbase] using hj
  have hzpure : (1, z.2) ∈ marked r Finset.univ := by
    apply (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      Finset.univ z.2).mpr
    exact ⟨hzN, fun j hnot => False.elim (hnot (Finset.subset_univ _))⟩
  have hzeq : (1, z.2) = z := by
    apply Prod.ext
    · exact hzbase.symm
    · rfl
  have hzx : z * w = x := by simp [z]
  rw [hzeq] at hzpure
  have hm := (marked r Finset.univ).mul_mem hzpure hw
  rwa [hzx] at hm

#print axioms pure_kernel_mem
#print axioms kernel_profile
#print axioms generated_eq_fiber

/-- Full marked IP follows from the proved kernel profiles and base IP.
The final meet and lifting arguments reuse the existing formal library. -/
theorem marked_intersection_property
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (hbaseIP : ∀ L M : Finset I,
      marked (fun i => (r i).1) L ⊓ marked (fun i => (r i).1) M =
        marked (fun i => (r i).1) (L ∩ M))
    (L M : Finset I) :
    marked r L ⊓ marked r M = marked r (L ∩ M) := by
  apply LeemansLift.intersection_of_image_and_kernel
    (MonoidHom.fst B (∀ j, E j)) (marked r L) (marked r M) (marked r (L ∩ M))
  · exact marked_mono r Finset.inter_subset_left
  · exact marked_mono r Finset.inter_subset_right
  · rw [marked_map, marked_map, marked_map]
    exact hbaseIP L M
  · intro w hw
    have hwbase : w.1 = 1 := hw.2
    have hwpure : (1, w.2) = w := by
      apply Prod.ext
      · exact hwbase.symm
      · rfl
    have hL : (1, w.2) ∈ marked r L := by rw [hwpure]; exact hw.1.1
    have hM : (1, w.2) ∈ marked r M := by rw [hwpure]; exact hw.1.2
    have profileL := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj L w.2).mp hL
    have profileM := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj M w.2).mp hM
    let scopes : J → Set I := fun j => (scope j : Set I)
    have coordL : w.2 ∈ LeemansCoordinates.coordinateKernel scopes (L : Set I) := profileL.2
    have coordM : w.2 ∈ LeemansCoordinates.coordinateKernel scopes (M : Set I) := profileM.2
    have coordMeet : w.2 ∈
        LeemansCoordinates.coordinateKernel scopes ((L : Set I) ∩ (M : Set I)) := by
      rw [← LeemansCoordinates.coordinate_kernel_meet]
      exact ⟨coordL, coordM⟩
    have hzero : ∀ j, ¬ scope j ⊆ L ∩ M → w.2 j = 1 := by
      intro j hj
      apply coordMeet j
      intro hsub
      apply hj
      intro i hi
      exact Finset.mem_inter.mpr (hsub hi)
    rw [← hwpure]
    exact (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      (L ∩ M) w.2).mpr ⟨profileL.1, hzero⟩

#print axioms marked_intersection_property

/-- One complete construction statement for generation, every actual
kernel profile, and full marked IP. The finite order formula and the
separate local/deletion/lower-central/separator corollaries are not bundled here. -/
theorem supported_kernel_construction [Fintype I]
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (T : Finset I), T ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) T, q j x = 1 → x = 1)
    (hbase : marked (fun i => (r i).1) Finset.univ = ⊤)
    (hbaseIP : ∀ L M : Finset I,
      marked (fun i => (r i).1) L ⊓ marked (fun i => (r i).1) M =
        marked (fun i => (r i).1) (L ∩ M)) :
    marked r Finset.univ = simultaneousFiber q p ∧
    (∀ L (y : ∀ j, E j), (1, y) ∈ marked r L ↔
      (∀ j, q j (y j) = 1) ∧ (∀ j, ¬ scope j ⊆ L → y j = 1)) ∧
    (∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M)) := by
  exact ⟨generated_eq_fiber r scope hscope q p hout hcompatible hfix hgen hinj hbase,
    kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj,
    marked_intersection_property r scope hscope q p hout hcompatible hfix hgen hinj hbaseIP⟩

#print axioms supported_kernel_construction

end MathCompression.SupportedKernelGeneration
