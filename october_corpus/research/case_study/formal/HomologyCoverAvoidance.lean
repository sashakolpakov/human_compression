import Mathlib.Algebra.Module.Submodule.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Fin
import Mathlib.Tactic.Abel
import Lean.Elab.Tactic.Omega

/-! Elementary finite-field interfaces for phase256's written rank-four proof.
These statements prove the affine-line uniqueness and finite avoidance step.
They do not formalize cellular homology, surface topology, or the identification
of the actual end fibers with the affine cosets in these hypotheses. -/
namespace MathCompression.HomologyCoverAvoidance

variable {F V : Type*} [Field F] [AddCommGroup V] [Module F V]

/-- A line transverse to a subspace meets an affine translate at most once. -/
theorem affine_line_unique (S : Submodule F V) (u x c : V) (hu : u ∉ S)
    {a b : F} (ha : a • u + x - c ∈ S) (hb : b • u + x - c ∈ S) :
    a = b := by
  by_contra hab
  have hdiff : (a - b) • u ∈ S := by
    have heq : (a • u + x - c) - (b • u + x - c) = (a - b) • u := by
      rw [sub_smul]
      abel
    rw [← heq]
    exact S.sub_mem ha hb
  exact hu ((S.smul_mem_iff (sub_ne_zero.mpr hab)).mp hdiff)

/-- Fewer affine constraints than field elements leave a permitted scalar. -/
theorem exists_avoiding_affine_translates {I : Type*} [Fintype I] [Fintype F]
    (S : I → Submodule F V) (x c : I → V) (u : V)
    (hu : ∀ i, u ∉ S i) (hcard : Fintype.card I < Fintype.card F) :
    ∃ a : F, ∀ i, a • u + x i - c i ∉ S i := by
  classical
  let bad : I → Finset F := fun i => Finset.univ.filter
    (fun a => a • u + x i - c i ∈ S i)
  have hbad : ∀ i, (bad i).card ≤ 1 := by
    intro i
    apply Finset.card_le_one.mpr
    intro a ha b hb
    exact affine_line_unique (S i) u (x i) (c i) (hu i)
      (Finset.mem_filter.mp ha).2 (Finset.mem_filter.mp hb).2
  have hbound : (Finset.univ.biUnion bad).card ≤ Fintype.card I := by
    simpa using Finset.card_biUnion_le_card_mul Finset.univ bad 1 (fun i _ => hbad i)
  have hne : Finset.univ.biUnion bad ≠ (Finset.univ : Finset F) :=
    (Finset.card_lt_iff_ne_univ _).mp (lt_of_le_of_lt hbound hcard)
  have hex : ∃ a : F, a ∉ Finset.univ.biUnion bad := by
    by_contra hn
    apply hne
    apply Finset.eq_univ_iff_forall.mpr
    intro a
    by_contra ha
    exact hn ⟨a, ha⟩
  obtain ⟨a, ha⟩ := hex
  refine ⟨a, fun i hi => ha ?_⟩
  exact Finset.mem_biUnion.mpr ⟨i, Finset.mem_univ i,
    Finset.mem_filter.mpr ⟨Finset.mem_univ a, hi⟩⟩

/-- Two possible forbidden end fibers at each of n visited vertices. -/
theorem exists_avoiding_two_subspaces [Fintype F] (n : ℕ)
    (A B : Submodule F V) (x a b : Fin n → V) (u : V)
    (hA : u ∉ A) (hB : u ∉ B) (hp : 2 * n < Fintype.card F) :
    ∃ k : F, ∀ i, (k • u + x i - a i ∉ A) ∧ (k • u + x i - b i ∉ B) := by
  let S : Fin n × Bool → Submodule F V := fun j => if j.2 then A else B
  let c : Fin n × Bool → V := fun j => if j.2 then a j.1 else b j.1
  have hu : ∀ j, u ∉ S j := by
    intro ⟨i, t⟩
    cases t <;> simp [S, hA, hB]
  have hcard : Fintype.card (Fin n × Bool) < Fintype.card F := by
    simpa [Fintype.card_prod, Nat.mul_comm] using hp
  obtain ⟨k, hk⟩ := exists_avoiding_affine_translates S (fun j => x j.1) c u hu hcard
  refine ⟨k, fun i => ⟨?_, ?_⟩⟩
  · simpa [S, c] using hk (i, true)
  · simpa [S, c] using hk (i, false)

/-- The path-length bound used for spanning-tree graph loops. -/
theorem path_constraint_bound (g L p : ℕ) (hg : 0 < g)
    (hL : L ≤ 2 * g - 1) (hp : 4 * g < p) : 2 * (L + 1) < p := by
  omega

/-- Repeating an odd-length walk an odd number of times keeps odd parity. -/
theorem odd_repetition (p L : ℕ) (hp : p % 2 = 1) (hL : L % 2 = 1) :
    (p * L) % 2 = 1 := by
  rw [Nat.mul_mod, hp, hL]

#print axioms affine_line_unique
#print axioms exists_avoiding_affine_translates
#print axioms exists_avoiding_two_subspaces
#print axioms path_constraint_bound
#print axioms odd_repetition

end MathCompression.HomologyCoverAvoidance
