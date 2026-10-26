Independent review of the symplectic endpoint argument
======================================================

Reviewer: /root/f004_flag_proof_review.
Author reviewed: /root/f004_uniform_prefix_theory.

Disposition: the six-dimensional theorem and its stated conditional
application are mathematically supported. There is no mathematical
blocker. This is an independent hand review, not an operational Source
verdict, a fresh matrix computation, a Lean proof or a ledger acceptance.

The reviewed manuscript is endpoint_images.tex, 14194 bytes, SHA256
2bedc0c9f53e0a37e4140ee7fd6b27be084e5805b2a9b1849c2536f32c860dee.
The author's provenance.json is 10249 bytes, SHA256
6f0fce516966486312756bbea7da0df49387f25d0db4c7b334cb0825d67a7e7b.
Both remained unchanged during this review.

The abstract argument
---------------------

Let V have dimension six over a field of characteristic two, and let its
alternating form be nondegenerate. If S is an isometric involution, its
adjoint is S inverse, hence S itself. Thus S-I is self-adjoint and
(im(S-I)) perpendicular equals ker(S-I). Its square is zero, since
S squared is I and the characteristic is two.

For E with rank(E-I)=3, image and kernel of E-I coincide by rank-nullity;
the same subspace U is its own orthogonal complement. For A with
rank(A-I)=2 and (A-I)(E-I)=0, the commuting endpoint relation gives the
reverse zero product as well. Therefore P=im(A-I) is contained in U,
and U is contained in ker(A-I). Their dimensions are two and three.

Write B for the second mark. It commutes with E in every string of
rank at least five and therefore preserves U. There are two exhaustive
cases.

If B preserves P, every other mark preserves P because it either is A
or commutes with A. All marks are invertible, so preservation is
stabilization, not merely an inclusion into a smaller image. The
generated group stabilizes the proper nonzero plane P.

Suppose instead that B does not preserve P. Since B is invertible,
some p in P has Bp outside P. Then v=(B-I)p belongs to U but not P.
The restriction of B-I to U is nonzero and has square zero. A square
zero map on a space of dimension three has rank at most one; its rank
is consequently one, and its kernel has dimension two.

Let Q=im(B-I), and let F be the common fixed space of A and B.
The preceding vector gives U=P+kv contained in P+Q. Self-adjointness
therefore gives

    F = P perpendicular intersect Q perpendicular
      = (P+Q) perpendicular
      contained in U perpendicular = U.

Because A fixes U pointwise, F is exactly the fixed space of B on U,
so F has dimension two. It cannot equal P: that would make B fix P
pointwise, contrary to the case assumption. Two distinct planes in a
three-dimensional space span that space, so P+F=U.

Every linear map commuting with A and B preserves both P and F,
and hence preserves U. In particular, the penultimate mark does so:
its distances from the first and second marks are at least three
and two. Every other mark either is E or is at distance at least two
from E, and hence also preserves U. Thus the generated group
stabilizes U in the second case.

These two cases prove the theorem. They use neither the intersection
property, independence of the marks, a complete group centralizer,
a full linear commutant nor any special property of G2. The argument
also permits identity marks; it remains an exclusion criterion for
generating strings, so it applies in particular to string C-groups.

The corollary follows without faithfulness. If the original marking
generated the original group, its matrix images would generate the
entire matrix image. A member of that image escaping P or U rules out
the corresponding stabilization alternative. The same escaping
member may serve for both alternatives.

Hand check of the retained matrices
-----------------------------------

The adopted 25/26 member certificate is 7214 bytes, SHA256
db9bc6d249bd6184a53b2b29c2c28d0011ede97872b94105d4032f0315dd8da9.
Its Root acceptance is 861113 bytes, SHA256
291ecff1352e31aa8e539c9e1be09ece6a35bcafe813cb0c64c1ee546da570ce.
The acceptance names that exact saved certificate, family 4, members
stage, adopted=true. The certificate orders its first two matrices
as a,e. Its first two matrices, ambient matrices and complete field
codec also agree exactly, as JSON values, with the earlier adopted
member certificate (5,530 bytes, SHA256 9b0157df...) and its acceptance
(276,679 bytes, SHA256 372ef990...).

In column notation the first endpoint satisfies

    A-I = mu(E15+E26),  mu = code 4,

and the second has a zero lower half and upper right block

    [1 alpha delta; gamma 0 alpha; 0 gamma 1],

with alpha=code 5, delta=code 3, gamma=code 2. The nonzero field codes
are not integer scalars. The code table identifies code 1 as the unit
and code 0 as zero; all four named coefficients are nonzero.

The image of A-I is span(e1,e2). Its rank is two. The upper block of
E-I has determinant delta times gamma squared: the two alpha-gamma
terms cancel in characteristic two. Its determinant is nonzero,
so E-I has rank three and both its image and kernel are
span(e1,e2,e3). Both differences annihilate that first summand
and map the second into it. Their two products are zero.

For J with antidiagonal ones, an upper unipotent block matrix is
symplectic exactly when J3 times its upper right block is symmetric.
The manuscript lists these two symmetric matrices correctly. This
independently checks form preservation of A and E, though the
application still retains their original membership correspondence.

The first ambient generator is diagonal with codes 2,7,3,6,2,7.
The adopted multiplication table explicitly lists
code 2 times code 7, code 7 times code 2 and code 3 times code 6 as code 1.
Those are the three paired products required to preserve J.

The second ambient generator has columns

    e1+e2, e3+e4, e1, e5+e6, e3, e5.

Under the antidiagonal form, its paired columns 1,6;2,5;3,4 have value
one. All other off-diagonal pairings vanish. In particular the
potential pairing1,4 equals1+1=0. This checks the second form identity
by hand. Its second column is e3+e4, which belongs to neither
span(e1,e2) nor span(e1,e2,e3), so it supplies both required escapes.

No new matrix multiplication kernel or finite-field operation was
run for this review. The symbolic calculations above are hand
mathematics; field-code products are entries read from the already
accepted multiplication table.

Original jobs and representation premises
-----------------------------------------

The catalogue (65,946 bytes, SHA256 d83a3fcb...) maps each job [27,5]
through [36,5] to pair 4 and the same pair04.g
(549,385 bytes, SHA256 e523da47...). Every such job occurs in the
unchanged required universe of 686 rows (SHA256 04bac8aa...) and in
the pending snapshot of 87 rows (SHA256 708721c0...). The ten jobs
are distinct. These are metadata
membership and identity checks, not new group calculations.

The original three_mark_frontier_functions.g code constructs triples
[a,b,c], where a,b are the chosen commuting endpoint pair and c is
the second string mark. The original ends_queue_functions_v6.g states
and implements the mark order1,r,2,r-1,... . Thus the pair identified
by the accepted a,e matrices is the first/last pair required by the
theorem. No replacement of the full Q=C_A(e) by its smaller stabilizer
is used.

There are 20 original pair 4 rows with labels 19 through 38, 17 active
acquired family rows 20 through 36, and 10 currently pending eligible
rank-five jobs 27 through 36. These counts must not be conflated.
The written theorem covers all completions of the fixed endpoint pair,
but this review proposes no new credit outside those ten pending jobs.

The bridge remains an imported accepted representation/correspondence
premise. Its accepted record explicitly says it supplies no marking
exclusion or matrix-properness claim; this new hand argument supplies
that part. I checked the exact bridge and member references and the
small retained matrix values, but did not re-execute the original
group model, matrix transport, centralizer construction or old
proof protocols. The original named-group identification, full
original-generator correspondence and membership route retain their
existing qualifications. If any such premise were withdrawn, this
finite application would remain conditional on it.

The column convention is internally consistent. A row-vector
presentation of the original action does not change the abstract
matrix subgroup or its generation problem. The proof does not
identify a column with an original permutation point. No raw point
query or contragredient identification is required.

Attribution, limits and next use
--------------------------------

Adjoints, orthogonal-complement identities and the rank bound for a
square zero map are standard linear algebra. The contribution reviewed
here is the combination giving the P-or-U dichotomy and its application
to the retained endpoint pair. The original group data and earlier
transport results keep their attribution. No historical-priority
claim is assessed.

The broader 2m paragraph should be read with m at least two whenever
proper nonzero P is wanted. This is an editorial qualification of
that optional extension; the main six-dimensional theorem has no
such ambiguity or gap.

Before ledger use, Root still needs a typed acceptance of this new
SYMPLECTIC_ENDPOINT_IMAGES proof kind, binding the exact theorem,
independent review, accepted original matrix premises, required-job
universe and fresh pending snapshot. Existing commutant certificates
must not be relabelled as this proof. No per-B matrix, K or H
acquisition is mathematically needed for the ten jobs once that
application is accepted. Any fresh finite checking or Lean
formalization would require its own genuine execution and is not
supplied by this hand review.

No operational Source PASS, Root acceptance, ledger update, new
completed manuscript, compression factor or open-conjecture solution
is claimed. No Source/helper, guard, runtime, scientific kernel,
group enumeration, native probe, Lean or compilation operation ran.

