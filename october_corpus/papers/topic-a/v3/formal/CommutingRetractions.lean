import Mathlib.Algebra.Group.Subgroup.Ker
import Mathlib.Algebra.Group.Equiv.Basic
import Mathlib.Tactic

/-!
Two commuting retractions identify a group, modulo their common kernel,
with the full group of compatible pairs in their ranges. The preimage of
(x,y), with common image c, is the explicit element x*c⁻¹*y.
No finite group order or generation of the compatible product is assumed.
-/

namespace HumanCompression.CommutingRetractions

variable {G : Type*} [Group G]

def compatiblePairs (e f : G →* G) : Subgroup (G × G) where
  carrier := {p | e p.1 = p.1 ∧ f p.2 = p.2 ∧ f p.1 = e p.2}
  one_mem' := by simp
  mul_mem' := by
    intro a b ha hb
    exact ⟨by simp only [Prod.fst_mul, map_mul, ha.1, hb.1],
      by simp only [Prod.snd_mul, map_mul, ha.2.1, hb.2.1],
      by simp only [Prod.fst_mul, Prod.snd_mul, map_mul, ha.2.2, hb.2.2]⟩
  inv_mem' := by
    intro a ha
    exact ⟨by simp only [Prod.fst_inv, map_inv, ha.1],
      by simp only [Prod.snd_inv, map_inv, ha.2.1],
      by simp only [Prod.fst_inv, Prod.snd_inv, map_inv, ha.2.2]⟩

def pairMap (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) : G →* compatiblePairs e f where
  toFun g := ⟨(e g, f g), by
    refine ⟨?_, ?_, ?_⟩
    · exact congrArg (fun h : G →* G => h g) he
    · exact congrArg (fun h : G →* G => h g) hf
    · exact congrArg (fun h : G →* G => h g) hcomm.symm⟩
  map_one' := by apply Subtype.ext; exact Prod.ext (map_one e) (map_one f)
  map_mul' a b := by apply Subtype.ext; exact Prod.ext (map_mul e a b) (map_mul f a b)

/-- An explicit preimage, using multiplication in the original group. -/
def liftPair (e f : G →* G) (p : compatiblePairs e f) : G :=
  p.val.1 * (e p.val.2)⁻¹ * p.val.2

theorem first_lift (e f : G →* G) (he : e.comp e = e)
    (p : compatiblePairs e f) : e (liftPair e f p) = p.val.1 := by
  have hee : e (e p.val.2) = e p.val.2 :=
    congrArg (fun h : G →* G => h p.val.2) he
  simp only [liftPair, map_mul, map_inv, p.property.1, hee]
  group

theorem second_lift (e f : G →* G) (hcomm : e.comp f = f.comp e)
    (p : compatiblePairs e f) : f (liftPair e f p) = p.val.2 := by
  have hfe : f (e p.val.2) = e p.val.2 := by
    simpa only [MonoidHom.comp_apply, p.property.2.1] using
      congrArg (fun h : G →* G => h p.val.2) hcomm.symm
  simp only [liftPair, map_mul, map_inv, p.property.2.2, hfe, p.property.2.1]
  group

theorem pairMap_liftPair (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) (p : compatiblePairs e f) :
    pairMap e f he hf hcomm (liftPair e f p) = p := by
  apply Subtype.ext
  exact Prod.ext (first_lift e f he p) (second_lift e f hcomm p)

theorem pairMap_surjective (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) :
    Function.Surjective (pairMap e f he hf hcomm) := by
  intro p
  exact ⟨liftPair e f p, pairMap_liftPair e f he hf hcomm p⟩

theorem pairMap_kernel (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) :
    (pairMap e f he hf hcomm).ker = e.ker ⊓ f.ker := by
  ext g
  change (pairMap e f he hf hcomm g = 1) ↔ e g = 1 ∧ f g = 1
  constructor
  · intro h
    have hp : (e g, f g) = (1, 1) := congrArg Subtype.val h
    exact ⟨congrArg Prod.fst hp, congrArg Prod.snd hp⟩
  · rintro ⟨he1, hf1⟩
    apply Subtype.ext
    exact Prod.ext he1 hf1

theorem pairMap_injective (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) (hker : e.ker ⊓ f.ker = ⊥) :
    Function.Injective (pairMap e f he hf hcomm) := by
  apply (MonoidHom.ker_eq_bot_iff _).mp
  rw [pairMap_kernel, hker]

/-- The inverse of this isomorphism is the displayed lift. -/
def pairEquiv (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) (hker : e.ker ⊓ f.ker = ⊥) :
    G ≃* compatiblePairs e f where
  toFun := pairMap e f he hf hcomm
  invFun := liftPair e f
  left_inv g := by
    apply pairMap_injective e f he hf hcomm hker
    exact pairMap_liftPair e f he hf hcomm _
  right_inv := pairMap_liftPair e f he hf hcomm
  map_mul' := (pairMap e f he hf hcomm).map_mul

theorem pairEquiv_symm_apply (e f : G →* G)
    (he : e.comp e = e) (hf : f.comp f = f)
    (hcomm : e.comp f = f.comp e) (hker : e.ker ⊓ f.ker = ⊥)
    (p : compatiblePairs e f) :
    (pairEquiv e f he hf hcomm hker).symm p = p.val.1 * (e p.val.2)⁻¹ * p.val.2 := rfl

#print axioms compatiblePairs
#print axioms pairMap
#print axioms liftPair
#print axioms first_lift
#print axioms second_lift
#print axioms pairMap_liftPair
#print axioms pairMap_surjective
#print axioms pairMap_kernel
#print axioms pairMap_injective
#print axioms pairEquiv
#print axioms pairEquiv_symm_apply

end HumanCompression.CommutingRetractions
