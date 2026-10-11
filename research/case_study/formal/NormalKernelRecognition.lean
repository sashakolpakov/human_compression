import Mathlib.Algebra.Group.Subgroup.Pointwise
import Mathlib.GroupTheory.QuotientGroup.Basic

/-!
Coordinate recognition of a normally generated kernel.
No finiteness of the groups, nilpotence, IP, source presentation, or desired
isomorphism is assumed. The finite index set enumerates local kernel factors.
The application-specific facts that the local factors are normal and generate
the kernel of the base map remain genuine hypotheses.
-/

namespace HumanCompression.NormalKernelRecognition

variable {J P B : Type*} [DecidableEq J] [Group P] [Group B]
variable {E : J → Type*} [∀ j, Group (E j)]

omit [DecidableEq J] in
/-- A coordinate which kills each selected local subgroup kills their join. -/
theorem coordinate_kills_join (K : J → Subgroup P) (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (S : Finset J) (i : J) (hi : i ∉ S) :
    (⨆ j ∈ S, K j) ≤ (rho i).ker := by
  refine iSup_le fun j => iSup_le fun hj => ?_
  intro x hx
  exact hzero i j (by intro he; subst j; exact hi hj) x hx

/-- Normality gives a product decomposition; coordinate detection makes it
faithful. No final injectivity or kernel-triviality conclusion is a premise. -/
theorem finite_join_detected (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1)
    (S : Finset J) :
    ∀ x ∈ (⨆ j ∈ S, K j), (∀ i ∈ S, rho i x = 1) → x = 1 := by
  induction S using Finset.induction_on with
  | empty =>
      intro x hx _
      simpa using hx
  | @insert i S hi ih =>
      intro x hx hcoords
      have heq : (⨆ j ∈ insert i S, K j) = K i ⊔ (⨆ j ∈ S, K j) := by
        simp only [Finset.mem_insert, iSup_or, iSup_sup_eq, iSup_iSup_eq_left]
      rw [heq] at hx
      obtain ⟨a, ha, b, hb, hab⟩ := Subgroup.mem_sup_of_normal_left.mp hx
      have hbi : rho i b = 1 := coordinate_kills_join K rho hzero S i hi hb
      have hai : rho i a = 1 := by
        have hxi := hcoords i (Finset.mem_insert_self i S)
        rw [← hab, map_mul, hbi, mul_one] at hxi
        exact hxi
      have ha1 : a = 1 := hfaithful i a ha hai
      have hbx : b = x := by simpa [ha1] using hab
      have hb1 : b = 1 := ih b hb (by
        intro j hj
        rw [hbx]
        exact hcoords j (Finset.mem_insert_of_mem hj))
      exact hbx.symm.trans hb1

/-- All local coordinates together detect the full finite join. -/
theorem all_local_coordinates_detect [Fintype J]
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (rho : ∀ j, P →* E j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1)
    {x : P} (hx : x ∈ ⨆ j, K j) (hcoords : ∀ i, rho i x = 1) : x = 1 := by
  apply finite_join_detected K rho hzero hfaithful Finset.univ x
  · simpa using hx
  · intro i _
    exact hcoords i

/-- The actual homomorphism to the base and all local coordinates. -/
def coordinateMap (pi : P →* B) (rho : ∀ j, P →* E j) :
    P →* B × (∀ j, E j) where
  toFun x := (pi x, fun j => rho j x)
  map_one' := by ext <;> simp
  map_mul' x y := by ext <;> simp

/-- Recognition of the complete group from its base and normal local kernels.
Only local injectivity and base-kernel generation are assumed. -/
theorem normal_kernel_coordinate_injective [Fintype J]
    (pi : P →* B) (rho : ∀ j, P →* E j)
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (hkernel : pi.ker ≤ ⨆ j, K j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i x = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i x = 1 → x = 1) :
    Function.Injective (coordinateMap pi rho) := by
  apply (injective_iff_map_eq_one _).mpr
  intro x hx
  have hbase : pi x = 1 := congrArg Prod.fst hx
  have hcoords : ∀ i, rho i x = 1 := by
    intro i
    exact congrArg (fun y : B × (∀ j, E j) => y.2 i) hx
  exact all_local_coordinates_detect K rho hzero hfaithful
    (hkernel hbase) hcoords

/-- If the coordinate map is obtained through a quotient whose markers already
surject, the preceding recognition gives an actual bijective homomorphism. -/
theorem supported_quotient_bijective {H : Type*} [Group H] [Fintype J]
    (f : P →* H) (hsurj : Function.Surjective f)
    (pi : H →* B) (rho : ∀ j, H →* E j)
    (K : J → Subgroup P) [∀ j, (K j).Normal]
    (hkernel : (pi.comp f).ker ≤ ⨆ j, K j)
    (hzero : ∀ i j, i ≠ j → ∀ x ∈ K j, rho i (f x) = 1)
    (hfaithful : ∀ i, ∀ x ∈ K i, rho i (f x) = 1 → x = 1) :
    Function.Bijective f := by
  refine ⟨?_, hsurj⟩
  intro x y hxy
  apply normal_kernel_coordinate_injective (pi.comp f)
    (fun j => (rho j).comp f) K hkernel hzero hfaithful
  change (pi (f x), fun j => rho j (f x)) = (pi (f y), fun j => rho j (f y))
  rw [hxy]

#print axioms coordinate_kills_join
#print axioms finite_join_detected
#print axioms all_local_coordinates_detect
#print axioms coordinateMap
#print axioms normal_kernel_coordinate_injective
#print axioms supported_quotient_bijective

end HumanCompression.NormalKernelRecognition
