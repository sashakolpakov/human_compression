# Independent review of the diagonal unitary construction

10 October 2026. This is a separate internal mathematical review of
[phase17_unitary_diagonal.md](phase17_unitary_diagonal.md). The associated
JSON identifies the reviewed proof bytes. This review does not establish
publication priority or constitute external peer review.

**Verdict: PASS under the stated retained inputs.** The written argument
proves that PGU4(q), for every odd q congruent to one modulo four, admits
the displayed rank-four string C-group marking of type
{4, 2(q+1), 2p}. Maximum rank four additionally uses the earlier dimension-four
upper bound. The present proof does not itself prove that bound.

## Parameter and product orders

The full-field assertion is valid for all prime powers in the stated
congruence class, including q=5. If k² lies in a proper subfield Fr of
Fq, its nonsquareness forces q=r^d with d odd and at least three. The
quadratic equations for k and λ put λ in Fr⁴, whereas its original field
is F_(r^(2d)). Their intersection is Fr². Its proposed order r^d+1 then
exceeds the multiplicative order of that field. There is no hidden
large-q condition or exceptional-field search.

The middle characteristic polynomial has four distinct roots. A more
explicit check of the scalar exponent is useful. Write q+1=2m with m
odd. Comparing i and −i forces an exponent 2t. The equality of the
i and λ powers says λ^(2t)=(-1)^t. The left side lies in a group of odd
order m, so both sides are one. Hence m divides t and t is even: the
least possible exponent is 4m=2(q+1). This also proves exactness.

The last product has nontrivial unipotent part of order p and projective
semisimple part of order two. Thus its projective order is exactly 2p.
The matrices are nonidentity projective involutions, with the asserted
distant commutations.

## Generation and the retained adapter

I read the full phase-eleven generation argument used here, including
its connected-coordinate-SU2 elimination proof. The modified generators
have the same block-diagonal word d and the same r2. Their changed
block unipotent differs by −I, which already belongs to the group as
r2². Thus even the actual block subgroup can be identified with the
old one; the projective comparison in the present proof suffices.

The rank-one argument retains the stated Dickson maximal-subgroup list.
The nontrivial unipotent, its moved fixed line, the outer diagonal class
of Z and the full trace-square field exclude the listed proper types.
The exceptional S4 type cannot survive the remaining prime-field case,
since its prime p is at least five. The kernel word is nonscalar in its
second block, and its normal projective image contains PSU2(q). The
scalar first block is necessarily ±I, so perfection produces a whole
coordinate SU2. The connected pair argument then produces SU4.

The determinant of r1 is −1. Because the norm-one scalar group has
order twice an odd number, −1 represents the nonidentity class modulo
fourth powers. This establishes the full diagonal index-two extension,
rather than merely the simple socle.

## The projective intersection and its scalar factors

The row-unitary convention and the column-Hermitian convention are
compatible here because H²=I. I checked the conversion explicitly.
For σ=BH followed by field conjugation, σ²=νI and its Hermitian
multiplier is ν=−1−k², which is nonzero. The vectors v and σv form a
nondegenerate isotropic pair because their cross-pair is 4i+2k≠0.

The argument correctly permits an arbitrary initial symmetric-form
multiplier μ for a chosen vertex lift. The relation gσ=μσg and the
eigenvalue gv=αv yield μ bar(α)²=1. Since α belongs to μ4 in Fq, this
forces μ=α². One must not presume this sign restriction merely from
the facet generators; the proof does not do so.

The α=1 kernel fixes the entire plane spanned by v and σv and commutes
with σ. Scaling σ by a scalar of the required norm gives an antiunitary
semilinear involution on the orthogonal complement. The explicit
quadratic descent decomposition proves that its fixed space is
two-dimensional over Fq and spans the complement. Its restricted form
is nondegenerate and symmetric, and the kernel acts faithfully on it.
The binary orthogonal order bound therefore gives at most 2(q+1)
kernel elements. The four possible α values give at most 8(q+1)
matrix elements.

The scalar subgroup of the actual vertex lift is exactly {I,−I}:
its elements have eigenvalue in μ4 and norm one, and −I=r2² occurs.
It is also contained in J. Dividing by two is therefore justified and
gives the required projective bound 4(q+1). The known middle dihedral
subgroup attains this bound. No recognition or order formula for the
whole vertex subgroup is used.

## Rank-three intersections and recursive IP

The four sign patterns in the left dihedral orbit are correct and
projectively distinct in every odd characteristic. Its stabilizer of
the chosen line has exactly two elements. This proves the first
adjacent-pair intersection.

For the right intersection the adjacent dihedral orders have gcd four.
Every order-four subgroup of the order-4p dihedral group is a Sylow
two-subgroup containing its central rotation involution. The expression
C=M(I+N/2) satisfies C²=−I and M^p is a sign times C, so C is itself
in the actual vertex subgroup. Its eigenvalue on v is i. If C preserved
B up to scalar, the previous cross-pair argument would force multiplier
−1. The nonzero entry −ik²/2 of CBCᵀ+B excludes this. Allowing a further
projective scalar does not help: being a B-similitude is invariant under
scalar multiplication. Hence the intersection has order two.

Both rank-three markings thus satisfy IP. Their common maximal
parabolic intersection is exactly the middle rank-two group. The
retained recursive string C-group criterion applies with all these
hypotheses supplied, giving full IP.

## Independent execution and limits

The separately written
[symbolic checker](phase17_unitary_diagonal_independent_check.py), with
[its report](phase17_unitary_diagonal_independent_check.json), passes
32 checks in SymPy 1.14.0. It does not import the author's checker.
It verifies the four unitary equations, squares, determinants, three
form multipliers, distant relations, block word, both characteristic
polynomials, the nonzero square-zero N, the semilinear identities,
isotropic-pair calculation, C identities, its form defect, and the
left dihedral orbit. It treats conjugation as i↦i and k↦−k, rather
than complex conjugation. The identities take place over Q(i,k) with
i²=−1; their denominators are powers of two, so they specialize to
every odd characteristic.

These algebra checks do not execute Dickson classification, generation,
the binary orthogonal order theorem, or all subset intersections in
finite fields. Those are the written proof and its explicit retained
inputs. This audit makes no fresh Lean compilation claim and no claim
that a finite sample proves the uniform theorem. The q congruent to
three modulo four extension, if studied separately, is outside this
audit.
