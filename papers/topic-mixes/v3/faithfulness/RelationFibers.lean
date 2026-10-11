import Mathlib.GroupTheory.GroupAction.Basic

/-! Formal scope: common refinements, jointly separating maps, transporter
    membership, and the two-coordinate parity step. No graph classification
    or assertion about a source theorem is assumed or formalized here. -/
namespace RelationFibers

def Common {I X : Type*} (R : I → X → X → Prop) (x y : X) : Prop :=
  ∀ i, R i x y

def Separating {I X : Type*} (R : I → X → X → Prop) : Prop :=
  ∀ x y, Common R x y → x = y

theorem common_maps_jointly_separate {I J X : Type*} {Y : J → Type*}
    (R : I → X → X → Prop) (S : (j : J) → I → Y j → Y j → Prop)
    (f : (j : J) → X → Y j)
    (hpres : ∀ j i x y, R i x y → S j i (f j x) (f j y))
    (hsep : ∀ j, Separating (S j))
    (hinj : Function.Injective (fun x j => f j x)) : Separating R := by
  intro x y hxy
  apply hinj
  funext j
  exact hsep j (f j x) (f j y) (fun i => hpres j i x y (hxy i))

theorem separates_of_injective_on_one_class {I X Y : Type*}
    (R : I → X → X → Prop) (S : I → Y → Y → Prop) (f : X → Y)
    (hpres : ∀ i x y, R i x y → S i (f x) (f y))
    (hsep : Separating S) (j : I)
    (hinj : ∀ x y, R j x y → f x = f y → x = y) : Separating R := by
  intro x y hxy
  exact hinj x y (hxy j) (hsep (f x) (f y) (fun i => hpres i x y (hxy i)))

section Transport
variable {G I X : Type*} [Group G] [MulAction G X]

/-- Left-action convention: a transporter is a right coset of the class
stabilizer. The manuscript uses the equivalent right-action convention. -/
theorem transporter_membership
    (R : X → X → Prop) (hR : Equivalence R)
    (hpres : ∀ (g : G) x y, R x y → R (g • x) (g • y))
    (x y : X) (τ g : G) (hτ : R (τ • y) x) :
    R (g • y) x ↔ R ((g * τ⁻¹) • x) x := by
  have h : R (g • y) ((g * τ⁻¹) • x) := by
    simpa only [mul_smul, inv_smul_smul] using hpres (g * τ⁻¹) (τ • y) x hτ
  constructor
  · intro hg
    exact hR.trans (hR.symm h) hg
  · intro hg
    exact hR.trans h hg

theorem common_transporter_membership
    (R : I → X → X → Prop) (hR : ∀ i, Equivalence (R i))
    (hpres : ∀ i (g : G) x y, R i x y → R i (g • x) (g • y))
    (x y : X) (τ : I → G) (g : G)
    (hτ : ∀ i, R i (τ i • y) x) :
    Common R (g • y) x ↔ ∀ i, R i ((g * (τ i)⁻¹) • x) x := by
  constructor
  · intro h i
    exact (transporter_membership (R i) (hR i) (hpres i) x y (τ i) g (hτ i)).mp (h i)
  · intro h i
    exact (transporter_membership (R i) (hR i) (hpres i) x y (τ i) g (hτ i)).mpr (h i)

theorem common_nonempty_transporter_is_coset
    (R : I → X → X → Prop) (hR : ∀ i, Equivalence (R i))
    (hpres : ∀ i (g : G) x y, R i x y → R i (g • x) (g • y))
    (x y : X) (g₀ g : G) (h₀ : Common R (g₀ • y) x) :
    Common R (g • y) x ↔ Common R ((g * g₀⁻¹) • x) x := by
  exact common_transporter_membership R hR hpres x y (fun _ => g₀) g h₀
end Transport

/-- The actual parity exclusion used by the thin-mix argument. -/
theorem equal_color_forces_matched_choice {X Y C : Type*}
    (cx : X → C) (cy : Y → C) (x x' u : X) (y y' v : Y)
    (h00 : cx x = cy y) (h11 : cx x' = cy y')
    (hdiff : cx x ≠ cx x') (hu : u = x ∨ u = x')
    (hv : v = y ∨ v = y') (heq : cx u = cy v) :
    (u = x ∧ v = y) ∨ (u = x' ∧ v = y') := by
  rcases hu with rfl | rfl
  · rcases hv with rfl | rfl
    · exact Or.inl ⟨rfl, rfl⟩
    · exact False.elim (hdiff (heq.trans h11.symm))
  · rcases hv with rfl | rfl
    · exact False.elim (hdiff (h00.trans heq.symm))
    · exact Or.inr ⟨rfl, rfl⟩

#print axioms common_maps_jointly_separate
#print axioms separates_of_injective_on_one_class
#print axioms transporter_membership
#print axioms common_transporter_membership
#print axioms common_nonempty_transporter_is_coset
#print axioms equal_color_forces_matched_choice
end RelationFibers
