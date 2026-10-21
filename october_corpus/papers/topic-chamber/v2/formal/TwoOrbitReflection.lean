import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.GroupTheory.GroupAction.Defs

/-!
The actual two-copy chamber model. The second coordinate false denotes the
positive copy and true denotes the negative copy. This file proves the
involution, color-preservation and conjugation formulas on G × Bool, including
involutivity of an inverting automorphism from the actual generation hypothesis.
It does not formalize residual connectivity or reconstruction of geometry.
-/
namespace MathCompression.TwoOrbitReflection
variable {G I : Type*} [Group G]

def neighbor (a : G) (x : G × Bool) : G × Bool :=
  if x.2 then (x.1 * a, false) else (x.1 * a⁻¹, true)

def reflect (θ : G ≃* G) (x : G × Bool) : G × Bool :=
  (θ x.1, !x.2)

def translate (g : G) (x : G × Bool) : G × Bool := (g * x.1, x.2)

theorem neighbor_involutive (a : G) : Function.Involutive (neighbor a) := by
  rintro ⟨g, b⟩
  cases b <;> simp [neighbor, mul_assoc]

theorem neighbor_translate (a g : G) (x : G × Bool) :
    neighbor a (translate g x) = translate g (neighbor a x) := by
  rcases x with ⟨h,b⟩
  cases b <;> simp [neighbor, translate, mul_assoc]

theorem inversion_is_involutive (α : I → G)
    (hgen : Subgroup.closure (Set.range α) = ⊤)
    (θ : G ≃* G) (hinv : ∀ i, θ (α i) = (α i)⁻¹) :
    Function.Involutive θ := by
  intro g
  have hg : g ∈ Subgroup.closure (Set.range α) := by rw [hgen]; trivial
  induction hg using Subgroup.closure_induction with
  | mem x hx =>
      obtain ⟨i, rfl⟩ := hx
      simp [hinv]
  | one => simp
  | mul x y _ _ hx hy => simp only [map_mul, hx, hy]
  | inv x _ hx => simp only [map_inv, hx]

theorem reflect_involutive (θ : G ≃* G) (hθ : Function.Involutive θ) :
    Function.Involutive (reflect θ) := by
  rintro ⟨g,b⟩
  cases b <;> simp [reflect, hθ g]

theorem reflect_preserves_color (θ : G ≃* G) (a : G)
    (ha : θ a = a⁻¹) (x : G × Bool) :
    reflect θ (neighbor a x) = neighbor a (reflect θ x) := by
  rcases x with ⟨g,b⟩
  cases b <;> simp [reflect, neighbor, map_mul, ha]

theorem reflect_translate (θ : G ≃* G) (g : G) (x : G × Bool) :
    reflect θ (translate g x) = translate (θ g) (reflect θ x) := by
  rcases x with ⟨h,b⟩
  simp [reflect, translate, map_mul]

theorem actual_reflection (α : I → G)
    (hgen : Subgroup.closure (Set.range α) = ⊤)
    (θ : G ≃* G) (hinv : ∀ i, θ (α i) = (α i)⁻¹) :
    Function.Involutive (reflect θ) ∧
      (∀ i x, reflect θ (neighbor (α i) x) = neighbor (α i) (reflect θ x)) ∧
      (∀ g x, reflect θ (translate g x) = translate (θ g) (reflect θ x)) := by
  exact ⟨reflect_involutive θ (inversion_is_involutive α hgen θ hinv),
    fun i x => reflect_preserves_color θ (α i) (hinv i) x,
    fun g x => reflect_translate θ g x⟩

#print axioms neighbor_involutive
#print axioms neighbor_translate
#print axioms inversion_is_involutive
#print axioms reflect_involutive
#print axioms reflect_preserves_color
#print axioms reflect_translate
#print axioms actual_reflection
end MathCompression.TwoOrbitReflection
