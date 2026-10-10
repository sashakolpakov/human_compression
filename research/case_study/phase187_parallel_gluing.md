# Parallel gluing and simultaneous matching

Working manuscript, phase187. This note gives an exact common-lift
criterion for parallel gluings, a counterexample to the pairwise
criterion in [BHP94, Lemma3.4], and its relation to the existing typed
coset Helly interface. It is a partial source contract. It does not
replace all of [BHP94], whose expansion theory and numerous examples
have additional obligations.

## 1. Source and construction

The retained source is F. Buekenhout, C. Huybrechts and A. Pasini,
*Parallelism in diagram geometry*, Bulletin of the Belgian Mathematical
Society–Simon Stevin 1(3) (1994), 355–397. The journal's primary PDF is
`sources/phase187_parallelism1994.pdf`; Section3 defines the construction
on pp.362–363, and Lemma3.4 is on p.365. Its exact text and property(O)
were checked in the original rendering.
[Primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BBMS/Bulletin/bul943/PASINI.PDF).

We retain the source's construction and its term *parallelism*. In a
geometry Γ with a distinguished point type0, a parallelism partitions
the objects of each other type into directions. Each direction has
exactly one representative through each point; representatives of
incident directions through a common point are incident. The direction
geometry Δ is isomorphic to each point residue. A parallel-preserving
automorphism therefore induces an automorphism of Δ.

Take n≥2 geometries Γ_j with parallelisms and direction geometries
Δ_j. Fix isomorphisms α_j:Δ_j→Δ to a common typed geometry. The
glued geometry Γ_α has a separate point type 0_j for each j. Its objects
of any other type are tuples (x_j), all of that type, satisfying

    α_j(dir(x_j)) = α_k(dir(x_k))  for every j,k.

Points of distinct point types are always incident. A point of type0_j
is incident with a tuple precisely when it is incident with the jth
coordinate. Two tuples are incident precisely when all their respective
coordinates are incident. This is exactly [BHP94, Section3.1].

The source's property(O) is: “distinct elements of the same type have
different 0-shadows.” We assume it for each Γ_j whenever discussing
all type-preserving isomorphisms of gluings. For parallel-preserving
glued isomorphisms, the common-lift criterion below does not need(O).

Let

    A_j = Aut(Γ_j, parallelism),
    ρ_j:A_j→Aut(Δ_j),  H_j=im(ρ_j),  K_j=ker(ρ_j),
    D=Aut(Δ).

Automorphisms throughout preserve types. The possibility of permuting
types is a separate quotient problem, as in the source's Section3.5.

## 2. The common-lift theorem

**Theorem 2.1.** Let α=(α_j) and β=(β_j) be two choices of matching
isomorphisms for the same family. Under(O),

    Γ_α ≅ Γ_β  iff  ⋂_j β_j H_j α_j^−1 is nonempty.                 (2.1)

Without(O), the right side is equivalent to the existence of a glued,
parallel-preserving isomorphism. Each set in the intersection is a
coset in the common automorphism group D.

**Proof.** A family φ_j∈A_j induces a glued isomorphism precisely when
its direction actions agree after matching:

    β_j ρ_j(φ_j) α_j^−1 = d  independently of j.                    (2.2)

In that event define the map on points by the separate φ_j and on a
tuple by applying φ_j to its jth coordinate. Equation(2.2) preserves
the matching equations. Local incidence preservation then preserves
all incidences, and the inverse family proves bijectivity. Conversely,
a glued isomorphism yields such a family and hence such a common d.
Every element of H_j lifts through ρ_j by its definition as the image,
so equation(2.2) is equivalent to (2.1).

For completeness, the reconstruction from an arbitrary isomorphism
under(O) is the retained argument of [BHP94, Lemma3.2 and Theorem3.3].
The 0_j-shadow of a tuple is precisely the point shadow of its jth
coordinate. Thus two tuples with an equal jth coordinate have images
with equal jth coordinates, by(O) in the target factor. If two tuples
have the same direction, replace one coordinate at a time to pass from
one to the other. Each step shares a coordinate because n≥2. Their
image directions consequently agree. This proves preservation of the
glued parallelism. A local object's image is then the corresponding
coordinate of the image of any tuple containing it; the shadow argument
makes this independent of the other coordinates. The inverse map gives
local bijectivity. To check incidence, extend a local incident pair to
a point, and in every other factor choose the unique representatives
of its two directions through an arbitrary point. The parallelism axiom
makes these representatives incident, so the local pair occurs in a
global incident pair. Incidence of the local image follows. The same
argument for the inverse gives a local isomorphism. These local maps
preserve directions and induce one common action on Δ. This proves
the asserted reconstruction and finishes the proof. ∎

Write P_j=α_j H_j α_j^−1. Inverting the cosets in (2.1) gives the
family of right cosets

    P_j (α_j β_j^−1).                                            (2.3)

**Corollary 2.2.** If (P_j) has typed coset Helly, the pairwise test in
[BHP94, Lemma3.4] is sufficient. For a fixed tuple α, sufficiency of
that test for every β and every subfamily of factors is equivalent to
typed coset Helly for (P_j).

**Proof.** For two indices the intersection in (2.1) is nonempty exactly
when

    α_j β_j^−1 β_k α_k^−1 ∈ P_j P_k.                             (2.4)

This follows by equating β_j h_j α_j^−1 and β_k h_k α_k^−1 and
rearranging. Inversion turns pairwise intersection of those sets into
pairwise intersection of the cosets(2.3). Typed coset Helly supplies a
common element, and Theorem2.1 applies. Conversely, varying β_j ranges
over all right cosets of P_j. Applying this observation to every
subfamily proves the converse. Subfamilies with at most one factor
already have a common element and need no gluing test. ∎

The last qualification matters: a test restricted to the full index
set alone is not automatically a theorem about all its subfamilies.
The reusable umbrella interface U.Helly supplies the all-subfamilies
version directly. Consequently the missing assumption is an existing
mathematical interface, rather than a separate assumption about each
particular drawing of a glued geometry. Intersection properties of
subgroups alone do not provide it.

## 3. Orbit classification and automorphisms

Choose one identification of each Δ_j with Δ. Matching data then form
the product of coset spaces ∏_j D/H_j, and D acts diagonally on the
left. Theorem2.1 identifies the type-preserving isomorphism classes of
gluings with the orbits of this action. In the case of two factors the
description reduces to H₁\D/H₂. This recovers the double-coset
classification under the stated shadow-separation assumption; for three
or more factors a single double-coset comparison does not replace the
whole simultaneous orbit problem.

The same argument describes the automorphism group without requiring
sections of any quotient map:

    Aut(Γ_α) ≅ { (g_j)∈∏_j A_j :
       α_j ρ_j(g_j) α_j^−1 is independent of j }.                 (3.1)

Under(O) this is the full type-preserving group. Without(O) it is the
parallel-preserving subgroup. Projection to the common direction action
gives the exact sequence

    1 → ∏_j K_j → Aut(Γ_α) → ⋂_j P_j → 1.                       (3.2)

Surjectivity holds because each element of the intersection has a lift
in each A_j independently. The kernel is the product of the kernels.
Formula(3.1), rather than a presumed splitting of (3.2), is the primary
group description. A semidirect product follows when compatible sections
of the relevant quotient maps are supplied.

The source's uniqueness criterion in Theorem3.5 survives the correction
to Lemma3.4. Here is a direct proof from the orbit description.

**Proposition 3.1.** The diagonal D-action on ∏_j D/P_j is transitive
if and only if

    D = (⋂_(j≠k) P_j) P_k  for every k.                          (3.3)

**Proof.** If the action is transitive, fix all coordinates except k
at their base cosets. An element carrying that base tuple to an arbitrary
kth coordinate must belong to every P_j with j≠k, proving (3.3).
Conversely induct on the number of factors. Condition(3.3) is inherited
when a factor is deleted, since deleting a subgroup enlarges the relevant
intersection. First move all but one coordinate to their base cosets by
induction. The remaining coordinate can be moved to its base coset by
the intersection of those stabilizers, by (3.3). This proves transitivity. ∎

This proof uses a common stabilizer for all previously fixed coordinates;
it does not replace it by unrelated pairwise choices. The construction,
the diagonal orbit method and the two-factor result remain attributed
to the earlier gluing theory. The correction concerns the unrestricted
pairwise criterion for three or more factors.

## 4. A three-factor counterexample satisfying(O)

Let the base point set be Ω=Z/8Z. The twelve lines are the blocks of
the following four parallel classes:

    P₀ = {01,23,45,67},
    P₁ = {12,34,56,70},
    P₂ = {0145,2367},
    P₃ = {1256,0347}.

Here a string lists the elements of a subset, not a cyclic interval.
Every class partitions Ω, and all twelve subsets are distinct. This is
a rank-two geometry with parallelism and property(O). It is firm: each
point is on four lines, and each line has two or four points. Its incidence
graph is connected because its two-point lines form the cycle C₈.

Every point permutation preserving the line family preserves cardinality
and hence preserves C₈. It therefore belongs to its dihedral automorphism
group of order16. Conversely the rotation x↦x+1 and reflection x↦−x
both preserve all twelve lines and all four parallel classes. Thus they
generate the full type-preserving automorphism group. Both interchange
P₀ with P₁ and P₂ with P₃. The induced group on the direction geometry
Δ, a four-element rank-one geometry, is therefore

    H={1,a},  a=(0 1)(2 3) ∈ D=Sym({0,1,2,3}).

Take three copies of this base geometry and the matching families

    α=(1,s,t),       β=(1,s,at),
    s=(1 2),        t=(1 3),

where products act from right to left. Set b=(0 2)(1 3). Direct
conjugation gives the three common-lift cosets

    β₀Hα₀^−1={1,a},
    β₁Hα₁^−1={1,b},
    β₂Hα₂^−1={a,b}.

Each pair has one element in common, and their total intersection is
empty. Hence all six ordered instances of the printed condition(2.4)
hold. The corrected criterion excludes an isomorphism.

There is an even simpler invariant proving that exclusion directly.
For a fixed common direction d, the number of tuple lines in Γ_α is
the product of the three numbers of lines in the matched classes. The
base class sizes are (4,4,2,2). Thus the two gluing families give

| Common direction | 0 | 1 | 2 | 3 | Total tuple lines |
|---|---:|---:|---:|---:|---:|
| α | 64 | 16 | 16 | 16 | 112 |
| β | 32 | 32 | 32 | 8 | 104 |

Each geometry has three point types of size8. Their total numbers of
objects are136 and128, so they cannot even be isomorphic by a map that
permutes types. This count follows from the literal source construction.

Both gluings are firm geometries and residually connected. Any flag of
point objects extends to a chamber by choosing a common direction and
the unique line of that direction through each specified point; unfilled
coordinates can then be chosen freely. A flag containing a tuple line
extends by taking points in its component blocks. Missing-line panels
have four completions, and missing-point panels have two or four.
For connectivity, two or more remaining point types form a complete
multipartite connected subgraph, to which every tuple line attaches.
If just one point type and the tuple-line type remain after fixing the
other points, uniqueness of parallels identifies the residue with the
connected base rank-two geometry. If a tuple line is fixed, its remaining
point types form a complete multipartite graph. These exhaust residues
of rank at least two.

The program `phase187_parallel_gluing_check.py` independently enumerates
all8! point permutations to recover the full base group, checks(O),
the partition axioms, all six printed product conditions, the common
lift obstruction, and both literal incidence structures. It enumerates
all typed flags, panels and residues of both gluings. Run with a fresh
output path:

```sh
python3 -O phase187_parallel_gluing_check.py \
  --output /private/tmp/phase187_parallel_gluing.json
```

It uses no saved geometric or group tables and no Python assertions.

The separate `phase187_formal/SimultaneousMatching.lean` contains twelve
checked declarations: the common-image/coherent-family equivalence,
the Klein four-group multiplication laws and subgroup closures, the
translated third coset, the three pairwise intersections, the absence
of a common element, and faithfulness of the regular permutation action.
It imports only the compiler's standard library. The observed axioms
are Classical.choice for simultaneous lifting and propext for the finite
contradiction proof; no sorry or additional axiom is used. These are
formal components, not a formalization of the geometric reconstruction
or the identification of the twelve-line base geometry's full group.

`phase187_run.py` runs the literal finite calculation, recompiles that
Lean source in a fresh directory, and applies three negative controls.
A globally compatible matching must fail the claimed obstruction;
duplicating a line shadow must fail(O); and replacing the third formal
coset by an identity-containing subgroup must stop the Lean proof from
compiling. The replay records exact source and compiler hashes and checks
that the sources remain unchanged during execution.

## 5. Source contract and remaining work

The positive contract currently covers the source's matching construction,
the reconstruction behind Lemma3.2 and Theorem3.3, a corrected Lemma3.4,
the diagonal-orbit and two-factor double-coset descriptions, the exact
fiber-product automorphism group, and the uniqueness criterion of
Theorem3.5. The construction and reconstruction are borrowed and credited;
the present contribution is the explicit missing common-intersection
condition, its precise connection to U.Helly, and the small geometric
counterexample.

This note does not claim the full source as replaced. In particular the
parallel-expansion theorem of Section4 has density and flat-intersection
hypotheses requiring a separate proof, while Sections5–7 contain many
individual geometric examples and group calculations. Their contracts
must be stated and recovered before any paper-level admission or matched
compression ratio. Nor is this a solution of an open conjecture. The
historical priority of the correction has not been investigated.
