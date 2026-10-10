# Lean certificates and their scope

These files compile with Lean 4.32.2 and mathlib revision
`905b95818eb32af7874a58b427f50c1711a5e96c`. Exact dependency revisions
are in [dependency_manifest.json](dependency_manifest.json).

[TriangularWordTermination.lean](TriangularWordTermination.lean) proves
well-foundedness of a recursive order on blocks of words, its compatibility
with contexts, and termination of triangular square/swap rewriting.
[LabelEightTermination.lean](LabelEightTermination.lean) applies that
theorem to the actual all-rank table and proves existence of sufficient
fuel for the implemented collector. The [scope](../phase172_termination_scope.md)
and [root review with fresh public build](../../../provenance/phase107_review.md)
cover eleven new printed declarations. Confluence, support transfer and
the full group construction remain separate formal obligations.

[LabelEightTriangular.lean](LabelEightTriangular.lean) proves all-rank
strict triangularity of the actual square and correction table, and
alphabet-range preservation for steps and finite rewrite chains. The
[scope and fresh build](../phase174_label_eight_scope.md) and
[independent reading review](../phase174_label_eight_independent_review.md)
cover all five declarations. This supplies local hypotheses for the
termination proof above; it does not assume or establish confluence.

[LabelEightAlphabet.lean](LabelEightAlphabet.lean) completes a three-module
proof of the finite rewrite lemma behind the uniform label-eight construction.
All 43,680 descending triples on its rank-fourteen alphabet have joining
rewrite paths; all eight local source words reduce to empty. Every
intermediate word remains in the finite alphabet. The [readable scope](../phase171_label_eight_scope_reader.md)
and [independent review/fresh build](../phase171_label_eight_formal_review.md)
state the exact proof and trust boundary. The kernel evaluates all cases
using ordinary `decide`. The remaining all-rank locality,
confluence and group construction are written proofs, not consequences
claimed formalized by these three files.

Four scoped components support the separately named equal-label question
track. [CharacteristicTwoTranslations](CharacteristicTwoTranslations.scope.md)
proves the full ambient quadratic power relation for every integer exponent.
[LabelFourRelations](LabelFourRelations.scope.md) proves the local relator
equivalence in both directions. [IntervalOverlapCancellation](IntervalOverlapCancellation.scope.md)
proves zero-sum weight cancellation on the derived interval-overlap forest;
[FinIntervalOverlapCancellation](FinIntervalOverlapCancellation.scope.md)
transports that theorem to actual finite marker sets. Complete independent
proof reviews and fresh compilations accompany all four. Retained
presentation/generation theorems and complete polytope conclusions remain
separate obligations.

[ParityMixTheorem.lean](ParityMixTheorem.lean) now proves the general
group consumer: the actual paired marking has full ambient and intrinsic
intersection property, generates its group, and consists of nonidentity
string involutions. Its twelve-module package derives the connected fibers,
component profiles and overlap character equations from the two-primary,
odd-adjacency, genuine-character and factor string/IP hypotheses. The
[complete scope](../phase146_parity_mix_scope.md) and
[independent review](../phase157_parity_mix_review.md) cover fifty new
printed declarations, with twenty-five reports from six retained modules.
All use standard axioms. The package is one construction theorem; finite
order formulas, concrete characters and the complete polytope application
remain outside its formal scope.

[SupportedKernelConsequences.lean](SupportedKernelConsequences.lean) proves
the order formula, local recognition, separator factorization and the
lower-central consequence from the actual supported-kernel hypotheses.
[SupportedKernelHelly.lean](SupportedKernelHelly.lean) proves typed-coset
Helly transfer and discharges its kernel profiles and lifting conditions
for the supported-kernel construction. Both allow nonabelian kernel factors.
Their [consequences scope](SupportedKernelConsequences.scope.md) and
[Helly scope](SupportedKernelHelly.scope.md) bind the complete independent
proof reviews and fresh compilations. Geometry recognition, source-specific
presentations and Boolean deletions remain separate formal tasks.

[SupportedKernelGeneration.lean](SupportedKernelGeneration.lean) proves
the structural part of U.SK: generation of the full simultaneous fiber
product, both directions of every actual parabolic kernel profile and
the complete intersection property. The kernel profile is derived from
the local construction hypotheses. Its [scope](SupportedKernelGeneration.scope.md)
and [independent review](../phase133_supported_kernel_review.md) distinguish
these ten declarations from the separate consequences and Helly modules
above and from application bindings still to be formalized. Nonabelian
kernels are allowed. The
[fresh public report](SupportedKernelGeneration.check.json) records only
standard axioms.

[CoprimePullback.lean](CoprimePullback.lean) proves complete generation of
a fiber product by a compatible subgroup with surjective projections and
coprime kernel cardinalities. Its paired-generator corollary proves the
projection-generation obligations explicitly. This classical argument
allows nonabelian kernels. The [scope](CoprimePullback.scope.md) and
[independent review](../phase126_coprime_pullback_review.md) distinguish
this full algebraic theorem from the still separate geometric applications.
All three declarations use only the standard recorded axioms.

[OddCoverSeparation.lean](OddCoverSeparation.lean) proves six general
kernel-divisibility, odd-degree and finite-maximality statements. A quotient
over the same base preserves odd covering degree and cannot factor onto
a double cover. The maximality theorem takes an explicit admissibility
predicate; polytopality and the cover/quotient correspondence are separate
inputs. The [scope](OddCoverSeparation.scope.md),
[independent review](../phase107_odd_cover_formal_review_audit.md) and
[fresh public admission](../phase108_odd_cover_formal_root_admission.md)
state exactly what the certificate covers. All six statements use only
the standard recorded axioms.

The presented-group pair is [Phase32VoltageTheory.lean](Phase32VoltageTheory.lean)
and [Phase32L003Infinitude.lean](Phase32L003Infinitude.lean). The first proves
that exact integer-voltage relators and a nonzero loop imply infinitude of
an actual PresentedGroup. The second instantiates that theorem with216
states and the exact ten source words. Its [scope](Phase32L003Infinitude.scope.md)
identifies the source bridge and all unformalized consequences. The final
axioms are propext, Classical.choice and Quot.sound; the finite data checks
use only propext. A [dedicated runner](../phase32_L003_formal_check.py) verifies
the pinned packages and builds missing PresentedGroup dependencies in a new
output overlay before compiling both modules. Use it when those dependency
objects are absent from the installed package cache.

[LiftCertificate.lean](LiftCertificate.lean) checks that an automorphism
inverting an element preserves any subgroup generated by a power of that
element; it uses this to transfer absence of simultaneous generator-reversing
automorphisms across a surjection with such a kernel. It also transfers a
trivial cyclic intersection when the projection is injective on the first
cyclic subgroup.

It additionally checks a general intersection-transport theorem: for any
group homomorphism, once two subgroup images have the desired intersection,
the only remaining obstruction is their common intersection with the kernel.
This statement assumes neither finiteness nor centrality nor surjectivity.

[FieldIntersection.lean](FieldIntersection.lean) checks the core of the
proposed proof of the 2017 Conjecture 6.2:

1. Subtracting the image of an identity under a field automorphism gives the
   product obstruction for two subfields.
2. A square root of a sum of two field components, each outside the other
   subfield, cannot belong to the additive sum of the subfields.
3. A determinant-one matrix over one subfield whose unipotent conjugate is
   over the other must be a signed unipotent over their intersection.
4. The entry equations for a matrix fixing the third generator and inverting
   the first force that matrix to be zero when the discriminant is nonzero;
   hence no invertible matrix can perform that conjugation.

The fixed-field properties of the automorphism are explicit hypotheses;
the paper proof supplies them using finite fields and Frobenius. The matrix
theorem takes the four conjugated entry conditions as hypotheses. The
finite-field instantiation, normalization identities, passage from SL to PSL,
and polytope correspondence are not formalized here. The central-lift
certificate likewise does not formalize the source group construction.
These are certificates for substantial proof components, not end-to-end
formalizations of the existence theorems.

[TransvectionIntersection.lean](TransvectionIntersection.lean) generalizes the
matrix intersection argument to every dimension and arbitrary subfields. It
proves an exact equivalence: a matrix over A has its displayed transvection
conjugate over B precisely when it lies over A ∩ B and commutes with the
elementary matrix, assuming the parameter lies outside A+B. The certificate
uses the expanded conjugation formula. Identifying that formula with finite
matrix multiplication and packaging the result as an SL or GL subgroup
intersection are mathematical corollaries, not additional hidden Lean results.

There are sixty-six certificates. To compile them on another machine, install Git,
Python 3.10 or newer, and Lean's `elan` toolchain manager, then run from the
repository root:

```sh
cd research/case_study/formal
lake exe cache get
python3 verify_lean.py --check-env
python3 verify_lean.py --all
```

The checked-in `lean-toolchain` selects Lean 4.32.2. `lakefile.lean` pins
mathlib and `lake-manifest.json` locks all transitive dependency revisions.
The first Lake command obtains missing dependency checkouts and their compiled
cache; it requires network access. Keep the supplied manifest when reproducing
these results. Running `lake update` is an intentional dependency update, not
part of this reproduction procedure. A plain `lake build` is an alternative
way to compile the sixty-six modules, but does not produce the runner's JSON reports.

For an existing built checkout of exactly these dependencies:

```sh
python3 verify_lean.py --all \
  --packages /path/to/project/.lake/packages \
  --lean /path/to/lean
```

`--packages` overrides `MATH_COMPRESSION_PACKAGES`; absent either, the runner
uses this directory's `.lake/packages`. `--lean` overrides
`MATH_COMPRESSION_LEAN`; otherwise it uses `lean` on `PATH`. The runner checks
the compiler version, each recorded dependency's Git revision, and absence of
tracked changes. Compiled dependency files remain trusted build inputs; these
checks do not independently rebuild or authenticate the dependency cache.
Unrelated inherited `LEAN_PATH` entries are not used.

Fresh compiled files and hash-bearing JSON reports go to `.verification/`.
Use `--output-dir PATH` to choose another directory. Historical reports beside
the source are preserved. A single certificate can be selected, for example
`python3 verify_lean.py TransvectionIntersection.lean`; local prerequisites
are compiled automatically. `--timeout SECONDS` changes the default 120-second
limit per certificate. `--check-env` checks the environment without compiling.

To inspect the saved results without installing Lean:

```sh
python3 verify_lean.py --check-saved
```

This checks that all sixty-six source hashes match the historical successful reports
and that those reports contain no `sorryAx` dependency. It does **not** execute
Lean or verify a proof anew. Sixty-two saved runs use only a subset of the standard axioms
`propext`, `Classical.choice`, and `Quot.sound`. The transfer supplement also
prints four `native_decide` evaluation axioms and trusts the compiler/interpreter
for its four arithmetic claims. Its dimensions assertion is kernel checked. The detailed boundaries below
are part of each certificate's claim; none certifies the entire research corpus.

Saved reports: [lift](LiftCertificate.check.json),
[field intersection](FieldIntersection.check.json),
[arbitrary-dimensional intersection](TransvectionIntersection.check.json),
[connectivity from generating moves](ResidueConnectivity.check.json),
[chamber orbit criterion](ChamberOrbit.check.json),
[torsor partitions](TorsorPartitions.check.json),
[coordinate kernel transport](CoordinateKernels.check.json),
[Suzuki pentagon word](SuzukiPentagons.check.json),
[local string intersection obstruction](StringIntersection.check.json),
[Boolean shadow witnesses](BooleanShadow.check.json),
[consecutive-rank witnesses](ConsecutiveShadow.check.json),
[rank-three factorization](RankThreeFactorization.check.json),
[all-rank coset coordinates](CosetCoordinates.check.json),
[intertwiner separation](IntertwinerSeparation.check.json),
[transvection-invariant forms](TransvectionForms.check.json),
[involution-centralizer rank obstruction](InvolutionCentralizers.check.json),
[binary Frattini actions](BinaryFrattiniActions.check.json), and
[marked square descent](MarkedSquareDescent.check.json).

[BinaryFrattiniActions.lean](BinaryFrattiniActions.lean) proves the exact
four-case classification of the commuting binary actions satisfying the
three square-extension equations. Its six theorems include the converse,
nonvacuous coordinate support, and preservation of binary addition. The
finite decision proofs are checked by the Lean kernel. The
[scope note](BinaryFrattiniActions.scope.md) separates this complete finite
lemma from the written minimum-counterexample and central-element arguments
needed for the cyclic-subgroup inequality. The public report records a fresh
compilation; the sixteen older saved reports retain their original bytes.

[ResidueConnectivity.lean](ResidueConnectivity.lean) proves that a transitive
group action connects a relation whenever a generating set moves each point
within its undirected reachability class. Neither finiteness nor a free action
is required. The Hermitian-unital proof supplies the norm-shell identification,
transitive SU(2,q) action and generating root groups in ordinary mathematics;
those geometric identifications are not part of this Lean certificate.

[ChamberOrbit.lean](ChamberOrbit.lean) checks that an adjacency-closed group
orbit in a connected chamber set contains every chamber. It further derives
orbit closure from equivariance and unique base panel mates supplied by group
elements. The standard coset-geometry hypotheses, and the implication from
residual connectedness to chamber connectedness used for the 2016 questions,
are established in the written proof rather than in this formalization.

[TorsorPartitions.lean](TorsorPartitions.lean) proves the exact correspondence
between subgroups and left-translation-invariant equivalence relations on a
group torsor. It checks reconstruction in both directions, the zero-one
Hadamard intersection identity, and equivalence of subgroup intersection
identities with the partition identities. Ordinary matrix-product counts,
matrix ranks and the geometric Helly criterion are outside this certificate.

[CoordinateKernels.lean](CoordinateKernels.lean) proves that subgroups of a
product supported on coordinates whose prescribed vertex sets lie in I obey
the intersection law for I and J. Combined with `LiftCertificate`, it proves
the complete abstract transport implication: once a cover's kernel has that
coordinate-membership description and its image diagram has IP, its subgroup
diagram has IP. The edge-inflation construction must supply this explicit
kernel description; its construction, orders and coset Helly argument are
written proofs. The runner compiles `LiftCertificate.lean` first automatically.

[SuzukiPentagons.lean](SuzukiPentagons.lean) checks all three forced matrix
entries of a five-step Suzuki coset walk and proves the exact membership
equivalence: the word belongs to the displayed subgroup ZT precisely when
its four parameters are `(a,a⁻¹,a,a⁻¹)` with a nonzero. This includes the
converse through a full sixteen-entry matrix identity and its torus
factorization. The field is any characteristic-two field with a field
automorphism θ satisfying θ²(x)=x². The certificate also checks the entries
excluding triangles and nonbacktracking four-step returns. Its predicate
`BorelPart` denotes ZT, not the larger Borel subgroup UT. The finite-field
instantiation, exact source graph identification, and correspondence of
closing words with pentagons are proved in [the written argument](../suzuki_cycle_proof.md);
the graph theorem is not yet formalized end to end.

[StringIntersection.lean](StringIntersection.lean) proves a local obstruction
used in the written rank-eight exclusion: if involutions a,c commute, their
product commutes with b, and the adjacent parabolics intersect only in 1,b,
then a and b commute. The intersection hypothesis is supplied explicitly.
The Pauli representation argument and the resulting PSL4 rank bound are
written proofs, outside this certificate.

[BooleanShadow.lean](BooleanShadow.lean) proves the exact interval and
singleton descriptions of common shadows of arbitrary finite families of
subsets. It then proves that every nonempty shadow at a proper rank has a
witness of at most two nonempty proper subsets: a chain incident with the
whole query family and having exactly the same shadow. The
[scope note](BooleanShadow.scope.md) distinguishes this universal theorem
from the written tree identification, claw obstruction and residue-join
arguments used in the 2005 geometric characterization.

[ConsecutiveShadow.lean](ConsecutiveShadow.lean) proves that a witness of at
most two vertices still exists when only a consecutive interval of proper
Boolean ranks is retained. Every witness belongs to those retained ranks;
the theorem applies to arbitrary finite query families in the interval.
It imports BooleanShadow, which the runner compiles first. The
[scope note](ConsecutiveShadow.scope.md) separates this formal theorem from
the weighted-tree realization, branching obstruction and residue arguments.

[RankThreeFactorization.lean](RankThreeFactorization.lean) proves a group
Helly theorem: if one parabolic is the product of its intersections with
the other two, then any cosets of those two meeting its coset have a common
point there. It has no finiteness assumption. This provides the formal
common-point implication for the separate Suzuki example; the matrices,
factorization hypothesis and primitivity remain external to this certificate.
See its [scope note](RankThreeFactorization.scope.md).

[CosetCoordinates.lean](CosetCoordinates.lean) extends the common-point
argument to any family of cosets. If a subgroup covers every tuple of coset
coordinates, all cosets meeting its coset have a common point there. The
converse is proved as well. Neither normality nor finiteness is assumed.
The [scope note](CosetCoordinates.scope.md) separates this formal attachment
lemma from the written Chinese-remainder and Suzuki descent instantiations.

[IntertwinerSeparation.lean](IntertwinerSeparation.lean) proves additive
commutator transport across an intertwiner. If the left pair commutes and
the right additive commutator has a right inverse, the intertwiner is zero.
Both theorems are axiom-free as reported by Lean. The
[scope note](IntertwinerSeparation.scope.md) separates this ring lemma from
the written endpoint normal forms and their complete case coverage.

[TransvectionForms.lean](TransvectionForms.lean) proves that exact invariance
under all elementary-transvection congruences forces a bilinear-form matrix
to vanish when a third coordinate is available. It verifies actual matrix
products and transposes over any ring, with a four-dimensional instance.
The [scope note](TransvectionForms.scope.md) separates this certificate from
the written projective-multiplier reduction and complete group rank theorem.

The involution-centralizer certificate proves an abstract rank bound: a center-free group generated by nonidentity involutions in a string has rank at most three if any two involutions commuting with a third nonidentity involution commute with each other. It formalizes generation via subgroup closure. Verification of this centralizer condition for Suzuki groups, and Suzuki existence results, remain outside this certificate.

[MarkedSquareDescent.lean](MarkedSquareDescent.lean) adds the exact commuting
marked-action classification and the final fixed-coordinate transport
obstruction. Its finite decisions are checked by the kernel; the abstract
transport lemma has no axioms. The [scope note](MarkedSquareDescent.scope.md)
separates those components from the written group and hypertope proofs.
The [fresh public-run reports](../../../provenance/phase14_review.md) include
both this module and its binary-action dependency. All seventeen earlier
saved reports retain their original bytes.

[GradedSupport.lean](GradedSupport.lean) proves disjointness of subgroup
images when a homomorphism kernel factors through the two original
disjoint subgroups, injectivity of their ordered product, and finite
product exhaustion from a stated cardinality equality. Its
[scope note](GradedSupport.scope.md) distinguishes these kernel-checked
steps from the written Lie-algebra spanning argument, quotient-index
calculation, descending induction and complete forest theorem. This is
the nineteenth partial certificate; all earlier saved reports are preserved.

The twentieth module, [BooleanRetractions.lean](BooleanRetractions.lean),
proves intersection of endomorphism images from the Boolean composition
law and the four-marker centralization identity used in the complete
fiber-product presentation. Its [scope note](BooleanRetractions.scope.md)
separates these two formal implications from the toroidal lattice,
finite-order and geometric arguments. The public runner freshly compiled
it with the pinned dependencies, preserving all earlier saved reports.

[PrincipalKernelIntersections.lean](PrincipalKernelIntersections.lean) proves
the full intersection property for a monotone family of subgroups when
their images have exact intersections and the possible kernel involution
belongs to a subgroup precisely when its index set contains a fixed
support. Its more general first lemma corrects a common lift by a kernel
element. This proves a reusable implication in the first-excess census;
the actual seed extensions, kernel-membership calculation, completeness
and 5d−10 count remain written proofs. The [scope](PrincipalKernelIntersections.scope.md)
and [saved report](PrincipalKernelIntersections.check.json) specify that
boundary. The new [fresh public compilation](../../../provenance/phase17_kernel_public_compile.json)
checks the exported source independently of its historical report.

[NestedKernelIntersections.lean](NestedKernelIntersections.lean) extends
the kernel adapter to nested supports. An exact K/L/1 parabolic kernel
profile, with L≤K and its smaller support contained in its larger support,
has exact meets. Together with exact image intersections and monotonicity,
this gives actual IP. A second theorem allows arbitrary chains of supports.
The [scope note](NestedKernelIntersections.scope.md) makes the actual kernel
profile an explicit hypothesis: this certificate does not construct the
noncentral seeds or prove the excess-two classification. A
[fresh compilation](../../../provenance/phase19_nested_kernel_public_compile.json)
checks the exported module and its unchanged principal-kernel dependency;
all twenty-one earlier sources and historical reports retain their bytes.


[Phase23TransferAnnihilator.lean](Phase23TransferAnnihilator.lean) embeds all
706 initial rows and 1,522 edges of the saved 708-state integer transfer graph.
It verifies complete 2,832-coordinate identities, including
`delta^3(v7) = 125*e`, `T(e) = e`, `delta^4(v7) = 0`, and the Newton
coefficients `[2499, 1780, 715, 125]`. These four checks use native evaluation;
the [scope note](Phase23TransferAnnihilator.scope.md) and
[saved report](Phase23TransferAnnihilator.check.json) explicitly name the four
generated evaluation axioms. This has a stronger compiler trust requirement
than the preceding certificates. The [fresh public compilation](../../../provenance/phase24_transfer_public_compile.json)
rechecks the unchanged source and pinned dependencies. The general binomial
argument and the group-to-graph completeness theorem remain outside Lean.


## Endpoint changes and fixed overlaps

[EndpointDoublingIntersections.lean](EndpointDoublingIntersections.lean) proves
that if an automorphism fixes the overlap of a subgroup and its image
pointwise, that overlap determines every mixed intersection of their
subgroups. It also identifies the expected common marked subgroup from
its two restrictions. The [scope](EndpointDoublingIntersections.scope.md)
excludes the remaining C-group cases, odd-order generation, typed Helly
and the finite Janko-group recognition. Fresh compilation prints only
`propext` and `Quot.sound`; no native-evaluation axiom is used.


## The two-coset obstruction

[TwoCosetIntersection.lean](TwoCosetIntersection.lean) proves that an
intermediate subgroup in a two-coset interval equals its lower endpoint
exactly when containing the chosen representative adds nothing. The
intersection form supplies both directions of the endpoint criterion's
support obstruction; a third lemma transports any excess element to
that representative. All three theorems allow arbitrary groups and
print only `propext` and `Quot.sound`. The
[scope note](TwoCosetIntersection.scope.md) leaves the actual marked
subgroup definitions, two-coset covering hypothesis, all-subset assembly
and geometric recognition to the written argument.

## Common fibers and monodromy

[Phase29CosetMonodromy.lean](Phase29CosetMonodromy.lean) proves that a
nonempty intersection of left cosets is a coset of the subgroup intersection.
For H contained in that intersection, the common fiber is one H-class
exactly when H is the whole intersection. A further lemma supplies an
explicit pair in different classes from any excess element. The five
theorems allow arbitrary groups and indexed families, without normality.
Their printed axioms are standard: `propext`, with `Classical.choice`
and `Quot.sound` in four of them; no native evaluation is used.

The [scope](Phase29CosetMonodromy.scope.md) leaves graph covers, walk lifting,
the identification of monodromy classes with connected components, typed
Helly and the full incidence theorem to the written argument. The
[fresh public compile](../../../provenance/phase30_monodromy_compile.json)
uses the unchanged source and pinned dependencies. Use the public scratch
runner in [REPRODUCING.md](../../../REPRODUCING.md); the frozen scope note's
private-workspace invocation records its original development environment.


[Phase30AffineData.lean](Phase30AffineData.lean) checks six literal finite-data
predicates for the affine regular counterexample: shapes and distinct columns,
720 block memberships, 60 exact span intersections, and all 24 odd relations
and span sizes. The [scope](Phase30AffineData.scope.md) excludes seed geometry,
code generation/invariance, quotient interpretation and the affine theorem.
The [transcription adapter](../phase30_affine_formal_data_check.py) binds its
four arrays to the separately frozen report. A fresh public-run compile passed:
five theorem axiom lists contain only `propext`, one contains no axioms, and
none uses native evaluation. Historical compile reports retain their bytes.


[ParabolicQuotientTransport.lean](ParabolicQuotientTransport.lean) proves that
injectivity on each parabolic and exact image intersections lift typed coset
Helly, and that injectivity on maximal marked parabolics lifts full subgroup
IP. The combined theorem allows arbitrary groups and type sets. It assumes
the stated image properties; it does not formalize the particular finite
census or toroidal source identification. Its [scope](ParabolicQuotientTransport.scope.md)
records the exact assumptions and standard axioms.


[OneExceptionalParabolic.lean](OneExceptionalParabolic.lean) extends quotient
transport to allow one noninjective maximal parabolic. It proves full marked
IP and arbitrary typed coset Helly under exact image hypotheses, for arbitrary
groups and type sets. See its [scope](OneExceptionalParabolic.scope.md).
The source imports the unchanged earlier transport module, which the runner
compiles first. Particular presentations and geometric adapters are not encoded.


[SplitLatticeReduction.lean](SplitLatticeReduction.lean) proves the generic
all-modulus divisibility criterion for an additive map with additive left
inverse, and checks the literal six-coordinate matrix inverse. Its
[scope](SplitLatticeReduction.scope.md) excludes the full Schreier census
and geometric adapter. The finite inverse is kernel-checked, with no
native-evaluation axiom.


[CompactAffineData.lean](CompactAffineData.lean) checks four literal
homogeneous integer matrices, the nine fixed source relators and the local
and basis translation words. All four theorem blocks use kernel evaluation
and only standard axioms. Its [scope](CompactAffineData.scope.md) leaves
finite closure, lattice spanning, source identification and geometry to the
separate exact certificates and written proof.


[FibonacciModulus.lean](FibonacciModulus.lean) proves the Fibonacci matrix
power formula over every semiring, and the exact first scalar power modulo
F_s for every s>=3. The [scope](FibonacciModulus.scope.md) leaves the tensor
bridge, invertibility, local groups and geometry to the separate arguments.
No finite sample is used to prove the uniform arithmetic statements.


[ParabolicProductComparison.lean](ParabolicProductComparison.lean) proves
typed coset Helly in both directions from injectivity on protected subgroup
products and exact exceptional membership. It covers arbitrary groups and
type sets, with no global surjectivity assumption. Its [scope](ParabolicProductComparison.scope.md)
separates the formal Helly theorem from the written full marked-IP and
geometric adapters. The public runner freshly compiled its two transitive
local dependencies and the new module; only standard axioms occur.


[ParabolicMarkedComparison.lean](ParabolicMarkedComparison.lean) completes the
full marked-IP equivalence under the same hypotheses and proves the exact
source/image marking bridge. Its [scope](ParabolicMarkedComparison.scope.md)
covers both IP and typed Helly, even for infinite groups and type sets.
All four local modules passed a fresh public compilation with standard axioms.
The concrete arithmetic hypotheses and geometric adapters remain separate.


## Uniform triangle quotients of the two universal presentations

[TriangleWreathQuotient.lean](TriangleWreathQuotient.lean) defines the exact
six-relator triangle group and ten-relator rotational source, checks the
marked row-wreath homomorphism and constructs a subgroup surjecting onto
the triangle group. [Its scope](TriangleWreathQuotient.scope.md) records
the literal source convention. [TriangleWreathInvolutory.lean](TriangleWreathInvolutory.lean)
adds the explicit reversing involution, all fourteen full-group relations
and a direct subgroup surjection for that presentation; [its scope](TriangleWreathInvolutory.scope.md)
does not assume the separate split-extension identification.

Both transfer lemmas require triangle-group infinitude as an explicit hypothesis.
The reflection module below proves that hypothesis uniformly. The earlier
[root review](../phase40_triangle_quotients_root_audit.md) records fresh public
builds and all eight standard-axiom audits for the transfer lemmas.

The general runner now builds absent imported mathlib objects in its output
overlay, without changing installed package sources or object files. Existing
compiled dependencies remain trusted inputs. Missing-object builds are
recorded separately in `dependency_builds.json`.

## Full infinitude for every parameter at least six

[TriangleReflection.lean](TriangleReflection.lean) constructs the explicit real
reflection representation of the exact triangle presentation. A surjective
coordinate change proves the finite-order parameter relation. Expanding orbits
for parameters greater than six and an explicit unipotent orbit at six prove
the triangle group infinite. The two frozen subgroup-surjection modules then
give infinitude of the exact ten-relator and fourteen-relator source groups.

The final three infinitude statements assume only a natural parameter at least
six. Their [scope](TriangleReflection.scope.md), [independent full review and replay](../phase42_triangle_spectral_audit.md)
and [root source review and fresh public build](../phase42_triangle_spectral_root_audit.json)
record the exact interfaces. All twelve central declarations across the three
modules use only the standard three axioms. The geometric universal-object
identification, finite small-parameter baseline and historical priority remain
outside this formal claim.

## Exact quotient intersections

[QuotientIntersectionCriterion.lean](QuotientIntersectionCriterion.lean) proves
that a homomorphism preserves an intersection of two subgroup images exactly
when its kernel meets their subset product in the product of the restricted
kernels. Actual quotients and the locally injective defect criterion are
included. No finiteness, centrality or surjectivity is assumed. The complete
[scope](QuotientIntersectionCriterion.scope.md), [root review](../phase53_cover_kernel_root_audit.md)
and [fresh public build](QuotientIntersectionCriterion.check.json) bind all four
declarations. Geometry and cover-classification consequences remain separate.

## Separating marked covers by kernel characters

[CoverCharacterSeparation.lean](CoverCharacterSeparation.lean) proves that
inversion on a non-self-inverse kernel element is incompatible with a
marked isomorphism to a cover whose corresponding generator fixes the kernel.
The odd-prime-order specialization is included. The [scope](CoverCharacterSeparation.scope.md)
and [fresh build](CoverCharacterSeparation.check.json) make the boundary explicit:
family construction, kernel orders, action tables and geometry remain written inputs.
The [independent semantic review](../phase69_cover_family_interfaces_recent_audit.md)
and [root build admission](../phase68_cover_character_root_audit.md) record
the exact family interface and two fresh successful compiler runs.

## Noncommutative odd-kernel obstruction

[OddKernelWord.lean](OddKernelWord.lean) proves that 35 literal cell equations
in an arbitrary group force a distinguished word to square to one. A second
theorem proves that the two distinguished entries coincide in a finite
group of odd order. The [scope](OddKernelWord.scope.md),
[saved fresh build](OddKernelWord.check.json) and
[independent review](../phase86_nonabelian_cover_recent_audit.md) bind the
exact statements. The fixed permutation orbit, Sylow normalization and
source-family geometry remain separately checked inputs.
