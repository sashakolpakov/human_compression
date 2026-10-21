import Lean

/- The covering criterion from the existing written phase4 shadow argument.
   This formalizes that criterion only, not the sporadic census or coset algorithm. -/
namespace HumanCompression.ShadowCover

variable {X I : Type}

def Flag (inc : X → X → Prop) (C : X → Prop) : Prop :=
  ∀ v, C v → ∀ w, C w → inc v w

def Shadow (inc : X → X → Prop) (type : X → I)
    (i : I) (C : X → Prop) (y : X) : Prop :=
  type y = i ∧ ∀ v, C v → inc y v

def Eligible (inc : X → X → Prop) (type : X → I)
    (i : I) (U S : X → Prop) (v : X) : Prop :=
  type v ≠ i ∧ (∀ u, U u → inc v u) ∧ (∀ s, S s → inc s v)

def Witness (inc : X → X → Prop) (type : X → I)
    (i : I) (U S C : X → Prop) : Prop :=
  Flag inc C ∧ (∀ v, C v → ∀ u, U u → inc v u) ∧
    ∀ y, Shadow inc type i C y ↔ S y

def Cover (inc : X → X → Prop) (type : X → I)
    (i : I) (U S C : X → Prop) : Prop :=
  Flag inc C ∧ (∀ v, C v → Eligible inc type i U S v) ∧
    ∀ y, type y = i → ¬ S y → ∃ v, C v ∧ ¬ inc y v

theorem witness_avoids_type
    (inc : X → X → Prop) (type : X → I) (i : I) (U S C : X → Prop)
    (same_type : ∀ a b, type a = type b → inc a b → a = b)
    (p q : X) (hp : S p) (hq : S q) (hne : p ≠ q)
    (h : Witness inc type i U S C) :
    ∀ v, C v → type v ≠ i := by
  intro v hv hvi
  have sp := (h.2.2 p).mpr hp
  have sq := (h.2.2 q).mpr hq
  have epv : p = v := same_type p v (sp.1.trans hvi.symm) (sp.2 v hv)
  have eqv : q = v := same_type q v (sq.1.trans hvi.symm) (sq.2 v hv)
  exact hne (epv.trans eqv.symm)

theorem witness_implies_cover
    (inc : X → X → Prop) (type : X → I) (i : I) (U S C : X → Prop)
    (same_type : ∀ a b, type a = type b → inc a b → a = b)
    (p q : X) (hp : S p) (hq : S q) (hne : p ≠ q)
    (h : Witness inc type i U S C) : Cover inc type i U S C := by
  classical
  refine ⟨h.1, ?_, ?_⟩
  · intro v hv
    refine ⟨witness_avoids_type inc type i U S C same_type p q hp hq hne h v hv,
      h.2.1 v hv, ?_⟩
    intro s hs
    exact ((h.2.2 s).mpr hs).2 v hv
  · intro y hy hny
    by_cases hex : ∃ v, C v ∧ ¬ inc y v
    · exact hex
    · exfalso
      apply hny
      apply (h.2.2 y).mp
      refine ⟨hy, ?_⟩
      intro v hv
      exact Classical.byContradiction (fun hn => hex ⟨v, hv, hn⟩)

theorem cover_implies_witness
    (inc : X → X → Prop) (type : X → I) (i : I) (U S C : X → Prop)
    (typed : ∀ s, S s → type s = i)
    (h : Cover inc type i U S C) : Witness inc type i U S C := by
  classical
  refine ⟨h.1, ?_, ?_⟩
  · intro v hv
    exact (h.2.1 v hv).2.1
  · intro y
    constructor
    · intro sy
      by_cases hs : S y
      · exact hs
      · obtain ⟨v, hv, hn⟩ := h.2.2 y sy.1 hs
        exact False.elim (hn (sy.2 v hv))
    · intro hs
      refine ⟨typed y hs, ?_⟩
      intro v hv
      exact (h.2.1 v hv).2.2 y hs

theorem exact_covering_criterion
    (inc : X → X → Prop) (type : X → I) (i : I) (U S C : X → Prop)
    (same_type : ∀ a b, type a = type b → inc a b → a = b)
    (typed : ∀ s, S s → type s = i)
    (p q : X) (hp : S p) (hq : S q) (hne : p ≠ q) :
    Witness inc type i U S C ↔ Cover inc type i U S C :=
  ⟨witness_implies_cover inc type i U S C same_type p q hp hq hne,
    cover_implies_witness inc type i U S C typed⟩

#print axioms witness_avoids_type
#print axioms witness_implies_cover
#print axioms cover_implies_witness
#print axioms exact_covering_criterion

end HumanCompression.ShadowCover
