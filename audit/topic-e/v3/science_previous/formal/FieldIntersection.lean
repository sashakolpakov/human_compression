import Mathlib.Algebra.Field.Subfield.Basic
import Mathlib.Tactic

/-!
Algebraic core of the proposed proof of Leemans--Moerenhout--O'Reilly-Regueiro
Conjecture 6.2. No finite-field or projective-group instantiation is hidden:
the Frobenius fixed-field facts are explicit hypotheses. The last theorem
formalizes the four matrix-entry conditions for intersection of conjugate
SL(2) subfield groups.
-/

namespace LeemansIntersection

variable {L : Type*} [Field L]

def InSum (A B : Subfield L) (z : L) : Prop :=
  ∃ x ∈ A, ∃ y ∈ B, z = x + y

/-- Frobenius subtraction proves the product obstruction. -/
theorem product_in_sum (A B : Subfield L) (τ : L ≃+* L)
    (hfixA : ∀ x ∈ A, τ x = x)
    (hmapB : ∀ y ∈ B, τ y ∈ B)
    (hfixedB : ∀ y ∈ B, τ y = y → y ∈ A)
    {x y : L} (hx : x ∈ A) (hy : y ∈ B)
    (hxy : InSum A B (x * y)) : x ∈ B ∨ y ∈ A := by
  by_cases hfix : τ y = y
  · exact Or.inr (hfixedB y hy hfix)
  · left
    rcases hxy with ⟨a, ha, b, hb, h⟩
    have ht := congrArg τ h
    simp only [map_mul, map_add, hfixA x hx, hfixA a ha] at ht
    have hid : x * (τ y - y) = τ b - b := by
      linear_combination ht - h
    have hn : τ y - y ≠ 0 := sub_ne_zero.mpr hfix
    have heq : x = (τ b - b) / (τ y - y) := (eq_div_iff hn).2 hid
    rw [heq]
    exact B.div_mem (B.sub_mem (hmapB b hb) hb) (B.sub_mem (hmapB y hy) hy)

/-- A square root of a sum of two genuinely different field components
cannot belong to the additive sum of the fields. -/
theorem square_root_not_in_sum (A B : Subfield L) (htwo : (2 : L) ≠ 0)
    (hproduct : ∀ {x y : L}, x ∈ A → y ∈ B →
      InSum A B (x * y) → x ∈ B ∨ y ∈ A)
    {a b z : L} (ha : a ∈ A) (hb : b ∈ B)
    (haB : a ∉ B) (hbA : b ∉ A) (hsq : z ^ 2 = a + b) :
    ¬ InSum A B z := by
  rintro ⟨x, hx, y, hy, hz⟩
  have hxy : InSum A B (x * y) := by
    refine ⟨(a - x ^ 2) / 2, A.div_mem (A.sub_mem ha (A.pow_mem hx 2))
      (by simpa using A.add_mem A.one_mem A.one_mem), (b - y ^ 2) / 2,
      B.div_mem (B.sub_mem hb (B.pow_mem hy 2))
        (by simpa using B.add_mem B.one_mem B.one_mem), ?_⟩
    rw [hz] at hsq
    field_simp
    linear_combination hsq
  rcases hproduct hx hy hxy with hxB | hyA
  · have hzB : z ∈ B := hz ▸ B.add_mem hxB hy
    apply haB
    have haeq : a = z ^ 2 - b := by linear_combination -hsq
    rw [haeq]
    exact B.sub_mem (B.pow_mem hzB 2) hb
  · have hzA : z ∈ A := hz ▸ A.add_mem hx hyA
    apply hbA
    have hbeq : b = z ^ 2 - a := by linear_combination -hsq
    rw [hbeq]
    exact A.sub_mem (A.pow_mem hzA 2) ha

/-- The square-root obstruction with explicit Frobenius hypotheses. -/
theorem square_root_not_in_sum_of_automorphism (A B : Subfield L)
    (τ : L ≃+* L) (htwo : (2 : L) ≠ 0)
    (hfixA : ∀ x ∈ A, τ x = x)
    (hmapB : ∀ y ∈ B, τ y ∈ B)
    (hfixedB : ∀ y ∈ B, τ y = y → y ∈ A)
    {a b z : L} (ha : a ∈ A) (hb : b ∈ B)
    (haB : a ∉ B) (hbA : b ∉ A) (hsq : z ^ 2 = a + b) :
    ¬ InSum A B z :=
  square_root_not_in_sum A B htwo
    (fun hx hy hxy => product_in_sum A B τ hfixA hmapB hfixedB hx hy hxy)
    ha hb haB hbA hsq

/-- Entrywise SL(2) intersection certificate. A determinant-one matrix over A
whose conjugate by U(t) is over B must be a signed unipotent over A ∩ B,
provided t lies outside the additive sum A+B. -/
theorem conjugate_intersection_entries (A B : Subfield L) {t a b c d : L}
    (ht : ¬ InSum A B t)
    (ha : a ∈ A) (hb : b ∈ A) (hc : c ∈ A) (hd : d ∈ A)
    (ha' : a - t * c ∈ B)
    (hb' : b + t * (a - d) - t ^ 2 * c ∈ B)
    (hc' : c ∈ B) (hd' : d + t * c ∈ B)
    (hdet : a * d - b * c = 1) :
    c = 0 ∧ a = d ∧ b ∈ A ⊓ B ∧ (a = 1 ∨ a = -1) := by
  have hc0 : c = 0 := by
    by_contra hcn
    apply ht
    refine ⟨a / c, A.div_mem ha hc, -(a - t * c) / c,
      B.div_mem (B.neg_mem ha') hc', ?_⟩
    field_simp
    ring
  have haB : a ∈ B := by simpa [hc0] using ha'
  have hdB : d ∈ B := by simpa [hc0] using hd'
  have hbB : b + t * (a - d) ∈ B := by simpa [hc0] using hb'
  have had : a = d := by
    by_contra hn
    have hdiff : a - d ≠ 0 := sub_ne_zero.mpr hn
    apply ht
    refine ⟨-b / (a - d), A.div_mem (A.neg_mem hb) (A.sub_mem ha hd),
      (b + t * (a - d)) / (a - d),
      B.div_mem hbB (B.sub_mem haB hdB), ?_⟩
    field_simp
    ring
  have hbfinal : b ∈ B := by simpa [had] using hbB
  have ha2 : a * a = 1 := by simpa [hc0, ← had] using hdet
  exact ⟨hc0, had, ⟨hb, hbfinal⟩, mul_self_eq_one_iff.mp ha2⟩

#print axioms product_in_sum
#print axioms square_root_not_in_sum_of_automorphism
#print axioms conjugate_intersection_entries

/-- The entry equations for a conjugator fixing gamma and inverting alpha
force that conjugator to be zero when the discriminant root is nonzero.
This is the linear-algebra obstruction used in the chirality argument. -/
theorem reversing_entries_vanish {u v D x y z w : L}
    (htwo : (2 : L) ≠ 0) (hu : u ≠ 0) (hD : D ≠ 0)
    (hcomm00 : D * y = D * z)
    (hcomm01 : D * x + 4 * v * y = D * w)
    (hinv00 : (u - 2) * y = -(u + 2) * z)
    (hinv01 : (u + 2) * (x + w) = 0)
    (hinv10 : (u - 2) * (x + w) = 0) :
    x = 0 ∧ y = 0 ∧ z = 0 ∧ w = 0 := by
  have hyz : y = z := mul_left_cancel₀ hD hcomm00
  have hyprod : (2 * u) * y = 0 := by
    rw [← hyz] at hinv00
    linear_combination hinv00
  have hy : y = 0 := (mul_eq_zero.mp hyprod).resolve_left (mul_ne_zero htwo hu)
  have hz : z = 0 := hyz.symm.trans hy
  have hxw : x = w := by
    apply mul_left_cancel₀ hD
    simpa [hy] using hcomm01
  have hfour : (4 : L) ≠ 0 := by
    have := mul_ne_zero htwo htwo
    norm_num at this ⊢
    exact this
  have hsumprod : (4 : L) * (x + w) = 0 := by
    linear_combination hinv01 - hinv10
  have hsum : x + w = 0 := (mul_eq_zero.mp hsumprod).resolve_left hfour
  have hxprod : (2 : L) * x = 0 := by
    rw [← hxw] at hsum
    linear_combination hsum
  have hx : x = 0 := (mul_eq_zero.mp hxprod).resolve_left htwo
  exact ⟨hx, hy, hz, hxw.symm.trans hx⟩

#print axioms reversing_entries_vanish

end LeemansIntersection
