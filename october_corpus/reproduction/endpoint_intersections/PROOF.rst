Failure of the intersection property at position 2352
====================================================

1. Statement and hypotheses
----------------------------

Let C be the split Cayley algebra over F_11, let V be its seven-dimensional
trace-zero subspace, and let G=Aut_F_11(C)=G_2(11) in its faithful natural
representation on V. Write vectors on the left of matrices. Let
(a,b,c,e) be the original quartet at position 2352 of job 24, rank 4,
with representative J-index 7302. Put

             L=<a,b,c>,   R=<b,c,e>,   M=<b,c>.

The identification with this particular natural representation, the
membership of all four matrices in G, and their association with the
original quartet are retained acquisition premises. Neither the name
G_2(11) nor membership in it follows merely from a matrix digest. The
four original marks are nonidentity involutions and satisfy the string
commutations. In particular, a and c are distinct commuting involutions.
The exact acquired quartet, frame and original-record references are
listed in EVIDENCE.json; no replacement tuple is used in the argument.

Theorem. Under these model, membership and acquisition premises, the
quartet at position 2352 generates G but does not have the rank-four
intersection property. More precisely,

             L=G,      |R|=1,742,400,      |M|<=24,

and consequently

                    L intersection R = R != M.

The finite hypotheses below are established by explicit arithmetic
certificates for this original quartet. Their identities, verification
records and association with the acquired model are listed separately
in EVIDENCE.json. The mathematical argument remains conditional on the
stated natural-model and membership premises.

2. A consequence of the maximal-subgroup classification
-------------------------------------------------------

Lemma 1. If H<=G acts irreducibly on V over F_11, has |H|>12,096, and
contains an element of order 4, then H=G.

Proof. Suppose that H is proper, and choose a maximal subgroup X of G
containing it. We use the complete classification for the inner group
G_2(11), including its restrictions at q=11, before any elimination based
on character degrees. This is the classification of Kleidman [K], in
the form retained in [N] and the common theory cited in EVIDENCE.json.

First consider either parabolic subgroup. It has a nontrivial normal
11-subgroup U. A finite 11-group acting on V has a nonzero fixed vector:
its nontrivial orbits on V have cardinality divisible by 11, so the
cardinality of V^U is divisible by 11 and cannot be just one. Since the
natural representation is faithful and U is nontrivial, V^U is also a
proper subspace of V. Normality makes V^U invariant under X. It is
therefore an H-invariant nonzero proper subspace, a contradiction.

The full normalizers of type SL_3(11):2 and SU_3(11):2 preserve rational
nonisotropic lines in the natural Cayley module. Preservation of a line
is the assertion required here; an element in the outer half need not
fix a chosen vector on it. The quaternion subgroup
(SL_2(11) circ SL_2(11)).2 preserves the decomposition into the
three-dimensional trace-zero part of its quaternion algebra and its
four-dimensional complement. These descriptions concern the full
subgroups in this representation, not just their index-two subgroups.
They exclude these maximal subgroups by ordinary F_11-irreducibility.
The rational geometric assertions are borrowed from [W], Sections
4.2.5--4.2.6, and the retained Cayley-module proof.

The remaining small rows 2^3.PSL_3(2), PGL_2(11) and G_2(2) have orders
1,344, 1,320 and 12,096. They cannot contain H. The exceptional envelopes
PGL_2(13) and PSL_2(8):3 would have orders only 2,184 and 1,512 even if
retained without their usual restrictions, so retaining them cannot
weaken this argument. There is no proper subfield subgroup because 11
is prime; the characteristic-two and characteristic-three exceptions
do not apply. The remaining possible row is J_1. Its Sylow 2-subgroups
are elementary abelian of order 8, so J_1 has no element of order 4.
This also contradicts a hypothesis on H. Every maximal overgroup has
been excluded, and H=G. QED.

Only ordinary irreducibility over F_11 was used. Absolute irreducibility
and a computed matrix-algebra dimension are not additional hypotheses.
The lemma is a classical classification corollary; no priority for the
classification, rational geometry or the J_1 fact is claimed here.

3. Irreducibility of the original left endpoint
-----------------------------------------------

For signs s,t in {1,-1}, let

              V_(s,t)={v in V: va=sv and vc=tv}.

Since a and c are commuting involutions in odd characteristic, the four
operators

                 P_(s,t)=(I+sa)(I+tc)/4

are projections with pairwise disjoint images, and their sum is I.
Thus V is the direct sum of the four simultaneous sign spaces.

The complete independently checked AC-space certificate gives their
dimensions as 1,2,2,2. A one-dimensional space over F_11 has one
projective line, and a two-dimensional one has (11^2-1)/(11-1)=12.
The complete projective domains of these four spaces therefore contain
exactly 1+12+12+12=37 lines.

For each of those 37 lines, the independent cyclic-basis consumer
checked a nonzero representative v and seven rows v_0,...,v_6. The first
row is that same representative. Each subsequent row is a fresh image
of an earlier row under one of a,b,c. If A is the square matrix with
these rows, the consumer also checked a supplied right inverse B with
AB=I. Hence the rows are independent and span V. In particular, they
lie in the cyclic submodule vF_11[L], and that cyclic submodule is V.
The certificates were consumed on the disjoint intervals [0,8), [8,16),
[16,24), [24,32), [32,37); their union is the whole 37-line domain.

Lemma 2. The subgroup L acts irreducibly on V over F_11.

Proof. Let W be a nonzero L-invariant subspace. It is stable under a,c,
and hence under each polynomial P_(s,t) in these matrices. Applying the
four projections to a nonzero vector of W shows that W contains a
nonzero vector of at least one V_(s,t). The line through that vector is
one of the complete 37 projective lines just described. Its normalized
representative v belongs to W, since W is an F_11-subspace. All seven
rows of the verified cyclic-basis certificate for v then belong to W,
because they are actual L-word images of v. Those rows span V, so W=V.
This proves irreducibility. QED.

Both completeness statements matter: the AC spaces must be complete,
and every projective line in them must occur in the consumed domain.

4. A size bound from a partial point orbit
------------------------------------------

Lemma 3. The subgroup L has order at least 12,100.

Proof. The independent point-prefix consumer checked that a,c are
nonidentity distinct involutions, ac=ca, and that the four full matrices
I,a,c,ac are distinct. Thus A_0=<a,c> has order 4. It also checked a
nonzero vector u with ua=uc=u. Hence A_0<=L_u.

Starting at this same u, the consumer reconstructed 3,025 vectors. Each
nonroot row is the fresh image of a strictly earlier row under a,b or c;
all full seven-coordinate vectors are distinct. Induction on the parent
indices proves that every reconstructed row belongs to u^L. Therefore
|u^L|>=3,025. Orbit-stabilizer gives

                |L|=|u^L||L_u| >= 3,025*4 = 12,100.

No closure assertion about the stored prefix is required. QED.

The prefix certificate requires 3,024 parent images, as well as the two
fixed-vector identities in the setup. It records the whole parent tree;
no enumeration of the remaining orbit is needed.

5. The order-four witness and the middle subgroup
-------------------------------------------------

The independent word consumer replayed the original-label word

                 w=b c b c b c=(bc)^3

in the same a,b,c endpoint, and checked w^2!=I and w^4=I. Thus w has
exact order 4. The certificate uses the literal sequence of original labels
(1,2,1,2,1,2); thus the relation with bc concerns these original marks.

Lemma 4. The subgroup L contains an element of order 4, and |M|<=24.

Proof. The first assertion is the consumed witness w. Set r=bc. Then
r^12=w^4=I, so the order of r divides 12. Since b,c are involutions,
b r b=r^(-1), and c=b r. Every element of <b,c> therefore has a normal
form r^j or r^j b. It follows that

                    |M|<=2|<r>|<=24.

This is a bound on the actual two-involution subgroup and requires no
identification of R with a named orthogonal group. QED.

Combining Lemmas 2--4 with Lemma 1 yields L=G: the order bound is
12,100>12,096 and the exact order-four witness belongs to L. In
particular, the quartet generates G, since it already contains L.

6. The right endpoint and failure of the intersection property
--------------------------------------------------------------

The independent complete Schreier consumer gives

                         |R|=1,320*1,320=1,742,400.

Here the point orbit is closed under all three original right-endpoint
marks. The verifier reconstructs its 1,320 points and parent lifts,
checks all 3,960 generator edges, derives the selected stabilizer
loops as actual R-words, and closes their subgroup K of order 1,320.
It checks every Schreier loop in K. The stabilizer theorem therefore
identifies K with the full point stabilizer, and orbit-stabilizer gives
the displayed exact order. A truncated orbit, an unclosed stabilizer
search, or a list of selected loops alone would not establish it.
No abstract type of R is needed in the present proof.

For a rank-four marking, the intersection property requires, among
other identities,

       <a,b,c> intersection <b,c,e> = <b,c>.

The left side is L intersection R=G intersection R=R. Lemma 4 gives
|M|<=24, whereas the complete right certificate gives |R|=1,742,400.
Thus R!=M, so this required identity fails. This proves the theorem.

7. Attribution and scope
-------------------------

The maximal-subgroup classification is due to Kleidman. Its complete
list is used through the retained common theory and Nguyen's displayed
pre-elimination list. The rational natural-module descriptions come
from Wilson and the retained Cayley-algebra arguments. The elementary
abelian Sylow 2-structure of J_1 is a prior fact, attributed in the
retained order-four note to Janko, the ATLAS record and the cited modern
primary source. The projection, cyclic-span, orbit-stabilizer, Schreier
and two-involution arguments are standard algebra. The present work
combines them with particular independently checked finite certificates
for the original quartet. It does not claim these general results as
new theorems of classification.

The particular finite ingredients are the complete 37-seed left
cyclic-basis certificates, the partial 3,025-point left certificate,
the exact order-four word, and the complete right orbit/stabilizer
certificate. The arithmetic checks verify those finite identities.
They do not constitute a Lean formalization of the imported
classification or the natural Cayley-model identification.


References
----------

[K] P. B. Kleidman, The maximal subgroups of the Chevalley groups G_2(q)
with q odd, the Ree groups ^2G_2(q), and their automorphism groups,
Journal of Algebra 117 (1988), 30--71,
doi:10.1016/0021-8693(88)90239-6. Classification origin.

[N] H. N. Nguyen, Irreducible restrictions of Brauer characters of the
Chevalley group G_2(q) to its proper subgroups, arXiv:0910.4994v1,
proof of Theorem 4.4, pp. 10--11. The complete list before character-degree
elimination is the relevant statement.

[W] R. A. Wilson, The Finite Simple Groups, retained preliminary text,
Table 4.1 and Sections 4.2.5--4.2.6; Section 5.9.1 for J_1. The published
edition renumbers the Cayley chapter. Exact retained source identities,
separate reviews and finite certificate references are in EVIDENCE.json.
