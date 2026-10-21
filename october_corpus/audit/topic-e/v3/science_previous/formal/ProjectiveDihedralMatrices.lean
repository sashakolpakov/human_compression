import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Matrix algebra of the projective dihedral centralizer, in its actual
split semisimple and unipotent normal forms. General conjugacy and field
descent remain separate obligations. -/
namespace HumanCompression.ProjectiveDihedral
variable {F : Type*} [Field F]
abbrev Mat2 := Matrix (Fin 2) (Fin 2) F

def projectivelyCommutes (A B : Mat2 (F := F)) : Prop :=
  ∃ c : F, c ≠ 0 ∧ A * B = c • (B * A)

theorem off_diagonal_zero {l u v w z : F}
    (hl : l ≠ 0) (hlsq : l ^ 2 ≠ 1)
    (hdet : u * z - v * w ≠ 0)
    (h : projectivelyCommutes !![u,v;w,z] !![l,0;0,1]) :
    v = 0 ∧ w = 0 := by
  obtain ⟨c, hc, hC⟩ := h
  have h00 := congrArg (fun M : Mat2 (F := F) => M 0 0) hC
  have h01 := congrArg (fun M : Mat2 (F := F) => M 0 1) hC
  have h10 := congrArg (fun M : Mat2 (F := F) => M 1 0) hC
  have h11 := congrArg (fun M : Mat2 (F := F) => M 1 1) hC
  simp [Matrix.mul_apply, Fin.sum_univ_two] at h00 h01 h10 h11
  have hc1 : c = 1 := by
    by_contra hn
    have hcf : 1-c ≠ 0 := sub_ne_zero.mpr (Ne.symm hn)
    have hu : u = 0 := by
      have hh : (1-c)*u*l = 0 := by linear_combination h00
      simpa [hcf, hl] using hh
    have hz : z = 0 := by
      have hh : (1-c)*z = 0 := by linear_combination h11
      simpa [hcf] using hh
    have hv : v ≠ 0 := by intro hv; simp [hu,hz,hv] at hdet
    have hw : w ≠ 0 := by intro hw; simp [hu,hz,hw] at hdet
    have hcl : 1-c*l = 0 := by
      have hh : (1-c*l)*v = 0 := by linear_combination h01
      exact (mul_eq_zero.mp hh).resolve_right hv
    have hlc : l-c = 0 := by
      have hh : (l-c)*w = 0 := by linear_combination h10
      exact (mul_eq_zero.mp hh).resolve_right hw
    apply hlsq
    linear_combination -hcl + l*hlc
  subst c
  have hl1 : l-1 ≠ 0 := by
    intro hh
    have he : l=1 := sub_eq_zero.mp hh
    simp [he] at hlsq
  constructor
  · have hh : (l-1)*v=0 := by linear_combination -h01
    exact (mul_eq_zero.mp hh).resolve_left hl1
  · have hh : (l-1)*w=0 := by linear_combination h10
    exact (mul_eq_zero.mp hh).resolve_left hl1

theorem split_semisimple_centralizer (M : Mat2 (F := F)) (l d : F)
    (hl : l ≠ 0) (hlsq : l ^ 2 ≠ 1) (hd : d ≠ 0) (hdet : M.det ≠ 0)
    (hA : projectivelyCommutes M !![l,0;0,1])
    (hS : projectivelyCommutes M !![0,d;1,0]) :
    ∃ c : F, c ≠ 0 ∧ (M = c • (1 : Mat2 (F := F)) ∨ M = c • !![-1,0;0,1]) := by
  have hM : M = !![M 0 0,M 0 1;M 1 0,M 1 1] := by
    ext i j; fin_cases i <;> fin_cases j <;> rfl
  have hdet' : M 0 0 * M 1 1 - M 0 1 * M 1 0 ≠ 0 := by
    simpa only [Matrix.det_fin_two] using hdet
  have hA' : projectivelyCommutes !![M 0 0,M 0 1;M 1 0,M 1 1] !![l,0;0,1] :=
    hM ▸ hA
  obtain ⟨hv,hw⟩ := off_diagonal_zero hl hlsq hdet' hA'
  have hz : M 1 1 ≠ 0 := by intro hh; simp [hh,hv,hw] at hdet'
  obtain ⟨c,hc,hC⟩ := hS
  have h01 := congrArg (fun B : Mat2 (F := F) => B 0 1) hC
  have h10 := congrArg (fun B : Mat2 (F := F) => B 1 0) hC
  simp [Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two, hv, hw] at h01 h10
  have hu : M 0 0 - c * M 1 1 = 0 := by
    have hh : (M 0 0 - c * M 1 1)*d = 0 := by linear_combination h01
    exact (mul_eq_zero.mp hh).resolve_right hd
  have hh2 : M 1 1 - c * M 0 0 = 0 := sub_eq_zero.mpr h10
  have hsq : (M 0 0)^2 = (M 1 1)^2 := by
    linear_combination (M 0 0)*hu - (M 1 1)*hh2
  refine ⟨M 1 1,hz,?_⟩
  rcases eq_or_eq_neg_of_sq_eq_sq (M 0 0) (M 1 1) hsq with h | h
  · left; ext i j; fin_cases i <;> fin_cases j <;> simp [h,hv,hw]
  · right; ext i j; fin_cases i <;> fin_cases j <;> simp [h,hv,hw]

theorem unipotent_commutant_entries {u v w z : F}
    (hdet : u*z-v*w ≠ 0)
    (h : projectivelyCommutes !![u,v;w,z] !![1,1;0,1]) :
    w = 0 ∧ u = z := by
  obtain ⟨c,hc,hC⟩ := h
  have h00 := congrArg (fun M : Mat2 (F := F) => M 0 0) hC
  have h01 := congrArg (fun M : Mat2 (F := F) => M 0 1) hC
  have h10 := congrArg (fun M : Mat2 (F := F) => M 1 0) hC
  have h11 := congrArg (fun M : Mat2 (F := F) => M 1 1) hC
  simp [Matrix.mul_apply, Fin.sum_univ_two] at h00 h01 h10 h11
  have hc1 : c=1 := by
    by_contra hn
    have hcf : 1-c ≠ 0 := sub_ne_zero.mpr (Ne.symm hn)
    have hw : w=0 := by
      have hh : (1-c)*w=0 := by linear_combination h10
      exact (mul_eq_zero.mp hh).resolve_left hcf
    have hu : u=0 := by
      have hh : (1-c)*u=0 := by linear_combination h00 + c*hw
      exact (mul_eq_zero.mp hh).resolve_left hcf
    exact hdet (by simp [hw,hu])
  subst c
  have hw : w=0 := by linear_combination -h00
  exact ⟨hw,by linear_combination h01⟩

theorem split_unipotent_centralizer (M : Mat2 (F := F)) (d : F)
    (h2 : (2 : F) ≠ 0) (hdet : M.det ≠ 0)
    (hA : projectivelyCommutes M !![1,1;0,1])
    (hS : projectivelyCommutes M !![-1,d;0,1]) :
    ∃ c : F, c ≠ 0 ∧ M = c • (1 : Mat2 (F := F)) := by
  have hM : M = !![M 0 0,M 0 1;M 1 0,M 1 1] := by
    ext i j; fin_cases i <;> fin_cases j <;> rfl
  have hdet' : M 0 0 * M 1 1 - M 0 1 * M 1 0 ≠ 0 := by
    simpa only [Matrix.det_fin_two] using hdet
  have hA' : projectivelyCommutes !![M 0 0,M 0 1;M 1 0,M 1 1] !![1,1;0,1] :=
    hM ▸ hA
  obtain ⟨hw,hu⟩ := unipotent_commutant_entries hdet' hA'
  have hz : M 1 1 ≠ 0 := by intro hh; simp [hh,hw] at hdet'
  obtain ⟨c,hc,hC⟩ := hS
  have h11 := congrArg (fun B : Mat2 (F := F) => B 1 1) hC
  have h01 := congrArg (fun B : Mat2 (F := F) => B 0 1) hC
  simp [Matrix.mul_apply, Matrix.vecMul, dotProduct, Fin.sum_univ_two, hu, hw] at h11 h01
  have hc1 : c=1 := by
    have hh : (c-1)*M 1 1=0 := by linear_combination -h11
    exact sub_eq_zero.mp ((mul_eq_zero.mp hh).resolve_right hz)
  subst c
  have hv : M 0 1=0 := by
    have hh : (2:F)*M 0 1=0 := by linear_combination h01
    exact (mul_eq_zero.mp hh).resolve_left h2
  refine ⟨M 1 1,hz,?_⟩
  ext i j; fin_cases i <;> fin_cases j <;> simp [hu,hv,hw]

/-- The trace-zero representative in the semisimple normal form. -/
theorem trace_zero_representative (l : F) (h2 : (2 : F) ≠ 0) :
    !![l,0;0,1] - ((l+1)/2) • (1 : Mat2 (F := F)) =
      ((1-l)/2) • !![-1,0;0,1] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp <;> field_simp <;> ring

/-- The displayed representative is invertible when the eigenvalues differ. -/
theorem trace_zero_representative_det (l : F) (h2 : (2 : F) ≠ 0)
    (hl : l ≠ 1) :
    ( !![l,0;0,1] - ((l+1)/2) • (1 : Mat2 (F := F))).det ≠ 0 := by
  rw [trace_zero_representative l h2]
  simp [Matrix.det_fin_two, h2, sub_ne_zero.mpr (Ne.symm hl)]

#print axioms off_diagonal_zero
#print axioms split_semisimple_centralizer
#print axioms unipotent_commutant_entries
#print axioms split_unipotent_centralizer
#print axioms trace_zero_representative
#print axioms trace_zero_representative_det
end HumanCompression.ProjectiveDihedral
