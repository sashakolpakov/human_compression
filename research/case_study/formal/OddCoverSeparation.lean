import Mathlib.GroupTheory.Index
import Mathlib.Algebra.Ring.Parity
import Mathlib.Order.Preorder.Finite
import Mathlib.Data.Fintype.Sets

/-!
Kernel-cardinality obstruction to factoring a cover over a common base.
This file does not construct polytopes or prove a proposed cover's
intersection property. Those remain separate mathematical obligations.
-/

namespace MathCompression.OddCoverSeparation

variable {H J G : Type*} [Group H] [Group J] [Group G]

/-- A commuting map over the base induces a homomorphism of the kernels. -/
def kernelMap (π : H →* G) (σ : J →* G) (q : H →* J)
    (hcomm : σ.comp q = π) : π.ker →* σ.ker where
  toFun x := ⟨q x, by
    change σ (q x) = 1
    have he := congrArg (fun f : H →* G => f x) hcomm
    exact he.trans x.property⟩
  map_one' := by ext; simp
  map_mul' x y := by ext; simp

/-- Surjectivity over a common base also holds on the entire covering kernel. -/
theorem kernelMap_surjective (π : H →* G) (σ : J →* G) (q : H →* J)
    (hcomm : σ.comp q = π) (hq : Function.Surjective q) :
    Function.Surjective (kernelMap π σ q hcomm) := by
  intro y
  obtain ⟨x, hx⟩ := hq y
  have hπx : π x = 1 := by
    have he := congrArg (fun f : H →* G => f x) hcomm
    change σ (q x) = π x at he
    rw [hx] at he
    exact he.symm.trans y.property
  exact ⟨⟨x, hπx⟩, Subtype.ext hx⟩

/-- The degree of every quotient over the base divides the original degree. -/
theorem kernel_card_dvd (π : H →* G) (σ : J →* G) (q : H →* J)
    (hcomm : σ.comp q = π) (hq : Function.Surjective q) :
    Nat.card σ.ker ∣ Nat.card π.ker :=
  Subgroup.card_dvd_of_surjective (kernelMap π σ q hcomm)
    (kernelMap_surjective π σ q hcomm hq)

/-- Every quotient over the same base of an odd-degree cover still has odd degree. -/
theorem odd_kernel_of_quotient (π : H →* G) (σ : J →* G) (q : H →* J)
    (hcomm : σ.comp q = π) (hq : Function.Surjective q)
    (hodd : Odd (Nat.card π.ker)) : Odd (Nat.card σ.ker) := by
  apply Nat.not_even_iff_odd.mp
  rintro ⟨n, hn⟩
  have hd : 2 ∣ Nat.card σ.ker := ⟨n, by omega⟩
  exact hodd.not_two_dvd_nat (dvd_trans hd (kernel_card_dvd π σ q hcomm hq))

/-- An odd-degree cover cannot map onto an even-degree cover over the same base. -/
theorem no_even_kernel_factor (π : H →* G) (σ : J →* G)
    (hodd : Odd (Nat.card π.ker)) (heven : 2 ∣ Nat.card σ.ker) :
    ¬ ∃ q : H →* J, Function.Surjective q ∧ σ.comp q = π := by
  rintro ⟨q, hq, hcomm⟩
  exact hodd.not_two_dvd_nat (dvd_trans heven (kernel_card_dvd π σ q hcomm hq))

/-- In particular the odd-degree cover cannot factor onto a double cover. -/
theorem no_double_cover_factor (π : H →* G) (σ : J →* G)
    (hodd : Odd (Nat.card π.ker)) (hdouble : Nat.card σ.ker = 2) :
    ¬ ∃ q : H →* J, Function.Surjective q ∧ σ.comp q = π := by
  have heven : 2 ∣ Nat.card σ.ker := by rw [hdouble]
  exact no_even_kernel_factor π σ hodd heven

/-- A finite group has a maximal admissible normal kernel over a fixed base.
The predicate is supplied by the application; no polytope predicate is hidden here. -/
theorem exists_maximal_admissible_kernel [Finite H] (π : H →* G)
    (admissible : Subgroup H → Prop) (hbot : admissible ⊥) :
    ∃ N : Subgroup H, N.Normal ∧ N ≤ π.ker ∧ admissible N ∧
      ∀ M : Subgroup H, M.Normal → M ≤ π.ker → admissible M → N ≤ M → M = N := by
  classical
  letI : Finite (Subgroup H) := Finite.of_injective
    (fun N : Subgroup H => (N : Set H)) SetLike.coe_injective
  let S : Set (Subgroup H) := {N | N.Normal ∧ N ≤ π.ker ∧ admissible N}
  have hb : (⊥ : Subgroup H) ∈ S := ⟨inferInstance, bot_le, hbot⟩
  obtain ⟨N, hN⟩ := S.toFinite.exists_maximal ⟨⊥, hb⟩
  refine ⟨N, hN.1.1, hN.1.2.1, hN.1.2.2, ?_⟩
  intro M hnormal hker hadmissible hNM
  exact le_antisymm (hN.2 ⟨hnormal, hker, hadmissible⟩ hNM) hNM

#print axioms kernelMap_surjective
#print axioms kernel_card_dvd
#print axioms odd_kernel_of_quotient
#print axioms no_even_kernel_factor
#print axioms no_double_cover_factor
#print axioms exists_maximal_admissible_kernel

end MathCompression.OddCoverSeparation
