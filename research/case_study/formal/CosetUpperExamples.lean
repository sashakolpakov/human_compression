import CosetUpperCertificate

namespace HumanCompression.CosetUpperCertificate.Examples
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

def facet11Reps : Fin 11 → List (Fin 2) := fun v =>
  [[], [1], [1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0], [1, 0, 1, 0], [1, 0]][v.val]!
def facet11Trace : List (Instruction (Fin 2) (Fin 11)) :=
  [ .rootLoop 0,
    .tree 0 1 1,
    .reverse ⟨0, 1, 1⟩,
    .tree 1 0 10,
    .reverse ⟨1, 0, 10⟩,
    .tree 10 1 2,
    .reverse ⟨10, 1, 2⟩,
    .tree 2 0 9,
    .reverse ⟨2, 0, 9⟩,
    .tree 9 1 3,
    .reverse ⟨9, 1, 3⟩,
    .tree 3 0 8,
    .reverse ⟨3, 0, 8⟩,
    .tree 8 1 4,
    .reverse ⟨8, 1, 4⟩,
    .tree 4 0 7,
    .reverse ⟨4, 0, 7⟩,
    .tree 7 1 5,
    .reverse ⟨7, 1, 5⟩,
    .tree 5 0 6,
    .reverse ⟨5, 0, 6⟩,
    .gap 0 [⟨0, 0, 0⟩, ⟨0, 1, 1⟩, ⟨1, 0, 10⟩, ⟨10, 1, 2⟩, ⟨2, 0, 9⟩, ⟨9, 1, 3⟩, ⟨3, 0, 8⟩, ⟨8, 1, 4⟩, ⟨4, 0, 7⟩, ⟨7, 1, 5⟩, ⟨5, 0, 6⟩] 1 [⟨0, 1, 1⟩, ⟨1, 0, 10⟩, ⟨10, 1, 2⟩, ⟨2, 0, 9⟩, ⟨9, 1, 3⟩, ⟨3, 0, 8⟩, ⟨8, 1, 4⟩, ⟨4, 0, 7⟩, ⟨7, 1, 5⟩, ⟨5, 0, 6⟩] ]
def facet11Rels : List (List (Fin 2)) := [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
theorem facet11_accepted : accept facet11Rels [0] 0 facet11Reps facet11Trace = true := by decide
theorem facet11_index_bound :
    (facet (listSet facet11Rels) (listSet ([0] : List (Fin 2)))).index ≤ 11 := by
  have h := accepted_universal_index_bound facet11Rels [0] 0 facet11Reps facet11Trace (by decide) facet11_accepted
  simpa using h.2

def group22Reps : Fin 22 → List (Fin 2) := fun v =>
  [[], [0], [1, 0], [1], [1, 0, 1, 0], [1, 0, 1], [1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, 1, 0], [0, 1], [0, 1, 0]][v.val]!
def group22Trace : List (Instruction (Fin 2) (Fin 22)) :=
  [ .tree 0 0 1,
    .reverse ⟨0, 0, 1⟩,
    .tree 0 1 3,
    .reverse ⟨0, 1, 3⟩,
    .tree 1 1 20,
    .reverse ⟨1, 1, 20⟩,
    .tree 3 0 2,
    .reverse ⟨3, 0, 2⟩,
    .tree 20 0 21,
    .reverse ⟨20, 0, 21⟩,
    .tree 2 1 5,
    .reverse ⟨2, 1, 5⟩,
    .tree 21 1 18,
    .reverse ⟨21, 1, 18⟩,
    .tree 5 0 4,
    .reverse ⟨5, 0, 4⟩,
    .tree 18 0 19,
    .reverse ⟨18, 0, 19⟩,
    .tree 4 1 7,
    .reverse ⟨4, 1, 7⟩,
    .tree 19 1 16,
    .reverse ⟨19, 1, 16⟩,
    .tree 7 0 6,
    .reverse ⟨7, 0, 6⟩,
    .tree 16 0 17,
    .reverse ⟨16, 0, 17⟩,
    .tree 6 1 9,
    .reverse ⟨6, 1, 9⟩,
    .tree 17 1 14,
    .reverse ⟨17, 1, 14⟩,
    .tree 9 0 8,
    .reverse ⟨9, 0, 8⟩,
    .tree 14 0 15,
    .reverse ⟨14, 0, 15⟩,
    .tree 8 1 11,
    .reverse ⟨8, 1, 11⟩,
    .tree 15 1 12,
    .reverse ⟨15, 1, 12⟩,
    .tree 11 0 10,
    .reverse ⟨11, 0, 10⟩,
    .tree 12 0 13,
    .reverse ⟨12, 0, 13⟩,
    .gap 0 [⟨0, 0, 1⟩, ⟨1, 1, 20⟩, ⟨20, 0, 21⟩, ⟨21, 1, 18⟩, ⟨18, 0, 19⟩, ⟨19, 1, 16⟩, ⟨16, 0, 17⟩, ⟨17, 1, 14⟩, ⟨14, 0, 15⟩, ⟨15, 1, 12⟩, ⟨12, 0, 13⟩] 1 [⟨0, 1, 3⟩, ⟨3, 0, 2⟩, ⟨2, 1, 5⟩, ⟨5, 0, 4⟩, ⟨4, 1, 7⟩, ⟨7, 0, 6⟩, ⟨6, 1, 9⟩, ⟨9, 0, 8⟩, ⟨8, 1, 11⟩, ⟨11, 0, 10⟩],
    .reverse ⟨13, 1, 10⟩ ]
def group22Rels : List (List (Fin 2)) := [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
theorem group22_accepted : accept group22Rels [] 0 group22Reps group22Trace = true := by decide
theorem group22_index_bound :
    (facet (listSet group22Rels) (listSet ([] : List (Fin 2)))).index ≤ 22 := by
  have h := accepted_universal_index_bound group22Rels [] 0 group22Reps group22Trace (by decide) group22_accepted
  simpa using h.2

theorem group22_order_bound : Nat.card (Universal (listSet group22Rels)) ≤ 22 := by
  simpa [facet, listSet] using group22_index_bound
#print axioms group22_order_bound
theorem root_alone_rejected : accept facet11Rels [0] (0 : Fin 1) (fun _ => []) [.rootLoop 0] = false := by decide
theorem no_relators_rejected : accept ([] : List (List (Fin 2))) [] 0 group22Reps group22Trace = false := by decide
theorem empty_trace_rejected : accept group22Rels [] 0 group22Reps [] = false := by decide
theorem false_tree_rejected : step group22Rels [] 0 group22Reps [] (.tree 0 0 0) = none := by decide

#print axioms facet11_accepted
#print axioms facet11_index_bound
#print axioms group22_accepted
#print axioms group22_index_bound
#print axioms root_alone_rejected
#print axioms no_relators_rejected
#print axioms empty_trace_rejected
#print axioms false_tree_rejected

end HumanCompression.CosetUpperCertificate.Examples
