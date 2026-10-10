# Independent review: centralizer extensions of projective-line maniplexes

**Decision: accept the corrected principal PSL contract of phase258.** The
review covers the entire bound manuscript, its source contract, all 32 ledger
rows, both new mathematical programs, the retained ten-row program, the three
new Lean proofs and their stated limitations. It permits one principal-source
admission after the root review. It does not award a whole-paper, question,
historical-priority or compression-ratio credit.

The author manifest is `phase258_manifest.json`, SHA256
`ccd07fd98645aa1ae31213b9c7d3f76501ca5225ae05992b64e7ac9dc80915cc`.
All 27 exports and 13 retained bindings were checked. The complete nine-page
render was inspected visually; no missing text, overlapping mathematics or
unreadable table was found. No frozen author file was changed.

## 1. Source and exact coverage

The primary is Leemans–Toledo, *Maniplexes with automorphism group PSL(2,q)*,
the eleven-page author manuscript dated 15 May 2023, bound as
`sources/psl2_maniplex2023.pdf`, SHA256
`ae0e8cd95b06b682afd7bff89f9e1dfd14977a5fe3275ad9deabf78c8e132c93`.
All eleven pages, including the references and final remarks, were read. The
same edition was already read for the separate phase261 question review;
its complete mathematical text was checked again here against the application.
No assertion is made about uncollated published or later versions.

| Primary statement | Accepted replacement |
|---|---|
| Introduction p.2; rank restriction p.4 | No rank at least five for any prime power, with small fields and characteristic two handled explicitly. |
| Theorem 3.10, p.6 | Every rank-three end is S4, A5 or the full PSL group. |
| Proposition 4.2, p.7 | If both ends are proper, precisely the marked 11-cell and 57-cell occur; local maps, types, IP, uniqueness and duality are covered by the retained complete table. |
| Lemma 4.3, p.7 | No rank-four marking in characteristic two. |
| Theorem 4.4, p.7 | The entire odd-divisor half-turn extension theorem, for every odd prime power satisfying its hypotheses. |
| Lemma 4.5 and Corollary 4.6, p.8 | The explicit source marking for every prime congruent to 1 modulo 12, both ends full, infinitely many nonorientable examples. |
| Proposition 4.7 and Corollary 4.8, pp.8–9 | A5/full-PSL examples for every prime congruent to ±1 modulo 20 other than 19, with the claimed infinitude and nonorientability. |
| Suzuki remark, p.9 | The rank bound follows from the explicitly retained fixed-point theorem; the nonsimple small group is separately excluded. |

The introduction and conclusion omit the possible S4 end. The application
supplies the complete additional family for primes congruent to ±1 modulo 24,
not only a sample. It also gives direct finite counterexamples to the literal
self-duality sentence and involution-centralizer maximality claim. These are
corrections to the bound edition, not newly answered open questions.

The final PGL discussion and four-family conjecture are a separate scope.
Phase257/261 addresses that question. It is not silently included in this
principal recovery, and the false blanket PGL subgroup sentence is not a
retained classification input. This application does not enumerate every
rank-four PSL marking or every possible self-duality.

### A necessary reading of the two subfield rows

There is a further literal-versus-intended qualification in source Lemmas 3.7
and 3.8, p.5. Their printed statements exclude ends merely *isomorphic* to
PSL2(q′) or PGL2(q′) with q′<q. Taken without a natural-subfield qualification,
these statements are false: the source's own 11-cell has ends
A5≅PSL2(5), and the accepted PSL2(23) example has an end
S4≅PGL2(3). The correct exclusion is for the natural subfield embeddings in
Dickson's subgroup list. Frozen258 §4 states this distinction explicitly and
its ledger labels the rows as subfield exclusions. This review accepts those
qualified rows, not the unqualified abstract-isomorphism formulations. This
annotation is additive; it does not change the author freeze or the principal
theorems. No further question or source credit attaches to it.

## 2. General mathematical audit

The category change is proved, rather than assumed. The regular left action
of a marked group has exactly its right regular group as the full
colour-preserving automorphism group. Distinct nonidentity involutions ensure
the required fixed-point-free adjacency products. This proves the actual
maniplex interface, its face indices, and its reversal criterion without IP.
The even-word subgroup is normal of index at most two; simplicity proves
nonorientability in the stated cases.

In a centre-free string marking the first adjacent pair cannot commute:
otherwise its first generator would commute with every generator. At rank
five the fourth and fifth generators are distinct nonidentity elements of
the common centralizer of that noncommuting pair. The retained projective
centralizer theorem therefore rules out rank five and above. The argument
does not use a direct-product claim whose trivial-intersection premise would
need proof. In characteristic two, the abelian centralizer of the fourth
involution instead forces the first pair to commute. PSL2(2) and PSL2(3) are
treated directly. In the remaining simple cases, an adjacent commuting pair
would split the string into commuting nontrivial normal generated subgroups,
which simplicity forbids. Thus the adjacent-order hypotheses used later are
proved without IP.

The proper-end exclusions are complete relative to the retained Dickson
classification. Cyclic and elementary abelian groups cannot contain the
nonabelian first dihedral pair. Involutions cannot generate A4. Distinct
involutions in the odd-characteristic affine case have multiplier −1 and
cannot commute. A dihedral end with distinct commuting endpoints has a
central involution; common-centralizer uniqueness would make the fourth
marker that involution, contradicting properness. For a natural subfield
end, the descent theorem places the fourth marker in the same PGL2(k),
and the strict order inequality excludes generation of PSL2(q). No blanket
maximality or dihedral uniqueness assertion from the source is imported.

The passage from two proper ends to the ten universal presentations needs
an actual local sggi-to-C result. The new program supplies it before using
the old table; our independent computation confirms it. All fourteen
compatible ordered type pairs occur among the ten rows and their reversals.
Their presentations impose exactly the two complete local presentations and
the distant commutations. The quotient elimination is valid without global
IP: the trivial rows, collapsed-end rows and order-96 row cannot work; the
order-120 row is S5, whose only nontrivial proper quotient is C2. The two
remaining universals are the simple groups of orders 660 and 3420, so their
only nontrivial quotients are themselves. The order formula fixes q=11 or
19; the retained actual markings provide IP, duality and the ordered-marking
uniqueness. The finite GAP presentation algorithms remain an explicit trust
boundary, not a Lean proof of those orders.

For the extension theorem, k>1 divides one of the two coprime PSL torus
orders and is prime to the characteristic. Its rotation is semisimple with
a determined eigenline pair. Both generating reflections normalize that
pair. The unique involution in the even cyclic torus centralizes the
dihedral pair and lies outside the odd-rotation dihedral subgroup. The
second adjacent order excludes coincidence with the third marker. The
original three markers still generate the full group, so the new object
really has the same group and the original map as its unique facet. The
small cases where the hypotheses are impossible do not yield exceptions.

For a proper maximal end, the application additionally proves the internal
common centralizer is trivial; this is what places the new half-turn
outside that end. The A5 and S4 prime ranges are the exact cases of Giudici,
Theorem 2.2(6),(8), physical and printed p.4. That primary statement was read
and visually checked in phase261 and rechecked here against the two uses.
The opposite end is full by the proved two-proper-end classification and
the excluded field values. The application carefully does not assert that
there are no Class 2 markings at p=19.

The constant matrices are explicitly conjugate to the source's original
three matrices. Both −1 and 3 are squares for p≡1 mod 12, so the projective
classes lie in PSL. Their two root subgroups give elementary generation of
SL2(Fp), and hence PSL2(p). The trace-zero centralizer formula binds the
fourth marker to the source extension. Its opposite end contains an element
of order p≥13, excluding the two possible proper exceptional ends. Dirichlet
and the strict growth of group orders establish the claimed infinitude;
they are retained classical inputs.

## 3. Independent evidence and controls

The fresh complete reviewer replay is produced by `phase263_check.py`.
It first runs the frozen author replay with primary verification, then runs
the independently written checks. No author mathematical function is imported
by either independent checker.

`phase263_independent.py` implements permutation composition, closure,
orders and intersections using Python tuples and sets. It enumerates every
ordered distinct involution triple in S4 and A5, admitting only the string
commutation and generation conditions. It finds exactly 72 and 360 triples,
then checks all 64 subset intersections for each: 27,648 tests. The three
type classes have multiplicities 24 in S4 and 120 in A5; natural symmetric
conjugation is already transitive on each class. Thus no unseen automorphism
classification assumption is needed to conclude precisely three classes.

The same independently implemented closures verify the literal degree-24
PSL2(23) marking: whole order 6072, end orders 24 and 6072, adjacent orders
3,4,12, one vertex and 253 facets. Its first end has the S4 element-order
inventory and satisfies IP. They also verify the literal degree-14 marking
of order 1092, both ends full, type 3,7,3, and all four reversal conjugacies.
Identification with the named projective groups is additionally checked in
the separately replayed GAP certificate. Conjugating only the fourth
PSL2(23) marker by a transposition preserves its involution order but destroys
a distant commutation; the independent checker rejects the corrupted data.
The altered PSL2(13) conjugator is also rejected.

`phase263_field_checks.g` constructs different native cases: A5/full-PSL
at p=59 and 61, S4/full-PSL at p=71 and 97, and full rank-three extension
inputs over the nonprime fields q=25 and 49. In every case it verifies actual
common centralizers, all four distinct involutions, the string relations,
the whole generated group and both end orders. These six checks supplement
the eight author models. They test the interfaces; the all-prime and all-field
theorems are justified by the written arguments, not by sample extrapolation.

The full author replay also rechecks all ten universals, the exact source
basis adapter, the centralizer-maximality counterexample, the dihedral
non-C control, and the two rank-hypothesis countermodels. GAP sometimes
returns exit status zero after an error; both drivers consequently check
completion markers and error output as well as exit status.

The review's initial mutation used multiplication by a transposition and
was correctly rejected earlier, at the involution check. The final control
was strengthened to conjugation so that it specifically tests the distant
commutation condition. This was a review-harness adjustment; the author
mathematics and author freeze were unchanged.

## 4. Formal boundary, attribution and cost

All three new Lean declarations were read in full. They prove closure of
commutation from generators, noncommutation of the first pair in a
centre-free string marking, and the rank-four upper bound under the actual
common-centralizer condition. Distinctness, nonidentity, generation and the
string commutations appear as explicit hypotheses. The proofs do not assume
IP or the final rank bound. The fresh replay compiles them and the two
retained characteristic-two interface declarations, with only `propext`,
`Classical.choice` and `Quot.sound` in the axiom reports. Removing the string
hypothesis or permitting identity markers fails, with actual finite
countermodels explaining both failures.

The separate six matrix-normal-form declarations in phase237 retain their
previous scope; they are not new phase258 declarations and are not recompiled
by its driver. Neither set formalizes Dickson, projective conjugacy and
descent, torus existence, the finite universal orders, Dirichlet, all positive
families or the full principal theorem.

Attribution is adequate. The source's theorems and normalized matrices remain
Leemans–Toledo results. The exceptional local maps and 11-/57-cell geometry
retain the earlier authors and Leemans–Schulte classification. Dickson,
Giudici, cyclic tori, Dirichlet and the Suzuki fixed-point theorem are retained
inputs. The new contributions here are the explicit category interface,
proof organization, formal verification, omitted S4 family and bounded
literal corrections. No general first-priority assertion follows.

The following are the exact UTF-8 artifact sizes, not a matched compression
measurement:

| Mathematical or verification artifact | Bytes |
|---|---:|
| Full retained Topic E umbrella | 23,390 |
| Complete new application | 27,710 |
| Retained ten-row GAP program | 5,310 |
| Two new GAP programs | 8,237 |
| Three new Lean declarations | 3,431 |
| Retained characteristic-two Lean file | 3,462 |
| Separately retained phase237 matrix Lean file | 6,834 |
| Author replay driver | 7,940 |
| Formal dependency manifest | 3,518 |

The two full mathematical manuscripts total 51,100 bytes; with all three
mathematical GAP programs they total 64,647 bytes. All displayed rows total
89,832 bytes. The last figure is an explicitly enumerated artifact subtotal,
not a complete transitive toolchain acquisition cost or a rendered-paper
denominator. It excludes the PDF, ledger, review/support records, external
software and proofs of retained classical background. The phase237 driver
is not included, so that subtotal must not be represented as a replay of the
entire older matrix package. Future topic measurements must apply the same
declared retained-input convention to source and replacement, pay the full
umbrella once within the topic, and include every required program. No
numerical compression rate is admitted by this review.

## 5. Disposition

The main principal contract is complete and independently accepted, with the
source corrections and subfield qualification above. All 32 ledger rows are
accepted with their stated dispositions; the two subfield rows must retain
the natural-embedding interpretation. The unused auxiliary Lemmas 3.2 and
3.4 are not silently claimed to be rederived. There is no mathematical
revision request for the frozen author packet. Admission may add one
principal-source record, once, and no question or whole-paper record.
