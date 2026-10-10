# Phase-eleven review record

10 October 2026. This phase adds a short theorem for all finite odd-order
nilpotent groups, a Frattini-action theorem and its powerful-group extension,
and a conditional uniform unitary construction. Earlier proof and execution
artifacts retain their bytes. The new formal component is the seventeenth
Lean module. These are internal mathematical reviews, not external peer
review or publication-priority determinations.

## Odd-order cyclic TPP

Root and an independent agent reviewed the complete
[short proof](../research/case_study/phase11_odd_nilpotent.md).
In a minimum cyclic-TPP counterexample, proper-pair induction forces every
pair to generate the group. Minimality in the Frattini subgroup gives an
equality triple of cyclic p-th-power subgroups; those subgroups must
generate the Frattini subgroup. Consequently Φ(P)=P^p. For odd p the group
is powerful, and the retained arbitrary-generating-list factorization
theorem gives P=AB, contradicting nontrivial C and TPP. Sylow products
give the odd-order nilpotent statement.

Root independently read the exact forward proof of Lubotzky–Mann
Theorem 1.11 on printed pages 489–490 in the author-uploaded primary text.
That retained theorem applies to the given generating pair, not merely
some unspecified cyclic factorization. This source was accessed as rendered
primary text; no verified local PDF hash or whole-paper reading is claimed.
The short argument does not depend on the earlier norm/action lemmas or
the powerful-embedding criterion. Those independently reviewed arguments
remain available with their distinct scopes.

The [bounded priority audit](../research/case_study/phase11_odd_nilpotent_status.md)
records thirty search queries and the precise primary-reading scope. It
found no matching all-class cyclic theorem, without establishing novelty.
Murthy's [Proposition 2.7](https://arxiv.org/html/2602.15796v1) already supplies
the subgroup restriction underlying the proper-pair reduction. That step,
the basic abelian bound and the powerful-group theorem are credited prior
ingredients. The new candidate argument is the Frattini reduction that
links them; it is not asserted to settle a previously named open conjecture.

The standalone order-21 witness confirms that nilpotence cannot be deleted:
three cyclic subgroups of order three have TPP and product 27>21 in C7:C3.
This example was already published in Hedtke–Murthy,
[Table 1, row [21,1]](https://arxiv.org/pdf/1104.5097). Root and the independent
reviewer freshly reran the witness; it is a re-verification of a known
boundary example, not a new counterexample or a finite census. The 2-group case
and the unrestricted source hypertope order conjecture remain unresolved.

## Frattini actions and the remaining 2-group boundary

Root and an independent agent reviewed the full
[abelian-Frattini argument](../research/case_study/phase11_abelian_frattini.md).
It proves cyclic TPP for all finite 2-groups with abelian Frattini subgroup.
The proof makes the Frattini subgroup an actual direct product of three
cyclic square factors. Their conjugation actions on a three-dimensional
binary quotient satisfy additional square equations; these force one of
four action pairs. A maximal-exponent lift then gives a prohibited central
involution. No classification or group catalogue enters this argument.

The [all-prime abelian-Frattini extension](../research/case_study/phase11_nilpotent_frattini.md)
was reviewed in full by two independent agents and root. Its norm/Jordan
argument covers p=3 as well as larger odd primes; unequal exponents and the
nilpotent Sylow product were checked explicitly. The subsequent shorter
odd-order proof subsumes its odd-prime consequence, without invalidating
the earlier proof or overwriting its records.

The [powerful-Frattini theorem](../research/case_study/phase11_powerful_frattini.md)
was reviewed in full by root and another agent, including the retained
power-subgroup and factorization statements in the Lubotzky–Mann primary
text. Powerful-group coordinates and an equivariant top-power map replace
abelian direct-product arithmetic. Induction is justified for the class
where Φ(H) is powerful for every subgroup H. Merely assuming powerful Φ(P)
has not been substituted for this hereditary condition.

The [metacyclic adapter](../research/case_study/phase11_metacyclic_adapter.md)
proves that condition for every metacyclic 2-group and every subgroup thereof.
It supplies a new derivation of the earlier metacyclic family, without
retaining a metacyclic classification or counting the result twice. The
earlier class-three odd-prime corollary is also preserved, explicitly
subsumed by the stronger odd-order theorem.

Root additionally reviewed the complete
[smallest-factor-eight restrictions](../research/case_study/phase11_cyclic_tpp.md)
and freshly ran their frozen normal-form checker. Its report exactly matches
the author and independent reports: 46 models and 96,640 outside elements.
This argument retains the phase-ten marked isobicyclic classification.
It gives necessary structure, not a complete exclusion of that boundary.

Root freshly ran the two independently implemented binary checkers and
the F3 norm checker. The saved reports match their earlier reports exactly:
32 compatible binary (action,d,f) solutions, four action pairs, and 2,187
F3 norm solutions in 81 action pairs. Bounded exponent-lifting diagnostics
cover 256 cases and 17,580 coefficient vectors. Their finite scopes do not
replace the written uniform proofs. Root also freshly ran the order-32
and order-64 witnesses showing that numerical equality plus TPP does not
imply injectivity of the global product map; logs match exactly.

## Seventeenth Lean certificate

Root reviewed the literal definitions and all six statements in
[BinaryFrattiniActions.lean](../research/case_study/formal/BinaryFrattiniActions.lean).
Vectors are Boolean triples, maps are actual column-linear maps, and the
compatibility predicate includes all three square-extension equations.
The source proves the four-case classification in both directions, its
coordinate-support consequence, and preservation of binary addition.
Finite decisions are checked by the kernel with `decide +kernel`.

The frozen public source was freshly compiled through the portable runner
with the pinned toolchain and dependency revisions. All six theorems report
only `propext`, `Classical.choice` and `Quot.sound`; no admitted lemma or
external decision axiom appears. An independent agent reviewed the source,
the saved compiler output, nonvacuity and correspondence with the written
binary lemma, without claiming its own compiler rerun.

The private compiler report is preserved as
`phase11_binary_frattini_private_check.json`; the adjacent public `.check.json`
is the separate fresh portable run. The independent audit's reference to
the private report's original path describes its original context. All
sixteen earlier reports remain byte-identical. The scope note explicitly
excludes the group-theoretic induction and lifting from the Lean result.

## Unitary template and exact examples

Root and an independent agent reviewed the complete
[generation](../research/case_study/phase11_unitary_template.md) and
[conditional intersection](../research/case_study/phase11_unitary_intersection.md)
proofs. The first retains the rank-one maximal-subgroup list and standard
rank-one unitary structure; its kernel word and coordinate-SU2 generation
are proved explicitly. The second proves quadratic descent, bounds a
regular centralizer through reciprocal eigenlines, and checks both smaller
rank-three intersections directly. Its hypothesis is middle projective
order q²−1 or q²+1. Existence of such a parameter over every intended field
is not proved.

Root and the independent reviewer freshly reran both symbolic checkers
in scratch copies: 33 generation identities and 14 intersection checks.
Reports agree with the frozen reports apart from timestamp. Both also
freshly ran the natural-action GAP checker: q=5,9,13 give string C-groups
of types {4,26,10}, {4,80,6}, {4,170,26}; a second q=9 marking of type
{4,40,6} generates the same full group and fails IP. There are 64 subset
groups and 1,024 ordered intersection checks across the four markings.
All positive checks pass; the negative control has exactly two failures.
All mathematical output fields agree apart from runtime.

Group identification uses explicit determinant-one Hermitian isometries,
their natural isotropic-plane action, and the projective unitary order
formula. No external generator database or simple-group recognition is
used. The earlier upper bound then gives maximum rank four at q=5,9,13.
These finite cases do not imply the unresolved field-uniform existence.

## Export, measurement and coverage

[Original-file provenance](phase11_original_files.json) binds the exported
original proof, code and review bytes. Frozen headers such as “private” or
“review in progress” record their drafting stage; the later bound audits
and this record state the completed review. They are not silently rewritten.
Separate root reports identify fresh execution. The snapshot manifest checks
integrity and local links; it does not rerun all historical mathematics.
Third-party full texts and scratch discovery probes remain excluded.
The abelian-Frattini certificate retains the private hash of the older
phase-three geometric reduction. Its public counterpart differs only by
the already documented replacement of a local PDF link with the primary
URL. That exact one-link difference was verified and is recorded in the
phase-eleven export provenance; mathematical text is unchanged.

The registry remains at eight principal-result reductions. The new theorem
classes and unitary cases expand precise targets without promoting entire
papers. The conditional matched-proof ratio remains 127/38≈3.34 for the
specified two L066 formulas; no new length ratio or infinity marker is
assigned. Publication priority and the unresolved conjecture cases remain
explicit in the living map.
