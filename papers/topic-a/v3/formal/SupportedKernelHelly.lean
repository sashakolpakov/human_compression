import SupportedKernelConsequences

/-!
Typed Helly transfer through coordinate kernels. The proof follows the
right-coset convention P*g: x belongs exactly when x*g^-1 belongs to P.
The common fiber and the coordinate solution are proved, not assumed.
-/

namespace MathCompression.SupportedKernelHelly

variable {G H B T A : Type*} [Group G] [Group H] [Group B]

def InRightCoset (P : Subgroup G) (g x : G) : Prop := x * g⁻¹ ∈ P

/-- Rebase a right coset at any one of its elements. -/
theorem right_coset_rebase (P : Subgroup G) (g x y : G)
    (hx : InRightCoset P g x) (hy : InRightCoset P g y) :
    InRightCoset P x y := by
  have hm := P.mul_mem hy (P.inv_mem hx)
  have he : (y * g⁻¹) * (x * g⁻¹)⁻¹ = y * x⁻¹ := by group
  change y * x⁻¹ ∈ P
  exact he ▸ hm

theorem right_coset_trans (P : Subgroup G) (g x y : G)
    (hx : InRightCoset P g x) (hy : InRightCoset P x y) :
    InRightCoset P g y := by
  have hm := P.mul_mem hy hx
  have he : (y * x⁻¹) * (x * g⁻¹) = y * g⁻¹ := by group
  change y * g⁻¹ ∈ P
  exact he ▸ hm

/-- A finite family has at most one coset for each type because its indices
form a finite subset of the type set. Repeated types are not silently allowed. -/
def TypedHelly (P : T → Subgroup G) : Prop :=
  ∀ (K : Finset T) (g : T → G),
    (∀ i ∈ K, ∀ j ∈ K, ∃ x, InRightCoset (P i) (g i) x ∧
      InRightCoset (P j) (g j) x) →
    ∃ x, ∀ i ∈ K, InRightCoset (P i) (g i) x

/-- Pairwise compatible coordinate constraints have one common solution.
Coordinates are free or fixed to one specified value; no group law is used. -/
theorem coordinate_constraints_glue {E : A → Type*} (one : ∀ a, E a)
    (free : T → Set A) (v : T → ∀ a, E a)
    (hpair : ∀ i j a, a ∉ free i → a ∉ free j → v i a = v j a) :
    ∃ w : ∀ a, E a, ∀ i a, a ∉ free i → w a = v i a := by
  classical
  let w : ∀ a, E a := fun a =>
    if h : ∃ i, a ∉ free i then v h.choose a else one a
  refine ⟨w, ?_⟩
  intro i a ha
  have hex : ∃ i, a ∉ free i := ⟨i, ha⟩
  simp only [w, dif_pos hex]
  exact hpair _ i a hex.choose_spec ha

/-- Move a common point of two right cosets into a specified common base
fiber. The intersection-image identity supplies the adjustment element. -/
theorem common_fiber_pair (q : H →* B)
    (P₁ P₂ : Subgroup H) (Q₁ Q₂ : Subgroup B)
    (h₁ : P₁.map q = Q₁) (h₂ : P₂.map q = Q₂)
    (hinter : (P₁ ⊓ P₂).map q = Q₁ ⊓ Q₂)
    (g₁ g₂ : H) (b : B)
    (hb₁ : InRightCoset Q₁ (q g₁) b)
    (hb₂ : InRightCoset Q₂ (q g₂) b)
    (hmeet : ∃ x, InRightCoset P₁ g₁ x ∧ InRightCoset P₂ g₂ x) :
    ∃ y, q y = b ∧ InRightCoset P₁ g₁ y ∧ InRightCoset P₂ g₂ y := by
  obtain ⟨x, hx₁, hx₂⟩ := hmeet
  have image_mem (P : Subgroup H) (Q : Subgroup B) (he : P.map q = Q)
      (g : H) (hx : InRightCoset P g x) : InRightCoset Q (q g) (q x) := by
    have hm : q (x * g⁻¹) ∈ P.map q := ⟨x * g⁻¹, hx, rfl⟩
    rw [he] at hm
    simpa [InRightCoset] using hm
  have hδ₁ := right_coset_rebase Q₁ (q g₁) (q x) b (image_mem P₁ Q₁ h₁ g₁ hx₁) hb₁
  have hδ₂ := right_coset_rebase Q₂ (q g₂) (q x) b (image_mem P₂ Q₂ h₂ g₂ hx₂) hb₂
  have hδ : b * (q x)⁻¹ ∈ (P₁ ⊓ P₂).map q := by
    rw [hinter]
    exact ⟨hδ₁, hδ₂⟩
  obtain ⟨h, hh, he⟩ := hδ
  refine ⟨h * x, ?_, ?_, ?_⟩
  · rw [map_mul, he]
    group
  · have hm := P₁.mul_mem hh.1 hx₁
    simpa [InRightCoset, mul_assoc] using hm
  · have hm := P₂.mul_mem hh.2 hx₂
    simpa [InRightCoset, mul_assoc] using hm

/-- Kernel coordinates identify a right coset in a fixed base fiber with
its fixed-coordinate constraints, including both implications. -/
theorem coordinate_coset_iff {E : A → Type*} [∀ a, Group (E a)]
    (q : H →* B) (P : Subgroup H) (e : q.ker ≃* (∀ a, E a))
    (free : Set A)
    (hprofile : ∀ k : q.ker, k.val ∈ P ↔ ∀ a, a ∉ free → e k a = 1)
    (u : H) (k l : q.ker) :
    InRightCoset P (l.val * u) (k.val * u) ↔
      ∀ a, a ∉ free → e k a = e l a := by
  have he : (k.val * u) * (l.val * u)⁻¹ = (k * l⁻¹).val := by
    change (k.val * u) * (l.val * u)⁻¹ = k.val * l.val⁻¹
    group
  unfold InRightCoset
  rw [he, hprofile]
  simp only [map_mul, map_inv, Pi.mul_apply, Pi.inv_apply, mul_inv_eq_one]

#print axioms right_coset_rebase
#print axioms right_coset_trans
#print axioms coordinate_constraints_glue
#print axioms common_fiber_pair
#print axioms coordinate_coset_iff


/-- Typed Helly transfers through an explicitly coordinated kernel. The
common base fiber, its pairwise intersections and the coordinate solution
are all constructed in the proof. No intersection property upstairs or common-fiber
Helly conclusion is assumed. -/
theorem typed_helly_transfer {E : A → Type*} [∀ a, Group (E a)]
    (q : H →* B) (hq : Function.Surjective q)
    (P : T → Subgroup H) (Q : T → Subgroup B)
    (himage : ∀ i, (P i).map q = Q i)
    (hinter : ∀ i j, ((P i) ⊓ (P j)).map q = (Q i) ⊓ (Q j))
    (e : q.ker ≃* (∀ a, E a)) (free : T → Set A)
    (hprofile : ∀ i (k : q.ker), k.val ∈ P i ↔
      ∀ a, a ∉ free i → e k a = 1)
    (hbase : TypedHelly Q) : TypedHelly P := by
  classical
  intro K g hpair
  have hbasepair : ∀ i ∈ K, ∀ j ∈ K,
      ∃ x, InRightCoset (Q i) (q (g i)) x ∧ InRightCoset (Q j) (q (g j)) x := by
    intro i hi j hj
    obtain ⟨x, hxi, hxj⟩ := hpair i hi j hj
    refine ⟨q x, ?_, ?_⟩
    · have hm : q (x * (g i)⁻¹) ∈ (P i).map q := ⟨_, hxi, rfl⟩
      rw [himage i] at hm
      simpa [InRightCoset] using hm
    · have hm : q (x * (g j)⁻¹) ∈ (P j).map q := ⟨_, hxj, rfl⟩
      rw [himage j] at hm
      simpa [InRightCoset] using hm
  obtain ⟨b, hb⟩ := hbase K (fun i => q (g i)) hbasepair
  obtain ⟨u, hu⟩ := hq b
  have hfiber : ∀ i ∈ K, ∀ j ∈ K,
      ∃ y, q y = b ∧ InRightCoset (P i) (g i) y ∧ InRightCoset (P j) (g j) y := by
    intro i hi j hj
    exact common_fiber_pair q (P i) (P j) (Q i) (Q j)
      (himage i) (himage j) (hinter i j) (g i) (g j) b
      (hb i hi) (hb j hj) (hpair i hi j hj)
  choose x hx using fun i : {i // i ∈ K} => hfiber i.val i.property i.val i.property
  let k : {i // i ∈ K} → q.ker := fun i =>
    ⟨x i * u⁻¹, by simp only [MonoidHom.mem_ker, map_mul, map_inv, (hx i).1, hu,
      mul_inv_cancel]⟩
  have hxrep : ∀ i, (k i).val * u = x i := by
    intro i
    dsimp [k]
    group
  have hagree : ∀ i j a, a ∉ free i.val → a ∉ free j.val →
      e (k i) a = e (k j) a := by
    intro i j a hai haj
    obtain ⟨y, hyq, hyi, hyj⟩ := hfiber i.val i.property j.val j.property
    let ky : q.ker := ⟨y * u⁻¹, by simp only [MonoidHom.mem_ker, map_mul, map_inv, hyq, hu,
      mul_inv_cancel]⟩
    have hyrep : ky.val * u = y := by dsimp [ky]; group
    have hci : InRightCoset (P i.val) ((k i).val * u) (ky.val * u) := by
      rw [hxrep, hyrep]
      exact right_coset_rebase (P i.val) (g i.val) (x i) y (hx i).2.1 hyi
    have hcj : InRightCoset (P j.val) ((k j).val * u) (ky.val * u) := by
      rw [hxrep, hyrep]
      exact right_coset_rebase (P j.val) (g j.val) (x j) y (hx j).2.1 hyj
    have hvi := (coordinate_coset_iff q (P i.val) e (free i.val)
      (hprofile i.val) u ky (k i)).mp hci a hai
    have hvj := (coordinate_coset_iff q (P j.val) e (free j.val)
      (hprofile j.val) u ky (k j)).mp hcj a haj
    exact hvi.symm.trans hvj
  obtain ⟨w, hw⟩ := coordinate_constraints_glue (fun a => (1 : E a))
    (fun i : {i // i ∈ K} => free i.val) (fun i => e (k i)) hagree
  let z : q.ker := e.symm w
  refine ⟨z.val * u, ?_⟩
  intro i hi
  have hc : InRightCoset (P i) ((k ⟨i, hi⟩).val * u) (z.val * u) := by
    apply (coordinate_coset_iff q (P i) e (free i) (hprofile i) u z (k ⟨i, hi⟩)).mpr
    intro a ha
    simpa [z] using hw ⟨i, hi⟩ a ha
  rw [hxrep] at hc
  exact right_coset_trans (P i) (g i) (x ⟨i, hi⟩) (z.val * u) (hx ⟨i, hi⟩).2.1 hc

#print axioms typed_helly_transfer


open MathCompression.SupportedKernelGeneration

section GeneralMarkedTransfer

variable {I : Type*} [DecidableEq I]

/-- For corresponding marked parabolics, base IP supplies the exact
intersection-image identity. No IP of the group upstairs is required. -/
theorem marked_intersection_image (r : I → H) (q : H →* B)
    (hbaseIP : ∀ L M : Finset I,
      marked (fun i => q (r i)) L ⊓ marked (fun i => q (r i)) M =
        marked (fun i => q (r i)) (L ∩ M))
    (L M : Finset I) :
    (marked r L ⊓ marked r M).map q =
      marked (fun i => q (r i)) L ⊓ marked (fun i => q (r i)) M := by
  ext b
  constructor
  · rintro ⟨w, hw, rfl⟩
    constructor
    · rw [← marked_map r q L]
      exact ⟨w, hw.1, rfl⟩
    · rw [← marked_map r q M]
      exact ⟨w, hw.2, rfl⟩
  · intro hb
    have hb' : b ∈ marked (fun i => q (r i)) (L ∩ M) := by
      rw [← hbaseIP]
      exact hb
    rw [← marked_map r q (L ∩ M)] at hb'
    obtain ⟨w, hw, rfl⟩ := hb'
    exact ⟨w, ⟨marked_mono r Finset.inter_subset_left hw,
      marked_mono r Finset.inter_subset_right hw⟩, rfl⟩

/-- The general marked coordinate-kernel theorem U.SK.Helly. Its hypotheses
are exactly a quotient, base IP, kernel coordinates and the selected
parabolic kernel profiles; the intersection-image premise is now derived. -/
theorem marked_typed_helly {E : A → Type*} [∀ a, Group (E a)]
    (r : I → H) (q : H →* B) (hq : Function.Surjective q)
    (hbaseIP : ∀ L M : Finset I,
      marked (fun i => q (r i)) L ⊓ marked (fun i => q (r i)) M =
        marked (fun i => q (r i)) (L ∩ M))
    (labels : T → Finset I)
    (e : q.ker ≃* (∀ a, E a)) (free : T → Set A)
    (hprofile : ∀ t (k : q.ker), k.val ∈ marked r (labels t) ↔
      ∀ a, a ∉ free t → e k a = 1)
    (hbase : TypedHelly (fun t => marked (fun i => q (r i)) (labels t))) :
    TypedHelly (fun t => marked r (labels t)) := by
  exact typed_helly_transfer q hq (fun t => marked r (labels t))
    (fun t => marked (fun i => q (r i)) (labels t))
    (fun t => marked_map r q (labels t))
    (fun s t => marked_intersection_image r q hbaseIP (labels s) (labels t))
    e free hprofile hbase

#print axioms marked_intersection_image
#print axioms marked_typed_helly

end GeneralMarkedTransfer

section ActualSupportedKernels

variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]
variable {E : J → Type*} [∀ j, Group (E j)]

/-- The actual L-parabolic regarded as a subgroup of the fully generated
group. This uses subgroup inclusion, not an abstractly postulated marking. -/
def parabolicInFull (r : I → B × (∀ j, E j)) (L : Finset I) :
    Subgroup (marked r Finset.univ) :=
  (marked r L).comap (marked r Finset.univ).subtype

omit [DecidableEq I] [Fintype J] [DecidableEq J] in
/-- Every actual parabolic has precisely its corresponding base image. -/
theorem parabolicInFull_image (r : I → B × (∀ j, E j)) (L : Finset I) :
    (parabolicInFull r L).map (baseProjection r Finset.univ) =
      marked (fun i => (r i).1) L := by
  ext b
  constructor
  · rintro ⟨w, hw, rfl⟩
    rw [← baseProjection_range r L]
    exact ⟨⟨w.val, hw⟩, rfl⟩
  · intro hb
    rw [← baseProjection_range r L] at hb
    obtain ⟨w, hw⟩ := hb
    refine ⟨⟨w.val, marked_mono r (Finset.subset_univ _) w.property⟩, w.property, ?_⟩
    exact hw

/-- The already proved coordinate equivalence is multiplicative. The
subtype's multiplication is the literal coordinatewise multiplication. -/
noncomputable def kernelCoordinatesMulEquiv
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (q : ∀ j, E j →* B) (L : Finset I)
    (hprofile : ∀ y : ∀ j, E j, (1, y) ∈ marked r L ↔
      (∀ j, q j (y j) = 1) ∧ (∀ j, ¬ scope j ⊆ L → y j = 1)) :
    (baseProjection r L).ker ≃* (∀ j : {j // scope j ⊆ L}, (q j.val).ker) :=
  { kernelCoordinatesEquiv r scope q L hprofile with
    map_mul' := by intro x y; rfl }

/-- The exact supported-kernel attachment to typed Helly transfer. The
kernel profile, coordinate isomorphism and intersection-image identities
are proved from the construction. The permitted types may select any family
of label subsets, such as the maximal parabolics. -/
theorem supported_kernel_typed_helly
    (r : I → B × (∀ j, E j)) (scope : J → Finset I)
    (hscope : Function.Injective scope)
    (q : ∀ j, E j →* B) (p : J → B →* B)
    (hout : ∀ j i, i ∉ scope j → (r i).2 j = 1)
    (hcompatible : ∀ j i, q j ((r i).2 j) = p j ((r i).1))
    (hfix : ∀ j i, i ∈ scope j → p j ((r i).1) = (r i).1)
    (hgen : ∀ j, marked (fun i => (r i).2 j) (scope j) = ⊤)
    (hinj : ∀ j (L : Finset I), L ⊂ scope j →
      ∀ x ∈ marked (fun i => (r i).2 j) L, q j x = 1 → x = 1)
    (hbasegen : marked (fun i => (r i).1) Finset.univ = ⊤)
    (hbaseIP : ∀ L M : Finset I,
      marked (fun i => (r i).1) L ⊓ marked (fun i => (r i).1) M =
        marked (fun i => (r i).1) (L ∩ M))
    (labels : T → Finset I)
    (hbaseHelly : TypedHelly (fun t => marked (fun i => (r i).1) (labels t))) :
    TypedHelly (fun t => parabolicInFull r (labels t)) := by
  classical
  let π := baseProjection r Finset.univ
  let P := fun t => parabolicInFull r (labels t)
  let Q := fun t => marked (fun i => (r i).1) (labels t)
  let e := kernelCoordinatesMulEquiv r scope q Finset.univ
    (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj Finset.univ)
  let free : T → Set {j // scope j ⊆ Finset.univ} :=
    fun t => {j | scope j.val ⊆ labels t}
  have hπ : Function.Surjective π := by
    intro b
    have hb : b ∈ π.range := by
      change b ∈ (baseProjection r Finset.univ).range
      rw [baseProjection_range, hbasegen]
      trivial
    exact hb
  have himage : ∀ t, (P t).map π = Q t := by
    intro t
    exact parabolicInFull_image r (labels t)
  have hinter : ∀ s t, ((P s) ⊓ (P t)).map π = (Q s) ⊓ (Q t) := by
    intro s t
    have hmeet : P s ⊓ P t = parabolicInFull r (labels s ∩ labels t) := by
      change (marked r (labels s)).comap (marked r Finset.univ).subtype ⊓
        (marked r (labels t)).comap (marked r Finset.univ).subtype =
          (marked r (labels s ∩ labels t)).comap (marked r Finset.univ).subtype
      rw [← Subgroup.comap_inf]
      rw [marked_intersection_property r scope hscope q p hout hcompatible hfix hgen hinj
        hbaseIP (labels s) (labels t)]
    rw [hmeet, parabolicInFull_image]
    exact (hbaseIP (labels s) (labels t)).symm
  have hprofile : ∀ t (k : π.ker), k.val ∈ P t ↔
      ∀ a, a ∉ free t → e k a = 1 := by
    intro t k
    have he : (1, k.val.val.2) = k.val.val := Prod.ext k.property.symm rfl
    have hall := (kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj
      Finset.univ k.val.val.2).mp (he ▸ k.val.property)
    change k.val.val ∈ marked r (labels t) ↔ _
    rw [← he, kernel_profile r scope hscope q p hout hcompatible hfix hgen hinj]
    constructor
    · intro hk a ha
      apply Subtype.ext
      exact hk.2 a.val ha
    · intro hk
      refine ⟨hall.1, ?_⟩
      intro j hj
      have hh := hk ⟨j, Finset.subset_univ _⟩ hj
      exact congrArg Subtype.val hh
  exact typed_helly_transfer π hπ P Q himage hinter e free hprofile hbaseHelly

#print axioms parabolicInFull_image
#print axioms kernelCoordinatesMulEquiv
#print axioms supported_kernel_typed_helly

end ActualSupportedKernels

end MathCompression.SupportedKernelHelly
