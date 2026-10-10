# Torsor and matrix compression: demonstrated scope

10 October 2026. The mathematical proposal is a finite group torsor with a
marked family of invariant partitions. An intrinsic version is the split
algebra Q^X, its group action, and marked invariant subalgebras: algebra
automorphisms are exactly permutations of the primitive idempotents. The
[core note](torsor_matrix_theory.md) proves this description and explains
which geometric constraints it solves. These are internally reviewed proof
drafts and exact computations, not externally reviewed publications.

The [detailed introduction](../../INTRODUCTION.md) explains the ideas with
worked examples. The [living paper map](../../PAPER_MAP.md) records all 152
indexed works, including the 1996–2006 intake; this note focuses on reductions.

## The common calculus

After choosing a torsor point, write

    A_H[x,y] = 1_(x^(-1)y in H).

Then

    A_H Hadamard A_K = A_(H intersect K),
    A_H A_K = |H intersect K| A_(HK),
    BooleanClosure(A_H OR A_K) = A_<H,K>.

The first identity gives subgroup intersections, the second counts
factorizations, and the third gives generated subgroups. A typed coset Helly
condition gives flag transitivity. Panel sizes are subgroup indices; after
flag transitivity is established, connected residues are subgroup-generation
conditions. A missing reversing symmetry is an automorphism obstruction for
the marked system.

This is exact, but recognition alone is not proof compression. The substantive
reductions below supply the orbit normal forms, coordinate kernels, affine
lattices or relation matrices that actually solve those conditions. The common
language incorporates established coset geometry, finite group actions and
linear algebra; no claim of inventing those subjects is made.

## Results reconstructed

Catalogue IDs refer to [the literature inventory](literature_inventory.json).
Each row names the exact target rather than counting a partial reduction as
an entire paper.

| Source and target | Replacement argument | Scope and remaining input |
|---|---|---|
| L102 (2003), Section 5.1.2 and the remaining spread case | Prime-degree arithmetic, irreducible semilinear descent and an explicit scalar-affine converse | Proposed exact existence and uniqueness of the spaces in the one-dimensional RWPRI case; source translation/spread reduction retained, external review and priority unverified |
| L096 (2004), geometric shadow-IP decision problem | Flag-constrained covering inequalities, orbit normalization and a rank-two four-cycle argument | Exact criterion and independent finite checks; original Magma implementation and sporadic tables not reproduced by this criterion |
| L104 (2002), full principal census in every rank | Arbitrary-Borel maximal-residue augmentation, normalizer panel actions and automorphism/type fusion | Complete 8/19/3 census and higher-rank exclusion independently reproduced, conditional on TomLib; original geometry lists are not inputs |
| L109 (2000), dihedral classification | Rank-two rigidity, prime-index subgroup arithmetic and CRT Helly | Complete published all-rank theorem and counts matched through L110 Theorem4; original full-paper comparison still unavailable |
| N001–N003 and L089 (1998–2005), symmetric-group tree geometries | Forest component groups, laminar subset flags, balanced cuts and Boolean shadow witnesses | Four 1998 principal property tests and specified tree/path results rederived; foundational 1997 classification retained and source-access limits explicit |
| L114/L110 (1999–2001), Suzuki subgroup realizations | Normalizer uniqueness, field intersections, trace transversal and invariant-subspace obstruction | Proposed decisions for every printed parameter shape: four impossible intersections; one further embedded pattern fails RWPRI; all others realized. Candidate completeness was subsequently disproved and withdrawn; a full replacement classification and external priority remain unresolved |
| L066, *On pairs of commuting involutions in Sym(n) and Alt(n)*, all four principal results | Five orbit multiplicities for C2²-actions, two rational generating functions, one degree-six orbit certificate | All principal counts and both S6/A6 polyhedron conclusions recovered; standard automorphism theorems remain inputs |
| L032, *On regular polytopes of 2-power order*, Theorem 1.2 | Explicit square-grid seed plus independent dihedral factors | Whole principal all-rank existence theorem; no classification of every group |
| L030, *An infinite family of locally X graphs based on incidence geometries*, principal construction and parameters | The single tensor relation K_r tensor KG(N,k), replacement distances and a spectral automorphism argument | Construction, residues, diagram and full graph automorphism group recovered; two source displays corrected |
| L008, *Testing chirality on hypertopes*, Theorem 1.1 | Double-coset extension fiber with two points, then a uniform residue argument | Principal criterion recovered, retaining the standard marked-inversion correspondence |
| L034, *Existence of regular 3-hypertopes with 2^n chambers*, Theorem 3.2 and parts of Conjecture 3.3 | Same grid/dihedral construction; presentation comparison; cyclic triple-product lower bound | Presented construction recovered; alternate printed quotient display not separately verified. Bound proved for minimum pair order ≤8 and for hereditary powerful-Frattini derived groups, including metacyclic and abelian-Frattini cases; full bound remains |
| L035, *2-groups behaving as automorphism groups of regular 3-polytopes*, Theorems 1.2 and 1.3 | Grid construction, bounded cyclic-core quotients, eight binary extension models | Both principal theorems recovered, including completeness of all eight families; retains Lucchini's theorem and one exhaustive order-256 SmallGroups census |
| L025, Suzuki graph Conjecture 3.2 | Three zero matrix entries solve a four-parameter coset-walk word | Proposed all-q proof of exactly q−1 pentagons per edge; full matrix-membership equivalence Lean checked; graph/source correspondence is a written proof |
| L012, *Regular 3-polytopes of order 2^n p*, Theorem 5.1 and Corollary 5.2 | Three affine transformations, one index-48 presentation, three invariant lattices | Actual three families and every order 3·2^n for n≥5 recovered; other classification/nonexistence results remain |
| J2 and Sz(8), published rank-two censuses | One normalizer-orbit algorithm on subgroup inclusions | All eight J2 rank-two objects and all 29 Sz(8) objects reproduced; complete GAP subgroup catalogues are explicit inputs; J2 higher ranks are now handled above, all-q Suzuki classification remains |
| PSL(2,3^e), complete A4–A4 counting family | Additive torsor F_(3^e)/F_3, sign and Frobenius orbits | Published prime-degree family recovered and extended to composite odd degrees as connected locally two-transitive geometries; Dickson's subgroup theorem remains an input; composite degrees are not RWPRI |
| L009, *Geometries with trialities arising from linear spaces* | Two flag partitions and D=(A−I)(B−I); a common deleted-pencil residue | Construction, correlation group, connectivity and Hermitian transitivity branch recovered; classification of the underlying linear spaces remains |
| L029, *On residual connectedness in chiral geometries* | Two cyclic matchings connect rank-two residues | Designated-action theorem and rank-three corollary; a bridge to the source's literal full-automorphism formulation remains unproved here |
| L050, McLaughlin-subgraph codes | Adjacency identities and complementary projections over F3 | Orthogonality/LCD/complement-dual assertions; ranks, minimum distances, weight enumerators and module classifications remain |

These rows do not establish that dozens of entire papers follow from one short
theory. They establish several complete principal-result reductions and further
precisely identified partial reductions. Classification inputs are not erased
by rewriting them as hypotheses. Nor does a shorter proof establish a personal
or historical judgment about the original authors.

## Useful extensions beyond the reproduced statements

The [odd-order nilpotent theorem](phase11_odd_nilpotent.md) reduces every
cyclic-TPP inequality in that class to minimality and a retained powerful-group
factorization theorem. The [Frattini extension](phase11_powerful_frattini.md)
uses a four-case binary action lemma to handle the hereditary powerful-Frattini
2-group class; a [short adapter](phase11_metacyclic_adapter.md) recovers the
earlier metacyclic family within that framework. The unrestricted 2-group
inequality remains. These are theorem gains without a new measured ratio.

The [unitary template](phase11_unitary_template.md) and its
[two-form intersection proof](phase11_unitary_intersection.md) give a conditional
family for q≡1 mod4 and exact rank-four examples at q=5,9,13. Suitable
parameter existence for every field remains unresolved. The source survey
receives partial-progress coverage, not a full-survey reduction.

The [all-rank action formula](elementary_action_theorem.md) counts independent
commuting r-tuples modulo point conjugacy and generator reordering. Subspace
Möbius inversion enforces faithfulness; a character filter enforces even
permutations. It produces rank-three and rank-four counts without enumerating
the symmetric group on the underlying points.

The [construction theorem](compression_phase2.md) inflates selected even
dihedral edge orders independently. If B is the explicit seed, q_e its old
orders, and m_e their chosen multiples, the result has

    |H| = |B| product_e (m_e/q_e),
    ker(H_I -> B_I) = product_(e subset I) K_e.

The coordinate formula proves IP, and a separate coordinate-consistency
argument proves the coset Helly property. The cube seed handles arbitrary even
diagrams; square-grid quotients handle the required extra powers of two.

The [cubic affine model](phase2_cubic_lattices.md) identifies the source's actual
three {6,6} families as quotients by m times the lattices
4Z³, 4D3, and 8Z³+4Z(1,1,1). Their orders are 192m³, 384m³ and 768m³.
A single excluded difference vector proves the required intersection for every m.

The [classification note](classification_compression.md) gives a closed count
for every odd extension degree in the A4 family, including the necessary
nonfree Frobenius correction when three divides the degree. It also isolates
a published ordered/unordered counting discrepancy without changing the
published isomorphism counts.

The [incidence note](incidence_compression.md) proves uniformly
`Cor(Delta(S)) = C3 semidirect_epsilon Cor(S)` for thick uniform linear spaces.
It connects the 2005 unital construction with the 2026 triangle construction:
their difficult residues differ by deleting one pencil. The same norm-shell
torsor argument proves the latter residues connected for every prime power q.

The [cyclic-core theorem](phase3_classification.md) reduces groups of type
{4,2^t} and order 2^(t+s) to marked quotients of order 2^(2s−2), independent
of t. For s=3,4,5, the remaining extensions have at most two binary parameters.
This supplies a completeness argument as well as constructions. The finite
catalogue input for s=5 is explicitly retained, rather than counted as a
consequence of the matrix identities.

The [Suzuki word calculation](suzuki_cycle_proof.md) and
[Wenger moment calculation](phase3_egr_conjecture_audit.md) add another
reusable operation: express closed walks as a short matrix system and solve
its fibers. In the Suzuki family the solution set is F_q*, giving q−1;
in the classical Wenger families a Vandermonde rank calculation handles
all characteristics and corrects one later preprint's odd-q formula.

The [hypertope order reduction](phase3_order_bound.md) identifies the
unresolved sharp bound with a cyclic triple-product inequality inside the
Frattini subgroup. It proves several uniform classes, while preserving the
distinction between the coset Helly property and subgroup IP. The
[PSL4 reductions](phase3_psl4.md) likewise isolate precise remaining
representation configurations rather than claiming a full rank classification.

The [fixed-excess theorem](phase3_bounded_families.md) makes the cyclic
extension method general: for fixed excess, the number of cocycle variables
stays bounded while the long edge order grows. Marked group isomorphism is
a free linear change-of-section action. Schreier kernel exponents then test
IP by gcds and fiber congruences without enumerating the growing group.
The finite quotient catalogue remains an explicit input.

The [rank-seven tensor proof](phase3_psl4_rank7.md), independently reviewed
in [its audit](phase3_psl4_rank7_audit.md), now reduces the odd-q PSL4 upper
bound to six. The later [endpoint reductions](phase7_psl4.md) and
[zero-product classification](phase7_psl4_zero_product.md) exclude rank five
by common-form and invariant-subspace arguments, with independent internal
review and exact symbolic checks. The subsequent [rank-six proof](phase8_psl4_rank6.md)
completes the proposed maximum-rank-four argument, retaining published
rank-four existence, while publication priority remains unverified. It also
proves a bilinear-form alternative for finite irreducible projective string
actions in dimension four and odd characteristic. The new Lean
intertwiner-separation lemma checks one algebraic implication; the
Pauli-support and module-classification arguments remain written proofs.

The [linear/unitary corollary](phase9_linear_unitary.md) verifies the form
theorem's hypotheses for every odd-field group between PSL4 and PGL4, and
between PSU4 and PGU4. Both intervals have rank at most four; index-four
extensions have a cyclic quotient obstruction to involution generation.
The [explicit unitary matrix certificate](phase10_unitary_matrix_certificate.md)
now gives maximum rank four for PSU4(5), with all 256 subgroup intersections
checked. General unitary rank-four existence and field/graph extensions remain
incomplete here. An additional Lean certificate checks the actual
transvection-invariance matrix obstruction, with its projective-multiplier
reduction and full group theorem outside the formal scope.

The first [matched-proof measurement](phase9_L066_measurement.md) is now
available: 10,668/3,192, approximately 3.34, for the two exact commuting-pair
formulas outside degree six. It counts shared arguments once and retains
explicit common background. It does not measure the other two principal
results of that paper or the full literature corpus.

## Later extensions and a withdrawn completeness assumption

The [weighted-tree theorem](phase6_weighted_tree.md) extends the known
transposition-tree model to every truncation: omitted edges are contracted
and component sizes become weights. One derivation gives all residues and
exact primitivity, local two-transitivity, rank-two intersection and full
shadow-intersection tests. A new formal theorem ensures the bounded Boolean
shadow witnesses remain in a retained consecutive rank interval. The original
2003 full-paper comparison is still unavailable.

The [general panel enumeration](phase6_sporadic_theory.md) allows arbitrary
primitive panels and checks every necessary double coset. One implementation
exhausts J1, M11 and M12, with 127 independently recognized representatives.
Subgroup catalogue completeness remains a dependency, and source-specific
axioms and equivalence conventions are recorded separately. This does not
turn the unrelated M11 maximal-subgroup classification into a reduced paper.

The [explicit Suzuki example](phase6_suzuki_realization.md) changes an earlier
assumption: the printed L114/L110 rank-three candidate list is not exhaustive.
Matrices in Sz(2^15) give a firm, residually connected, flag-transitive RWPRI
geometry with subgroup intersections absent from that list. The immutable
phase-five notes still decide their specified printed shapes, but their
retained completeness assumption is superseded. A corrected exhaustive
classification and publication priority remain unresolved. The new formal
factorization theorem proves the common-coset-point implication; exact
matrix membership and classical subgroup maximality are separate inputs.

The [living paper map](../../PAPER_MAP.md) includes the later source intake
and supersedes this overview's earlier coverage totals. The
[measurement rules](../../MEASUREMENT.md) keep finite proof-length ratios
separate from proposed new results. The measured ratio above concerns only
its two-theorem subset; no corpus ratio or infinity marker is assigned.

The [next Suzuki extension](phase7_suzuki_descent.md) closes the rank-four
geometry gap and gives an unconditional family in every rank. Compatible
field cosets satisfy Helly by Lang–Steinberg descent; independent cyclic
coordinates attach the additional torus-normalizer type. One binary torus
aligns the finite subfields, and an elementary valuation argument supplies
all needed distinct prime factors. Classical descent and Suzuki structure
remain inputs; the result does not claim an exhaustive classification.

The [pure-subfield and mixed-center extension](phase8_suzuki_subfields.md)
recovers every canonical Construction 11 parameter and identifies its sharp
rank bound, including the omitted repeated-prime boundary. For Construction
10, the relevant overgroups form a lattice of scalar subspaces. Its
prescribed intersections have codimension greater than one, so every such
embedding fails RWPRI, although the bare intersection lattice exists.

The same [panel engine now covers M22 and M23](phase7_sporadic_theory.md),
with 360 exhausted stabilizer anchors and 105 independently recognized
witnesses. Both primary summary tables and the archived higher-rank lists
match exactly. These are stated census components; unavailable article
bodies prevent a whole-paper claim.

The [metacyclic cyclic-TPP theorem](phase7_cyclic_tpp.md) supplies a new
uniform structural class for the hypertope order bound, for all primes and
all orders. Its separate order-512 certificate extends the finite hypertope
range through order2^12. The unrestricted conjecture remains unresolved.

The [small-factor theorem](phase10_cyclic_tpp.md) proves the inequality for
every cyclic-TPP triple in a finite 2-group with a factor of order at most
four. Equality in an elementary cyclic-subgroup bound forces an involutory
swap of a marked isobicyclic pair; the retained classification then gives a
central-involution obstruction. Consequently the hypertope order conjecture
holds whenever a distinguished pair product has order at most eight, at any
ambient order. Larger-factor cases remain unresolved.

The [two-coordinate Suzuki reduction](phase10_suzuki_marked_fields.md)
recovers the full rank/existence theorem restated from L085 (2006) and both
principal counting theorems of L074 (2010). Generation is exactly the joint
field-of-definition condition; Frobenius and duality give one Möbius sum.
Classical subgroup and centralizer facts remain inputs. The full L074
manuscript has been read; the original L085 body remains unavailable. Lean
certifies the abstract rank obstruction, and exact finite checks verify
field orbits and actual generating triples. No length ratio is assigned to
this reduction yet.

## Evidence and limits

Sixteen [Lean modules](formal/README.md) compile with the pinned toolchain and
without `sorry`. They include subgroup/partition reconstruction, intersection
transfer for coordinate kernels, the exact Suzuki closing-word equivalence, and a local string-intersection obstruction.
They do not formalize the entire
literature reduction, affine presentation calculation, character bounds or
finite subgroup catalogues.

The [matrix check](torsor_matrix_check.json) verifies all 900 ordered subgroup
pairs in S4, plus counterexamples detecting two insufficient replacements:
ordinary rational-module equivalence loses the permutation action, and C-group
IP alone does not imply the coset Helly condition.

The construction, incidence and classification notes link each exact script,
saved output and source version. The [verification manifest](torsor_verification_manifest.json)
records the earlier artifacts and their nine historical Lean reports. The
public snapshot checker additionally covers the six later modules and their
successful reports. Finite examples support uniform proofs; they are
not described as proofs of infinite parameter ranges.

For the public distribution, run `python3 scripts/verify_snapshot.py` from
the repository root. It verifies the published bytes and the saved formal
source hashes. The historical archive verifier also expects excluded local
source and dependency files. The individual notes give mathematical checks;
use the scratch-run instructions in [REPRODUCING.md](../../REPRODUCING.md).

This phase updates the earlier [36-paper audit](compression_audit.md), which
is retained as a baseline with its narrower scope. The [research README](README.md)
separately records the proposed conjecture proofs and the significant questions
that remain unresolved.
