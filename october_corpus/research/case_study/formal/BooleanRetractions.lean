import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Algebra.Group.Commute.Basic
import Mathlib.Tactic

/-!
Two components of the fiber-product construction. The first proves full
intersection of images from Boolean composition of endomorphisms. The
second proves the four-marker centralization identity in an arbitrary group.
Neither statement constructs a polytope, proves a lattice classification,
or formalizes the complete finite or infinite construction theorem.
-/

namespace MathCompression.BooleanRetractions

variable {G V : Type*} [Group G]

theorem range_intersection
    (e : Set V → G →* G)
    (hcomp : ∀ S T, (e S).comp (e T) = e (S ∩ T))
    (S T : Set V) :
    (e S).range ⊓ (e T).range = (e (S ∩ T)).range := by
  ext x
  constructor
  · rintro ⟨⟨a, ha⟩, ⟨b, hb⟩⟩
    refine ⟨b, ?_⟩
    have hid : (e S) ((e S) a) = (e S) a := by
      have h := congrArg (fun f : G →* G => f a) (hcomp S S)
      simpa only [MonoidHom.comp_apply, Set.inter_self] using h
    have h := congrArg (fun f : G →* G => f b) (hcomp S T)
    simpa only [MonoidHom.comp_apply, hb, ← ha, hid] using h.symm
  · rintro ⟨a, ha⟩
    constructor
    · refine ⟨(e T) a, ?_⟩
      have h := congrArg (fun f : G →* G => f a) (hcomp S T)
      simpa only [MonoidHom.comp_apply, ha] using h
    · refine ⟨(e S) a, ?_⟩
      have h := congrArg (fun f : G →* G => f a) (hcomp T S)
      simpa only [MonoidHom.comp_apply, Set.inter_comm T S, ha] using h

theorem four_marker_centralization
    (a b c d : G)
    (ha : a * a = 1) (hb : b * b = 1)
    (hc : c * c = 1) (hd : d * d = 1)
    (hac : Commute a c) (had : Commute a d) (hbd : Commute b d)
    (hef : Commute ((a * b)^2) ((c * d)^2)) :
    Commute ((c * b * a * b)^2) d ∧
      Commute ((a * b * c * b)^2) d := by
  have hai : a⁻¹ = a := inv_eq_of_mul_eq_one_left ha
  have hbi : b⁻¹ = b := inv_eq_of_mul_eq_one_left hb
  have hci : c⁻¹ = c := inv_eq_of_mul_eq_one_left hc
  have hdi : d⁻¹ = d := inv_eq_of_mul_eq_one_left hd
  let x := b * a * b
  let f := (c * d)^2
  have haf : Commute a f := (hac.mul_right had).pow_right 2
  have hxf : Commute x f := by
    have h := haf.inv_left.mul_left hef
    have hx : a⁻¹ * (a * b)^2 = x := by dsimp [x]; rw [pow_two]; group
    simpa only [hx] using h
  have hxd : Commute x d := (hbd.mul_left had).mul_left hbd
  have hxc : Commute x (c * d * c) := by
    have h := hxf.mul_right hxd
    have heq : f * d = c * d * c := by
      dsimp [f]
      rw [pow_two]
      calc
        c * d * (c * d) * d = c * d * c * (d * d) := by group
        _ = c * d * c := by rw [hd, mul_one]
    simpa only [heq] using h
  have hconj : Commute (c * x * c) d := by
    have h := hxc.conj c
    have heq : c * (c * d * c) * c⁻¹ = d := by
      calc
        c * (c * d * c) * c⁻¹ = (c * c) * d := by group
        _ = d := by rw [hc, one_mul]
    rw [heq, hci] at h
    exact h
  have hu : Commute ((c * b * a * b)^2) d := by
    have h := hconj.mul_left hxd
    have heq : (c * x * c) * x = (c * b * a * b)^2 := by
      dsimp [x]
      rw [pow_two]
      group
    simpa only [heq] using h
  refine ⟨hu, ?_⟩
  have h := hu.inv_left.conj b
  have hr : b * d * b⁻¹ = d := hbd.mul_inv_cancel
  have hl : b * ((c * b * a * b)^2)⁻¹ * b⁻¹ = (a * b * c * b)^2 := by
    simp only [pow_two, mul_inv_rev, hai, hbi, hci, ← mul_assoc, hb, one_mul]
  simpa only [hl, hr] using h

#print axioms range_intersection
#print axioms four_marker_centralization

end MathCompression.BooleanRetractions
