import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Data.Fintype.Fin
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.FinCases

/-
The exact eighteen-point output in the separate written counterexample.
Written point k corresponds to k-1 : Fin 18. Equiv.Perm uses function
composition, the reverse of the written right-action product. Thus the
written bc is c*b here, the written w=a(bc)^2ba(cb)^8a is reverseWord,
and the written conjugate x^w is reverseWord*x*reverseWord⁻¹.
Actual marked subgroups are Subgroup.closure of the generator images.
The old input C property, its S18 identification and the source hypotheses
are not assertions of this module; they remain in the complete written proof.
-/
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

namespace RankAugmentationObstruction

def a : Equiv.Perm (Fin 18) :=
  Equiv.swap 0 1 * Equiv.swap 4 5 * Equiv.swap 6 7 *
  Equiv.swap 10 11 * Equiv.swap 12 13 * Equiv.swap 16 17

def b : Equiv.Perm (Fin 18) :=
  Equiv.swap 1 2 * Equiv.swap 3 4 * Equiv.swap 6 8 *
  Equiv.swap 9 10 * Equiv.swap 13 14 * Equiv.swap 15 16

def c : Equiv.Perm (Fin 18) :=
  Equiv.swap 2 3 * Equiv.swap 4 6 * Equiv.swap 5 7 *
  Equiv.swap 8 9 * Equiv.swap 10 12 * Equiv.swap 11 13 * Equiv.swap 14 15

def t : Equiv.Perm (Fin 18) := Equiv.swap 0 17

def delta (i : Fin 4) : Equiv.Perm (Fin 18) :=
  if i = 0 then t else if i = 1 then a else if i = 2 then b else c

def markedSubgroup {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) (I : Set (Fin n)) : Subgroup G :=
  Subgroup.closure (ρ '' I)

def HasIntersectionProperty {n : ℕ} {G : Type*} [Group G]
    (ρ : Fin n → G) : Prop :=
  ∀ I J, markedSubgroup ρ I ⊓ markedSubgroup ρ J = markedSubgroup ρ (I ∩ J)

def leftLabels : Set (Fin 4) := {0}
def rightLabels : Set (Fin 4) := {1, 2, 3}

def reverseWord : Equiv.Perm (Fin 18) :=
  a * (b * c) ^ 8 * a * b * (c * b) ^ 2 * a

theorem delta_involutions : ∀ i, delta i * delta i = 1 ∧ delta i ≠ 1 := by decide
theorem delta_distinct : Function.Injective delta := by decide
theorem delta_string : ∀ i j, i.val + 1 < j.val ∨ j.val + 1 < i.val →
    delta i * delta j = delta j * delta i := by decide
theorem t_ne_one : t ≠ 1 := by decide
theorem word_seed : (c * b) ^ 45 = Equiv.swap 5 7 := by
  let p : Equiv.Perm (Fin 18) := Equiv.swap 5 7 * Equiv.swap 11 14 *
    Equiv.swap 14 16 * Equiv.swap 16 15 * Equiv.swap 15 13
  have h9 : (c * b) ^ 9 = p := by decide
  calc
    (c * b) ^ 45 = ((c * b) ^ 9) ^ 5 := by rw [← pow_mul]
    _ = p ^ 5 := by rw [h9]
    _ = Equiv.swap 5 7 := by decide
theorem word_endpoints : reverseWord 5 = 0 ∧ reverseWord 7 = 17 := by decide
theorem witness_word : reverseWord * (c * b) ^ 45 * reverseWord⁻¹ = t := by
  rw [word_seed]
  decide

theorem label_intersection : leftLabels ∩ rightLabels = ∅ := by
  ext i
  fin_cases i <;> simp [leftLabels, rightLabels]

theorem t_mem_left : t ∈ markedSubgroup delta leftLabels := by
  exact Subgroup.subset_closure ⟨0, by simp [leftLabels], rfl⟩

theorem reverse_word_mem_right : reverseWord ∈ markedSubgroup delta rightLabels := by
  have ha : a ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨1, by simp [rightLabels], rfl⟩
  have hb : b ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨2, by simp [rightLabels], rfl⟩
  have hc : c ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨3, by simp [rightLabels], rfl⟩
  let K := markedSubgroup delta rightLabels
  exact K.mul_mem (K.mul_mem (K.mul_mem (K.mul_mem
    (K.mul_mem ha (K.pow_mem (K.mul_mem hb hc) 8)) ha) hb)
    (K.pow_mem (K.mul_mem hc hb) 2)) ha

theorem t_mem_right : t ∈ markedSubgroup delta rightLabels := by
  have hb : b ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨2, by simp [rightLabels], rfl⟩
  have hc : c ∈ markedSubgroup delta rightLabels :=
    Subgroup.subset_closure ⟨3, by simp [rightLabels], rfl⟩
  let K := markedSubgroup delta rightLabels
  rw [← witness_word]
  exact K.mul_mem (K.mul_mem reverse_word_mem_right (K.pow_mem (K.mul_mem hc hb) 45))
    (K.inv_mem reverse_word_mem_right)

theorem empty_marked_subgroup : markedSubgroup delta ∅ = ⊥ := by
  simp [markedSubgroup]

theorem delta_not_C : ¬ HasIntersectionProperty delta := by
  intro h
  have ht : t ∈ markedSubgroup delta leftLabels ⊓ markedSubgroup delta rightLabels :=
    ⟨t_mem_left, t_mem_right⟩
  rw [h leftLabels rightLabels, label_intersection, empty_marked_subgroup] at ht
  exact t_ne_one ht

#print axioms delta_involutions
#print axioms delta_distinct
#print axioms delta_string
#print axioms t_ne_one
#print axioms word_seed
#print axioms word_endpoints
#print axioms witness_word
#print axioms label_intersection
#print axioms t_mem_left
#print axioms reverse_word_mem_right
#print axioms t_mem_right
#print axioms empty_marked_subgroup
#print axioms delta_not_C
end RankAugmentationObstruction
