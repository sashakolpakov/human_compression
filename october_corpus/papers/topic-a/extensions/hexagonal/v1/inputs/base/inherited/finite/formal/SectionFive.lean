import Mathlib.GroupTheory.Perm.Fin

/- Exact finite countermodel to the two literal modified Section 5 relators.
   No group-order, fp-group isomorphism or geometry formalization is claimed. -/
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000
namespace L121SectionFive
abbrev P := Equiv.Perm (Fin 11)
def a : P := Equiv.swap 0 2 * Equiv.swap 1 3 * Equiv.swap 4 5 * Equiv.swap 6 8
def b : P := Equiv.swap 0 1 * Equiv.swap 2 4 * Equiv.swap 3 5 * Equiv.swap 6 7
def c : P := Equiv.swap 2 5 * Equiv.swap 3 4 * Equiv.swap 8 9
def d : P := Equiv.swap 0 3 * Equiv.swap 1 2 * Equiv.swap 9 10

def Base (a b c d : P) : Prop :=
  a^2 = 1 ∧ b^2 = 1 ∧ c^2 = 1 ∧ d^2 = 1 ∧
  (a*b)^3 = 1 ∧ (a*c)^6 = 1 ∧ (a*d)^2 = 1 ∧
  (b*c)^2 = 1 ∧ (b*d)^6 = 1 ∧ (c*d)^3 = 1 ∧
  (d*(c*a)^2*c)^2 = 1 ∧ (a*(b*d)^2)^2 = 1 ∧ (b*(a*c)^2*a)^2 = 1

instance : Decidable (Base a b c d) := inferInstanceAs (Decidable (_ ∧ _))

theorem base_relations : Base a b c d := by decide

theorem modified_power_two : (c*(d*b)^2)^2 = 1 := by decide

theorem modified_power_four : (c*(d*b)^2)^4 = 1 := by decide

theorem bd_square_ne_one : (b*d)^2 ≠ 1 := by decide

theorem not_universal_power_two_consequence :
    ¬ (∀ (a b c d : P), Base a b c d → (c*(d*b)^2)^2 = 1 → (b*d)^2 = 1) := by
  intro h
  exact bd_square_ne_one (h a b c d base_relations modified_power_two)

theorem not_universal_power_four_consequence :
    ¬ (∀ (a b c d : P), Base a b c d → (c*(d*b)^2)^4 = 1 → (b*d)^2 = 1) := by
  intro h
  exact bd_square_ne_one (h a b c d base_relations modified_power_four)

#print axioms base_relations
#print axioms modified_power_two
#print axioms modified_power_four
#print axioms bd_square_ne_one
#print axioms not_universal_power_two_consequence
#print axioms not_universal_power_four_consequence
end L121SectionFive
