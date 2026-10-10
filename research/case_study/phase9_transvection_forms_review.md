# Independent review of the transvection-form Lean certificate

10 October 2026. Internal mathematical and statement-scope review by
recent_conjectures; not external peer review.

**Result: PASS.** The saved Lean compilation reports exit code zero
for all three theorems. The source hash is
899f4a93c3cd7417cef45a4a58a74a0abef648d382ace2a07502ec6a6d244c56; the reviewed report hash is
e736b16cea88d9b1e06ecc7332226fcba6978d5f172d396bfa7a42f4d610ad3c. The report lists only the standard axioms
propext, Classical.choice and Quot.sound, with no sorryAx.

For a matrix unit E_ij and b distinct from j, the (j,b)-entry of
(I+E_ij)^T B (I+E_ij) is B_jb+B_ib. The right factor leaves column b
unchanged, and the left factor adds row i to row j. Equating with B_jb
therefore forces B_ib=0 by additive cancellation. This remains correct
even when i=j in the first, local lemma: then the relevant row is simply
doubled. No characteristic restriction, field hypothesis, commutativity
of the coefficient ring, symmetry of B, or invertibility assumption on
I+E_ij is needed for that entry implication.

The second theorem assumes a third index j distinct from each i,b.
For a nonempty finite index type this is the precise dimension-at-least-three
condition (the empty case satisfies it vacuously and also has only the zero matrix); it permits using the hypothesis for genuine elementary
transvections with i distinct from j. Every entry of B consequently
vanishes. The final theorem proves the required third-index property for
Fin 4 and instantiates the result. All three statements match the actual
matrix calculation, including characteristic two.

The certificate starts with **exact invariance**, not preservation up to
a scalar. For the SL4 application in characteristic p, the written
argument still supplies the reduction: I+E_ij has order p; a similarity
multiplier has p-th power one; in a field of characteristic p it is one.
The source itself deliberately leaves this reduction outside Lean.

Also unformalized here are the natural-group generation and
irreducibility facts, projective-centralizer argument, simplicity and
connected-string reduction, the phase-eight normal-form classification,
the global rank bound, and retained rank-existence theorems. This is a
partial formal certificate for one elementary obstruction, not a
formalization of the PSL4/PSU4 classification or rank theorem.

The exact-invariance result is slightly stronger and shorter than the
odd-characteristic subtraction argument in the frozen phase-nine
written note. It removes the need to compare I+E_ij with I-E_ij at this
step. No frozen authored file was edited during this review.
