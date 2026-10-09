import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Union
import Mathlib.Data.Fintype.Basic
import Lean.Elab.Tactic.Omega

/-!
Boolean shadows for arbitrary finite families of finite subsets.
There is no flag hypothesis on the query family. This module does not define
an incidence geometry, identify the tree model, or formalize residue joins.
-/

namespace BooleanShadow

variable {α : Type*} [DecidableEq α] [Fintype α]

/-- Incidence in the Boolean subset geometry, including reflexivity. -/
def Comparable (X Y : Finset α) : Prop := X ⊆ Y ∨ Y ⊆ X

/-- A common shadow consists of subsets of the prescribed cardinality. -/
def Shadow (U : Finset (Finset α)) (k : ℕ) (Y : Finset α) : Prop :=
  Y.card = k ∧ ∀ X ∈ U, Comparable X Y

/-- The union of query members strictly smaller than the target rank. -/
def lower (U : Finset (Finset α)) (k : ℕ) : Finset α :=
  (U.filter fun X => X.card < k).biUnion id

/-- The intersection of query members strictly larger than the target rank.
The empty intersection is the entire finite universe. -/
def upper (U : Finset (Finset α)) (k : ℕ) : Finset α :=
  Finset.univ.filter fun a => ∀ X ∈ U, k < X.card → a ∈ X

omit [Fintype α] in
theorem mem_lower {U : Finset (Finset α)} {k : ℕ} {a : α} :
    a ∈ lower U k ↔ ∃ X ∈ U, X.card < k ∧ a ∈ X := by
  simp [lower, and_assoc]

theorem mem_upper {U : Finset (Finset α)} {k : ℕ} {a : α} :
    a ∈ upper U k ↔ ∀ X ∈ U, k < X.card → a ∈ X := by
  simp [upper]

omit [Fintype α] in
theorem smaller_subset_lower {U : Finset (Finset α)} {k : ℕ}
    {X : Finset α} (hX : X ∈ U) (hcard : X.card < k) : X ⊆ lower U k := by
  intro a ha
  exact mem_lower.mpr ⟨X, hX, hcard, ha⟩

theorem upper_subset_larger {U : Finset (Finset α)} {k : ℕ}
    {X : Finset α} (hX : X ∈ U) (hcard : k < X.card) : upper U k ⊆ X := by
  intro a ha
  exact mem_upper.mp ha X hX hcard

omit [Fintype α] in
theorem subset_of_comparable_of_card_lt {X Y : Finset α}
    (h : Comparable X Y) (hlt : X.card < Y.card) : X ⊆ Y := by
  rcases h with h | h
  · exact h
  · have hc := Finset.card_le_card h
    omega

omit [DecidableEq α] [Fintype α] in
theorem eq_of_comparable_of_card_eq {X Y : Finset α}
    (h : Comparable X Y) (heq : X.card = Y.card) : X = Y := by
  rcases h with h | h
  · exact Finset.eq_of_subset_of_card_le h heq.symm.le
  · exact (Finset.eq_of_subset_of_card_le h heq.le).symm

omit [DecidableEq α] [Fintype α] in
/-- A query member at the target rank forces every shadow element to be it. -/
theorem shadow_eq_of_same_rank_member {U : Finset (Finset α)} {k : ℕ}
    {X Y : Finset α} (hX : X ∈ U) (hXcard : X.card = k)
    (hY : Shadow U k Y) : Y = X := by
  exact (eq_of_comparable_of_card_eq (hY.2 X hX) (hXcard.trans hY.1.symm)).symm

/-- Every common shadow point lies between the union/intersection bounds. -/
theorem shadow_bounds {U : Finset (Finset α)} {k : ℕ} {Y : Finset α}
    (hY : Shadow U k Y) : lower U k ⊆ Y ∧ Y ⊆ upper U k := by
  have hcardY := hY.1
  constructor
  · intro a ha
    obtain ⟨X, hX, hcard, haX⟩ := mem_lower.mp ha
    have hXY : X ⊆ Y := subset_of_comparable_of_card_lt (hY.2 X hX) (by omega)
    exact hXY haX
  · intro a ha
    apply mem_upper.mpr
    intro X hX hcard
    have hYX : Y ⊆ X := subset_of_comparable_of_card_lt
      (Or.symm (hY.2 X hX)) (by omega)
    exact hYX ha

/-- Exact interval description, with no flag assumption on the query family. -/
theorem shadow_iff_interval {U : Finset (Finset α)} {k : ℕ}
    (hno : ∀ X ∈ U, X.card ≠ k) (Y : Finset α) :
    Shadow U k Y ↔ Y.card = k ∧ lower U k ⊆ Y ∧ Y ⊆ upper U k := by
  constructor
  · intro hY
    exact ⟨hY.1, shadow_bounds hY⟩
  · rintro ⟨hcard, hL, hV⟩
    refine ⟨hcard, ?_⟩
    intro X hX
    have hne := hno X hX
    by_cases hlt : X.card < k
    · exact Or.inl ((smaller_subset_lower hX hlt).trans hL)
    · have hgt : k < X.card := by omega
      exact Or.inr (hV.trans (upper_subset_larger hX hgt))

omit [DecidableEq α] [Fintype α] in
/-- Once the shadow is nonempty, a same-rank member gives exactly a singleton. -/
theorem shadow_iff_eq_of_same_rank_member {U : Finset (Finset α)} {k : ℕ}
    {X : Finset α} (hX : X ∈ U) (hcard : X.card = k)
    (hne : ∃ Y, Shadow U k Y) (Y : Finset α) : Shadow U k Y ↔ Y = X := by
  obtain ⟨Z, hZ⟩ := hne
  have hZX : Z = X := shadow_eq_of_same_rank_member hX hcard hZ
  constructor
  · exact shadow_eq_of_same_rank_member hX hcard
  · intro hYX
    simpa only [hZX, hYX] using hZ

/-- Remove the improper bottom/top subsets from the two interval boundaries. -/
def boundaryFlag (L V : Finset α) : Finset (Finset α) :=
  ({L, V} : Finset (Finset α)).filter fun X => X ≠ ∅ ∧ X ≠ Finset.univ

theorem mem_boundaryFlag {L V X : Finset α} :
    X ∈ boundaryFlag L V ↔ (X = L ∨ X = V) ∧ X ≠ ∅ ∧ X ≠ Finset.univ := by
  simp [boundaryFlag]

theorem boundaryFlag_card_le (L V : Finset α) : (boundaryFlag L V).card ≤ 2 := by
  exact (Finset.card_filter_le _ _).trans Finset.card_le_two

theorem boundaryFlag_chain {L V : Finset α} (hLV : L ⊆ V) :
    ∀ X ∈ boundaryFlag L V, ∀ Z ∈ boundaryFlag L V, Comparable X Z := by
  intro X hX Z hZ
  rcases (mem_boundaryFlag.mp hX).1 with rfl | rfl <;>
    rcases (mem_boundaryFlag.mp hZ).1 with rfl | rfl <;>
    simp_all [Comparable]

theorem boundaryFlag_incident {U : Finset (Finset α)} {L V : Finset α}
    (hLV : L ⊆ V) (hsplit : ∀ X ∈ U, X ⊆ L ∨ V ⊆ X) :
    ∀ W ∈ boundaryFlag L V, ∀ X ∈ U, Comparable W X := by
  intro W hW X hX
  rcases (mem_boundaryFlag.mp hW).1 with rfl | rfl
  · rcases hsplit X hX with h | h
    · exact Or.inr h
    · exact Or.inl (hLV.trans h)
  · rcases hsplit X hX with h | h
    · exact Or.inr (h.trans hLV)
    · exact Or.inl h

/-- Strict interval boundaries have precisely the desired common shadow,
including when the empty/full boundary has been omitted. -/
theorem shadow_boundaryFlag_iff {L V : Finset α} {k : ℕ}
    (hL : L.card < k) (hV : k < V.card) (Y : Finset α) :
    Shadow (boundaryFlag L V) k Y ↔ Y.card = k ∧ L ⊆ Y ∧ Y ⊆ V := by
  constructor
  · intro hY
    have hYcard := hY.1
    refine ⟨hYcard, ?_, ?_⟩
    · by_cases hbot : L = ∅
      · simp [hbot]
      · have htop : L ≠ Finset.univ := by
          intro h
          have hc := Finset.card_le_card (Finset.subset_univ V)
          have heq := congrArg Finset.card h
          omega
        have hm : L ∈ boundaryFlag L V := mem_boundaryFlag.mpr ⟨Or.inl rfl, hbot, htop⟩
        exact subset_of_comparable_of_card_lt (hY.2 L hm) (by omega)
    · by_cases htop : V = Finset.univ
      · simp [htop]
      · have hbot : V ≠ ∅ := by
          intro h
          have hc : V.card = 0 := by simp [h]
          omega
        have hm : V ∈ boundaryFlag L V := mem_boundaryFlag.mpr ⟨Or.inr rfl, hbot, htop⟩
        exact subset_of_comparable_of_card_lt (Or.symm (hY.2 V hm)) (by omega)
  · rintro ⟨hcard, hLY, hYV⟩
    refine ⟨hcard, ?_⟩
    intro X hX
    rcases (mem_boundaryFlag.mp hX).1 with rfl | rfl
    · exact Or.inl hLY
    · exact Or.inr hYV

/-- A small proper flag, incident with the query family, with exactly its shadow. -/
def Witness (U : Finset (Finset α)) (k : ℕ) (C : Finset (Finset α)) : Prop :=
  C.card ≤ 2 ∧
  (∀ X ∈ C, X ≠ ∅ ∧ X ≠ Finset.univ) ∧
  (∀ X ∈ C, ∀ Z ∈ C, Comparable X Z) ∧
  (∀ X ∈ C, ∀ Z ∈ U, Comparable X Z) ∧
  (∀ Y, Shadow C k Y ↔ Shadow U k Y)

/-- In the strict-boundary case the witness is the explicit filtered pair. -/
theorem boundaryFlag_witness {U : Finset (Finset α)} {k : ℕ}
    (hno : ∀ X ∈ U, X.card ≠ k) (hne : ∃ Y, Shadow U k Y)
    (hL : (lower U k).card < k) (hV : k < (upper U k).card) :
    Witness U k (boundaryFlag (lower U k) (upper U k)) := by
  obtain ⟨Y, hY⟩ := hne
  have hb := shadow_bounds hY
  have hLV := hb.1.trans hb.2
  have hsplit : ∀ X ∈ U, X ⊆ lower U k ∨ upper U k ⊆ X := by
    intro X hX
    have hneX := hno X hX
    by_cases hlt : X.card < k
    · exact Or.inl (smaller_subset_lower hX hlt)
    · exact Or.inr (upper_subset_larger hX (by omega))
  refine ⟨boundaryFlag_card_le _ _, ?_, boundaryFlag_chain hLV,
    boundaryFlag_incident hLV hsplit, ?_⟩
  · intro X hX
    exact (mem_boundaryFlag.mp hX).2
  · intro Z
    exact (shadow_boundaryFlag_iff hL hV Z).trans (shadow_iff_interval hno Z).symm

omit [DecidableEq α] in
/-- A unique shadow point is itself a proper one-vertex witness. -/
theorem singleton_witness {U : Finset (Finset α)} {k : ℕ} {X : Finset α}
    (hk0 : 0 < k) (hktop : k < (Finset.univ : Finset α).card)
    (hX : Shadow U k X) (hunique : ∀ Y, Shadow U k Y → Y = X) :
    Witness U k {X} := by
  have hcard := hX.1
  have hproper : X ≠ ∅ ∧ X ≠ Finset.univ := by
    constructor
    · intro h
      have hc : X.card = 0 := by simp [h]
      omega
    · intro h
      have hc := congrArg Finset.card h
      omega
  refine ⟨by simp, ?_, ?_, ?_, ?_⟩
  · intro Z hZ
    have hZX := Finset.mem_singleton.mp hZ
    simpa only [hZX] using hproper
  · intro W hW Z hZ
    have hWX := Finset.mem_singleton.mp hW
    have hZX := Finset.mem_singleton.mp hZ
    simp [hWX, hZX, Comparable]
  · intro W hW Z hZ
    have hWX := Finset.mem_singleton.mp hW
    simpa only [hWX, Comparable] using Or.symm (hX.2 Z hZ)
  · intro Y
    constructor
    · intro hY
      have hcomp : Comparable X Y := hY.2 X (by simp)
      have heq : X = Y := eq_of_comparable_of_card_eq hcomp (hcard.trans hY.1.symm)
      simpa only [heq] using hX
    · intro hY
      have heq := hunique Y hY
      subst Y
      exact ⟨hcard, by intro Z hZ; simp [Finset.mem_singleton.mp hZ, Comparable]⟩

/-- Every nonempty shadow at a proper Boolean rank has an explicit-size witness.
The query family need not be a flag, and the witness contains at most two
nonempty proper subsets, forms a flag, and is incident with the entire query. -/
theorem exists_witness_card_le_two {U : Finset (Finset α)} {k : ℕ}
    (hk0 : 0 < k) (hktop : k < (Finset.univ : Finset α).card)
    (hne : ∃ Y, Shadow U k Y) : ∃ C, Witness U k C := by
  obtain ⟨Y₀, hY₀⟩ := hne
  by_cases heq : ∃ X ∈ U, X.card = k
  · obtain ⟨X, hX, hXcard⟩ := heq
    have hYX : Y₀ = X := shadow_eq_of_same_rank_member hX hXcard hY₀
    have hSX : Shadow U k X := by simpa only [hYX] using hY₀
    exact ⟨{X}, singleton_witness hk0 hktop hSX
      (fun Y hY => shadow_eq_of_same_rank_member hX hXcard hY)⟩
  · have hno : ∀ X ∈ U, X.card ≠ k := by
      intro X hX hcard
      exact heq ⟨X, hX, hcard⟩
    have hb := shadow_bounds hY₀
    have hYcard := hY₀.1
    have hLcard := Finset.card_le_card hb.1
    have hVcard := Finset.card_le_card hb.2
    by_cases hLeq : (lower U k).card = k
    · have hLY : lower U k = Y₀ := Finset.eq_of_subset_of_card_le hb.1 (by omega)
      have hSL : Shadow U k (lower U k) := by simpa only [hLY] using hY₀
      refine ⟨{lower U k}, singleton_witness hk0 hktop hSL ?_⟩
      intro Y hY
      have hc := hY.1
      exact (Finset.eq_of_subset_of_card_le (shadow_bounds hY).1 (by omega)).symm
    · by_cases hVeq : (upper U k).card = k
      · have hYV : Y₀ = upper U k := Finset.eq_of_subset_of_card_le hb.2 (by omega)
        have hSV : Shadow U k (upper U k) := by simpa only [hYV] using hY₀
        refine ⟨{upper U k}, singleton_witness hk0 hktop hSV ?_⟩
        intro Y hY
        have hc := hY.1
        exact Finset.eq_of_subset_of_card_le (shadow_bounds hY).2 (by omega)
      · exact ⟨boundaryFlag (lower U k) (upper U k),
          boundaryFlag_witness hno ⟨Y₀, hY₀⟩ (by omega) (by omega)⟩

#print axioms shadow_iff_interval
#print axioms shadow_iff_eq_of_same_rank_member
#print axioms exists_witness_card_le_two

end BooleanShadow
