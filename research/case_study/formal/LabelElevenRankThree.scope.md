# Scope of LabelElevenRankThree.lean

The actual universal group has three involutions, pair relations with exponents 11, 2, 11, and all ten relations ((r1 r2)^k (r0 r1)^k)^2=1, for 1 ≤ k ≤ 10. A kernel-checked equation identifies the emitted relator list with that formula.

There are 1,024 representative names and 3,072 individually proved directed transitions. Every tree edge is a literal word definition; each other edge cites previously proved deductions and the stated relators. The row array carries proofs of all three transitions at every name, and Lean checks that its name projection covers all 1,024 names. This proves completeness and, through the generic theorem, finite facet index at most 1,024 in the actual presented group.

The three selected axiom reports concern the literal relators, completeness, and the index bound. Their dependency closure includes all edge proofs. The Python generator, the table used to discover deductions, and ACE are not trusted proof oracles. Ordinary kernel checking supplies the deduction semantics; no native-evaluation axiom is used.

The [fresh public report](../phase225_public_replay/report.json), [compiler record](LabelElevenRankThree.check.json), and [independent review](../phase226_coset_review.md) bind the result. The concrete dihedral-to-facet map and composed group-order bound 22,528 are not yet formalized. Rank-four and rank-five certificates, matrix-group orders, simplicity, signed memberships, and the complete F014 refutation remain outside this file.
