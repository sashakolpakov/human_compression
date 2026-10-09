# Torsor and matrix compression: demonstrated scope

9 October 2026. The mathematical proposal is a finite group torsor with a
marked family of invariant partitions. An intrinsic version is the split
algebra Q^X, its group action, and marked invariant subalgebras: algebra
automorphisms are exactly permutations of the primitive idempotents. The
[core note](torsor_matrix_theory.md) proves this description and explains
which geometric constraints it solves. These are internally reviewed proof
drafts and exact computations, not externally reviewed publications.

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
| L066, *On pairs of commuting involutions in Sym(n) and Alt(n)*, all four principal results | Five orbit multiplicities for C2²-actions, two rational generating functions, one degree-six orbit certificate | All principal counts and both S6/A6 polyhedron conclusions recovered; standard automorphism theorems remain inputs |
| L032, *On regular polytopes of 2-power order*, Theorem 1.2 | Explicit square-grid seed plus independent dihedral factors | Whole principal all-rank existence theorem; no classification of every group |
| L030, *An infinite family of locally X graphs based on incidence geometries*, principal construction and parameters | The single tensor relation K_r tensor KG(N,k), replacement distances and a spectral automorphism argument | Construction, residues, diagram and full graph automorphism group recovered; two source displays corrected |
| L008, *Testing chirality on hypertopes*, Theorem 1.1 | Double-coset extension fiber with two points, then a uniform residue argument | Principal criterion recovered, retaining the standard marked-inversion correspondence |
| L034, *Existence of regular 3-hypertopes with 2^n chambers*, Theorem 3.2 and parts of Conjecture 3.3 | Same grid/dihedral construction; presentation comparison; cyclic triple-product lower bound | Presented construction recovered; alternate printed quotient display not separately verified. Bound proved for minimum pair order ≤4 and several uniform derived-subgroup classes; full bound remains |
| L035, *2-groups behaving as automorphism groups of regular 3-polytopes*, Theorems 1.2 and 1.3 | Grid construction, bounded cyclic-core quotients, eight binary extension models | Both principal theorems recovered, including completeness of all eight families; retains Lucchini's theorem and one exhaustive order-256 SmallGroups census |
| L025, Suzuki graph Conjecture 3.2 | Three zero matrix entries solve a four-parameter coset-walk word | Proposed all-q proof of exactly q−1 pentagons per edge; full matrix-membership equivalence Lean checked; graph/source correspondence is a written proof |
| L012, *Regular 3-polytopes of order 2^n p*, Theorem 5.1 and Corollary 5.2 | Three affine transformations, one index-48 presentation, three invariant lattices | Actual three families and every order 3·2^n for n≥5 recovered; other classification/nonexistence results remain |
| J2 and Sz(8), published rank-two censuses | One normalizer-orbit algorithm on subgroup inclusions | All eight J2 rank-two objects and all 29 Sz(8) objects reproduced; complete GAP subgroup catalogues are explicit inputs; higher ranks and all-q Suzuki classification remain |
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
bound to six. It does not settle ranks five or six or establish publication
priority. Its Pauli-support argument remains a written proof.

## Evidence and limits

Nine [Lean modules](formal/README.md) compile with the pinned toolchain and
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
records the reviewed artifacts and checks that all nine Lean reports match
their current source hashes. Finite examples support uniform proofs; they are
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
