import Mathlib.GroupTheory.Subgroup.Centralizer
import Mathlib.Order.Atoms
import Mathlib.Tactic

/-! The group-theoretic extension leg in phase258 §5. No finite-field,
projective-group, torus, maximal-subgroup classification, or IP input is proved here. -/
namespace HumanCompression.MarkedInvolutionExtension
variable {G : Type*} [Group G]

/-- The string axioms without generation or the intersection property. -/
def IsStringTuple {n : ℕ} (r : Fin n → G) : Prop :=
  (∀ i, r i ≠ 1) ∧ (∀ i, r i * r i = 1) ∧ Function.Injective r ∧
    (∀ i j, i.val + 1 < j.val → Commute (r i) (r j))

/-- A genuine marked generating group; no intersection property is included. -/
def IsGeneratingStringMarking {n : ℕ} (r : Fin n → G) : Prop :=
  IsStringTuple r ∧ Subgroup.closure (Set.range r) = ⊤

abbrev triple (a b c : G) : Fin 3 → G := ![a, b, c]
abbrev quadruple (a b c z : G) : Fin 4 → G := ![a, b, c, z]

omit [Group G] in
/-- Extending the tuple preserves its actual first three generators. -/
theorem prefix_preserved (a b c z : G) :
    (fun i : Fin 3 => quadruple a b c z i.castSucc) = triple a b c := by
  funext i
  fin_cases i <;> rfl

/-- The original generated subgroup is contained in the extended one. -/
theorem prefix_closure_le (a b c z : G) :
    Subgroup.closure (Set.range (triple a b c)) ≤
      Subgroup.closure (Set.range (quadruple a b c z)) := by
  apply Subgroup.closure_mono
  rintro x ⟨i, rfl⟩
  refine ⟨i.castSucc, ?_⟩
  fin_cases i <;> rfl

/-- All rank-four string axioms follow from the rank-three tuple and the
three new distinctness/commutation conditions. Generation is proved separately. -/
theorem extend_string_tuple {a b c z : G}
    (h : IsStringTuple (triple a b c))
    (hz1 : z ≠ 1) (hz2 : z * z = 1)
    (hza : z ≠ a) (hzb : z ≠ b) (hzc : z ≠ c)
    (hza_comm : Commute z a) (hzb_comm : Commute z b) :
    IsStringTuple (quadruple a b c z) := by
  obtain ⟨hn, hi, hd, hs⟩ := h
  have ha := hn 0
  have hb := hn 1
  have hc := hn 2
  have haa := hi 0
  have hbb := hi 1
  have hcc := hi 2
  have hab : a ≠ b := by
    intro e
    have h01 := hd (show triple a b c 0 = triple a b c 1 from e)
    exact (by decide : (0 : Fin 3) ≠ 1) h01
  have hac : a ≠ c := by
    intro e
    have h02 := hd (show triple a b c 0 = triple a b c 2 from e)
    exact (by decide : (0 : Fin 3) ≠ 2) h02
  have hbc : b ≠ c := by
    intro e
    have h12 := hd (show triple a b c 1 = triple a b c 2 from e)
    exact (by decide : (1 : Fin 3) ≠ 2) h12
  have hac_comm : Commute a c := hs 0 2 (by decide)
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simpa using (by assumption)
  · intro i; fin_cases i <;> simpa using (by assumption)
  · intro i j heq
    fin_cases i <;> fin_cases j <;> simp_all [quadruple]
  · intro i j hij
    fin_cases i <;> fin_cases j <;>
      simp_all [quadruple, Commute.symm_iff]

/-- A nontrivial element centralizing a,b cannot belong to a subgroup whose
internal common centralizer of a,b is trivial. This is an actual subgroup condition. -/
theorem outside_of_internal_centralizer_bot (H : Subgroup G) {a b z : G}
    (hcent : H ⊓ Subgroup.centralizer ({a, b} : Set G) = ⊥)
    (hz1 : z ≠ 1) (hza : Commute z a) (hzb : Commute z b) : z ∉ H := by
  intro hzH
  have hzC : z ∈ Subgroup.centralizer ({a, b} : Set G) := by
    rw [Subgroup.mem_centralizer_iff]
    intro x hx
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hx
    rcases hx with rfl | rfl
    · exact hza.symm.eq
    · exact hzb.symm.eq
  have hz : z ∈ H ⊓ Subgroup.centralizer ({a, b} : Set G) := ⟨hzH, hzC⟩
  rw [hcent, Subgroup.mem_bot] at hz
  exact hz1 hz

/-- At a maximal proper subgroup, adjoining an outside element generates the whole group. -/
theorem generation_of_coatom {a b c z : G}
    (hm : IsCoatom (Subgroup.closure (Set.range (triple a b c))))
    (hz : z ∉ Subgroup.closure (Set.range (triple a b c))) :
    Subgroup.closure (Set.range (quadruple a b c z)) = ⊤ := by
  apply hm.2
  apply lt_of_le_of_ne (prefix_closure_le a b c z)
  intro heq
  apply hz
  rw [heq]
  exact Subgroup.subset_closure ⟨3, rfl⟩

/-- The full-end case: the old triple already generates. Noncommuting adjacent
pairs ensure that a common-centralizing involution cannot repeat any old marker. -/
theorem full_end_extension {a b c z : G}
    (h : IsGeneratingStringMarking (triple a b c))
    (hab : ¬ Commute a b) (hbc : ¬ Commute b c)
    (hz1 : z ≠ 1) (hz2 : z * z = 1)
    (hza : Commute z a) (hzb : Commute z b) :
    IsGeneratingStringMarking (quadruple a b c z) := by
  have hza' : z ≠ a := by intro e; subst z; exact hab hzb
  have hzb' : z ≠ b := by intro e; subst z; exact hab hza.symm
  have hzc' : z ≠ c := by intro e; subst z; exact hbc hzb.symm
  refine ⟨extend_string_tuple h.1 hz1 hz2 hza' hzb' hzc' hza hzb, ?_⟩
  apply top_unique
  rw [← h.2]
  exact prefix_closure_le a b c z

/-- An alternative full-end interface matches the odd-dihedral torus proof:
the new involution is outside the first pair subgroup and differs from c. -/
theorem full_end_extension_of_pair_outside {a b c z : G}
    (h : IsGeneratingStringMarking (triple a b c))
    (hzD : z ∉ Subgroup.closure ({a, b} : Set G)) (hzc : z ≠ c)
    (hz1 : z ≠ 1) (hz2 : z * z = 1)
    (hza : Commute z a) (hzb : Commute z b) :
    IsGeneratingStringMarking (quadruple a b c z) := by
  have hza' : z ≠ a := by
    intro e; apply hzD; rw [e]
    exact Subgroup.subset_closure (by simp)
  have hzb' : z ≠ b := by
    intro e; apply hzD; rw [e]
    exact Subgroup.subset_closure (by simp)
  refine ⟨extend_string_tuple h.1 hz1 hz2 hza' hzb' hzc hza hzb, ?_⟩
  apply top_unique
  rw [← h.2]
  exact prefix_closure_le a b c z

/-- The proper-end case derives all distinctness from outside membership, then
uses genuine maximality to obtain generation. -/
theorem maximal_end_extension {a b c z : G}
    (h : IsStringTuple (triple a b c))
    (hm : IsCoatom (Subgroup.closure (Set.range (triple a b c))))
    (hz : z ∉ Subgroup.closure (Set.range (triple a b c)))
    (hz1 : z ≠ 1) (hz2 : z * z = 1)
    (hza : Commute z a) (hzb : Commute z b) :
    IsGeneratingStringMarking (quadruple a b c z) := by
  have hne (i : Fin 3) : z ≠ triple a b c i := by
    intro e; apply hz; rw [e]; exact Subgroup.subset_closure ⟨i, rfl⟩
  exact ⟨extend_string_tuple h hz1 hz2 (hne 0) (hne 1) (hne 2) hza hzb,
    generation_of_coatom hm hz⟩

/-- The reusable proper-end theorem: no outside or final-generation conclusion
is assumed; internal centralizer triviality and maximality supply them. -/
theorem maximal_end_extension_of_internal_centralizer {a b c z : G}
    (h : IsStringTuple (triple a b c))
    (hm : IsCoatom (Subgroup.closure (Set.range (triple a b c))))
    (hc : Subgroup.closure (Set.range (triple a b c)) ⊓
      Subgroup.centralizer ({a, b} : Set G) = ⊥)
    (hz1 : z ≠ 1) (hz2 : z * z = 1)
    (hza : Commute z a) (hzb : Commute z b) :
    IsGeneratingStringMarking (quadruple a b c z) := by
  apply maximal_end_extension h hm
  · exact outside_of_internal_centralizer_bot _ hc hz1 hza hzb
  · exact hz1
  · exact hz2
  · exact hza
  · exact hzb

#print axioms prefix_preserved
#print axioms prefix_closure_le
#print axioms extend_string_tuple
#print axioms outside_of_internal_centralizer_bot
#print axioms generation_of_coatom
#print axioms full_end_extension
#print axioms full_end_extension_of_pair_outside
#print axioms maximal_end_extension
#print axioms maximal_end_extension_of_internal_centralizer
end HumanCompression.MarkedInvolutionExtension
