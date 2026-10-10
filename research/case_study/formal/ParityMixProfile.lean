import ParityMixLocal

/-!
Exact component profiles of the actual mixed parabolics. The component
factorizations of the two input markings are proved from their IP; the
intersection property of the mix is never a premise.
-/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {I C E G : Type*} [DecidableEq I] [Fintype C] [DecidableEq C]
  [Group E] [Group G]

omit [DecidableEq I] [Fintype C] [DecidableEq C] in
theorem paired_component_comm (e : I → E) (g : I → G) (scope : C → Finset I)
    (hE : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (e i) (e j))
    (hG : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (g i) (g j)) :
    Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d,
      Commute (e i, g i) (e j, g j) := by
  intro c d hcd i hi j hj
  exact Prod.ext (hE hcd i hi j hj).eq (hG hcd i hi j hj).eq

/-- Component membership in the mixed parabolic is equivalent to
membership of each pair of actual unique factor coordinates. -/
theorem mixed_component_profile (e : I → E) (g : I → G) (scope : C → Finset I)
    (hE : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (e i) (e j))
    (hG : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (g i) (g j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (x : ∀ c, marked e (scope c)) (y : ∀ c, marked g (scope c)) :
    (componentAssembly e scope hE x, componentAssembly g scope hG y) ∈
        marked (fun i => (e i, g i)) (Finset.univ.biUnion scope) ↔
      ∀ c, ((x c : E), (y c : G)) ∈ marked (fun i => (e i, g i)) (scope c) := by
  let r := fun i => (e i, g i)
  let hc := paired_component_comm e g scope hE hG
  let af := componentAssembly r scope hc
  have hrange := componentAssembly_range r scope hc
  have hfst (z : ∀ c, marked r (scope c)) :
      (af z).1 = componentAssembly e scope hE
        (fun c => mapMarked r (MonoidHom.fst E G) (scope c) (z c)) :=
    componentAssembly_map r (MonoidHom.fst E G) scope hc hE z
  have hsnd (z : ∀ c, marked r (scope c)) :
      (af z).2 = componentAssembly g scope hG
        (fun c => mapMarked r (MonoidHom.snd E G) (scope c) (z c)) :=
    componentAssembly_map r (MonoidHom.snd E G) scope hc hG z
  constructor
  · intro hm
    rw [← hrange] at hm
    obtain ⟨z, hz⟩ := hm
    have hx : (fun c => mapMarked r (MonoidHom.fst E G) (scope c) (z c)) = x := by
      apply componentAssembly_injective e scope hE hdisj hipE
      rw [← hfst]
      exact congrArg Prod.fst hz
    have hy : (fun c => mapMarked r (MonoidHom.snd E G) (scope c) (z c)) = y := by
      apply componentAssembly_injective g scope hG hdisj hipG
      rw [← hsnd]
      exact congrArg Prod.snd hz
    intro c
    have hxc := congrArg (fun u => (u c : E)) hx
    have hyc := congrArg (fun u => (u c : G)) hy
    have hzval : (z c : E × G) = ((x c : E), (y c : G)) :=
      Prod.ext hxc hyc
    rw [← hzval]
    exact (z c).property
  · intro hm
    let z : ∀ c, marked r (scope c) := fun c => ⟨((x c : E), (y c : G)), hm c⟩
    have heq : af z = (componentAssembly e scope hE x, componentAssembly g scope hG y) := by
      apply Prod.ext
      · rw [hfst]
        rfl
      · rw [hsnd]
        rfl
    rw [← hrange]
    exact ⟨z, heq⟩

#print axioms mixed_component_profile

end MathCompression.ParityMix
