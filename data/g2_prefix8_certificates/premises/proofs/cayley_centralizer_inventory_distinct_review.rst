Independent mathematical Source review: the Cayley centralizer catalogue
========================================================================

Verdict: qualified mathematical Source PASS. No supported mathematical blocker
was found in Unit's frozen cayley_centralizer_inventory_reduction.rst,
25,604 bytes, SHA256
665de95492ec34b949252c4c5955eba3c997b806f87363a4bc4262031a64a816.
The author Source is unchanged. This is a written proof assessment, not an
acquired catalogue, coordinate certificate, native/Saved result or census.

Exact hypotheses
----------------

The field is finite of odd order. C is a genuine split unital Cayley algebra
with its canonical multiplicative norm and full polar form, and G=Aut_k(C).
The q11 application additionally retains the actual forms/kappa7 normalization,
faithful saved-group frame and full-group identification described in the
acquired-model bridge. Inclusion in an orthogonal group alone is insufficient.
For the original marked orbit quotient, the permitted group A=G must be joined;
otherwise the construction covers finer inner orbits and still owes fusion.
All original marked-prefix guards and terminal generation/IP predicates stay.

1. Full rational quaternion stabilizer
--------------------------------------

For the exact multiplication convention (1), the formula

  (x,y) -> (p x p^-1, q y p^-1),  det(p)=det(q)

is correct. Quaternion conjugation gives bar(p^-1)=p/d and bar(q)q=dI,
so the first product component is p(xz-bar(w)y)p^-1; the second is
q(wx+y bar(z))p^-1. Thus this is an algebra automorphism, not merely an
isometry. An automorphism preserving H is inner on M2(k). If its image
of l is u l, norm preservation gives det(u)=1, and its image of y l is
u p y p^-1 l. Hence q=u p proves surjectivity. Trivial action forces p
scalar and q=p. The kernel is exactly common scalar pairs, and paired
composition is (p,q)(r,s)=(pr,qs).

Equal determinant imposes one k* condition on GL2(k)^2; quotienting common
scalars imposes the second factor q-1. This gives q^2(q^2-1)^2. Determinant
squareclass descends to the quotient. Its square fibre is the central
product of two SL2 groups; the nonsquare fibre is a real second rational
coset and cannot be omitted. This avoids the rational-points/isogeny pitfall.
The finite-field splitting and involution conjugacy steps are justified by
the inherited 4+4 eigenframe lemma and quaternion doubling: the fixed norm
is nondegenerate, finite quaternion algebras split, and a norm-one vector
in the perpendicular complement gives the same doubling parameter.

Dijols, MPIM22-43, Lemma5.1, printed9--10, independently confirms the
classical quaternion-stabilizer/SO4 setting. Its ambient paper is p-adic;
it supplies no finite-field enumeration or substitute for the explicit
rational surjectivity proof here:
https://archive.mpim-bonn.mpg.de/4752/1/mpim-preprint_2022-43.pdf .
Wilson's retained Sections4.2.2--4.2.3, physical116--118, supply the
norm, frame and multiplication facts. No external code is used.

2. Every involution in K, including the nonsquare coset
------------------------------------------------------

Here 14,763 counts Inv(K), K=C_G(a0), not the involutions of all G2(11).
Order dividing two means p^2=q^2=lambda I. In odd characteristic a
nonscalar matrix with scalar square has trace zero. If exactly one matrix
were scalar, equal determinants would give opposite nonzero scalar squares,
which is impossible. Both scalar matrices give identity or a0; every pair
of nonzero equal determinant trace-zero matrices gives a noncentral
involution. Common scaling reduces determinant to 1 or eta, and the only
remaining equivalence is simultaneous negation. This action is free and
never identifies the two determinant squareclasses.

For a trace-zero matrix the equation is x^2+yz=-delta. Separating the
1+epsilon roots for which yz=0 gives n_delta=q(q+epsilon), exactly as in
the note. The two opposite epsilons give

  |Inv(K)|=1+(n_1^2+n_eta^2)/2=q^4+q^2+1.

Each determinant part is one K-conjugacy class: ordinary GL2 conjugacy
is determined by the separable polynomial X^2+delta, and the determinant
of its quadratic centralizer is surjective. Adjusting one conjugator's
determinant therefore yields an equal-determinant conjugating pair.
The centralizer factor is 2(q-epsilon)^2. At q11 the abstract formulas are:

=================  ========  ========  ==========  ==========  ==========
delta              epsilon   n_delta   class size  |Q_delta|   |Inv(Q)|
=================  ========  ========  ==========  ==========  ==========
1                  -1        110       6050        288         147
eta nonsquare      +1        132       8712        200         103
=================  ========  ========  ==========  ==========  ==========

Together with the single central involution these give 14,763. These
are hand-checked algebraic expectations, not an executed finite catalogue.

3. Ordered endpoint types and the full rational torus
-----------------------------------------------------

All nonidentity involutions are rationally conjugate by their split fixed
quaternion algebras and norm-one doubling vectors. After fixing a0, the
two noncentral K classes therefore give exactly two ORDERED commuting
endpoint-pair classes. No endpoint swap is used.

There is also a direct rational-points check of the claimed torus. For
D=k[i_delta], the branch centralizing i_delta consists of

  {(p,q) in D* x D*: N(p)=N(q)}/k*.

It is isomorphic to D^1 x D^1 through

  [p,q] -> (p/bar(p), q/p).

The first map D* -> D^1 has kernel k*, and finite group sizes show it
is onto for BOTH split and field quadratic algebras. Thus every pair
(alpha,beta) lifts by choosing p and setting q=beta p. The kernel is
exactly the common scalars. This verifies the full rational product,
not only its order. The sign frame map i->-i,u->u,v->v has order two
and inverts both coordinates. Hence Q is the stated generalized dihedral
group, E4=T[2], and its involutions are three central elements plus all
h^2 reflections. No unacquired centralizer or odd-order exception occurs.
Eight ordered E8 classes refine these two endpoint classes by four
reflection classes; their unlabelled normalizers are not prefix stabilizers.

4. Original marked-domain and weight logic
------------------------------------------

For rank4, prefix(a,d,b) fixes exactly S=C_G(a,b,d) inside Q. Every final
c commutes with a, so the raw domain is the entire J=Inv(C_G(a)); requiring
c in Q would wrongly impose commutation with adjacent d. Filtering J and
taking complete S-orbits preserves all fixed-prefix invariant predicates.

For rank5, prefix(a,e,b) has exact S=C_G(a,b,e). The fourth mark's distant
requirements are precisely [d,a]=[d,b]=1, so D_b={d in J:[d,b]=1} is
complete without constructing C_G(a,b). After choosing d, S_d is exactly
the remaining prefix stabilizer. The final middle mark c commutes with
only the fixed distant endpoints a,e, giving Inv(Q). Complete S_d-orbits
with every unchanged guard/terminal predicate reproduce the original
marked orbit cover. Omitting the central E4 elements is legitimate only
when the actual outside-four-mark guard supplies their rejection.
No assumption that b,d normalize an alternating frame is introduced.

An actual finite orbit proof must check its complete index action,
disjointness and coverage; a weight sum alone cannot establish completeness.
For right conjugation, orbit size is |S|/|C_S(x^g)| and the corresponding
old double-coset size is |C_Q(x)| times that orbit size. Equation(16) is
therefore correct. The direct-orbit contract avoids inventing a missing
C_G(a,b) class factor. Old indexed inventories require an explicit
old-index/new-orbit map and compatible weights; regenerating an ordering
never pays an old index or transports an old rejection automatically.

Exact remaining obligations and limits
--------------------------------------

A real application still needs one acquired standard-to-current Cayley
frame/basis with exact norms/products/orthogonalities and nonsingular basis,
the literal ordered endpoint/prefix transporter, and all actual original
A/model/frame/Binder/phi/mu joins. RIGHT_ROW v_new=v_old R gives
A_new=R^-1 A_old R as stated. A known matrix's induced full paid line-domain
action or a verified word lift remains necessary to emit original
permutations; checking eight line images alone is insufficient for an
arbitrary proposed matrix. The algebra-automorphism proof supplies
membership only after the full-group join.

The catalogue, endpoint models, stabilizer filters and orbit/index/weight
certificates have not been acquired by this note. No coordinate field,
model or group routine was executed in this review. All accepted positive
tuples and previously closed indices must be retained without duplicate
credit. Proper-middle/end conditions, full rank4-end string/IP, maximal
parabolic intersections and exact full generation remain owed at every
unpaid candidate. Actual native/strict/independent review/Root composition,
resource fit and any larger A fusion remain independent acquisition duties.
There is no universal rank5 nonexistence, q8, whole-original, Lean, new
census count, speed, memory or completion conclusion.

Authorship and execution boundary
---------------------------------

Author of the reviewed note: /root/unit_actual_review. Independent reviewer:
/root/c5_terminal_audit. C5 authored the earlier ordered-E8 proof, tensor
normalization theorem/verifier and related integration/reviews. Those
retained premises are ancestry, not independently reacquired arithmetic.
The present paired rational centralizer, involution classification and
stabilizer-refinement reasoning were checked independently in writing.
Only ordinary small Source reads/hashes and this report write were executed;
no proposed, finite-field, matrix, group, Reader, model, test, control or
scientific computation or state edit occurred. Author bytes are unchanged.
