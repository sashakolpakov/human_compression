# Independent review of finite covers from the end-coset complex

10 October 2026. **Accepted within the stated hypotheses.** The paper proves
an exact criterion for locally faithful finite abelian C-covers of a finite
string group whose two end groups are already C-groups. It proves the
conditional finite-multiplicity theorem, classifies the Tomotope's locally
faithful abelian-kernel covers, and excludes all its locally faithful covers
with nontrivial odd-prime-power kernel. It does not solve the general finite
minimal-cover question.

I read the complete frozen phase246 paper, its programs and runner, all three
Lean proofs, the source ledger and qualifications. I viewed every page of the
six-page PDF. I freshly read the primary Tomotope pages 8–9 and 13–14 and
Monson–Schulte pages 5–6, and viewed the first two pairs of these primary
pages. The retained literal flag model has the source identification already
independently accepted in phase218; this review uses that identification
explicitly rather than claiming a new reconstruction of the source's flags.

## The amalgam and the actual kernel

The assumptions suffice in every finite rank at least three. Write
\(A=G_{0,\ldots,n-2}\), \(B=G_{1,\ldots,n-1}\),
\(C=G_{1,\ldots,n-2}\), and \(D=A\cap B\).
The embeddings of C into both factors are the actual inclusions in G.
The map \(V=A*_C B\to G\) is onto and injective on each factor. Its kernel F
therefore acts freely on the Bass–Serre tree, and its quotient graph has
exactly the stated vertices and edges. Connectivity follows from generation
of G by A and B. The free-action theorem is a retained classical input.

Every string relation except the commutation of the two extreme generators
already lies in one of the factors. Hence adjoining
\((r_0r_{n-1})^2\) supplies the correct universal completion for string covers
whose end groups remain faithful. Since that relator lies in F, its normal
closure in V equals its normal closure in F after adjoining one conjugate
for every coset of F. These are precisely the translated square loops in
the quotient graph, up to base paths and reversal. Attaching the full
translated family thus gives the stated kernel \(\Pi\), not merely a group
mapping onto it. This proves Proposition 2.1 with the declared topological
input. Degenerate boundaries are allowed and do not invalidate this
presentation argument.

The left-coset display and right-coset implementation agree under inversion.
In the latter convention the four oriented terms are
\(e_{Cg}-e_{Cr_0g}+e_{Cr_0r_{n-1}g}-e_{Cr_{n-1}g}\).
The extreme generators commute in the finite base, so the central product
order is immaterial there. No unproved comparison between distinct coset
complexes is being used.

## Complete intersection and abelian criteria

For each \(g\in D\), the factor lifts \(a_g\in A\), \(b_g\in B\) are unique.
Their discrepancy \(a_gb_g^{-1}\) lies in the kernel. The path from A to
\(a_gb_g^{-1}A\) has first edge \(a_gC\), oriented positively, and second
edge \(a_gb_g^{-1}C\), oriented negatively. Its projection is exactly
\(e_g-e_1\). Thus the class used in the matrix is the class of the actual
lift discrepancy. This step is essential: testing only the image of an
intersection in G would omit possible kernel elements.

Both end groups embed in every quotient over G. Any element in their
intersection projects into D; over each g there is at most one lift in
each end. The lifts agree automatically for g in C and agree for no other
g precisely when every listed discrepancy survives. The recursive C-group
criterion then gives both directions of Theorem 3.1. The argument controls
all parabolic intersections through that retained criterion.

Abelianization is intrinsic to \(\Pi\), so the subgroups defining the
canonical quotients are characteristic in \(\Pi\) and normal in U.
The cellular complex is finite. Its integral first homology is therefore
finitely generated, and its quotient by m is finite; this proves that the
constructed covers really are finite. The universal coefficient assertion
in degree one has no hidden Tor term because H0 is torsion-free.

Any abelian kernel is a quotient of this integral homology. Vanishing of a
listed discrepancy therefore obstructs every such cover. Conversely, a
single m can separate the finite collection of nonzero classes: use a
multiple of the torsion exponent and a sufficiently large integer for
their nonzero free coordinates. This proves the complete finite abelian
criterion, not just a sufficient construction. The exponent-p version is
the corresponding maximal elementary abelian quotient.

The prime-group obstruction is also valid for nonabelian kernels. A
nontrivial finite p-group has a nontrivial quotient of order p. A quotient
of \(\Pi\) of this form contradicts vanishing of its mod-p first homology.
Nothing here says that the arbitrary-cover construction is residually finite.

For the conditional multiplicity theorem, every finite C-cover has a
minimal C-quotient over G. Its kernel is a nontrivial p-group when it
descends from the p-cover and G itself is not C. Distinct primes therefore
give distinct orders, hence distinct minimal covers. A nonzero rational
class has a nonzero free coordinate and survives modulo all but finitely
many primes. The finite list of discrepancies gives one finite exceptional
set. The theorem's hypotheses are sufficient conditions, not an assertion
that every genuine polytope monodromy satisfies them.

## Independent Tomotope reconstruction and finite checks

The independent program `phase255_native_complex.py` imports none of the
phase246 cell or voltage code. Starting with the retained four literal
flag permutations, it uses native GAP right cosets and the orbit of the
ordered square under the induced right action. It obtains:

| Quantity | Independent result |
|---|---:|
| Base group order | 18,432 |
| End orders | 576 and 1,152 |
| Middle and overlap orders | 24 and 48 |
| Graph vertices and edges | 48 and 768 |
| Translated square cells | 18,432 |
| Cycle-lattice rank | 721 |

Every independently generated boundary was checked to be an integral cycle.
There is exactly one nontrivial parallel-edge coset. Applying the separately
frozen exact integer algorithm to this independently numbered matrix gives
719 unit factors, two factors equal to 2, and no free part. The remaining
columns are 282 and 672, rather than the author's 165 and 509, and the
defect image is (1,0). Thus this is not a comparison of identical cached
matrix files. It independently confirms
\(H_1(X;\mathbb Z)\cong C_2^2\) and nonvanishing of the defect modulo two.

The full author replay passed freshly in 21.52 seconds. It regenerates all
three diagnostic complexes, verifies their integer and modular conclusions,
and constructs the actual Tomotope voltage permutations. GAP proves that
their group is regular of order 73,728, maps onto the literal base with
kernel \(C_2^2\), retains the two end orders and satisfies all 256 pairs of
marked subgroup intersections. The universal property and equality of
orders identify this concrete group with the canonical H2. No assumed
voltage-cover identification substitutes for these direct checks.

I separately checked the action of the actual four generators by conjugation
on the three nonidentity kernel elements. Its image has order two and has
exactly one fixed nonidentity element. Hence there is exactly one kernel
line invariant under the whole group. All 24 elements of \(D\setminus C\)
give the same nonzero lift discrepancy, which lies outside that line.
The line is also the intersection of the kernel with the centre. This
independent check uses the conjugation action, rather than the author's
enumeration of normal subgroups.

The canonical abelian kernel is C2 squared, so every locally faithful
abelian-kernel cover is a quotient of H2 by an invariant kernel subgroup.
There are only the trivial subgroup, the unique invariant line and the
full kernel. The full kernel gives the non-C base; the other two give
orders 73,728 and 36,864. The latter is minimal because its kernel over G
has prime order. Proposition 5.1 therefore gives the complete classification
within its specified class.

For precision, its reference to Theorem 3.1 uses the lift-discrepancy
argument in that theorem's proof for the quotient by the invariant line.
That argument works for every quotient over G, not only the displayed
canonical H_m. The formal subgroup equivalence also states this more
general interface. There is no additional unproved quotient assertion.

The integral computation gives zero mod-p homology for every odd prime,
not merely the few primes tested by the finite-field program. Corollary 3.3
therefore excludes all nontrivial odd-primary locally faithful kernels.
The two smaller input markings remain group diagnostics; this review gives
them no new status as monodromy groups of actual polytopes.

## Source attribution and the remaining general problem

Monson–Pellicer–Williams explicitly construct the earlier order-73,728
covers in Examples 4.1–4.2. Their equality of orders does not identify their
markings with the present cover. The source explicitly says that their
vertex-figure subgroup orders differ. The paper correctly makes no new
existence claim merely from obtaining that order.

Proposition 4.5 of the primary paper states a marked epimorphism of order
two from its order-36,864 C-group to the Tomotope monodromy and gives end
orders 576 and 1,152. The restrictions to the ends are onto groups of the
same orders, hence are isomorphisms. That prior cover is therefore locally
faithful with abelian kernel. The complete classification above identifies
it with the unique smaller quotient; this uses the marked covering property
and local orders, not group order alone. The known infinitely many finite
minimal covers remain attributed to the source's Theorem 5.9.

The kernel-containment discussion matches Monson–Schulte Lemma 3.3 and
Theorem 3.4 exactly: their finite C-group maps onto the specified finite
string group. That construction moves to a smaller kernel in the universal
string group, whereas making a prescribed cover finite by a quotient
requires a larger kernel. The two directions cannot be interchanged.
The separate residual-finiteness lemma is valid when all proper parabolics
are finite; then the set of nontrivial differences of pairs of parabolic
elements is finite and can be avoided simultaneously. It cannot be applied
to the retained arbitrary-cover construction without establishing that
extra hypothesis.

The new restriction concerns covers preserving both ends, a condition that
the earlier surface construction deliberately does not satisfy. It is no
counterexample to the general finite minimal-cover question. No additional
principal source, complete source replacement or conjecture solution is
admitted by this review. Historical priority for the new formulation is
not asserted.

## Formal scope and decision

I read each of the three Lean proofs. The strongest is an equivalence for
images of actual subgroups under a quotient homomorphism over a base. It
requires injectivity on one end; the geometric application has both ends
injective. The second theorem preserves that faithfulness under a quotient
over the base. The third gives the correct direction of kernel containment.
All three freshly compile under the pinned Lean and Mathlib versions using
only the reported standard axioms. The finite C2 counterexample in the
driver correctly demonstrates why omitting the injectivity premise would
make the first equivalence false.

The three deliberate computational changes are rejected: killing the real
homology defect, removing the voltage data and claiming a false kernel
order. These checks complement the written proof; they do not formalize
the topology. Bass–Serre theory, cellular homology, the C-group criterion,
the integer matrix evaluation and GAP's group algorithms retain their
declared written or computational status.

No mathematical correction to the frozen author package is required.
Acceptance is for the complete stated general criterion and the restricted
Tomotope classification/obstruction, with the retained inputs above. It is
not acceptance of the unresolved general finite-cover conjecture.
