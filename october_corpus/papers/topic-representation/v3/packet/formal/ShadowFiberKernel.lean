import Mathlib.Algebra.Group.End
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
The pointwise kernel in a typed incidence extension whose new-new
incidence depends only on distinctness of new types. The signature of a
new object is its type and its complete old-object shadow.
-/

namespace HumanCompression.ShadowFiberKernel

variable {Q B : Type*}

def fiberGroup (f : Q → B) : Subgroup (Equiv.Perm Q) where
  carrier := {g | ∀ q, f (g q) = f q}
  one_mem' := by intro q; rfl
  mul_mem' := by
    intro g h hg hh q
    exact (hg (h q)).trans (hh q)
  inv_mem' := by
    intro g hg q
    simpa using (hg (g⁻¹ q)).symm

def restrictFiber (f : Q → B) (g : fiberGroup f) (b : B) :
    Equiv.Perm {q // f q = b} :=
  g.val.subtypePerm (fun q => by rw [g.property q])

def assembleFiber (f : Q → B) (g : ∀ b, Equiv.Perm {q // f q = b}) :
    fiberGroup f :=
  ⟨Equiv.ofFiberEquiv g, Equiv.ofFiberEquiv_map g⟩

def fiberGroupEquiv (f : Q → B) :
    fiberGroup f ≃* (∀ b, Equiv.Perm {q // f q = b}) where
  toFun := restrictFiber f
  invFun := assembleFiber f
  left_inv := by
    intro g
    apply Subtype.ext
    ext q
    rfl
  right_inv := by
    intro g
    funext b
    ext ⟨q, h⟩
    subst b
    rfl
  map_mul' := by
    intro g h
    funext b
    ext q
    rfl

theorem fiberGroup_trivial_iff (f : Q → B) :
    (∀ g : fiberGroup f, g = 1) ↔ Function.Injective f := by
  classical
  constructor
  · intro h x y hxy
    have hm : Equiv.swap x y ∈ fiberGroup f := by
      intro q
      by_cases hx : q = x
      · subst q; simpa using hxy.symm
      by_cases hy : q = y
      · subst q; simpa using hxy
      simp [Equiv.swap_apply_of_ne_of_ne hx hy]
    have hh := congrArg (fun g : fiberGroup f => g.val x) (h ⟨Equiv.swap x y, hm⟩)
    simpa using hh.symm
  · intro h g
    apply Subtype.ext
    ext q
    exact h (g.property q)

section Incidence

variable {P J : Type*}

def color (c : Q → J) : P ⊕ Q → Option J
  | .inl _ => none
  | .inr q => some (c q)

def incidence (R : P → P → Prop) (c : Q → J) (s : Q → Set P) :
    P ⊕ Q → P ⊕ Q → Prop
  | .inl p, .inl p' => R p p'
  | .inl p, .inr q => p ∈ s q
  | .inr q, .inl p => p ∈ s q
  | .inr q, .inr q' => c q ≠ c q'

def signature (c : Q → J) (s : Q → Set P) (q : Q) : J × Set P := (c q, s q)

def pointwiseKernel (R : P → P → Prop) (c : Q → J) (s : Q → Set P) :
    Subgroup (Equiv.Perm (P ⊕ Q)) where
  carrier := {g | (∀ p, g (.inl p) = .inl p) ∧
    (∀ x, color c (g x) = color c x) ∧
    ∀ x y, incidence R c s (g x) (g y) ↔ incidence R c s x y}
  one_mem' := by exact ⟨fun _ => rfl, fun _ => rfl, fun _ _ => Iff.rfl⟩
  mul_mem' := by
    rintro g h ⟨gp, gc, gi⟩ ⟨hp, hc, hi⟩
    exact ⟨fun p => by simpa [hp p] using gp p,
      fun x => (gc (h x)).trans (hc x),
      fun x y => (gi (h x) (h y)).trans (hi x y)⟩
  inv_mem' := by
    rintro g ⟨gp, gc, gi⟩
    refine ⟨?_, ?_, ?_⟩
    · intro p
      apply g.injective
      simpa using (gp p).symm
    · intro x
      simpa using (gc (g⁻¹ x)).symm
    · intro x y
      simpa using (gi (g⁻¹ x) (g⁻¹ y)).symm

def extend (g : Equiv.Perm Q) : Equiv.Perm (P ⊕ Q) :=
  Equiv.sumCongr (Equiv.refl P) g

theorem extend_mem_iff (R : P → P → Prop) (c : Q → J) (s : Q → Set P)
    (g : Equiv.Perm Q) :
    extend g ∈ pointwiseKernel R c s ↔ g ∈ fiberGroup (signature c s) := by
  constructor
  · rintro ⟨_, hc, hi⟩ q
    have ct : c (g q) = c q := by
      simpa [extend, color] using hc (.inr q)
    have sh : s (g q) = s q := by
      ext p
      simpa [extend, incidence] using hi (.inl p) (.inr q)
    exact Prod.ext ct sh
  · intro h
    have ct (q) : c (g q) = c q := congrArg Prod.fst (h q)
    have sh (q) : s (g q) = s q := congrArg Prod.snd (h q)
    refine ⟨fun _ => rfl, ?_, ?_⟩
    · intro x
      cases x <;> simp [extend, color, ct]
    · intro x y
      cases x <;> cases y <;> simp [extend, incidence, ct, sh]

theorem exists_extend (g : Equiv.Perm (P ⊕ Q))
    (fixes : ∀ p, g (.inl p) = .inl p) :
    ∃ h : Equiv.Perm Q, extend h = g := by
  classical
  have hn (q : Q) : ∃ r, g (.inr q) = .inr r := by
    cases he : g (.inr q) with
    | inr r => exact ⟨r, rfl⟩
    | inl p =>
      have hh : g (.inr q) = g (.inl p) := he.trans (fixes p).symm
      have := g.injective hh
      contradiction
  let h : Q → Q := fun q => Classical.choose (hn q)
  have hs (q : Q) : g (.inr q) = .inr (h q) := Classical.choose_spec (hn q)
  have hinj : Function.Injective h := by
    intro x y he
    apply Sum.inr.inj
    apply g.injective
    rw [hs, hs, he]
  have hsurj : Function.Surjective h := by
    intro y
    obtain ⟨x, hx⟩ := g.surjective (.inr y)
    cases x with
    | inl p => simpa [fixes] using hx
    | inr q =>
      refine ⟨q, ?_⟩
      apply Sum.inr.inj
      exact (hs q).symm.trans hx
  refine ⟨Equiv.ofBijective h ⟨hinj, hsurj⟩, ?_⟩
  ext x
  cases x with
  | inl p => exact (fixes p).symm
  | inr q => exact (hs q).symm

def extendHom (R : P → P → Prop) (c : Q → J) (s : Q → Set P) :
    fiberGroup (signature c s) →* pointwiseKernel R c s where
  toFun g := ⟨extend g.val, (extend_mem_iff R c s g.val).mpr g.property⟩
  map_one' := by apply Subtype.ext; ext x; cases x <;> rfl
  map_mul' := by intro g h; apply Subtype.ext; ext x; cases x <;> rfl

theorem extendHom_bijective (R : P → P → Prop) (c : Q → J) (s : Q → Set P) :
    Function.Bijective (extendHom R c s) := by
  constructor
  · intro g h he
    apply Subtype.ext
    ext q
    have hp := congrArg (fun k : pointwiseKernel R c s => k.val (.inr q)) he
    exact Sum.inr.inj hp
  · intro g
    obtain ⟨h, hh⟩ := exists_extend g.val g.property.1
    have hm : h ∈ fiberGroup (signature c s) :=
      (extend_mem_iff R c s h).mp (hh ▸ g.property)
    exact ⟨⟨h, hm⟩, Subtype.ext hh⟩

noncomputable def pointwiseKernelEquiv (R : P → P → Prop) (c : Q → J)
    (s : Q → Set P) :
    pointwiseKernel R c s ≃*
      (∀ b : J × Set P, Equiv.Perm {q // signature c s q = b}) :=
  (MulEquiv.ofBijective (extendHom R c s) (extendHom_bijective R c s)).symm.trans
    (fiberGroupEquiv (signature c s))

theorem pointwiseKernel_trivial_iff (R : P → P → Prop) (c : Q → J)
    (s : Q → Set P) :
    (∀ g : pointwiseKernel R c s, g = 1) ↔ Function.Injective (signature c s) := by
  rw [← fiberGroup_trivial_iff]
  constructor
  · intro h g
    apply (extendHom_bijective R c s).injective
    rw [map_one]
    exact h _
  · intro h g
    obtain ⟨k, rfl⟩ := (extendHom_bijective R c s).surjective g
    rw [h k, map_one]

end Incidence

#print axioms fiberGroupEquiv
#print axioms fiberGroup_trivial_iff
#print axioms extend_mem_iff
#print axioms exists_extend
#print axioms extendHom_bijective
#print axioms pointwiseKernelEquiv
#print axioms pointwiseKernel_trivial_iff

end HumanCompression.ShadowFiberKernel
