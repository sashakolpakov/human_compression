import FieldIntersection

/-!
The entrywise core of the general transvection/subfield intersection theorem.
There is no restriction on matrix dimension and no determinant hypothesis.
`shearEntry` is the expanded entry formula for (I-t E_rs) M (I+t E_rs),
where r ≠ s. The theorem proves that if M is over A, its conjugate is over B,
and t is outside A+B, then M is over A ∩ B and commutes with E_rs.
Actual matrix multiplication and the final SL-subgroup packaging are not hidden
inside this certificate: the expanded conjugation formula is explicit.
-/

namespace LeemansTransvection

open LeemansIntersection

variable {L : Type*} [Field L]
variable {ι : Type*} [DecidableEq ι]

/-- A nonzero slope over both fields would recover t as an additive field sum. -/
theorem slope_vanishes (A B : Subfield L) {t x c : L}
    (ht : ¬ InSum A B t) (hx : x ∈ A)
    (hcA : c ∈ A) (hcB : c ∈ B) (hy : x + t * c ∈ B) : c = 0 := by
  by_contra hc
  apply ht
  refine ⟨-x / c, A.div_mem (A.neg_mem hx) hcA,
    (x + t * c) / c, B.div_mem hy hcB, ?_⟩
  field_simp
  ring

def shearEntry (M : ι → ι → L) (r s : ι) (t : L) (i j : ι) : L :=
  M i j + t * (if j = s then M i r else 0)
    - t * (if i = r then M s j else 0)
    - t ^ 2 * (if i = r ∧ j = s then M s r else 0)

/-- All-dimensional field-intersection and transvection-centralizer certificate. -/
theorem transvection_intersection_entries (A B : Subfield L)
    {M : ι → ι → L} {r s : ι} (hrs : r ≠ s) {t : L}
    (ht : ¬ InSum A B t)
    (hM : ∀ i j, M i j ∈ A)
    (hC : ∀ i j, shearEntry M r s t i j ∈ B) :
    (∀ i j, M i j ∈ A ⊓ B) ∧
    (∀ i, i ≠ r → M i r = 0) ∧
    (∀ j, j ≠ s → M s j = 0) ∧ M r r = M s s := by
  have hsr : s ≠ r := Ne.symm hrs
  have hsrB : M s r ∈ B := by
    simpa [shearEntry, hrs, hsr] using hC s r
  have hsr0 : M s r = 0 := by
    have hz : -M s r = 0 := slope_vanishes A B ht (hM r r)
      (A.neg_mem (hM s r)) (B.neg_mem hsrB) (by
        simpa [shearEntry, hrs, hsr, sub_eq_add_neg, mul_neg] using hC r r)
    exact neg_eq_zero.mp hz
  have hcol : ∀ i, i ≠ r → M i r = 0 := by
    intro i hi
    have hirB : M i r ∈ B := by
      simpa [shearEntry, hrs, hi] using hC i r
    exact slope_vanishes A B ht (hM i s) (hM i r) hirB (by
      simpa [shearEntry, hi] using hC i s)
  have hrow : ∀ j, j ≠ s → M s j = 0 := by
    intro j hj
    have hsjB : M s j ∈ B := by
      simpa [shearEntry, hsr, hj] using hC s j
    have hz : -M s j = 0 := slope_vanishes A B ht (hM r j)
      (A.neg_mem (hM s j)) (B.neg_mem hsjB) (by
        simpa [shearEntry, hj, sub_eq_add_neg, mul_neg] using hC r j)
    exact neg_eq_zero.mp hz
  have hrrB : M r r ∈ B := by
    simpa [shearEntry, hrs, hsr0] using hC r r
  have hssB : M s s ∈ B := by
    simpa [shearEntry, hsr, hsr0] using hC s s
  have hdiag : M r r = M s s := by
    have hz : M r r - M s s = 0 := slope_vanishes A B ht (hM r s)
      (A.sub_mem (hM r r) (hM s s)) (B.sub_mem hrrB hssB) (by
        have hc := hC r s
        simp only [shearEntry, and_self, if_true, hsr0,
          mul_zero, sub_zero] at hc
        convert hc using 1; ring)
    exact sub_eq_zero.mp hz
  refine ⟨?_, hcol, hrow, hdiag⟩
  intro i j
  refine ⟨hM i j, ?_⟩
  by_cases hi : i = r
  · subst i
    by_cases hj : j = s
    · subst j
      simpa [shearEntry, hsr0, hdiag] using hC r s
    · simpa [shearEntry, hj, hrow j hj] using hC r j
  · by_cases hj : j = s
    · subst j
      simpa [shearEntry, hi, hcol i hi] using hC i s
    · simpa [shearEntry, hi, hj] using hC i j

/-- Explicit entries of M E_rs and E_rs M agree. -/
theorem transvection_commutator_entries (A B : Subfield L)
    {M : ι → ι → L} {r s : ι} (hrs : r ≠ s) {t : L}
    (ht : ¬ InSum A B t)
    (hM : ∀ i j, M i j ∈ A)
    (hC : ∀ i j, shearEntry M r s t i j ∈ B) :
    ∀ i j, (if j = s then M i r else 0) =
      (if i = r then M s j else 0) := by
  obtain ⟨_, hcol, hrow, hdiag⟩ :=
    transvection_intersection_entries A B hrs ht hM hC
  intro i j
  by_cases hi : i = r
  · subst i
    by_cases hj : j = s
    · subst j
      simpa using hdiag
    · simp [hj, hrow j hj]
  · by_cases hj : j = s
    · subst j
      simp [hi, hcol i hi]
    · simp [hi, hj]

/-- Exact intersection characterization in the full matrix algebra. -/
theorem transvection_intersection_iff (A B : Subfield L)
    {M : ι → ι → L} {r s : ι} (hrs : r ≠ s) {t : L}
    (ht : ¬ InSum A B t) (hM : ∀ i j, M i j ∈ A) :
    (∀ i j, shearEntry M r s t i j ∈ B) ↔
      ((∀ i j, M i j ∈ A ⊓ B) ∧
        ∀ i j, (if j = s then M i r else 0) =
          (if i = r then M s j else 0)) := by
  constructor
  · intro hC
    exact ⟨(transvection_intersection_entries A B hrs ht hM hC).1,
      transvection_commutator_entries A B hrs ht hM hC⟩
  · rintro ⟨hfield, hcomm⟩ i j
    have hsr0 : M s r = 0 := by
      simpa [Ne.symm hrs] using hcomm s s
    convert (hfield i j).2 using 1
    simp [shearEntry, hcomm i j, hsr0]

#print axioms slope_vanishes
#print axioms transvection_intersection_entries
#print axioms transvection_commutator_entries
#print axioms transvection_intersection_iff

end LeemansTransvection
