import Mathlib.GroupTheory.Index
import Mathlib.Tactic

/-! Formal interfaces for the odd-kernel construction. The cyclotomic lattice
and classification hypotheses are established in the accompanying written
proof, not postulated as axioms in this file. -/
namespace HumanCompression.OddKernelIntersection

variable {G : Type*} [Group G]

/-- The intersection step used for the prime dihedral facet. -/
theorem prime_index_intersection (C H J : Subgroup G) (p : ℕ)
    (hp : p.Prime) (hCH : C ≤ H) (hCJ : C ≤ J)
    (hindex : C.relIndex H = p) (hnot : ¬ H ≤ J) : H ⊓ J = C := by
  have hCI : C ≤ H ⊓ J := le_inf hCH hCJ
  have hprod := Subgroup.relIndex_mul_relIndex C (H ⊓ J) H hCI inf_le_left
  rw [hindex] at hprod
  have hdvd : C.relIndex (H ⊓ J) ∣ p := ⟨(H ⊓ J).relIndex H, hprod.symm⟩
  rcases (Nat.dvd_prime hp).mp hdvd with hfirst | hfirst
  · exact le_antisymm (Subgroup.relIndex_eq_one.mp hfirst) hCI
  · have hsecond : (H ⊓ J).relIndex H = 1 := by
      rw [hfirst] at hprod
      have := hp.pos
      nlinarith
    have hHI : H ≤ H ⊓ J := Subgroup.relIndex_eq_one.mp hsecond
    exact False.elim (hnot (le_trans hHI inf_le_right))

/-- Generation rules out containment in a proper second parabolic. -/
theorem prime_index_intersection_of_generate (C H J : Subgroup G) (p : ℕ)
    (hp : p.Prime) (hCH : C ≤ H) (hCJ : C ≤ J)
    (hindex : C.relIndex H = p) (hg : H ⊔ J = ⊤) (hj : J ≠ ⊤) : H ⊓ J = C := by
  apply prime_index_intersection C H J p hp hCH hCJ hindex
  intro h
  have hh : H ⊔ J = J := sup_eq_right.mpr h
  exact hj (hh.symm.trans hg)

/-- An element times an involution which inverts it is an involution. -/
theorem inverted_reflection_square (s h : G)
    (hinv : h * s * h = s⁻¹) : (s * h) * (s * h) = 1 := by
  calc
    (s * h) * (s * h) = s * (h * s * h) := by group
    _ = s * s⁻¹ := by rw [hinv]
    _ = 1 := mul_inv_cancel s

/-- The common involution cancels, giving the odd adjacent rotation. -/
theorem adjacent_reflection_product (s b h : G)
    (hinv : h * b * h = b⁻¹) : (s * h) * (b * h) = s * b⁻¹ := by
  calc
    (s * h) * (b * h) = s * (h * b * h) := by group
    _ = s * b⁻¹ := by rw [hinv]

/-- The source's faulty abelian marking has square x². -/
theorem fixed_inverted_marking_square (x y a : G)
    (hcomm : Commute x y) (ha : a * a = 1)
    (hx : a * x * a = x) (hy : a * y * a = y⁻¹) :
    (x * y * a) * (x * y * a) = x * x := by
  have hxy : a * (x * y) * a = x * y⁻¹ := by
    calc
      a * (x * y) * a = (a * x * a) * (a * y * a) := by
        calc
          _ = a * x * (a * a) * y * a := by rw [ha]; group
          _ = _ := by group
      _ = _ := by rw [hx,hy]
  calc
    (x * y * a) * (x * y * a) = x * y * (a * (x * y) * a) := by group
    _ = x * y * (x * y⁻¹) := by rw [hxy]
    _ = x * x := by rw [mul_assoc, ← mul_assoc y, hcomm.symm.eq]; group

#print axioms prime_index_intersection
#print axioms prime_index_intersection_of_generate
#print axioms inverted_reflection_square
#print axioms adjacent_reflection_product
#print axioms fixed_inverted_marking_square
end HumanCompression.OddKernelIntersection
