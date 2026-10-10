# Independent review of the four-family PGL construction

Review status: **accepted for the complete four-family question in the
bound source**. The complete written proof, exact source scope, frozen
certificates and formal boundary have been independently reviewed. No
registry or publication change is made here.

## The exact historical question

I read the complete eleven-page Leemans–Toledo author manuscript dated
May 15, 2023, and visually inspected physical/printed page 9. The final
paragraph of Section 5 asks for infinitely many regular rank-four
maniplexes in each of four end-group configurations: one end is PGL2(q),
and the other is S4, A5, PSL2(q) or PGL2(q). This is an existence question,
not a classification or an assertion about every prime power. The
four-family answer must remain separate from recovery of the source's
principal PSL results and from corrections to other source statements.

The preceding unqualified sentence about all proper nonabelian PGL
subgroups is not a valid subgroup list: affine and dihedral groups are
counterexamples. The proposed proof correctly uses the actual maximal
subgroup classification instead. Giudici's Theorem 2.2(6), physical and
printed page 4, supplies A5 in PSL; Theorem 3.5, physical and printed page
10, supplies the prime-field PGL list. Both primary pages were inspected
visually. The incorrect printed-page locators in the working note were
reported before author freeze.

The separate `phase261_priority_search.md` records twelve exact queries,
the institutional author copy, the earlier arXiv version and the journal
record. It found no later primary resolving this exact question. This
bounded search does not establish historical priority or continued
openness as of 2026.

## Universal proof assessment

The constant quadruple is nonsingular for every prime p>3. Its projective
classes are four distinct nonidentity involutions, and the three required
distant pairs commute. The product of the middle pair supplies the full
prime-field lower root subgroup, not merely an element of unspecified
p-power order. The first and fourth matrices each move its fixed point.
Conjugation and the transitivity of the full root subgroup off that point
give the opposite root subgroup. Elementary row reduction therefore
puts PSL2(p) in both end groups. The determinant character then gives
PGL/PGL for p congruent to 3 modulo 4 and PSL/PGL for p congruent to 5
modulo 12. The latter includes p=5. No extrapolation from samples or
maximal-subgroup classification is needed for these two families.

For p>5 congruent to 3 or 5 modulo 8, the maximal S4 in PGL is outside
PSL and its determinant character is the ordinary sign character. The
tetrahedral marking supplies the commuting endpoints and adjacent orders
three. The unique nonidentity common projective centralizer of the first
dihedral pair lies outside S4, whose internal centralizer of that S3 is
trivial. Maximality proves generation of the entire ambient group.

For the other end, the proof pays separately for generation. An affine
point stabilizer contains no distinct commuting involutions in odd
characteristic. In a dihedral candidate, the middle involutions are
reflections with product order three. A central last involution would be
central in the whole marked group; a noncentral one differs from the
first reflection by the central involution. The other adjacent product
then has order six, and its cube recovers that central involution. Thus
the remaining pair generates the first reflection, contradicting the
noncommutation at the other end. This argument uses neither IP nor a
C-group classification.

If the remaining proper maximal candidate is S4, its two relevant odd
involutions are transpositions. The distinct commuting last involution
has exactly two possibilities, giving last adjacent order three or four.
The whole ambient group would be a quotient of the finite Coxeter group
[3,3,3] or [3,3,4]. Their orders 120 and 384 exclude every prime p>5
occurring in the construction. Hence the other end is the whole PGL.

For p congruent to 9 or 11 modulo 20, an A5 inside PSL has its standard
hemi-dodecahedral marking. The unique involution centralizing its first
D10 lies in a cyclic torus of order p+1 or p−1, respectively. In both
progressions the half-order is odd. The determinant map is onto the
square-class group on both split and nonsplit tori; its kernel is the
half-order PSL torus. Thus the added involution is outside PSL. No proper
maximal PGL subgroup outside PSL contains A5, so the four generators
generate PGL. The same affine/dihedral exclusion applies to the other
end. A putative S4 would put its first two involutions in A4, whose
involutions commute, contradicting their product order three. This pays
for the second full end without assuming a classification of maniplexes.

I requested a short explicit split/nonsplit torus and determinant
explanation to make this arithmetic interface visible, and supplied the
concrete A5 triple
`(1,2)(3,4), (2,4)(3,5), (1,3)(2,4)` for the final note or certificate.
Neither request changes the proposed theorem's scope.

Each progression is reduced, so the retained Dirichlet theorem supplies
infinitely many primes. The strictly increasing orders p(p²−1) ensure
pairwise nonisomorphic maniplexes. The regular-action construction checks
the source's actual colored-maniplex definition: distinct involutions
make every generator and pair product fixed-point-free, generation gives
connectedness, and the color-preserving automorphism group is exactly the
opposite regular action. Reversing the marking puts the full group at
the specified facet end. No polytopality, intersection property or
additional orientability condition is being inserted into the question.

## Independent native constructions

`phase261_independent_families.g` imports no phase257 code. It builds PGL
on the projective line directly from independently evaluated fractional
linear maps. It locates small subgroups using native GAP and transports
the standard S4/A5 markings through actual group isomorphisms. It checks
four distinct involutions, all distant commutations, the exact whole
group and both actual distinguished end subgroups.

The seventeen positive samples are:

| Family | Primes |
|---|---|
| PGL/PGL | 7, 11, 19, 23 |
| PSL/PGL | 5, 17, 29, 41 |
| S4/PGL | 11, 13, 19, 29, 37 |
| A5/PGL | 11, 29, 31, 71 |

All pass. Three excluded-parameter controls establish that the arithmetic
and small-prime boundaries have content: the S4 construction at p=5 has
two S4 ends; the A5 construction at p=19 generates PSL rather than PGL;
and the constant quadruple at p=13 generates only PSL.

The program also exhausts all 48 local S4 choices relevant to the
other-end argument: 24 give last adjacent order three, and 24 give order
four. It computes the exact literal Coxeter presentation orders 120 and
384. These are finite cross-checks of the uniform written argument, not
the source of its infinite quantifiers.

An early reviewer test mistakenly included p=59 in the positive A5 list.
It was correctly rejected because 59 is 19, not 9 or 11, modulo 20.
The test list was corrected to p=71 and explicit progression guards were
added. This was a reviewer parameter error, not a counterexample to the
stated theorem.

## Attribution and final verdict

The question and the strategy of adjoining a common dihedral centralizer
come from the source. The projective centralizer theorem is reused from
the reviewed umbrella. The local S4/A5 maps, subgroup classification,
Dirichlet theorem and finite Coxeter identifications remain classical
inputs. The constant quadruple is a normalization of the source's known
special-linear family. If the source parameter is s with s²=−1 and
D=diag(−s,1), direct calculation gives D A0 D⁻¹=−s R0,
D A1 D⁻¹=s R1 and D A2 D⁻¹=s R2. The fourth projective class is
then fixed by the uniqueness of the common centralizer. The proposed
answer uses this family at other determinant classes, adds the four
parameter selections and complete arguments forcing the opposite end
to be full. It does not claim the source's normalized matrices as a new
construction. Historical priority for the added arguments is not
inferred from a bounded search.

The all-parameter written proof is accepted. I read the final academic
manuscript completely, all twelve source/interface dispositions and eight
complete proof spans, the actual author programs and all eleven Lean
declarations. The final six-page PDF was inspected page by page; the
mathematics and source attribution are readable without overlap. No
frozen-author correction is requested.

The accepted author manifest is `phase257_manifest.json`, SHA256
`e27a461990413f41af0799efa7f41f965ec534691251fe1fe8e12ca5b80ba67b`,
binding 22 exports and eight retained inputs. Fresh independent replay
with primary verification passed in 11.104 seconds, including all 16
author examples, all 17 independent examples, 48 small S4 cases, the two
literal Coxeter presentations, three excluded-parameter examples and
four rejection mutations across the two implementations. All eleven
Lean declarations compiled with only the declared standard axioms.

The Lean statements establish actual matrix and lower-unipotent
identities: squares, determinants, distant anticommutation, adjacent
products, nonscalarity, pairwise nonproportionality, natural powers,
scalar-period equivalence and root-group exhaustion. They do not
formalize the complete generation lemma, subgroup classification,
exceptional-group arguments, Dirichlet theorem or the complete
four-family theorem. The false-period control and the matrix/marking
controls reject relevant incorrect statements or objects. Their success
does not replace the written proof assessment above.

The two native implementations use different projective actions and
different sample sets. GAP can choose different subgroup isomorphisms;
the returned markings and some adjacent orders need not be byte-identical
between replays. The verified targets are the actual marked-group
conditions and end groups, not agreement with a stored list of
permutation bytes. The runner checks those targets explicitly.

This admits one complete affirmative answer to the four-family
conjecture stated in the bound source. It adds no principal-source
recovery, whole-paper claim or compression rate. The bounded search
did not find a later solution, but historical priority and the exact
state of openness immediately before this project remain unproved.
Publication should therefore describe the proved answer and its source,
and retain that priority qualification. A full Lean certificate must
not be claimed.
