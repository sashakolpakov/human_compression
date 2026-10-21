Formal proof of the shadow covering criterion
=============================================

ShadowCover.lean verifies the exact eligibility-and-exclusion equivalence from
the existing phase4_shadow_ip written proof. It applies to an arbitrary typed
incidence relation with no incident distinct objects of the same type. For a
shadow containing two distinct objects, its witness flags are exactly its
eligible covering flags. The set to which the witness must be incident is
arbitrary; it need not itself be a flag.

The Lean predicates retain the flag condition, all incidence requirements and
both directions of shadow equality. The same-type axiom and two distinct
shadow elements are explicit hypotheses. The reverse implication requires
only that all target shadow elements have the requested type.

This is a formalization of a previously written argument, not a new theorem
or a source recovery. It does not formalize group actions, orbit normalization,
the program, any sporadic census, or all of L096. Four declarations comprise
one criterion and its proof lemmas. Independent scope review is pending.

The exact Lean 4.32.2 compiler and axiom output are recorded in compile.json
and compile.stdout.log. The first lemma uses no axioms; the remaining proof
uses the standard propext, Classical.choice and Quot.sound. There is no sorry
or added axiom. Import Lean supplies the core proof environment, without Mathlib.
