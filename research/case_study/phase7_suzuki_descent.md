# Field descent and one torus give Suzuki geometries in every rank

10 October 2026. Proposed proofs. This note uses classical Lang–Steinberg
descent and Suzuki subgroup theory explicitly; it does not assume the
candidate completeness claims disproved by the phase-six example.
The earlier notes and executed certificates remain unchanged.

## 1. Main statements

The rank-four configuration in
[phase6_suzuki_realization.md](phase6_suzuki_realization.md) is a
flag-transitive geometry. It is firm and residually connected as well as
RWPRI. This closes the geometric gap left in that note: the argument
below establishes the common-point property for every flag, without
enumerating the ambient \(\operatorname{Sz}(2^{105})\).

There is also an unconditional family in every rank. Define, for positive
odd \(d\),

\[
\tau_d=2^d+1-\big((1+i)^d+(1-i)^d\big).
\tag{1}
\]

Thus \(\tau_1=1,\tau_3=13,\tau_5=41,\tau_7=113,\tau_9=481\).
Equivalently, \(\tau_d=2^d+1-\epsilon_d2^{(d+1)/2}\), where
\(\epsilon_d=1\) for \(d\equiv1,7\pmod8\), and
\(\epsilon_d=-1\) for \(d\equiv3,5\pmod8\).

**Theorem A.** Fix odd \(e\ge3\), and any distinct odd primes
\(a_1,\ldots,a_k\) not dividing \(\tau_e\). For each \(i\), choose any
prime divisor

\[
\ell_i\mid \tau_{ea_i}/\tau_e.
\]

These quotients are integers greater than one. Their prime divisors are
coprime to \(\tau_e\) and distinct between different indices.
Put \(n=e\prod_i a_i\), \(m=\tau_e\prod_i\ell_i\), and
\(G=\operatorname{Sz}(2^n)\). There are simultaneous standard subfield
subgroups

\[
S_i=\operatorname{Sz}(2^{n/a_i})
\]

and one subgroup \(K=C_m:C_4\) for which
\(\Gamma(G;S_1,\ldots,S_k,K)\) is a thick, residually connected,
flag-transitive RWPRI geometry of rank \(k+1\).
The theorem provides explicit intersection formulas in Section 6.

In particular, fixing \(e=3\) and choosing any \(k\) distinct odd primes
other than 13 gives a geometry of rank \(k+1\). No conjecture about
infinitely many prime values of Suzuki torus orders is used.

For example, with \(e=3\) and relative field primes \(3,5,7,11\), one can
choose \(\ell_i=37,41,113,2113\). This gives a rank-five example over
\(\mathbb F_{2^{3465}}\), described by the same formulas as the smaller
ones. Enumerating this field or group is unnecessary.

The construction specializes the nonsplit-torus pattern in Construction 9
of L110, Leemans,
[*The residually weakly primitive pre-geometries of the Suzuki simple
groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995),
pp.17–18. It supplies simultaneous embeddings and flag transitivity for
this family. It is not a replacement classification of all the paper's
configurations or all relative positions of its subgroup types.

Two reusable principles do most of the geometric work:

* compatible cosets of fixed subgroups of coprime field automorphisms
  have a common point, by Lang descent;
* a subgroup with independent coset coordinates can be added as another
  type without losing that common-point property.

## 2. Cyclic descent and subfield-coset Helly

Let \(\mathbf H\) be a connected algebraic group over an algebraic closure
of a finite field, and let \(F\) be a Steinberg endomorphism. We use
Lang–Steinberg surjectivity: every \(u\in\mathbf H\) has the form
\(x^{-1}F(x)\). This is retained classical theory, not reproved here;
see, for example, Harper,
[*Totally deranged elements of almost simple groups and invariable
generating sets*](https://doi.org/10.1112/jlms.12935), Section 2.2 and
equation (2.1), which use it for Steinberg endomorphisms, including the
very twisted groups.

**Lemma B: finite cyclic descent.** Set \(G=\mathbf H^{F^m}\), and let
\(\sigma=F^d|_G\), where \(d\mid m\) and \(h=m/d\).
If \(u\in G\) satisfies

\[
u\,\sigma(u)\cdots\sigma^{h-1}(u)=1,
\]

then \(u=x^{-1}\sigma(x)\) for some \(x\in G\).

Indeed, apply Lang–Steinberg to \(F^d\) on the connected algebraic group:
choose \(x\in\mathbf H\) with \(u=x^{-1}F^d(x)\).
The displayed norm telescopes to \(x^{-1}F^m(x)\).
Its being one proves \(x\in G\), which is precisely the finite-field
conclusion needed. No coprimality with the characteristic is required.

Equivalently, in \(G\rtimes C_h\), with the specified cyclic action, every
element projecting to a generator and having order \(h\) is
\(G\)-conjugate to that generator. The cyclic factor here may be treated
as an abstract group of order \(h\), so no faithfulness issue is hidden.

**Theorem C: coprime subfield-coset Helly.** Suppose \(b_1,\ldots,b_k\)
are pairwise coprime divisors of \(m\). Define

\[
S_i=\mathbf H^{F^{m/b_i}}\le G=\mathbf H^{F^m}.
\]

For any selection of indices, if the left cosets \(g_iS_i\) intersect
pairwise, then their total intersection is nonempty.

Proof. Work in \(E=G\rtimes\langle f\rangle\), with \(f\) an abstract
element of order \(m\) acting as \(F|_G\), and put \(f_i=f^{m/b_i}\).
Associate to \(g_iS_i\) the element

\[
c_i=g_i f_i g_i^{-1}.
\]

This association is well defined: \(S_i=C_G(f_i)\).
If \(g_iS_i\) and \(g_jS_j\) meet at \(y\), both \(c_i,c_j\) are
conjugated from \(f_i,f_j\) by \(y\). Hence they commute.
Their orders \(b_i\) are pairwise coprime, so the group \(D\) that they
generate is cyclic of order \(b=\prod_i b_i\). Its projection to
\(\langle f\rangle\) is an isomorphism onto
\(\langle f^{m/b}\rangle\).

Let \(c\) be its unique element projecting to \(f^{m/b}\).
Write \(c=u f^{m/b}\). Since \(c^b=1\), its coefficient \(u\) satisfies
the norm condition in Lemma B, with \(d=m/b\). Consequently \(D\) is
conjugate by an element \(x\in G\) to
\(\langle f^{m/b}\rangle\). The conjugating element may be oriented so
that

\[
c_i=x f_i x^{-1}\quad\hbox{for every }i.
\]

There is no ambiguity of generators: conjugation by \(G\) acts trivially
on the quotient \(E/G\), and the projection is injective on \(D\).
Thus \(g_i^{-1}x\) centralizes \(f_i\), so \(x\in g_iS_i\) for every
\(i\). This proves the theorem.

For Suzuki groups take \(\mathbf H=\operatorname{Sp}_4(\overline{\mathbb
F}_2)\) and its standard exceptional Steinberg endomorphism \(\rho\),
with \(\rho^2=\phi_2\), ordinary binary Frobenius. For positive odd \(d\),
\(\mathbf H^{\rho^d}=\operatorname{Sz}(2^d)\) in compatible standard
coordinates. This is the classical Suzuki construction; see
De Medts–Naert, [*Suzuki–Ree groups as algebraic groups over
\(\mathbb F_{\sqrt p}\)*](https://arxiv.org/abs/1904.10741), Section 2,
for the exceptional endomorphism and its square.
On \(\mathbf H^{\rho^n}\), \(n\) odd, \(\rho\) and ordinary binary
Frobenius generate the same cyclic field-automorphism group.
Taking \(F=\rho^e\), \(m=\prod_i a_i\), therefore gives Theorem C for
the standard \(S_i\) in Theorem A.

## 3. Adding a type by independent coset coordinates

The following lemma is purely group theoretic. In particular it does not
identify a coset set with a quotient group.

**Lemma D.** Let \((S_i)\) be a typed coset family in a group \(G\) with
the common-point property of Theorem C. Suppose \(K\le G\), and put
\(H_i=K\cap S_i\). If the set map

\[
K\longrightarrow\prod_i K/H_i,\qquad
k\longmapsto(kH_i)_i
\tag{2}
\]

is surjective, then the enlarged typed coset family \((S_i,K)\) also
has the common-point property.

A flag not containing a \(K\)-coset is handled by the original property.
Otherwise translate its \(K\)-coset to \(K\). Each other coset meets
\(K\), so it is \(k_iS_i\) with \(k_i\in K\), and its intersection with
\(K\) is \(k_iH_i\). Surjectivity in (2) supplies a common element.
Partial selections of types cause no problem: assign arbitrary cosets to
the unused coordinates. Every flag therefore has a common representative
and extends to a full standard-chamber translate. This proves the
geometry axiom and flag transitivity.

A convenient sufficient condition is

\[
K=(V_1\times\cdots\times V_k)\rtimes B,\qquad
H_i=\Big(\prod_{j\ne i}V_j\Big)\rtimes B,
\tag{3}
\]

where \(B\) preserves each direct factor. The restricted set map from
\(\prod_iV_i\) to the product of coset sets is a bijection: its \(i\)-th
coordinate is just the \(V_i\)-coordinate. Neither \(H_i\) nor \(B\)
needs to be normal in \(K\).

This already settles the phase-six rank-four example. There
\(V=C_{13}\times C_{41}\times C_{113}\), \(B=C_4\), and the exact
certificate gives precisely (3). The three standard subfield coset
types satisfy Theorem C. Hence the four-type coset system is a
flag-transitive geometry. Its RWPRI proof was already given there.
Firmness and residual connectedness also follow from the argument in
Section 7 below, with base \(\operatorname{Sz}(2)\) and the three full
prime-order tori 13, 41, 113.

## 4. One binary algebra, compatible tori in every odd degree

Here is the uniform construction behind the field-compatible cyclic
groups, rather than an extrapolation from small computations.

Use the binary matrices \(M,r\) displayed in the immutable phase-six
note, where \(M^4+M+I=0\), \(r=U(1,0)\), \(|r|=4\), and
\(r^{-1}Mr=M^2\). The polynomial \(X^4+X+1\) is irreducible.
Thus \(\mathbb F_2[M]\) is the field with sixteen elements.

The exact order-13 matrix \(a\in\operatorname{Sz}(8)\) found in the
phase-six seed commutes with \(M\). Since the multiplicative order of
8 modulo 13 is four, every nontrivial order-13 matrix in dimension four
over \(\mathbb F_8\) has irreducible minimal polynomial of degree four.
In particular \(a\) has four distinct eigenlines. The same is true of
\(M\): its degree-four binary polynomial remains irreducible over
\(\mathbb F_8\), since \(\gcd(4,3)=1\).
Both therefore generate the same degree-four algebra over
\(\mathbb F_8\), and their commuting regular matrices have the same general
linear centralizer. Put

\[
\mathbf T=C_{\mathbf H}(M)=C_{\mathbf H}(a).
\]

As the centralizer in \(\operatorname{Sp}_4\) of this regular semisimple
element, \(\mathbf T\) is a connected maximal torus of dimension two.
This can also be seen directly in the eigenbasis of \(a\): its
symplectic eigenvalue pairs are inverse pairs, and the centralizer
consists of the corresponding two independent diagonal coordinates.

Because \(M\) is binary, \(\phi_2\) preserves \(\mathbf T\).
Because \(\rho^3(a)=a\), one has
\(\rho(a)=\rho^4(a)=\phi_2^2(a)\). This is another regular element of
\(\mathbf T\), so \(\rho\) also preserves \(\mathbf T\).

Let \(B\) be the integral endomorphism induced by \(\rho\) on the
rank-two character lattice of \(\mathbf T\).
Binary Frobenius permutes the four eigenlines of \(M\) in a four-cycle,
since its minimal polynomial has degree four over \(\mathbb F_2\).
The corresponding action on the four symplectic weights
\(\{\chi_1,\chi_2,-\chi_1,-\chi_2\}\) is a rotation \(w\) of order four,
with trace zero and determinant one. Therefore

\[
B^2=2w,\qquad
(\operatorname{tr} B)^2-2\det B=0,\qquad(\det B)^2=4.
\]

Integrality forces \(\det B=2\) and
\(\operatorname{tr}B=\pm2\).
The remaining sign is fixed by a tiny exact binary check:
\[
\mathbf T^\rho=C_{\operatorname{Sz}(2)}(M)=1.
\]
The new seed checker verifies this against all twenty matrices of
\(\operatorname{Sz}(2)=\langle r,w\rangle\).
Equivalently, its unique order-five subgroup is generated by \(r^2w\),
which does not commute with \(M\).

For a torus, the fixed-point count for an endomorphism whose character
matrix is \(B\) is \(|\det(I-B)|\) when this determinant is odd.
This particular count needs only Smith normal form: diagonalizing
\(I-B\) over the integers turns its kernel on
\((\overline{\mathbb F}_2^\times)^2\) into a product of groups of roots
of unity of odd orders. Here the two sign choices give one or five
fixed points, so the check selects \(\operatorname{tr}B=2\).

The eigenvalues of \(B\) are consequently \(1+i,1-i\).
The same Smith-normal-form argument gives, for every positive odd \(d\),

\[
|\mathbf T^{\rho^d}|=\det(I-B^d)
=2^d+1-\big((1+i)^d+(1-i)^d\big)=\tau_d.
\]

These are the nonsplit Suzuki torus orders. We retain the classical
fact that such finite tori are cyclic and their normalizers in the
simple Suzuki groups have order \(4\tau_d\) and are maximal.
Write \(T_d=\mathbf T^{\rho^d}\).
The binary \(r\) normalizes \(\mathbf T\), belongs to every
\(\operatorname{Sz}(2^d)\), and has order four. Thus
\(\langle T_d,r\rangle=T_d:C_4\) is that full normalizer for \(d>1\).
For \(d=1\), \(T_1=1\) and \(\langle r\rangle=C_4\) has index five
in \(\operatorname{Sz}(2)\); the simple-group normalizer assertion is
not being applied in this exceptional case.

The benefit is simultaneous position. For all positive odd \(a,b\),

\[
T_a\cap T_b=T_{\gcd(a,b)},\qquad
\gcd(\tau_a,\tau_b)=\tau_{\gcd(a,b)}.
\tag{4}
\]

The first equality follows from the fixed-point equations and Euclid's
algorithm. For the second, place both cyclic groups in
\(T_{\operatorname{lcm}(a,b)}\), then use uniqueness of subgroups of
each order in a cyclic group.

### Exact matrix convention for the exceptional endomorphism

There is an elementary way to check that the exceptional endomorphism
used above matches the phase-six matrices. Take the symplectic form
with antidiagonal matrix \(J\). On the exterior square of the natural
module, quotient the kernel of symplectic contraction by its invariant
line \(\langle e_1\wedge e_4+e_2\wedge e_3\rangle\).
The exterior-product pairing descends to a nondegenerate alternating
form on this quotient, with antidiagonal matrix in the basis below.
In the quotient basis

\[
e_1\wedge e_2,\ e_1\wedge e_3,\ e_2\wedge e_4,\ e_3\wedge e_4,
\]

the induced matrix \(\rho(g)\) consists of the \(2\times2\) minors
whose row and column pairs are \(12,13,24,34\).
This is the exceptional isogeny in the given coordinates.
For four independent variables, let
\[
u(a,A,b,B)=
\begin{pmatrix}
1&0&0&0\\a&1&0&0\\aA+b&A&1&0\\
a^2A+ab+B&b&a&1
\end{pmatrix}.
\]
Direct polynomial multiplication gives
\[
\rho(u(a,A,b,B))=u(A,a^2,B,b^2).
\tag{7}
\]
Consequently \(\rho^2\) is entrywise squaring on this full unipotent
group. The diagonal matrix
\(\operatorname{diag}(x,y,y^{-1},x^{-1})\) maps to
\(\operatorname{diag}(xy,x/y,y/x,(xy)^{-1})\), giving the same square;
the antidiagonal \(w\) is fixed. These groups generate the symplectic
group, so the identities recover \(\rho^2=\phi_2\).
The exterior-square construction makes \(\rho\) a group homomorphism;
the polynomial checks are not a test of that property on a sample.

Setting \(A=a^\theta,B=b^\theta\), with \(\theta^2=2\) on the
finite field, equation (7) becomes exactly
\(\rho(U(a,b))=U(a,b)^\theta\), with entrywise exponent on the right.
The phase-six diagonal and antidiagonal generators satisfy the same
fixed-point relation. This binds the usual exceptional Suzuki
construction to those particular matrices. The new checker proves (7)
as an identity of sparse polynomials over \(\mathbb F_2\), checks the
symplectic identity in four independent variables, and checks the
diagonal identities as Laurent-polynomial identities. It also directly
verifies \(\rho(a)=a^{(4)}\), \(\rho^3(a)=a\), and all twenty binary
centralizer tests for the actual seed.

## 5. The prime choices exist without a prime-value conjecture

Let
\(\tau'_d=2^d+1+((1+i)^d+(1-i)^d)\). For odd \(d\),

\[
\tau_d\tau'_d=2^{2d}+1,\qquad
\gcd(\tau_d,\tau'_d)=1.
\tag{5}
\]

Indeed the trace square is \(2^{d+1}\), while the difference between
the two odd factors is a power of two.

Fix odd \(e\ge3\) and an odd prime \(a\nmid\tau_e\).
Since \(T_e\le T_{ea}\), \(\tau_e\mid\tau_{ea}\).
The quotient is greater than one from (1), for example by bounding
\(\tau_{ea}\) below by \(2^{ea}+1-2^{(ea+1)/2}\) and
\(\tau_e\) above by \(2^e+1+2^{(e+1)/2}\).

If an odd prime \(\ell\mid\tau_e\), the elementary lifting-the-exponent
identity applied to \((2^{2e})^a+1\) gives

\[
v_\ell(2^{2ea}+1)=v_\ell(2^{2e}+1)+v_\ell(a)
=v_\ell(\tau_e).
\]

The last equality uses \(a\nmid\tau_e\) and (5). Divisibility
\(\tau_e\mid\tau_{ea}\) forces exactly that same valuation in
\(\tau_{ea}\). Thus
\[
\gcd(\tau_{ea}/\tau_e,\tau_e)=1.
\]
Every prime divisor of the nontrivial quotient is therefore new.
For distinct \(a_i,a_j\), equation (4) gives
\(\gcd(\tau_{ea_i},\tau_{ea_j})=\tau_e\), so selected new primes
cannot repeat. This proves all the prime-choice assertions of Theorem A.
There is no appeal to Zsigmondy's theorem and no exceptional case hidden
in an assumed primitive-prime-divisor statement.

## 6. Exact subgroup intersections and RWPRI

Let \(P=\prod_i a_i\), \(n=eP\), and choose the cyclic subgroup
\(A\le T_n\) of order \(m=\tau_e\prod_i\ell_i\).
It exists because each factor divides \(\tau_n\) and the factors are
pairwise coprime. Put \(K=A:\langle r\rangle\).
The action of \(r\) preserves every subgroup of the cyclic torus.

For a subset \(J\subseteq\{1,\ldots,k\}\), put
\[
n_J=e\prod_{i\notin J}a_i,\qquad
m_J=\tau_e\prod_{i\notin J}\ell_i.
\]
Then
\[
\bigcap_{j\in J}S_j=\operatorname{Sz}(2^{n_J}),\qquad
K\cap\bigcap_{j\in J}S_j=C_{m_J}:C_4.
\tag{6}
\]
The first is the standard coefficient-field intersection.
For the second, \(T_e\) is always retained. The \(\ell_i\)-factor
is retained if \(i\notin J\). If \(i\in J\), it cannot occur:
by (4) it would divide
\(\gcd(\tau_{ea_i},\tau_{n_J})=\tau_e\), contrary to its choice.
Binary \(r\) belongs to every subfield group, so the same formula
holds for all four cosets of the cyclic subgroup.

The RWPRI condition now follows for every proper subset of the
\(k+1\) types.

* Before \(K\) is selected, select an unused \(S_i\) whenever one
  remains. The current and next groups are simple standard Suzuki
  subfield groups of relative field degree \(a_i\), so the next is
  maximal. The lower field exponent remains at least \(e\ge3\).
* When all \(S_i\) have been selected, selecting \(K\) gives
  \(T_e:C_4\), a full nonsplit torus normalizer and maximal subgroup
  of \(\operatorname{Sz}(2^e)\).
* Once \(K\) has been selected, selecting any unused \(S_i\) removes
  exactly one factor \(\ell_i\), giving a subgroup of prime index.

These uses of subfield and torus-normalizer maximality are retained
classical Suzuki facts, not consequences of the disputed source list.

For flag transitivity, write
\[
V=\prod_i C_{\ell_i},\qquad B_0=T_e:C_4.
\]
Then \(K=V\rtimes B_0\), and (6) gives exactly the coordinate
stabilizers in (3). Lemma D and Theorem C apply.
This completes the geometry and flag-transitivity parts of Theorem A.

## 7. Firmness, residual connectedness, and the base-two exception

The common intersection of all parabolics is \(B_0=T_e:C_4\).
A panel missing \(S_i\) has size \(\ell_i\). A panel missing \(K\),
with \(q=2^e\ge8\), has size
\[
|\operatorname{Sz}(q):B_0|=q^2(q-1)\tau'_e/4\ \ge\ 560.
\]
The inequality follows from
\(\tau'_e\ge q+1-\sqrt{2q}\) and its value five at \(q=8\);
all factors in the lower bound increase for \(q\ge8\).
Each \(\ell_i\) is an odd prime, hence at least three.
Thus the flag-transitive geometry is thick.

For residual connectedness, flag transitivity reduces all residues to
their standard subgroup systems. The incidence graph of a coset system
with at least two types is connected when its marked subgroups generate
the ambient residue group. This generation holds uniformly:

* If \(K\) was already selected, at least two unused field types
  remove different prime factors. Their two subgroups together
  contain every cyclic factor and \(B_0\), hence generate the residue.
* If \(K\) is unused and at least two field types remain, their two
  distinct maximal simple subfields generate the current Suzuki
  group.
* If only one field type and \(K\) remain, the simple base subfield
  is maximal in the current Suzuki group. The cyclic-by-four
  subgroup has an extra \(\ell_i\)-factor, so is not contained in
  that subfield, by (6). Together they generate.

These cases include the ambient incidence graph.
They prove residual connectedness in every rank.

The phase-six rank-four example has \(e=1\), so the last simple-subfield
step cannot be used: \(\operatorname{Sz}(2)\) is not simple and is not
being declared maximal in \(\operatorname{Sz}(2^{a_i})\).
Instead its chosen \(\tau_{a_i}=13,41,113\) are full prime-order
nonsplit tori for \(a_i=3,5,7\). At that step select the full torus
normalizer, which is maximal. The remaining \(C_4\) has index five
in \(\operatorname{Sz}(2)\), and the other panel indices are
13, 41, 113. The rank-two residue with one field type and \(K\)
is connected because its full torus normalizer is maximal and the
order-twenty base group contains an element of order five outside it.
All other arguments above apply unchanged.

Thus the rank-four example is thick, residually connected,
flag-transitive, and RWPRI. This is a proof supplement to the immutable
phase-six record, whose “unproved” statements correctly describe what
had been established at that earlier stage.

## 8. Retained theory and scope

The substantial external inputs are Lang–Steinberg surjectivity,
the standard exceptional Suzuki endomorphism/model, cyclicity of the
finite nonsplit tori, and the classical maximality theorems for their
normalizers and prime-degree simple subfields. The binary seed,
character-lattice calculation, finite descent argument, typed Helly
theorem, coordinate attachment, prime-choice argument, and all-subset
RWPRI/residue calculations are given here.

The result is an existence and flag-transitivity theorem for explicitly
aligned families. It does not say arbitrary subgroups with the same
isomorphism types have these intersections. It does not classify all
Suzuki geometries, prove a geometric intersection-property axiom, or
restore the old candidate completeness claims. Classical ingredients
are credited as such, and novelty of this particular assembly remains
subject to a fuller literature and external mathematical review.

## 9. Executable and formal evidence

Run the new exact seed checker from this directory:

    python3 phase7_suzuki_seed_check.py

The [script](phase7_suzuki_seed_check.py), its
[record](phase7_suzuki_seed_check.json), and
[run log](phase7_suzuki_seed_check.log) are separate from every earlier
executed artifact. The script reads the hash-bound phase-six matrices
and arithmetic modules without rewriting them.
Its polynomial identities establish the exact exceptional-endomorphism
convention. Its twenty-element check selects the sign of the torus
character polynomial. It also records finite corroborations of the
proved integer identities, a factored rank-five parameter example,
and the coordinate-surjectivity input from the rank-four certificate.
Those finite arithmetic checks are not a proof by enumeration of
Theorems A or C, or of infinitely many prime choices.

The abstract attachment implication in Lemma D is separately formalized
in [CosetCoordinates.lean](formal/CosetCoordinates.lean), with
[a fresh successful report](formal/CosetCoordinates.check.json) and
[its precise scope](formal/CosetCoordinates.scope.md).
It does not formalize the coordinate construction, Lang–Steinberg,
the torus character calculation, or the classical maximality inputs.
The algebraic and geometric applications remain written proofs.

The independent review and temporary-copy rerun are recorded in
[phase7_suzuki_independent_audit.md](phase7_suzuki_independent_audit.md) and
[phase7_suzuki_audit_run.json](phase7_suzuki_audit_run.json).
These are internal independent checks, not external peer review.
The source PDF files used for the literature check are excluded from
the public artifact export; their provenance is recorded separately.
