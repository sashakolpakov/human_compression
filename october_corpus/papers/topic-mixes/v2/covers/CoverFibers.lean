import Mathlib.GroupTheory.GroupAction.Basic
import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic.Abel

/-! Generic equivariant projections and actual voltage-lift maps. No graph
    connectivity, thinness, source family, or finite presentation is formalized. -/
namespace CoverFibers
variable {W Q X : Type*} [Group W] [MulAction W Q] [MulAction W X]

def orbit (S : Subgroup W) (q q' : Q) : Prop := ∃ g ∈ S, g • q = q'

/-- An actual equivariant projection reduces orbit intersections to one fiber. -/
theorem projection_intersection_from_fiber (π : Q → X)
    (hequiv : ∀ (g : W) (q : Q), π (g • q) = g • π q)
    (A B C : Subgroup W) (hCA : C ≤ A) (hCB : C ≤ B) (q : Q)
    (hbase : ∀ x, orbit A (π q) x → orbit B (π q) x → orbit C (π q) x)
    (hfiber : ∀ q', π q' = π q → orbit A q q' → orbit B q q' → orbit C q q') :
    ∀ q', orbit A q q' → orbit B q q' → orbit C q q' := by
  intro q' hA hB
  obtain ⟨a, ha, haq⟩ := hA
  obtain ⟨b, hb, hbq⟩ := hB
  have hax : a • π q = π q' := by rw [← hequiv, haq]
  have hbx : b • π q = π q' := by rw [← hequiv, hbq]
  obtain ⟨c, hc, hcx⟩ := hbase (π q') ⟨a, ha, hax⟩ ⟨b, hb, hbx⟩
  have hp : π (c⁻¹ • q') = π q := by
    rw [hequiv, ← hcx, inv_smul_smul]
  have hA' : orbit A q (c⁻¹ • q') := by
    exact ⟨c⁻¹ * a, A.mul_mem (A.inv_mem (hCA hc)) ha, by rw [mul_smul, haq]⟩
  have hB' : orbit B q (c⁻¹ • q') := by
    exact ⟨c⁻¹ * b, B.mul_mem (B.inv_mem (hCB hc)) hb, by rw [mul_smul, hbq]⟩
  obtain ⟨d, hd, hdq⟩ := hfiber (c⁻¹ • q') hp hA' hB'
  exact ⟨c * d, C.mul_mem hc hd, by rw [mul_smul, hdq, smul_inv_smul]⟩

theorem projection_intersection_iff_fiber (π : Q → X)
    (hequiv : ∀ (g : W) (q : Q), π (g • q) = g • π q)
    (A B C : Subgroup W) (hCA : C ≤ A) (hCB : C ≤ B) (q : Q)
    (hbase : ∀ x, orbit A (π q) x → orbit B (π q) x → orbit C (π q) x) :
    (∀ q', orbit A q q' → orbit B q q' → orbit C q q') ↔
    (∀ q', π q' = π q → orbit A q q' → orbit B q q' → orbit C q q') := by
  constructor
  · intro h q' _
    exact h q'
  · exact projection_intersection_from_fiber π hequiv A B C hCA hCB q hbase

section Voltage
variable {V K I : Type*} [AddCommGroup K]

def lift (φ : V ≃ V) (f : K ≃+ K) (h : V → K) (p : V × K) : V × K :=
  (φ p.1, f p.2 + h p.1)

theorem lift_bijective (φ : V ≃ V) (f : K ≃+ K) (h : V → K) :
    Function.Bijective (lift φ f h) := by
  constructor
  · rintro ⟨u, k⟩ ⟨v, l⟩ heq
    have huv : u = v := φ.injective (congrArg Prod.fst heq)
    subst v
    have hkl : f k + h u = f l + h u := congrArg Prod.snd heq
    have hkl' : k = l := f.injective (add_right_cancel hkl)
    subst l
    rfl
  · rintro ⟨v, l⟩
    refine ⟨(φ.symm v, f.symm (l - h (φ.symm v))), ?_⟩
    simp [lift]

/-- The displayed voltage equation gives commutation with every actual adjacency. -/
theorem lift_preserves_adjacency (φ : V ≃ V) (f : K ≃+ K) (h : V → K)
    (adj : I → V → V) (z : I → V → K)
    (hφ : ∀ i u, φ (adj i u) = adj i (φ u))
    (hz : ∀ i u, z i (φ u) = f (z i u) + h (adj i u) - h u)
    (i : I) (p : V × K) :
    lift φ f h (adj i p.1, z i p.1 + p.2) =
      (adj i (lift φ f h p).1, z i (lift φ f h p).1 + (lift φ f h p).2) := by
  apply Prod.ext
  · exact hφ i p.1
  · simp only [lift, map_add, hz]
    abel
end Voltage

#print axioms projection_intersection_from_fiber
#print axioms projection_intersection_iff_fiber
#print axioms lift_bijective
#print axioms lift_preserves_adjacency
end CoverFibers
