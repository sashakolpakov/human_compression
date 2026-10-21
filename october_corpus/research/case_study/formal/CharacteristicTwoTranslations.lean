import Mathlib.LinearAlgebra.QuadraticForm.Basic
import Mathlib.Algebra.CharP.Two
import Mathlib.Tactic

/-!
Ambient characteristic-two quadratic-space identities. The vector space
may be degenerate; no calculation is restricted to a three-dimensional span.
All definitions use the actual quadratic form; no target relation or
translation-group assertion is supplied as a premise.
-/

namespace MathCompression.CharacteristicTwoTranslations

variable {F V : Type*} [Field F] [CharP F 2] [AddCommGroup V] [Module F V]

open QuadraticMap

def translation (Q : QuadraticForm F V) (z u x : V) : V :=
  x + polar Q x z • u + (polar Q x u + Q u * polar Q x z) • z

def symmetry (Q : QuadraticForm F V) (u x : V) : V :=
  x + polar Q x u • u

theorem polar_self_zero (Q : QuadraticForm F V) (x : V) : polar Q x x = 0 := by
  rw [polar_self, CharTwo.two_nsmul]

include F in
theorem vector_add_self (x : V) : x + x = 0 := by
  calc x + x = (2 : F) • x := (two_smul F x).symm
       _ = 0 := by rw [CharTwo.two_eq_zero, zero_smul]

omit [CharP F 2] in
theorem quadratic_add (Q : QuadraticForm F V) (u v : V) :
    Q (u + v) = Q u + Q v + polar Q u v := by
  unfold polar
  ring

/-- The whole-ambient-space composition law, proved from the actual
quadratic form and its polar form. It remains valid for degenerate forms. -/
theorem translation_comp (Q : QuadraticForm F V) (z u v x : V)
    (huz : polar Q u z = 0) (hvz : polar Q v z = 0) :
    translation Q z u (translation Q z v x) = translation Q z (u + v) x := by
  have hzu : polar Q z u = 0 := by rw [polar_comm]; exact huz
  have hvu : polar Q v u = polar Q u v := polar_comm Q v u
  simp only [translation, polar_add_left, polar_smul_left, polar_add_right,
    smul_eq_mul, hvz, hzu, polar_self_zero, mul_zero, add_zero,
    quadratic_add, hvu]
  module

omit [CharP F 2] in
theorem translation_zero (Q : QuadraticForm F V) (z x : V) :
    translation Q z 0 x = x := by
  simp [translation]

/-- Each translation squares to the identity on the full ambient space. -/
theorem translation_involutive (Q : QuadraticForm F V) (z u : V)
    (huz : polar Q u z = 0) : Function.Involutive (translation Q z u) := by
  intro x
  rw [translation_comp Q z u u x huz huz, vector_add_self (F := F), translation_zero]

/-- The pair of actual ambient symmetries gives the stated translation.
The equation is algebraic; singularity of z additionally ensures that u+z
has the same quadratic value, as used in the source construction. -/
theorem symmetry_pair (Q : QuadraticForm F V) (z u x : V)
    (hu : Q u = 1) (huz : polar Q u z = 0) :
    symmetry Q u (symmetry Q (u + z) x) = translation Q z u x := by
  have hzu : polar Q z u = 0 := by rw [polar_comm]; exact huz
  simp only [symmetry, translation, polar_add_left, polar_add_right, polar_smul_left,
    smul_eq_mul, hzu, polar_self_zero, add_zero, mul_zero, hu, one_mul]
  match_scalars <;> ring_nf
  simp [CharTwo.two_eq_zero]

#print axioms polar_self_zero
#print axioms vector_add_self
#print axioms quadratic_add
#print axioms translation_comp
#print axioms translation_zero
#print axioms translation_involutive
#print axioms symmetry_pair


/-- The actual symmetry is linear, without a nondegeneracy assumption. -/
def symmetryLinear (Q : QuadraticForm F V) (u : V) : V →ₗ[F] V where
  toFun := symmetry Q u
  map_add' x y := by simp only [symmetry, polar_add_left]; module
  map_smul' a x := by
    change symmetry Q u (a • x) = a • symmetry Q u x
    simp only [symmetry, polar_smul_left, smul_eq_mul]
    module

/-- A symmetry is an involution as a map of the whole ambient space. -/
theorem symmetry_involutive (Q : QuadraticForm F V) (u : V) :
    Function.Involutive (symmetry Q u) := by
  intro x
  simp only [symmetry, polar_add_left, polar_smul_left, smul_eq_mul,
    polar_self_zero, mul_zero, add_zero]
  match_scalars <;> ring_nf
  simp [CharTwo.two_eq_zero]

def symmetryEquiv (Q : QuadraticForm F V) (u : V) : V ≃ₗ[F] V :=
  LinearEquiv.ofInvolutive (symmetryLinear Q u) (symmetry_involutive Q u)

/-- A unit-value symmetry preserves the actual quadratic form. -/
theorem symmetry_preserves (Q : QuadraticForm F V) (u : V) (hu : Q u = 1) (x : V) :
    Q (symmetry Q u x) = Q x := by
  simp only [symmetry, quadratic_add, QuadraticMap.map_smul, polar_smul_right,
    smul_eq_mul, hu, mul_one]
  ring_nf
  simp [CharTwo.two_eq_zero]

omit [CharP F 2] in
theorem polar_preserves (Q : QuadraticForm F V) (g : V ≃ₗ[F] V)
    (hQ : ∀ x, Q (g x) = Q x) (x y : V) :
    polar Q (g x) (g y) = polar Q x y := by
  unfold polar
  rw [← map_add, hQ, hQ, hQ]

/-- The displayed translation is linear in its ambient argument. -/
def translationLinear (Q : QuadraticForm F V) (z u : V) : V →ₗ[F] V where
  toFun := translation Q z u
  map_add' x y := by simp only [translation, polar_add_left]; module
  map_smul' a x := by
    change translation Q z u (a • x) = a • translation Q z u x
    simp only [translation, polar_smul_left, smul_eq_mul]
    module

def translationEquiv (Q : QuadraticForm F V) (z u : V)
    (huz : polar Q u z = 0) : V ≃ₗ[F] V :=
  LinearEquiv.ofInvolutive (translationLinear Q z u) (translation_involutive Q z u huz)

omit [CharP F 2] in
/-- Covariance under an actual linear isometry fixing z, proved directly
from its linearity and preservation of the polar and quadratic forms. -/
theorem translation_covariant (Q : QuadraticForm F V) (g : V ≃ₗ[F] V)
    (hQ : ∀ x, Q (g x) = Q x) (z : V) (hz : g z = z) (u x : V) :
    g (translation Q z u x) = translation Q z (g u) (g x) := by
  have hpol := polar_preserves Q g hQ
  have hxz : polar Q (g x) z = polar Q x z := by simpa only [hz] using hpol x z
  simp only [translation, map_add, map_smul, hxz, hpol, hQ, hz]

/-- Coordinate-free ambient conjugation, with the transformed parameter
again perpendicular to z. -/
theorem translation_conjugate (Q : QuadraticForm F V) (g : V ≃ₗ[F] V)
    (hQ : ∀ x, Q (g x) = Q x) (z : V) (hz : g z = z) (u : V)
    (huz : polar Q u z = 0) :
    ∃ hgu : polar Q (g u) z = 0,
      g * translationEquiv Q z u huz * g⁻¹ = translationEquiv Q z (g u) hgu := by
  have hgu : polar Q (g u) z = 0 := by
    rw [← hz, polar_preserves Q g hQ, huz]
  refine ⟨hgu, ?_⟩
  ext x
  change g (translation Q z u (g.symm x)) = translation Q z (g u) x
  rw [translation_covariant Q g hQ z hz]
  simp

/-- The ambient symmetry-pair identity as an equality of actual group
elements, not only their restrictions to a selected subspace. -/
theorem symmetry_pair_equiv (Q : QuadraticForm F V) (z u : V)
    (hu : Q u = 1) (huz : polar Q u z = 0) :
    symmetryEquiv Q u * symmetryEquiv Q (u + z) = translationEquiv Q z u huz := by
  ext x
  exact symmetry_pair Q z u x hu huz

omit [CharP F 2] in
theorem singular_shift (Q : QuadraticForm F V) (z u : V)
    (hz : Q z = 0) (hu : Q u = 1) (huz : polar Q u z = 0) : Q (u + z) = 1 := by
  rw [quadratic_add, hu, hz, huz]
  simp

#print axioms symmetry_involutive
#print axioms symmetry_preserves
#print axioms polar_preserves
#print axioms translation_covariant
#print axioms translation_conjugate
#print axioms symmetry_pair_equiv
#print axioms singular_shift


/-- The subgroup of actual ambient translations, with closure proved from
translation_comp rather than postulated as a model of the required relator. -/
def translationGroup (Q : QuadraticForm F V) (z : V) : Subgroup (V ≃ₗ[F] V) where
  carrier := {g | ∃ u, ∃ huz : polar Q u z = 0, g = translationEquiv Q z u huz}
  one_mem' := by
    refine ⟨0, by simp, ?_⟩
    ext x
    change x = translation Q z 0 x
    exact (translation_zero Q z x).symm
  mul_mem' := by
    rintro g h ⟨u, huz, rfl⟩ ⟨v, hvz, rfl⟩
    refine ⟨u + v, by rw [polar_add_left, huz, hvz, add_zero], ?_⟩
    ext x
    exact translation_comp Q z u v x huz hvz
  inv_mem' := by
    rintro g ⟨u, huz, rfl⟩
    refine ⟨u, huz, ?_⟩
    ext x
    rfl

/-- Every element of the constructed translation subgroup has square one. -/
theorem translationGroup_square (Q : QuadraticForm F V) (z : V)
    (g : V ≃ₗ[F] V) (hg : g ∈ translationGroup Q z) : g ^ 2 = 1 := by
  obtain ⟨u, huz, rfl⟩ := hg
  ext x
  change translation Q z u (translation Q z u x) = x
  exact translation_involutive Q z u huz x

/-- Every actual linear isometry fixing z normalizes the constructed
translations in the indicated conjugation direction. -/
theorem translationGroup_conjugate (Q : QuadraticForm F V) (z : V)
    (g : V ≃ₗ[F] V) (hQ : ∀ x, Q (g x) = Q x) (hz : g z = z)
    (t : V ≃ₗ[F] V) (ht : t ∈ translationGroup Q z) :
    g * t * g⁻¹ ∈ translationGroup Q z := by
  obtain ⟨u, huz, rfl⟩ := ht
  obtain ⟨hgu, he⟩ := translation_conjugate Q g hQ z hz u huz
  exact ⟨g u, hgu, he⟩

/-- All integer powers, with the positive and negative steps proved inside
the subgroup. Normality in the whole ambient group is unnecessary. -/
theorem integer_power_product_mem {G : Type*} [Group G]
    (N : Subgroup G) (a c : G) (hac : a * c ∈ N)
    (hforward : ∀ x ∈ N, a * x * a⁻¹ ∈ N)
    (hbackward : ∀ x ∈ N, a⁻¹ * x * a ∈ N) (k : ℤ) :
    c ^ k * a ^ k ∈ N := by
  induction k using Int.induction_on with
  | zero => simp
  | succ n ih =>
    have hm := N.mul_mem (hbackward (a * c) hac)
      (hbackward (c ^ (n : ℤ) * a ^ (n : ℤ)) ih)
    have he : c ^ ((n : ℤ) + 1) * a ^ ((n : ℤ) + 1) =
        (a⁻¹ * (a * c) * a) * (a⁻¹ * (c ^ (n : ℤ) * a ^ (n : ℤ)) * a) := by
      simp only [zpow_add, zpow_one]
      group
    rw [he]
    exact hm
  | pred n ih =>
    have hm := N.mul_mem (N.inv_mem hac)
      (hforward (c ^ (-(n : ℤ)) * a ^ (-(n : ℤ))) ih)
    have he : c ^ (-(n : ℤ) - 1) * a ^ (-(n : ℤ) - 1) =
        (a * c)⁻¹ * (a * (c ^ (-(n : ℤ)) * a ^ (-(n : ℤ))) * a⁻¹) := by
      simp only [zpow_sub, zpow_one]
      group
    rw [he]
    exact hm

/-- The exponent-two conclusion for every integer, derived through actual
subgroup membership rather than supplied as an input relation. -/
theorem integer_power_product_square {G : Type*} [Group G]
    (N : Subgroup G) (a c : G) (hac : a * c ∈ N)
    (hforward : ∀ x ∈ N, a * x * a⁻¹ ∈ N)
    (hbackward : ∀ x ∈ N, a⁻¹ * x * a ∈ N)
    (hsquare : ∀ x ∈ N, x ^ 2 = 1) (k : ℤ) :
    (c ^ k * a ^ k) ^ 2 = 1 :=
  hsquare _ (integer_power_product_mem N a c hac hforward hbackward k)

#print axioms translationGroup_square
#print axioms translationGroup_conjugate
#print axioms integer_power_product_mem
#print axioms integer_power_product_square

/-- Equal adjacent polar values and orthogonal end vectors make e+h
singular and perpendicular to all three vectors. -/
theorem triple_singular_radical (Q : QuadraticForm F V) (e f h : V)
    (he : Q e = 1) (hh : Q h = 1) (heh : polar Q e h = 0)
    (hequal : polar Q e f = polar Q f h) :
    Q (e + h) = 0 ∧ polar Q e (e + h) = 0 ∧
      polar Q f (e + h) = 0 ∧ polar Q h (e + h) = 0 := by
  have hfe : polar Q f e = polar Q f h := by rw [polar_comm Q f e, hequal]
  have hhe : polar Q h e = 0 := by rw [polar_comm]; exact heh
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [quadratic_add, he, hh, heh, add_zero, CharTwo.add_self_eq_zero]
  · rw [polar_add_right, polar_self_zero, heh, add_zero]
  · rw [polar_add_right, hfe, CharTwo.add_self_eq_zero]
  · rw [polar_add_right, hhe, polar_self_zero, add_zero]

/-- The exact all-integer relator for three actual ambient symmetries.
There is no nondegeneracy or dimension hypothesis: in particular the
three-vector span may have a radical. All subgroup, conjugation, and
exponent-two facts are derived from the displayed quadratic-form data. -/
theorem equal_label_integer_relation (Q : QuadraticForm F V) (e f h : V)
    (he : Q e = 1) (hf : Q f = 1) (hh : Q h = 1)
    (heh : polar Q e h = 0) (hequal : polar Q e f = polar Q f h) (k : ℤ) :
    ((symmetryEquiv Q f * symmetryEquiv Q h) ^ k *
      (symmetryEquiv Q e * symmetryEquiv Q f) ^ k) ^ 2 = 1 := by
  let z := e + h
  let a := symmetryEquiv Q e * symmetryEquiv Q f
  let c := symmetryEquiv Q f * symmetryEquiv Q h
  let N := translationGroup Q z
  obtain ⟨_, hez, hfz, _⟩ := triple_singular_radical Q e f h he hh heh hequal
  have hez' : polar Q e z = 0 := hez
  have hfz' : polar Q f z = 0 := hfz
  have hefix : symmetry Q e z = z := by
    simp only [symmetry, polar_comm Q z e, hez', zero_smul, add_zero]
  have hffix : symmetry Q f z = z := by
    simp only [symmetry, polar_comm Q z f, hfz', zero_smul, add_zero]
  have haQ : ∀ x, Q (a x) = Q x := by
    intro x
    change Q (symmetry Q e (symmetry Q f x)) = Q x
    rw [symmetry_preserves Q e he, symmetry_preserves Q f hf]
  have haz : a z = z := by
    change symmetry Q e (symmetry Q f z) = z
    rw [hffix, hefix]
  have haQinv : ∀ x, Q (a⁻¹ x) = Q x := by
    intro x
    change Q (a.symm x) = Q x
    have ht := haQ (a.symm x)
    simpa only [a.apply_symm_apply] using ht.symm
  have hazinv : a⁻¹ z = z := by
    change a.symm z = z
    have ht := congrArg (fun x => a.symm x) haz
    simpa only [a.symm_apply_apply] using ht.symm
  have hezh : e + z = h := by
    dsimp [z]
    rw [← add_assoc, vector_add_self (F := F), zero_add]
  have hac : a * c ∈ N := by
    have hff : symmetryEquiv Q f * symmetryEquiv Q f = 1 := by
      ext x
      exact symmetry_involutive Q f x
    have heq : a * c = symmetryEquiv Q e * symmetryEquiv Q h := by
      dsimp [a, c]
      calc
        (symmetryEquiv Q e * symmetryEquiv Q f) *
            (symmetryEquiv Q f * symmetryEquiv Q h) =
            symmetryEquiv Q e * (symmetryEquiv Q f * symmetryEquiv Q f) *
              symmetryEquiv Q h := by group
        _ = _ := by rw [hff, mul_one]
    refine ⟨e, hez', ?_⟩
    rw [heq]
    simpa only [hezh] using symmetry_pair_equiv Q z e he hez'
  have hforward : ∀ x ∈ N, a * x * a⁻¹ ∈ N :=
    translationGroup_conjugate Q z a haQ haz
  have hbackward : ∀ x ∈ N, a⁻¹ * x * a ∈ N := by
    intro x hx
    simpa only [inv_inv] using translationGroup_conjugate Q z a⁻¹ haQinv hazinv x hx
  exact integer_power_product_square N a c hac hforward hbackward
    (translationGroup_square Q z) k

#print axioms triple_singular_radical
#print axioms equal_label_integer_relation

end MathCompression.CharacteristicTwoTranslations
