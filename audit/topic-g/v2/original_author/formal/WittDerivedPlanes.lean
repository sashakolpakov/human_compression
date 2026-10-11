import DeletedLineFourResidue

/-! Explicit finite derived-plane incidence maps. The original Witt
designs and their derivation remain GAP-checked inputs; this file
checks every incidence against literal F4 coordinate arithmetic. -/

namespace MathCompression.WittDerivedPlanes
open MathCompression.DeletedLineFourResidue
set_option maxRecDepth 1000000
set_option maxHeartbeats 0

def coordinate : Fin 21 → Fin 3 → F4 :=
  ![![(0, 0), (0, 0), (1, 0)], ![(0, 0), (1, 0), (0, 0)], ![(0, 0), (1, 0), (1, 0)], ![(0, 0), (1, 0), (0, 1)], ![(0, 0), (1, 0), (1, 1)], ![(1, 0), (0, 0), (0, 0)], ![(1, 0), (0, 0), (1, 0)], ![(1, 0), (0, 0), (0, 1)], ![(1, 0), (0, 0), (1, 1)], ![(1, 0), (1, 0), (0, 0)], ![(1, 0), (1, 0), (1, 0)], ![(1, 0), (1, 0), (0, 1)], ![(1, 0), (1, 0), (1, 1)], ![(1, 0), (0, 1), (0, 0)], ![(1, 0), (0, 1), (1, 0)], ![(1, 0), (0, 1), (0, 1)], ![(1, 0), (0, 1), (1, 1)], ![(1, 0), (1, 1), (0, 0)], ![(1, 0), (1, 1), (1, 0)], ![(1, 0), (1, 1), (0, 1)], ![(1, 0), (1, 1), (1, 1)]]

def coordinateIncident (p l : Fin 21) : Prop :=
  mul4 (coordinate p 0) (coordinate l 0) +
  mul4 (coordinate p 1) (coordinate l 1) +
  mul4 (coordinate p 2) (coordinate l 2) = 0

instance (p l : Fin 21) : Decidable (coordinateIncident p l) :=
  inferInstanceAs (Decidable (_ = _))

structure IncidenceIso (source : Fin 21 → Fin 21 → Prop) where
  points : Fin 21 ≃ Fin 21
  lines : Fin 21 ≃ Fin 21
  preserves : ∀ p l, source p l ↔ coordinateIncident (points p) (lines l)

def nativeLines22 : Fin 21 → List (Fin 21) :=
  ![[0, 1, 5, 8, 18], [0, 2, 13, 15, 16], [0, 3, 11, 12, 19], [0, 4, 7, 9, 17], [0, 6, 10, 14, 20], [1, 2, 3, 7, 20], [1, 4, 10, 16, 19], [1, 6, 11, 13, 17], [1, 9, 12, 14, 15], [2, 4, 5, 6, 12], [2, 8, 14, 17, 19], [2, 9, 10, 11, 18], [3, 4, 13, 14, 18], [3, 5, 10, 15, 17], [3, 6, 8, 9, 16], [4, 8, 11, 15, 20], [5, 7, 11, 14, 16], [5, 9, 13, 19, 20], [6, 7, 15, 18, 19], [7, 8, 10, 12, 13], [12, 16, 17, 18, 20]]

def pointMap22 : Fin 21 → Fin 21 :=
  ![0, 1, 5, 17, 10, 2, 15, 9, 3, 12, 14, 19, 20, 7, 16, 8, 6, 11, 4, 18, 13]

def lineMap22 : Fin 21 → Fin 21 :=
  ![5, 1, 13, 9, 17, 0, 6, 8, 7, 2, 4, 3, 16, 15, 14, 19, 10, 20, 11, 12, 18]

theorem maps22_bijective : Function.Bijective pointMap22 ∧
    Function.Bijective lineMap22 := by decide

theorem incidence22 : ∀ p l : Fin 21,
    p ∈ nativeLines22 l ↔ coordinateIncident (pointMap22 p) (lineMap22 l) := by
  decide

noncomputable def iso22 : IncidenceIso (fun p l => p ∈ nativeLines22 l) where
  points := Equiv.ofBijective pointMap22 maps22_bijective.1
  lines := Equiv.ofBijective lineMap22 maps22_bijective.2
  preserves := incidence22

#print axioms maps22_bijective
#print axioms incidence22
#print axioms iso22

def nativeLines23 : Fin 21 → List (Fin 21) :=
  ![[0, 1, 3, 12, 15], [0, 2, 11, 14, 20], [0, 4, 5, 17, 19], [0, 6, 9, 10, 16], [0, 7, 8, 13, 18], [1, 2, 9, 17, 18], [1, 4, 6, 8, 11], [1, 5, 7, 14, 16], [1, 10, 13, 19, 20], [2, 3, 5, 6, 13], [2, 4, 7, 10, 15], [2, 8, 12, 16, 19], [3, 4, 16, 18, 20], [3, 7, 9, 11, 19], [3, 8, 10, 14, 17], [4, 9, 12, 13, 14], [5, 8, 9, 15, 20], [5, 10, 11, 12, 18], [6, 7, 12, 17, 20], [6, 14, 15, 18, 19], [11, 13, 15, 16, 17]]

def pointMap23 : Fin 21 → Fin 21 :=
  ![0, 1, 5, 3, 10, 11, 18, 15, 14, 17, 20, 6, 4, 16, 7, 2, 19, 9, 13, 12, 8]

def lineMap23 : Fin 21 → Fin 21 :=
  ![5, 1, 9, 13, 17, 0, 6, 8, 7, 4, 2, 3, 19, 14, 12, 16, 15, 18, 11, 20, 10]

theorem maps23_bijective : Function.Bijective pointMap23 ∧
    Function.Bijective lineMap23 := by decide

theorem incidence23 : ∀ p l : Fin 21,
    p ∈ nativeLines23 l ↔ coordinateIncident (pointMap23 p) (lineMap23 l) := by
  decide

noncomputable def iso23 : IncidenceIso (fun p l => p ∈ nativeLines23 l) where
  points := Equiv.ofBijective pointMap23 maps23_bijective.1
  lines := Equiv.ofBijective lineMap23 maps23_bijective.2
  preserves := incidence23

#print axioms maps23_bijective
#print axioms incidence23
#print axioms iso23

def nativeLines24 : Fin 21 → List (Fin 21) :=
  ![[0, 1, 4, 7, 9], [0, 2, 11, 14, 20], [0, 3, 6, 8, 19], [0, 5, 12, 13, 16], [0, 10, 15, 17, 18], [1, 2, 6, 15, 16], [1, 3, 5, 11, 17], [1, 8, 12, 14, 18], [1, 10, 13, 19, 20], [2, 3, 9, 10, 12], [2, 4, 8, 13, 17], [2, 5, 7, 18, 19], [3, 4, 16, 18, 20], [3, 7, 13, 14, 15], [4, 5, 6, 10, 14], [4, 11, 12, 15, 19], [5, 8, 9, 15, 20], [6, 7, 12, 17, 20], [6, 9, 11, 13, 18], [7, 8, 10, 11, 16], [9, 14, 16, 17, 19]]

def pointMap24 : Fin 21 → Fin 21 :=
  ![0, 1, 5, 10, 3, 14, 9, 4, 11, 2, 20, 6, 15, 16, 7, 17, 13, 18, 19, 12, 8]

def lineMap24 : Fin 21 → Fin 21 :=
  ![5, 1, 9, 17, 13, 0, 6, 8, 7, 2, 4, 3, 19, 16, 12, 14, 15, 11, 10, 18, 20]

theorem maps24_bijective : Function.Bijective pointMap24 ∧
    Function.Bijective lineMap24 := by decide

theorem incidence24 : ∀ p l : Fin 21,
    p ∈ nativeLines24 l ↔ coordinateIncident (pointMap24 p) (lineMap24 l) := by
  decide

noncomputable def iso24 : IncidenceIso (fun p l => p ∈ nativeLines24 l) where
  points := Equiv.ofBijective pointMap24 maps24_bijective.1
  lines := Equiv.ofBijective lineMap24 maps24_bijective.2
  preserves := incidence24

#print axioms maps24_bijective
#print axioms incidence24
#print axioms iso24

end MathCompression.WittDerivedPlanes
