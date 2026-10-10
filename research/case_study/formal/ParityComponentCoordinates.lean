import ParityMixComponents

/-! Actual component coordinates and their behavior under support refinement. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration
open scoped BigOperators

variable {I C G : Type*} [DecidableEq I] [Fintype C] [DecidableEq C] [Group G]

noncomputable def componentEquiv (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M)) :
    (∀ c, marked r (scope c)) ≃* marked r (Finset.univ.biUnion scope) := by
  let a := componentAssembly r scope hcomm
  have hm : ∀ x, a x ∈ marked r (Finset.univ.biUnion scope) := by
    intro x
    rw [← componentAssembly_range r scope hcomm]
    exact ⟨x, rfl⟩
  let f := a.codRestrict _ hm
  apply MulEquiv.ofBijective f
  constructor
  · intro x y hxy
    apply componentAssembly_injective r scope hcomm hdisj hip
    exact congrArg Subtype.val hxy
  · intro y
    have hy : (y : G) ∈ (componentAssembly r scope hcomm).range := by
      rw [componentAssembly_range r scope hcomm]
      exact y.property
    obtain ⟨x, hx⟩ := hy
    exact ⟨x, Subtype.ext hx⟩

theorem componentEquiv_apply (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M))
    (x : ∀ c, marked r (scope c)) :
    (componentEquiv r scope hcomm hdisj hip x : G) = componentAssembly r scope hcomm x := rfl

noncomputable def componentCoordinate (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M)) (c : C) :
    marked r (Finset.univ.biUnion scope) →* G :=
  (marked r (scope c)).subtype.comp
    ((Pi.evalMonoidHom (fun d => marked r (scope d)) c).comp
      (componentEquiv r scope hcomm hdisj hip).symm.toMonoidHom)

/-- A whole element supported in a single component has that value in
its own coordinate and identity in every other coordinate. -/
theorem componentCoordinate_local (r : I → G) (scope : C → Finset I)
    (hcomm : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M))
    (c d : C) (x : marked r (scope d))
    (hx : (x : G) ∈ marked r (Finset.univ.biUnion scope)) :
    componentCoordinate r scope hcomm hdisj hip c ⟨x, hx⟩ =
      if c = d then (x : G) else 1 := by
  have he : componentEquiv r scope hcomm hdisj hip (Pi.mulSingle d x) = ⟨x, hx⟩ := by
    apply Subtype.ext
    rw [componentEquiv_apply]
    exact Subgroup.noncommPiCoprod_mulSingle
      (H := fun c => marked r (scope c))
      (hcomm := fun c d hcd => marked_commute r (scope c) (scope d) (hcomm hcd)) d x
  change (((componentEquiv r scope hcomm hdisj hip).symm ⟨x, hx⟩) c : G) = _
  rw [← he, MulEquiv.symm_apply_apply]
  by_cases hcd : c = d
  · subst c
    simp
  · simp [hcd]

#print axioms componentCoordinate_local

variable {T A : Type*} [Fintype T] [DecidableEq T] [CommGroup A]

/-- A homomorphism from a finite direct product to a commutative group is
the product of its restrictions to the individual coordinate factors. -/
theorem hom_pi_product {F : T → Type*} [∀ t, Group (F t)]
    (f : (∀ t, F t) →* A) (x : ∀ t, F t) :
    f x = ∏ t, f (Pi.mulSingle t (x t)) := by
  conv_lhs => rw [← Finset.noncommProd_mulSingle x]
  rw [Finset.map_noncommProd, Finset.noncommProd_eq_prod]

omit [DecidableEq T] in
/-- An assembled family whose every support lies in U is an element of
the actual marked parabolic on U. -/
theorem componentAssembly_mem_super (r : I → G) (scope : T → Finset I)
    (hcomm : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (r i) (r j))
    (U : Finset I) (hsub : ∀ t, scope t ⊆ U) (x : ∀ t, marked r (scope t)) :
    componentAssembly r scope hcomm x ∈ marked r U := by
  apply marked_mono r (show Finset.univ.biUnion scope ⊆ U from by
    intro i hi
    obtain ⟨t, _, hit⟩ := Finset.mem_biUnion.mp hi
    exact hsub t hit)
  rw [← componentAssembly_range r scope hcomm]
  exact ⟨x, rfl⟩

/-- Refining a support partition gives an exact formula for every
coarse-coordinate character. This derives the row and column parity
sums from actual group elements; it does not assume those sums. -/
theorem component_coordinate_refinement (r : I → G)
    (coarse : C → Finset I) (fine : T → Finset I)
    (hc : Pairwise fun c d => ∀ i ∈ coarse c, ∀ j ∈ coarse d, Commute (r i) (r j))
    (hf : Pairwise fun c d => ∀ i ∈ fine c, ∀ j ∈ fine d, Commute (r i) (r j))
    (hd : Pairwise fun c d => Disjoint (coarse c) (coarse d))
    (hip : ∀ L M, marked r L ⊓ marked r M = marked r (L ∩ M))
    (parent : T → C) (hsub : ∀ t, fine t ⊆ coarse (parent t))
    (ε : G →* A) (c : C) (x : ∀ t, marked r (fine t))
    (hx : componentAssembly r fine hf x ∈ marked r (Finset.univ.biUnion coarse)) :
    ε (componentCoordinate r coarse hc hd hip c ⟨componentAssembly r fine hf x, hx⟩) =
      ∏ t, if c = parent t then ε (x t) else 1 := by
  have hU : ∀ t, fine t ⊆ Finset.univ.biUnion coarse := by
    intro t i hi
    exact Finset.mem_biUnion.mpr ⟨parent t, Finset.mem_univ _, hsub t hi⟩
  let a := (componentAssembly r fine hf).codRestrict
    (marked r (Finset.univ.biUnion coarse))
    (componentAssembly_mem_super r fine hf _ hU)
  let f := (componentCoordinate r coarse hc hd hip c).comp a
  have hsingle (t : T) (y : marked r (fine t)) :
      f (Pi.mulSingle t y) = if c = parent t then (y : G) else 1 := by
    have hval : componentAssembly r fine hf (Pi.mulSingle t y) = (y : G) :=
      Subgroup.noncommPiCoprod_mulSingle
        (H := fun t => marked r (fine t))
        (hcomm := fun t u htu => marked_commute r (fine t) (fine u) (hf htu)) t y
    let z : marked r (coarse (parent t)) := ⟨y, marked_mono r (hsub t) y.property⟩
    have hz : (z : G) ∈ marked r (Finset.univ.biUnion coarse) :=
      marked_mono r (hU t) y.property
    have haz : a (Pi.mulSingle t y) = ⟨z, hz⟩ := Subtype.ext hval
    change componentCoordinate r coarse hc hd hip c (a (Pi.mulSingle t y)) = _
    rw [haz]
    exact componentCoordinate_local r coarse hc hd hip c (parent t) z hz
  change ε (f x) = _
  have hp := hom_pi_product (ε.comp f) x
  change ε (f x) = ∏ t, ε (f (Pi.mulSingle t (x t))) at hp
  rw [hp]
  apply Finset.prod_congr rfl
  intro t _
  rw [hsingle]
  by_cases hct : c = parent t <;> simp [hct]

#print axioms hom_pi_product
#print axioms componentAssembly_mem_super
#print axioms component_coordinate_refinement

end MathCompression.ParityMix
