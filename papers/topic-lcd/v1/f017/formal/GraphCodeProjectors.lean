import Mathlib.Algebra.Module.Submodule.Ker
import Mathlib.Algebra.Module.Submodule.Range
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.Abel

/-
Generic formal portion of umbrella_projectors.tex.
The finite graph constructions, degree-regularity deduction, image identifications,
and source-specific distances and module assertions are not formalized here.
No result is declared as an axiom.
-/
namespace GraphCodeProjectors

section RingIdentities
variable {R : Type*} [Ring R]

/-- The two complementary projections associated with a reflexive graph code. -/
theorem reflexive_projections (a : R) (h : a * a = -a) :
    (-a) * (-a) = -a ∧
    (1 + a) * (1 + a) = 1 + a ∧
    (-a) * (1 + a) = 0 ∧
    (1 + a) * (-a) = 0 ∧
    -a + (1 + a) = 1 := by
  constructor
  · simpa using h
  constructor
  · calc
      (1 + a) * (1 + a) = 1 + a + a + a * a := by noncomm_ring
      _ = 1 + a := by rw [h]; abel
  constructor
  · calc
      (-a) * (1 + a) = -a - a * a := by noncomm_ring
      _ = 0 := by rw [h]; abel
  constructor
  · calc
      (1 + a) * (-a) = -a - a * a := by noncomm_ring
      _ = 0 := by rw [h]; abel
  · abel

/-- In the exceptional case the constant projection is a third summand. -/
theorem exceptional_projections (a b j : R)
    (ha : a * a = -a) (hb : b * b = -b) (hj : j * j = j)
    (hab : a * b = 0) (hba : b * a = 0)
    (haj : a * j = 0) (hja : j * a = 0)
    (hbj : b * j = 0) (hjb : j * b = 0)
    (hsum : a + b = j - 1) :
    (-a) * (-a) = -a ∧ (-b) * (-b) = -b ∧ j * j = j ∧
    (-a) * (-b) = 0 ∧ (-b) * (-a) = 0 ∧
    (-a) * j = 0 ∧ j * (-a) = 0 ∧
    (-b) * j = 0 ∧ j * (-b) = 0 ∧ -a + -b + j = 1 := by
  refine ⟨by simpa using ha, by simpa using hb, hj,
    by simpa using hab, by simpa using hba,
    by simp [haj], by simp [hja], by simp [hbj], by simp [hjb], ?_⟩
  calc
    -a + -b + j = -(a + b) + j := by abel
    _ = 1 := by rw [hsum]; abel
end RingIdentities

section LinearAlgebra
variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Idempotents have disjoint image and kernel over an arbitrary field. -/
theorem range_ker_disjoint (e : V →ₗ[K] V)
    (he : ∀ x, e (e x) = e x) :
    Disjoint (LinearMap.range e) (LinearMap.ker e) := by
  rw [Submodule.disjoint_def]
  intro x hx hk
  obtain ⟨y, rfl⟩ := hx
  have hk' : e (e y) = 0 := hk
  simpa only [he] using hk'

/-- A symmetric idempotent has an LCD image for any nondegenerate bilinear form.
The last hypothesis states nondegeneracy in the first argument explicitly. -/
theorem idempotent_image_lcd (e : V →ₗ[K] V)
    (b : V →ₗ[K] V →ₗ[K] K)
    (he : ∀ x, e (e x) = e x)
    (hsym : ∀ x y, b (e x) y = b x (e y))
    (hnd : ∀ x, (∀ y, b x y = 0) → x = 0)
    (x : V) (hx : x ∈ LinearMap.range e)
    (horth : ∀ z ∈ LinearMap.range e, b x z = 0) : x = 0 := by
  obtain ⟨y, hy⟩ := hx
  have hex : e x = x := by rw [← hy, he]
  apply hnd x
  intro z
  calc
    b x z = b (e x) z := by rw [hex]
    _ = b x (e z) := hsym x z
    _ = 0 := horth (e z) ⟨z, rfl⟩

/-- Complementary annihilating idempotents give an actual direct decomposition. -/
theorem complementary_images (e f : V →ₗ[K] V)
    (he : ∀ x, e (e x) = e x)
    (hef : ∀ x, e (f x) = 0)
    (hsum : ∀ x, e x + f x = x) :
    Disjoint (LinearMap.range e) (LinearMap.range f) ∧
    (∀ x, ∃ y ∈ LinearMap.range e, ∃ z ∈ LinearMap.range f, x = y + z) := by
  constructor
  · rw [Submodule.disjoint_def]
    intro x hx hf
    obtain ⟨y, hy⟩ := hx
    obtain ⟨z, hz⟩ := hf
    have h1 : e x = x := by rw [← hy, he]
    have h2 : e x = 0 := by rw [← hz, hef]
    exact h1.symm.trans h2
  · intro x
    exact ⟨e x, ⟨x, rfl⟩, f x, ⟨x, rfl⟩, (hsum x).symm⟩

/-- Annihilation and adjoint symmetry imply orthogonality of the two images. -/
theorem images_orthogonal (e f : V →ₗ[K] V)
    (b : V →ₗ[K] V →ₗ[K] K)
    (hsym : ∀ x y, b (e x) y = b x (e y))
    (hef : ∀ x, e (f x) = 0)
    (x y : V) (hx : x ∈ LinearMap.range e) (hy : y ∈ LinearMap.range f) :
    b x y = 0 := by
  obtain ⟨u, rfl⟩ := hx
  obtain ⟨v, rfl⟩ := hy
  rw [hsym, hef, map_zero]
end LinearAlgebra

#print axioms reflexive_projections
#print axioms exceptional_projections
#print axioms range_ker_disjoint
#print axioms idempotent_image_lcd
#print axioms complementary_images
#print axioms images_orthogonal
end GraphCodeProjectors
