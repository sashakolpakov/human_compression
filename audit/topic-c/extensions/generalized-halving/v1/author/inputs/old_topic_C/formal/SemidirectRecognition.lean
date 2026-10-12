import Mathlib.GroupTheory.SemidirectProduct
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic

/-!
An explicit inverse for a semidirect-product presentation.
The component homomorphisms and their covariance are actual hypotheses;
generation is expressed as a subgroup closure. No order or finiteness
hypothesis is used. The augmentation basis and the source-specific cyclic
instance remain separate written arguments.

This uses mathlib's SemidirectProduct.lift; no priority claim is made for
the standard semidirect-product universal property.
-/

namespace HumanCompression.SemidirectRecognition

variable {N H P : Type*} [Group N] [Group H] [Group P]
variable {φ : H →* MulAut N}
variable (f : N →* P) (j : H →* P)
variable (hc : ∀ h, f.comp (φ h).toMonoidHom =
  (MulAut.conj (j h)).toMonoidHom.comp f)

/-- The inverse candidate has the literal formula f(n) * j(h). -/
def inverseMap : N ⋊[φ] H →* P := SemidirectProduct.lift f j hc

theorem inverseMap_apply (v : N ⋊[φ] H) :
    inverseMap f j hc v = f v.left * j v.right := rfl

theorem inverseMap_surjective
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤) :
    Function.Surjective (inverseMap f j hc) := by
  have hle : Subgroup.closure (Set.range f ∪ Set.range j) ≤
      (inverseMap f j hc).range := by
    apply (Subgroup.closure_le _).mpr
    intro x hx
    rcases hx with ⟨n, rfl⟩ | ⟨h, rfl⟩
    · exact ⟨SemidirectProduct.inl n, SemidirectProduct.lift_inl f j hc n⟩
    · exact ⟨SemidirectProduct.inr h, SemidirectProduct.lift_inr f j hc h⟩
  intro p
  exact hle (hgen ▸ Subgroup.mem_top p)

variable (q : P →* N ⋊[φ] H)
variable (hf : ∀ n, q (f n) = SemidirectProduct.inl n)
variable (hj : ∀ h, q (j h) = SemidirectProduct.inr h)

include hf hj in
theorem forward_inverse (v : N ⋊[φ] H) :
    q (inverseMap f j hc v) = v := by
  rw [inverseMap_apply, map_mul, hf, hj]
  exact SemidirectProduct.inl_left_mul_inr_right v

include hf hj in
theorem inverse_forward
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤) (p : P) :
    inverseMap f j hc (q p) = p := by
  obtain ⟨v, rfl⟩ := inverseMap_surjective f j hc hgen p
  rw [forward_inverse f j hc q hf hj]

/-- The actual inverse map, rather than a cardinality argument, gives the equivalence. -/
def recognitionEquiv
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤) :
    P ≃* N ⋊[φ] H where
  toFun := q
  invFun := inverseMap f j hc
  left_inv := inverse_forward f j hc q hf hj hgen
  right_inv := forward_inverse f j hc q hf hj
  map_mul' := q.map_mul

theorem recognitionEquiv_symm_apply
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤)
    (v : N ⋊[φ] H) :
    (recognitionEquiv f j hc q hf hj hgen).symm v = f v.left * j v.right := rfl

theorem recognitionEquiv_inl
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤) (n : N) :
    (recognitionEquiv f j hc q hf hj hgen).symm (SemidirectProduct.inl n) = f n :=
  SemidirectProduct.lift_inl f j hc n

theorem recognitionEquiv_inr
    (hgen : Subgroup.closure (Set.range f ∪ Set.range j) = ⊤) (h : H) :
    (recognitionEquiv f j hc q hf hj hgen).symm (SemidirectProduct.inr h) = j h :=
  SemidirectProduct.lift_inr f j hc h

#print axioms inverseMap
#print axioms inverseMap_apply
#print axioms inverseMap_surjective
#print axioms forward_inverse
#print axioms inverse_forward
#print axioms recognitionEquiv
#print axioms recognitionEquiv_symm_apply
#print axioms recognitionEquiv_inl
#print axioms recognitionEquiv_inr

end HumanCompression.SemidirectRecognition
