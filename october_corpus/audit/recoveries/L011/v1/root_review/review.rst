Distinct review of the simple-group exclusion theorem
=====================================================

Accepted as a complete principal recovery of L011, using the frozen v2
packet. The four-page common paper and four-page application recover the
source's two named theorems, all four infinite exception families, and all
eight isolated exceptions. The positive generation classification remains
an explicitly retained theorem of Nuzhin and Mazurov, with the source's
Jones--Macaj correction. This is not a new independent classification of
all finite simple groups and is not a new conjecture answer.

Root read the complete six-page primary text, directly checked primary
pages two through five, read all eight replacement pages, all nine complete
proof environments, the 27 dispositions, and every required GAP program.
All eight replacement pages were directly viewed. The source's finite
Magma assertion is replaced by the acquired complete GAP implementation;
neither an absent source program nor a generic possible search is treated
as an executed proof.

Projective dimension three
--------------------------

The determinant argument normalizes a projective involution to a unique
linear involution with the prescribed center and axis. Conjugation respects
this normalization, so projective commutation becomes literal commutation.
The odd-characteristic incidence criterion correctly requires distinct
projectivities. In characteristic two the rank-one nilpotent calculation
shows that commuting transvections have a common center or common axis.

For an irreducible lift, its commuting division algebra restricts
injectively to the one-dimensional center of an involution and is exactly
the ground field. The faithful irreducible image algebra has zero radical
and one simple factor, hence is the full matrix algebra. This proves
absolute irreducibility without a semisimplicity assumption on the group
algebra in modular characteristic. The direct-product tensor argument then
rules out a commuting adjacent cut in dimension three.

The characteristic-two cases exhaust the two possible cross-incidences
between the first centers and axes. A possible tail either does not exist
or fixes a common line. For odd characteristic, a third involution commuting
with both initial generators has its center and axis uniquely prescribed,
giving the rank bound. In rank three the invariant-form spaces intersect
nontrivially; irreducibility kills the radical. In rank four, simultaneous
endpoint diagonalization leaves exactly two homogeneous equations on the
three diagonal entries of a symmetric form. This replaces the source's
inference about irreducibility of the initial subgroup, which need not
follow from irreducibility of the whole marking. The order comparisons use
isometry groups, not larger similitude groups. Their stated ratios exclude
both projective three-dimensional families in all nonabelian simple cases.

Six-dimensional orthogonal support proof
---------------------------------------

The classical Dickson parity and Klein identifications are explicit
retained inputs, including both quadratic signs in characteristic two.
For an involution, N=g-I is self-adjoint with square zero and rank two.
Its image is totally isotropic for the polar alternating form and its
kernel is the perpendicular complement. Perfectness of the finite field
gives a singular vector in the support. The coefficient calculation in
that basis follows by equating Q(Nx) with B(x,Nx); rank two eliminates the
remaining diagonal coefficient. This proves the displayed formula.

Commuting involutions with disjoint supports would produce a four-dimensional
totally isotropic space for a nonsingular alternating form in dimension
six. A singular common support line instead makes the two displayed maps
commute. The case split for arbitrarily many string generators is complete:
disjoint adjacent supports force a proper total support; intersecting
adjacent supports force either that same conclusion or a common fixed
nonsingular vector. The short strings of lengths at most four have proper
total support directly. Simplicity and marked IP rule out disconnected
strings before applying the obstruction. This proves both even-field
four-dimensional exclusions, including the unitary case at q=2.

Rank-three intersection and finite exhaustion
---------------------------------------------

The simple rank-three intersection argument includes the exceptional
four-group case. If the two rotation subgroups in the common dihedral
subgroup coincide, they give a cyclic normal subgroup of the whole group.
If they differ in a four-group, b=uv with u central in the first dihedral
subgroup and v central in the second. The two indicated generating pairs
then commute across the pairs and yield nontrivial commuting normal factors,
contradicting simplicity. The endpoint intersections and independence
complete all rank-three subset intersections.

The finite search chooses representatives of every involution class, then
every eligible involution orbit under the pointwise centralizer of the
ordered prefix. Its candidate set is invariant under that centralizer.
String commutation, independence and noncommuting adjacency are necessary
conditions for a connected C-marking. Every subset intersection is checked
literally after the cheap necessary rejection. Each recursion strictly
increases subgroup order, so the algorithm terminates without an imposed
rank cutoff. Its orbit-coverage checks and full IP tests match the written
proof. Simplicity excludes disconnected final strings.

Named alternating, Mathieu and McLaughlin library identifications remain
retained input; order alone is not used to recognize an arbitrary sporadic
group. The two unitary models check determinant one, a nonsingular Hermitian
form, actual isometry equations, all isotropic projective points and the
scalar kernel. Verified projective order together with containment proves
that their images are the full named groups.

Correction required during review
---------------------------------

The first packet's call to StabChain could use an order or stabilizer chain
already cached by a constructor. GAP's official permutation-group manual,
sections 43.7--43.8, confirms that the size option defaults to a known order.
Root requested an explicit calculation from permutation generators alone.
The author preserved v1 and supplied v2. FreshPermutationOrder now creates
a distinct generator-only group and checks that it has no known size,
cached chain, ambient parent, size option or upper bound. Its verified
chain uses random=1000 and tryPcgs=false. The method still permits random
construction internally; its verification is guaranteed under the named
GAP implementation. The source code and manual agree on this distinction.

Root reran all of v2 at /private/tmp/L011_v2_root_review01. All eleven
fresh order calculations pass, as do the eight exclusions, all 1,209 proper
prefix representatives, and the six positive A5 markings. The optional
separate A5/A6 coordinate implementation also agrees. All 47 exports,
27 dispositions, nine proof bindings and 24 negative controls pass.
Both clean two-pass pdfLaTeX builds reproduce all eight full page texts.
The common document and all complete proof bodies are unchanged from the
version already read; all four current application pages were also viewed.

The three whole GAP files are required proof components. The Python oracle
is optional validation, and the two Python runners are operational tools.
Correctness of the finite group operations, named model libraries, retained
classical structural results and positive classification is explicit.
Their external proof and runtime costs remain unknown, not zero. There is
one whole-original recovery credit, no new question credit, no new Lean
declaration and no numerical compression factor in this acceptance.

Official manual checked during review:
https://gap-system.github.io/gap/doc/ref/chap43.html
