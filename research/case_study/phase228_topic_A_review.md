# Independent review of Topic A and its first application

10 October 2026. **The two written mathematical papers and the declared
L032 principal contract are accepted. The planned multi-source topic and
its compression measurement remain incomplete.**

The exact intake-to-replacement statement is

\[
\text{L032, Theorem 1.2 and the attributed Proposition 2.2}
\quad\Longleftarrow\quad
U_A+\textit{Prescribed rank, type and two-power order}.
\]

Here \(U_A\) is the complete paper *Supported extensions and finite
two-group quotients*. This is one completed source-specific application,
not six newly completed papers or an additional principal-source credit.
L032 was already covered in the predecessor work.

## 1. Material read and exact source contract

I read both complete phase207 manuscripts, the complete mathematical body
of the eight-page Hou–Feng–Leemans author edition dated 8 November 2019,
the decomposition plan, provenance ledger and formal scope. I visually
checked the primary pages containing Theorem 1.2, Problem 1.1 and the
attribution of Proposition 2.2. The source PDF has SHA256
`3f670cf785ac3147c2b5ee501b595241a567910d8a94a096b26b78f8dcb76c66`.
All fifteen author exports and fourteen retained bindings are unchanged.

The source's main theorem asserts existence for every rank \(d\geq3\),
order exponent \(n\geq5\), and adjacent exponents \(k_i\geq2\) with
\(\sum k_i\leq n-1\). The application recovers precisely those quantifiers,
exact group order, every adjacent product order, the intersection property,
the string condition and the standard regular-polytope interpretation.
No small-parameter case is excluded. The additional endpoint-coset proof
recovers the necessary order bound attributed by the source to Conder.

This covers the promised principal theorem completely. It does not
identify the constructed group with the source's particular presentation,
reprove every auxiliary proposition, or classify all regular polytopes
of two-power order. In particular source Problem 1.1 remains outside this
contract. Treating an existence theorem as recovered does not require
reproducing the historical construction, but it does require all the
existence theorem's conclusions; those are present here.

## 2. The reusable umbrella is mathematical content

The common paper contains several connected proof interfaces, rather than
only a list of repeated notation. The fundamental extension theorem proves
that the designated tuples generate the entire compatible product. It
isolates the kernel factors by induction over distinct supports and proves
the exact kernel in every marked parabolic. A quotient intersection lemma
then gives the full intersection property. Neither a kernel profile nor
the equality of the generated subgroup with its ambient compatible product
is assumed.

The induction also handles nested supports and nonabelian kernels. For a
kernel element attached to support \(S\), a word on \(S\) can have other
nontrivial coordinates only at smaller supports. Inductively isolated
smaller coordinates can be removed independently. Proper-parabolic
injectivity is used exactly where a coordinate has support not contained
in \(S\). Injectivity on individual generators would not suffice.

The local-recognition, deletion, lower-central and separator corollaries
are correct. In the separator proof, the assigned pure kernel factors are
normal in the full compatible product, which justifies moving one factor
past a chosen lift. The two-factor fiber-product statement uses actual
split deletions; it is not a group pushout assertion.

The geometric branch correctly keeps typed coset Helly separate from the
intersection property. Its proof first adjusts pairwise coset intersections
into one chosen base fiber, then solves the fixed/free coordinate constraints
in the kernel. It does not assume that arbitrary intersections map onto
intersections of images. The regular-hypertope recognition proof supplies
thinness, residual connectedness and faithfulness, with involutivity stated
where needed. The singleton-support counterexample explains the boundary.

The finite two-group branch is also complete at its declared retained-input
level. Burnside's basis theorem gives the parabolic Frattini identities.
In the forest proof, a deepest participating edge in a hypothetical degree-two
relation yields a separation into two pure graded subalgebras. The descending
nilpotent argument lifts that separation to the actual commutator subgroup;
actual IP then contradicts the noncommuting edge. The class-two coordinate
model realizes the sharp order and every deletion. No IP in an unproved
intermediate quotient is assumed.

The finite-quotient parameter theorem bounds all lower-central graded
pieces, hence produces a genuinely finite search space. The excess-order
condition bounds the needed nilpotence class. Its kernel intersection test
is both necessary and sufficient, and marked isomorphisms correspond to
identical kernels or to the explicitly allowed label permutations. The
normal index-two descent is exhaustive by the finite two-group action on
nonzero linear forms. These statements prove a finite procedure, not any
particular census output.

Finally, the affine normal form, both lattice quotients, their decompositions
and the dihedral-attachment theorem have the stated properties. In the square
normal form, conjugation by \(ab\) sends the two translation generators to
one another and an inverse; expanding \((x_0ab)^4\) therefore gives precisely
the translation commutator relation. In the finite seed, each deletion makes
the two lattice generators involutions or identities, so every even lattice
relator survives. The linear dihedral coordinate remains present even when
its action on the translation quotient is not faithful. The two weight-three
commutators produce the doubled unit translations, which establishes the
claimed third lower-central subgroup. The diagonal decomposition's parity
argument excludes the remaining possible intersection with \(\langle a,c\rangle\),
including the smallest lattice parameter.

The amalgam section has a separate, correct universal-property proof and
uses its explicitly retained normal-form theorem for torsion and infinitude.
It does not identify a compatible product with an amalgam. I found no
mathematical defect requiring a change to the frozen umbrella.

## 3. The standalone L032 proof closes every adapter

Write \(\delta=n-1-\sum k_i\). The selected base is
\(C_2^{d-3}\times H_{\delta+5}\), whose deletions come from the two factors.
The first consecutive pair orders are two and the last two are four. Each
desired order \(2^{k_i}\) is divisible by that base order, yielding an
explicit marked dihedral quotient. Its proper marked subgroups are trivial
or reflection subgroups, on which the quotient is injective.

Thus all hypotheses of the common theorem are supplied, not referred to
as an unspecified compatibility check. Local recognition gives the exact
adjacent orders. The base coordinates of distant markers commute, and no
attached support contains both; consequently the lifted markers satisfy
all string commutations. The supported theorem proves generation of the
whole group before its order is counted. The order calculation gives
\(2^{1+\delta+\sum k_i}=2^n\). Empty initial products handle \(d=3\), and
\(\delta=0\) uses the proved order-32 seed.

The lower bound follows by distinct endpoint rotation cosets and induction
on the rank. Its attribution to Conder is retained. The only geometric
input is the explicitly stated McMullen–Schulte correspondence. There is
no hidden atlas lookup or numerical small-group check in this proof.
The application is a complete short paper relative to its common theorem
library, rather than just the final exponent substitution.

## 4. Attribution and actual Lean coverage

The historical main theorem belongs to Hou, Feng and Leemans, and the
lower bound is attributed to Conder. The regular-polytope and covering
correspondences are retained from McMullen–Schulte. Burnside's theorem,
finite-p-group nilpotence, the lower-central graded Lie-ring rules and
amalgam normal forms are declared classical inputs. The paper does not
claim to have newly established those results.

The project's contribution in this edition is the closed reusable
interface and the reorganization of already reviewed proofs. The support
induction, forest argument and affine model are substantive mathematical
proofs, but were already part of this repository's preceding work.
Historical priority is not inferred from their present organization.
The provenance builder reproduces the frozen umbrella and its ledger
byte for byte. Its twenty-two spans partition every character; the
recorded predecessor passages, renamings and local additions are visible.

I read all five actual retained Lean sources, totaling 1,356 lines, including
the definitions and the hypotheses of the final construction and transfer
theorems. The supported-kernel statements really prove generation, kernel
profiles and IP from local generation, literal compatibility/deletions and
proper-parabolic injectivity. The profile is not an extra axiom. The later
files prove cardinality, local bijectivity, separator factorization and
lower-central identities. Their lower-central index convention is explicitly
shifted by one. The typed Helly specialization derives its actual coordinate
model and common-fiber intersection data from the construction.

A fresh independent execution of the retained runner passed in 9.47 seconds:
five local modules, two specified Mathlib modules, and thirty-four selected
axiom reports, using only the standard axioms. All thirty-four are inherited
for phase207. The runner's older labels of eleven new and twenty-three old
declarations refer to phase137 and must not be recycled as phase207 novelty.

This does **not** provide a complete Lean proof of either paper. Derived
Boolean deletions, the forest argument, the affine-square construction and
its full family of lattice quotients, the complete dihedral/application
specialization and the group-to-polytope correspondence are not connected
into a complete formal theorem. Some unrelated earlier lemmas remain in
the imported `LiftCertificate` file and therefore in the currently compiled
file closure. A certificate-inclusive cost must retain that actual closure
unless a reviewed extraction changes it.

## 5. Product structure, rendering and costs

The existing split has the correct basic architecture: a common paper and
a complete source-specific application that invokes it. The common paper
is intentionally larger than the dependency closure of L032. The group
clauses of UA.Edge used by L032 do not need the hypertope/Helly clauses.
Clause-level dependency drawings should identify that distinction explicitly,
since the author contract currently names the full UA.Edge label. Under the
user's topic accounting policy, however, the **whole** chosen \(U_A\) is still
charged once. Another topic must pay its whole umbrella independently even
if the texts overlap.

I rendered the unchanged complete manuscripts using the established A4,
one-inch-margin, 11-point STIXGeneral format. The umbrella is **15 pages**;
the L032 application is **4 pages**. Every rendered page was visually
inspected. Mathematical, table and code nodes are preserved by the rendering
transform. There are no overfull boxes or missing glyphs. Two underfull
paragraph warnings in the umbrella do not hide content. The source edition
itself has eight PDF pages; these page counts are layout diagnostics, not a
matched compression ratio.

The current application is not a 20–25-page multi-source volume recovering
a decade of work. It is one successful short application with one principal
source contract. The other five proposed application manuscripts have not
been completed by this split. They must not be credited merely because the
old combined manuscript contains material intended for them. Equally, there
is no reason to pad a complete four-page application to an arbitrary length;
a larger application paper needs additional coherent source results.

The two manuscripts contain 69,528 raw UTF-8 bytes: 58,410 in the common
paper and 11,118 in the application. Their native NFC whitespace-token
counts are 8,278 and 1,529. These are file-integrity and native representation
measurements, not matched source/replacement proof costs. No mathematical
program is a premise of either written proof. If formal verification is
included in the measured product, the five actual Lean files, the runner,
pinned dependencies and any required interfaces must be charged under a
declared common metric. Provenance builders, audit evidence and optional
rendering should be identified separately rather than silently charged as
mathematical proof or silently discarded from an all-artifact measure.

No topic ratio is currently licensed. The denominator requires the finished
application collection plus the full common paper and declared required
artifacts. The numerator needs matched source-body boundaries. A chronological
acquisition curve additionally requires a frozen task order and libraries;
phase207 has not measured such a sequence or established a sawtooth pattern.

## 6. Concrete work remaining

The next author work should reuse the existing proof bank. The remaining
planned contracts are the eight rank-three families in L035; the canonical
quotient and corrected auxiliary claims in F013; the section/free-extension
results in F016; the order-1024 census in N009; and the complete designated
hypertope presentation theorem in L034. Their exact extra obligations are
already listed in phase203 and are not discharged by this review.

F013 is a direct next application of the now closed forest interface,
with the source's false prescribed kernel kept separate from its valid main
quotient and cover conclusions. L035 and N009 share a computational routine;
an L035-only driver needs a real extraction and fresh equivalent outputs,
not deletion of the N009 cost from the unchanged combined runner. F016 still
needs its actual embeddings, assembly and universal-presentation argument;
L034 still needs its source-word checks and sharp order recognition.

For formal progress on the present application, the missing general affine
seed and deletion construction is a substantive target. Once it is connected
to the existing supported-kernel theorems, the marked dihedral adapter and
parameterized existence statement can be formalized. An arithmetic-only
check of the exponent identity would not close that gap.

The final editions should attach per-clause provenance signs or equivalent
margin annotations distinguishing historical results, retained inputs,
reused project proofs and new interfaces. There is no open-conjecture result
to mark in these two papers. Finish the other complete applications, render
and review each, then perform matched topic measurements. This review accepts
the present mathematics while leaving those product and verification tasks
explicitly outstanding.
