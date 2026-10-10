# Independent review of the mixed-prime polyhedron application

This review concerns the complete principal-result contract for L012,
Hou–Feng–Leemans, *Regular 3-polytopes of order* $2^n p$, in
arXiv:2001.02945v2 (14 July 2024), seventeen pages. It reviews the new
affine umbrella and its complete application, not a collection of sampled
finite cases. Final frozen bindings and the verdict are recorded below.

## Source reading and scope

I read the entire bound primary, both complete replacement manuscripts,
the source ledger and contract, all new mathematical programs and all
three new Lean declarations. I checked the retained cubic component and
the supported-extension interface used by this application. The primary
PDF is bound by SHA256
`89829c32c489b49840eb5c7505ecf98aefd565c8ad500ccb1a966c265b009efd`.
Physical pages 11–12 were additionally inspected as images to verify the
definitions and the literal sign in Lemma 4.5.

The principal contract comprises the full type restriction in Theorems
1.2/3.1, the exact odd-factor presentation in Theorem 4.1 and Corollary
4.2, the exact existence range in Theorem 1.3, all three literal cubic
families in Theorem 4.3 and Corollary 4.4, and all three literal families
in Theorem 5.1 and Corollary 5.2. The latter component is reused with its
complete proof and executable dependencies. The corrected extension
presentations close the auxiliary construction obligations for the
existence theorem.

This contract excludes the separate complete Table 1 census, the
ancillary assertion that there are exactly two order-384 seeds of the
specified type, the general classification problem, and the historical
survey. It is one distinct principal contract, not a whole-paper
replacement claim. There is no new open-question credit or compression
ratio. The principal results remain attributed to the original authors.

## Mathematical assessment

The type restriction follows from the dihedral quotient
$G/O_2(G)\cong D_{2p}$. The proof correctly uses solvability, a minimal
normal subgroup of order $p$, and its centralizer. It allows identities
among the three generating elements as required by the source's stronger
algebraic statement. It does not impose the narrower construction's
lower bounds on the exponents in the type restriction.

The all-odd-factor construction uses the exact square-group lattice
presentations from the retained umbrella and two supported cyclic
extensions. Both the quotient and reverse-order bounds are supplied.
The cases with the smallest lattice scale are included. The argument
establishes the literal source presentation, order, type, intersection
property and solvability, including odd factors larger than primes and
odd factors having a common divisor.

The affine umbrella separates three obligations: identifying the actual
abstract presentation kernel, identifying its integral translation
lattice, and comparing the affine lifts of common point-group elements.
The first obligation uses an exact presentation of the kernel, proved
abelian of rank three; its abelianization alone would not suffice. The
period sublattices are invariant, so adjoining the powers gives exactly
the indicated lattice quotient. The finite overlap calculation then
proves intersection for every period, not just tested periods.

For the new $\{6,4\}$ group the point quotient has order 48 and the
translation lattice has index four in $\mathbb Z^3$. The three period
lattices have relative indices 2, 4 and 8. Both adjacent subgroups are
faithful in the point quotient and its relevant intersection has order
two. For the retained $\{6,6\}$ group the translation lattice is
$2D_3$, of index 16, and the relative period indices are 4, 8 and 16.
The two extra elements of the point-group intersection have translation
differences excluded from every relevant period lattice. This supplies
the distinction which would be lost by using group orders alone.

The dihedral fiber-product extension proves generation, the cyclic
kernel, injectivity on the unchanged adjacent subgroup, and intersection.
Its exact presentation variant pays for each retained relator in the
product. The corrected source period presentations are identified with
these products; the exceptional excess-five family uses its actual
order-384 presentation. The excess-two constructions use the retained
square seed. The excess-three exclusion descends to order 384 using the
cyclic-core bound; injectivity on the other adjacent subgroup and the
quotient intersection property are established. The finite base search
exhausts the retained order-384 catalogue with complete conjugacy
reductions, rather than searching a selected list.

## Changes required before the author freeze

The first draft's raw left-prefix differences need not generate the
translation kernel as an abelian group. I supplied the involutory affine
counterexample with generators $(-I,e_1)$, $(-I,0)$ and coordinate swap
in dimension two. Its raw differences span $\mathbb Ze_1$, whereas its
translation kernel contains both coordinate directions. The final lemma
uses the normalized transitions
$\widehat{\bar s q}^{-1}s\widehat q$, with a complete telescoping
argument. Its separate invariant-lattice corollary justifies the
unchanged historical program: the $Q$-orbits of its raw differences
generate the kernel, its proposed $2D_3$ lattice is $Q$-invariant, and
the exhibited raw vectors span that lattice. This is an explicit proof
repair, not a claim that the original raw formula was sound.

I also required distinct marked generators and adjacent orders at least
three in the general affine intersection theorem. Without a
nondegeneracy hypothesis, three equal involutions satisfy the displayed
adjacent-intersection condition while failing the full intersection
property. The actual applications already satisfy the added hypotheses.
The elementary rank-three intersection proof is now included in full,
with its attribution, so it is not an unpaid external proof dependency.

I acquired and read the complete original article by Lucchini,
*On the order of transitive permutation groups with cyclic
point-stabilizer* (1998), printed pages 241–243. Its proposition gives
the required core bound directly. The bound archive PDF has two cover
pages and three article pages, SHA256
`2ca47ecb49e06640c10311bfd7752f609d3cf979a05ab7d8b4c6dfffff5cd8ec`.
Primary acquisition:
<http://www.bdim.eu/item?fmt=pdf&id=RLIN_1998_9_9_4_241_0>.
The final package retains this original theorem explicitly.

## The source correction and formal boundary

The first period equality in the first branch of the bound source's
Lemma 4.5 needs its right-hand exponent changed from $+2M$ to $-2M$.
The actual source words satisfy $x_1^a=y_1^{-1}$. Together with the
source's commutation relation and even $M$, the two positive signs force
$x^{4M}=1$. The source target is therefore lost for applicable parameters;
the literal $n=10,s=4$ presentation has order 1536 and rotation order
eight, while the corrected presentation has order 3072 and rotation
order sixteen. The uniform corrected construction, not this single
witness, establishes the surviving main existence theorem.

The three Lean declarations prove the actual source-word conjugacy, the
general equal-sign power collapse under the necessary commutation
hypothesis, and their composition for the literal source words. They
are substantive group identities with the stated hypotheses. They do
not formalize the positive affine recognition theorem, the complete
classification, Burnside's theorem, Lucchini's theorem, or SmallGroups
completeness. The correction is limited to the bound arXiv edition; the
journal display was not collated. No historical-priority claim for this
correction is made.

## Independent computational evidence

The independent affine program imports no author program. It constructs
the marked affine quotients using exact adjugate coordinates for each
period lattice, enumerates the actual groups and all eight distinguished
subgroups, and tests all 64 subset intersections. It tests all six
families at periods one, two and three: eighteen models. Collapsing the
$\{6,6\}$ translation lattice to the whole kernel gives the point
group of order 48 and fails intersection, providing a relevant negative
case. The orientation counterexample above is checked independently.

The independent GAP program transcribes the literal source Theorem 4.1
presentation for six parameter tuples. They give groups of orders
1120, 384, 640, 1920, 3840 and 864. For each it checks both adjacent orders,
all 64 intersections, all eight Boolean deletion homomorphisms and
solvability. These include both parity branches and the composite,
noncoprime pair of odd factors 9 and 3. These finite cases check the source-to-program
bridge; the written argument supplies all parameters.

The final review runner also performs the entire frozen author replay
with primary bindings, the full catalogue exclusion, both exact
presentation kernels, the restored assertion checks for the historical
Python program, and fresh compilation of all three Lean declarations.
Its controls include a collapsed affine translation, the incorrect
literal sign, a counterexample after removing commutation, a positive
catalogue search, and a corrupted legacy lattice assertion. Exact
versions and outputs are bound in the review manifest.

## Retained costs and admission boundary

Burnside's solvability theorem, Lucchini's original bound, the complete
SmallGroups 1.5.4 catalogue, exact GAP presentation algorithms and the
regular-polytope correspondence remain explicit retained inputs. The
full earlier Topic A umbrella and cubic proof component, their required
programs and the new umbrella/application remain chargeable in any
future topic measurement. The finite tests are neither a substitute for
those dependencies nor a measure of compression. No source-count total
is inferred from this local review.

## Final verdict and frozen binding

**Accepted for the exact principal contract above.** The final author
manifest is `phase250_manifest.json`, SHA256
`27f605517f1fec35aef62ec181229d5ed2b8f73aeda09f5cd0ccd9a1af44c62e`.
It binds 37 exports and 12 retained inputs. All 33 source dispositions
and 14 complete proof spans are accepted with their qualifications.
The fresh full author replay with primary verification passed, including
all 20,169 catalogue groups, both exact affine kernels, the literal and
corrected presentations, all controls and the three standard-axiom Lean
reports. The independent phase254 runner binds its further evidence.

I inspected every page of both final PDFs: the umbrella has five pages
and the application nine, including their references. The corrected
vector display and lattice table are legible without overlap. These
fourteen pages do not include the full retained umbrella and cubic
component; they are not a complete denominator for a compression rate.

No author correction remains requested. The pre-freeze changes described
above are part of the reviewed final version. Frozen previous components
remain unchanged. Root may admit one distinct principal contract after
its own publication checks; this review neither changes the registry nor
awards a new open-question solution.
