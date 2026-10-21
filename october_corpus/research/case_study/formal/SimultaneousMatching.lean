import Std

/- Independent formal components for the parallel-gluing note.
   This file does not formalize the incidence construction or its full
   automorphism group. The geometric reconstruction remains a written proof. -/
namespace SimultaneousMatching

theorem common_image_iff_coherent_family
    {I : Type u} {D : Type v} {A : I → Type w}
    (anchor : I) (eligible : ∀ i, A i → Prop) (image : ∀ i, A i → D) :
    (∃ d, ∀ i, ∃ a, eligible i a ∧ image i a = d) ↔
    (∃ a : ∀ i, A i, ∀ i,
      eligible i (a i) ∧ image i (a i) = image anchor (a anchor)) := by
  classical
  constructor
  · rintro ⟨d, hd⟩
    let a : ∀ i, A i := fun i => Classical.choose (hd i)
    have ha (i : I) : eligible i (a i) ∧ image i (a i) = d :=
      Classical.choose_spec (hd i)
    exact ⟨a, fun i => ⟨(ha i).1, (ha i).2.trans (ha anchor).2.symm⟩⟩
  · rintro ⟨a, ha⟩
    exact ⟨image anchor (a anchor), fun i => ⟨a i, ha i⟩⟩

inductive Klein where
  | one | a | b | c
  deriving DecidableEq, Repr

open Klein

def mul : Klein → Klein → Klein
  | one, y => y
  | x, one => x
  | a, a => one
  | a, b => c
  | a, c => b
  | b, a => c
  | b, b => one
  | b, c => a
  | c, a => b
  | c, b => a
  | c, c => one

theorem mul_assoc (x y z : Klein) : mul (mul x y) z = mul x (mul y z) := by
  cases x <;> cases y <;> cases z <;> rfl

theorem one_mul (x : Klein) : mul one x = x := by rfl
theorem mul_one (x : Klein) : mul x one = x := by cases x <;> rfl
theorem mul_self (x : Klein) : mul x x = one := by cases x <;> rfl

def H₀ (x : Klein) : Prop := x = one ∨ x = a
def H₁ (x : Klein) : Prop := x = one ∨ x = b
def H₂ (x : Klein) : Prop := x = one ∨ x = c
def shifted (x : Klein) : Prop := x = a ∨ x = b

theorem H₀_closed (x y : Klein) (hx : H₀ x) (hy : H₀ y) : H₀ (mul x y) := by
  cases x <;> cases y <;> simp_all [H₀, mul]

theorem H₁_closed (x y : Klein) (hx : H₁ x) (hy : H₁ y) : H₁ (mul x y) := by
  cases x <;> cases y <;> simp_all [H₁, mul]

theorem H₂_closed (x y : Klein) (hx : H₂ x) (hy : H₂ y) : H₂ (mul x y) := by
  cases x <;> cases y <;> simp_all [H₂, mul]

theorem shifted_is_coset (g : Klein) :
    (∃ h, H₂ h ∧ mul a h = g) ↔ shifted g := by
  constructor
  · rintro ⟨h, hh, rfl⟩
    rcases hh with rfl | rfl
    · exact Or.inl rfl
    · exact Or.inr rfl
  · intro hg
    rcases hg with rfl | rfl
    · exact ⟨one, Or.inl rfl, rfl⟩
    · exact ⟨c, Or.inr rfl, rfl⟩

theorem pairwise_intersections :
    (∃ g, H₀ g ∧ H₁ g) ∧
    (∃ g, H₀ g ∧ shifted g) ∧
    (∃ g, H₁ g ∧ shifted g) := by
  exact ⟨⟨one, Or.inl rfl, Or.inl rfl⟩,
    ⟨a, Or.inr rfl, Or.inl rfl⟩, ⟨b, Or.inr rfl, Or.inr rfl⟩⟩

theorem no_common_element : ¬ ∃ g, H₀ g ∧ H₁ g ∧ shifted g := by
  rintro ⟨g, hg⟩
  cases g <;> simp_all [H₀, H₁, shifted]

-- The regular permutation representation is faithful: its value at the
-- identity determines the multiplier. Composition is mul_assoc above.
theorem regular_action_faithful (x y : Klein)
    (h : ∀ z, mul x z = mul y z) : x = y := by
  simpa only [mul_one] using h one

#print axioms common_image_iff_coherent_family
#print axioms mul_assoc
#print axioms one_mul
#print axioms mul_one
#print axioms mul_self
#print axioms H₀_closed
#print axioms H₁_closed
#print axioms H₂_closed
#print axioms shifted_is_coset
#print axioms pairwise_intersections
#print axioms no_common_element
#print axioms regular_action_faithful

end SimultaneousMatching
