import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-! The Fibonacci modulus and scalar powers of one 2x2 matrix.
This module does not construct the 8D group or prove geometric properties. -/
namespace MathCompression.FibonacciModulus

def N (R : Type*) [Semiring R] : Matrix (Fin 2) (Fin 2) R := !![0,1;1,1]

theorem power_formula (R : Type*) [Semiring R] (n : ℕ) :
    N R ^ (n+1) = !![(Nat.fib n : R), (Nat.fib (n+1) : R);
      (Nat.fib (n+1) : R), (Nat.fib (n+2) : R)] := by
  induction n with
  | zero => simp [N]
  | succ n ih =>
    rw [show n+1+1 = (n+1)+1 by omega, pow_succ, ih]
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [N, Matrix.mul_apply, Fin.sum_univ_two, Nat.fib_add_two, Nat.cast_add]

theorem fib_strict_below {s k : ℕ} (hs : 3 ≤ s) (hk : 0 < k) (hks : k < s) :
    0 < Nat.fib k ∧ Nat.fib k < Nat.fib s := by
  refine ⟨Nat.fib_pos.mpr hk, ?_⟩
  by_cases h : k = 1
  · subst k
    have h2 : Nat.fib 2 < Nat.fib s := (Nat.fib_lt_fib (by omega)).mpr (by omega)
    simpa using h2
  · exact (Nat.fib_lt_fib (by omega)).mpr hks

theorem fib_cast_nonzero {s k : ℕ} (hs : 3 ≤ s) (hk : 0 < k) (hks : k < s) :
    (Nat.fib k : ZMod (Nat.fib s)) ≠ 0 := by
  intro h
  have hd := (ZMod.natCast_eq_zero_iff (Nat.fib k) (Nat.fib s)).mp h
  have hb := fib_strict_below hs hk hks
  exact (not_le_of_gt hb.2) (Nat.le_of_dvd hb.1 hd)

theorem scalar_at_modulus {s : ℕ} (hs : 3 ≤ s) :
    N (ZMod (Nat.fib s)) ^ s =
      !![(Nat.fib (s-1) : ZMod (Nat.fib s)),0;
         0,(Nat.fib (s-1) : ZMod (Nat.fib s))] := by
  have hp := power_formula (ZMod (Nat.fib s)) (s-1)
  have hzero : (Nat.fib s : ZMod (Nat.fib s)) = 0 :=
    (ZMod.natCast_eq_zero_iff _ _).mpr (dvd_refl _)
  have heq : s-1+1 = s := by omega
  rw [heq, show s-1+2 = s+1 by omega] at hp
  rw [hp, Nat.fib_add_one (by omega), Nat.cast_add, hzero, add_zero]

theorem no_earlier_scalar {s k : ℕ} (hs : 3 ≤ s) (hk : 0 < k) (hks : k < s)
    (c : ZMod (Nat.fib s)) :
    N (ZMod (Nat.fib s)) ^ k ≠ !![c,0;0,c] := by
  intro h
  have hp := power_formula (ZMod (Nat.fib s)) (k-1)
  rw [show k-1+1 = k by omega] at hp
  have off := congrArg (fun A : Matrix (Fin 2) (Fin 2) (ZMod (Nat.fib s)) => A 0 1) h
  rw [hp] at off
  exact fib_cast_nonzero hs hk hks (by simpa using off)

#print axioms power_formula
#print axioms fib_cast_nonzero
#print axioms scalar_at_modulus
#print axioms no_earlier_scalar
end MathCompression.FibonacciModulus
