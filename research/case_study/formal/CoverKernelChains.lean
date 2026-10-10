import Mathlib.Tactic
import Mathlib.Data.Int.GCD
import Mathlib.Algebra.Group.Subgroup.Pointwise
import Mathlib.Order.Zorn

/-!
Kernel intersection property, directed unions, and coprime-power joins.
The geometric/polytope correspondence and surface theorem are not asserted here.
-/
namespace MathCompression.CoverKernelChains

variable {W ι : Type*} [Group W]

/-- The word form of the quotient intersection property for specified parabolics. -/
def IntersectionProperty (P : Set ι → Subgroup W) (N : Subgroup W) : Prop :=
  ∀ I J : Set ι, ∀ a ∈ P I, ∀ b ∈ P J,
    a * b⁻¹ ∈ N → ∃ c ∈ P (I ∩ J), a * c⁻¹ ∈ N

theorem intersectionProperty_sSup_of_directed
    (P : Set ι → Subgroup W) (C : Set (Subgroup W))
    (hne : C.Nonempty) (hdir : DirectedOn (· ≤ ·) C)
    (hC : ∀ N ∈ C, IntersectionProperty P N) :
    IntersectionProperty P (sSup C) := by
  intro I J a ha b hb hab
  obtain ⟨N, hNC, habN⟩ := (Subgroup.mem_sSup_of_directedOn hne hdir).mp hab
  obtain ⟨c, hc, hac⟩ := hC N hNC I J a ha b hb habN
  exact ⟨c, hc, Subgroup.mem_sSup_of_mem hNC hac⟩

theorem intersectionProperty_sSup_of_chain
    (P : Set ι → Subgroup W) (C : Set (Subgroup W))
    (hne : C.Nonempty) (hchain : IsChain (· ≤ ·) C)
    (hC : ∀ N ∈ C, IntersectionProperty P N) :
    IntersectionProperty P (sSup C) :=
  intersectionProperty_sSup_of_directed P C hne hchain.directedOn hC

/-- The algebraic requirements on a regular-cover kernel below a fixed target. -/
def Admissible (P : Set ι → Subgroup W) (K N : Subgroup W) : Prop :=
  N.Normal ∧ N ≤ K ∧ IntersectionProperty P N

/-- Every admissible kernel has a maximal admissible overgroup, even at infinite index. -/
theorem exists_maximal_admissible_over (P : Set ι → Subgroup W) (K N : Subgroup W)
    (hN : Admissible P K N) :
    ∃ M, N ≤ M ∧ Maximal (Admissible P K) M := by
  apply zorn_le_nonempty₀ {L | Admissible P K L} ?_ N hN
  intro C hC hchain y hy
  refine ⟨sSup C, ?_, fun z hz => le_sSup hz⟩
  refine ⟨Subgroup.sSup_normal C (fun L hL => (hC hL).1), ?_, ?_⟩
  · exact sSup_le (fun L hL => (hC hL).2.1)
  · exact intersectionProperty_sSup_of_chain P C ⟨y, hy⟩ hchain
      (fun L hL => (hC hL).2.2)

/-- Uniqueness of a maximal admissible kernel implies that it contains all the others. -/
theorem unique_maximal_is_greatest (P : Set ι → Subgroup W) (K M : Subgroup W)
    (_hM : Maximal (Admissible P K) M)
    (hunique : ∀ L, Maximal (Admissible P K) L → L = M) :
    ∀ N, Admissible P K N → N ≤ M := by
  intro N hN
  obtain ⟨L, hNL, hL⟩ := exists_maximal_admissible_over P K N hN
  simpa only [hunique L hL] using hNL

/-- Two coprime powers in a subgroup force the element itself into it. -/
theorem mem_of_coprime_powers (L : Subgroup W) (x : W) (p q : ℕ)
    (hcop : p.Coprime q) (hp : x ^ p ∈ L) (hq : x ^ q ∈ L) : x ∈ L := by
  have bez : (1 : ℤ) = (p : ℤ) * Nat.gcdA p q + (q : ℤ) * Nat.gcdB p q := by
    simpa [hcop.gcd_eq_one] using Nat.gcd_eq_gcd_ab p q
  have hprod := L.mul_mem (L.zpow_mem hp (Nat.gcdA p q))
    (L.zpow_mem hq (Nat.gcdB p q))
  simpa only [← zpow_natCast, ← zpow_mul, ← zpow_add, ← bez, zpow_one] using hprod

/-- No finiteness or commutativity hypothesis is needed for this join witness. -/
theorem sup_eq_of_coprime_powers (K A B : Subgroup W) (p q : ℕ)
    (hA : A ≤ K) (hB : B ≤ K) (hcop : p.Coprime q)
    (hp : ∀ x ∈ K, x ^ p ∈ A) (hq : ∀ x ∈ K, x ^ q ∈ B) : A ⊔ B = K := by
  apply le_antisymm
  · exact sup_le hA hB
  · intro x hx
    exact mem_of_coprime_powers (A ⊔ B) x p q hcop
      ((show A ≤ A ⊔ B from le_sup_left) (hp x hx))
      ((show B ≤ A ⊔ B from le_sup_right) (hq x hx))

#print axioms intersectionProperty_sSup_of_directed
#print axioms intersectionProperty_sSup_of_chain
#print axioms exists_maximal_admissible_over
#print axioms unique_maximal_is_greatest
#print axioms mem_of_coprime_powers
#print axioms sup_eq_of_coprime_powers

end MathCompression.CoverKernelChains
