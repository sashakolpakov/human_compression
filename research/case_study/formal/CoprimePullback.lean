import Mathlib.GroupTheory.OrderOfElement

/-!+A subgroup with surjective projections onto two groups over a common base
is their full fiber product when the two kernel cardinalities are coprime.
The proof isolates one kernel by taking a coprime root and then a power.
This is a classical finite-group argument, not a priority claim.
-/

namespace MathCompression.CoprimePullback

variable {A B D : Type*} [Group A] [Group B] [Group D]

def fiberProduct (f : A →* D) (g : B →* D) : Subgroup (A × B) where
  carrier := {x | f x.1 = g x.2}
  one_mem' := by simp
  mul_mem' := by
    intro x y hx hy
    change f (x.1 * y.1) = g (x.2 * y.2)
    simpa only [map_mul] using congrArg₂ (· * ·) hx hy
  inv_mem' := by
    intro x hx
    change f x.1⁻¹ = g x.2⁻¹
    simpa only [map_inv] using congrArg Inv.inv hx

@[simp] theorem mem_fiberProduct (f : A →* D) (g : B →* D) (x : A × B) :
    x ∈ fiberProduct f g ↔ f x.1 = g x.2 := Iff.rfl

/-- Surjectivity to the second factor, together with coprimality, isolates
its entire kernel inside the subgroup. -/
theorem snd_kernel_mem (f : A →* D) (g : B →* D) (H : Subgroup (A × B))
    (hH : H ≤ fiberProduct f g)
    (hsnd : Function.Surjective fun x : H => x.val.2)
    (hcop : (Nat.card f.ker).Coprime (Nat.card g.ker))
    (b : B) (hb : g b = 1) : (1, b) ∈ H := by
  obtain ⟨z, hz⟩ :=
    (powCoprime (G := g.ker) hcop.symm).surjective ⟨b, hb⟩
  have hzB : (z : B) ^ Nat.card f.ker = b := congrArg Subtype.val hz
  obtain ⟨x, hx⟩ := hsnd (z : B)
  change x.val.2 = (z : B) at hx
  have ha : f x.val.1 = 1 := by
    have hc := hH x.property
    change f x.val.1 = g x.val.2 at hc
    rw [hx] at hc
    exact hc.trans z.property
  have haPow : x.val.1 ^ Nat.card f.ker = 1 := by
    exact congrArg Subtype.val (pow_card_eq_one' (x := (⟨x.val.1, ha⟩ : f.ker)))
  have hm := H.pow_mem x.property (Nat.card f.ker)
  have he : x.val ^ Nat.card f.ker = (1, b) := by
    apply Prod.ext
    · simpa using haPow
    · simpa [hx] using hzB
  rwa [he] at hm

/-- A subdirect subgroup over a common base is the full fiber product
when the two kernel cardinalities are coprime. -/
theorem eq_fiberProduct_of_coprime (f : A →* D) (g : B →* D)
    (H : Subgroup (A × B)) (hH : H ≤ fiberProduct f g)
    (hfst : Function.Surjective fun x : H => x.val.1)
    (hsnd : Function.Surjective fun x : H => x.val.2)
    (hcop : (Nat.card f.ker).Coprime (Nat.card g.ker)) :
    H = fiberProduct f g := by
  apply le_antisymm hH
  intro x hx
  obtain ⟨y, hy⟩ := hfst x.1
  change y.val.1 = x.1 at hy
  have hxy : g y.val.2 = g x.2 := by
    have hc := hH y.property
    change f y.val.1 = g y.val.2 at hc
    rw [hy] at hc
    exact hc.symm.trans hx
  have hk : g (y.val.2⁻¹ * x.2) = 1 := by
    simp only [map_mul, map_inv, hxy, inv_mul_cancel]
  have hm := H.mul_mem y.property
    (snd_kernel_mem f g H hH hsnd hcop (y.val.2⁻¹ * x.2) hk)
  have he : y.val * (1, y.val.2⁻¹ * x.2) = x := by
    apply Prod.ext
    · simpa using hy
    · simp
  rwa [he] at hm

/-- Paired generators generate the full compatible fiber product if their
two coordinate families generate and the covering kernel orders are coprime. -/
theorem closure_paired_generators (f : A →* D) (g : B →* D)
    {I : Type*} (a : I → A) (b : I → B)
    (hcompatible : ∀ i, f (a i) = g (b i))
    (hA : Subgroup.closure (Set.range a) = ⊤)
    (hB : Subgroup.closure (Set.range b) = ⊤)
    (hcop : (Nat.card f.ker).Coprime (Nat.card g.ker)) :
    Subgroup.closure (Set.range fun i => (a i, b i)) = fiberProduct f g := by
  let H : Subgroup (A × B) := Subgroup.closure (Set.range fun i => (a i, b i))
  have hH : H ≤ fiberProduct f g := by
    apply (Subgroup.closure_le _).mpr
    rintro x ⟨i, rfl⟩
    exact hcompatible i
  have hmapA : H.map (MonoidHom.fst A B) = ⊤ := by
    change (Subgroup.closure (Set.range fun i => (a i, b i))).map _ = ⊤
    rw [MonoidHom.map_closure, ← Set.range_comp]
    exact hA
  have hmapB : H.map (MonoidHom.snd A B) = ⊤ := by
    change (Subgroup.closure (Set.range fun i => (a i, b i))).map _ = ⊤
    rw [MonoidHom.map_closure, ← Set.range_comp]
    exact hB
  apply eq_fiberProduct_of_coprime f g H hH
  · intro x
    have hx : x ∈ H.map (MonoidHom.fst A B) := by rw [hmapA]; trivial
    obtain ⟨y, hy, he⟩ := hx
    exact ⟨⟨y, hy⟩, he⟩
  · intro x
    have hx : x ∈ H.map (MonoidHom.snd A B) := by rw [hmapB]; trivial
    obtain ⟨y, hy, he⟩ := hx
    exact ⟨⟨y, hy⟩, he⟩
  · exact hcop

#print axioms snd_kernel_mem
#print axioms eq_fiberProduct_of_coprime
#print axioms closure_paired_generators

end MathCompression.CoprimePullback
