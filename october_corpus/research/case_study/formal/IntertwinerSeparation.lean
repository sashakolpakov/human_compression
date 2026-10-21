import Mathlib.Algebra.Ring.Basic

/-!
An abstract obstruction to an off-block intertwiner. In the written
four-dimensional projective argument, R is the ring of two-by-two matrices;
the signs of the source generators are absorbed into x and y. The normal
forms and the invertibility of their commutators are separate inputs.
-/
namespace MathCompression

variable {R : Type*} [Ring R]

theorem additive_commutator_transport (a b x y c : R)
    (ha : a * c = c * x) (hb : b * c = c * y) :
    (a * b - b * a) * c = c * (x * y - y * x) := by
  have h₁ : (a * b) * c = c * (x * y) := by
    calc
      (a * b) * c = a * (b * c) := mul_assoc a b c
      _ = a * (c * y) := by rw [hb]
      _ = (a * c) * y := (mul_assoc a c y).symm
      _ = (c * x) * y := by rw [ha]
      _ = c * (x * y) := mul_assoc c x y
  have h₂ : (b * a) * c = c * (y * x) := by
    calc
      (b * a) * c = b * (a * c) := mul_assoc b a c
      _ = b * (c * x) := by rw [ha]
      _ = (b * c) * x := (mul_assoc b c x).symm
      _ = (c * y) * x := by rw [hb]
      _ = c * (y * x) := mul_assoc c y x
  rw [sub_mul, h₁, h₂, mul_sub]

theorem intertwiner_zero_of_commuting_left (a b x y c d : R)
    (ha : a * c = c * x) (hb : b * c = c * y)
    (hab : a * b = b * a) (hd : (x * y - y * x) * d = 1) :
    c = 0 := by
  have hz : c * (x * y - y * x) = 0 := by
    rw [← additive_commutator_transport a b x y c ha hb, hab, sub_self, zero_mul]
  calc
    c = c * 1 := (mul_one c).symm
    _ = c * ((x * y - y * x) * d) := by rw [hd]
    _ = (c * (x * y - y * x)) * d := (mul_assoc c _ d).symm
    _ = 0 := by rw [hz, zero_mul]

#print axioms additive_commutator_transport
#print axioms intertwiner_zero_of_commuting_left

end MathCompression
