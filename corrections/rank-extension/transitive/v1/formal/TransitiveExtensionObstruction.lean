import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.FinCases

/-
Actual six-generator output of the transitive degree-eleven example.
Written point k corresponds to (k-1 : Fin 12). Actual subgroups are generated
by Subgroup.closure. This module proves the output fails the intersection
property. The input C property and source split/fracture hypotheses remain
in the complete written proof; no formal source-level disproof is claimed.
-/
set_option maxRecDepth 4096

namespace TransitiveExtensionObstruction

def markedSubgroup {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) (I : Set (Fin n)) : Subgroup G :=
  Subgroup.closure (ρ '' I)

def HasIntersectionProperty {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) : Prop :=
  ∀ I J, markedSubgroup ρ I ⊓ markedSubgroup ρ J = markedSubgroup ρ (I ∩ J)

def beta : Equiv.Perm (Fin 12) := Equiv.swap 2 3

def delta (i : Fin 6) : Equiv.Perm (Fin 12) :=
  if i = 0 then Equiv.swap 7 8 * Equiv.swap 9 10
  else if i = 1 then Equiv.swap 0 7 * Equiv.swap 8 9
  else if i = 2 then Equiv.swap 0 11
  else if i = 3 then Equiv.swap 1 11 * beta
  else if i = 4 then Equiv.swap 1 5 * Equiv.swap 2 4 * Equiv.swap 3 6
  else Equiv.swap 2 3 * Equiv.swap 5 6

def leftLabels : Set (Fin 6) := {2, 3}
def rightLabels : Set (Fin 6) := {3, 4, 5}

def shortWord : Equiv.Perm (Fin 12) :=
  delta 3 * delta 4 * (delta 3 * delta 5 * delta 4) ^ 4 * delta 5

theorem delta_involutions : ∀ i, delta i * delta i = 1 ∧ delta i ≠ 1 := by decide
theorem delta_distinct : Function.Injective delta := by decide
theorem delta_string : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val →
    delta i * delta j = delta j * delta i := by decide
theorem beta_ne_one : beta ≠ 1 := by decide
theorem beta_ne_delta : beta ≠ delta 3 := by decide
theorem left_cube : (delta 2 * delta 3) ^ 3 = beta := by decide
theorem short_word_value : shortWord = Equiv.swap 3 4 := by decide
theorem short_word_conjugate : delta 3 * shortWord * delta 3 = Equiv.swap 2 4 := by decide
theorem beta_word : shortWord * (delta 3 * shortWord * delta 3) * shortWord = beta := by decide

theorem label_intersection : leftLabels ∩ rightLabels = {3} := by
  ext i
  fin_cases i <;> simp [leftLabels, rightLabels]

theorem beta_mem_left : beta ∈ markedSubgroup delta leftLabels := by
  have h2 : delta 2 ∈ markedSubgroup delta leftLabels :=
    Subgroup.subset_closure ⟨2, by simp [leftLabels], rfl⟩
  have h3 : delta 3 ∈ markedSubgroup delta leftLabels :=
    Subgroup.subset_closure ⟨3, by simp [leftLabels], rfl⟩
  rw [← left_cube]
  exact (markedSubgroup delta leftLabels).pow_mem
    ((markedSubgroup delta leftLabels).mul_mem h2 h3) 3

theorem short_word_mem_right : shortWord ∈ markedSubgroup delta rightLabels := by
  have h3 : delta 3 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨3, by simp [rightLabels], rfl⟩
  have h4 : delta 4 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨4, by simp [rightLabels], rfl⟩
  have h5 : delta 5 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨5, by simp [rightLabels], rfl⟩
  let K := markedSubgroup delta rightLabels
  exact K.mul_mem (K.mul_mem (K.mul_mem h3 h4)
    (K.pow_mem (K.mul_mem (K.mul_mem h3 h5) h4) 4)) h5

theorem beta_mem_right : beta ∈ markedSubgroup delta rightLabels := by
  have h3 : delta 3 ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨3, by simp [rightLabels], rfl⟩
  let K := markedSubgroup delta rightLabels
  rw [← beta_word]
  exact K.mul_mem (K.mul_mem short_word_mem_right
    (K.mul_mem (K.mul_mem h3 short_word_mem_right) h3)) short_word_mem_right

def commonBound : Subgroup (Equiv.Perm (Fin 12)) where
  carrier := {g | g = 1 ∨ g = delta 3}
  one_mem' := Or.inl rfl
  mul_mem' := by
    intro a b ha hb
    rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
    · exact Or.inl (one_mul 1)
    · exact Or.inr (one_mul _)
    · exact Or.inr (mul_one _)
    · exact Or.inl (delta_involutions 3).1
  inv_mem' := by
    intro a ha
    rcases ha with rfl | rfl
    · exact Or.inl inv_one
    · exact Or.inr (by decide)

theorem common_subgroup_bound : markedSubgroup delta {3} ≤ commonBound := by
  apply (Subgroup.closure_le commonBound).mpr
  rintro g ⟨i, hi, rfl⟩
  have hi' : i = 3 := Set.mem_singleton_iff.mp hi
  subst i
  exact Or.inr rfl

theorem beta_not_common : beta ∉ markedSubgroup delta {3} := by
  intro h
  rcases common_subgroup_bound h with h | h
  · exact beta_ne_one h
  · exact beta_ne_delta h

theorem delta_not_C : ¬ HasIntersectionProperty delta := by
  intro h
  have hb : beta ∈ markedSubgroup delta leftLabels ⊓
      markedSubgroup delta rightLabels := ⟨beta_mem_left, beta_mem_right⟩
  rw [h leftLabels rightLabels, label_intersection] at hb
  exact beta_not_common hb

#print axioms delta_involutions
#print axioms delta_distinct
#print axioms delta_string
#print axioms beta_ne_one
#print axioms beta_ne_delta
#print axioms left_cube
#print axioms short_word_value
#print axioms short_word_conjugate
#print axioms beta_word
#print axioms label_intersection
#print axioms beta_mem_left
#print axioms short_word_mem_right
#print axioms beta_mem_right
#print axioms common_subgroup_bound
#print axioms beta_not_common
#print axioms delta_not_C
end TransitiveExtensionObstruction
