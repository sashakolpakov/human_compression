import Mathlib.Tactic.Group
import Mathlib.Tactic.Convert
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.GroupTheory.Coset.Card

/-!
An exact, noncommutative word consequence of 35 explicitly listed cells in
the reviewed 128-point Gamma2 complement presentation. The cell orbit and
its geometric interpretation are separately checked written/computational
inputs. This file assumes the displayed cell relations and proves the
involution defect, with a finite odd-order specialization. It does not
formalize Sylow normalization or polytope recognition.

Generated from phase83_word_elimination.json by phase83_generate_lean.py.
No native evaluation or unproved declaration is used.
-/

namespace MathCompression.OddKernelWord

variable {K : Type*} [Group K]

private theorem solve_pos (a b x : K) (h : a * x * b = 1) :
    x = a⁻¹ * b⁻¹ := by
  calc
    x = a⁻¹ * (a * x * b) * b⁻¹ := by group
    _ = a⁻¹ * b⁻¹ := by rw [h]; simp

private theorem solve_neg (a b x : K) (h : a * x⁻¹ * b = 1) :
    x = b * a := by
  have hi := solve_pos a b x⁻¹ h
  calc
    x = (x⁻¹)⁻¹ := by group
    _ = (a⁻¹ * b⁻¹)⁻¹ := congrArg Inv.inv hi
    _ = b * a := by group

/-- The literal 35 cells sufficient for the defect identity. -/
def requiredCells : List (ℕ × ℕ × ℕ × ℕ) := [
  (9, 102, 128, 37),
  (4, 21, 85, 126),
  (4, 25, 85, 123),
  (1, 9, 39, 120),
  (17, 119, 20, 44),
  (2, 113, 10, 57),
  (21, 33, 126, 112),
  (8, 24, 16, 108),
  (1, 106, 5, 67),
  (3, 105, 54, 68),
  (2, 102, 10, 4),
  (1, 2, 5, 97),
  (25, 78, 123, 34),
  (10, 78, 53, 62),
  (8, 11, 17, 76),
  (17, 119, 40, 70),
  (49, 55, 53, 62),
  (2, 3, 50, 54),
  (5, 97, 7, 53),
  (2, 102, 50, 37),
  (7, 53, 16, 49),
  (16, 108, 19, 43),
  (2, 3, 97, 31),
  (29, 34, 97, 31),
  (17, 76, 20, 30),
  (6, 22, 39, 120),
  (8, 11, 16, 49),
  (4, 21, 102, 106),
  (67, 5, 126, 19),
  (68, 16, 105, 40),
  (70, 113, 119, 57),
  (43, 112, 108, 32),
  (32, 50, 112, 30),
  (55, 128, 62, 22),
  (30, 112, 76, 33)]

/-- These noncommutative cell equations force the marked defect to square to one. -/
theorem defect_square (t : ℕ → K)
    (hcells : ∀ a b c d, (a, b, c, d) ∈ requiredCells →
      (t d)⁻¹ * t c * (t a)⁻¹ * t b = 1) :
    ((t 1)⁻¹ * t 40) ^ 2 = 1 := by
  -- Original orbit row 69; elementary elimination 0.
  have e0 : t 128 = (t 37) * (t 102)⁻¹ * (t 9) := by
    have hh := hcells 9 102 128 37 (by decide)
    have hr : ((t 37)⁻¹) * (t 128) * ((t 9)⁻¹ * (t 102)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 37)⁻¹) ((t 9)⁻¹ * (t 102)) (t 128) hr
    convert hs using 1 ; group
  -- Original orbit row 26; elementary elimination 2.
  have e2 : t 126 = (t 85) * (t 4)⁻¹ * (t 21) := by
    have hh := hcells 4 21 85 126 (by decide)
    have hr : ((1 : K)) * (t 126)⁻¹ * ((t 85) * (t 4)⁻¹ * (t 21)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 85) * (t 4)⁻¹ * (t 21)) (t 126) hr
    convert hs using 1 ; group
  -- Original orbit row 29; elementary elimination 5.
  have e5 : t 123 = (t 85) * (t 4)⁻¹ * (t 25) := by
    have hh := hcells 4 25 85 123 (by decide)
    have hr : ((1 : K)) * (t 123)⁻¹ * ((t 85) * (t 4)⁻¹ * (t 25)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 85) * (t 4)⁻¹ * (t 25)) (t 123) hr
    convert hs using 1 ; group
  -- Original orbit row 2; elementary elimination 8.
  have e8 : t 120 = (t 39) * (t 1)⁻¹ * (t 9) := by
    have hh := hcells 1 9 39 120 (by decide)
    have hr : ((1 : K)) * (t 120)⁻¹ * ((t 39) * (t 1)⁻¹ * (t 9)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 39) * (t 1)⁻¹ * (t 9)) (t 120) hr
    convert hs using 1 ; group
  -- Original orbit row 134; elementary elimination 9.
  have e9 : t 119 = (t 17) * (t 20)⁻¹ * (t 44) := by
    have hh := hcells 17 119 20 44 (by decide)
    have hr : ((t 44)⁻¹ * (t 20) * (t 17)⁻¹) * (t 119) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 44)⁻¹ * (t 20) * (t 17)⁻¹) ((1 : K)) (t 119) hr
    convert hs using 1 ; group
  -- Original orbit row 14; elementary elimination 15.
  have e15 : t 113 = (t 2) * (t 10)⁻¹ * (t 57) := by
    have hh := hcells 2 113 10 57 (by decide)
    have hr : ((t 57)⁻¹ * (t 10) * (t 2)⁻¹) * (t 113) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 57)⁻¹ * (t 10) * (t 2)⁻¹) ((1 : K)) (t 113) hr
    convert hs using 1 ; group
  -- Original orbit row 163; elementary elimination 16.
  have e16 : t 112 = (t 85) * (t 4)⁻¹ * (t 33) := by
    have hh := hcells 21 33 126 112 (by decide)
    simp only [e2] at hh
    have hr : ((1 : K)) * (t 112)⁻¹ * ((t 85) * (t 4)⁻¹ * (t 33)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 85) * (t 4)⁻¹ * (t 33)) (t 112) hr
    convert hs using 1 ; group
  -- Original orbit row 58; elementary elimination 20.
  have e20 : t 108 = (t 16) * (t 8)⁻¹ * (t 24) := by
    have hh := hcells 8 24 16 108 (by decide)
    have hr : ((1 : K)) * (t 108)⁻¹ * ((t 16) * (t 8)⁻¹ * (t 24)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 16) * (t 8)⁻¹ * (t 24)) (t 108) hr
    convert hs using 1 ; group
  -- Original orbit row 6; elementary elimination 22.
  have e22 : t 106 = (t 1) * (t 5)⁻¹ * (t 67) := by
    have hh := hcells 1 106 5 67 (by decide)
    have hr : ((t 67)⁻¹ * (t 5) * (t 1)⁻¹) * (t 106) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 67)⁻¹ * (t 5) * (t 1)⁻¹) ((1 : K)) (t 106) hr
    convert hs using 1 ; group
  -- Original orbit row 22; elementary elimination 23.
  have e23 : t 105 = (t 3) * (t 54)⁻¹ * (t 68) := by
    have hh := hcells 3 105 54 68 (by decide)
    have hr : ((t 68)⁻¹ * (t 54) * (t 3)⁻¹) * (t 105) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 68)⁻¹ * (t 54) * (t 3)⁻¹) ((1 : K)) (t 105) hr
    convert hs using 1 ; group
  -- Original orbit row 12; elementary elimination 26.
  have e26 : t 102 = (t 2) * (t 10)⁻¹ * (t 4) := by
    have hh := hcells 2 102 10 4 (by decide)
    have hr : ((t 4)⁻¹ * (t 10) * (t 2)⁻¹) * (t 102) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 4)⁻¹ * (t 10) * (t 2)⁻¹) ((1 : K)) (t 102) hr
    convert hs using 1 ; group
  -- Original orbit row 0; elementary elimination 31.
  have e31 : t 97 = (t 5) * (t 1)⁻¹ * (t 2) := by
    have hh := hcells 1 2 5 97 (by decide)
    have hr : ((1 : K)) * (t 97)⁻¹ * ((t 5) * (t 1)⁻¹ * (t 2)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 5) * (t 1)⁻¹ * (t 2)) (t 97) hr
    convert hs using 1 ; group
  -- Original orbit row 197; elementary elimination 42.
  have e42 : t 85 = (t 34) * (t 78)⁻¹ * (t 4) := by
    have hh := hcells 25 78 123 34 (by decide)
    simp only [e5] at hh
    have hr : ((t 34)⁻¹) * (t 85) * ((t 4)⁻¹ * (t 78)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 34)⁻¹) ((t 4)⁻¹ * (t 78)) (t 85) hr
    convert hs using 1 ; group
  -- Original orbit row 77; elementary elimination 49.
  have e49 : t 78 = (t 10) * (t 53)⁻¹ * (t 62) := by
    have hh := hcells 10 78 53 62 (by decide)
    have hr : ((t 62)⁻¹ * (t 53) * (t 10)⁻¹) * (t 78) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 62)⁻¹ * (t 53) * (t 10)⁻¹) ((1 : K)) (t 78) hr
    convert hs using 1 ; group
  -- Original orbit row 57; elementary elimination 51.
  have e51 : t 76 = (t 17) * (t 8)⁻¹ * (t 11) := by
    have hh := hcells 8 11 17 76 (by decide)
    have hr : ((1 : K)) * (t 76)⁻¹ * ((t 17) * (t 8)⁻¹ * (t 11)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 17) * (t 8)⁻¹ * (t 11)) (t 76) hr
    convert hs using 1 ; group
  -- Original orbit row 135; elementary elimination 57.
  have e57 : t 70 = (t 40) * (t 20)⁻¹ * (t 44) := by
    have hh := hcells 17 119 40 70 (by decide)
    simp only [e9] at hh
    have hr : ((1 : K)) * (t 70)⁻¹ * ((t 40) * (t 20)⁻¹ * (t 44)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 40) * (t 20)⁻¹ * (t 44)) (t 70) hr
    convert hs using 1 ; group
  -- Original orbit row 389; elementary elimination 64.
  have e64 : t 62 = (t 53) * (t 49)⁻¹ * (t 55) := by
    have hh := hcells 49 55 53 62 (by decide)
    have hr : ((1 : K)) * (t 62)⁻¹ * ((t 53) * (t 49)⁻¹ * (t 55)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 53) * (t 49)⁻¹ * (t 55)) (t 62) hr
    convert hs using 1 ; group
  -- Original orbit row 10; elementary elimination 67.
  have e67 : t 54 = (t 50) * (t 2)⁻¹ * (t 3) := by
    have hh := hcells 2 3 50 54 (by decide)
    have hr : ((1 : K)) * (t 54)⁻¹ * ((t 50) * (t 2)⁻¹ * (t 3)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 50) * (t 2)⁻¹ * (t 3)) (t 54) hr
    convert hs using 1 ; group
  -- Original orbit row 37; elementary elimination 68.
  have e68 : t 53 = (t 7) * (t 1)⁻¹ * (t 2) := by
    have hh := hcells 5 97 7 53 (by decide)
    simp only [e31] at hh
    have hr : ((1 : K)) * (t 53)⁻¹ * ((t 7) * (t 1)⁻¹ * (t 2)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 7) * (t 1)⁻¹ * (t 2)) (t 53) hr
    convert hs using 1 ; group
  -- Original orbit row 13; elementary elimination 71.
  have e71 : t 50 = (t 37) * (t 4)⁻¹ * (t 10) := by
    have hh := hcells 2 102 50 37 (by decide)
    simp only [e26] at hh
    have hr : ((t 37)⁻¹) * (t 50) * ((t 10)⁻¹ * (t 4)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 37)⁻¹) ((t 10)⁻¹ * (t 4)) (t 50) hr
    convert hs using 1 ; group
  -- Original orbit row 53; elementary elimination 72.
  have e72 : t 49 = (t 16) * (t 1)⁻¹ * (t 2) := by
    have hh := hcells 7 53 16 49 (by decide)
    simp only [e68] at hh
    have hr : ((1 : K)) * (t 49)⁻¹ * ((t 16) * (t 1)⁻¹ * (t 2)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 16) * (t 1)⁻¹ * (t 2)) (t 49) hr
    convert hs using 1 ; group
  -- Original orbit row 127; elementary elimination 75.
  have e75 : t 43 = (t 19) * (t 8)⁻¹ * (t 24) := by
    have hh := hcells 16 108 19 43 (by decide)
    simp only [e20] at hh
    have hr : ((1 : K)) * (t 43)⁻¹ * ((t 19) * (t 8)⁻¹ * (t 24)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 19) * (t 8)⁻¹ * (t 24)) (t 43) hr
    convert hs using 1 ; group
  -- Original orbit row 11; elementary elimination 78.
  have e78 : t 31 = (t 5) * (t 1)⁻¹ * (t 3) := by
    have hh := hcells 2 3 97 31 (by decide)
    simp only [e31] at hh
    have hr : ((1 : K)) * (t 31)⁻¹ * ((t 5) * (t 1)⁻¹ * (t 3)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 5) * (t 1)⁻¹ * (t 3)) (t 31) hr
    convert hs using 1 ; group
  -- Original orbit row 227; elementary elimination 79.
  have e79 : t 34 = (t 29) * (t 2)⁻¹ * (t 3) := by
    have hh := hcells 29 34 97 31 (by decide)
    simp only [e31, e78] at hh
    have hr : ((t 3)⁻¹ * (t 2) * (t 29)⁻¹) * (t 34) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 3)⁻¹ * (t 2) * (t 29)⁻¹) ((1 : K)) (t 34) hr
    convert hs using 1 ; group
  -- Original orbit row 129; elementary elimination 80.
  have e80 : t 30 = (t 20) * (t 8)⁻¹ * (t 11) := by
    have hh := hcells 17 76 20 30 (by decide)
    simp only [e51] at hh
    have hr : ((1 : K)) * (t 30)⁻¹ * ((t 20) * (t 8)⁻¹ * (t 11)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 20) * (t 8)⁻¹ * (t 11)) (t 30) hr
    convert hs using 1 ; group
  -- Original orbit row 40; elementary elimination 83.
  have e83 : t 22 = (t 6) * (t 1)⁻¹ * (t 9) := by
    have hh := hcells 6 22 39 120 (by decide)
    simp only [e8] at hh
    have hr : ((t 9)⁻¹ * (t 1) * (t 6)⁻¹) * (t 22) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 9)⁻¹ * (t 1) * (t 6)⁻¹) ((1 : K)) (t 22) hr
    convert hs using 1 ; group
  -- Original orbit row 56; elementary elimination 85.
  have e85 : t 11 = (t 8) * (t 1)⁻¹ * (t 2) := by
    have hh := hcells 8 11 16 49 (by decide)
    simp only [e72] at hh
    have hr : ((t 2)⁻¹ * (t 1) * (t 8)⁻¹) * (t 11) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 2)⁻¹ * (t 1) * (t 8)⁻¹) ((1 : K)) (t 11) hr
    convert hs using 1 ; group
  -- Original orbit row 27; elementary elimination 86.
  have e86 : t 67 = (t 5) * (t 1)⁻¹ * (t 2) * (t 10)⁻¹ * (t 21) := by
    have hh := hcells 4 21 102 106 (by decide)
    simp only [e22, e26] at hh
    have hr : ((1 : K)) * (t 67)⁻¹ * ((t 5) * (t 1)⁻¹ * (t 2) * (t 10)⁻¹ * (t 21)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 5) * (t 1)⁻¹ * (t 2) * (t 10)⁻¹ * (t 21)) (t 67) hr
    convert hs using 1 ; group
  -- Original orbit row 529; elementary elimination 89.
  have e89 : t 55 = (t 16) * (t 19)⁻¹ * (t 29) * (t 2)⁻¹ * (t 3) := by
    have hh := hcells 67 5 126 19 (by decide)
    simp only [e2, e42, e49, e64, e72, e79, e86] at hh
    have hr : ((t 19)⁻¹ * (t 29) * (t 2)⁻¹ * (t 3)) * (t 55)⁻¹ * ((t 16)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((t 19)⁻¹ * (t 29) * (t 2)⁻¹ * (t 3)) ((t 16)) (t 55) hr
    convert hs using 1 ; group
  -- Original orbit row 536; elementary elimination 95.
  have e95 : t 40 = (t 2) * (t 10)⁻¹ * (t 4) * (t 37)⁻¹ * (t 16) := by
    have hh := hcells 68 16 105 40 (by decide)
    simp only [e23, e67, e71] at hh
    have hr : ((1 : K)) * (t 40)⁻¹ * ((t 2) * (t 10)⁻¹ * (t 4) * (t 37)⁻¹ * (t 16)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((1 : K)) ((t 2) * (t 10)⁻¹ * (t 4) * (t 37)⁻¹ * (t 16)) (t 40) hr
    convert hs using 1 ; group
  -- Original orbit row 559; elementary elimination 96.
  have e96 : t 37 = (t 16) * (t 17)⁻¹ * (t 4) := by
    have hh := hcells 70 113 119 57 (by decide)
    simp only [e9, e15, e57, e95] at hh
    have hr : ((t 57)⁻¹ * (t 17) * (t 16)⁻¹) * (t 37) * ((t 4)⁻¹ * (t 57)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 57)⁻¹ * (t 17) * (t 16)⁻¹) ((t 4)⁻¹ * (t 57)) (t 37) hr
    convert hs using 1 ; group
  -- Original orbit row 342; elementary elimination 98.
  have e98 : t 33 = (t 10) * (t 2)⁻¹ * (t 1) * (t 16)⁻¹ * (t 32) := by
    have hh := hcells 43 112 108 32 (by decide)
    simp only [e16, e20, e42, e49, e64, e72, e75, e79, e89] at hh
    have hr : ((t 32)⁻¹ * (t 16) * (t 1)⁻¹ * (t 2) * (t 10)⁻¹) * (t 33) * ((1 : K)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_pos ((t 32)⁻¹ * (t 16) * (t 1)⁻¹ * (t 2) * (t 10)⁻¹) ((1 : K)) (t 33) hr
    convert hs using 1 ; group
  -- Original orbit row 248; elementary elimination 102.
  have e102 : t 20 = (t 19) * (t 17)⁻¹ * (t 10) * (t 2)⁻¹ * (t 1) := by
    have hh := hcells 32 50 112 30 (by decide)
    simp only [e16, e42, e49, e64, e71, e72, e79, e80, e85, e89, e96, e98] at hh
    have hr : ((t 2)⁻¹ * (t 1)) * (t 20)⁻¹ * ((t 19) * (t 17)⁻¹ * (t 10)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((t 2)⁻¹ * (t 1)) ((t 19) * (t 17)⁻¹ * (t 10)) (t 20) hr
    convert hs using 1 ; group
  -- Original orbit row 439; elementary elimination 107.
  have e107 : t 17 = (t 10) * (t 2)⁻¹ * (t 1) * (t 6)⁻¹ * (t 7) := by
    have hh := hcells 55 128 62 22 (by decide)
    simp only [e0, e26, e64, e68, e72, e83, e96] at hh
    have hr : ((t 9)⁻¹ * (t 1) * (t 6)⁻¹ * (t 7)) * (t 17)⁻¹ * ((t 10) * (t 2)⁻¹ * (t 9)) = 1 := by
      convert hh using 1 ; group
    have hs := solve_neg ((t 9)⁻¹ * (t 1) * (t 6)⁻¹ * (t 7)) ((t 10) * (t 2)⁻¹ * (t 9)) (t 17) hr
    convert hs using 1 ; group
  have hh := hcells 30 112 76 33 (by decide)
  simp only [e16, e42, e49, e51, e64, e72, e79, e80, e89, e98, e102, e107] at hh
  have hr : (t 32)⁻¹ * (t 16) * (t 6)⁻¹ * (t 7) * (t 6)⁻¹ * (t 7) * (t 16)⁻¹ * (t 32) = 1 := by
    convert hh using 1 ; group
  have hs : ((t 6)⁻¹ * t 7) ^ 2 = 1 := by
    calc
      ((t 6)⁻¹ * t 7) ^ 2 = (t 16)⁻¹ * t 32 * ((t 32)⁻¹ * (t 16) * (t 6)⁻¹ * (t 7) * (t 6)⁻¹ * (t 7) * (t 16)⁻¹ * (t 32)) * (t 32)⁻¹ * t 16 := by simp only [pow_two]; group
      _ = 1 := by rw [hr]; group
  have hd : (t 1)⁻¹ * t 40 = (t 6)⁻¹ * t 7 := by
    simp only [e95, e96, e107]
    group
  rw [hd]
  exact hs

/-- In a finite group of odd order, the two distinguished entries coincide. -/
theorem defect_trivial_of_odd_card [Finite K] (t : ℕ → K)
    (hcells : ∀ a b c d, (a, b, c, d) ∈ requiredCells →
      (t d)⁻¹ * t c * (t a)⁻¹ * t b = 1)
    (hodd : Odd (Nat.card K)) : t 1 = t 40 := by
  have hs := defect_square t hcells
  have hd := orderOf_dvd_of_pow_eq_one hs
  have hone : (t 1)⁻¹ * t 40 = 1 := by
    rcases (Nat.dvd_prime Nat.prime_two).mp hd with h | h
    · exact orderOf_eq_one_iff.mp h
    · have htwo : 2 ∣ Nat.card K := by
        simpa only [h] using orderOf_dvd_natCard ((t 1)⁻¹ * t 40)
      exact False.elim ((Nat.not_even_iff_odd.mpr hodd) (even_iff_two_dvd.mpr htwo))
  exact inv_mul_eq_one.mp hone

#print axioms defect_square
#print axioms defect_trivial_of_odd_card

end MathCompression.OddKernelWord
