import Mathlib.GroupTheory.PresentedGroup
import Mathlib.GroupTheory.SemidirectProduct
import Mathlib.Tactic

/-!
The uniform wreath quotient of the literal ten-relator rotational presentation.
The infinitude of the triangle Coxeter group is deliberately not postulated here.
-/

set_option linter.unusedSimpArgs false
set_option linter.unusedSectionVars false

namespace MathCompression.TriangleWreath

abbrev Ind := Fin 3
abbrev Outer := (Equiv.Perm Ind)ᵐᵒᵖ

variable {K : Type*} [Group K]

/-- Precomposition, with opposite permutations, realizes the row convention. -/
def rowAction : Outer →* MulAut (Ind → K) where
  toFun p :=
    { toFun := fun a i => a (MulOpposite.unop p i)
      invFun := fun a i => a ((MulOpposite.unop p).symm i)
      left_inv := by intro a; funext i; simp
      right_inv := by intro a; funext i; simp
      map_mul' := by intros; rfl }
  map_one' := by ext a i; rfl
  map_mul' p q := by ext a i; rfl

abbrev Wreath (K : Type*) [Group K] := (Ind → K) ⋊[rowAction] Outer

def cycle : Equiv.Perm Ind where
  toFun := ![2, 0, 1]
  invFun := ![1, 2, 0]
  left_inv := by decide +kernel
  right_inv := by decide +kernel

def X (d v : K) : Wreath K := ⟨![d,v,v], MulOpposite.op cycle⟩
def Y : Wreath K := ⟨1, MulOpposite.op cycle⟩
def Z (h q : K) : Wreath K := ⟨![h,q,h], 1⟩

@[simp] theorem row_mul (a b : Wreath K) (i : Ind) :
    (a * b).left i = a.left i * b.left (MulOpposite.unop a.right i) := rfl

@[simp] theorem row_inv (a : Wreath K) (i : Ind) :
    (a⁻¹).left i = (a.left ((MulOpposite.unop a.right)⁻¹ i))⁻¹ := rfl

section Relations
variable (d h q : K)
variable (dd : d*d=1) (hh : h*h=1) (qq : q*q=1)
variable (dh : (d*h)^2=1) (dq : (d*q)^3=1)

lemma invol_cancel {a : K} (ha : a*a=1) (b : K) : a*(a*b)=b := by
  rw [← mul_assoc, ha, one_mul]

lemma invol_inv {a : K} (ha : a*a=1) : a⁻¹=a := by
  exact (inv_eq_of_mul_eq_one_right ha)

include dd qq dq in
lemma dqd_eq_qdq : d*q*d=q*d*q := by
  have e := congrArg (fun a => d*a*q*d) dq
  simpa [pow_succ, mul_assoc, invol_cancel dd, invol_cancel qq, dd, qq] using e.symm

include dd dh in
lemma hdh_eq_d : h*d*h=d := by
  have e := congrArg (fun a => d*a) dh
  simpa [pow_succ, mul_assoc, invol_cancel dd, dd] using e

include dd qq dq in
lemma vdv_eq_q : (d*q*d)*d*(d*q*d)=q := by
  calc
    (d*q*d)*d*(d*q*d) = (d*q*d)*d*(q*d*q) :=
      congrArg (fun a => (d*q*d)*d*a) (dqd_eq_qdq d q dd qq dq)
    _ = q := by simp [mul_assoc, invol_cancel dd, invol_cancel qq, dd, qq]

include dd qq dq in
lemma vqv_eq_d : (d*q*d)*q*(d*q*d)=d := by
  calc
    (d*q*d)*q*(d*q*d) = (q*d*q)*q*(d*q*d) :=
      congrArg (fun a => a*q*(d*q*d)) (dqd_eq_qdq d q dd qq dq)
    _ = d := by simp [mul_assoc, invol_cancel dd, invol_cancel qq, dd, qq]

include dd qq dq in
lemma qvq_eq_d : q*(d*q*d)*q=d := by
  rw [dqd_eq_qdq d q dd qq dq]
  simp [mul_assoc, invol_cancel qq, qq]

end Relations

section WreathIdentities
variable (d h q v : K)
variable (dd : d*d=1) (hh : h*h=1) (qq : q*q=1) (vv : v*v=1)
variable (vdv : v*d*v=q) (vqv : v*q*v=d) (qvq : q*v*q=d)
variable (hdh : h*d*h=d) (dhd : d*h*d=h)

include vv vdv in
lemma X_cube : (X d v)^3 = (⟨![d,q,d],1⟩ : Wreath K) := by
  simp only [pow_succ, pow_zero, one_mul, mul_one]
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · change d*v*v=d
      rw [mul_assoc, vv, mul_one]
    · change v*d*v=q
      exact vdv
    · change v*v*d=d
      rw [vv, one_mul]
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

lemma triple_tail {a b c e : K} (h : a*b*c=e) (w : K) :
    a*(b*(c*w))=e*w := by simpa only [mul_assoc] using congrArg (fun u => u*w) h

variable (dvd : d*v*d=q) (dqd : d*q*d=v) (qdq : q*d*q=v)
include dd hh qq vv vdv vqv qvq hdh dhd dvd dqd qdq in
lemma nine_fixed :
    (X d v)^6 = 1 ∧
    (Y : Wreath K)^3 = 1 ∧
    (Z h q)^2 = 1 ∧
    (Z h q * X d v)^3 = 1 ∧
    (Z h q * Y)^6 = 1 ∧
    ((X d v)⁻¹ * Y)^2 = 1 ∧
    ((Y : Wreath K)⁻¹ * ((X d v)⁻¹)^2)^3 = 1 ∧
    (Z h q * (X d v)^3)^2 = 1 ∧
    (X d v)⁻¹ * Z h q * ((Y : Wreath K)⁻¹ * Z h q)^2 * Z h q * X d v * (Z h q * Y)^2 = 1 := by
  have hdht : h*(d*h)=d := by simpa only [mul_assoc] using hdh
  have dhdt : d*(h*d)=h := by simpa only [mul_assoc] using dhd
  have vdvt : v*(d*v)=q := by simpa only [mul_assoc] using vdv
  have vqvt : v*(q*v)=d := by simpa only [mul_assoc] using vqv
  have qvqt : q*(v*q)=d := by simpa only [mul_assoc] using qvq
  have dvdt : d*(v*d)=q := by simpa only [mul_assoc] using dvd
  have qdqt : q*(d*q)=v := by simpa only [mul_assoc] using qdq
  have dqdt : d*(q*d)=v := by simpa only [mul_assoc] using dqd
  refine ⟨?_,?_,?_,?_,?_,?_,?_,?_,?_⟩
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change (((((d * v) * v) * d) * v) * v) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((((v * d) * v) * v) * d) * v) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((((v * v) * d) * v) * v) * d) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change (((1 : K) * 1) * 1) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((1 : K) * 1) * 1) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((1 : K) * 1) * 1) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change (h * h) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (q * q) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (h * h) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change (((h * d) * (h * v)) * (q * v)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((q * v) * (h * d)) * (h * v)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((h * v) * (q * v)) * (h * d)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change ((((((h * 1) * (h * 1)) * (q * 1)) * (h * 1)) * (h * 1)) * (q * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((((q * 1) * (h * 1)) * (h * 1)) * (q * 1)) * (h * 1)) * (h * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((((h * 1) * (q * 1)) * (h * 1)) * (h * 1)) * (q * 1)) * (h * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change (((v)⁻¹ * 1) * ((v)⁻¹ * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((v)⁻¹ * 1) * ((v)⁻¹ * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change (((d)⁻¹ * 1) * ((d)⁻¹ * 1)) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change ((((1)⁻¹ * ((v)⁻¹ * (d)⁻¹)) * ((1)⁻¹ * ((v)⁻¹ * (d)⁻¹))) * ((1)⁻¹ * ((v)⁻¹ * (d)⁻¹))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((1)⁻¹ * ((d)⁻¹ * (v)⁻¹)) * ((1)⁻¹ * ((d)⁻¹ * (v)⁻¹))) * ((1)⁻¹ * ((d)⁻¹ * (v)⁻¹))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((1)⁻¹ * ((v)⁻¹ * (v)⁻¹)) * ((1)⁻¹ * ((v)⁻¹ * (v)⁻¹))) * ((1)⁻¹ * ((v)⁻¹ * (v)⁻¹))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change ((h * ((d * v) * v)) * (h * ((d * v) * v))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((q * ((v * d) * v)) * (q * ((v * d) * v))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((h * ((v * v) * d)) * (h * ((v * v) * d))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl
  · simp only [pow_succ, pow_zero, one_mul]
    apply SemidirectProduct.ext
    · funext i
      fin_cases i
      · change ((((((v)⁻¹ * q) * (((1)⁻¹ * h) * ((1)⁻¹ * h))) * h) * d) * ((h * 1) * (q * 1))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((((v)⁻¹ * h) * (((1)⁻¹ * h) * ((1)⁻¹ * q))) * q) * v) * ((h * 1) * (h * 1))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
      · change ((((((d)⁻¹ * h) * (((1)⁻¹ * q) * ((1)⁻¹ * h))) * h) * v) * ((q * 1) * (h * 1))) = 1
        simp only [one_mul, mul_one, inv_one, invol_inv dd, invol_inv hh,
          invol_inv qq, invol_inv vv, mul_assoc, invol_cancel dd,
          invol_cancel hh, invol_cancel qq, invol_cancel vv,
          dd, hh, qq, vv, qdqt, dqdt, hdht, dhdt, vdvt, vqvt, qvqt, dvdt,
          triple_tail hdh, triple_tail dhd, triple_tail vdv,
          triple_tail vqv, triple_tail qvq, triple_tail dvd,
          triple_tail dqd, triple_tail qdq]
    · apply MulOpposite.unop_injective
      apply Equiv.ext
      intro i
      fin_cases i <;> rfl

end WreathIdentities

section MoreIdentities
variable (d h q : K)

lemma parameter_word (hh : h*h=1) :
    Y * (Z h q * Y)^2 = (⟨![h*q,1,q*h],1⟩ : Wreath K) := by
  simp only [pow_succ, pow_zero, one_mul]
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · change 1 * ((h*1)*(q*1)) = h*q
      simp
    · change 1 * ((h*1)*(h*1)) = 1
      simpa using hh
    · change 1 * ((q*1)*(h*1)) = q*h
      simp
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

lemma conjugate_Z : (Y : Wreath K)⁻¹ * Z h q * Y = ⟨![q,h,h],1⟩ := by
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · change (1 : K)⁻¹ * q * 1 = q
      simp
    · change (1 : K)⁻¹ * h * 1 = h
      simp
    · change (1 : K)⁻¹ * h * 1 = h
      simp
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

lemma pure_pow (a : Ind → K) (n : ℕ) :
    (⟨a,1⟩ : Wreath K)^n = ⟨fun i => (a i)^n,1⟩ := by
  induction n with
  | zero => simp only [pow_zero]; rfl
  | succ n ih =>
    rw [pow_succ, ih]
    apply SemidirectProduct.ext
    · funext i
      change (a i)^n * a i = (a i)^(n+1)
      rw [pow_succ]
    · rfl

lemma parameter_relator (s : ℕ) (hh : h*h=1) (qq : q*q=1)
    (hs : (h*q)^s=1) : (Y * (Z h q * Y)^2)^s = 1 := by
  rw [parameter_word h q hh, pure_pow]
  have invpair : q*h=(h*q)⁻¹ := by
    simp [mul_inv_rev, invol_inv hh, invol_inv qq]
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · exact hs
    · exact one_pow s
    · change (q*h)^s=1
      rw [invpair, inv_pow, hs, inv_one]
  · rfl

end MoreIdentities

/-- All ten literal source words, in the printed source order. -/
def sourceWord {G : Type*} [Group G] (s : ℕ) (f : Ind → G) : Fin 10 → G :=
  ![(f 0)^6, (f 1)^3, (f 2)^2, (f 2*f 0)^3, (f 2*f 1)^6,
    ((f 0)⁻¹*f 1)^2, ((f 1)⁻¹*((f 0)⁻¹)^2)^3,
    (f 2*(f 0)^3)^2,
    (f 0)⁻¹*f 2*((f 1)⁻¹*f 2)^2*f 2*f 0*(f 2*f 1)^2,
    (f 1*(f 2*f 1)^2)^s]

/-- Exactly the six relations of the triangle Coxeter presentation. -/
def triangleWord {G : Type*} [Group G] (s : ℕ) (f : Ind → G) : Fin 6 → G :=
  ![(f 0)^2,(f 1)^2,(f 2)^2,(f 0*f 1)^2,(f 0*f 2)^3,(f 1*f 2)^s]

def sourceRels (s : ℕ) : Set (FreeGroup Ind) := Set.range (sourceWord s FreeGroup.of)
def triangleRels (s : ℕ) : Set (FreeGroup Ind) := Set.range (triangleWord s FreeGroup.of)
abbrev Source (s : ℕ) := PresentedGroup (sourceRels s)
abbrev Triangle (s : ℕ) := PresentedGroup (triangleRels s)

theorem map_sourceWord {G H : Type*} [Group G] [Group H]
    (φ : G →* H) (s : ℕ) (f : Ind → G) (j : Fin 10) :
    φ (sourceWord s f j) = sourceWord s (φ ∘ f) j := by
  fin_cases j <;> simp [sourceWord]

theorem map_triangleWord {G H : Type*} [Group G] [Group H]
    (φ : G →* H) (s : ℕ) (f : Ind → G) (j : Fin 6) :
    φ (triangleWord s f j) = triangleWord s (φ ∘ f) j := by
  fin_cases j <;> simp [triangleWord]

theorem ten_relators (s : ℕ) (d h q : K)
    (dd : d*d=1) (hh : h*h=1) (qq : q*q=1)
    (dh : (d*h)^2=1) (dq : (d*q)^3=1) (hq : (h*q)^s=1) :
    ∀ j, sourceWord s ![X d (d*q*d),Y,Z h q] j = 1 := by
  have vv : (d*q*d)*(d*q*d)=1 := by
    simp [mul_assoc, invol_cancel dd, invol_cancel qq, dd]
  have hdh := hdh_eq_d d h dd dh
  have dhd : d*h*d=h := by
    have e := congrArg (fun a => a*h) dh
    simpa [pow_succ, mul_assoc, invol_cancel hh, hh] using e
  have dvd : d*(d*q*d)*d=q := by
    simp [mul_assoc, invol_cancel dd, dd]
  have nine := nine_fixed d h q (d*q*d) dd hh qq vv
    (vdv_eq_q d q dd qq dq) (vqv_eq_d d q dd qq dq)
    (qvq_eq_d d q dd qq dq) hdh dhd dvd rfl (dqd_eq_qdq d q dd qq dq).symm
  rcases nine with ⟨r0,r1,r2,r3,r4,r5,r6,r7,r8⟩
  intro j
  fin_cases j <;> simp only [sourceWord, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val, Matrix.head_cons, Matrix.tail_cons, Nat.succ_eq_add_one]
  · exact r0
  · exact r1
  · exact r2
  · exact r3
  · exact r4
  · exact r5
  · exact r6
  · exact r7
  · exact r8
  · exact parameter_relator h q s hh qq hq

/-- The three marked generators of the exact triangle presentation. -/
def triangleGen (s : ℕ) : Ind → Triangle s := PresentedGroup.of

theorem triangle_relations (s : ℕ) (j : Fin 6) :
    triangleWord s (triangleGen s) j = 1 := by
  have mem : triangleWord s (FreeGroup.of : Ind → FreeGroup Ind) j ∈ triangleRels s :=
    ⟨j,rfl⟩
  have e := PresentedGroup.one_of_mem mem
  rw [map_triangleWord] at e
  exact e

theorem triangle_basic (s : ℕ) :
    triangleGen s 0 * triangleGen s 0 = 1 ∧
    triangleGen s 1 * triangleGen s 1 = 1 ∧
    triangleGen s 2 * triangleGen s 2 = 1 ∧
    (triangleGen s 0 * triangleGen s 1)^2 = 1 ∧
    (triangleGen s 0 * triangleGen s 2)^3 = 1 ∧
    (triangleGen s 1 * triangleGen s 2)^s = 1 := by
  refine ⟨?_,?_,?_,?_,?_,?_⟩
  · simpa [triangleWord, pow_two] using triangle_relations s 0
  · simpa [triangleWord, pow_two] using triangle_relations s 1
  · simpa [triangleWord, pow_two] using triangle_relations s 2
  · exact triangle_relations s 3
  · exact triangle_relations s 4
  · exact triangle_relations s 5

def markedRows (s : ℕ) : Ind → Wreath (Triangle s) :=
  ![X (triangleGen s 0) (triangleGen s 0 * triangleGen s 2 * triangleGen s 0),
    Y, Z (triangleGen s 1) (triangleGen s 2)]

theorem markedRows_valid (s : ℕ) (j : Fin 10) : sourceWord s (markedRows s) j = 1 := by
  obtain ⟨dd,hh,qq,dh,dq,hq⟩ := triangle_basic s
  exact ten_relators s _ _ _ dd hh qq dh dq hq j

/-- The homomorphism induced by all ten source relations. -/
def sourceMap (s : ℕ) : Source s →* Wreath (Triangle s) :=
  PresentedGroup.toGroup (f := markedRows s) (by
    intro r hr
    obtain ⟨j,rfl⟩ := hr
    rw [map_sourceWord]
    simpa only [Function.comp_def, FreeGroup.lift_apply_of] using markedRows_valid s j)

@[simp] theorem sourceMap_generator (s : ℕ) (i : Ind) :
    sourceMap s (PresentedGroup.of i) = markedRows s i :=
  PresentedGroup.toGroup.of _

/-- The subgroup of the source whose image has trivial outer permutation. -/
def pureKernel (s : ℕ) : Subgroup (Source s) :=
  ((SemidirectProduct.rightHom : Wreath (Triangle s) →* Outer).comp (sourceMap s)).ker

lemma pureKernel_mem (s : ℕ) (a : pureKernel s) : (sourceMap s a).right = 1 := a.property

/-- Coordinate projection on that subgroup is a homomorphism. -/
def coordinateMap (s : ℕ) : pureKernel s →* Triangle s where
  toFun a := (sourceMap s a).left 0
  map_one' := by
    change (sourceMap s 1).left 0 = 1
    rw [map_one]
    rfl
  map_mul' a b := by
    change (sourceMap s ((a : Source s)*(b : Source s))).left 0 = _
    rw [map_mul, row_mul, pureKernel_mem s a]
    rfl

lemma source_witness_x (s : ℕ) :
    sourceMap s ((PresentedGroup.of (0 : Ind))^3) =
      ⟨![triangleGen s 0,triangleGen s 2,triangleGen s 0],1⟩ := by
  rw [map_pow, sourceMap_generator]
  obtain ⟨dd,hh,qq,dh,dq,hq⟩ := triangle_basic s
  have vv : (triangleGen s 0 * triangleGen s 2 * triangleGen s 0) *
      (triangleGen s 0 * triangleGen s 2 * triangleGen s 0) = 1 := by
    simp [mul_assoc, invol_cancel dd, invol_cancel qq, dd]
  exact X_cube _ _ _ vv (vdv_eq_q _ _ dd qq dq)

lemma source_witness_z (s : ℕ) :
    sourceMap s (PresentedGroup.of (2 : Ind)) =
      ⟨![triangleGen s 1,triangleGen s 2,triangleGen s 1],1⟩ := by
  rw [sourceMap_generator]
  rfl

lemma source_witness_yzy (s : ℕ) :
    sourceMap s ((PresentedGroup.of (1 : Ind))⁻¹ * PresentedGroup.of (2 : Ind) *
      PresentedGroup.of (1 : Ind)) = ⟨![triangleGen s 2,triangleGen s 1,triangleGen s 1],1⟩ := by
  simp only [map_mul, map_inv, sourceMap_generator]
  exact conjugate_Z _ _

/-- Each of the three triangle generators has an explicit preimage. -/
theorem coordinate_generator_preimage (s : ℕ) (i : Ind) :
    ∃ a : pureKernel s, coordinateMap s a = triangleGen s i := by
  fin_cases i
  · refine ⟨⟨(PresentedGroup.of (0 : Ind))^3, ?_⟩, ?_⟩
    · change (sourceMap s ((PresentedGroup.of (0 : Ind))^3)).right=1
      rw [source_witness_x]
    · change (sourceMap s ((PresentedGroup.of (0 : Ind))^3)).left 0=triangleGen s 0
      rw [source_witness_x]
      rfl
  · refine ⟨⟨PresentedGroup.of (2 : Ind), ?_⟩, ?_⟩
    · change (sourceMap s (PresentedGroup.of (2 : Ind))).right=1
      rw [source_witness_z]
    · change (sourceMap s (PresentedGroup.of (2 : Ind))).left 0=triangleGen s 1
      rw [source_witness_z]
      rfl
  · refine ⟨⟨(PresentedGroup.of (1 : Ind))⁻¹ * PresentedGroup.of (2 : Ind) *
      PresentedGroup.of (1 : Ind), ?_⟩, ?_⟩
    · change (sourceMap s ((PresentedGroup.of (1 : Ind))⁻¹ * PresentedGroup.of (2 : Ind) *
        PresentedGroup.of (1 : Ind))).right=1
      rw [source_witness_yzy]
    · change (sourceMap s ((PresentedGroup.of (1 : Ind))⁻¹ * PresentedGroup.of (2 : Ind) *
        PresentedGroup.of (1 : Ind))).left 0=triangleGen s 2
      rw [source_witness_yzy]
      rfl

/-- The explicit subgroup of the source surjects onto the exact triangle group. -/
theorem coordinateMap_surjective (s : ℕ) : Function.Surjective (coordinateMap s) := by
  intro a
  exact PresentedGroup.generated_by (triangleRels s) (coordinateMap s).range
    (coordinate_generator_preimage s) a

/-- Transfer only: infinitude of the triangle group is an explicit hypothesis. -/
theorem source_infinite_of_triangle (s : ℕ) [Infinite (Triangle s)] : Infinite (Source s) := by
  haveI : Infinite (pureKernel s) := Infinite.of_surjective _ (coordinateMap_surjective s)
  exact Infinite.of_injective (fun a : pureKernel s => (a : Source s)) Subtype.val_injective

#print axioms ten_relators
#print axioms sourceMap
#print axioms coordinateMap_surjective
#print axioms source_infinite_of_triangle

end MathCompression.TriangleWreath


