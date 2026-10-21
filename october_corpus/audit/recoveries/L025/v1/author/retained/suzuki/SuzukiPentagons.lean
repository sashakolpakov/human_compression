import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Algebra.CharP.Two
import Mathlib.Tactic

/-!
Matrix and scalar core of the Suzuki graph pentagon count. The graph/coset
walk correspondence and identification with the source graph are written
proofs. There is no hidden finite-field enumeration in these theorems.
-/
namespace LeemansSuzuki

open scoped CharTwo

variable {K : Type*} [Field K] [CharP K 2]

def z (a A : K) : Matrix (Fin 4) (Fin 4) K :=
  !![1,0,0,0; 0,1,0,0; a,0,1,0; A,a,0,1]

def w : Matrix (Fin 4) (Fin 4) K :=
  !![0,0,0,1; 0,0,1,0; 0,1,0,0; 1,0,0,0]

def five (a A b B c C d D : K) : Matrix (Fin 4) (Fin 4) K :=
  w * z a A * w * z b B * w * z c C * w * z d D * w

def three (a A b B : K) : Matrix (Fin 4) (Fin 4) K :=
  w * z a A * w * z b B * w

def four (a A b B c C : K) : Matrix (Fin 4) (Fin 4) K :=
  w * z a A * w * z b B * w * z c C * w

theorem five_entries (a A b B c C d D : K) :
    (five a A b B c C d D) 2 1 = b*c+1 ∧
    (five a A b B c C d D) 0 1 = A*B*c+a*b*c+a+c ∧
    (five a A b B c C d D) 3 2 = B*C*d+b*c*d+b+d := by
  refine ⟨?_,?_,?_⟩ <;>
    simp [five, z, w, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

theorem no_triangle (a A b B : K) :
    (three a A b B) 2 1 = 1 := by
  simp [three, z, w, Matrix.mul_apply, Fin.sum_univ_succ]

theorem four_entry (a A b B c C : K) :
    (four a A b B c C) 0 1 = A*b := by
  simp [four, z, w, Matrix.mul_apply, Fin.sum_univ_succ]

set_option maxHeartbeats 1500000 in
theorem closing_matrix (a A : K) (ha : a ≠ 0) (hA : A ≠ 0) :
    five a A a⁻¹ A⁻¹ a A a⁻¹ A⁻¹ =
    !![A,0,0,0; 0,a^2/A,0,0; A/a,0,A/a^2,0; 1,a/A,0,A⁻¹] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [five, z, w, Matrix.mul_apply, Fin.sum_univ_succ, ha, hA] <;>
    field_simp

def torus (θ : K ≃+* K) (l : K) : Matrix (Fin 4) (Fin 4) K :=
  !![l*θ l,0,0,0; 0,l,0,0; 0,0,l⁻¹,0; 0,0,0,(l*θ l)⁻¹]

def BorelPart (θ : K ≃+* K) (M : Matrix (Fin 4) (Fin 4) K) : Prop :=
  ∃ u l : K, l ≠ 0 ∧ M = z u (θ u) * torus θ l

theorem torus_parameter (θ : K ≃+* K) (hθ : ∀ x, θ (θ x)=x^2)
    (a : K) (ha : a ≠ 0) :
    a^2 / θ a ≠ 0 ∧ (a^2 / θ a) * θ (a^2 / θ a) = θ a := by
  have hA : θ a ≠ 0 := (map_ne_zero θ).mpr ha
  refine ⟨div_ne_zero (pow_ne_zero 2 ha) hA, ?_⟩
  rw [map_div₀, map_pow, hθ]
  field_simp

set_option maxHeartbeats 1500000 in
theorem closing_in_borel (θ : K ≃+* K) (hθ : ∀ x, θ (θ x)=x^2)
    (a : K) (ha : a ≠ 0) :
    BorelPart θ (five a (θ a) a⁻¹ (θ a⁻¹) a (θ a) a⁻¹ (θ a⁻¹)) := by
  have hA : θ a ≠ 0 := (map_ne_zero θ).mpr ha
  obtain ⟨hl, hn⟩ := torus_parameter θ hθ a ha
  refine ⟨a⁻¹,a^2 / θ a,hl,?_⟩
  simp only [map_inv₀]
  rw [closing_matrix a (θ a) ha hA]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [z, torus, Matrix.mul_apply, Fin.sum_univ_succ, hθ, ha, hA] <;>
    field_simp <;> simp [hθ, ha]

/-- The three forced zero entries classify the four walk parameters. -/
theorem closing_parameters (θ : K ≃+* K) (a b c d : K)
    (h32 : b*c+1=0)
    (h12 : θ a*θ b*c+a*b*c+a+c=0)
    (h43 : θ b*θ c*d+b*c*d+b+d=0) :
    a ≠ 0 ∧ b=a⁻¹ ∧ c=a ∧ d=a⁻¹ := by
  have hbc : b*c=1 := by
    have := eq_neg_of_add_eq_zero_left h32
    simpa only [CharTwo.neg_eq] using this
  have hb : b ≠ 0 := left_ne_zero_of_mul_eq_one hbc
  have hc : c ≠ 0 := right_ne_zero_of_mul_eq_one hbc
  have habθ : θ a*θ b=1 := by
    have habc : a*b*c=a := by rw [mul_assoc, hbc, mul_one]
    rw [habc] at h12
    have hs : (θ a*θ b+1)*c=0 := by
      calc
        (θ a*θ b+1)*c = θ a*θ b*c+c := by ring
        _ = θ a*θ b*c+a+a+c := by simp
        _ = 0 := h12
    have hs' := (mul_eq_zero.mp hs).resolve_right hc
    simpa only [CharTwo.neg_eq] using eq_neg_of_add_eq_zero_left hs'
  have hab : a*b=1 := θ.injective (by simpa using habθ)
  have ha : a ≠ 0 := left_ne_zero_of_mul_eq_one hab
  have hba : b=a⁻¹ := by
    apply mul_left_cancel₀ ha
    simpa [ha] using hab
  have hca : c=a := mul_left_cancel₀ hb (by simpa [mul_comm] using hbc.trans hab.symm)
  have hθbc : θ b*θ c=1 := by simpa using congrArg θ hbc
  rw [hθbc, one_mul, hbc, one_mul] at h43
  have hdb : d=b := by
    have hs : b+d=0 := by simpa [add_assoc, CharTwo.add_self_eq_zero] using h43
    simpa only [CharTwo.neg_eq] using eq_neg_of_add_eq_zero_right hs
  exact ⟨ha,hba,hca,hdb.trans hba⟩

set_option maxHeartbeats 1500000 in
theorem five_in_borel_iff (θ : K ≃+* K) (hθ : ∀ x, θ (θ x)=x^2)
    (a b c d : K) :
    BorelPart θ (five a (θ a) b (θ b) c (θ c) d (θ d)) ↔
    a ≠ 0 ∧ b=a⁻¹ ∧ c=a ∧ d=a⁻¹ := by
  constructor
  · rintro ⟨u,l,hl,heq⟩
    obtain ⟨e32,e12,e43⟩ := five_entries a (θ a) b (θ b) c (θ c) d (θ d)
    have hz32 := congrArg (fun M : Matrix (Fin 4) (Fin 4) K => M 2 1) heq
    have hz12 := congrArg (fun M : Matrix (Fin 4) (Fin 4) K => M 0 1) heq
    have hz43 := congrArg (fun M : Matrix (Fin 4) (Fin 4) K => M 3 2) heq
    rw [e32] at hz32
    rw [e12] at hz12
    rw [e43] at hz43
    simp [z, torus, Matrix.mul_apply, Fin.sum_univ_succ] at hz32 hz12 hz43
    exact closing_parameters θ a b c d hz32 hz12 hz43
  · rintro ⟨ha,hb,hc,hd⟩
    rw [hb,hc,hd]
    exact closing_in_borel θ hθ a ha

#print axioms five_entries
#print axioms closing_matrix
#print axioms closing_parameters
#print axioms five_in_borel_iff
end LeemansSuzuki
