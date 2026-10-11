import Mathlib.Combinatorics.Enumerative.IncidenceAlgebra
import Mathlib.GroupTheory.GroupAction.Quotient
import Mathlib.GroupTheory.GroupAction.SubMulAction
import Mathlib.Data.Rat.Cast.Order
import Mathlib.SetTheory.Cardinal.Finite

noncomputable section
open scoped BigOperators
open Finset

namespace MathCompression.SupportCounting

variable {L X G : Type*}
variable [PartialOrder L] [OrderTop L] [Fintype L] [LocallyFiniteOrder L]
  [DecidableEq L] [DecidableLE L]

/-- The actual incidence-algebra Möbius coefficient at the greatest element. -/
def topMobius (l : L) : ℚ := IncidenceAlgebra.mu ℚ l ⊤

/-- Möbius inversion detects exact greatest support, not merely bounded support. -/
theorem exact_top_indicator (s : L) :
    (∑ l : L, if s ≤ l then topMobius l else 0) = if s = ⊤ then 1 else 0 := by
  classical
  calc
    _ = ∑ l ∈ Finset.Icc s ⊤, topMobius l := by
      rw [← Finset.sum_filter]
      congr 1
      ext l
      simp
    _ = _ := IncidenceAlgebra.sum_Icc_mu_left s ⊤

/-- Summing the actual indicator over an arbitrary tested finite subset. -/
theorem exact_top_count [Fintype X] (s : X → L) (P : X → Prop) :
    (Nat.card {x : X // P x ∧ s x = ⊤} : ℚ) =
      ∑ l : L, topMobius l * (Nat.card {x : X // P x ∧ s x ≤ l} : ℚ) := by
  classical
  have card_as_sum (Q : X → Prop) :
      (Nat.card {x : X // Q x} : ℚ) = ∑ x : X, if Q x then 1 else 0 := by
    rw [Nat.card_eq_fintype_card, Fintype.card_subtype]
    simp only [Finset.card_eq_sum_ones, Nat.cast_sum, Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro x _
    by_cases h : Q x <;> simp [h]
  simp_rw [card_as_sum, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro x hx
  by_cases hp : P x
  · simp only [hp, true_and]
    simpa [mul_ite] using (exact_top_indicator (s x)).symm
  · simp [hp]


section Actions
variable [Group G] [MulAction G X]

/-- Only the exact-top subset is required to be invariant. Sublevel sets need not be. -/
def exactSupport (s : X → L)
    (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) : SubMulAction G X where
  carrier := {x | s x = ⊤}
  smul_mem' := by intro g x hx; exact hs g x hx

omit [Fintype L] [LocallyFiniteOrder L] [DecidableEq L] [DecidableLE L] in
/-- Order-automorphic transport of support gives the invariant subset actually counted. -/
theorem top_support_invariant (s : X → L) (transport : G → L ≃o L)
    (heq : ∀ (g : G) (x : X), s (g • x) = transport g (s x)) :
    ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤ := by
  intro g x hx
  rw [heq, hx]
  exact (transport g).map_top

/-- Fixed points of the restricted action are precisely fixed ambient points of exact support. -/
def exactSupportFixedEquiv (s : X → L)
    (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) (g : G) :
    MulAction.fixedBy (exactSupport s hs) g ≃
      {x : X // g • x = x ∧ s x = ⊤} where
  toFun x := ⟨x.val.val, congrArg Subtype.val x.property, x.val.property⟩
  invFun x := ⟨⟨x.val, x.property.2⟩, Subtype.ext x.property.1⟩
  left_inv x := by apply Subtype.ext; rfl
  right_inv x := by apply Subtype.ext; rfl

/-- The exact-support fixed-point cardinal is the Möbius weighted sublevel count. -/
theorem exact_support_fixed_count [Fintype X] (s : X → L)
    (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) (g : G) :
    (Nat.card (MulAction.fixedBy (exactSupport s hs) g) : ℚ) =
      ∑ l : L, topMobius l * (Nat.card {x : X // g • x = x ∧ s x ≤ l} : ℚ) := by
  rw [Nat.card_congr (exactSupportFixedEquiv s hs g)]
  exact exact_top_count s (fun x => g • x = x)

/-- The actual finite orbit count, with no sublevel-invariance assumption. -/
theorem exact_support_orbits [Fintype G] [Fintype X] (s : X → L)
    (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) :
    (Nat.card (MulAction.orbitRel.Quotient G (exactSupport s hs)) : ℚ) =
      (∑ g : G, ∑ l : L, topMobius l *
        (Nat.card {x : X // g • x = x ∧ s x ≤ l} : ℚ)) / (Nat.card G : ℚ) := by
  classical
  let Y := exactSupport s hs
  letI : Fintype Y := Fintype.ofFinite Y
  letI : Fintype (MulAction.orbitRel.Quotient G Y) := Fintype.ofFinite _
  letI (g : G) : Fintype (MulAction.fixedBy Y g) := Fintype.ofFinite _
  have hb := MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group G Y
  have hbQ : (∑ g : G, (Nat.card (MulAction.fixedBy Y g) : ℚ)) =
      (Nat.card (MulAction.orbitRel.Quotient G Y) : ℚ) * (Nat.card G : ℚ) := by
    simpa only [Nat.card_eq_fintype_card, Nat.cast_sum, Nat.cast_mul] using
      congrArg (fun n : ℕ => (n : ℚ)) hb
  have hn : (Nat.card G : ℚ) ≠ 0 := by
    simp [Nat.card_eq_fintype_card, Fintype.card_ne_zero]
  apply (eq_div_iff hn).2
  rw [← hbQ]
  apply Finset.sum_congr rfl
  intro g _
  exact exact_support_fixed_count s hs g

/-- UD.ExactSupportOrbits with the paper's order-automorphic support hypothesis. -/
theorem order_automorphic_exact_support_orbits [Fintype G] [Fintype X]
    (s : X → L) (transport : G → L ≃o L)
    (heq : ∀ (g : G) (x : X), s (g • x) = transport g (s x)) :
    (Nat.card (MulAction.orbitRel.Quotient G
      (exactSupport s (top_support_invariant s transport heq))) : ℚ) =
      (∑ g : G, ∑ l : L, topMobius l *
        (Nat.card {x : X // g • x = x ∧ s x ≤ l} : ℚ)) / (Nat.card G : ℚ) :=
  exact_support_orbits s (top_support_invariant s transport heq)


section Fibers
variable {E : Type*} [MulAction G E]

/-- The actual extension fiber is stable under the stabilizer of its base. -/
def extensionFiber (p : X → E)
    (hp : ∀ (g : G) (x : X), p (g • x) = g • p x) (e : E) :
    SubMulAction (MulAction.stabilizer G e) X where
  carrier := {x | p x = e}
  smul_mem' := by
    intro g x hx
    change p ((g : G) • x) = e
    rw [hp, hx]
    exact g.property

omit [Fintype L] [LocallyFiniteOrder L] [DecidableEq L] [DecidableLE L] in
/-- Ambient exact support is invariant on the actual stabilizer fiber. -/
theorem fiber_top_invariant (p : X → E)
    (hp : ∀ (g : G) (x : X), p (g • x) = g • p x) (e : E)
    (s : X → L) (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) :
    ∀ (a : MulAction.stabilizer G e) (z : extensionFiber p hp e),
      s z.val = ⊤ → s (a • z).val = ⊤ := by
  intro a z hz
  exact hs a.val z.val hz

/-- The sublevel count in a fiber uses ambient fixed points and the exact base condition. -/
def fiberSublevelEquiv (p : X → E)
    (hp : ∀ (g : G) (x : X), p (g • x) = g • p x) (e : E)
    (s : X → L) (a : MulAction.stabilizer G e) (l : L) :
    {z : extensionFiber p hp e // a • z = z ∧ s z.val ≤ l} ≃
      {x : X // p x = e ∧ (a : G) • x = x ∧ s x ≤ l} where
  toFun z := ⟨z.val.val, z.val.property, congrArg Subtype.val z.property.1, z.property.2⟩
  invFun x := ⟨⟨x.val, x.property.1⟩, Subtype.ext x.property.2.1, x.property.2.2⟩
  left_inv x := by apply Subtype.ext; rfl
  right_inv x := by apply Subtype.ext; rfl

/-- UD.AdmissibleExtensions' complete Möbius/Burnside summand over one base representative.
The finite ambient action may already be the admissible subset R. -/
theorem admissible_extension_fiber_count [Fintype G] [Fintype X] [DecidableEq E]
    (p : X → E) (hp : ∀ (g : G) (x : X), p (g • x) = g • p x) (e : E)
    (s : X → L) (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤) :
    (Nat.card (MulAction.orbitRel.Quotient (MulAction.stabilizer G e)
      (exactSupport (fun z : extensionFiber p hp e => s z.val)
        (fiber_top_invariant p hp e s hs))) : ℚ) =
      (∑ a : MulAction.stabilizer G e, ∑ l : L, topMobius l *
        (Nat.card {x : X // p x = e ∧ (a : G) • x = x ∧ s x ≤ l} : ℚ)) /
          (Nat.card (MulAction.stabilizer G e) : ℚ) := by
  classical
  rw [exact_support_orbits]
  congr 1
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro l _
  rw [Nat.card_congr (fiberSublevelEquiv p hp e s a l)]


/-- Sum the proved stabilizer-fiber counts over any finite set of base representatives.
Selecting one representative of every relevant base orbit supplies precisely the
numerical right side of UD.AdmissibleExtensions. -/
theorem admissible_extension_fiber_sum [Fintype G] [Fintype X] [DecidableEq E]
    (p : X → E) (hp : ∀ (g : G) (x : X), p (g • x) = g • p x)
    (s : X → L) (hs : ∀ (g : G) (x : X), s x = ⊤ → s (g • x) = ⊤)
    (representatives : Finset E) :
    (∑ e ∈ representatives,
      (Nat.card (MulAction.orbitRel.Quotient (MulAction.stabilizer G e)
        (exactSupport (fun z : extensionFiber p hp e => s z.val)
          (fiber_top_invariant p hp e s hs))) : ℚ)) =
      ∑ e ∈ representatives,
        (∑ a : MulAction.stabilizer G e, ∑ l : L, topMobius l *
          (Nat.card {x : X // p x = e ∧ (a : G) • x = x ∧ s x ≤ l} : ℚ)) /
            (Nat.card (MulAction.stabilizer G e) : ℚ) := by
  apply Finset.sum_congr rfl
  intro e _
  exact admissible_extension_fiber_count p hp e s hs

end Fibers
end Actions

#print axioms exact_top_indicator
#print axioms exact_top_count
#print axioms top_support_invariant
#print axioms exactSupportFixedEquiv
#print axioms exact_support_fixed_count
#print axioms exact_support_orbits
#print axioms order_automorphic_exact_support_orbits
#print axioms extensionFiber
#print axioms fiber_top_invariant
#print axioms fiberSublevelEquiv
#print axioms admissible_extension_fiber_count
#print axioms admissible_extension_fiber_sum

end MathCompression.SupportCounting


