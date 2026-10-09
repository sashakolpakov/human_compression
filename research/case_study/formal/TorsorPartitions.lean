import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Logic.Relation

/-!
Basis-aware torsor partitions.  A subgroup is exactly a left-translation
invariant equivalence relation on the regular torsor, with intersections
corresponding to entrywise conjunction of incidence matrices.
This file formalizes relations and their zero-one entrywise product, not
ordinary numerical matrix products or rank formulas.
-/

namespace LeemansTorsor

variable {G : Type*} [Group G]

def partitionRelation (H : Subgroup G) (x y : G) : Prop := x⁻¹ * y ∈ H

theorem partition_equivalence (H : Subgroup G) :
    Equivalence (partitionRelation H) := by
  constructor
  · intro x
    simp [partitionRelation]
  · intro x y h
    have hi := H.inv_mem h
    simpa [partitionRelation, mul_inv_rev] using hi
  · intro x y z hxy hyz
    have hm := H.mul_mem hxy hyz
    simpa [partitionRelation, mul_assoc] using hm

theorem partition_left_invariant (H : Subgroup G) (g x y : G) :
    partitionRelation H (g * x) (g * y) ↔ partitionRelation H x y := by
  simp [partitionRelation, mul_inv_rev, mul_assoc]

def subgroupOfRelation (R : G → G → Prop) (heq : Equivalence R)
    (hinv : ∀ g x y, R x y → R (g * x) (g * y)) : Subgroup G where
  carrier := {g | R 1 g}
  one_mem' := heq.refl 1
  mul_mem' := by
    intro a b ha hb
    have hab : R a (a * b) := by simpa using hinv a 1 b hb
    exact heq.trans ha hab
  inv_mem' := by
    intro a ha
    have hi : R a⁻¹ 1 := by simpa using hinv a⁻¹ 1 a ha
    exact heq.symm hi

theorem relation_reconstructed (R : G → G → Prop) (heq : Equivalence R)
    (hinv : ∀ g x y, R x y → R (g * x) (g * y)) (x y : G) :
    partitionRelation (subgroupOfRelation R heq hinv) x y ↔ R x y := by
  change R 1 (x⁻¹ * y) ↔ R x y
  constructor
  · intro h
    simpa [mul_assoc] using hinv x 1 (x⁻¹ * y) h
  · intro h
    simpa using hinv x⁻¹ x y h

theorem subgroup_reconstructed (H : Subgroup G) :
    subgroupOfRelation (partitionRelation H) (partition_equivalence H)
      (fun g x y h => (partition_left_invariant H g x y).mpr h) = H := by
  ext g
  change partitionRelation H 1 g ↔ g ∈ H
  simp [partitionRelation]

theorem partition_intersection (H K : Subgroup G) (x y : G) :
    partitionRelation (H ⊓ K) x y ↔
      partitionRelation H x y ∧ partitionRelation K x y := Iff.rfl

noncomputable def partitionEntry (H : Subgroup G) (x y : G) : ℕ := by
  classical
  exact if partitionRelation H x y then 1 else 0

/-- The exact zero-one Hadamard identity; no finiteness is needed. -/
theorem partition_entrywise_product (H K : Subgroup G) (x y : G) :
    partitionEntry H x y * partitionEntry K x y = partitionEntry (H ⊓ K) x y := by
  classical
  by_cases hh : x⁻¹ * y ∈ H <;> by_cases hk : x⁻¹ * y ∈ K <;>
    simp [partitionEntry, partitionRelation, hh, hk]

theorem partition_injective {H K : Subgroup G}
    (h : ∀ x y, partitionRelation H x y ↔ partitionRelation K x y) : H = K := by
  ext g
  simpa [partitionRelation] using h 1 g

theorem intersection_property_iff_partition
    (H K M : Subgroup G) :
    H ⊓ K = M ↔ ∀ x y,
      (partitionRelation H x y ∧ partitionRelation K x y) ↔ partitionRelation M x y := by
  constructor
  · intro h x y
    rw [← h]
    rfl
  · intro h
    apply partition_injective
    exact h

#print axioms relation_reconstructed
#print axioms subgroup_reconstructed
#print axioms intersection_property_iff_partition
#print axioms partition_entrywise_product

end LeemansTorsor
