import Mathlib.Algebra.Group.Hom.Basic
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
An additive embedding with an additive left inverse preserves and reflects
divisibility by every positive or zero natural modulus. The literal inverse
below is the six-coordinate minor in the even-family lattice certificate.
The module does not encode the 1296-coordinate Schreier enumeration.
-/
namespace MathCompression.SplitLatticeReduction

variable {A B : Type*} [AddCommGroup A] [AddCommGroup B]

theorem modulus_membership (f : A →+ B) (p : B →+ A)
    (hleft : ∀ a, p (f a) = a) (m : ℕ) (a : A) :
    (∃ b : B, f a = m • b) ↔ ∃ c : A, a = m • c := by
  constructor
  · rintro ⟨b, hb⟩
    refine ⟨p b, ?_⟩
    calc
      a = p (f a) := (hleft a).symm
      _ = p (m • b) := congrArg p hb
      _ = m • p b := by simp
  · rintro ⟨c, rfl⟩
    exact ⟨f c, by simp⟩

theorem same_reduction_iff (f : A →+ B) (p : B →+ A)
    (hleft : ∀ a, p (f a) = a) (m : ℕ) (a b : A) :
    (∃ y : B, f a - f b = m • y) ↔ ∃ x : A, a - b = m • x := by
  simpa only [map_sub] using modulus_membership f p hleft m (a - b)

def minor : Matrix (Fin 6) (Fin 6) ℤ :=
  !![0,0,1,-1,0,0;
     0,0,0,0,-1,-1;
     1,0,0,1,1,0;
     0,0,-1,0,-1,1;
     0,0,0,0,1,0;
     1,1,-1,0,0,0]

def integralInverse : Matrix (Fin 6) (Fin 6) ℤ :=
  !![1,1,1,1,1,0;
     -1,-2,-1,-2,-3,1;
     0,-1,0,-1,-2,0;
     -1,-1,0,-1,-2,0;
     0,0,0,0,1,0;
     0,-1,0,0,-1,0]

theorem literal_two_sided_inverse :
    minor * integralInverse = 1 ∧ integralInverse * minor = 1 := by
  decide +kernel

#print axioms modulus_membership
#print axioms same_reduction_iff
#print axioms literal_two_sided_inverse
end MathCompression.SplitLatticeReduction
