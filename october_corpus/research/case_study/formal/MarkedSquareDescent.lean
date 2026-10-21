import BinaryFrattiniActions

/-!
Two finite-linear components of the cyclic-TPP descent.

The first theorem classifies commuting involutions that fix the three
marked coordinates individually and have no common fixed coordinate.
The second proves the incompatibility of a marked equivariant map from
the binary Frattini action to an action with no fixed marked coordinate.

The group-theoretic construction and well-definedness of the square maps,
and the reduction of arbitrary 2-group images to commuting involutions,
remain separate written arguments. No full group theorem is claimed here.
-/

namespace MathCompression.MarkedSquareDescent

open MathCompression.BinaryFrattini

def marked (v : V) : Prop := v = x ∨ v = y ∨ v = z

def noFixedMarked (S T : V → V) : Prop :=
  ∀ v, marked v → ¬ (S v = v ∧ T v = v)

def weakCompatible (sy sz tx tz : V) : Prop :=
  let S := lin x sy sz
  let T := lin tx y tz
  (∀ v, S (S v) = v) ∧ (∀ v, T (T v) = v) ∧
  (∀ v, S (T v) = T (S v)) ∧ S (T z) = z ∧
  noFixedMarked S T

def rigid (sy sz tx tz : V) : Prop :=
  sy = add x z ∧ sz = add x y ∧
  tx = add y z ∧ tz = add x y

instance markedDecidable (v : V) : Decidable (marked v) := by
  unfold marked
  infer_instance

instance noFixedMarkedDecidable (S T : V → V) :
    Decidable (noFixedMarked S T) := by
  unfold noFixedMarked
  infer_instance

instance weakCompatibleDecidable (sy sz tx tz : V) :
    Decidable (weakCompatible sy sz tx tz) := by
  unfold weakCompatible
  dsimp only
  infer_instance

instance rigidDecidable (sy sz tx tz : V) :
    Decidable (rigid sy sz tx tz) := by
  unfold rigid
  infer_instance

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem marked_action_rigidity :
    ∀ sy sz tx tz : V, weakCompatible sy sz tx tz → rigid sy sz tx tz := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem rigid_action_exists :
    ∀ sy sz tx tz : V, rigid sy sz tx tz → weakCompatible sy sz tx tz := by
  decide +kernel

theorem fixed_marked_transport
    (S T S' T' f : V → V)
    (hmarked : ∀ v, marked v → f v = v)
    (hS : ∀ v, f (S v) = S' (f v))
    (hT : ∀ v, f (T v) = T' (f v))
    (hfixed : ∃ v, marked v ∧ S v = v ∧ T v = v)
    (hno : noFixedMarked S' T') : False := by
  obtain ⟨v, hv, hsv, htv⟩ := hfixed
  have hfv := hmarked v hv
  apply hno v hv
  constructor
  · calc
      S' v = S' (f v) := by rw [hfv]
      _ = f (S v) := (hS v).symm
      _ = v := by rw [hsv, hfv]
  · calc
      T' v = T' (f v) := by rw [hfv]
      _ = f (T v) := (hT v).symm
      _ = v := by rw [htv, hfv]

theorem no_frattini_to_unfixed_marked_map
    (sy sz tx tz : V) (S' T' f : V → V)
    (hcompat : compatible sy sz tx tz)
    (hmarked : ∀ v, marked v → f v = v)
    (hS : ∀ v, f (lin x sy sz v) = S' (f v))
    (hT : ∀ v, f (lin tx y tz v) = T' (f v))
    (hno : noFixedMarked S' T') : False := by
  have hsupp := binary_action_has_coordinate_support sy sz tx tz hcompat
  obtain ⟨v, hv, hsv, htv, _⟩ := hsupp
  exact fixed_marked_transport (lin x sy sz) (lin tx y tz) S' T' f
    hmarked hS hT ⟨v, hv, hsv, htv⟩ hno

#print axioms marked_action_rigidity
#print axioms rigid_action_exists
#print axioms fixed_marked_transport
#print axioms no_frattini_to_unfixed_marked_map

end MathCompression.MarkedSquareDescent
