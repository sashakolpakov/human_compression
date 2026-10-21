import Mathlib.GroupTheory.FreeGroup.Basic
import Mathlib.Algebra.Group.Subgroup.Map

/-!
The complete mathematical scope is free-basis permutation transport of the
maximal standard parabolic subgroups. This does not formalize coset Helly,
residual connectedness, or the complete chamber-normalizer argument.
-/

namespace HumanCompression.Representation

variable {ι : Type*}

def basisComplement (i : ι) : Subgroup (FreeGroup ι) :=
  Subgroup.closure (FreeGroup.of '' {j : ι | j ≠ i})

theorem basisPermutation_on_generator (σ : Equiv.Perm ι) (i : ι) :
    FreeGroup.freeGroupCongr σ (FreeGroup.of i) = FreeGroup.of (σ i) := by
  simp [FreeGroup.freeGroupCongr]

theorem basisPermutation_transports_complement (σ : Equiv.Perm ι) (i : ι) :
    (basisComplement i).map (FreeGroup.freeGroupCongr σ).toMonoidHom =
      basisComplement (σ i) := by
  unfold basisComplement
  rw [MonoidHom.map_closure]
  congr 1
  ext x
  constructor
  · rintro ⟨y, ⟨j, hj, rfl⟩, rfl⟩
    exact ⟨σ j, fun h => hj (σ.injective h), (basisPermutation_on_generator σ j).symm⟩
  · rintro ⟨j, hj, rfl⟩
    refine ⟨FreeGroup.of (σ.symm j), ⟨σ.symm j, ?_, rfl⟩, ?_⟩
    · intro h
      apply hj
      simpa using congrArg σ h
    · simp

theorem basisPermutation_faithful :
    Function.Injective (fun σ : Equiv.Perm ι => FreeGroup.freeGroupCongr σ) := by
  intro σ τ h
  apply Equiv.ext
  intro i
  have hh := congrArg (fun f : FreeGroup ι ≃* FreeGroup ι => f (FreeGroup.of i)) h
  exact FreeGroup.of_injective (by simpa [basisPermutation_on_generator] using hh)

#print axioms basisPermutation_on_generator
#print axioms basisPermutation_transports_complement
#print axioms basisPermutation_faithful

end HumanCompression.Representation
