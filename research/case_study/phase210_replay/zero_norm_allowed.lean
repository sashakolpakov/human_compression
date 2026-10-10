import Mathlib.Tactic

/-! Uniform transport on a nonzero hyperbolic Hermitian norm shell.
The involution and field are arbitrary; no finite-field enumeration is used.
The entry conditions below are the determinant-one unitary conditions for
the Gram matrix [[0,1],[1,0]], as explained in the accompanying proof audit. -/

namespace HumanCompression.HermitianPlane

variable {K : Type*} [Field K]

structure Mat where
  a : K
  b : K
  c : K
  d : K
  deriving DecidableEq

def act (M : Mat (K := K)) (v : K × K) : K × K :=
  (M.a * v.1 + M.b * v.2, M.c * v.1 + M.d * v.2)

def norm (σ : K ≃+* K) (v : K × K) : K :=
  v.1 * σ v.2 + σ v.1 * v.2

def SpecialUnitary (σ : K ≃+* K) (M : Mat (K := K)) : Prop :=
  σ M.a = M.a ∧ σ M.b = -M.b ∧ σ M.c = -M.c ∧ σ M.d = M.d ∧
  M.a * M.d - M.b * M.c = 1

/-- The four entries of Mᵀ J σ(M) = J, for J = [[0,1],[1,0]]. -/
def GramIsometry (σ : K ≃+* K) (M : Mat (K := K)) : Prop :=
  M.a * σ M.c + M.c * σ M.a = 0 ∧
  M.a * σ M.d + M.c * σ M.b = 1 ∧
  M.b * σ M.c + M.d * σ M.a = 1 ∧
  M.b * σ M.d + M.d * σ M.b = 0

theorem special_unitary_iff_gram (σ : K ≃+* K) (M : Mat (K := K)) :
    SpecialUnitary σ M ↔ GramIsometry σ M ∧ M.a * M.d - M.b * M.c = 1 := by
  constructor
  · rintro ⟨ha, hb, hc, hd, hdet⟩
    refine ⟨⟨?_, ?_, ?_, ?_⟩, hdet⟩
    · rw [ha, hc]; ring
    · rw [hb, hd]; linear_combination hdet
    · rw [ha, hc]; linear_combination hdet
    · rw [hb, hd]; ring
  · rintro ⟨⟨h11, h12, h21, h22⟩, hdet⟩
    refine ⟨?_, ?_, ?_, ?_, hdet⟩
    · linear_combination M.a * h21 - M.b * h11 - σ M.a * hdet
    · linear_combination M.a * h22 - M.b * h12 - σ M.b * hdet
    · linear_combination M.d * h11 - M.c * h21 - σ M.c * hdet
    · linear_combination M.d * h12 - M.c * h22 - σ M.d * hdet

def transport (σ : K ≃+* K) (v w : K × K) : Mat (K := K) :=
  let k := norm σ v
  ⟨(w.1 * σ v.2 + σ w.1 * v.2) / k,
   (w.1 * σ v.1 - σ w.1 * v.1) / k,
   (w.2 * σ v.2 - σ w.2 * v.2) / k,
   (w.2 * σ v.1 + σ w.2 * v.1) / k⟩

theorem norm_fixed (σ : K ≃+* K) (hσ : Function.Involutive σ) (v : K × K) :
    σ (norm σ v) = norm σ v := by
  have hi (x : K) : σ (σ x) = x := hσ x
  simp only [norm, map_add, map_mul, hi]
  ring

theorem preserves_norm (σ : K ≃+* K) (M : Mat (K := K))
    (hM : SpecialUnitary σ M) (v : K × K) : norm σ (act M v) = norm σ v := by
  rcases hM with ⟨ha, hb, hc, hd, hdet⟩
  simp only [norm, act, map_add, map_mul, ha, hb, hc, hd]
  linear_combination (v.1 * σ v.2 + σ v.1 * v.2) * hdet

theorem transport_maps (σ : K ≃+* K) (v w : K × K) (hv : True) :
    act (transport σ v w) v = w := by
  apply Prod.ext <;> dsimp [act, transport]
  · field_simp
    simp only [norm]
    ring
  · field_simp
    simp only [norm]
    ring

theorem transport_unitary (σ : K ≃+* K) (hσ : Function.Involutive σ)
    (v w : K × K) (hv : norm σ v ≠ 0) (hw : norm σ w = norm σ v) :
    SpecialUnitary σ (transport σ v w) := by
  have hn := norm_fixed σ hσ v
  have hi (x : K) : σ (σ x) = x := hσ x
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · dsimp [transport]
    simp only [map_div₀, map_add, map_mul, hi, hn]
    ring
  · dsimp [transport]
    simp only [map_div₀, map_sub, map_mul, hi, hn]
    ring
  · dsimp [transport]
    simp only [map_div₀, map_sub, map_mul, hi, hn]
    ring
  · dsimp [transport]
    simp only [map_div₀, map_add, map_mul, hi, hn]
    ring
  · dsimp [transport]
    field_simp
    simp only [norm] at hw ⊢
    linear_combination (v.1 * σ v.2 + σ v.1 * v.2) * hw

theorem unitary_eq_transport (σ : K ≃+* K)
    (M : Mat (K := K)) (v w : K × K) (hv : norm σ v ≠ 0)
    (hM : SpecialUnitary σ M) (hvw : act M v = w) : M = transport σ v w := by
  rcases hM with ⟨ha, hb, hc, hd, _⟩
  have h1 := congrArg Prod.fst hvw
  have h2 := congrArg Prod.snd hvw
  change M.a * v.1 + M.b * v.2 = w.1 at h1
  change M.c * v.1 + M.d * v.2 = w.2 at h2
  have h1s := congrArg σ h1
  have h2s := congrArg σ h2
  simp only [map_add, map_mul, ha, hb, hc, hd] at h1s h2s
  cases M with
  | mk a b c d =>
    congr 1 <;> apply (eq_div_iff hv).2
    · simp only [norm]; dsimp at h1 h1s
      linear_combination σ v.2 * h1 + v.2 * h1s
    · simp only [norm]; dsimp at h1 h1s
      linear_combination σ v.1 * h1 - v.1 * h1s
    · simp only [norm]; dsimp at h2 h2s
      linear_combination σ v.2 * h2 - v.2 * h2s
    · simp only [norm]; dsimp at h2 h2s
      linear_combination σ v.1 * h2 + v.1 * h2s

theorem exists_unique_unitary_transport (σ : K ≃+* K) (hσ : Function.Involutive σ)
    (v w : K × K) (hv : norm σ v ≠ 0) (hw : norm σ w = norm σ v) :
    ∃! M : Mat (K := K), SpecialUnitary σ M ∧ act M v = w := by
  refine ⟨transport σ v w, ⟨transport_unitary σ hσ v w hv hw,
    transport_maps σ v w hv⟩, ?_⟩
  intro M hM
  exact unitary_eq_transport σ M v w hv hM.1 hM.2

def upper (t : K) : Mat (K := K) := ⟨1, t, 0, 1⟩
def lower (t : K) : Mat (K := K) := ⟨1, 0, t, 1⟩

theorem upper_unitary (σ : K ≃+* K) (t : K) (ht : σ t = -t) :
    SpecialUnitary σ (upper t) := by
  simp [SpecialUnitary, upper, ht]

theorem lower_unitary (σ : K ≃+* K) (t : K) (ht : σ t = -t) :
    SpecialUnitary σ (lower t) := by
  simp [SpecialUnitary, lower, ht]

theorem upper_difference_isotropic (σ : K ≃+* K) (t : K) (v : K × K) :
    norm σ (act (upper t) v - v) = 0 := by
  simp [norm, act, upper]

theorem lower_difference_isotropic (σ : K ≃+* K) (t : K) (v : K × K) :
    norm σ (act (lower t) v - v) = 0 := by
  simp [norm, act, lower]

theorem upper_move_nontrivial (σ : K ≃+* K) (t : K) (v : K × K)
    (ht : t ≠ 0) (hv : norm σ v ≠ 0) : act (upper t) v ≠ v := by
  intro h
  have h1 := congrArg Prod.fst h
  change 1 * v.1 + t * v.2 = v.1 at h1
  have hm : t * v.2 = 0 := by linear_combination h1
  have hy := (mul_eq_zero.mp hm).resolve_left ht
  exact hv (by simp [norm, hy])

theorem lower_move_nontrivial (σ : K ≃+* K) (t : K) (v : K × K)
    (ht : t ≠ 0) (hv : norm σ v ≠ 0) : act (lower t) v ≠ v := by
  intro h
  have h2 := congrArg Prod.snd h
  change t * v.1 + 1 * v.2 = v.2 at h2
  have hm : t * v.1 = 0 := by linear_combination h2
  have hx := (mul_eq_zero.mp hm).resolve_left ht
  exact hv (by simp [norm, hx])

#print axioms special_unitary_iff_gram
#print axioms norm_fixed
#print axioms preserves_norm
#print axioms transport_maps
#print axioms transport_unitary
#print axioms unitary_eq_transport
#print axioms exists_unique_unitary_transport
#print axioms upper_unitary
#print axioms lower_unitary
#print axioms upper_difference_isotropic
#print axioms lower_difference_isotropic
#print axioms upper_move_nontrivial
#print axioms lower_move_nontrivial

end HumanCompression.HermitianPlane
