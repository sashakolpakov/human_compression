import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic

/-!
Two components of the descending support-factorization argument.

The first theorem transports actual subgroup disjointness to images when
the kernel splits into factors from the two subgroups. The second converts
the proved cardinality equality into an actual ordered factorization.

The lower-central Lie algebra, graded spanning, the quotient cardinality
calculation, and the descending induction are separate written arguments.
No full forest theorem is claimed here.
-/

namespace MathCompression.GradedSupport

variable {G Q : Type*} [Group G] [Group Q]

theorem common_image_trivial_of_split_kernel
    (A B : Subgroup G) (f : G →* Q)
    (hdisjoint : ∀ g : G, g ∈ A → g ∈ B → g = 1)
    (hkernel : ∀ n : G, f n = 1 →
      ∃ a : G, a ∈ A ∧ f a = 1 ∧
        ∃ b : G, b ∈ B ∧ f b = 1 ∧ n = a * b)
    {a b : G} (ha : a ∈ A) (hb : b ∈ B) (hab : f a = f b) :
    f a = 1 ∧ f b = 1 := by
  have hn : f (a * b⁻¹) = 1 := by simp [map_mul, map_inv, hab]
  obtain ⟨a₀, ha₀, hfa₀, b₀, hb₀, hfb₀, heq⟩ := hkernel _ hn
  have hcross : a₀⁻¹ * a = b₀ * b := by
    calc
      a₀⁻¹ * a = a₀⁻¹ * (a * b⁻¹) * b := by group
      _ = a₀⁻¹ * (a₀ * b₀) * b := by rw [heq]
      _ = b₀ * b := by group
  have hone : a₀⁻¹ * a = 1 := hdisjoint _
    (A.mul_mem (A.inv_mem ha₀) ha)
    (hcross ▸ B.mul_mem hb₀ hb)
  have haa : a = a₀ := by
    calc
      a = a₀ * (a₀⁻¹ * a) := by group
      _ = a₀ := by rw [hone, mul_one]
  have hfa : f a = 1 := by rw [haa, hfa₀]
  exact ⟨hfa, hab ▸ hfa⟩

theorem subgroup_product_injective
    (A B : Subgroup G)
    (hdisjoint : ∀ g : G, g ∈ A → g ∈ B → g = 1) :
    Function.Injective (fun p : A × B => (p.1 : G) * (p.2 : G)) := by
  intro p q hpq
  change (p.1 : G) * (p.2 : G) = (q.1 : G) * (q.2 : G) at hpq
  have hcross : (q.1 : G)⁻¹ * (p.1 : G) = (q.2 : G) * (p.2 : G)⁻¹ := by
    calc
      (q.1 : G)⁻¹ * (p.1 : G) =
          (q.1 : G)⁻¹ * ((p.1 : G) * (p.2 : G)) * (p.2 : G)⁻¹ := by group
      _ = (q.1 : G)⁻¹ * ((q.1 : G) * (q.2 : G)) * (p.2 : G)⁻¹ := by rw [hpq]
      _ = (q.2 : G) * (p.2 : G)⁻¹ := by group
  have hone : (q.1 : G)⁻¹ * (p.1 : G) = 1 := hdisjoint _
    (A.mul_mem (A.inv_mem q.1.property) p.1.property)
    (hcross ▸ B.mul_mem q.2.property (B.inv_mem p.2.property))
  have hfirst : (p.1 : G) = (q.1 : G) := by
    calc
      (p.1 : G) = (q.1 : G) * ((q.1 : G)⁻¹ * (p.1 : G)) := by group
      _ = (q.1 : G) := by rw [hone, mul_one]
  have hsecond : (p.2 : G) = (q.2 : G) := by
    apply mul_left_cancel (a := (q.1 : G))
    simpa only [hfirst] using hpq
  exact Prod.ext (Subtype.ext hfirst) (Subtype.ext hsecond)

theorem factorization_of_cardinality
    (A B D : Subgroup G) [Fintype A] [Fintype B] [Fintype D]
    (hA : A ≤ D) (hB : B ≤ D)
    (hdisjoint : ∀ g : G, g ∈ A → g ∈ B → g = 1)
    (hcard : Fintype.card D = Fintype.card A * Fintype.card B) :
    ∀ g : G, g ∈ D → ∃ a : G, a ∈ A ∧ ∃ b : G, b ∈ B ∧ g = a * b := by
  let mulInto : A × B → D := fun p =>
    ⟨(p.1 : G) * (p.2 : G), D.mul_mem (hA p.1.property) (hB p.2.property)⟩
  have hinj : Function.Injective mulInto := by
    intro p q hpq
    apply subgroup_product_injective A B hdisjoint
    exact congrArg Subtype.val hpq
  have hsize : Fintype.card (A × B) = Fintype.card D := by
    rw [Fintype.card_prod, hcard]
  have hsurj : Function.Surjective mulInto :=
    ((Fintype.bijective_iff_injective_and_card mulInto).2 ⟨hinj, hsize⟩).2
  intro g hg
  obtain ⟨p, hp⟩ := hsurj ⟨g, hg⟩
  exact ⟨p.1, p.1.property, p.2, p.2.property,
    (congrArg Subtype.val hp).symm⟩

#print axioms common_image_trivial_of_split_kernel
#print axioms subgroup_product_injective
#print axioms factorization_of_cardinality

end MathCompression.GradedSupport
