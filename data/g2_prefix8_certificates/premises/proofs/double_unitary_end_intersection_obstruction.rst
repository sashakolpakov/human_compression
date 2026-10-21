Two proper order-37 ends force an intersection failure
======================================================

Author: Unit (/root/unit_actual_review), 20 October 2026.
Written Source only. No field, matrix, group, model, Reader, predicate,
control, worker, or proposed certificate function was executed for this note.

The reusable conclusion
-----------------------

Let G be the acquired natural split Cayley group G2(11). Let a,b,c,e be
nonidentity involutions with [a,c]=[a,e]=[b,e]=1, a != c, and b != e.
Put L=<a,b,c>, R=<b,c,e>, D=<b,c>.

Suppose EACH end has (i) a verified word of exact order37, and (ii) a
verified common rational invariant line in the actual pure seven-space.
Then L intersect R strictly contains D. Consequently this marking fails
the rank-four intersection property. No exact end-order computation,
subgroup closure, particular value of |bc|, or faithfulness of a newly
constructed small action is needed.

The existing order37/line theorem first places each end in a proper
unitary line stabilizer. The new deductions below identify each entire
end with that stabilizer and compare their orders with a uniform bound
on D. The proof does not assume that a proper subgroup equals a maximal
overgroup. That equality is proved using a separate unitary-subgroup
theorem and the actual commuting involutions.

External structural inputs and their scope
-----------------------------------------

1. The retained generation note f1b6c8a6 and its independent Root review
   use the complete odd-characteristic G2 maximal-subgroup classification.
   Its q11 consequence is: a proper subgroup containing order37 preserves
   the unique rational line fixed by that word, and its full stabilizer
   K is SU3(11):2. It is the natural Cayley-module line stabilizer, not
   an arbitrary representation of an abstract group. The full natural
   G2(11) group has no invariant line, so an end with the verified common
   line is proper before this classification consequence is applied.

2. Write F=SU3(11), Z=Z(F), |Z|=3. The standard finite classical group
   F is perfect. Its natural three-space is over E=F_121. The geometric
   line stabilizer has normal F of index2. An element in its other coset
   acts conjugate-linearly on this three-space, with conjugation x->x^11.
   Equivalently it has the form A followed by this field conjugation in
   a Hermitian basis. This is the usual unitary stabilizer of a nonsplit
   quadratic subalgebra of a Cayley algebra. This standard geometric
   interpretation, perfectness and classical group orders are inherited
   structural theorems; no new actual model identification is asserted.

3. The following specialization of the projective unitary subgroup
   classification is used: every proper subgroup of PSU3(11) containing
   order37 lies in a Singer normalizer of order111. The inverse image
   of that normalizer in F has order333, hence is odd.

   This is checked from Montanucci--Zini, Section2, (I)--(IV) and
   Theorem2.1, printed pp.2--3, arXiv:1804.03398v1. At q11 only the
   Singer row has37 in its order. The other geometric rows involve
   q, q-1, q+1; the remaining listed possibilities have types Hessian,
   PGL2(11), PSL2(7), A6, A7 or order720. None has37. There is no
   proper subfield row because11 is prime. Projective orders are used
   here, including the divisor gcd(3,12)=3; the centre is restored in
   the order333 lift. The full classification is attributed to Mitchell
   and Hartley as in that primary paper, not proved by this note.

   Primary research source inspected directly:
   https://arxiv.org/pdf/1804.03398
   Journal version: https://doi.org/10.1007/s10801-019-00905-7

The retained Wilson book was read first, including the unitary construction
and G2 line-stabilizer discussion. Its exact local locator is
reboot_20261013/F004_recovery_work/wilson_early_book.txt,
633091B/d0af6d76130d73a143e76218c7c66ca0167d06f70d591f9c3482ec8e04fe895f.
The original Mitchell/Hartley papers were not retrieved here. The complete
list is taken from the explicitly identified primary research statement.

Lemma 1: the even kernel of a unitary-normalizer end is full
-----------------------------------------------------------

Let H<=K contain order37 and contain a Klein four group. Set H0=H intersect F.
An element of order37 lies in H0 because K/F has order2. Also H0 contains
a nonidentity involution: the kernel of the map from C2^2 to K/F has
order at least2.

Let pi:F->PSU3(11) be the central quotient. The order37 element retains
order37 under pi because |Z|=3. If pi(H0) were proper, structural input3
would place H0 in an odd subgroup of order333. This contradicts its
involution. Therefore H0 Z=F. Since Z is central, commutators of elements
of H0 Z belong to H0. Perfectness gives F=[F,F]<=H0. Thus H0=F, and
H is either F or K. This argument neither assumes a splitting of the
central cover nor drops its centre.

Lemma 2: three such involutions cannot generate F
------------------------------------------------

Suppose x,z are distinct commuting nonidentity involutions of F, and y
is another nonidentity involution of F. In the natural Hermitian
three-space over E, every such involution has eigenvalue1 of multiplicity1
and eigenvalue-1 of multiplicity2: it is semisimple in odd characteristic,
has determinant1, and is not the identity.

The two fixed lines of x and z are distinct. Each is in the other's
negative eigenspace, since equality of the positive lines would force
x=z. There is an orthogonal common eigenbasis e1,e2,e3, with nonzero
Hermitian diagonal entries alpha_i in F_11. In this basis x,z are
diagonal matrices with entries in {1,-1}.

Let u span the positive eigenspace of y. Its Hermitian norm is nonzero:
the positive and negative eigenspaces of a unitary semisimple involution
are orthogonal and nondegenerate. Rescale ei by the i-th coordinate
u_i when that coordinate is nonzero, and by1 otherwise. This change of
basis need not be unitary. Its new Hermitian diagonal entries are still
nonzero members of F_11, and u now has coordinates epsilon_i in {0,1}.

Take the Hermitian form linear in its first argument. The positive
projection formula gives, for every vector v,

  y(v) = -v + 2 h(v,u) u / h(u,u).

Its entire matrix now has entries in F_11: epsilon_i, alpha_i and
h(u,u)=sum(alpha_i epsilon_i) are in that field and the last scalar is
nonzero. The matrices of x,z are unchanged by the diagonal rescaling.
Thus <x,y,z> consists of F_11 matrices preserving the nonsingular
symmetric form diag(alpha_i); in fact it lies in SO3(11).

In particular it cannot contain order37. A nonidentity order37 matrix
over F_11 needs a nontrivial irreducible constituent of degree6, since
the multiplicative order of11 modulo37 is6. Such a constituent cannot
fit in dimension3. This is the same elementary root-of-unity argument
as the retained unique-line lemma, without an order enumeration.

Combining Lemmas1--2: if H=<x,y,z><=K contains order37 and its two
nonadjacent marks x,z are distinct commuting involutions, then H=K.
Lemma1 permits only F or K, while Lemma2 excludes F. The conclusion
does not require the three-mark intersection property.

Lemma 3: every element of K has order at most132
----------------------------------------------

First consider g in F. Its commuting semisimple and unipotent parts are
powers of g. For a semisimple unitary three-matrix, its eigenvalue
multiset is stable under lambda -> lambda^(-11). If these orbits have
lengths1+1+1,1+2, or3, respectively, determinant1 gives orders dividing
12,120, or111. In the length3 case the product of the eigenvalues is
lambda^(11^2-11+1)=1; in the length2 case lambda^(11^2-1)=1.
These statements also cover repeated semisimple eigenvalues.

For nontrivial unipotent part, the Jordan types are3 or2+1, and its
order is11. Type3 forces scalar semisimple part of order dividing3,
giving total order at most33. In type2+1 the repeated eigenvalue has
norm1 because its multiplicity2 cannot be paired with a different
inverse-conjugate eigenvalue of multiplicity1. Determinant1 determines
the last eigenvalue. The semisimple order divides12, so the total order
is at most132. Hence all orders in F are at most132.

Now let g be in K outside F. On the natural E-space it is A followed
by field conjugation. Its square s=A bar(A) is in F. Furthermore
bar(s)=bar(A) A=A^(-1) s A, so its characteristic polynomial has
coefficients in F_11. A determinant1 unitary three-matrix has polynomial

  t^3 - c t^2 + bar(c) t - 1.

Here c is in F_11. Thus the polynomial factors as

  (t-1)(t^2+(1-c)t+1).

If the quadratic roots are distinct and not1, they are reciprocal. They
either lie in F_11, with orders dividing10, or are a conjugate pair over
F_11 with orders dividing12. If all roots are1, the matrix is unipotent
of order dividing11. The only remaining repeated-root possibility has
roots1,-1,-1, where a size2 Jordan block gives order dividing22. Therefore
|s|<=22 and |g|<=44. Together with the inner case this proves the bound132.
This bound does not assert that any displayed maximum is attained.

The intersection obstruction
----------------------------

Each end in the initial statement contains a Klein four group: <a,c>
or <b,e>. Its verified proper37 line places it in the corresponding
K. Lemmas1--2 therefore show L and R are full unitary normalizers, each
of order

  k = 2 * 11^3 * (11^3+1) * (11^2-1).

The two line stabilizers may be equal or different; no line-distinctness
assumption is needed. The element bc lies in L. Lemma3 gives |bc|<=132.
The two-involution normal form therefore gives |D|<=264.

Using the acquired ambient order

  |G| = 11^6 * (11^6-1) * (11^2-1),

we have the strict rational inequality

  k^2/|G| = 4*(11^2-1)*(11^3+1)/(11^3-1) > 480 > 264.

The standard product-set formula now gives

  |L intersect R| = |L|*|R|/|LR| >= k^2/|G| > 264 >= |D|.

Since D is already a subgroup of both ends, containment is strict. This
is the same intersection obstruction as the retained lower-order note;
its new end-order lower bounds are supplied by the unitary theorem,
not by an actual exact-order algorithm. This proves the opening claim.
The fixed prefix order |ab|=3 is not needed for this deduction.

Narrow application to the retained original prefix8
-------------------------------------------------

The indispensable domain is the acquired original-prefix8 certificate
cases/original_prefix8/output/result.json,513255B/
e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8,
with original_job=[8,4], original labels/end order and full model/frame
transport. This note does not replace or reinterpret its raw catalogue,
orbits, weights, A=G premise or actual standard/actual coordinate maps.

The first returned search report is only INCOMPLETE_WITH_EXPLICIT_UNPAID_ORBITS:
result4886B/d9d5dc7171a3659d278b4df05e63686125242ba2da17f98d84a3b5dad518d713,
journal191639B/58a0c96fdbaec4fd3f0827f88b31ea5a985fd381c9ee5290b9c2918177cfedf8.
An ordinary journal-metadata read cb7c35 counted39(PROPER,PROPER),12 mixed
and484(None,None) among535 unpaid rows. It did not evaluate any matrices.
Those39 are the exact finite prospective scope of this next sufficient leg.
They are NOT declared rejected or accepted by this written assessment.

The smallest future verification is a Source-reviewed extension of the
existing certificate verifier, not a new subgroup-order engine:

* Bind the actual e712 domain and unchanged original ordered (a,b,c,e),
  and recheck all four nonidentity involutions, the required commutations,
  a!=c and b!=e. For left candidates the retained prefix-membership filter
  already supplies c!=a; the independent future verifier must retain it.
* For each exact double-PROPER row, take its two recorded checkpoints.
  Re-evaluate those two actual end words using the unchanged word encoding,
  and check Y!=I, Y^37=I, nonzero fixed row and every generator preserving
  its line. Reuse the existing complete verify_end37 equalities; a tag or
  hash alone is not a new mathematical certificate.
* Join both successful proper37 facts to this theorem, the same acquired
  G2(11)/natural Cayley identification, the actual original lift and the
  specified D=<b,c>. No actual |bc| or exact end orders are required.
* Retain all old journal/output bytes and explicit535 unpaid list. Emit
  separate complete witnesses for the newly verified rows, preserving all
  previous3244 rejections. Root performs actual admission, acquisition,
  closure, independent actual audit, disjoint composition and any adoption.

Before acquisition this theorem itself needs independent written review
and its primary-source premise in the Root Source union. Any focused controls
for the future certificate extension should cover a valid pair of recorded
proper37 witnesses, mixed/missing37 facts refused, wrong ordered/domain
joins refused, and the existing distinct-involution hypotheses. The inner
three-involution and odd Singer-lift arguments need independent written
review; they do not require a new subgroup-discovery control framework.
No controls are implemented or run here.

The484 misses remain inconclusive. The12 mixed rows have only one full
unitary end; this two-end inequality does not reject them. No universal
odd-q rank-four/rank-five nonexistence result, complete prefix closure,
original recovery, manuscript or Lean credit is claimed.

Reused local proof Sources
-------------------------

* g2_11_generation_by_prime_witnesses.tex,
  f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b,
  and g2_11_generation_independent_review.rst: fullG2 overgroups, unique37
  line and proper-unitary dichotomy, including the normalizer factor2.
* acquired_cayley_full_group_bridge.rst,
  a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801:
  exact mathematical model-equality hypotheses; actual retained joins remain.
* invariant_line_lower_order_obstruction.tex: middle dihedral upper bound
  and product-set intersection inequality, without exact-order necessity.
* search_prefix8_end_rejections.py: current proper37 witness schema and
  original-domain binding. No search function is called for this note.

The classification and classical-group construction are attributed inputs.
The basis-rescaling, unitary/semilinear eigenvalue bounds and their assembly
above are elementary written deductions, with no historical novelty claim.
