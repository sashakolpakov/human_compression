import Mathlib.Algebra.Group.Conj
import Mathlib.Tactic

namespace HumanCompression.PeriodSignObstruction
variable {G : Type*} [Group G]

/-- The two literal source words, simplified using involutivity. -/
def firstWord (a b c : G) : G := (b * a * b * c * b * a) ^ 2
def secondWord (a b c : G) : G := (b * c * b * a * b * a) ^ 2

/-- Conjugation by a reverses the other period word. -/
theorem literal_word_conjugacy (a b c : G)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1) :
    a⁻¹ * firstWord a b c * a = (secondWord a b c)⁻¹ := by
  have hia : a⁻¹ = a := inv_eq_of_mul_eq_one_right ha
  have hib : b⁻¹ = b := inv_eq_of_mul_eq_one_right hb
  have hic : c⁻¹ = c := inv_eq_of_mul_eq_one_right hc
  have hbase : a * (b * a * b * c * b * a) * a =
      (b * c * b * a * b * a)⁻¹ := by
    calc
      _ = a * b * a * b * c * b * (a * a) := by group
      _ = a * b * a * b * c * b := by rw [ha, mul_one]
      _ = _ := by simp only [mul_inv_rev, hia, hib, hic, mul_assoc]
  unfold firstWord secondWord
  rw [hia]
  calc
    _ = (a * (b * a * b * c * b * a) * a) ^ 2 := by
      simpa only [hia] using (conj_pow (i := 2) (a := a)
        (b := b * a * b * c * b * a)).symm
    _ = ((b * c * b * a * b * a)⁻¹) ^ 2 := by rw [hbase]
    _ = _ := inv_pow _ _

/-- Equal rather than opposite period signs force an extra rotation relation. -/
theorem equal_period_signs_collapse (a u v x : G) (k : ℕ)
    (hconj : a⁻¹ * u * a = v⁻¹)
    (hcomm : Commute a (x ^ 4))
    (hu : u ^ (2 * k) = x ^ (4 * k))
    (hv : v ^ (2 * k) = x ^ (4 * k)) : x ^ (8 * k) = 1 := by
  have hcommk : Commute a (x ^ (4 * k)) := by
    simpa only [pow_mul] using hcomm.pow_right k
  have hpow : a⁻¹ * u ^ (2 * k) * a = (v ^ (2 * k))⁻¹ := by
    calc
      _ = (a⁻¹ * u * a) ^ (2 * k) := by
        simpa only [inv_inv] using (conj_pow (i := 2 * k) (a := a⁻¹) (b := u)).symm
      _ = (v⁻¹) ^ (2 * k) := by rw [hconj]
      _ = _ := inv_pow _ _
  rw [hu, hv] at hpow
  have hleft : a⁻¹ * x ^ (4 * k) * a = x ^ (4 * k) := by
    rw [hcommk.inv_left.eq]
    group
  rw [hleft] at hpow
  calc
    x ^ (8 * k) = x ^ (4 * k) * x ^ (4 * k) := by
      rw [← pow_add]; congr 1; omega
    _ = (x ^ (4 * k))⁻¹ * x ^ (4 * k) := by rw [← hpow]
    _ = 1 := inv_mul_cancel _

/-- Direct specialization to the actual literal source words. -/
theorem source_period_sign_obstruction (a b c : G) (k : ℕ)
    (ha : a * a = 1) (hb : b * b = 1) (hc : c * c = 1)
    (hcomm : Commute a ((b * c) ^ 4))
    (hfirst : ((b * ((b * a)⁻¹ * c * (b * a))) ^ 2) ^ (2 * k) =
      (b * c) ^ (4 * k))
    (hsecond : (((b⁻¹ * c * b) * (a⁻¹ * b * a)) ^ 2) ^ (2 * k) =
      (b * c) ^ (4 * k)) :
    (b * c) ^ (8 * k) = 1 := by
  have hia : a⁻¹ = a := inv_eq_of_mul_eq_one_right ha
  have hib : b⁻¹ = b := inv_eq_of_mul_eq_one_right hb
  apply equal_period_signs_collapse a (firstWord a b c) (secondWord a b c) (b * c) k
    (literal_word_conjugacy a b c ha hb hc) hcomm
  · simpa only [firstWord, mul_inv_rev, hia, hib, mul_assoc] using hfirst
  · simpa only [secondWord, hia, hib, mul_assoc] using hsecond

#print axioms literal_word_conjugacy
#print axioms equal_period_signs_collapse
#print axioms source_period_sign_obstruction
end HumanCompression.PeriodSignObstruction
