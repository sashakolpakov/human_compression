import Mathlib.Data.Finset.Max
import Mathlib.Data.Fintype.Prod
import Mathlib.Order.Interval.Set.OrdConnected
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
Two disjoint families of finite integer intervals have a hereditary leaf property.
Consequently overlap weights with zero row and column sums vanish, even in an
additive commutative monoid. Empty intervals are permitted. Neither a forest
assumption nor additive cancellation is an input.
-/

namespace MathCompression.IntervalOverlapCancellation

open scoped BigOperators

variable {J K A : Type*}

/-- An overlapping interval whose right endpoint is later contains the earlier
right endpoint. -/
theorem endpoint_mem {s t : Finset ℕ}
    (ht : Set.OrdConnected (t : Set ℕ)) (hst : ¬ Disjoint s t)
    (hend : s.sup id ≤ t.sup id) : s.sup id ∈ t := by
  obtain ⟨x, hxs, hxt⟩ := Finset.not_disjoint_iff.mp hst
  have hmax : t.sup id ∈ t := by
    simpa only [Set.image_id, Finset.mem_coe] using
      (Finset.sup_mem_of_nonempty (f := id) ⟨x, hxt⟩)
  exact ht.out hxt hmax ⟨Finset.le_sup (f := id) hxs, hend⟩

/-- Every nonempty subgraph of the overlap graph has an edge incident to a leaf.
The arbitrary predicate `E` makes heredity explicit: all edges may be deleted
before applying the result. -/
theorem exists_leaf [Fintype J] [Fintype K]
    (L : J → Finset ℕ) (R : K → Finset ℕ)
    (hL : ∀ j, Set.OrdConnected (L j : Set ℕ))
    (hR : ∀ k, Set.OrdConnected (R k : Set ℕ))
    (dL : Pairwise (fun j j' => Disjoint (L j) (L j')))
    (dR : Pairwise (fun k k' => Disjoint (R k) (R k')))
    (E : J → K → Prop)
    (hE : ∀ j k, E j k → ¬ Disjoint (L j) (R k))
    (hne : ∃ j k, E j k) :
    ∃ j k, E j k ∧
      ((∀ k', E j k' → k' = k) ∨ (∀ j', E j' k → j' = j)) := by
  classical
  let edges : Finset (J × K) := Finset.univ.filter (fun p => E p.1 p.2)
  have hmem (j : J) (k : K) : (j, k) ∈ edges ↔ E j k := by simp [edges]
  have hedges : edges.Nonempty := by
    obtain ⟨j, k, hjk⟩ := hne
    exact ⟨(j, k), (hmem j k).mpr hjk⟩
  obtain ⟨⟨j, k⟩, hjk, hmin⟩ := edges.exists_min_image
    (fun p => min ((L p.1).sup id) ((R p.2).sup id)) hedges
  have he : E j k := (hmem j k).mp hjk
  refine ⟨j, k, he, ?_⟩
  rcases le_total ((L j).sup id) ((R k).sup id) with hl | hr
  · left
    have hk : (L j).sup id ∈ R k := endpoint_mem (hR k) (hE j k he) hl
    intro k' hk'
    have hm := hmin (j, k') ((hmem j k').mpr hk')
    rw [min_eq_left hl] at hm
    have hk'mem : (L j).sup id ∈ R k' :=
      endpoint_mem (hR k') (hE j k' hk') ((le_min_iff.mp hm).2)
    by_contra hneq
    exact (Finset.disjoint_left.mp (dR hneq)) hk'mem hk
  · right
    have hj : (R k).sup id ∈ L j :=
      endpoint_mem (hL j) (fun h => hE j k he h.symm) hr
    intro j' hj'
    have hm := hmin (j', k) ((hmem j' k).mpr hj')
    rw [min_eq_right hr] at hm
    have hj'mem : (R k).sup id ∈ L j' :=
      endpoint_mem (hL j') (fun h => hE j' k hj' h.symm) ((le_min_iff.mp hm).1)
    by_contra hneq
    exact (Finset.disjoint_left.mp (dL hneq)) hj'mem hj

/-- Zero row and column sums force every supported overlap weight to be zero.
The target requires only an additive commutative monoid, not a group. -/
theorem weights_eq_zero [Fintype J] [Fintype K] [AddCommMonoid A]
    (L : J → Finset ℕ) (R : K → Finset ℕ)
    (hL : ∀ j, Set.OrdConnected (L j : Set ℕ))
    (hR : ∀ k, Set.OrdConnected (R k : Set ℕ))
    (dL : Pairwise (fun j j' => Disjoint (L j) (L j')))
    (dR : Pairwise (fun k k' => Disjoint (R k) (R k')))
    (w : J → K → A)
    (hw : ∀ j k, Disjoint (L j) (R k) → w j k = 0)
    (hrow : ∀ j, ∑ k, w j k = 0)
    (hcol : ∀ k, ∑ j, w j k = 0) :
    ∀ j k, w j k = 0 := by
  classical
  by_contra h
  have hne : ∃ j k, w j k ≠ 0 := by simpa only [not_forall] using h
  obtain ⟨j, k, hjk, hleaf⟩ := exists_leaf L R hL hR dL dR
    (fun j k => w j k ≠ 0) (fun j k hne hd => hne (hw j k hd)) hne
  apply hjk
  rcases hleaf with hleaf | hleaf
  · have hsum : ∑ k', w j k' = w j k := by
      apply Finset.sum_eq_single_of_mem k (Finset.mem_univ _)
      intro k' _ hneq
      by_contra hnz
      exact hneq (hleaf k' hnz)
    exact hsum.symm.trans (hrow j)
  · have hsum : ∑ j', w j' k = w j k := by
      apply Finset.sum_eq_single_of_mem j (Finset.mem_univ _)
      intro j' _ hneq
      by_contra hnz
      exact hneq (hleaf j' hnz)
    exact hsum.symm.trans (hcol k)

end MathCompression.IntervalOverlapCancellation

#print axioms MathCompression.IntervalOverlapCancellation.endpoint_mem
#print axioms MathCompression.IntervalOverlapCancellation.exists_leaf
#print axioms MathCompression.IntervalOverlapCancellation.weights_eq_zero
