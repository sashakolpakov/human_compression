import Mathlib.Algebra.Group.Subgroup.Lattice
import Mathlib.Algebra.Group.Equiv.Basic
import Mathlib.Tactic.Group

namespace HumanCompression.PrefixCoordinates
variable {G : Type*} [Group G]

def prefixWord (s : ℕ → G) : ℕ → G
  | 0 => 1
  | n + 1 => prefixWord s n * s n

def segment (s : ℕ → G) (i : ℕ) : ℕ → G
  | 0 => 1
  | n + 1 => segment s i n * s (i + n)

/-- Every interval word is the difference of its two prefix coordinates. -/
theorem interval_telescope (s : ℕ → G) (i n : ℕ) :
    segment s i n = (prefixWord s i)⁻¹ * prefixWord s (i + n) := by
  induction n with
  | zero => simp [segment]
  | succ n ih =>
    rw [segment, ih, Nat.add_succ, prefixWord]
    group

/-- Taking successive differences is a left inverse of taking prefixes. -/
theorem recover_generators (s : ℕ → G) (i : ℕ) :
    (prefixWord s i)⁻¹ * prefixWord s (i + 1) = s i := by
  rw [prefixWord]
  group

/-- Taking prefixes is a right inverse on all normalized coordinate sequences. -/
theorem recover_coordinates (a : ℕ → G) (ha : a 0 = 1) (i : ℕ) :
    prefixWord (fun j => (a j)⁻¹ * a (j + 1)) i = a i := by
  induction i with
  | zero => simpa [prefixWord] using ha.symm
  | succ i ih => rw [prefixWord, ih]; group

def intervalSubgroup (s : ℕ → G) (J : Set ℕ) : Subgroup G :=
  Subgroup.closure {g | ∃ i n, i ∈ J ∧ i + n ∈ J ∧ g = segment s i n}

def differenceSubgroup (a : ℕ → G) (J : Set ℕ) : Subgroup G :=
  Subgroup.closure {g | ∃ i j, i ∈ J ∧ j ∈ J ∧ g = (a i)⁻¹ * a j}

/-- The actual subgroup diagrams agree; reversed endpoint pairs add inverses only. -/
theorem subgroup_dictionary (s : ℕ → G) (J : Set ℕ) :
    intervalSubgroup s J = differenceSubgroup (prefixWord s) J := by
  apply le_antisymm
  · apply (Subgroup.closure_le _).mpr
    rintro g ⟨i,n,hi,hj,rfl⟩
    exact Subgroup.subset_closure ⟨i,i+n,hi,hj,(interval_telescope s i n)⟩
  · apply (Subgroup.closure_le _).mpr
    rintro g ⟨i,j,hi,hj,rfl⟩
    by_cases h : i ≤ j
    · apply Subgroup.subset_closure
      refine ⟨i,j-i,hi,by simpa [Nat.add_sub_of_le h] using hj,?_⟩
      rw [interval_telescope, Nat.add_sub_of_le h]
    · have hji : j ≤ i := Nat.le_of_lt (Nat.lt_of_not_ge h)
      have hmem : (prefixWord s j)⁻¹ * prefixWord s i ∈ intervalSubgroup s J := by
        apply Subgroup.subset_closure
        refine ⟨j,i-j,hj,by simpa [Nat.add_sub_of_le hji] using hi,?_⟩
        rw [interval_telescope, Nat.add_sub_of_le hji]
      simpa using (intervalSubgroup s J).inv_mem hmem

/-- The full intersection property transfers through the concrete dictionary. -/
theorem intersection_transport (s : ℕ → G) :
    (∀ I J, intervalSubgroup s I ⊓ intervalSubgroup s J = intervalSubgroup s (I ∩ J)) ↔
    (∀ I J, differenceSubgroup (prefixWord s) I ⊓ differenceSubgroup (prefixWord s) J =
      differenceSubgroup (prefixWord s) (I ∩ J)) := by
  simp only [subgroup_dictionary]

/-- Inverting normalized involutory tails gives the classical reflected rotations. -/
theorem reflected_second (a b : G) (f : G ≃* G)
    (ha : f a = a⁻¹) (hb : f b = b) :
    f (a⁻¹ * b) = a ^ 2 * (a⁻¹ * b) := by
  rw [map_mul, map_inv, ha, hb]
  group

/-- Any automorphism which inverts a generating set has square equal to identity. -/
theorem inversion_automorphism_square (S : Set G)
    (hS : Subgroup.closure S = ⊤) (f : G ≃* G)
    (hf : ∀ x ∈ S, f x = x⁻¹) :
    ∀ x : G, f (f x) = x := by
  intro x
  have hx : x ∈ Subgroup.closure S := by rw [hS]; trivial
  induction hx using Subgroup.closure_induction with
  | mem x hx => rw [hf x hx, map_inv, hf x hx, inv_inv]
  | one => simp
  | mul x y _ _ hx hy => simp only [map_mul, hx, hy]
  | inv x _ hx => simp only [map_inv, hx]

#print axioms interval_telescope
#print axioms recover_generators
#print axioms recover_coordinates
#print axioms subgroup_dictionary
#print axioms intersection_transport
#print axioms reflected_second
#print axioms inversion_automorphism_square
end HumanCompression.PrefixCoordinates
