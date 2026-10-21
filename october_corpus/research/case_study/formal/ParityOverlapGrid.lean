import ParityMixCoordinateProfile
import Mathlib.Order.Interval.Set.OrdConnected

/-! Exact support refinement by the component-overlap grid. -/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration

variable {I C T G : Type*} [DecidableEq I] [Fintype C] [Fintype T]
  [DecidableEq C] [DecidableEq T] [Group G]

def overlapScope (L : C → Finset I) (R : T → Finset I) (p : C × T) : Finset I :=
  L p.1 ∩ R p.2

omit [DecidableEq C] [DecidableEq T] in
theorem overlapScope_cover (L : C → Finset I) (R : T → Finset I) :
    Finset.univ.biUnion (overlapScope L R) =
      (Finset.univ.biUnion L) ∩ (Finset.univ.biUnion R) := by
  ext i
  simp only [Finset.mem_biUnion, Finset.mem_univ, true_and, overlapScope,
    Finset.mem_inter, Prod.exists]
  aesop

omit [Fintype C] [Fintype T] [DecidableEq C] [DecidableEq T] in
theorem overlapScope_disjoint (L : C → Finset I) (R : T → Finset I)
    (hL : Pairwise fun c d => Disjoint (L c) (L d))
    (hR : Pairwise fun c d => Disjoint (R c) (R d)) :
    Pairwise fun p q : C × T => Disjoint (overlapScope L R p) (overlapScope L R q) := by
  intro p q hpq
  apply Finset.disjoint_left.mpr
  intro i hip hiq
  obtain ⟨hiL, hiR⟩ := Finset.mem_inter.mp hip
  obtain ⟨hjL, hjR⟩ := Finset.mem_inter.mp hiq
  by_cases hfst : p.1 = q.1
  · have hsnd : p.2 ≠ q.2 := fun h => hpq (Prod.ext hfst h)
    exact Finset.disjoint_left.mp (hR hsnd) hiR hjR
  · exact Finset.disjoint_left.mp (hL hfst) hiL hjL

omit [Fintype C] [Fintype T] [DecidableEq C] [DecidableEq T] in
theorem overlapScope_commute (r : I → G) (L : C → Finset I) (R : T → Finset I)
    (hL : Pairwise fun c d => ∀ i ∈ L c, ∀ j ∈ L d, Commute (r i) (r j))
    (hR : Pairwise fun c d => ∀ i ∈ R c, ∀ j ∈ R d, Commute (r i) (r j)) :
    Pairwise fun p q : C × T =>
      ∀ i ∈ overlapScope L R p, ∀ j ∈ overlapScope L R q, Commute (r i) (r j) := by
  intro p q hpq i hip j hjq
  obtain ⟨hiL, hiR⟩ := Finset.mem_inter.mp hip
  obtain ⟨hjL, hjR⟩ := Finset.mem_inter.mp hjq
  by_cases hfst : p.1 = q.1
  · have hsnd : p.2 ≠ q.2 := fun h => hpq (Prod.ext hfst h)
    exact hR hsnd i hiR j hjR
  · exact hL hfst i hiL j hjL

omit [Fintype C] [Fintype T] [DecidableEq C] [DecidableEq T] in
theorem overlapScope_ordConnected [LinearOrder I] (L : C → Finset I) (R : T → Finset I)
    (hL : ∀ c, Set.OrdConnected (L c : Set I))
    (hR : ∀ t, Set.OrdConnected (R t : Set I)) (p : C × T) :
    Set.OrdConnected (overlapScope L R p : Set I) := by
  letI := hL p.1
  letI := hR p.2
  unfold overlapScope
  rw [Finset.coe_inter]
  infer_instance

#print axioms overlapScope_cover
#print axioms overlapScope_disjoint
#print axioms overlapScope_commute
#print axioms overlapScope_ordConnected

end MathCompression.ParityMix
