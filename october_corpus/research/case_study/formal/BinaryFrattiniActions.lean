import Mathlib.Tactic
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Basic

/-!
Finite binary-linear component of the abelian-Frattini argument.
Vectors are triples of bits, with coordinatewise xor addition. A matrix
is specified by its three columns. The group-theoretic identification
with a Frattini quotient and the lifting to central involutions are
separate written arguments.
-/

namespace MathCompression.BinaryFrattini

abbrev V := Bool × Bool × Bool

def zero : V := (false, false, false)
def x : V := (true, false, false)
def y : V := (false, true, false)
def z : V := (false, false, true)

def add (a b : V) : V :=
  (Bool.xor a.1 b.1, Bool.xor a.2.1 b.2.1, Bool.xor a.2.2 b.2.2)

def select (t : Bool) (a : V) : V := if t then a else zero

def lin (a b c : V) (v : V) : V :=
  add (add (select v.1 a) (select v.2.1 b)) (select v.2.2 c)

def compatible (sy sz tx tz : V) : Prop :=
  let S := lin x sy sz
  let T := lin tx y tz
  (∀ v, S (S v) = v) ∧ (∀ v, T (T v) = v) ∧
  (∀ v, S (T v) = T (S v)) ∧
  ∃ d f : V,
    add (T x) x = add (S d) d ∧
    add (S y) y = add (T d) d ∧
    z = add (add (add (add x y) (T d)) f) (S (T f))

def classified (sy sz tx tz : V) : Prop :=
  (sy = y ∧ sz = z ∧ tx = x ∧ tz = z) ∨
  (sy = y ∧ sz = add y z ∧ tx = add x y ∧ tz = add y z) ∨
  (sy = add x y ∧ sz = add x z ∧ tx = x ∧ tz = add x z) ∨
  (sy = add y z ∧ sz = z ∧ tx = add x z ∧ tz = z)

instance compatibleDecidable (sy sz tx tz : V) :
    Decidable (compatible sy sz tx tz) := by
  unfold compatible
  dsimp only
  infer_instance

instance classifiedDecidable (sy sz tx tz : V) :
    Decidable (classified sy sz tx tz) := by
  unfold classified
  infer_instance

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem binary_action_classification :
    ∀ sy sz tx tz : V, compatible sy sz tx tz → classified sy sz tx tz := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem classified_is_compatible :
    ∀ sy sz tx tz : V, classified sy sz tx tz → compatible sy sz tx tz := by
  decide +kernel

theorem binary_action_classification_iff (sy sz tx tz : V) :
    compatible sy sz tx tz ↔ classified sy sz tx tz :=
  ⟨binary_action_classification sy sz tx tz, classified_is_compatible sy sz tx tz⟩

def coordinateSupported (sy sz tx tz : V) : Prop :=
  let S := lin x sy sz
  let T := lin tx y tz
  ∃ w : V, (w = x ∨ w = y ∨ w = z) ∧
    S w = w ∧ T w = w ∧
    (∀ v, add (S v) v = zero ∨ add (S v) v = w) ∧
    (∀ v, add (T v) v = zero ∨ add (T v) v = w)

instance coordinateSupportedDecidable (sy sz tx tz : V) :
    Decidable (coordinateSupported sy sz tx tz) := by
  unfold coordinateSupported
  dsimp only
  infer_instance

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem classified_has_coordinate_support :
    ∀ sy sz tx tz : V, classified sy sz tx tz → coordinateSupported sy sz tx tz := by
  decide +kernel

theorem binary_action_has_coordinate_support (sy sz tx tz : V)
    (h : compatible sy sz tx tz) : coordinateSupported sy sz tx tz :=
  classified_has_coordinate_support sy sz tx tz
    (binary_action_classification sy sz tx tz h)

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem lin_preserves_binary_addition :
    ∀ a b c u v : V, lin a b c (add u v) = add (lin a b c u) (lin a b c v) := by
  decide +kernel

#print axioms binary_action_classification
#print axioms classified_is_compatible
#print axioms binary_action_classification_iff
#print axioms classified_has_coordinate_support
#print axioms binary_action_has_coordinate_support
#print axioms lin_preserves_binary_addition

end MathCompression.BinaryFrattini
