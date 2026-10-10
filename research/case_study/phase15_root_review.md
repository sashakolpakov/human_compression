# Phase-fifteen root review and fresh verification

10 October 2026. **PASS within the scopes recorded below.** These are
independent internal mathematical reviews and exact executions, not external
peer review or verified publication priority. Original proof files and earlier
frozen artifacts retain their bytes. The accompanying
[JSON record](phase15_root_review.json) binds the reviewed inputs and outputs.

## Canonical quotient in every class

Root read the complete [graded-support proof](phase15_graded_support.md)
and its [primary-source adapter](phase15_graded_support_scope.md). The proof
passes without using the earlier class-three or class-four restrictions.
Burnside gives independent marked generators in the abelianization. The
lower-central Lie algebra is generated in degree one, and every layer is
an F2-vector space. A deepest participating edge in a forest relation cuts
the support so that all cross brackets lie in the opposite pure-support
Lie subalgebra. Jacobi propagates that containment to all degrees.

Root checked the descending lifting step directly: from ab^-1=n_A n_B,
the identity n_A^-1 a=n_B b lies in the actual disjoint parabolics. The
two images in the next abelian layer therefore meet trivially. The precise
index and order equalities give an actual ordered product filling that
lower-central term. No subgroup normality, commutativity, general triple
factorization, or intermediate quotient intersection property is assumed.
Two original-group support intersections then kill the selected commutator,
contradicting the edge. Class-two collection and the explicit cocycle prove
the exact marked isomorphism and quotient IP.

The primary F013 manuscript's introductory statements and definitions
were rechecked: its Theorems 1.1 and 1.2 are both recovered, the second
using the retained standard marked-group/polytope-covering correspondence.
This is a replacement proof of an already stated theorem. The earlier
counterexamples to the specified auxiliary kernel assertions remain valid.
The forest extension's priority has not been established.

Root also read and passed the separate
[prime-order and excess corollaries](phase15_graded_support_corollaries.md).
The all-prime argument uses the same Lie and support steps. The ordered
edge-subgroup product is injective by leaf peeling in the original group.
The nilpotency-class and additive edge-order bounds follow from the exact
gamma3 kernel size. The path's numerical type bound overlaps a known
source inequality and is explicitly not claimed as new.

## Quotient diagnostics and partial Lean

Root freshly reran the class-four GAP/NQ checker. Its
[captured log](phase15_common_quotient_root.log) matches the original after
outer whitespace normalization. It checks universal collection in ranks
two through six, with 120 local z/t equations, 350 double commutators,
20 edge commutators, 62 fourth-power masks, 1,724 distributed double
commutators and 400 cut-correction equations. The rank-three diagnostic
examines all 207 normal subgroups of the computed universal group, including
174 derived kernels, 167 nondegenerate markings and 114 markings with IP;
10,688 actual subset intersections were checked. These finite diagnostics
are not premises of the all-class proof.

The standalone [permutation verifier](phase15_quotient_ip_verify.py) was
freshly executed. Its [root report](phase15_quotient_ip_root_verify.json)
matches the saved report exactly: order 256, lower-central orders
256,32,8,2,1, all 64 original intersections, and the exact enlarged
intersection in the gamma4 quotient. The gamma3 quotient has order 32 and
passes all 64 comparisons. This backend imports neither GAP nor a catalogue.

Root read the complete [GradedSupport Lean source](formal/GradedSupport.lean)
and freshly compiled its byte-identical public copy with the public runner.
The [fresh report](phase15_graded_support_public_compile.json) records Lean
4.32.2, all pinned dependency revisions and tracked-file cleanliness, exit
zero and no sorryAx. A first environment-only attempt pointed to an absent
dependency directory; the successful run used the existing pinned checkout.
The three theorems formalize image disjointness for a split kernel, binary
subgroup-product injectivity and finite exhaustion under an explicit
cardinality equality. They do not formalize graded Lie spanning, the index
calculation, descending induction or the entire forest theorem. All eighteen
previous saved Lean reports remain unchanged.

## Eight-result 2002 measurement

Root compared the complete primary manuscript with the
[compact replacement](phase15_N003_matched_proof.md), retaining the exact
finite-group and n>=7 scope of its eight numbered targets. The module
bound, forest reconstruction, parity kernel, counts, balanced-cut overgroups,
typed Helly argument and arbitrary-parabolic reconstruction are charged
proof steps. Whiston W1 and W2, including CFSG dependence, Cayley's count
and the general coset criteria are explicit common background.

The [independent mathematical audit](phase15_N003_matched_audit.md) and
[source-span audit](phase15_N003_measurement_scope_audit.md) both pass.
Root freshly ran the exported measurement script against the exact primary
PDF, regenerating the bound extraction with pypdf 6.13.0. Its
[public-run report](phase15_N003_public_measurement.json) differs from the
author report only in timestamp. A fresh execution of the independent
position-set/state-machine counter matches its saved report exactly in
[the root record](phase15_N003_root_scope_check.json).

The primary counts are 9,680 and 7,260 normalized non-whitespace characters:
4/3, a 25 percent reduction. Tokens give 2439/1675 and raw bytes 12462/8693.
All nine source intervals, eight replacement intervals, 23 physical-layout
exclusions, the common W2 recital exclusion and marginal allocations pass.
The first 127/38 measurement is unchanged. These are two separate conditional
description-length measurements, not a corpus ratio or shortest-proof claim.

## The second unitary family

Root read the complete generation, intersection, parameter, twisted-curve
and final sieve notes, and passed their written arguments. In generation,
the block kernel's derived subgroup removes the possible scalar first
blocks before perfection supplies an actual coordinate SU2. For IP,
only sign similitudes of the two forms are used; the regular relative form
places their exact common stabilizer in the appropriate symplectic torus.
The order-four scalar center is charged correctly. The direct rank-three
power calculations and recursive criterion complete the intersections.

The large middle rotation forces the full square field by the smaller-field
semisimple order bound. The sphere offers q+1 second-block choices, exceeding
the six composite-field or 26 prime-field exclusions in the stated range.
The norm curve has eight simple punctures, no rational boundary and genus
one outside characteristic three. The Lang character has local exponents
of absolute values 1 and q, so every nontrivial order, including even order,
ramifies. The rational characteristic-three component has four punctures
and exactly q+1 rational points. The retained trace/weight machinery yields
the stated 8sqrt(q) and 2sqrt(q) bounds. The primitive and core-sieve constants,
strict endpoint inequalities and three primorial bootstraps pass root review.

The [complete independent audit](phase15_unitary_independent_audit.md)
separately reviews every written step and the finite certificates. Root
freshly executed both independent standard-library checkers from their
public copies. The [sieve report](phase15_unitary_root_sieve_check.json)
matches its saved record exactly: all 40,389 fields, 80,778 factorizations
and all 1,699 exceptions. The
[polynomial report](phase15_unitary_root_witnesses_check.json) matches except
elapsed time: all 1,697 primitive norm witnesses, exact quartic roots and
orders, full square fields in the required range, and the three direct
q=19,23,43 parameter checks pass. These computations use no author code
or GAP finite-field backend.

Root also freshly ran the frozen q=11 GAP checker, with its source hash
checked before and after execution. The
[report](phase15_unitary_q11_root_check.json) and
[log](phase15_unitary_q11_root.log) confirm projective order
1,036,388,695,478,400, 15,984 isotropic planes, type {4,60,10}, all 16
subset groups and all 256 intersections. This reruns the author's checker;
it is not a separate subgroup-arithmetic implementation. The q=7 full
certificate and earlier first-congruence-class construction are retained.
The [symbolic root report](phase15_unitary_root_symbolic_check.json)
records a fresh execution of all 37 exact matrix identities in scratch.

Together these establish the proposed rank-four construction for every
q congruent to three modulo four, q>=7. With the earlier construction and
upper bound, maximum rank is four for every odd q>=5; published rank-three
existence gives rank set {3,4}. The published PSU4(3) nonexistence exception
is retained explicitly. The broader survey's field/graph extensions and
general index-two existence are not settled. No end-to-end unitary Lean
formalization, verified current priority or infinity marker is claimed.
