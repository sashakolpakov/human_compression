import Mathlib.Tactic

/-! The generic restriction/extension interface for recognizable constructions.
The vertex recognition, graph incidence, palette recognition and every concrete
extension formula are hypotheses to be discharged in the written application.
No arbitrary finite-group incidence representation is formalized here. -/

namespace HumanCompression.RecognizableRestriction

variable {X Y : Type*} (ι : X ↪ Y)
variable (G : Subgroup (Equiv.Perm Y)) (H : Subgroup (Equiv.Perm X))

/-- A chosen restriction, together with its actual action on the retained copy.
Multiplicativity is a conclusion below, not a field of this structure. -/
structure Data where
  restrict : G → H
  commutes : ∀ (g : G) (x : X),
    ι ((restrict g : Equiv.Perm X) x) = (g : Equiv.Perm Y) (ι x)

variable {ι G H} (D : Data ι G H)

/-- Restriction of actual permutations is automatically a homomorphism. -/
def restrictionHom : G →* H where
  toFun := D.restrict
  map_one' := by
    apply Subtype.ext
    apply Equiv.ext
    intro x
    apply ι.injective
    simpa using D.commutes (1 : G) x
  map_mul' a b := by
    apply Subtype.ext
    apply Equiv.ext
    intro x
    apply ι.injective
    calc
      ι ((D.restrict (a * b) : Equiv.Perm X) x) =
          ((a * b : G) : Equiv.Perm Y) (ι x) := D.commutes (a * b) x
      _ = (a : Equiv.Perm Y) ((b : Equiv.Perm Y) (ι x)) := rfl
      _ = (a : Equiv.Perm Y) (ι ((D.restrict b : Equiv.Perm X) x)) :=
          congrArg (a : Equiv.Perm Y) (D.commutes b x).symm
      _ = ι ((D.restrict a : Equiv.Perm X) ((D.restrict b : Equiv.Perm X) x)) :=
          (D.commutes a _).symm

theorem restriction_unique (D' : Data ι G H) (g : G) :
    D.restrict g = D'.restrict g := by
  apply Subtype.ext
  apply Equiv.ext
  intro x
  apply ι.injective
  exact (D.commutes g x).trans (D'.commutes g x).symm

theorem restrict_eq_one_iff (g : G) :
    D.restrict g = 1 ↔ ∀ x, (g : Equiv.Perm Y) (ι x) = ι x := by
  constructor
  · intro h x
    simpa [h] using (D.commutes g x).symm
  · intro h
    apply Subtype.ext
    apply Equiv.ext
    intro x
    apply ι.injective
    simpa using (D.commutes g x).trans (h x)

/-- Pointwise rigidity on the retained copy kills the actual restriction kernel. -/
theorem restriction_injective
    (rigid : ∀ g : G, (∀ x, (g : Equiv.Perm Y) (ι x) = ι x) → g = 1) :
    Function.Injective (restrictionHom D) := by
  apply (restrictionHom D).ker_eq_bot_iff.mp
  apply le_antisymm
  · intro g hg
    change g = 1
    exact rigid g (((restrict_eq_one_iff D) g).mp hg)
  · exact bot_le

/-- Existence of genuine vertex extensions makes the restriction surjective. -/
theorem restriction_surjective
    (extend : ∀ h : H, ∃ g : G,
      ∀ x, (g : Equiv.Perm Y) (ι x) = ι ((h : Equiv.Perm X) x)) :
    Function.Surjective (restrictionHom D) := by
  intro h
  obtain ⟨g, hg⟩ := extend h
  refine ⟨g, ?_⟩
  apply Subtype.ext
  apply Equiv.ext
  intro x
  apply ι.injective
  exact (D.commutes g x).trans (hg x)

noncomputable def recognitionEquiv
    (rigid : ∀ g : G, (∀ x, (g : Equiv.Perm Y) (ι x) = ι x) → g = 1)
    (extend : ∀ h : H, ∃ g : G,
      ∀ x, (g : Equiv.Perm Y) (ι x) = ι ((h : Equiv.Perm X) x)) : G ≃* H :=
  MulEquiv.ofBijective (restrictionHom D)
    ⟨(restriction_injective D) rigid, (restriction_surjective D) extend⟩

/-- The distinguished subgroup is transported exactly under the pair hypothesis. -/
theorem distinguished_subgroup_map
    (rigid : ∀ g : G, (∀ x, (g : Equiv.Perm Y) (ι x) = ι x) → g = 1)
    (extend : ∀ h : H, ∃ g : G,
      ∀ x, (g : Equiv.Perm Y) (ι x) = ι ((h : Equiv.Perm X) x))
    (K : Subgroup G) (L : Subgroup H)
    (compatible : ∀ g, g ∈ K ↔ D.restrict g ∈ L) :
    K.map ((recognitionEquiv D) rigid extend).toMonoidHom = L := by
  ext h
  constructor
  · rintro ⟨g, hg, rfl⟩
    exact (compatible g).mp hg
  · intro hh
    obtain ⟨g, hg⟩ := (restriction_surjective D) extend h
    refine ⟨g, ?_, hg⟩
    apply (compatible g).mpr
    simpa only [show D.restrict g = h from hg] using hh

/-- Existence of restriction maps, not their choice, is the mathematical input. -/
noncomputable def dataOfRestriction
    (restriction_exists : ∀ g : G, ∃ h : H,
      ∀ x, ι ((h : Equiv.Perm X) x) = (g : Equiv.Perm Y) (ι x)) : Data ι G H where
  restrict g := Classical.choose (restriction_exists g)
  commutes g := Classical.choose_spec (restriction_exists g)

#print axioms restrictionHom
#print axioms restriction_unique
#print axioms restrict_eq_one_iff
#print axioms restriction_injective
#print axioms restriction_surjective
#print axioms recognitionEquiv
#print axioms distinguished_subgroup_map
#print axioms dataOfRestriction

end HumanCompression.RecognizableRestriction
