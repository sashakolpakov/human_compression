import TriangleWreathQuotient

/-!
The direct four-involution wreath quotient of the exact universal presentation.
Triangle-group infinitude remains an explicit hypothesis of the transfer theorem.
-/

set_option linter.unusedSimpArgs false

namespace MathCompression.TriangleWreath

variable {K : Type*} [Group K]

def flip : Equiv.Perm Ind where
  toFun := ![2,1,0]
  invFun := ![2,1,0]
  left_inv := by decide +kernel
  right_inv := by decide +kernel

def F : Wreath K := ⟨1, MulOpposite.op flip⟩

theorem F_square : (F : Wreath K)^2 = 1 := by
  simp only [pow_succ, pow_zero, one_mul]
  apply SemidirectProduct.ext
  · funext i
    fin_cases i <;> change (1 : K)*1=1 <;> simp
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

theorem flip_X (d v : K) (dd : d*d=1) (vv : v*v=1) :
    F * X d v * F = (X d v)⁻¹ := by
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · change (1*v)*1=v⁻¹
      simp [invol_inv vv]
    · change (1*v)*1=v⁻¹
      simp [invol_inv vv]
    · change (1*d)*1=d⁻¹
      simp [invol_inv dd]
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

theorem flip_Y : F * (Y : Wreath K) * F = Y⁻¹ := by
  apply SemidirectProduct.ext
  · funext i
    fin_cases i <;> change (1 : K)*1*1=1⁻¹ <;> simp
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

theorem flip_Z (h q : K) : F * Z h q * F = Z h q := by
  apply SemidirectProduct.ext
  · funext i
    fin_cases i
    · change (1*h)*1=h
      simp
    · change (1*q)*1=q
      simp
    · change (1*h)*1=h
      simp
  · apply MulOpposite.unop_injective
    apply Equiv.ext
    intro i
    fin_cases i <;> rfl

abbrev Four := Fin 4

/-- The exact source convention: x=r0*r1, y=r0*r2, z=r0*r3. -/
def rotations {G : Type*} [Group G] (f : Four → G) : Ind → G :=
  ![f 0*f 1,f 0*f 2,f 0*f 3]

/-- Four involutions, six Coxeter pair relations, and four literal extra words. -/
def universalWord {G : Type*} [Group G] (s : ℕ) (f : Four → G) : Fin 14 → G :=
  ![(f 0)^2,(f 1)^2,(f 2)^2,(f 3)^2,
    (f 0*f 1)^6,(f 0*f 2)^3,(f 0*f 3)^2,
    (f 1*f 2)^2,(f 1*f 3)^3,(f 2*f 3)^6,
    sourceWord s (rotations f) 6,sourceWord s (rotations f) 7,
    sourceWord s (rotations f) 8,sourceWord s (rotations f) 9]

def universalRels (s : ℕ) : Set (FreeGroup Four) :=
  Set.range (universalWord s FreeGroup.of)

abbrev Universal (s : ℕ) := PresentedGroup (universalRels s)

def involutoryRows {G : Type*} [Group G] (f x y z : G) : Four → G :=
  ![f,f*x,f*y,f*z]

theorem rotations_involutoryRows {G : Type*} [Group G] (f x y z : G)
    (ff : f*f=1) : rotations (involutoryRows f x y z) = ![x,y,z] := by
  funext i
  fin_cases i <;> simp [rotations, involutoryRows, invol_cancel ff]

lemma reversed_square {G : Type*} [Group G] (f x : G)
    (h : f*x*f=x⁻¹) : (f*x)^2=1 := by
  calc
    (f*x)^2 = (f*x*f)*x := by simp only [pow_two, mul_assoc]
    _ = 1 := by rw [h, inv_mul_cancel]

lemma reversed_pair {G : Type*} [Group G] (f x y : G)
    (h : f*x*f=x⁻¹) : (f*x)*(f*y)=x⁻¹*y := by
  calc
    (f*x)*(f*y) = (f*x*f)*y := by group
    _ = x⁻¹*y := by rw [h]

/-- A generic group adapter: all fourteen relations follow from the literal ten
rotation relations and the displayed reversing involution identities. -/
theorem universal_relators_of_reversal {G : Type*} [Group G]
    (s : ℕ) (f x y z : G) (ff : f*f=1)
    (fx : f*x*f=x⁻¹) (fy : f*y*f=y⁻¹) (fz : f*z*f=z)
    (valid : ∀ j, sourceWord s ![x,y,z] j=1) :
    ∀ j, universalWord s (involutoryRows f x y z) j=1 := by
  have zz : z*z=1 := by simpa [sourceWord,pow_two] using valid 2
  have fz' : f*z*f=z⁻¹ := by rw [invol_inv zz]; exact fz
  have rx := rotations_involutoryRows f x y z ff
  intro j
  fin_cases j
  · simpa [universalWord, involutoryRows, pow_two] using ff
  · exact reversed_square f x fx
  · exact reversed_square f y fy
  · exact reversed_square f z fz'
  · simpa [universalWord, involutoryRows, invol_cancel ff, sourceWord] using valid 0
  · simpa [universalWord, involutoryRows, invol_cancel ff, sourceWord] using valid 1
  · simpa [universalWord, involutoryRows, invol_cancel ff, sourceWord] using valid 2
  · change ((f*x)*(f*y))^2=1
    rw [reversed_pair f x y fx]
    exact valid 5
  · change ((f*x)*(f*z))^3=1
    rw [reversed_pair f x z fx]
    have invprod : x⁻¹*z=(z*x)⁻¹ := by simp [mul_inv_rev, invol_inv zz]
    rw [invprod, inv_pow]
    have e : (z*x)^3=1 := valid 3
    rw [e, inv_one]
  · change ((f*y)*(f*z))^6=1
    rw [reversed_pair f y z fy]
    have invprod : y⁻¹*z=(z*y)⁻¹ := by simp [mul_inv_rev, invol_inv zz]
    rw [invprod, inv_pow]
    have e : (z*y)^6=1 := valid 4
    rw [e, inv_one]
  · change sourceWord s (rotations (involutoryRows f x y z)) 6=1
    rw [rx]
    exact valid 6
  · change sourceWord s (rotations (involutoryRows f x y z)) 7=1
    rw [rx]
    exact valid 7
  · change sourceWord s (rotations (involutoryRows f x y z)) 8=1
    rw [rx]
    exact valid 8
  · change sourceWord s (rotations (involutoryRows f x y z)) 9=1
    rw [rx]
    exact valid 9

def universalRows (s : ℕ) : Four → Wreath (Triangle s) :=
  involutoryRows F (markedRows s 0) (markedRows s 1) (markedRows s 2)

theorem universalRows_valid (s : ℕ) (j : Fin 14) :
    universalWord s (universalRows s) j=1 := by
  obtain ⟨dd,hh,qq,dh,dq,hq⟩ := triangle_basic s
  have vv : (triangleGen s 0 * triangleGen s 2 * triangleGen s 0) *
      (triangleGen s 0 * triangleGen s 2 * triangleGen s 0)=1 := by
    simp [mul_assoc, invol_cancel dd, invol_cancel qq, dd]
  have ff : (F : Wreath (Triangle s))*F=1 := by simpa only [pow_two] using F_square (K := Triangle s)
  apply universal_relators_of_reversal s F (markedRows s 0) (markedRows s 1)
    (markedRows s 2) ff
  · exact flip_X _ _ dd vv
  · exact flip_Y
  · exact flip_Z _ _
  · intro i
    exact markedRows_valid s i

theorem map_universalWord {G H : Type*} [Group G] [Group H]
    (φ : G →* H) (s : ℕ) (f : Four → G) (j : Fin 14) :
    φ (universalWord s f j) = universalWord s (φ ∘ f) j := by
  fin_cases j <;> simp [universalWord,sourceWord,rotations]

/-- The direct marked quotient of the exact fourteen-relator involutory group. -/
def universalMap (s : ℕ) : Universal s →* Wreath (Triangle s) :=
  PresentedGroup.toGroup (f := universalRows s) (by
    intro r hr
    obtain ⟨j,rfl⟩ := hr
    rw [map_universalWord]
    simpa only [Function.comp_def,FreeGroup.lift_apply_of] using universalRows_valid s j)

@[simp] theorem universalMap_generator (s : ℕ) (i : Four) :
    universalMap s (PresentedGroup.of i) = universalRows s i :=
  PresentedGroup.toGroup.of _

def universalRotation (s : ℕ) : Ind → Universal s :=
  rotations PresentedGroup.of

@[simp] theorem universalMap_rotation (s : ℕ) (i : Ind) :
    universalMap s (universalRotation s i) = markedRows s i := by
  have ff : (F : Wreath (Triangle s))*F=1 := by simpa only [pow_two] using F_square (K := Triangle s)
  fin_cases i <;> simp [universalRotation, rotations, universalRows, involutoryRows,
    invol_cancel ff]

/-- The kernel of the outer permutation action in the involutory source itself. -/
def universalKernel (s : ℕ) : Subgroup (Universal s) :=
  ((SemidirectProduct.rightHom : Wreath (Triangle s) →* Outer).comp (universalMap s)).ker

lemma universalKernel_mem (s : ℕ) (a : universalKernel s) : (universalMap s a).right=1 :=
  a.property

def universalCoordinate (s : ℕ) : universalKernel s →* Triangle s where
  toFun a := (universalMap s a).left 0
  map_one' := by
    change (universalMap s 1).left 0=1
    rw [map_one]
    rfl
  map_mul' a b := by
    change (universalMap s ((a : Universal s)*(b : Universal s))).left 0 = _
    rw [map_mul,row_mul,universalKernel_mem s a]
    rfl

lemma universal_witness_x (s : ℕ) :
    universalMap s ((universalRotation s 0)^3) =
      ⟨![triangleGen s 0,triangleGen s 2,triangleGen s 0],1⟩ := by
  calc
    universalMap s ((universalRotation s 0)^3) =
        sourceMap s ((PresentedGroup.of (0 : Ind))^3) := by simp
    _ = _ := source_witness_x s

lemma universal_witness_z (s : ℕ) :
    universalMap s (universalRotation s 2) =
      ⟨![triangleGen s 1,triangleGen s 2,triangleGen s 1],1⟩ := by
  calc
    universalMap s (universalRotation s 2) = sourceMap s (PresentedGroup.of (2 : Ind)) := by simp
    _ = _ := source_witness_z s

lemma universal_witness_yzy (s : ℕ) :
    universalMap s ((universalRotation s 1)⁻¹ * universalRotation s 2 * universalRotation s 1) =
      ⟨![triangleGen s 2,triangleGen s 1,triangleGen s 1],1⟩ := by
  calc
    universalMap s ((universalRotation s 1)⁻¹ * universalRotation s 2 * universalRotation s 1) =
        sourceMap s ((PresentedGroup.of (1 : Ind))⁻¹ * PresentedGroup.of (2 : Ind) *
          PresentedGroup.of (1 : Ind)) := by simp
    _ = _ := source_witness_yzy s

theorem universalCoordinate_generator_preimage (s : ℕ) (i : Ind) :
    ∃ a : universalKernel s, universalCoordinate s a = triangleGen s i := by
  fin_cases i
  · refine ⟨⟨(universalRotation s 0)^3, ?_⟩, ?_⟩
    · change (universalMap s ((universalRotation s 0)^3)).right=1
      rw [universal_witness_x]
    · change (universalMap s ((universalRotation s 0)^3)).left 0=triangleGen s 0
      rw [universal_witness_x]
      rfl
  · refine ⟨⟨universalRotation s 2, ?_⟩, ?_⟩
    · change (universalMap s (universalRotation s 2)).right=1
      rw [universal_witness_z]
    · change (universalMap s (universalRotation s 2)).left 0=triangleGen s 1
      rw [universal_witness_z]
      rfl
  · refine ⟨⟨(universalRotation s 1)⁻¹ * universalRotation s 2 * universalRotation s 1, ?_⟩, ?_⟩
    · change (universalMap s ((universalRotation s 1)⁻¹ * universalRotation s 2 *
        universalRotation s 1)).right=1
      rw [universal_witness_yzy]
    · change (universalMap s ((universalRotation s 1)⁻¹ * universalRotation s 2 *
        universalRotation s 1)).left 0=triangleGen s 2
      rw [universal_witness_yzy]
      rfl

/-- The explicit subgroup of U_s surjects onto the exact triangle group. -/
theorem universalCoordinate_surjective (s : ℕ) : Function.Surjective (universalCoordinate s) := by
  intro a
  exact PresentedGroup.generated_by (triangleRels s) (universalCoordinate s).range
    (universalCoordinate_generator_preimage s) a

/-- Only triangle infinitude is a hypothesis; the full-group map is constructed. -/
theorem universal_infinite_of_triangle (s : ℕ) [Infinite (Triangle s)] : Infinite (Universal s) := by
  haveI : Infinite (universalKernel s) := Infinite.of_surjective _ (universalCoordinate_surjective s)
  exact Infinite.of_injective (fun a : universalKernel s => (a : Universal s)) Subtype.val_injective

#print axioms universalRows_valid
#print axioms universalMap
#print axioms universalCoordinate_surjective
#print axioms universal_infinite_of_triangle

end MathCompression.TriangleWreath

