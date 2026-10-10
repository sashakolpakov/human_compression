# L068: Livingstone-graph constructions — fixed author target

**Status:** full primary body read; second main construction recovered literally; first main construction recovered only after an explicit repair. No unchanged whole-source principal credit is claimed.

Hartley, Hubard and Leemans, *Regular 4-polytopes from the Livingstone graph of Janko's first group*, Journal of Algebraic Combinatorics 35 (2012), 193–214, DOI 10.1007/s10801-011-0300-x. The exact 22-page local edition is `sources/catalogue_L068.pdf`, SHA256 `e40b3ee73dec3754248a7c9b659fc3015f8ee59c2b98ce46141baae8fe825ad9`. Pages 13 and 20 have additionally been inspected as page images to resolve the white/orange pentagon symbols in the incidence definitions.

## Principal contract

Recover both literal graph constructions, not merely the existence of abstract regular polytopes with the same group or Schläfli types:

1. Theorem 4.1: the explicitly defined incidence structure Q is the regular rank-four polytope of type {5,3,5}, with full type-preserving automorphism group J1, face counts 1463, 8778, 8778, 2926, and the printed flag-stabilizer lattice (Propositions 4.1–4.2 and Figure 9).
2. Proposition 5.1 and Theorem 5.1: the second explicitly defined incidence structure P is the regular rank-four polytope of type {5,6,5}, with full type-preserving automorphism group J1, face counts 1463, 8778, 8778, 266, and Figure 10's flag-stabilizer lattice.
3. Recover the finite auxiliary graph/subset properties actually used to define these two structures. In particular, verify the white/orange pentagons, the edge–Petersen correspondence, the two complementary pentagons in each source quadruple, and the vertex/5-set/6-set triples. Source Propositions 3.4–3.5 receive explicit proof/certificate rows, rather than disappearing into a claimed equality of abstract groups.

The introductory statement that exactly two regular J1 rank-four polytopes exist is attributed to prior classification. It is not a new theorem of this source and is not replaced by enumerating only the two constructions. Figure 11 is classical subgroup-lattice background, with its retained input to be stated. Theorem 2.1 is expressly borrowed from Aschbacher; the replacement may instead use the already proved U/C recognition theorems without claiming priority for the general correspondence.

## Intended reusable argument

Let G act transitively on each finite type set X_i, and let each literal binary incidence relation be G-invariant. Choose mutually incident objects x_i with stabilizers H_i. The map H_i g ↦ x_i^g identifies the coset type set with X_i. For i ≠ j the H_i-orbit of x_j consists of incident objects and has size [H_i : H_i ∩ H_j]. If this equals the *entire* literal neighbour count of x_i in X_j, then it is the entire neighbour set. Equivariance proves equality of the literal and coset incidence relations on every pair of objects. Thus the entire incidence structure, including all higher flags and residues, is identified with the existing marked coset geometry.

This proof uses a complete neighbour set, not a count sampled from a prescribed flag orbit. The source-specific exact computation will construct all finite objects from the graph and evaluate each of the six incidence predicates at one base object, after proving transitivity. The two sets of predicates differ in three places, so both require checking. The retained C certificate supplies the two markings, their full subgroup intersection property and typed Helly. It cannot substitute for these new geometric predicates.

This equivariant reconstruction is a standard orbit–stabilizer argument organized here as a reusable verification interface. No historical novelty is claimed. The genuinely additional work in this application is the exact source-object construction and its checked bridge to the retained markings.

## Proof and certificate limits

### Author outcome after the fixed contract was tested

The printed Q relation of types {2,3} omits the Proposition 3.5 induced-quadruple condition. Its complete neighbour set has 12 elements in stabilizer orbits of lengths 2 and 10; one extra pair-flag has no type-one extension. Thus the literal first main theorem cannot meet the fixed contract. Adding the explicit compatibility produces the intended {5,3,5} geometry. All six P predicates, the other five Q predicates, and the two intended stabilizer lattices pass the exact source-object bridge. Proposition 3.3 also has an auxiliary wording defect: the common distance-two set has 40 vertices; the 10-set requires the white-pentagon condition already in its preceding paragraph. These are source corrections, not silently weakened source targets. The independent enumeration reviewer gave a bounded visual wording/count check of the missing Q clause, not a full phase179 review.

The generic diagonal-orbit reconstruction and finite neighbour-cardinality criterion are now proved in `phase179_formal/EquivariantIncidence.lean`. The named graph, GAP data, source-specific computations and complete source polytope theorems remain outside this Lean component.

The finite work will be conditional on the named J1 permutation-group data and exact GAP group algorithms, with their hashes and versions recorded. The identification of that action with the classical Livingstone graph must be either explicitly retained or separately established; a matching vertex count is insufficient. There is no end-to-end Lean certificate at intake, and no open conjecture is being claimed solved. Source errors or notation ambiguities will be recorded explicitly rather than silently corrected to match a desired output.

All additions are private phase179 files. Frozen Modules C and D and their source contracts remain unchanged. Required new written proof, executable code and retained dependencies will be measured separately before admission; the 22-page source length is not by itself a matched numerator.
