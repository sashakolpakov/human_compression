# Full parameter realizations for Suzuki Constructions 8 and 9

10 October 2026. This is a companion to
[phase7_suzuki_descent.md](phase7_suzuki_descent.md), whose notation and
Lang–Helly and coset-coordinate lemmas are used below.
It proves existence, the prescribed standard-position intersection
formulas, RWPRI, firmness, residual connectedness, and flag transitivity
for every admissible parameter choice of the two constructions.
It does not classify arbitrary relative positions or restore the source's
disproved global candidate-completeness claim.

The source is L110, Leemans,
[*The residually weakly primitive pre-geometries of the Suzuki simple
groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995),
Constructions 8 and 9, printed pp.17–18. The displayed parameter ranges
and the prime-divisor conditions were read in the primary full text.
The theorem below supplies a canonical simultaneous position for these
subgroups; isomorphism types by themselves do not specify that position.

## 1. Source parameters, including the lower-field restriction

Write the field exponent as \(n\), so the ambient group is
\(G=\operatorname{Sz}(2^n)\). The source chooses \(k=\alpha-1\)
pairwise nonisomorphic maximal simple subfield groups
\(\operatorname{Sz}(2^{n/a_i})\), where the relative degrees
\(a_i\) are distinct odd primes.
Set
\[
e=n/\prod_i a_i,\qquad t=2^e.
\]

The upper bound \(\alpha\le\sum_j e_j=\Omega(n)\) in both constructions
implies \(\Omega(e)=\Omega(n)-k\ge1\). Since \(n\) is odd,
**\(e\ge3\) and \(t\ge8\)**. Thus neither construction includes a
nonsimple base \(\operatorname{Sz}(2)\).
The notation \(\Omega\) here counts prime factors with multiplicity.
Some \(a_i\) may also divide \(e\); the proof allows that.

Construction 8 chooses distinct primes
\[
\ell_i\mid\frac{t^{a_i}-1}{t-1}
\]
and adds the dihedral subgroup of order
\[
2(t-1)\prod_i\ell_i.
\]

Construction 9 chooses a base nonsplit torus order
\(\gamma=t+\sqrt{2t}+1\) or \(t-\sqrt{2t}+1\), and distinct primes
\(\ell_i\) such that \(\gamma\ell_i\) divides an appropriate nonsplit
torus order of \(\operatorname{Sz}(t^{a_i})\).
It also requires \(\gamma\prod_i\ell_i\) to divide one of the two
ambient nonsplit torus orders. Its added subgroup has order
\[
4\gamma\prod_i\ell_i
\]
and is cyclic by \(C_4\).

The source does **not** require \(\ell_i\nmid\gamma\).
This note covers those overlapping-prime cases explicitly.
The arbitrary-rank existence theorem in the main note uses the extra
restriction \(a_i\nmid\tau_e\) only to prove an unconditional supply
of parameters; that restriction is not needed for the present
conditional-on-admissible-parameters realization theorem.

## 2. Both nonsplit branches have compatible binary models

The main note constructs a torus \(\mathbf T\), stable under the
exceptional endomorphism \(\rho\), with
\[
|\mathbf T^{\rho^d}|=\tau_d
=2^d+1-\big((1+i)^d+(1-i)^d\big)
\]
for every odd \(d\). To obtain the other branch, retain its binary
order-four matrix \(r\) and antidiagonal \(w\), and set
\[
c=r^2w.
\]

The new exact seed check gives
\[
|c|=5,\qquad \rho(c)=c,\qquad
C_{\operatorname{Sz}(2)}(c)=\langle c\rangle.
\]
It also verifies that \(r\) conjugates \(c\) to \(c^2\) or \(c^3\),
so normalizes its centralizer.
As the multiplicative order of 2 modulo 5 is four, \(c\) has four
distinct eigenlines cyclically permuted by binary Frobenius.
Therefore
\(\mathbf T'=C_{\operatorname{Sp}_4}(c)\) is another maximal torus
with the same four-cycle Frobenius calculation as in the main note.
It is \(\rho\)-stable because \(\rho(c)=c\).

The character-lattice endomorphism has determinant two and trace
\(\pm2\); its five \(\rho\)-fixed points select trace **minus two**.
For odd \(d\), this gives
\[
|(\mathbf T')^{\rho^d}|=\tau'_d
=2^d+1+\big((1+i)^d+(1-i)^d\big).
\]
Both finite families are cyclic. Each satisfies
\[
T_a\cap T_b=T_{\gcd(a,b)},\qquad
\gcd(|T_a|,|T_b|)=|T_{\gcd(a,b)}|.
\tag{1}
\]
The binary \(r\) supplies the order-four complement in every odd
extension.

For any fixed odd base exponent \(e\), these two branches give precisely
the two possible base torus orders \(\gamma\). Choose the branch
whose order at \(e\) is \(\gamma\), and write its order at \(d\) as
\(h_d\). Since \(T_e\le T_{ea_i}\), \(\gamma\mid h_{ea_i}\).
The other order at \(ea_i\) is coprime to \(h_{ea_i}\).
Because \(\gamma>1\), it cannot also be divisible by \(\gamma\).
Consequently each source condition \(\gamma\ell_i\) dividing a
nonsplit torus order automatically selects this same compatible branch.
The same argument identifies the prescribed ambient branch.
Thus all the source's choices can be made simultaneously inside
one \(\rho\)-stable torus.

For Construction 8 use the standard split tori
\[
T_d=\{h(\lambda):\lambda\in\mathbb F_{2^d}^{\times}\},
\qquad h_d=2^d-1.
\]
They satisfy the same intersection and gcd identities (1).
Their common complement is the binary \(w\), of order two, acting by
inversion. In the main note's standard matrix convention,
the diagonal subgroups are compatible under every odd subfield
embedding: when \(d\mid n\) and \(n/d\) is odd,
\((n+1)/2\equiv(d+1)/2\pmod d\), so the ambient exponent
\(\theta_n\) restricts to \(\theta_d\) on \(\mathbb F_{2^d}\).

## 3. One intersection calculation covers both constructions

Write \(c_0=2\) for the split case and \(c_0=4\) for either nonsplit
case. Set \(\gamma=t-1\) in Construction 8; in Construction 9 retain
the chosen nonsplit base order. Thus \(\gamma=h_e\) in every case.
In the chosen ambient cyclic torus \(T_n\), let
\[
A=C_m,\qquad m=\gamma\prod_i\ell_i,\qquad
K=A:C_{c_0}.
\]
For Construction 9, \(m\mid h_n\) is a source assumption.
For Construction 8 it follows from the individual divisibilities:
each \(\gamma\ell_i\) divides \(2^n-1\), and, because the primes are
distinct, their least common multiple is \(m\).
The common binary complement normalizes \(A\).

Take the standard subfield parabolics
\(S_i=\operatorname{Sz}(2^{n/a_i})\).
For \(J\subseteq\{1,\ldots,k\}\), put
\[
n_J=e\prod_{i\notin J}a_i,\qquad
m_J=\gamma\prod_{i\notin J}\ell_i.
\]
Then
\[
\bigcap_{j\in J}S_j=\operatorname{Sz}(2^{n_J}),\qquad
K\cap\bigcap_{j\in J}S_j=C_{m_J}:C_{c_0}.
\tag{2}
\]

Here is the valuation argument that handles \(\ell_i\mid\gamma\).
For the prime \(\ell_i\), the exponent in \(m\) is
\(v_{\ell_i}(\gamma)+1\).
If \(i\notin J\), \(ea_i\mid n_J\), so
\(\gamma\ell_i\mid h_{n_J}\); the extra copy is retained.
If \(i\in J\), then
\[
\gcd(ea_i,n_J)=e,\qquad
\gcd(h_{ea_i},h_{n_J})=\gamma.
\]
Since \(\gamma\ell_i\mid h_{ea_i}\), this forces
\(v_{\ell_i}(h_{n_J})=v_{\ell_i}(\gamma)\): exactly the extra copy
is removed. Primes not selected among the \(\ell_i\) occur in \(m\)
only through \(\gamma\), which is always retained.
Thus \(\gcd(m,h_{n_J})=m_J\).
The binary complement belongs to every standard subfield group,
proving the full cyclic-by-complement equality in (2).

This proof allows \(a_i\mid e\): factoring \(e\) from both exponents
still gives \(\gcd(ea_i,n_J)=e\), since the remaining relative primes
are distinct from \(a_i\).

## 4. Coset coordinates without a coprime-base assumption

Let \(H_i=K\cap S_i=C_{m/\ell_i}:C_{c_0}\) and
\(A_i=A\cap H_i=C_{m/\ell_i}\).
Every left coset of \(H_i\) in \(K\) has a representative in \(A\),
because the complement is contained in \(H_i\), and
\[
A/A_i\longrightarrow K/H_i,\qquad aA_i\longmapsto aH_i
\]
is a bijection of sets.

The cyclic group \(A\) maps onto
\(\prod_i A/A_i\): these are cyclic quotients of the pairwise
distinct prime orders \(\ell_i\), so this is the ordinary Chinese
remainder theorem. Its kernel has order \(\gamma\).
This remains true when some selected primes divide \(\gamma\).
Hence the set map
\[
K\longrightarrow\prod_i K/H_i
\]
is surjective. No \(H_i\) is asserted to be normal in \(K\).
Only the subgroups \(A_i\) of the abelian \(A\) are used as
group-quotient kernels.

The standard subfield types satisfy Theorem C of the main note.
Its Lemma D now gives a common representative in every flag of the
enlarged coset system. The system is a geometry, and \(G\) is
flag-transitive.

## 5. RWPRI, thickness, and residual connectedness

The all-subset proof in the main note applies with (2).
Before selecting \(K\), each unused field type makes a maximal
simple-subfield step; their terminal group is
\(\operatorname{Sz}(2^e)\), with \(e\ge3\).
Selecting \(K\) there gives its full split or nonsplit torus
normalizer, a maximal subgroup.
After selecting \(K\), an unused field type removes precisely one
factor \(\ell_i\), giving prime subgroup index.
These are the source's RWPRI conditions.

Panel sizes are the odd primes \(\ell_i\), and the index of the
full base torus normalizer in the simple group
\(\operatorname{Sz}(2^e)\). The latter is greater than two
(an index-two subgroup of a simple group would be normal).
Thus the geometry is thick.

For residual connectedness, standard residues are enough because
flag transitivity is proved. With \(K\) already selected, two unused
field types give cyclic parts of orders \(m_J/\ell_i\) and
\(m_J/\ell_j\). Their least common multiple is \(m_J\), so they
generate the current cyclic-by-complement subgroup.
Without \(K\), two remaining distinct maximal simple subfields
generate the current Suzuki group. If only one field type and \(K\)
remain, the simple base subfield is maximal, and (2) shows that the
other marked subgroup is not contained in it. They therefore
generate as well. This proves connectedness of every residue of
rank at least two, including the whole geometry.

We have thus rederived the complete parameterized **existence
assertions** of Constructions 8 and 9, and proved flag transitivity
and residual connectedness for these canonical realizations.
Their inclusion in an exhaustive classification, the classification
of all embeddings with those isomorphism types, and geometric
intersection-property axioms are separate questions.

## 6. Extra exact checks

Run

    python3 phase7_suzuki_families_check.py

The [script](phase7_suzuki_families_check.py),
[record](phase7_suzuki_families_check.json), and
[log](phase7_suzuki_families_check.log) verify the new order-five
binary seed and its five-element centralizer.
They also check every intersection and every cyclic coset-coordinate
tuple in three examples that have a selected prime dividing the base
torus order:

| Branch | Base exponent | Relative primes | \(\gamma\) | Selected primes | \(|A|\) |
|---|---:|---|---:|---|---:|
| Split, Construction 8 | 3 | 7, 3 | 7 | 7, 73 | 3577 |
| First nonsplit, Construction 9 | 3 | 13, 3 | 13 | 13, 37 | 6253 |
| Second nonsplit, Construction 9 | 3 | 5, 3 | 5 | 5, 109 | 2725 |

These are finite corroborations of the valuation and coset-coordinate
proofs, not an exhaustive test of every source parameter.
The retained input is the classical Suzuki subgroup and torus theory,
together with Lang–Steinberg used in the main note.
No old candidate-completeness claim is used.
