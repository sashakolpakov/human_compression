import Mathlib.LinearAlgebra.Matrix.Notation

/-! Literal compact affine data only. The base census and geometric adapter
are external to this module. All finite identities are kernel-checked. -/
namespace MathCompression.CompactAffineData

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

def r0 : Matrix (Fin 7) (Fin 7) ℤ :=
  !![-1,-1,0,0,0,1,0;
     0,1,0,0,0,0,0;
     0,0,0,1,1,1,0;
     0,0,0,1,0,0,0;
     0,0,1,-1,0,-1,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1]

def r1 : Matrix (Fin 7) (Fin 7) ℤ :=
  !![0,0,0,1,0,0,0;
     0,-1,0,0,0,0,0;
     0,-1,1,0,0,0,0;
     1,0,0,0,0,0,0;
     0,0,0,0,0,-1,0;
     0,0,0,0,-1,0,0;
     0,0,0,0,0,0,1]

def r2 : Matrix (Fin 7) (Fin 7) ℤ :=
  !![1,0,0,0,0,0,0;
     -1,-1,0,1,0,0,0;
     0,0,-1,1,-1,1,-1;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1]

def r3 : Matrix (Fin 7) (Fin 7) ℤ :=
  !![1,1,0,0,0,-1,0;
     0,-1,0,0,0,0,0;
     0,0,0,-1,-1,-1,0;
     0,0,-1,0,-1,0,0;
     0,0,0,0,1,1,0;
     0,0,0,0,0,-1,0;
     0,0,0,0,0,0,1]

def x := r0 * r1
def y := r0 * r2
def z := r0 * r3
def xi := r1 * r0
def yi := r2 * r0

theorem marked_involutions :
    r0 * r0 = 1 ∧ r1 * r1 = 1 ∧ r2 * r2 = 1 ∧ r3 * r3 = 1 := by
  decide +kernel

theorem source_nine_relations :
    x^6 = 1 ∧ y^3 = 1 ∧ z^2 = 1 ∧ (z*x)^3 = 1 ∧
    (z*y)^6 = 1 ∧ (xi*y)^2 = 1 ∧ (yi*xi^2)^3 = 1 ∧
    (z*x^3)^2 = 1 ∧ (xi*z*(yi*z)^2)*(z*x*(z*y)^2) = 1 := by
  decide +kernel

def T := y * (z*y)^2
def u := yi*z
def ui := z*y

theorem parameter_translations :
    T^2 = !![1,0,0,0,0,0,-2;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    ui*T^2*u = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,-2;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] := by
  decide +kernel

def basisWord0 := r1 * r3 * r2 * r3 * r1 * r0 * r1 * r3 * r2 * r3 * r1 * r0
def basisWord1 := r2 * r0 * r3 * r2 * r0 * r3 * r2 * r3 * r0 * r2 * r3 * r0
def basisWord2 := r3 * r1 * r0 * r1 * r3 * r2 * r3 * r1 * r0 * r1 * r3 * r2
def basisWord3 := r3 * r2 * r3 * r1 * r0 * r1 * r3 * r2 * r3 * r1 * r0 * r1
def basisWord4 := r0 * r3 * r1 * r0 * r1 * r3 * r2 * r3 * r1 * r0 * r1 * r3 * r2 * r0
def basisWord5 := r1 * r0 * r1 * r2 * r3 * r1 * r0 * r1 * r3 * r2 * r0 * r1 * r3 * r0

theorem basis_translations :
    basisWord0 = !![1,0,0,0,0,0,2;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    basisWord1 = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,2;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    basisWord2 = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,2;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    basisWord3 = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,2;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    basisWord4 = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,2;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1] ∧
    basisWord5 = !![1,0,0,0,0,0,0;
     0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     0,0,0,0,1,0,0;
     0,0,0,0,0,1,2;
     0,0,0,0,0,0,1] := by
  decide +kernel

#print axioms marked_involutions
#print axioms source_nine_relations
#print axioms parameter_translations
#print axioms basis_translations
end MathCompression.CompactAffineData
