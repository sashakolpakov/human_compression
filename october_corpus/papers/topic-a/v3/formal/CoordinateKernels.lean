import Mathlib.Algebra.Group.Pi.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice
import LiftCertificate

/-!
Coordinate-supported kernels have the exact meet law required to lift
intersection diagrams. The edge-inflation construction supplies the product
kernel and its coordinate description in the written proof.
-/

namespace LeemansCoordinates

variable {E V : Type*} {K : E → Type*} [∀ e, Group (K e)]

def supported (S : Set E) : Subgroup ((e : E) → K e) where
  carrier := {x | ∀ e, e ∉ S → x e = 1}
  one_mem' := by intro e he; rfl
  mul_mem' := by
    intro x y hx hy e he
    simp [hx e he, hy e he]
  inv_mem' := by
    intro x hx e he
    simp [hx e he]

theorem supported_meet (S T : Set E) :
    supported (K := K) S ⊓ supported T = supported (S ∩ T) := by
  ext x
  constructor
  · rintro ⟨hx, hy⟩ e he
    by_cases hs : e ∈ S
    · apply hy e
      intro ht
      exact he ⟨hs, ht⟩
    · exact hx e hs
  · intro h
    constructor
    · intro e he
      apply h e
      intro hst
      exact he hst.1
    · intro e he
      apply h e
      intro hst
      exact he hst.2

def coordinateKernel (scope : E → Set V) (I : Set V) :
    Subgroup ((e : E) → K e) := supported {e | scope e ⊆ I}

theorem coordinate_kernel_meet (scope : E → Set V) (I J : Set V) :
    coordinateKernel (K := K) scope I ⊓ coordinateKernel scope J =
      coordinateKernel scope (I ∩ J) := by
  unfold coordinateKernel
  rw [supported_meet]
  congr 1
  ext e
  exact Set.subset_inter_iff.symm

variable {H G : Type*} [Group H] [Group G]

/-- Once kernel membership is given by coordinate supports, the image
intersection diagram lifts without any separate upstairs intersection test. -/
theorem intersection_transport_with_coordinates
    (π : H →* G) (κ : π.ker ≃* ((e : E) → K e))
    (scope : E → Set V) (P : Set V → Subgroup H)
    (hmono : Monotone P)
    (himage : ∀ I J, (P I).map π ⊓ (P J).map π = (P (I ∩ J)).map π)
    (hcoords : ∀ I (x : π.ker), (x : H) ∈ P I ↔
      κ x ∈ coordinateKernel scope I) :
    ∀ I J, P I ⊓ P J = P (I ∩ J) := by
  intro I J
  apply LeemansLift.intersection_of_image_and_kernel π (P I) (P J) (P (I ∩ J))
  · exact hmono Set.inter_subset_left
  · exact hmono Set.inter_subset_right
  · exact himage I J
  · intro x hx
    let z : π.ker := ⟨x, hx.2⟩
    have hi : κ z ∈ coordinateKernel scope I := (hcoords I z).mp hx.1.1
    have hj : κ z ∈ coordinateKernel scope J := (hcoords J z).mp hx.1.2
    have hij : κ z ∈ coordinateKernel scope (I ∩ J) := by
      rw [← coordinate_kernel_meet]
      exact ⟨hi, hj⟩
    exact (hcoords (I ∩ J) z).mpr hij

#print axioms coordinate_kernel_meet
#print axioms intersection_transport_with_coordinates

end LeemansCoordinates
