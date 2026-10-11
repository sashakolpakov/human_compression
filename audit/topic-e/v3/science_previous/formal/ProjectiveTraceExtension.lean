import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-! Algebraic interfaces for projective simultaneous reversal and the trace
extension quadratic. Absolute irreducibility, finite-field existence, group
classification, rotation intersection and geometric realization remain written. -/
namespace HumanCompression.ProjectiveTraceExtension
variable {F : Type*} [Field F]
abbrev Mat2 := Matrix (Fin 2) (Fin 2) F

def adj2 (A : Mat2 (F := F)) : Mat2 (F := F) :=
  !![A 1 1, -A 0 1; -A 1 0, A 0 0]

def comm (A B : Mat2 (F := F)) := A * B - B * A

theorem comm_left_intertwines (A B : Mat2 (F := F)) :
    comm A B * A = adj2 A * comm A B := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [comm, adj2, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem comm_right_intertwines (A B : Mat2 (F := F)) :
    comm A B * B = adj2 B * comm A B := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [comm, adj2, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem comm_square_scalar (A B : Mat2 (F := F)) :
    comm A B * comm A B = -(comm A B).det • (1 : Mat2 (F := F)) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [comm, Matrix.det_fin_two, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

def delta (U V b c : F) := (U ^ 2 + V ^ 2) * (c ^ 2 - 4) - b ^ 2 * c ^ 2

def first (U V b c z : F) := (-b * c * V + z * U) / (U ^ 2 + V ^ 2)
def second (U V b c z : F) := (b * c * U + z * V) / (U ^ 2 + V ^ 2)

theorem norm_decomposition (U V R S : F) :
    (V * R - U * S) ^ 2 + (U * R + V * S) ^ 2 =
      (U ^ 2 + V ^ 2) * (R ^ 2 + S ^ 2) := by ring

theorem forward_linear (U V b c z : F) (hd : U ^ 2 + V ^ 2 ≠ 0) :
    V * first U V b c z - U * second U V b c z = -b * c := by
  unfold first second
  field_simp
  ring

theorem forward_parameter (U V b c z : F) (hd : U ^ 2 + V ^ 2 ≠ 0) :
    U * first U V b c z + V * second U V b c z = z := by
  unfold first second
  field_simp
  ring

theorem forward_norm (U V b c z : F) (hd : U ^ 2 + V ^ 2 ≠ 0)
    (hz : z ^ 2 = delta U V b c) :
    first U V b c z ^ 2 + second U V b c z ^ 2 = c ^ 2 - 4 := by
  have h := norm_decomposition U V (first U V b c z) (second U V b c z)
  rw [forward_linear U V b c z hd, forward_parameter U V b c z hd, hz] at h
  unfold delta at h
  apply (mul_left_cancel₀ hd)
  linear_combination -h

theorem inverse_parameter (U V b c R S : F)
    (hline : V * R - U * S = -b * c) (hnorm : R ^ 2 + S ^ 2 = c ^ 2 - 4) :
    (U * R + V * S) ^ 2 = delta U V b c := by
  have h := norm_decomposition U V R S
  rw [hline, hnorm] at h
  unfold delta
  linear_combination h

theorem inverse_coordinates (U V b c R S : F) (hd : U ^ 2 + V ^ 2 ≠ 0)
    (hline : V * R - U * S = -b * c) :
    first U V b c (U * R + V * S) = R ∧
    second U V b c (U * R + V * S) = S := by
  constructor
  · unfold first
    apply (div_eq_iff hd).mpr
    linear_combination -V * hline
  · unfold second
    apply (div_eq_iff hd).mpr
    linear_combination U * hline

#print axioms comm_left_intertwines
#print axioms comm_right_intertwines
#print axioms comm_square_scalar
#print axioms norm_decomposition
#print axioms forward_linear
#print axioms forward_parameter
#print axioms forward_norm
#print axioms inverse_parameter
#print axioms inverse_coordinates
end HumanCompression.ProjectiveTraceExtension
