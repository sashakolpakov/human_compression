# Literal Witt models, derived planes and Figure3 stabilizers

This note supplies finite inputs to the written L092 deduction. The source constructions and their classical Mathieu interpretation are retained. The computation checks specific finite permutation groups and designs; it is not a new classification of those groups, and its completeness relies on GAP's permutation-group algorithms and DESIGN/GRAPE's full automorphism computation.

## Design models and full groups

The program phase186_witt_derived_check.g constructs the five native Mathieu designs from group orbits. For M₁₁ and M₁₂ the orbits on five- and six-subsets have sizes66,396 and132,792, respectively. Thus exactly one orbit can be the block set of the required Steiner system. For each large Mathieu group, the pointwise stabilizer of a fixed ordered t-tuple has two remaining point orbits, of sizes3 and16. The unique block through the tuple must consist of the tuple and the size-three orbit. This proves uniqueness of the native invariant block system before the actual Steiner condition is checked.

The program then checks that each t-subset occurs in exactly one block. The full design automorphism group is computed afresh from the incidence structure, its generators are checked to preserve the complete block set, and its relation to the original Mathieu subgroup is tested as an actual permutation-group inclusion or equality.

| Native model | Blocks | t-subsets checked | Native group order | Full design group order |
|---|---:|---:|---:|---:|
| S(4,5,11) | 66 | 330 | 7,920 | 7,920 |
| S(5,6,12) | 132 | 792 | 95,040 | 95,040 |
| S(3,6,22) | 77 | 1,540 | 443,520 | 887,040 |
| S(4,7,23) | 253 | 8,855 | 10,200,960 | 10,200,960 |
| S(5,8,24) | 759 | 42,504 | 244,823,040 | 244,823,040 |

For degrees11,12,23 and24 the full group equals the native group, not merely a group of the same order. At degree22 the native M₂₂ is a subgroup of index two. This pays the full-group bounds in the small-Witt exclusions: the chamber counts23,760 and285,120 exceed the respective full group orders by a factor of three.

## Explicit derived projective planes

The target plane is constructed directly from GF(4)³. Points are nonzero vectors normalized so that their first nonzero coordinate is1. Lines are the kernels of the21 similarly normalized nonzero linear forms. Hence the model is PG(2,4) by its coordinate definition, without invoking uniqueness of projective planes of order4.

For each large Witt design, remove the fixed (t−2)-set R={1,…,t−2} from every block containing R. The program finds an isomorphism of the resulting two-colored incidence graph with the coordinate plane. It then discards the graph-search conclusion as a black box and verifies the explicit point permutation: the mapped block set equals the coordinate line set, and all441 point/line incidences and nonincidences agree. Native t-transitivity transports this conclusion to every (t−2)-fold derivative.

The saved JSON witness records all original blocks, all derived blocks, the21 coordinate vectors, the coordinate lines, and each explicit point map. The independent phase186_witt_validate.py recomputes GF(4) arithmetic as coefficient-bit arithmetic modulo z²+z+1, reconstructs all coordinate lines, reconstructs each derivative from its original blocks, and checks each map. It also checks every Steiner condition and the design-preservation action of every saved group generator. The validator does not claim an independent proof that the saved automorphism generators exhaust the full group.

The file formal/WittDerivedPlanes.lean verifies explicit point and line bijections for all three displayed derivatives and proves that all incidences agree with the literal GF(4) dot-product equation. It reuses the frozen F4 arithmetic definitions and verified field-table laws in DeletedLineFourResidue. All nine new axiom reports use only propext, Classical.choice and Quot.sound. There is no assumed incidence-isomorphism axiom, sorry, admit or native_decide. Two deliberately altered coordinate-incidence maps are rejected by Lean in the fresh replay. The generator binds the sorted GAP line-support convention to the separately ordered coordinate linear forms; the resulting source is checked byte-for-byte against the reviewed Lean file.

This formal certificate starts from the displayed finite derivative tables. Its identification of those tables as derivatives of the original Witt blocks remains outside Lean, checked independently by GAP and Python. The all-rank residue recursion, full design automorphism groups, and stabilizer structures also remain outside this Lean certificate.

## A common stabilizer calculation

Let G be the native group, B a block of size k, and H=G_B. For k=6,7,8, restriction to B gives an exact sequence
\[
1\longrightarrow N\longrightarrow H\longrightarrow A_k\longrightarrow1.
\]
The computation proves that N is elementary abelian of order16, the image is the actual alternating permutation group on B, and a complement C exists with N∩C=1 and NC=H. Thus H=2⁴:A_k, with the action supplied by the saved permutation realization. An order factorization alone is not used to infer splitting.

A marked object is (T,B∖T), where |T|=t−1. Its stabilizer M is exactly H_T. Since N fixes every point of B, it fixes T, and
\[
M=N\rtimes C_T,\qquad
C_T\cong (S_{t-1}\times S_{k-t+1})\cap A_k.
\tag{W1}
\]
The program verifies the actual image equality, the complement intersection and the product order in (W1). These give all block and marked labels in the three Mathieu rows of Figure3:

| Group | Block stabilizer | Marked stabilizer | Orders |
|---|---|---|---|
| M₂₂ | 2⁴:A₆ | 2⁴:S₄ | 5,760;384 |
| M₂₃ | 2⁴:A₇ | 2⁴:((C₃×A₄):C₂) | 40,320;1,152 |
| M₂₄ | 2⁴:A₈ | 2⁴:((A₄×A₄):C₂) | 322,560;4,608 |

For the latter two descriptions, take the even permutations in the two disjoint factors. Their product has index two in the parity-matched subgroup; a pair of transpositions, one in each factor, gives a complementary involution. This proves the displayed semidirect descriptions directly.

The source writes the M₂₂ marked group as 2²·2⁴:S₃. To bind that notation as well, the program computes Q=O₂(M), proves |Q|=64, Z(Q)≅2² and Q/Z(Q)≅2⁴, proves M/Q≅S₃, and finds a complement to Q. Thus both descriptions refer to the same explicitly constructed group. The dot in the source's middle extension is retained; no unwarranted splitting of Q over its center is asserted.

For the first row, G=PSL(3,4) acts on the coordinate plane. Applying the identical block calculation to a line of size5 gives the line stabilizer2⁴:A₅, and fixing a point on that line gives the marked stabilizer2⁴:A₄. Projective duality, which normalizes PSL(3,4), gives the same2⁴:A₅ point stabilizer. Their orders are960 and192.

## Ordinary subset stabilizers

For an ordinary j-subset R, the set stabilizer G_R acts on the j-fold derived design. The computation verifies faithfulness of this action, finds an explicit incidence map to the appropriate smaller native Witt design or coordinate projective plane, and conjugates the actual residual permutation group by that map.

The pointwise stabilizer of R becomes precisely the smaller native Mathieu group, or precisely the group generated by the projective action of SL(3,4) when j=t−2. This is a group equality in the target permutation action. The set stabilizer gives:

| Native group | Ordinary subset size | Actual identified stabilizer |
|---|---:|---|
| M₂₂ | 1 | PSL(3,4), order20,160 |
| M₂₃ | 1 | M₂₂, order443,520 |
| M₂₃ | 2 | PSL(3,4):C₂, order40,320 |
| M₂₄ | 1 | M₂₃, order10,200,960 |
| M₂₄ | 2 | full Aut(S(3,6,22)), order887,040 |
| M₂₄ | 3 | PΓL(3,4)=PSL(3,4):S₃, order120,960 |

The source labels the penultimate group M₂₂:2. The current full-group computation gives the actual degree22 overgroup; identifying the colon as a split extension additionally requires a complementary involution, which is checked in the finite runner. The projective index-two case is also checked to split. For the final case the program builds PΓL(3,4) explicitly from GL(3,4) acting on normalized vectors together with the coordinate Frobenius map, and verifies equality with the transported stabilizer. Its quotient over PSL(3,4) is C₃:C₂: determinant modulo cubes gives C₃, and Frobenius inverts it. A diagonal matrix of order3 and the Frobenius map supply a complement, proving the displayed S₃ extension.

Copied-point stabilizers are ordinary-point stabilizers. This pays the Figure3 isomorphism labels, with explicit actions rather than recognition from orders.

## Remaining boundary

These finite computations complement the uniform written proofs of firmness, residual connectivity, (IP)₂ and the chamber-fiber criterion. The root's existing phase182 Mathieu fiber check remains the transitivity input; it is not reimplemented here.

The names Γ₂₃(4) and Γ₈(4) refer to geometries in A. Pasini, *Flag-transitive Extensions of Dual Affine Planes*, European Journal of Combinatorics17(1996),657–671. L092 identifies its two rank-five residues with those geometries. Their distinct type-size multisets and their actual M₂₃ and2⁴:A₈ actions are proved here, but an object-level identification with Pasini's definitions is still needed. Failed retrieval of that primary text is recorded as an intake gap. Equality of group names or type sizes does not pay this clause.
