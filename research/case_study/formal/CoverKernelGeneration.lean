import CoverKernelChains

/-!
Additional elementary statements for the general minimal-cover argument.
The geometric filling theorem and the polytope/group correspondence are not formalized.
The normal-generation and supply-of-powers hypotheses are explicit assumptions.
-/
namespace MathCompression.CoverKernelGeneration

open MathCompression.CoverKernelChains

/-- Inverse permutations supported on disjoint coordinate sets must be trivial.
The coordinates separate points, as the faces of a flag do. -/
theorem disjoint_coordinate_permutations
    {F ι β : Type*} (coord : ι → F → β)
    (hsep : ∀ x y, (∀ i, coord i x = coord i y) → x = y)
    (I J : Set ι) (hdisj : Disjoint I J) (a b : Equiv.Perm F)
    (ha : ∀ i ∉ I, ∀ x, coord i (a x) = coord i x)
    (hb : ∀ i ∉ J, ∀ x, coord i (b x) = coord i x)
    (hab : a * b = 1) : a = 1 ∧ b = 1 := by
  have hba : b * a = 1 := mul_eq_one_comm.mp hab
  have hea : a = 1 := by
    ext x
    apply hsep
    intro i
    change coord i (a x) = coord i x
    by_cases hi : i ∈ I
    · have hj : i ∉ J := fun hij => Set.disjoint_left.mp hdisj hi hij
      have h_eval : b (a x) = x := by
        simpa using congrArg (fun p : Equiv.Perm F => p x) hba
      simpa only [h_eval] using (hb i hj (a x)).symm
    · exact ha i hi x
  refine ⟨hea, ?_⟩
  simpa only [hea, one_mul] using hab

variable {W ι : Type*} [Group W]

/-- Injection on the union of proper parabolics preserves every intersection.
The hypothesis is stated as equality of words congruent modulo the kernel. -/
theorem intersectionProperty_of_injective_proper_union
    (P : Set ι → Subgroup W) (N : Subgroup W)
    (hbase : IntersectionProperty P ⊥)
    (hinj : ∀ I J : Set ι, I ≠ Set.univ → J ≠ Set.univ →
      ∀ a ∈ P I, ∀ b ∈ P J, a * b⁻¹ ∈ N → a = b) :
    IntersectionProperty P N := by
  classical
  intro I J a ha b hb hab
  by_cases hI : I = Set.univ
  · refine ⟨b, ?_, hab⟩
    simpa only [hI, Set.univ_inter] using hb
  by_cases hJ : J = Set.univ
  · refine ⟨a, ?_, ?_⟩
    · simpa only [hJ, Set.inter_univ] using ha
    · simp
  have heq := hinj I J hI hJ a ha b hb hab
  obtain ⟨c, hc, hac⟩ := hbase I J a ha b hb (by simp [heq])
  exact ⟨c, hc, (show (⊥ : Subgroup W) ≤ N from bot_le) hac⟩

/-- Each normal generator has two consecutive powers in admissible kernels.
These kernels and the exponent may depend on the generator. -/
def ConsecutivePowerSupply (P : Set ι → Subgroup W) (K : Subgroup W)
    (R : Set W) : Prop :=
  ∀ w ∈ R, ∃ m : ℕ, ∃ A B : Subgroup W,
    Admissible P K A ∧ Admissible P K B ∧ w ^ m ∈ A ∧ w ^ (m + 1) ∈ B

/-- The join of all admissible kernels is the target kernel, provided a normally
generating set has the stated supply of consecutive powers. -/
theorem admissible_join_eq_of_consecutive_powers
    (P : Set ι → Subgroup W) (K : Subgroup W) (R : Set W)
    (hgen : Subgroup.normalClosure R = K)
    (hsupply : ConsecutivePowerSupply P K R) :
    sSup {N : Subgroup W | Admissible P K N} = K := by
  let J : Subgroup W := sSup {N : Subgroup W | Admissible P K N}
  have hJK : J ≤ K := sSup_le (fun N hN => hN.2.1)
  have hnormal : J.Normal :=
    Subgroup.sSup_normal _ (fun N hN => hN.1)
  letI := hnormal
  have hRJ : R ⊆ J := by
    intro w hw
    change w ∈ J
    obtain ⟨m, A, B, hA, hB, hm, hnext⟩ := hsupply w hw
    have hmJ : w ^ m ∈ J := Subgroup.mem_sSup_of_mem hA hm
    have hnextJ : w ^ (m + 1) ∈ J := Subgroup.mem_sSup_of_mem hB hnext
    have hh := J.mul_mem hnextJ (J.inv_mem hmJ)
    simpa only [pow_succ', mul_inv_cancel_right] using hh
  have hKJ : K ≤ J := by
    rw [← hgen]
    exact Subgroup.normalClosure_le_normal hRJ
  exact le_antisymm hJK hKJ

/-- Under that supply, a unique maximal admissible kernel equals the target. -/
theorem unique_maximal_eq_target_of_consecutive_powers
    (P : Set ι → Subgroup W) (K M : Subgroup W) (R : Set W)
    (hgen : Subgroup.normalClosure R = K)
    (hsupply : ConsecutivePowerSupply P K R)
    (hM : Maximal (Admissible P K) M)
    (hunique : ∀ L, Maximal (Admissible P K) L → L = M) : M = K := by
  have hgreatest := unique_maximal_is_greatest P K M hM hunique
  have hjoin := admissible_join_eq_of_consecutive_powers P K R hgen hsupply
  apply le_antisymm hM.1.2.1
  rw [← hjoin]
  exact sSup_le hgreatest

/-- This is the final conditional implication; no geometric hypothesis is hidden. -/
theorem intersectionProperty_of_unique_maximal_and_power_supply
    (P : Set ι → Subgroup W) (K M : Subgroup W) (R : Set W)
    (hgen : Subgroup.normalClosure R = K)
    (hsupply : ConsecutivePowerSupply P K R)
    (hM : Maximal (Admissible P K) M)
    (hunique : ∀ L, Maximal (Admissible P K) L → L = M) :
    IntersectionProperty P K := by
  have heq := unique_maximal_eq_target_of_consecutive_powers P K M R hgen hsupply hM hunique
  simpa only [heq] using hM.1.2.2

#print axioms disjoint_coordinate_permutations
#print axioms intersectionProperty_of_injective_proper_union
#print axioms admissible_join_eq_of_consecutive_powers
#print axioms unique_maximal_eq_target_of_consecutive_powers
#print axioms intersectionProperty_of_unique_maximal_and_power_supply

end MathCompression.CoverKernelGeneration
