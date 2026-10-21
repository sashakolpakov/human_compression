import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.GroupTheory.Perm.Basic

/-!
Actual permutation orbits and their intersections under supported transpositions.
This is the orbit-intersection step of the written common-point theorem, not
an end-to-end formalization of permutation restriction, gluing or a source paper.
No finiteness is needed for the declarations in this file.
-/
namespace HumanCompression.RootOrbitIntersection

variable {α ι : Type*} [DecidableEq α]

def rootOrbit (H : Subgroup (Equiv.Perm α)) (a : α) : Set α :=
  {b | ∃ g : Equiv.Perm α, g ∈ H ∧ g a = b}

def hasRootSwaps (H : Subgroup (Equiv.Perm α)) (a : α) : Prop :=
  ∀ b ∈ rootOrbit H a, Equiv.swap a b ∈ H

omit [DecidableEq α] in
theorem root_mem (H : Subgroup (Equiv.Perm α)) (a : α) :
    a ∈ rootOrbit H a := by
  exact ⟨1, H.one_mem, rfl⟩

omit [DecidableEq α] in
theorem orbit_mono {H K : Subgroup (Equiv.Perm α)} (h : H ≤ K) (a : α) :
    rootOrbit H a ⊆ rootOrbit K a := by
  rintro b ⟨g, hg, hga⟩
  exact ⟨g, h hg, hga⟩

theorem conjugate_root_swap
    (H M : Subgroup (Equiv.Perm α)) (a b : α)
    (hM : M ≤ H) (hfix : ∀ g ∈ M, g a = a)
    (hswap : Equiv.swap a b ∈ H) {x : α} (hx : x ∈ rootOrbit M b) :
    Equiv.swap a x ∈ H := by
  obtain ⟨g, hg, hgb⟩ := hx
  have heq : Equiv.swap a x = g * Equiv.swap a b * g⁻¹ := by
    rw [← Equiv.swap_apply_apply, hfix g hg, hgb]
  rw [heq]
  exact H.mul_mem (H.mul_mem (hM hg) hswap) (H.inv_mem (hM hg))

theorem leaf_orbit_subset
    (H M : Subgroup (Equiv.Perm α)) (a b : α)
    (hM : M ≤ H) (hfix : ∀ g ∈ M, g a = a)
    (hswap : Equiv.swap a b ∈ H) :
    insert a (rootOrbit M b) ⊆ rootOrbit H a := by
  intro x hx
  rcases hx with h | h
  · subst x
    exact root_mem H a
  · exact ⟨Equiv.swap a x, conjugate_root_swap H M a b hM hfix hswap h,
      Equiv.swap_apply_left a x⟩

theorem orbit_inf (H K : Subgroup (Equiv.Perm α)) (a : α)
    (hH : hasRootSwaps H a) (hK : hasRootSwaps K a) :
    rootOrbit (H ⊓ K) a = rootOrbit H a ∩ rootOrbit K a := by
  ext b
  constructor
  · rintro ⟨g, hg, hga⟩
    exact ⟨⟨g, hg.1, hga⟩, ⟨g, hg.2, hga⟩⟩
  · rintro ⟨hbH, hbK⟩
    exact ⟨Equiv.swap a b, ⟨hH b hbH, hK b hbK⟩, Equiv.swap_apply_left a b⟩

theorem family_orbit_inter
    (H : Set ι → Subgroup (Equiv.Perm α)) (a : α)
    (hIP : ∀ J K, H J ⊓ H K = H (J ∩ K))
    (hs : ∀ J, hasRootSwaps (H J) a) (J K : Set ι) :
    rootOrbit (H (J ∩ K)) a = rootOrbit (H J) a ∩ rootOrbit (H K) a := by
  rw [← hIP J K]
  exact orbit_inf (H J) (H K) a (hs J) (hs K)

end HumanCompression.RootOrbitIntersection
#print axioms HumanCompression.RootOrbitIntersection.root_mem
#print axioms HumanCompression.RootOrbitIntersection.orbit_mono
#print axioms HumanCompression.RootOrbitIntersection.orbit_inf
#print axioms HumanCompression.RootOrbitIntersection.family_orbit_inter

#print axioms HumanCompression.RootOrbitIntersection.conjugate_root_swap
#print axioms HumanCompression.RootOrbitIntersection.leaf_orbit_subset
