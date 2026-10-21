import ParityRefinementCharacters
import ParityMixFiniteProfile
import FinIntervalOverlapCancellation

/-!
The actual intersection argument for marked parity mixes. Every row and
column equation is derived from mixed membership and component refinement;
interval cancellation is supplied by the independently proved theorem.
-/

namespace MathCompression.ParityMix

open MathCompression.SupportedKernelGeneration
open MathCompression.IntervalOverlapCancellation
open scoped BigOperators

variable {n : ℕ} {C T E G A : Type*} [Fintype C] [Fintype T]
  [DecidableEq C] [DecidableEq T] [Group E] [Group G] [CommGroup A]

/-- Projection of an actually generated mixed parabolic lands in each
actually generated coordinate parabolic. -/
theorem mixed_coordinate_membership (e : Fin n → E) (g : Fin n → G)
    (S : Finset (Fin n)) (z : E × G)
    (hz : z ∈ marked (fun i => (e i, g i)) S) :
    z.1 ∈ marked e S ∧ z.2 ∈ marked g S := by
  constructor
  · have h : z.1 ∈ (marked (fun i => (e i, g i)) S).map (MonoidHom.fst E G) :=
      ⟨z, hz, rfl⟩
    rwa [marked_map] at h
  · have h : z.2 ∈ (marked (fun i => (e i, g i)) S).map (MonoidHom.snd E G) :=
      ⟨z, hz, rfl⟩
    rwa [marked_map] at h

/-- Full intersection for two supports partitioned into separated integer
intervals. Exact local parity fibers suffice; no mixed intersection,
refinement parity sum, or forest property is assumed. -/
theorem parity_overlap_intersection (e : Fin n → E) (g : Fin n → G)
    (ε : E →* A) (δ : G →* A)
    (hipE : ∀ L M, marked e L ⊓ marked e M = marked e (L ∩ M))
    (hipG : ∀ L M, marked g L ⊓ marked g M = marked g (L ∩ M))
    (hlocal : ∀ S : Finset (Fin n), Set.OrdConnected (S : Set (Fin n)) →
      ∀ x : E × G, x ∈ marked (fun i => (e i, g i)) S ↔
        x.1 ∈ marked e S ∧ x.2 ∈ marked g S ∧ ε x.1 = δ x.2)
    (L : C → Finset (Fin n)) (R : T → Finset (Fin n))
    (hL : ∀ c, Set.OrdConnected (L c : Set (Fin n)))
    (hR : ∀ t, Set.OrdConnected (R t : Set (Fin n)))
    (dL : Pairwise fun c d => Disjoint (L c) (L d))
    (dR : Pairwise fun c d => Disjoint (R c) (R d))
    (hLE : Pairwise fun c d => ∀ i ∈ L c, ∀ j ∈ L d, Commute (e i) (e j))
    (hLG : Pairwise fun c d => ∀ i ∈ L c, ∀ j ∈ L d, Commute (g i) (g j))
    (hRE : Pairwise fun c d => ∀ i ∈ R c, ∀ j ∈ R d, Commute (e i) (e j))
    (hRG : Pairwise fun c d => ∀ i ∈ R c, ∀ j ∈ R d, Commute (g i) (g j)) :
    marked (fun i => (e i, g i)) (Finset.univ.biUnion L) ⊓
      marked (fun i => (e i, g i)) (Finset.univ.biUnion R) =
      marked (fun i => (e i, g i)) ((Finset.univ.biUnion L) ∩ (Finset.univ.biUnion R)) := by
  classical
  apply le_antisymm
  · intro z hz
    have hzL := mixed_coordinate_membership e g _ z hz.1
    have hzR := mixed_coordinate_membership e g _ z hz.2
    let fine := overlapScope L R
    let hfE := overlapScope_commute e L R hLE hRE
    let hfG := overlapScope_commute g L R hLG hRG
    have hx : z.1 ∈ marked e (Finset.univ.biUnion fine) := by
      rw [overlapScope_cover, ← hipE]
      exact ⟨hzL.1, hzR.1⟩
    have hy : z.2 ∈ marked g (Finset.univ.biUnion fine) := by
      rw [overlapScope_cover, ← hipG]
      exact ⟨hzL.2, hzR.2⟩
    have hxr : z.1 ∈ (componentAssembly e fine hfE).range := by
      rw [componentAssembly_range]
      exact hx
    have hyr : z.2 ∈ (componentAssembly g fine hfG).range := by
      rw [componentAssembly_range]
      exact hy
    obtain ⟨x, hxval⟩ := hxr
    obtain ⟨y, hyval⟩ := hyr
    have localL (c : C) (u : marked e (L c)) (v : marked g (L c)) :
        ((u : E), (v : G)) ∈ marked (fun i => (e i, g i)) (L c) ↔ ε u = δ v := by
      rw [hlocal (L c) (hL c)]
      exact ⟨fun h => h.2.2, fun h => ⟨u.property, v.property, h⟩⟩
    have localR (t : T) (u : marked e (R t)) (v : marked g (R t)) :
        ((u : E), (v : G)) ∈ marked (fun i => (e i, g i)) (R t) ↔ ε u = δ v := by
      rw [hlocal (R t) (hR t)]
      exact ⟨fun h => h.2.2, fun h => ⟨u.property, v.property, h⟩⟩
    have hmL : (componentAssembly e fine hfE x, componentAssembly g fine hfG y) ∈
        marked (fun i => (e i, g i)) (Finset.univ.biUnion L) := by
      rw [hxval, hyval]
      exact hz.1
    have hmR : (componentAssembly e fine hfE x, componentAssembly g fine hfG y) ∈
        marked (fun i => (e i, g i)) (Finset.univ.biUnion R) := by
      rw [hxval, hyval]
      exact hz.2
    have rows := refined_character_equality e g L fine hLE hLG hfE hfG dL hipE hipG
      ε δ localL Prod.fst (fun _ => Finset.inter_subset_left) x y hmL
    have cols := refined_character_equality e g R fine hRE hRG hfE hfG dR hipE hipG
      ε δ localR Prod.snd (fun _ => Finset.inter_subset_right) x y hmR
    let w : C → T → Additive A := fun c t => Additive.ofMul (ε (x (c, t)) * (δ (y (c, t)))⁻¹)
    have wrow : ∀ c, ∑ t, w c t = 0 := by
      intro c
      apply character_defect_sum
      simpa only [row_filtered_product] using rows c
    have wcol : ∀ t, ∑ c, w c t = 0 := by
      intro t
      apply character_defect_sum
      simpa only [column_filtered_product] using cols t
    have wsupport : ∀ c t, Disjoint (L c) (R t) → w c t = 0 := by
      intro c t hd
      have hempty : fine (c, t) = ∅ := Finset.disjoint_iff_inter_eq_empty.mp hd
      have hxone : (x (c, t) : E) = 1 := by
        have h := (x (c, t)).property
        simpa only [hempty, marked_empty, Subgroup.mem_bot] using h
      have hyone : (y (c, t) : G) = 1 := by
        have h := (y (c, t)).property
        simpa only [hempty, marked_empty, Subgroup.mem_bot] using h
      simp only [w, hxone, hyone, map_one, inv_one, mul_one]
      rfl
    have wzero := fin_weights_eq_zero L R hL hR dL dR w wsupport wrow wcol
    have hlocalFine : ∀ p, ((x p : E), (y p : G)) ∈ marked (fun i => (e i, g i)) (fine p) := by
      intro p
      apply (hlocal (fine p) (overlapScope_ordConnected L R hL hR p) _).mpr
      refine ⟨(x p).property, (y p).property, ?_⟩
      have heq : ε (x p) * (δ (y p))⁻¹ = 1 := by
        exact congrArg Additive.toMul (wzero p.1 p.2)
      exact mul_inv_eq_one.mp heq
    have hm := (mixed_component_profile e g fine hfE hfG
      (overlapScope_disjoint L R dL dR) hipE hipG x y).mpr hlocalFine
    rw [hxval, hyval, overlapScope_cover] at hm
    exact hm
  · apply le_inf
    · exact marked_mono _ Finset.inter_subset_left
    · exact marked_mono _ Finset.inter_subset_right

#print axioms mixed_coordinate_membership
#print axioms parity_overlap_intersection

end MathCompression.ParityMix
