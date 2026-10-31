Forty-two primitive-133 cubic certificates
==========================================

This package replays finite certificates for42 original quartets from
job24 in the acquired natural seven-dimensional G2(11) model. It is a
separate supplement to the existing matrix_certificates package. It does
not replace its earlier2308 cases or claim to finish a manuscript.

Imported setting
----------------

The original group, its identification with the full split Cayley group,
the original marking/member associations, faithful frame and complete
orbit/transporter proofs are imported. So are the complete maximal
subgroup classification and the natural geometry of its splitA2
normalizer. Seven-dimensional matrices, an invariant form, file hashes
or an abstract group name do not establish those premises.

The retained literal indexed-domain certificate is included locally,
with its entire catalogue and orbit array. The verifier checks their
hashes, each original position/representative/member/transporter row,
both frame inverses, all three prefix transports, and each missing
matrix's explicit two-by-two Cayley-parameter/frame construction. These
are actual finite calculations. They do not repeat the original354312
point/frame comparisons, full named-group generation, complete Cayley
normalization and model proofs, or every group-action/orbit transporter
check. SOURCE_PROVENANCE.json records that boundary explicitly. Its
absolute historical descriptors are documentary; none is opened.

The cubic implication
---------------------

Let f=X^3+u2 X^2+u1 X+u0 over F11. A cubic is irreducible exactly when it
has no root in its field. The verifier checks all eleven values. Its row
companion C has rows(0,1,0),(0,0,1),(-u0,-u1,-u2). Direct successive
matrix products establish C^133=I, C^7!=I and C^19!=I. Since133=7*19,
these equalities establish exact order133. No polynomial factor list,
remainder, gcd, binary power or elimination result is used for this test.

For the authentic left-end word T=abc, a nonzero row v with vf(T)=0
generates a nonzero cyclic quotient of F11[X]/(f). Irreducibility makes
it the whole field module, whose multiplication-by-X operator is C.
Hence T has order divisible133. The direct relation check first computes
v,vT,vT^2,vT^3 with nine row images, then forms their displayed linear
combination. It does not use the proposer's kernel or Horner expression.

All common rational LEFT lines are checked again
------------------------------------------------

Each a,b,c is checked to be an involution. On a common rational line its
scalar must therefore be+1 or-1 in odd characteristic. A row v with
vA=s*v satisfies(A^transpose-sI)*v^transpose=0. Thus a common line
exists exactly when one of the eight stacked21-by7 systems for the
three signs has rank less than7. The verifier computes all eight exact
ranks and requires rank7 in every case. Checking A-sI without the
transpose would be wrong for row vectors; a nonsymmetric synthetic
involution in the controls tests this orientation.

The four a,b sign-system row spaces are computed once, after every case
has been checked to have the identical literal a,b prefix. For each c
and each sign, its seven transposed equation rows are appended to each
prefix space by forward Gaussian elimination. Replacing a matrix's rows
by an echelon basis preserves its span; adding the same seven rows thus
has exactly the same rank as the full21-row stack. Prefix basis tuples
are not mutated, and the cache is local to one invocation. This is a
linear-algebra reuse, not an assumption about any sign-system rank.

A row reduction against a normalized pivot p costs at most2*(7-p)
field operations; an inserted pivot costs at most7-p plus4 for its
inverse. Seven new rows therefore cost at most7*56+77=469 operations.
Four initial fourteen-row prefix bases cost at most4*(14*56+77)=3444.
The336 extensions cost at most157584. Building the initial eight equation
blocks and two c blocks per case is billed conservatively by4508 further
operations. The total bound165536 is below the existing200000 rank-field
cap. Matrix products, row images, scalar root tests and the original
two-by-two inverse arithmetic are counted or described separately.

From the finite checks to IP failure
------------------------------------

The imported complete maximal cover says that a proper subgroup with19
in its order lies in split SL3(11):2 or J1. The full splitA2 normalizer,
including its outer half, stabilizes a rational line. The eight rank7
checks exclude that alternative for L=<a,b,c>. The retained J1 spectrum
is {6,7,10,11,15,19}: every element order divides one of these numbers,
so it has no element with order divisible133. Hence L is the full G2(11).
The authentic omitted involution e is nonidentity and belongs to G=L.
The subgroups on disjoint label sets{0,1,2} and{3} consequently intersect
in<e>!=1, contradicting the intersection property. This proves an IP
failure, not nongeneration of the full quartet.

Attribution and limits
----------------------

The classification is Kleidman's classical result, as retained through
Nguyen, arXiv:0910.4994, proof of Theorem4.4 before character-degree
exclusions. The split Cayley line-stabilizer description is Wilson,
The Finite Simple Groups, Sections4.2.5--4.2.6. The retained J1 spectrum
is Li, Moghaddamfar, Vasil'ev and Wang, arXiv:2312.07907, Lemma3.9(2).
These are documented imports; this package does not independently prove
their classification statements. The cyclic-module and Gaussian-span
arguments are standard algebra and carry no novelty claim.

The six finite-field helper definitions are literal copies of the
already public matrix_certificates verifier. The new rank and cubic
control flow is separately reviewable. The role retains400000 matrix
products,200000 rank-field operations,200000 row images,2MiB total
artifact reads and1MiB per file,100s internal time and128MiB self RSS.
The requested outer profile is128MiB/150s with4/10GiB admission and
3/8GiB floors. No actual fit, controls or replay result is asserted by
this UNRUN submission. No Original, Lean, conjecture or compression
credit is supplied merely by producing this package.
