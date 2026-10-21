import NormalKernelRecognition
import Mathlib.GroupTheory.NoncommPiCoprod
import Mathlib.GroupTheory.Commutator.Basic

/-!
The direct-product conclusion of normal kernel recognition.
The product map is multiplication of the actual subgroup factors. Normality,
coordinate detection and generation of the base kernel are explicit hypotheses;
neither finite group order nor the desired isomorphism is assumed.
-/

namespace HumanCompression.NormalKernelRecognition

open scoped commutatorElement

variable {J P B : Type*} [Group P] [Group B]
variable {E : J → Type*} [∀ j, Group (E j)]

/-- Separate faithful coordinates imply independence from the join of all
other factors, even when the index type is infinite. -/
theorem local_coordinates_independent (K : J → Subgroup P)
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    iSupIndep K := by
  apply iSupIndep_def.mpr
  intro i
  apply Subgroup.disjoint_def.mpr
  intro x hxi hothers
  apply hfaithful i x hxi
  have hkilled : (⨆ j, ⨆ (_ : j ≠ i), K j) ≤ (rho i).ker := by
    refine iSup_le fun j => iSup_le fun hji => ?_
    intro y hy
    exact hzero i j hji.symm y hy
  exact hkilled hothers

/-- Normality puts a commutator in one local subgroup; its faithful
coordinate then kills it. Thus different local factors commute. -/
theorem normal_local_factors_commute (K : J → Subgroup P)
    [∀ j, (K j).Normal] (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    Pairwise fun i j => ∀ x y : P, x ∈ K i → y ∈ K j → Commute x y := by
  intro i j hij x y hx hy
  apply commutatorElement_eq_one_iff_commute.mp
  apply hfaithful i ⁅x, y⁆
  · exact (Subgroup.commutator_le_left (K i) (K j))
      (Subgroup.commutator_mem_commutator hx hy)
  · rw [map_commutatorElement, hzero i j hij y hy]
    exact commutatorElement_one_right _

variable [Fintype J]

/-- Multiplication of the actual, commuting local subgroup elements. -/
def kernelProduct (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    (∀ j, K j) →* P :=
  Subgroup.noncommPiCoprod (normal_local_factors_commute K rho hzero hfaithful)

theorem kernelProduct_injective (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    Function.Injective (kernelProduct K rho hzero hfaithful) :=
  Subgroup.injective_noncommPiCoprod_of_iSupIndep
    (local_coordinates_independent K rho hzero hfaithful)

theorem kernelProduct_range (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    (kernelProduct K rho hzero hfaithful).range = ⨆ j, K j :=
  Subgroup.noncommPiCoprod_range

/-- The complete internal direct-product isomorphism onto the base kernel. -/
noncomputable def kernelProductEquiv (pi : P →* B)
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1)
    (hkernel : pi.ker = ⨆ j, K j) :
    (∀ j, K j) ≃* pi.ker :=
  (MonoidHom.ofInjective (kernelProduct_injective K rho hzero hfaithful)).trans
    (MulEquiv.subgroupCongr ((kernelProduct_range K rho hzero hfaithful).trans
      hkernel.symm))

theorem kernelProductEquiv_apply (pi : P →* B)
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1)
    (hkernel : pi.ker = ⨆ j, K j) (x : ∀ j, K j) :
    (kernelProductEquiv pi K rho hzero hfaithful hkernel x : P) =
      kernelProduct K rho hzero hfaithful x := rfl

/-- On a pure factor, this isomorphism is its given subgroup inclusion. -/
theorem kernelProductEquiv_mulSingle [DecidableEq J] (pi : P →* B)
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1)
    (hkernel : pi.ker = ⨆ j, K j) (i : J) (x : K i) :
    (kernelProductEquiv pi K rho hzero hfaithful hkernel (Pi.mulSingle i x) : P) = x := by
  rw [kernelProductEquiv_apply]
  exact Subgroup.noncommPiCoprod_mulSingle i x

#print axioms local_coordinates_independent
#print axioms normal_local_factors_commute
#print axioms kernelProduct
#print axioms kernelProduct_injective
#print axioms kernelProduct_range
#print axioms kernelProductEquiv
#print axioms kernelProductEquiv_apply
#print axioms kernelProductEquiv_mulSingle

end HumanCompression.NormalKernelRecognition
