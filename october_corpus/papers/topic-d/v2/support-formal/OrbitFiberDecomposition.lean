import SupportCounting

noncomputable section
open scoped BigOperators
namespace MathCompression.SupportCounting

variable {G X E I : Type*} [Group G] [MulAction G X] [MulAction G E]
variable (p : X → E) (hp : ∀ (g : G) (x : X), p (g • x) = g • p x)

/-- Send an orbit inside a stabilizer fiber to its ambient orbit. -/
def stabilizerFiberOrbitMap (e : E) :
    MulAction.orbitRel.Quotient (MulAction.stabilizer G e) (extensionFiber p hp e) →
      MulAction.orbitRel.Quotient G X :=
  Quotient.map Subtype.val (by
    intro x y h
    obtain ⟨g, hg⟩ := h
    exact ⟨g.val, congrArg Subtype.val hg⟩)

/-- Translation between two points of one fiber automatically stabilizes the base. -/
theorem stabilizerFiberOrbitMap_injective (e : E) :
    Function.Injective (stabilizerFiberOrbitMap p hp e) := by
  intro q t
  refine Quotient.inductionOn₂ q t ?_
  intro x y h
  obtain ⟨g, hg⟩ := Quotient.exact h
  have he : g • e = e := by
    calc
      g • e = g • p y.val := congrArg (g • ·) y.property.symm
      _ = p (g • y.val) := (hp g y.val).symm
      _ = p x.val := congrArg p hg
      _ = e := x.property
  exact Quotient.sound ⟨⟨g, he⟩, Subtype.ext hg⟩

/-- A representative-indexed disjoint union maps into the actual ambient orbit set. -/
def orbitFiberSumMap (representative : I → E) :
    (Σ i : I, MulAction.orbitRel.Quotient (MulAction.stabilizer G (representative i))
      (extensionFiber p hp (representative i))) → MulAction.orbitRel.Quotient G X :=
  fun q => stabilizerFiberOrbitMap p hp (representative q.1) q.2

/-- Distinct representative indices lie in distinct base orbits. This is the exact
transversal condition needed for injectivity, with no finiteness assumption. -/
theorem orbitFiberSumMap_injective (representative : I → E)
    (hseparate : ∀ (i j : I) (g : G), g • representative j = representative i → i = j) :
    Function.Injective (orbitFiberSumMap p hp representative) := by
  rintro ⟨i, q⟩ ⟨j, t⟩ h
  have hij : i = j := by
    revert h
    refine Quotient.inductionOn₂ q t ?_
    intro x y h
    obtain ⟨g, hg⟩ := Quotient.exact h
    apply hseparate i j g
    calc
      g • representative j = g • p y.val := congrArg (g • ·) y.property.symm
      _ = p (g • y.val) := (hp g y.val).symm
      _ = p x.val := congrArg p hg
      _ = representative i := x.property
  subst j
  have hqt : q = t := stabilizerFiberOrbitMap_injective p hp (representative i) h
  subst t
  rfl

/-- Every object whose base can be moved to a chosen representative supplies a
point in the corresponding fiber, without any chosen transporter in the theorem. -/
theorem orbitFiberSumMap_surjective (representative : I → E)
    (hcover : ∀ x : X, ∃ (i : I) (g : G), g • p x = representative i) :
    Function.Surjective (orbitFiberSumMap p hp representative) := by
  intro q
  refine Quotient.inductionOn q ?_
  intro x
  obtain ⟨i, g, hg⟩ := hcover x
  have hx : p (g • x) = representative i := (hp g x).trans hg
  refine ⟨⟨i, Quotient.mk _ ⟨g • x, hx⟩⟩, ?_⟩
  exact Quotient.sound ⟨g, rfl⟩

/-- The actual global orbit quotient is the disjoint union of actual stabilizer
fiber quotients over a complete base-orbit transversal. -/
def orbitFiberSumEquiv (representative : I → E)
    (hseparate : ∀ (i j : I) (g : G), g • representative j = representative i → i = j)
    (hcover : ∀ x : X, ∃ (i : I) (g : G), g • p x = representative i) :
    (Σ i : I, MulAction.orbitRel.Quotient (MulAction.stabilizer G (representative i))
      (extensionFiber p hp (representative i))) ≃ MulAction.orbitRel.Quotient G X :=
  Equiv.ofBijective (orbitFiberSumMap p hp representative)
    ⟨orbitFiberSumMap_injective p hp representative hseparate,
      orbitFiberSumMap_surjective p hp representative hcover⟩


/-- An equivariant equivalence induces an equivalence of the actual orbit quotients. -/
def equivariantOrbitEquiv {Y : Type*} [MulAction G Y] (e : X ≃ Y)
    (he : ∀ (g : G) (x : X), e (g • x) = g • e x) :
    MulAction.orbitRel.Quotient G X ≃ MulAction.orbitRel.Quotient G Y :=
  Quotient.congr e (by
    intro x y
    constructor
    · rintro ⟨g, hg⟩
      exact ⟨g, (he g y).symm.trans (congrArg e hg)⟩
    · rintro ⟨g, hg⟩
      exact ⟨g, e.injective ((he g y).trans hg)⟩)

/-- Classical quotient representatives satisfy orbit separation. -/
theorem orbitRepresentative_separate
    (i j : MulAction.orbitRel.Quotient G E) (g : G)
    (h : g • j.out = i.out) : i = j :=
  Quotient.out_equiv_out.mp ⟨g, h⟩

omit [MulAction G X] in
/-- Classical quotient representatives cover every base of every object. -/
theorem orbitRepresentative_cover (x : X) :
    ∃ (i : MulAction.orbitRel.Quotient G E) (g : G), g • p x = i.out :=
  ⟨Quotient.mk _ (p x), Quotient.mk_out (s := MulAction.orbitRel G E) (p x)⟩

section Support
variable {L : Type*} [PartialOrder L] [OrderTop L]
variable (s : X → L) (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤)

def exactSupportBase : exactSupport s hs → E := fun x => p x.val

include hp in
theorem exactSupportBase_equivariant (g : G) (x : exactSupport s hs) :
    exactSupportBase p s hs (g • x) = g • exactSupportBase p s hs x := hp g x.val

/-- Restricting to a base fiber and restricting to exact support commute, with their
actual stabilizer actions. This equivalence swaps the two subtype predicates. -/
def supportFiberEquiv (e : E) :
    extensionFiber (exactSupportBase p s hs) (exactSupportBase_equivariant p hp s hs) e ≃
      exactSupport (fun z : extensionFiber p hp e => s z.val)
        (fiber_top_invariant p hp e s hs) where
  toFun x := ⟨⟨x.val.val, x.property⟩, x.val.property⟩
  invFun x := ⟨⟨x.val.val, x.property⟩, x.val.property⟩
  left_inv x := by apply Subtype.ext; rfl
  right_inv x := by apply Subtype.ext; rfl

theorem supportFiberEquiv_equivariant (e : E) (g : MulAction.stabilizer G e)
    (x : extensionFiber (exactSupportBase p s hs) (exactSupportBase_equivariant p hp s hs) e) :
    supportFiberEquiv p hp s hs e (g • x) = g • supportFiberEquiv p hp s hs e x := rfl

/-- Global exact-support orbits are the disjoint union of the corresponding
stabilizer-fiber orbits. A complete transversal of all admissible bases suffices. -/
def exactSupportOrbitFiberSumEquiv (representative : I → E)
    (hseparate : ∀ (i j : I) (g : G), g • representative j = representative i → i = j)
    (hcover : ∀ x : X, ∃ (i : I) (g : G), g • p x = representative i) :
    (Σ i : I, MulAction.orbitRel.Quotient (MulAction.stabilizer G (representative i))
      (exactSupport (fun z : extensionFiber p hp (representative i) => s z.val)
        (fiber_top_invariant p hp (representative i) s hs))) ≃
      MulAction.orbitRel.Quotient G (exactSupport s hs) :=
  (Equiv.sigmaCongrRight (fun i =>
    (equivariantOrbitEquiv (supportFiberEquiv p hp s hs (representative i))
      (supportFiberEquiv_equivariant p hp s hs (representative i))).symm)).trans
    (orbitFiberSumEquiv (exactSupportBase p s hs) (exactSupportBase_equivariant p hp s hs)
      representative hseparate (fun x => hcover x.val))

include hp in
/-- The complete UD.AdmissibleExtensions formula, with its actual global orbit
quotient on the left and actual sublevel/fixed/base conditions on the right. -/
theorem admissible_extension_orbit_count
    [Fintype G] [Fintype X] [Fintype I] [Fintype L] [LocallyFiniteOrder L]
    [DecidableEq E] [DecidableEq L] [DecidableLE L]
    (representative : I → E)
    (hseparate : ∀ (i j : I) (g : G), g • representative j = representative i → i = j)
    (hcover : ∀ x : X, ∃ (i : I) (g : G), g • p x = representative i) :
    (Nat.card (MulAction.orbitRel.Quotient G (exactSupport s hs)) : ℚ) =
      ∑ i : I,
        (∑ a : MulAction.stabilizer G (representative i), ∑ l : L, topMobius l *
          (Nat.card {x : X // p x = representative i ∧ (a : G) • x = x ∧ s x ≤ l} : ℚ)) /
            (Nat.card (MulAction.stabilizer G (representative i)) : ℚ) := by
  classical
  rw [← Nat.card_congr (exactSupportOrbitFiberSumEquiv p hp s hs representative hseparate hcover),
    Nat.card_sigma, Nat.cast_sum]
  apply Finset.sum_congr rfl
  intro i _
  exact admissible_extension_fiber_count p hp (representative i) s hs

include hp in
/-- A complete transversal can be selected in Lean itself. Orbits of E disjoint
from the base image contribute empty fibers, hence zero summands. -/
theorem canonical_admissible_extension_orbit_count
    [Fintype G] [Fintype X] [Fintype E] [Fintype L] [LocallyFiniteOrder L]
    [DecidableEq E] [DecidableEq L] [DecidableLE L] :
    letI : Fintype (MulAction.orbitRel.Quotient G E) := Fintype.ofFinite _
    (Nat.card (MulAction.orbitRel.Quotient G (exactSupport s hs)) : ℚ) =
      ∑ i : MulAction.orbitRel.Quotient G E,
        (∑ a : MulAction.stabilizer G i.out, ∑ l : L, topMobius l *
          (Nat.card {x : X // p x = i.out ∧ (a : G) • x = x ∧ s x ≤ l} : ℚ)) /
            (Nat.card (MulAction.stabilizer G i.out) : ℚ) := by
  letI : Fintype (MulAction.orbitRel.Quotient G E) := Fintype.ofFinite _
  exact admissible_extension_orbit_count p hp s hs Quotient.out
    orbitRepresentative_separate (orbitRepresentative_cover p)

include hp in
/-- The full common counting theorem under the paper's equivariant support
hypothesis, with the invariant exact-support action and transversal constructed. -/
theorem order_automorphic_admissible_extension_orbit_count
    [Fintype G] [Fintype X] [Fintype E] [Fintype L] [LocallyFiniteOrder L]
    [DecidableEq E] [DecidableEq L] [DecidableLE L]
    (transport : G → L ≃o L)
    (heq : ∀ (g : G) (x : X), s (g • x) = transport g (s x)) :
    letI : Fintype (MulAction.orbitRel.Quotient G E) := Fintype.ofFinite _
    (Nat.card (MulAction.orbitRel.Quotient G
      (exactSupport s (top_support_invariant s transport heq))) : ℚ) =
      ∑ i : MulAction.orbitRel.Quotient G E,
        (∑ a : MulAction.stabilizer G i.out, ∑ l : L, topMobius l *
          (Nat.card {x : X // p x = i.out ∧ (a : G) • x = x ∧ s x ≤ l} : ℚ)) /
            (Nat.card (MulAction.stabilizer G i.out) : ℚ) :=
  canonical_admissible_extension_orbit_count p hp s (top_support_invariant s transport heq)

end Support

#print axioms stabilizerFiberOrbitMap
#print axioms stabilizerFiberOrbitMap_injective
#print axioms orbitFiberSumMap
#print axioms orbitFiberSumMap_injective
#print axioms orbitFiberSumMap_surjective
#print axioms orbitFiberSumEquiv
#print axioms equivariantOrbitEquiv
#print axioms exactSupportBase_equivariant
#print axioms supportFiberEquiv
#print axioms supportFiberEquiv_equivariant
#print axioms exactSupportOrbitFiberSumEquiv
#print axioms admissible_extension_orbit_count
#print axioms orbitRepresentative_separate
#print axioms orbitRepresentative_cover
#print axioms canonical_admissible_extension_orbit_count
#print axioms order_automorphic_admissible_extension_orbit_count
end MathCompression.SupportCounting
