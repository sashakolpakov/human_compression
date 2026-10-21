import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Tactic

/-!
Parabolic-injective quotient transport. Right cosets use x*g⁻¹ ∈ P.
No finiteness, central kernel, or global surjectivity is assumed. The target
parabolics are exactly the subgroup images. The geometric consequences remain
in the separate written proof.
-/
namespace MathCompression.ParabolicQuotientTransport

variable {G H I : Type*} [Group G] [Group H]

def TypedCosetHelly (P : I → Subgroup G) : Prop :=
  ∀ (S : Set I) (g : I → G),
    (∀ i ∈ S, ∀ j ∈ S, ∃ x : G, x * (g i)⁻¹ ∈ P i ∧ x * (g j)⁻¹ ∈ P j) →
    ∃ x : G, ∀ i ∈ S, x * (g i)⁻¹ ∈ P i

theorem same_right_coset_difference (P : Subgroup G) (x y g : G)
    (hx : x * g⁻¹ ∈ P) (hy : y * g⁻¹ ∈ P) : x * y⁻¹ ∈ P := by
  have h := P.mul_mem hx (P.inv_mem hy)
  simpa [mul_assoc] using h

/-- Exact image meets and injectivity on each parabolic lift typed coset Helly.
The type set and the selected family may both be infinite. -/
theorem typed_helly_transport (P : I → Subgroup G) (f : G →* H)
    (hinj : ∀ i, Set.InjOn f (P i))
    (hmeet : ∀ i j, (P i ⊓ P j).map f = (P i).map f ⊓ (P j).map f)
    (hdown : TypedCosetHelly (fun i => (P i).map f)) :
    TypedCosetHelly P := by
  classical
  intro S g hpair
  by_cases hS : S.Nonempty
  · obtain ⟨k, hk⟩ := hS
    have hpairdown : ∀ i ∈ S, ∀ j ∈ S, ∃ x : H,
        x * (f (g i))⁻¹ ∈ (P i).map f ∧ x * (f (g j))⁻¹ ∈ (P j).map f := by
      intro i hi j hj
      obtain ⟨x, hxi, hxj⟩ := hpair i hi j hj
      refine ⟨f x, ?_, ?_⟩
      · exact Subgroup.mem_map.mpr ⟨x * (g i)⁻¹, hxi, by simp⟩
      · exact Subgroup.mem_map.mpr ⟨x * (g j)⁻¹, hxj, by simp⟩
    obtain ⟨y, hy⟩ := hdown S (fun i => f (g i)) hpairdown
    obtain ⟨t, ht, hft⟩ := Subgroup.mem_map.mp (hy k hk)
    let x := t * g k
    have hfx : f x = y := by
      dsimp [x]
      rw [map_mul, hft]
      simp [mul_assoc]
    have hxk : x * (g k)⁻¹ ∈ P k := by simpa [x, mul_assoc] using ht
    refine ⟨x, ?_⟩
    intro i hi
    obtain ⟨a, hai, hak⟩ := hpair i hi k hk
    have hxak : x * a⁻¹ ∈ P k := same_right_coset_difference (P k) x a (g k) hxk hak
    have hfai : f a * (f (g i))⁻¹ ∈ (P i).map f :=
      Subgroup.mem_map.mpr ⟨a * (g i)⁻¹, hai, by simp⟩
    have hxaimage : f (x * a⁻¹) ∈ (P i).map f ⊓ (P k).map f := by
      constructor
      · simpa [map_mul, map_inv, hfx] using
          same_right_coset_difference ((P i).map f) y (f a) (f (g i)) (hy i hi) hfai
      · exact Subgroup.mem_map.mpr ⟨x * a⁻¹, hxak, rfl⟩
    rw [← hmeet i k] at hxaimage
    obtain ⟨c, hc, hfc⟩ := Subgroup.mem_map.mp hxaimage
    have hcx : c = x * a⁻¹ := hinj k hc.2 hxak hfc
    have hxai : x * a⁻¹ ∈ P i := hcx ▸ hc.1
    have hh := (P i).mul_mem hxai hai
    simpa [mul_assoc] using hh
  · refine ⟨1, ?_⟩
    intro i hi
    exact False.elim (hS ⟨i, hi⟩)

/-- A monotone marked-subgroup family with P(univ)=top has full IP whenever
its image has IP and the map is injective on every maximal marked parabolic. -/
theorem marked_intersection_transport (P : Set I → Subgroup G) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : ∀ i : I, Set.InjOn f (P ({i}ᶜ)))
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f) :
    ∀ S T : Set I, P S ⊓ P T = P (S ∩ T) := by
  classical
  intro S T
  by_cases hS : S = Set.univ
  · simp [hS, htop]
  obtain ⟨i, hi⟩ : ∃ i, i ∉ S := by
    by_contra hh
    apply hS
    apply Set.eq_univ_of_forall
    intro i
    by_contra hi
    exact hh ⟨i, hi⟩
  have hsub : S ⊆ ({i}ᶜ : Set I) := by
    intro j hj
    simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
    rintro rfl
    exact hi hj
  apply le_antisymm
  · intro x hx
    have hfx : f x ∈ (P S).map f ⊓ (P T).map f :=
      ⟨Subgroup.mem_map.mpr ⟨x, hx.1, rfl⟩, Subgroup.mem_map.mpr ⟨x, hx.2, rfl⟩⟩
    rw [himages] at hfx
    obtain ⟨c, hc, hfc⟩ := Subgroup.mem_map.mp hfx
    have hcS : c ∈ P S := hmono _ _ Set.inter_subset_left hc
    have hcx : c = x := hinj i (hmono S _ hsub hcS) (hmono S _ hsub hx.1) hfc
    exact hcx ▸ hc
  · exact le_inf (hmono _ _ Set.inter_subset_left) (hmono _ _ Set.inter_subset_right)

/-- Combined subgroup-IP and typed-Helly transport for the maximal parabolics
of a marked-subgroup family. It includes arbitrary groups and arbitrary rank. -/
theorem marked_quotient_transport (P : Set I → Subgroup G) (f : G →* H)
    (hmono : ∀ S T : Set I, S ⊆ T → P S ≤ P T)
    (htop : P Set.univ = ⊤)
    (hinj : ∀ i : I, Set.InjOn f (P ({i}ᶜ)))
    (himages : ∀ S T : Set I,
      (P S).map f ⊓ (P T).map f = (P (S ∩ T)).map f)
    (hhelly : TypedCosetHelly (fun i : I => (P ({i}ᶜ)).map f)) :
    (∀ S T : Set I, P S ⊓ P T = P (S ∩ T)) ∧
      TypedCosetHelly (fun i : I => P ({i}ᶜ)) := by
  have hip := marked_intersection_transport P f hmono htop hinj himages
  refine ⟨hip, typed_helly_transport (fun i : I => P ({i}ᶜ)) f hinj ?_ hhelly⟩
  intro i j
  rw [hip]
  exact (himages _ _).symm

#print axioms same_right_coset_difference
#print axioms typed_helly_transport
#print axioms marked_intersection_transport
#print axioms marked_quotient_transport
end MathCompression.ParabolicQuotientTransport
