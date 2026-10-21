import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice

/- Actual subgroup orbits in two arbitrary group actions.  The geometric
   path-intersection characterization and all source instantiations are written.
   No normality, finiteness, transitivity or intersection axiom is assumed. -/
namespace SimultaneousActions
variable {G X Y : Type*} [Group G] [MulAction G X] [MulAction G Y]

def inOrbit (S : Subgroup G) (x x' : X) : Prop :=
  ∃ g ∈ S, g • x = x'

def inDiagonal (S : Subgroup G) (x : X) (y : Y) (x' : X) (y' : Y) : Prop :=
  ∃ g ∈ S, g • x = x' ∧ g • y = y'

/-- Repairing the first coordinate reduces the entire intersection to its fiber. -/
theorem intersection_from_fiber (A B C : Subgroup G)
    (hCA : C ≤ A) (hCB : C ≤ B) (x : X) (y : Y)
    (hbase : ∀ x', inOrbit A x x' → inOrbit B x x' → inOrbit C x x')
    (hfiber : ∀ y', inDiagonal A x y x y' → inDiagonal B x y x y' →
      inDiagonal C x y x y') :
    ∀ x' y', inDiagonal A x y x' y' → inDiagonal B x y x' y' →
      inDiagonal C x y x' y' := by
  intro x' y' hA hB
  obtain ⟨a, ha, hax, hay⟩ := hA
  obtain ⟨b, hb, hbx, hby⟩ := hB
  obtain ⟨c, hc, hcx⟩ := hbase x' ⟨a, ha, hax⟩ ⟨b, hb, hbx⟩
  have ha' : inDiagonal A x y x (c⁻¹ • y') := by
    refine ⟨c⁻¹ * a, A.mul_mem (A.inv_mem (hCA hc)) ha, ?_, ?_⟩
    · rw [mul_smul, hax, ← hcx, inv_smul_smul]
    · rw [mul_smul, hay]
  have hb' : inDiagonal B x y x (c⁻¹ • y') := by
    refine ⟨c⁻¹ * b, B.mul_mem (B.inv_mem (hCB hc)) hb, ?_, ?_⟩
    · rw [mul_smul, hbx, ← hcx, inv_smul_smul]
    · rw [mul_smul, hby]
  obtain ⟨d, hd, hdx, hdy⟩ := hfiber (c⁻¹ • y') ha' hb'
  refine ⟨c * d, C.mul_mem hc hd, ?_, ?_⟩
  · rw [mul_smul, hdx, hcx]
  · rw [mul_smul, hdy, smul_inv_smul]

theorem intersection_iff_fiber (A B C : Subgroup G)
    (hCA : C ≤ A) (hCB : C ≤ B) (x : X) (y : Y)
    (hbase : ∀ x', inOrbit A x x' → inOrbit B x x' → inOrbit C x x') :
    (∀ x' y', inDiagonal A x y x' y' → inDiagonal B x y x' y' →
      inDiagonal C x y x' y') ↔
    (∀ y', inDiagonal A x y x y' → inDiagonal B x y x y' →
      inDiagonal C x y x y') := by
  constructor
  · intro h y'
    exact h x y'
  · exact intersection_from_fiber A B C hCA hCB x y hbase

#print axioms intersection_from_fiber
#print axioms intersection_iff_fiber
end SimultaneousActions
