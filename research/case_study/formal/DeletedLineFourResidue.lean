import Mathlib.Tactic

/-!
Literal q=4 residue for Construction 3 in L092, at the original line x=0.

F4 is represented in the basis (1, omega) over F2, with omega^2=omega+1.
Point objects are (x,y), x,y nonzero. Flag objects are (a,t), a,t nonzero,
representing ((0,t), x=a(y+t)). Incidence is exactly x=a(y+t).

The file proves a bijection of the resulting 18-vertex graph with three
disjoint 6-cycles, then proves disconnection using reflexive-transitive
reachability. It does not assume the source theorem or a connectivity claim.
-/

namespace MathCompression.DeletedLineFourResidue

abbrev F4 := ZMod 2 × ZMod 2
abbrev Exponent := ZMod 3
abbrev Pair := Exponent × Exponent
abbrev Vertex := Pair ⊕ Pair

def one4 : F4 := (1, 0)
def omega4 : F4 := (0, 1)

def mul4 (x y : F4) : F4 :=
  (x.1 * y.1 + x.2 * y.2, x.1 * y.2 + x.2 * y.1 + x.2 * y.2)

theorem field_table_laws :
    one4 ≠ 0 ∧
    (∀ x y : F4, mul4 x y = mul4 y x) ∧
    (∀ x y z : F4, mul4 (mul4 x y) z = mul4 x (mul4 y z)) ∧
    (∀ x y z : F4, mul4 x (y + z) = mul4 x y + mul4 x z) ∧
    (∀ x : F4, mul4 one4 x = x) ∧
    (∀ x : F4, x ≠ 0 → mul4 x (mul4 x x) = one4) := by decide

theorem omega_polynomial : mul4 omega4 omega4 = omega4 + one4 := by decide

/-- The three powers 1, omega, omega^2, in that order. -/
def nonzero (i : Exponent) : F4 :=
  if i = 0 then one4 else if i = 1 then omega4 else (1, 1)

theorem nonzero_bijection :
    Function.Injective nonzero ∧
    (∀ x : F4, x ≠ 0 ↔ ∃ i : Exponent, nonzero i = x) := by
  constructor
  · show ∀ i j, nonzero i = nonzero j → i = j
    decide
  · decide

theorem nonzero_mul (i j : Exponent) :
    mul4 (nonzero i) (nonzero j) = nonzero (i + j) := by
  revert i j
  decide

/-- The actual source-incidence equation in the F4 basis model. -/
def incident (point flag : Pair) : Prop :=
  nonzero point.1 = mul4 (nonzero flag.1) (nonzero point.2 + nonzero flag.2)

instance (point flag : Pair) : Decidable (incident point flag) :=
  inferInstanceAs (Decidable (_ = _))

def Adj : Vertex → Vertex → Prop
  | .inl point, .inr flag => incident point flag
  | .inr flag, .inl point => incident point flag
  | _, _ => False

instance (u v : Vertex) : Decidable (Adj u v) := by
  cases u <;> cases v <;> unfold Adj <;> infer_instance

theorem adj_symmetric (u v : Vertex) : Adj u v ↔ Adj v u := by
  cases u <;> cases v <;> rfl

theorem adj_irreflexive (u : Vertex) : ¬ Adj u u := by
  cases u <;> simp [Adj]

/-- This finite arithmetic implication is derived from the literal equation,
not imposed as the definition of the graph. -/
theorem incidence_formula (x y a t : Exponent) :
    incident (x, y) (a, t) ↔ x + y = a - t ∧ y ≠ t := by
  revert x y a t
  decide

def component : Vertex → Exponent
  | .inl point => point.1 + point.2
  | .inr flag => flag.1 - flag.2

theorem edge_preserves_component (u v : Vertex) (h : Adj u v) :
    component u = component v := by
  cases u with
  | inl point =>
    cases v with
    | inl other => exact False.elim h
    | inr flag => exact (incidence_formula _ _ _ _).mp h |>.1
  | inr flag =>
    cases v with
    | inl point => exact ((incidence_formula _ _ _ _).mp h).1.symm
    | inr other => exact False.elim h

def Reachable : Vertex → Vertex → Prop := Relation.ReflTransGen Adj
def Connected : Prop := ∀ u v, Reachable u v

theorem reachable_preserves_component {u v : Vertex} (h : Reachable u v) :
    component u = component v := by
  induction h with
  | refl => rfl
  | tail _ edge ih => exact ih.trans (edge_preserves_component _ _ edge)

def pointOne : Vertex := .inl (0, 0)
def pointOmega : Vertex := .inl (1, 0)

theorem not_reachable : ¬ Reachable pointOne pointOmega := by
  intro h
  have he := reachable_preserves_component h
  have hn : component pointOne ≠ component pointOmega := by decide
  exact hn he

theorem not_connected : ¬ Connected := by
  intro h
  exact not_reachable (h pointOne pointOmega)

/-- Cyclic order L0,R1,L2,R0,L1,R2 in each component. -/
def cycleVertex (k : Exponent) (i : Fin 6) : Vertex :=
  match i.val with
  | 0 => .inl (k, 0)
  | 1 => .inr (k + 1, 1)
  | 2 => .inl (k - 2, 2)
  | 3 => .inr (k, 0)
  | 4 => .inl (k - 1, 1)
  | _ => .inr (k + 2, 2)

def cycleCoordinates : Vertex → Exponent × Fin 6
  | .inl (x,y) => (x+y, if y=0 then 0 else if y=1 then 4 else 2)
  | .inr (a,t) => (a-t, if t=0 then 3 else if t=1 then 1 else 5)

def threeHexagons : (Exponent × Fin 6) ≃ Vertex where
  toFun p := cycleVertex p.1 p.2
  invFun := cycleCoordinates
  left_inv := by
    show ∀ p, cycleCoordinates (cycleVertex p.1 p.2) = p
    decide
  right_inv := by
    show ∀ v, cycleVertex (cycleCoordinates v).1 (cycleCoordinates v).2 = v
    decide

def cycleAdjacent (i j : Fin 6) : Prop :=
  (i.val + 1) % 6 = j.val ∨ (j.val + 1) % 6 = i.val

instance (i j : Fin 6) : Decidable (cycleAdjacent i j) :=
  inferInstanceAs (Decidable (_ ∨ _))

theorem three_hexagons_adjacency (k l : Exponent) (i j : Fin 6) :
    Adj (threeHexagons (k,i)) (threeHexagons (l,j)) ↔
      k = l ∧ cycleAdjacent i j := by
  revert k l i j
  decide

theorem vertex_count : Fintype.card Vertex = 18 := by decide

#print axioms field_table_laws
#print axioms nonzero_bijection
#print axioms incidence_formula
#print axioms reachable_preserves_component
#print axioms not_connected
#print axioms three_hexagons_adjacency
#print axioms vertex_count

end MathCompression.DeletedLineFourResidue
