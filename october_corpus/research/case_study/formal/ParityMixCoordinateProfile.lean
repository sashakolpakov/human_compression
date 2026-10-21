import ParityMixProfile
import ParityComponentCoordinates

/-! Character profiles in the actual inverse component coordinates. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {I C E G D : Type*} [DecidableEq I] [Fintype C] [DecidableEq C]
  [Group E] [Group G] [Group D]

/-- Exact membership in a mixed parabolic, expressed in its two factors'
actual component coordinates. The local fiber premise is supplied by the
proved interval_support_profile in the final finite-path attachment. -/
theorem mixed_membership_coordinates (e : I → E) (g : I → G) (scope : C → Finset I)
    (hE : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (e i) (e j))
    (hG : Pairwise fun c d => ∀ i ∈ scope c, ∀ j ∈ scope d, Commute (g i) (g j))
    (hdisj : Pairwise fun c d => Disjoint (scope c) (scope d))
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (ε : E →* D) (δ : G →* D)
    (hlocal : ∀ c, ∀ u : marked e (scope c), ∀ v : marked g (scope c),
      ((u : E), (v : G)) ∈ marked (fun i => (e i, g i)) (scope c) ↔ ε u = δ v)
    (x : marked e (Finset.univ.biUnion scope))
    (y : marked g (Finset.univ.biUnion scope)) :
    ((x : E), (y : G)) ∈ marked (fun i => (e i, g i)) (Finset.univ.biUnion scope) ↔
      ∀ c, ε (componentCoordinate e scope hE hdisj hipE c x) =
        δ (componentCoordinate g scope hG hdisj hipG c y) := by
  let ex := componentEquiv e scope hE hdisj hipE
  let ey := componentEquiv g scope hG hdisj hipG
  have hx : componentAssembly e scope hE (ex.symm x) = (x : E) := by
    rw [← componentEquiv_apply e scope hE hdisj hipE]
    exact congrArg Subtype.val (ex.apply_symm_apply x)
  have hy : componentAssembly g scope hG (ey.symm y) = (y : G) := by
    rw [← componentEquiv_apply g scope hG hdisj hipG]
    exact congrArg Subtype.val (ey.apply_symm_apply y)
  have hp := mixed_component_profile e g scope hE hG hdisj hipE hipG (ex.symm x) (ey.symm y)
  rw [hx, hy] at hp
  rw [hp]
  apply forall_congr'
  intro c
  exact hlocal c (ex.symm x c) (ey.symm y c)

#print axioms mixed_membership_coordinates

end MathCompression.ParityMix
