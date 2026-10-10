import TriangleWreathInvolutory
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-! Explicit real reflection representation and infinitude of the exact triangle group. -/

noncomputable section
set_option linter.unusedSimpArgs false

namespace MathCompression.TriangleReflection

open MathCompression.TriangleWreath

abbrev V := Fin 3 → ℝ

def D : Equiv.Perm V where
  toFun v := ![-v 0 + v 2,v 1,v 2]
  invFun v := ![-v 0 + v 2,v 1,v 2]
  left_inv := by intro v; funext i; fin_cases i <;> simp
  right_inv := by intro v; funext i; fin_cases i <;> simp

def H (t : ℝ) : Equiv.Perm V where
  toFun v := ![v 0,-v 1+t*v 2,v 2]
  invFun v := ![v 0,-v 1+t*v 2,v 2]
  left_inv := by intro v; funext i; fin_cases i <;> simp
  right_inv := by intro v; funext i; fin_cases i <;> simp

def Q (t : ℝ) : Equiv.Perm V where
  toFun v := ![v 0,v 1,v 0+t*v 1-v 2]
  invFun v := ![v 0,v 1,v 0+t*v 1-v 2]
  left_inv := by intro v; funext i; fin_cases i <;> simp
  right_inv := by intro v; funext i; fin_cases i <;> simp

theorem fixed_relations (t : ℝ) :
    D^2=1 ∧ (H t)^2=1 ∧ (Q t)^2=1 ∧ (D*H t)^2=1 ∧ (D*Q t)^3=1 := by
  refine ⟨?_,?_,?_,?_,?_⟩ <;>
    ext v i <;> fin_cases i <;>
    simp [pow_succ, D, H, Q, Equiv.Perm.mul_apply] <;> ring

def rotate (a : ℝ) (v : V) : V :=
  ![v 0,Real.cos a*v 1-Real.sin a*v 2,Real.sin a*v 1+Real.cos a*v 2]

theorem rotate_add (a b : ℝ) (v : V) :
    rotate a (rotate b v)=rotate (a+b) v := by
  funext i
  fin_cases i <;> simp [rotate,Real.sin_add,Real.cos_add] <;> ring

theorem rotate_zero (v : V) : rotate 0 v=v := by
  funext i
  fin_cases i <;> simp [rotate]

theorem rotate_two_pi (v : V) : rotate (2*Real.pi) v=v := by
  funext i
  fin_cases i <;> simp [rotate]

def changeCoordinates (a : ℝ) (v : V) : V :=
  let t := 2*Real.cos a
  ![(4-t^2)*v 0,t*v 0+Real.cos a*v 1-Real.sin a*v 2,2*v 0+v 1]

theorem HQ_changeCoordinates (a : ℝ) (v : V) :
    (H (2*Real.cos a)*Q (2*Real.cos a)) (changeCoordinates a v) =
      changeCoordinates a (rotate (2*a) v) := by
  have trig := Real.sin_sq_add_cos_sq a
  funext i
  fin_cases i <;>
    simp [Equiv.Perm.mul_apply,H,Q,changeCoordinates,rotate,Real.sin_two_mul,Real.cos_two_mul] <;>
    nlinarith [congrArg (fun x : ℝ => x * v 0) trig,
      congrArg (fun x : ℝ => x * Real.cos a * v 1) trig,
      congrArg (fun x : ℝ => x * Real.sin a * v 2) trig]

theorem changeCoordinates_surjective (a : ℝ)
    (hc : 4-(2*Real.cos a)^2 ≠ 0) (hs : Real.sin a ≠ 0) :
    Function.Surjective (changeCoordinates a) := by
  intro w
  let u := w 0/(4-(2*Real.cos a)^2)
  let b := w 2-2*u
  let c := (2*Real.cos a*u+Real.cos a*b-w 1)/Real.sin a
  refine ⟨![u,b,c],?_⟩
  funext i
  fin_cases i
  · change (4-(2*Real.cos a)^2)*(w 0/(4-(2*Real.cos a)^2))=w 0
    rw [mul_div_cancel₀ _ hc]
  · change 2*Real.cos a*u+Real.cos a*b-Real.sin a*c=w 1
    dsimp [c]
    field_simp [hs]
    ring
  · change 2*u+b=w 2
    dsimp [b]
    ring

theorem HQ_power_changeCoordinates (a : ℝ) (n : ℕ) (v : V) :
    ((H (2*Real.cos a)*Q (2*Real.cos a))^n) (changeCoordinates a v) =
      changeCoordinates a (rotate ((n:ℝ)*(2*a)) v) := by
  induction n with
  | zero => simp [rotate_zero]
  | succ n ih =>
    rw [pow_succ', Equiv.Perm.mul_apply, ih, HQ_changeCoordinates, rotate_add]
    congr 2
    push_cast
    ring

theorem HQ_period (a : ℝ) (n : ℕ)
    (hc : 4-(2*Real.cos a)^2 ≠ 0) (hs : Real.sin a ≠ 0)
    (hn : (n:ℝ)*(2*a)=2*Real.pi) :
    (H (2*Real.cos a)*Q (2*Real.cos a))^n=1 := by
  apply Equiv.ext
  intro w
  obtain ⟨v,rfl⟩ := changeCoordinates_surjective a hc hs w
  rw [HQ_power_changeCoordinates,hn,rotate_two_pi]
  rfl

def angle (s : ℕ) : ℝ := Real.pi/(s:ℝ)
def parameter (s : ℕ) : ℝ := 2*Real.cos (angle s)

theorem angle_bounds (s : ℕ) (hs : 6≤s) : 0<angle s ∧ angle s<Real.pi := by
  have hs6 : (6:ℝ)≤s := by exact_mod_cast hs
  have hs0 : (0:ℝ)<s := by linarith
  constructor
  · exact div_pos Real.pi_pos hs0
  · apply (div_lt_iff₀ hs0).2
    nlinarith [Real.pi_pos]

theorem parameter_relation (s : ℕ) (hs : 6≤s) : (H (parameter s)*Q (parameter s))^s=1 := by
  obtain ⟨ha0,hapi⟩ := angle_bounds s hs
  have hsin : 0<Real.sin (angle s) := Real.sin_pos_of_pos_of_lt_pi ha0 hapi
  have trig := Real.sin_sq_add_cos_sq (angle s)
  have hc : 4-(2*Real.cos (angle s))^2≠0 := by nlinarith [sq_pos_of_pos hsin]
  apply HQ_period (angle s) s hc (ne_of_gt hsin)
  have hs0 : (s:ℝ)≠0 := by exact_mod_cast (by omega : s≠0)
  dsimp [angle]
  field_simp

/-- Ordinary permutation multiplication composes column actions: C=D∘H∘Q. -/
def C (t : ℝ) : Equiv.Perm V := D*H t*Q t

theorem C_apply (t : ℝ) (v : V) : C t v =
    ![t*v 1-v 2,t*v 0+(t^2-1)*v 1-t*v 2,v 0+t*v 1-v 2] := by
  funext i
  fin_cases i <;> simp [C,D,H,Q,Equiv.Perm.mul_apply] <;> ring

theorem eigen_orbit (t r : ℝ) (hr : r^2-(t^2-1)*r+1=0) (n : ℕ) :
    ((C t)^n) ![r,t*r,r+1] = ![r^n*r,r^n*(t*r),r^n*(r+1)] := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ',Equiv.Perm.mul_apply,ih,C_apply]
    funext i
    fin_cases i <;> simp [Matrix.cons_val_zero,Matrix.cons_val_one,
      Matrix.cons_val,Matrix.head_cons,Matrix.tail_cons,pow_succ]
    · linear_combination -(r^n)*hr
    · linear_combination -(t*r^n)*hr
    · linear_combination -(r^n)*hr

theorem C_square_apply (t : ℝ) (ht : t^2=3) (v : V) :
    ((C t)^2) v =
      ![2*v 0+t*v 1-2*v 2,t*v 0+4*v 1-2*t*v 2,2*v 0+2*t*v 1-3*v 2] := by
  rw [pow_two,Equiv.Perm.mul_apply,C_apply,C_apply]
  funext i
  fin_cases i <;> simp [Matrix.cons_val_zero,Matrix.cons_val_one,
    Matrix.cons_val,Matrix.head_cons,Matrix.tail_cons]
  · linear_combination (v 0+t*v 1-v 2)*ht
  · linear_combination (t*v 0+(t^2+1)*v 1-t*v 2)*ht
  · linear_combination (v 0+t*v 1-v 2)*ht

theorem unipotent_orbit (t : ℝ) (ht : t^2=3) (n : ℕ) :
    (((C t)^2)^n) ![1,0,0] = ![(n:ℝ)+1,(n:ℝ)*t,2*(n:ℝ)] := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ',Equiv.Perm.mul_apply,ih,C_square_apply t ht]
    funext i
    fin_cases i <;> simp [Matrix.cons_val_zero,Matrix.cons_val_one,
      Matrix.cons_val,Matrix.head_cons,Matrix.tail_cons,Nat.cast_add,Nat.cast_one]
    · nlinarith [congrArg (fun a : ℝ => a*(n:ℝ)) ht]
    · ring
    · nlinarith [congrArg (fun a : ℝ => a*(n:ℝ)) ht]

theorem expanding_root (t : ℝ) (ht : 3<t^2) :
    ∃ r : ℝ, 1<r ∧ r^2-(t^2-1)*r+1=0 := by
  let a := t^2-1
  have ha : 2<a := by dsimp [a]; linarith
  have hdisc : 0≤a^2-4 := by nlinarith
  have hsquare := Real.sq_sqrt hdisc
  have hnonneg := Real.sqrt_nonneg (a^2-4)
  refine ⟨(a+Real.sqrt (a^2-4))/2,?_,?_⟩
  · linarith
  · change ((a+Real.sqrt (a^2-4))/2)^2-a*((a+Real.sqrt (a^2-4))/2)+1=0
    nlinarith

theorem parameter_six : (parameter 6)^2=3 := by
  have hs := Real.sq_sqrt (by norm_num : (0:ℝ)≤3)
  simp [parameter,angle,Real.cos_pi_div_six]
  nlinarith

theorem parameter_expanding (s : ℕ) (hs : 6<s) : 3<(parameter s)^2 := by
  have hs6 : (6:ℝ)<s := by exact_mod_cast hs
  have hs0 : (0:ℝ)<s := by linarith
  have hangle : angle s<Real.pi/6 := by
    apply (div_lt_div_iff₀ hs0 (by norm_num : (0:ℝ)<6)).2
    nlinarith [Real.pi_pos]
  have ha0 : 0≤angle s := (angle_bounds s (by omega)).1.le
  have hpibound : Real.pi/6≤Real.pi := by linarith [Real.pi_pos]
  have hc := Real.cos_lt_cos_of_nonneg_of_le_pi ha0 hpibound hangle
  rw [Real.cos_pi_div_six] at hc
  have hsq := Real.sq_sqrt (by norm_num : (0:ℝ)≤3)
  have hpos := Real.sqrt_nonneg (3:ℝ)
  dsimp [parameter]
  nlinarith

def reflectionGenerators (s : ℕ) : Ind → Equiv.Perm V :=
  ![D,H (parameter s),Q (parameter s)]

theorem reflection_valid (s : ℕ) (hs : 6≤s) (j : Fin 6) :
    triangleWord s (reflectionGenerators s) j=1 := by
  obtain ⟨dd,hh,qq,dh,dq⟩ := fixed_relations (parameter s)
  fin_cases j
  · exact dd
  · exact hh
  · exact qq
  · exact dh
  · exact dq
  · exact parameter_relation s hs

/-- An actual representation of the six-relator triangle presentation. -/
def representation (s : ℕ) (hs : 6≤s) : Triangle s →* Equiv.Perm V :=
  PresentedGroup.toGroup (f := reflectionGenerators s) (by
    intro r hr
    obtain ⟨j,rfl⟩ := hr
    rw [map_triangleWord]
    simpa only [Function.comp_def,FreeGroup.lift_apply_of] using reflection_valid s hs j)

@[simp] theorem representation_generator (s : ℕ) (hs : 6≤s) (i : Ind) :
    representation s hs (triangleGen s i) = reflectionGenerators s i :=
  PresentedGroup.toGroup.of _

def coxeterElement (s : ℕ) : Triangle s :=
  triangleGen s 0*triangleGen s 1*triangleGen s 2

@[simp] theorem representation_coxeter (s : ℕ) (hs : 6≤s) :
    representation s hs (coxeterElement s) = C (parameter s) := by
  simp [coxeterElement,reflectionGenerators,C]

/-- Distinct values on one orbit force distinct powers in the source group. -/
theorem infinite_of_orbit {G : Type*} [Group G] (φ : G →* Equiv.Perm V)
    (g : G) (v : V) (f : ℕ → ℝ)
    (orbit : ∀ n, (φ (g^n) v) 0=f n) (hinj : Function.Injective f) : Infinite G := by
  apply Infinite.of_injective (fun n : ℕ => g^n)
  intro m n h
  apply hinj
  have e := congrArg (fun a : G => (φ a v) 0) h
  simpa only [orbit] using e

/-- The exact triangle Coxeter presentation is infinite for every s≥6. -/
theorem triangle_infinite (s : ℕ) (hs : 6≤s) : Infinite (Triangle s) := by
  by_cases h6 : s=6
  · subst s
    apply infinite_of_orbit (representation 6 hs) ((coxeterElement 6)^2)
      ![1,0,0] (fun n => (n:ℝ)+1)
    · intro n
      simp only [map_pow,representation_coxeter]
      rw [unipotent_orbit (parameter 6) parameter_six]
      rfl
    · intro m n h
      exact_mod_cast (add_right_cancel h)
  · have hs' : 6<s := by omega
    obtain ⟨r,hr,hpoly⟩ := expanding_root (parameter s) (parameter_expanding s hs')
    apply infinite_of_orbit (representation s hs) (coxeterElement s)
      ![r,parameter s*r,r+1] (fun n => r^n*r)
    · intro n
      simp only [map_pow,representation_coxeter]
      rw [eigen_orbit (parameter s) r hpoly]
      rfl
    · intro m n h
      apply (pow_right_strictMono₀ hr).injective
      exact mul_right_cancel₀ (by linarith : r≠0) h

/-- The literal ten-relator rotational source is infinite for all s≥6. -/
theorem rotational_source_infinite (s : ℕ) (hs : 6≤s) : Infinite (Source s) := by
  haveI := triangle_infinite s hs
  exact source_infinite_of_triangle s

/-- The exact four-involution universal group is infinite for all s≥6. -/
theorem universal_source_infinite (s : ℕ) (hs : 6≤s) : Infinite (Universal s) := by
  haveI := triangle_infinite s hs
  exact universal_infinite_of_triangle s

#print axioms parameter_relation
#print axioms triangle_infinite
#print axioms rotational_source_infinite
#print axioms universal_source_infinite

end MathCompression.TriangleReflection


