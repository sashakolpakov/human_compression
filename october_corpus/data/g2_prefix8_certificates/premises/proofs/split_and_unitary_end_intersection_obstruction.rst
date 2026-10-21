Split and mixed line-stabilizer ends in G2(11)
=============================================

Author: C5 (/root/c5_terminal_audit), 20 October 2026.
Written mathematical Source only. No finite-field, matrix, group, word,
model, Reader, predicate, control, worker or proposed function was run.
All earlier Sources and acquired evidence remain unchanged.

Statement with exact structural premises
-----------------------------------------

Let G be the actual natural split Cayley group G2(11). Let a,b,c,e be
nonidentity involutions with

  [a,c]=[a,e]=[b,e]=1,  a!=c,  b!=e.

Put L=<a,b,c>, R=<b,c,e>, D=<b,c>. Each end must have one of the
following two separately established types in this SAME natural action.

S: It is contained in a specified full split quadratic-line stabilizer
   K_S=SL3(11):2 and contains an element of exact order19.
U: It is contained in a specified full nonsplit quadratic-line stabilizer
   K_U=SU3(11):2 and contains an element of exact order37.

In type S, the normal SL3 acts naturally on a three-space and dually
on its dual; the other coset induces the inverse-transpose graph
automorphism. In type U, the normal SU3 is the full natural Hermitian
group over F_121 and the other coset acts conjugate-linearly. These
are natural geometric identifications, not merely abstract names.

Then each end is its ENTIRE specified stabilizer, and L intersect R
strictly contains D. Thus the marking fails rank-four IP. The two
stabilizers need not be distinct. No rank-three IP, prescribed adjacent
order or exact subgroup-order algorithm is assumed. The same conclusion
holds with any independently certified ambient-order upper bound no
larger than 11^6(11^6-1)(11^2-1).

The unitary-unitary case is already the frozen d7e theorem. The new
written deductions here supply the split end and the split-split and
split-unitary comparisons. They do not establish any actual new witness,
row, orbit, original lift, prefix completion or census result.

Structural authorities and the complete linear list
----------------------------------------------------

The retained Wilson text, sections 4.2.3 and 4.2.6, supplies the Cayley
group order and natural line stabilizers. Its split stabilizer preserves
the natural/dual three-space pair; its outer half swaps these spaces.
The induced automorphism is the usual inverse transpose after choosing
dual bases. The unitary structure and all U-case deductions are taken
from double_unitary_end_intersection_obstruction.rst (d7e540f9) and
Root's independent review (591ca8e3), whose exact hypotheses remain.

For the linear subgroup classification, I read Nick Gill,
``PSL(3,q) and line-transitive linear spaces'', arXiv:math/0603293v3,
section 3.1, Theorem19, printed page7:
https://arxiv.org/pdf/math/0603293 . Its complete containing list is
attributed to Mitchell, Hartley, Bloom and Kleidman. It includes
parabolics, monomial and Singer normalizers, proper linear subfields,
unitary subfields, A6, the two listed Hessian types, conic SO3, and
PSL2(7). At11 the proper subfield and unitary-subfield cases do not
exist. Allowing listed exceptional types even when an existence
condition fails only enlarges the list harmlessly. This is a primary
research statement of the imported classification, not a new proof of it.

The original odd-characteristic references are H.H. Mitchell,
Trans. Amer. Math. Soc.12(1911),207--242, DOI
10.1090/S0002-9947-1911-1500887-3, and D.M. Bloom,
Trans. Amer. Math. Soc.127(1967),150--178, DOI
10.1090/S0002-9947-1967-0214671-1. Their full original texts were not
retrieved: AMS access refused and JSTOR returned the Mitchell metadata
page. No claim of independent retrieval of either original is made.
The actual complete list used here is the directly read Gill theorem.

1. An order19 element and a Klein four force SL3(11)
---------------------------------------------------

Write F=SL3(11). Its centre has order gcd(3,10)=1, so F=PSL3(11).
The complete list just identified gives the following containing
orders, sufficient even without applying every existence restriction:

  parabolics:       11^3*(11+1)*(11-1)^2;
  monomial group:   6*(11-1)^2;
  Singer normalizer:3*(11^2+11+1)=399;
  conic group:      |PGL2(11)|=11*(11^2-1);
  constants:        A6, 3^2:SL2(3), 3^2:Q8, PSL2(7).

Only the Singer row can contain19. In particular its FULL normalizer
has order399 and is odd. The cyclic Singer subgroup has order133;
one must not discard the normalizing factor3. Since11 is prime and
not a square, neither a proper linear subfield nor a unitary subfield
can contribute another case. Consequently every proper subgroup of F
containing19 lies in an odd subgroup.

Let H<=K_S contain19 and a Klein four, and put H0=H intersect F.
The odd-order element belongs to H0. The restriction of H->K_S/F=C2
to the Klein four has a kernel of order at least2, so H0 contains an
involution as well. If H0 were proper, the preceding odd-normalizer
consequence would be impossible. Thus H0=F, and H is F or K_S.
There is no central-cover loss here, because the centre is trivial.
Equivalently F is simple and perfect; neither a central complement nor
an unproved splitting is used to reach the conclusion.

2. The missing linear half-turn argument
----------------------------------------

It is NOT enough to repeat the Hermitian basis-rescaling proof inside
SL3. Three arbitrary linear involutions need not initially preserve
any given Hermitian or symmetric form. The order19 witness supplies
the needed irreducibility, after which a common symmetric form follows.

Suppose H=<x,y,z> is contained in F and x,z are distinct commuting
nonidentity involutions. Odd characteristic and determinant one give
positive dimension1 and negative dimension2 for each. There is a
simultaneous eigenbasis with x,z diagonal, their positive coordinate
lines distinct. Use row vectors throughout this paragraph.

Write the third half-turn as

  y=-I+2*ell*u/(u*ell),

where u is a nonzero ROW spanning its positive line and ell is a
COLUMN covector with u*ell!=0. This formula follows from the rank-one
positive projection (I+y)/2; it requires no preserved form in advance.

A nonidentity order19 matrix over F_11 is irreducible in dimension3.
Indeed ord_19(11)=3: 11^3=1 modulo19, whereas 11 and 11^2 are not1.
In characteristic11 an order19 matrix is semisimple, and every
nontrivial irreducible constituent has degree3. The whole natural
three-space must therefore be that constituent. Any subgroup containing
this element is irreducible on the three-space as well.

If u_i=0, the coordinate hyperplane v_i=0 is preserved by y and by
the diagonal x,z, contradicting irreducibility. If ell_i=0, the
coordinate line spanned by e_i is preserved by all three, again a
contradiction. Thus every u_i and ell_i is nonzero. Set

  C=diag(ell_1/u_1,ell_2/u_2,ell_3/u_3),
  B(v,w)=v*C*w^T.

This is a nonsingular symmetric form over F_11 and
B(v,u)=v*ell, B(u,u)=u*ell!=0. Therefore y is minus the identity
plus twice the B-orthogonal projection onto u. It preserves B, as
do the diagonal sign matrices x,z, and all have determinant one.
Hence H<=SO(B).

Every determinant-one isometry in odd dimension3 has eigenvalue1:
its multiset of eigenvalues is invariant under inversion, and its
determinant is1. Equivalently its reciprocal cubic has the factor
t-1. This is incompatible with the irreducible order19 element above.
Thus such a three-half-turn group inside F cannot contain19.

Combining parts1--2, an end in K_S with an actual19 witness and the
stated distinct commuting involutions is the full K_S, not its
index-two SL3. This argument proves the necessary implication without
claiming that arbitrary three involutions generate the normalizer.

3. Orders in the split normalizer
---------------------------------

For g in F, separate its commuting semisimple and unipotent parts.
The semisimple characteristic polynomial has degree pattern1+1+1,
2+1 or3. Determinant one gives respective order divisors

  10, 11^2-1=120, 11^2+11+1=133.

In the degree-three case, an eigenvalue lies in F_(11^3) and its norm
to F_11 is1. In degree2+1, the third eigenvalue is determined by the
norm of the degree-two eigenvalue, so no extra independent factor is
needed. All split eigenvalues have orders dividing10.

If the unipotent part is nontrivial, its Jordan type is3 or2+1 and
its order is11. A size-three block forces scalar semisimple part;
determinant one and gcd(3,10)=1 force that scalar to be1. In type2+1
the repeated semisimple eigenvalue lies in F_11^*, and the remaining
one is its inverse square. The semisimple order divides10, so the
total order is at most110. Thus every g in F has order at most133.

Let g be in the graph coset of K_S. Relative to the specified natural
identification write g=A*tau, A in F, tau(A)=A^(-T). Then

  s=g^2=A*A^(-T),
  s^(-T)=A^(-T)*A=A^(-1)*s*A.

The matrix s is therefore similar to its inverse transpose. Its
determinant is1, so its characteristic polynomial is

  t^3-c*t^2+c*t-1=(t-1)(t^2+(1-c)*t+1).

The remaining distinct roots are reciprocal, with orders dividing10
if split over F_11 or12 if conjugate over F_121. The repeated-root
possibilities are all-one unipotent, of order dividing11, or
1,-1,-1 with a possible size-two Jordan block, of order dividing22.
Consequently |s|<=22 and |g|=2|s|<=44. The equality uses the even
order of g in the nontrivial coset. In particular every element of
K_S has order at most133; no maximum-attainment claim is needed.

For K_U retain the separately proved q11 bounds: inner order at most132,
outer order at most44, so every element has order at most132. The
inverse-transpose calculation above is the SPLIT graph calculation;
it is not a claim that graph action and unitary field conjugation
are the same operation.

4. Split-split and mixed intersections
---------------------------------------

Put

  k_S=2*11^3*(11^3-1)*(11^2-1),
  k_U=2*11^3*(11^3+1)*(11^2-1),
  g0=11^6*(11^6-1)*(11^2-1).

Both ends are full specified stabilizers, by parts1--2 for S and by
d7e for U. If both are split, bc has order at most133 and
|D|<=266. But

  k_S^2/g0=4*(11^2-1)*(11^3-1)/(11^3+1)
          =480-960/1332 >479>266.

If one is split and one unitary, bc belongs to the unitary end,
so |D|<=264, while

  k_S*k_U/g0=4*(11^2-1)=480>264.

For two unitary ends d7e already gives k_U^2/g0>480>264.
The elementary two-involution normal form supplies |<b,c>|<=2|bc|
in every case. Even b=c or a smaller middle subgroup only improves
this upper bound. The product-set identity gives

  |L intersect R|=|L|*|R|/|LR|>=|L|*|R|/|G|>|D|.

Since D is contained in both ends, the claimed containment is strict.
Neither distinct stabilizers nor end-parabolic IP are used. The
commutation [a,e]=1 records the intended string setting but is not
needed for the final numerical comparison.

Exact future certificate duties; no new application result
----------------------------------------------------------

For type S, a future sufficient certificate must bind an actual word
in the actual ordered end with Y!=I and Y^19=I, and establish that
the entire end is in the specified natural split stabilizer. One
geometric route is a nonzero preserved pure line with canonical norm
N(v)!=0 and -N(v) a square, so that <1,v> is a split quadratic
subalgebra. The full line-stabilizer theorem supplies K_S. This uses
the ACQUIRED canonical norm, not an arbitrary scalar multiple of an
invariant bilinear form. Checking a common line without its type or
the actual natural-model join is not this certificate.

Type U retains the exact existing two-end37 certificate duties and
natural unitary-stabilizer theorem. A new type or mixed certificate
must recheck all four nonidentity involutions, both distinct commuting
end pairs and the same ordered middle D=<b,c>; it must retain the
actual original prefix/index/label and native lift/frame/A=G joins.
No unproved surrogate action or altered catalogue index is allowed.

This theorem does NOT say that a moved order19 fixed line certifies
the full G2(11). The J1 alternative in the retained G2 classification
prevents that inference. Here the relevant containment is positively
established by the specified natural line stabilizer. It is also not
enough to infer an exact full end from a merely plausible maximal
overgroup; parts1--2 are what prove that equality.

The complete original e712 catalogue/orbit/weight and original-domain
authorities remain borrowed acquired premises. This note evaluates no
new19 word, line type, matrix, row or end; it asserts no number of
newly covered rows among any currently unpaid set. Old missing-word,
mixed or NO_PROPOSAL records remain inconclusive until a new actual
certificate discharges the stated hypotheses. The separate39 verifier
and any prospective496 complement remain their own actual/acquisition
and adoption obligations. No output or state is changed here.

The proof is deliberately restricted to q11. A naive generic
ord_ell(p)=3n substitution would require, among other issues, the
proper unitary-subfield alternative when q is a square. No general
odd-q split theorem or new conjecture/completion claim is asserted.

Reused fixed mathematical Sources
----------------------------------

* double_unitary_end_intersection_obstruction.rst, 14424B,
  d7e540f9ad61fbacf1f18ca1a184a0638581e6693a972a7705febd44e21c7126.
* double_unitary_end_intersection_independent_review.rst, 4341B,
  591ca8e3a02c9213789f926c8a4fd1f67b5672c0fdeb12f4e33a10f4009047f7.
* g2_11_generation_by_prime_witnesses.tex, 26437B,
  f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b.
* acquired_cayley_full_group_bridge.rst, 9716B,
  a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801.
* The retained wilson_early_book.txt, 633091B,
  d0af6d76130d73a143e76218c7c66ca0167d06f70d591f9c3482ec8e04fe895f,
  at research/leemans/reboot_20261013/F004_recovery_work/.

The subgroup list and natural classical/Cayley constructions are
attributed structural inputs. The irreducibility/form argument,
split graph-square bound and assembled intersection deductions are
written elementary proofs here, without a historical novelty claim.
Independent mathematical review and any later actual certificate
implementation/acquisition remain separate from this Source preparation.
