import IntervalOverlapCancellation
import Mathlib.Data.Fin.Basic

/-! The exact interval-overlap theorem on finite marker types `Fin n`. -/

namespace MathCompression.IntervalOverlapCancellation

open scoped BigOperators

variable {n : ℕ} {J K A : Type*}

/-- Taking natural-number values preserves convexity of finite `Fin n` sets. -/
theorem fin_val_ordConnected (s : Finset (Fin n))
    (hs : Set.OrdConnected (s : Set (Fin n))) :
    Set.OrdConnected ((s.image Fin.val : Finset ℕ) : Set ℕ) := by
  constructor
  intro x hx y hy z hz
  obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
  obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp hy
  let c : Fin n := ⟨z, lt_of_le_of_lt hz.2 b.isLt⟩
  have hc : c ∈ s := hs.out ha hb ⟨hz.1, hz.2⟩
  exact Finset.mem_image.mpr ⟨c, hc, rfl⟩

/-- The value map preserves and reflects disjointness, including empty sets. -/
theorem fin_val_disjoint_iff (s t : Finset (Fin n)) :
    Disjoint (s.image Fin.val) (t.image Fin.val) ↔ Disjoint s t := by
  constructor
  · intro hd
    apply Finset.disjoint_left.mpr
    intro a ha hat
    exact (Finset.disjoint_left.mp hd)
      (Finset.mem_image.mpr ⟨a, ha, rfl⟩) (Finset.mem_image.mpr ⟨a, hat, rfl⟩)
  · intro hd
    apply Finset.disjoint_left.mpr
    intro x hx hxt
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hx
    obtain ⟨b, hb, hba⟩ := Finset.mem_image.mp hxt
    have h : b = a := Fin.ext hba
    exact (Finset.disjoint_left.mp hd) ha (h ▸ hb)

/-- The frozen natural-number interval theorem applied to actual finite marker
sets, with no new graph or group hypothesis. -/
theorem fin_weights_eq_zero [Fintype J] [Fintype K] [AddCommMonoid A]
    (L : J → Finset (Fin n)) (R : K → Finset (Fin n))
    (hL : ∀ j, Set.OrdConnected (L j : Set (Fin n)))
    (hR : ∀ k, Set.OrdConnected (R k : Set (Fin n)))
    (dL : Pairwise (fun j j' => Disjoint (L j) (L j')))
    (dR : Pairwise (fun k k' => Disjoint (R k) (R k')))
    (w : J → K → A)
    (hw : ∀ j k, Disjoint (L j) (R k) → w j k = 0)
    (hrow : ∀ j, ∑ k, w j k = 0)
    (hcol : ∀ k, ∑ j, w j k = 0) :
    ∀ j k, w j k = 0 := by
  apply weights_eq_zero (fun j => (L j).image Fin.val) (fun k => (R k).image Fin.val)
    (fun j => fin_val_ordConnected (L j) (hL j))
    (fun k => fin_val_ordConnected (R k) (hR k))
    (fun j j' h => (fin_val_disjoint_iff (L j) (L j')).mpr (dL h))
    (fun k k' h => (fin_val_disjoint_iff (R k) (R k')).mpr (dR h)) w
    (fun j k h => hw j k ((fin_val_disjoint_iff (L j) (R k)).mp h)) hrow hcol

end MathCompression.IntervalOverlapCancellation

#print axioms MathCompression.IntervalOverlapCancellation.fin_val_ordConnected
#print axioms MathCompression.IntervalOverlapCancellation.fin_val_disjoint_iff
#print axioms MathCompression.IntervalOverlapCancellation.fin_weights_eq_zero
