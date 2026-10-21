import Mathlib.GroupTheory.GroupAction.Basic

/-!
Actual stabilizer transport in fibers of an equivariant map.
The orbit equivalence below applies to a single selected base orbit.
No finiteness, faithfulness, geometric recognition or census is assumed.
-/

namespace MathCompression.ExtensionOrbits

variable {G Z E : Type*} [Group G] [MulAction G Z] [MulAction G E]
variable (p : Z → E) (hp : ∀ (g : G) (z : Z), p (g • z) = g • p z)

def Fiber (e : E) := {z : Z // p z = e}

include hp

/-- An ambient equivalence within one fiber is already a stabilizer equivalence. -/
theorem fiber_orbit_iff (e : E) (x y : Fiber p e) :
    (∃ g : G, g • x.val = y.val) ↔
      ∃ g : MulAction.stabilizer G e, (g : G) • x.val = y.val := by
  constructor
  · rintro ⟨g, hg⟩
    have he : g • e = e := by
      calc
        g • e = g • p x.val := congrArg (g • ·) x.property.symm
        _ = p (g • x.val) := (hp g x.val).symm
        _ = p y.val := congrArg p hg
        _ = e := y.property
    exact ⟨⟨g, he⟩, hg⟩
  · rintro ⟨g, hg⟩
    exact ⟨g.val, hg⟩

def fiberRelation (e : E) : Setoid (Fiber p e) :=
  (MulAction.orbitRel (MulAction.stabilizer G e) Z).comap Subtype.val

def fiberOrbitMap (e : E) :
    Quotient (fiberRelation (G := G) p e) → Quotient (MulAction.orbitRel G Z) :=
  Quotient.map Subtype.val (by
    intro x y h
    obtain ⟨g, hg⟩ := h
    exact ⟨g.val, hg⟩)

theorem fiberOrbitMap_injective (e : E) :
    Function.Injective (fiberOrbitMap (G := G) p e) := by
  intro a b
  refine Quotient.inductionOn₂ a b ?_
  intro x y h
  apply Quotient.sound
  obtain ⟨g, hg⟩ := Quotient.exact h
  obtain ⟨k, hk⟩ := (fiber_orbit_iff p hp e y x).mp ⟨g, hg⟩
  exact ⟨k, hk⟩

/-- Translating the image to a selected base also translates the object into its fiber. -/
theorem normalize_to_fiber (e : E) (z : Z) (g : G) (hg : g • p z = e) :
    p (g • z) = e := by
  rw [hp, hg]

/-- If the base image is a single orbit, every ambient orbit meets the chosen fiber. -/
theorem fiberOrbitMap_surjective (e : E)
    (hbase : ∀ z : Z, ∃ g : G, g • p z = e) :
    Function.Surjective (fiberOrbitMap (G := G) p e) := by
  intro q
  refine Quotient.inductionOn q ?_
  intro z
  obtain ⟨g, hg⟩ := hbase z
  refine ⟨Quotient.mk _ ⟨g • z, normalize_to_fiber p hp e z g hg⟩, ?_⟩
  apply Quotient.sound
  exact ⟨g, rfl⟩

/-- The actual ambient orbit quotient equals the stabilizer quotient of a chosen fiber. -/
noncomputable def fiberOrbitEquiv (e : E)
    (hbase : ∀ z : Z, ∃ g : G, g • p z = e) :
    Quotient (fiberRelation (G := G) p e) ≃ Quotient (MulAction.orbitRel G Z) :=
  Equiv.ofBijective (fiberOrbitMap (G := G) p e)
    ⟨fiberOrbitMap_injective p hp e, fiberOrbitMap_surjective p hp e hbase⟩

theorem fiberOrbitEquiv_apply (e : E)
    (hbase : ∀ z : Z, ∃ g : G, g • p z = e)
    (x : Fiber p e) :
    fiberOrbitEquiv p hp e hbase (Quotient.mk _ x) = Quotient.mk _ x.val := rfl

omit hp in
/-- An action with an odd period has the same fixed points for a and its square. -/
theorem fixed_of_square_fixed (a : G) (x : Z) (n : ℕ)
    (hperiod : a ^ (2 * n + 1) = 1) (hsquare : (a ^ 2) • x = x) :
    a • x = x := by
  have all_powers : ∀ m : ℕ, (a ^ 2) ^ m • x = x := by
    intro m
    induction m with
    | zero => simp
    | succ m ih => rw [pow_succ, mul_smul, hsquare, ih]
  have hfix : a ^ (2 * n) • x = x := by
    rw [pow_mul]
    exact all_powers n
  calc
    a • x = a • (a ^ (2 * n) • x) := congrArg (a • ·) hfix.symm
    _ = a ^ (2 * n + 1) • x := by rw [pow_succ', mul_smul]
    _ = x := by rw [hperiod, one_smul]

omit hp in
/-- A commuting fixed-point-free involution cannot fix an orbit of an odd-period action. -/
theorem odd_action_involution_no_fixed_orbit
    (D : Z → Z) (hD : Function.Involutive D)
    (hcomm : ∀ (g : G) (z : Z), D (g • z) = g • D z)
    (hfree : ∀ z : Z, D z ≠ z)
    (hodd : ∀ g : G, ∃ n : ℕ, g ^ (2 * n + 1) = 1) :
    ∀ z : Z, ¬ ∃ g : G, D z = g • z := by
  rintro z ⟨g, hg⟩
  obtain ⟨n, hn⟩ := hodd g
  have hsq : (g ^ 2) • z = z := by
    calc
      (g ^ 2) • z = g • (g • z) := by rw [pow_two, mul_smul]
      _ = g • D z := congrArg (g • ·) hg.symm
      _ = D (g • z) := (hcomm g z).symm
      _ = D (D z) := congrArg D hg.symm
      _ = z := hD z
  exact hfree z (hg.trans (fixed_of_square_fixed g z n hn hsq))

#print axioms fiber_orbit_iff
#print axioms fiberOrbitMap_injective
#print axioms normalize_to_fiber
#print axioms fiberOrbitMap_surjective
#print axioms fiberOrbitEquiv
#print axioms fiberOrbitEquiv_apply
#print axioms fixed_of_square_fixed
#print axioms odd_action_involution_no_fixed_orbit

end MathCompression.ExtensionOrbits
