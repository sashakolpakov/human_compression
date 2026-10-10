# Independent review of the twisted diagonal unitary construction

10 October 2026. Separate internal mathematical review of
[phase17_unitary_twisted.md](phase17_unitary_twisted.md), together with
the one-modulo-four proof where it is explicitly imported. Exact proof
bytes are identified in the associated JSON. This is not an external
peer review or a publication-priority finding.

**Verdict: PASS under the stated retained inputs and the exact q=3
generation certificate.** For every odd q congruent to three modulo
four, the unique diagonal index-two extension of PSU4(q) inside PGU4(q)
has the displayed rank-four marking of type {4, 2(q+1), 2p}. The theorem
does not assert that the full PGU4(q), with its cyclic quotient of
order four, is involution-generated. Its maximum-rank consequence
retains the phase-nine upper bound.

## Parameter, determinant class and product order

An element λ of order 2(q+1) exists in F_(q²), because q−1 is even.
Its norm is −1, so k=λ−λ⁻¹ lies in Fq and is nonzero. The two distinct
roots λ² and λ⁻² of X²−(k²+2)X+1 show that k² generates the whole
field: a proper subfield Frobenius would fix or interchange them and
force their order q+1 to divide r−1 or r+1. This is impossible for
r<q. The nonvanishing of 1+k² follows from the nonsquareness of −1.

The matrix r2 is a Hermitian anti-isometry. With ξ primitive in F_(q²),
η=ξ^((q−1)/2) has norm −1. Thus ηr2 is unitary, and its determinant
is ζ² for ζ=ξ^(q−1), which represents the nonidentity order-two class
in the diagonal quotient C4. The determinant of r1 is −1 and has even
exponent in that quotient. These computations establish containment
in the index-two group and the presence of its outer diagonal class.

The common algebraic matrix identities still apply. The middle order
is exact: for q+1=4m, λ is primitive of order 8m and i equals λ^(2m)
or λ^(6m). The exponent of λ/i is coprime to 8m, since any common
divisor divides four and that exponent is odd. Thus no smaller scalar
power of the middle matrix is possible. The first and last adjacent
orders remain four and 2p, respectively.

## Rank-one generation and normalization

I checked the use of normalized block matrices separately from the
unnormalized matrices used later for intersection bounds. They are
used consistently and have identical projective images.

The second block projection has the same unipotent and trace-square
invariant as before, so the point-stabilizer, torus-normalizer and
proper-subfield exclusions remain valid. The outer element is now
the normalized S block: its determinant η²=ζ is nonsquare in the
norm-one scalar group. The Dickson argument therefore supplies the
full rank-one projective group. Its exceptional S4 case is excluded
by the full trace field when this is not the prime field, and by
element order in the remaining prime-field cases q≥7.

The kernel of the first projective block projection has a nontrivial
normal second projective image. It contains PSU2(q) by the retained
simplicity and trivial-centralizer facts. No unjustified restriction
to first-block scalars ±I is made here: they may be arbitrary unitary
scalars. Commutators remove them. If D is the second ordinary image,
then D′ is in SU2 and its projective image contains the perfect group
PSU2. Hence D′ times the SU2 center is SU2. Perfection of SU2 now
implies D′=SU2. This establishes a full coordinate SU2, after which
the already reviewed connected-coordinate elimination applies.

The simplicity/perfection step is used only for q≥7. For q=3 the
proof expressly supplies a finite generation certificate instead.
The determinant calculation then identifies the full desired
index-two extension, rather than an unspecified subgroup containing
the socle.

## Similitude scalars, descent and the two small meets

The unnormalized vertex group P has two homomorphisms: its eigenvalue
α on v and its Hermitian multiplier ε. On each generator ε=α², and
therefore this equality holds throughout P. This is an essential extra
constraint in this branch.

Here σ=BH followed by field conjugation has square (1+k²)I and
Hermitian multiplier 1+k². Its invariant plane spanned by v and σv
is nondegenerate. For an arbitrary B-similitude multiplier μ, the
relation is gσ=(μ/ε)σg. The nonzero Hermitian cross-pair yields
μ bar(α)²=ε²=1, and hence μ=α²=ε. Consequently the α=1 kernel is an
ordinary isometry, fixes that plane pointwise, and commutes with σ.
The same explicit quadratic descent as in the first branch embeds
it in a binary orthogonal group, giving the order bound 2(q+1).

Although μ4 consists of norm-one scalars in this branch, the actual
scalar subgroup of P still has only two elements. For a scalar αI,
its Hermitian multiplier is one, whereas the group constraint gives
α². Thus α=±1, and −I=r2² occurs. The projective order division by
two is correct. Together with the four possible eigenvalues this
bounds the common projective parabolic group by 4(q+1), attained by
the middle dihedral subgroup.

The left sign-pattern argument is unchanged. For the right meet,
the possible extra central dihedral involution has a lift C with
Cv=iv. Here ε(C)=−1, so the same cross-pair argument forces any
B multiplier to be −1. The unchanged nonzero entry −ik²/2 in
CBCᵀ+B excludes it, even projectively. Thus both rank-three
intersections and the maximal-parabolic intersection are established.
The recursive string C-group criterion then supplies full IP.

## Exact execution and its scope

The independently written
[symbolic checker](phase17_unitary_twisted_independent_check.py) and
[report](phase17_unitary_twisted_independent_check.json) pass 32
identities in SymPy 1.14.0. The coefficient involution fixes k and
sends i to −i. The checks include the anti-isometry multiplier of
r2, σ²=(1+k²)I, the cross-pair, all unchanged word/form identities,
and both characteristic polynomials. This computation is independent
of the author's symbolic checker.

I also inspected and freshly executed the author's strengthened
natural-action script for q=3,7,11. The separate
[run report](phase17_unitary_twisted_independent_run.json) and
[log](phase17_unitary_twisted_independent_run.log) record all 48
subset groups and 768 meets passing. Source bytes were hashed before
execution and checked unchanged afterward. This is an independent
rerun, not a separately implemented group algorithm.

For q=3 the generated permutation order is 6,531,840, equal to twice
the standard PSU4(3) order, and the marking has type {4,8,6}. The
defining field polynomial used in this execution is X²+2X+2, with
k=1, λ its canonical primitive root and i=λ². The construction lies
in the desired projective unitary subgroup by the determinant and
Hermitian computations. Since scalars act trivially on isotropic
planes, the action order and ambient order give the required order
sandwich; no group-recognition oracle is required. The script also
verifies all 256 meets for that field, though only the finite
generation assertion is needed by the written uniform proof.

The q=7 and q=11 executions are bounded corroboration; they do not
replace the uniform generation or intersection arguments. No new
Lean formalization is claimed. Rank-three existence, field/graph
extensions, and priority remain outside this review.
