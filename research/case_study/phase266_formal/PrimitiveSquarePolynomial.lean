import Mathlib.Tactic

namespace PrimitiveSquarePolynomial

variable {F : Type*} [Field F]

def quartic (s x : F) : F := (s - 4) * (x ^ 2 + 1) ^ 2 - 4 * s * x ^ 2

def derivative (s x : F) : F := 4 * x * ((s - 4) * x ^ 2 - s - 4)

noncomputable def polynomial (s : F) : Polynomial F :=
  (Polynomial.C s - 4) * (Polynomial.X ^ 2 + 1) ^ 2 - 4 * Polynomial.C s * Polynomial.X ^ 2

theorem evaluated_polynomial (s x : F) :
    Polynomial.eval x (polynomial s) = quartic s x := by
  simp [polynomial, quartic]

theorem evaluated_derivative (s x : F) :
    Polynomial.eval x (polynomial s).derivative = derivative s x := by
  simp [polynomial, derivative, Polynomial.derivative_mul, Polynomial.derivative_pow]
  ring

theorem trace_identity (u x : F) (hx : x ≠ 0) :
    quartic (u ^ 2) x = x ^ 2 *
      (u ^ 2 * (x + x⁻¹) ^ 2 - 4 * (u ^ 2 + (x + x⁻¹) ^ 2)) := by
  unfold quartic
  field_simp
  ring

theorem bezout_identity (s x : F) :
    (s - 4) * quartic s x = ((s - 4) * x ^ 2 - s - 4) ^ 2 - 16 * s := by
  unfold quartic
  ring

theorem distinct_parameters_no_shared_root
    (h2 : (2 : F) ≠ 0) (s t x : F) (hst : s ≠ t)
    (hs : quartic s x = 0) : quartic t x ≠ 0 := by
  intro ht
  have heq : (s - t) * (x ^ 2 - 1) ^ 2 = 0 := by
    calc
      _ = quartic s x - quartic t x := by unfold quartic; ring
      _ = 0 := by rw [hs, ht]; ring
  have hx : x ^ 2 - 1 = 0 := by
    have := (mul_eq_zero.mp heq).resolve_left (sub_ne_zero.mpr hst)
    exact eq_zero_of_pow_eq_zero this
  have hxx : x ^ 2 = 1 := sub_eq_zero.mp hx
  have h16 : (16 : F) ≠ 0 := by
    simpa only [show (2 : F) ^ 4 = 16 by ring] using pow_ne_zero 4 h2
  apply h16
  have hh : quartic s x = -(16 : F) := by unfold quartic; rw [hxx]; ring
  exact neg_eq_zero.mp (hh.symm.trans hs)

theorem no_common_derivative_root
    (h2 : (2 : F) ≠ 0) (s x : F) (hs0 : s ≠ 0) (hs4 : s ≠ 4)
    (hf : quartic s x = 0) : derivative s x ≠ 0 := by
  intro hd
  have hx : x ≠ 0 := by
    intro hzero
    have hh : s - 4 = 0 := by simpa [quartic, hzero] using hf
    exact hs4 (sub_eq_zero.mp hh)
  have h4 : (4 : F) ≠ 0 := by
    simpa only [show (2 : F) ^ 2 = 4 by ring] using pow_ne_zero 2 h2
  have hz : (s - 4) * x ^ 2 - s - 4 = 0 := by
    exact (mul_eq_zero.mp hd).resolve_left (mul_ne_zero h4 hx)
  have hi := bezout_identity s x
  rw [hf, hz] at hi
  have h16 : (16 : F) ≠ 0 := by
    simpa only [show (4 : F) ^ 2 = 16 by ring] using pow_ne_zero 2 h4
  have : (16 : F) * s = 0 := by simpa using hi.symm
  exact (mul_ne_zero h16 hs0) this

#print axioms evaluated_polynomial
#print axioms evaluated_derivative
#print axioms trace_identity
#print axioms bezout_identity
#print axioms distinct_parameters_no_shared_root
#print axioms no_common_derivative_root
end PrimitiveSquarePolynomial
