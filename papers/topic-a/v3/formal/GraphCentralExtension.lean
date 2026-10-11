import Mathlib.Algebra.Group.Hom.Defs
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-! The explicit bilinear group used in the graph construction.
This file verifies the group law and the support subgroups. It does not
formalize the coset geometry, the presentation, or the SmallGroups search. -/
namespace GraphCentralExtension

variable {V Z : Type*} [AddCommGroup V] [AddCommGroup Z]

@[ext] structure Extension (β : V →+ V →+ Z) where
  vertex : V
  central : Z

variable (β : V →+ V →+ Z)

instance : Group (Extension β) where
  mul x y := ⟨x.vertex + y.vertex, x.central + y.central + β x.vertex y.vertex⟩
  one := ⟨0, 0⟩
  inv x := ⟨-x.vertex, -x.central + β x.vertex x.vertex⟩
  mul_assoc x y z := by
    apply Extension.ext
    · exact add_assoc _ _ _
    · change (x.central + y.central + β x.vertex y.vertex) + z.central +
          β (x.vertex + y.vertex) z.vertex =
        x.central + (y.central + z.central + β y.vertex z.vertex) +
          β x.vertex (y.vertex + z.vertex)
      simp only [map_add, AddMonoidHom.add_apply]
      abel
  one_mul x := by
    apply Extension.ext
    · exact zero_add _
    · change 0 + x.central + β 0 x.vertex = x.central
      simp
  mul_one x := by
    apply Extension.ext
    · exact add_zero _
    · change x.central + 0 + β x.vertex 0 = x.central
      simp
  inv_mul_cancel x := by
    apply Extension.ext
    · exact neg_add_cancel _
    · change (-x.central + β x.vertex x.vertex) + x.central +
        β (-x.vertex) x.vertex = 0
      simp only [map_neg, AddMonoidHom.neg_apply]
      abel

def vertexProjection : Extension β →* Multiplicative V where
  toFun x := Multiplicative.ofAdd x.vertex
  map_one' := rfl
  map_mul' _ _ := rfl

variable {I E : Type*}
abbrev Binary (I : Type*) := I → ZMod 2

def edgeForm (tail head : E → I) : Binary I →+ Binary I →+ Binary E where
  toFun v :=
    { toFun := fun w e => v (head e) * w (tail e)
      map_zero' := by ext e; simp
      map_add' := by intros; ext e; simp [mul_add] }
  map_zero' := by ext w e; simp
  map_add' := by intros; ext w e; simp [add_mul]

variable (tail head : E → I)

def supported (J : Set I) : Subgroup (Extension (edgeForm tail head)) where
  carrier := {x | (∀ i, i ∉ J → x.vertex i = 0) ∧
    (∀ e, (tail e ∉ J ∨ head e ∉ J) → x.central e = 0)}
  one_mem' := by constructor <;> intros <;> rfl
  mul_mem' := by
    rintro x y ⟨hxv, hxz⟩ ⟨hyv, hyz⟩
    constructor
    · intro i hi
      change x.vertex i + y.vertex i = 0
      simp [hxv i hi, hyv i hi]
    · intro e he
      change x.central e + y.central e + x.vertex (head e) * y.vertex (tail e) = 0
      rw [hxz e he, hyz e he]
      rcases he with ht | hh
      · simp [hyv _ ht]
      · simp [hxv _ hh]
  inv_mem' := by
    rintro x ⟨hxv, hxz⟩
    constructor
    · intro i hi
      change -x.vertex i = 0
      simp [hxv i hi]
    · intro e he
      change -x.central e + x.vertex (head e) * x.vertex (tail e) = 0
      rw [hxz e he]
      rcases he with ht | hh
      · simp [hxv _ ht]
      · simp [hxv _ hh]

theorem support_intersection (J K : Set I) :
    supported tail head J ⊓ supported tail head K = supported tail head (J ∩ K) := by
  ext x
  change ((_ ∧ _) ∧ (_ ∧ _)) ↔ (_ ∧ _)
  constructor
  · rintro ⟨⟨hjv, hjz⟩, ⟨hkv, hkz⟩⟩
    constructor
    · intro i hi
      by_cases hj : i ∈ J
      · exact hkv i (fun hk => hi ⟨hj, hk⟩)
      · exact hjv i hj
    · intro e he
      by_cases hj : tail e ∈ J ∧ head e ∈ J
      · apply hkz e
        tauto
      · apply hjz e
        tauto
  · rintro ⟨hv, hz⟩
    constructor
    · constructor
      · intro i hi
        exact hv i (fun h => hi h.1)
      · intro e he
        apply hz e
        simp only [Set.mem_inter_iff]
        tauto
    · constructor
      · intro i hi
        exact hv i (fun h => hi h.2)
      · intro e he
        apply hz e
        simp only [Set.mem_inter_iff]
        tauto

theorem power_gap (r k : ℕ) (h : 2 ^ r < 2 ^ k) : 2 ^ (r + 1) ≤ 2 ^ k := by
  have hrk : r < k := by
    by_contra hn
    have hk : k ≤ r := by omega
    have hp : (2 : ℕ) ^ k ≤ 2 ^ r := Nat.pow_le_pow_right (by omega) hk
    omega
  exact Nat.pow_le_pow_right (by omega) (by omega)

end GraphCentralExtension

#print axioms GraphCentralExtension.instGroupExtension
#print axioms GraphCentralExtension.vertexProjection
#print axioms GraphCentralExtension.edgeForm
#print axioms GraphCentralExtension.supported
#print axioms GraphCentralExtension.support_intersection
#print axioms GraphCentralExtension.power_gap
