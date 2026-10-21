import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.FinCases

/-
Literal five-generator output of the specified rank-extension example.
Point k in the written permutation notation corresponds to (k-1 : Fin 10).
This proves the output fails the intersection property. It does not formalize
that the old marking is C or the source's fracture/perfect-split hypotheses.
-/
namespace RankExtensionObstruction

def markedSubgroup {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) (I : Set (Fin n)) : Subgroup G :=
  Subgroup.closure (ρ '' I)

def HasIntersectionProperty {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) : Prop :=
  ∀ I J, markedSubgroup ρ I ⊓ markedSubgroup ρ J = markedSubgroup ρ (I ∩ J)

def sigma : Equiv.Perm (Fin 10) := Equiv.swap 5 6

def delta (i : Fin 5) : Equiv.Perm (Fin 10) :=
  if i = 0 then Equiv.swap 0 1 * Equiv.swap 7 8
  else if i = 1 then Equiv.swap 1 9
  else if i = 2 then Equiv.swap 2 9 * sigma
  else if i = 3 then Equiv.swap 2 3 * sigma
  else Equiv.swap 3 4

def leftLabels : Set (Fin 5) := {1, 2}
def rightLabels : Set (Fin 5) := {3, 4}

theorem delta_involutions : ∀ i, delta i * delta i = 1 ∧ delta i ≠ 1 := by decide

theorem delta_distinct : Function.Injective delta := by decide

theorem delta_string : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val →
    delta i * delta j = delta j * delta i := by decide

theorem sigma_ne_one : sigma ≠ 1 := by decide

theorem left_cube : (delta 1 * delta 2) ^ 3 = sigma := by decide

theorem right_cube : (delta 3 * delta 4) ^ 3 = sigma := by decide

theorem label_intersection : leftLabels ∩ rightLabels = ∅ := by
  ext i
  fin_cases i <;> simp [leftLabels, rightLabels]

theorem sigma_mem_left : sigma ∈ markedSubgroup delta leftLabels := by
  have h1 : delta 1 ∈ markedSubgroup delta leftLabels :=
    Subgroup.subset_closure ⟨1, by simp [leftLabels], rfl⟩
  have h2 : delta 2 ∈ markedSubgroup delta leftLabels :=
    Subgroup.subset_closure ⟨2, by simp [leftLabels], rfl⟩
  rw [← left_cube]
  exact (markedSubgroup delta leftLabels).pow_mem
    ((markedSubgroup delta leftLabels).mul_mem h1 h2) 3

theorem sigma_mem_right : sigma ∈ markedSubgroup delta rightLabels := by
  have h3 : delta 3 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨3, by simp [rightLabels], rfl⟩
  have h4 : delta 4 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨4, by simp [rightLabels], rfl⟩
  rw [← right_cube]
  exact (markedSubgroup delta rightLabels).pow_mem
    ((markedSubgroup delta rightLabels).mul_mem h3 h4) 3

theorem delta_not_C : ¬ HasIntersectionProperty delta := by
  intro h
  have hs : sigma ∈ markedSubgroup delta leftLabels ⊓
      markedSubgroup delta rightLabels := ⟨sigma_mem_left, sigma_mem_right⟩
  rw [h leftLabels rightLabels, label_intersection] at hs
  have hz : sigma = 1 := by simpa [markedSubgroup] using hs
  exact sigma_ne_one hz

#print axioms delta_involutions
#print axioms delta_distinct
#print axioms delta_string
#print axioms sigma_ne_one
#print axioms left_cube
#print axioms right_cube
#print axioms label_intersection
#print axioms sigma_mem_left
#print axioms sigma_mem_right
#print axioms delta_not_C
end RankExtensionObstruction
