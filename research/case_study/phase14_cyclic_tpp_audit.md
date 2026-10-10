# Independent mathematical audit of the two-square-map cyclic-TPP argument

10 October 2026. **PASS for the complete frozen written proof.** The companion JSON
records its exact source-byte binding. This audit concerns the
proposed uniform finite-two-group theorem in
[phase14_cyclic_tpp.md](phase14_cyclic_tpp.md). It checks the complete
dependency-reduced chain described below, including the removal of both
the finite order-256 input and the marked-isobicyclic classification from
this new proof. Earlier frozen proofs are unchanged.

## 1. The minimum-counterexample and powerful-subgroup inputs

The central-quotient absorption and proper-pair subgroup reductions preserve
cyclicity and TPP and establish center-disjointness and generation by every
pair. The maximal-subgroup argument then gives ratio two, two-dimensional
Frattini quotient and the three distinct nonzero marked classes. The
disjoint-conjugate estimate supplies the elementary lower bound four for
each cyclic order; it does not use the later isobicyclic theorem.

Writing K=Phi(P), the three square factors have order product |K| and
generate K by minimum order. This does not by itself give bijective
coordinates. The earlier powerful-Frattini obstruction has exactly the
needed classification-free scope: if K were powerful, the retained
Lubotzky–Mann any-generating-list factorization would give surjectivity,
then equality would give bijectivity. Its equivariant top-power map and
the elementary binary square-action lemma force a central marked element.
Thus K is not powerful. I rechecked the proof of this obstruction against
the earlier note; no finite catalogue or isobicyclic result enters it.

The weak-embedding lemma also has an independent elementary proof. In its
induction, all power subgroups factored out are characteristic and normal.
After reducing to exponent four and quotienting a central involution, N
has class at most two, with central elementary-abelian N². The assumption
[N,G]≤N² then makes every square of G centralize N. If N≤G² this proves
the required powerfulness. The argument does not assume arbitrary power
maps are homomorphisms or arbitrary subgroups of powerful groups are
powerful.

On K/K² the two marked conjugations satisfy the binary square identities.
In dimension at most two, their commuting involutory actions must be
trivial: the only possible nontrivial involutions have the same image and
kernel line, and the identities put all three spanning marked vectors in
that line. Weak embedding would then make K powerful. Consequently
d(K)=3. The square factors form a marked basis modulo S=K².

## 2. The second and third power layers without classification or census

Squaring the equality triple in K gives three factors of product |S|,
where S=K². Minimum order makes them generate S. Some of these factors
are allowed to be trivial at this stage; that possibility must not be
excluded by importing the phase-ten small-factor theorem.

If d(S)≤2, the two-group action on S/S² has exponent at most two.
Therefore K=P² acts trivially, and weak embedding with ambient K and
normal S=K² makes S powerful. If S=1, K is elementary abelian, already
excluded. If S≠1, powerful ordered factorization and the equality of
orders give an actual coordinate bijection on S. The largest-power-layer
lemma then forces all three marked coordinate orders to be equal and
nontrivial: one or two maximal coordinates would give a globally fixed
marked involution, by the dimension-one or dimension-two action argument.
Restriction of the bijection to squares gives |S:S²|=8, contradicting
d(S)≤2. Hence d(S)=3. In particular all three fourth-power factors are
nontrivial, recovering the lower bound eight without isobicyclic input.

The same equality and minimum-order reasoning yields
N=S²=<a⁸,b⁸,c⁸> with |S:N|=8 and d(N)≤3. A two-subgroup of GL_3(F_2)
has exponent dividing four: invariant complete flags make its matrices
upper unitriangular. Thus P⁴=S centralizes N/N². Weak embedding with
ambient S and N=S² makes N powerful. The power-subgroup equalities
S=P⁴ and N=P⁸ use the displayed generators for one inclusion and the
fact that a fourth or eighth power is the square of an element in the
preceding layer for the other. No unrestricted power-nesting identity is
assumed.

## 3. The abstract action lemma has exactly the required hypotheses

Let a three-dimensional marked P-module have a,b,c fixing its first,
second and third marked basis vectors respectively, with c∈ab Phi(P),
and suppose no marked vector is globally fixed. The image is a
two-subgroup of GL_3(F_2), hence embeds in a dihedral group of order eight.
An order-four matrix has a unique fixed line. The nonzero common fixed
space of the entire two-group lies in that line, so a marked order-four
action would make its own marked vector globally fixed. All three marked
actions therefore have order at most two.

A nonabelian image would be dihedral of order eight. The product of its
two generating involutions has order four, as do both elements in that
product's Frattini coset. Since surjections of finite two-groups preserve
the Frattini subgroup, the third marked action would be in that coset,
contradiction. An image of order one or two also fixes a marked vector.
Thus the image has order four and is elementary abelian. Its kernel is
exactly K=Phi(P), by inclusion and equal index. This reasoning applies to
an abstract module; it does not require that its vectors be actual top
involutions. The exact unique matrix normal form is unnecessary for this
conclusion.

## 4. Both square maps are well defined before they are used

First suppose N≠1. Powerful coordinates and the largest-power-layer lemma
give three equal nontrivial coordinate orders in N. Their highest powers
form an actual normal elementary-abelian subgroup U with its three marked
top involutions as a basis. Center-disjointness excludes every globally
fixed marked vector. The preceding abstract action lemma gives action
kernel K on U.

The powerful top-power map N/N²→U is a marked, linear, equivariant
isomorphism. Its source and target have dimension three because the
coordinate bijection restricts to every simultaneous power subgroup.
The map is the composition of adjacent-layer square maps; each is linear
because L/L⁴ is abelian for a powerful L, and powerful power generation
gives surjectivity. The exponent-two boundary case is the identity map.
Consequently K centralizes N/N², and no marked coordinate there is
globally fixed.

Now q₁:S/N→N/N², q₁(sN)=s²N², is well defined: S²=N,
[N,S]≤[N,K]≤N², and n²∈N² for n∈N. Its equivariance is simply the
compatibility of conjugation with squaring. It maps each marked basis
vector a⁴N,b⁴N,c⁴N to the corresponding eighth-power basis vector.
A globally fixed marked vector in S/N would therefore contradict the
absence of one in N/N². Applying the abstract action lemma again shows
that K centralizes S/N. No classification of quadratic maps, polarization
calculation, or proof that S is powerful is needed.

The second map q₂:K/S→S/N, q₂(kS)=k²N, is now well defined because
K²=S, S²=N and [S,K]≤N. It is equivariant and again preserves the
marked coordinates. But the binary square-action lemma on K/S supplies
a globally fixed marked coordinate. Its image under q₂ would be a
globally fixed marked coordinate in S/N, contradiction. The exact
canonical matrices and the order-32 presentation are unnecessary here.

## 5. The trivial eighth-power case needs no finite catalogue

If N=1, then S has order eight and generator rank three, so it is
elementary abelian. The established nontrivial fourth-power factors are
its basis, and the original cyclic orders are all exactly eight. Thus
S itself is the actual top-involution module U. Center-disjointness and
the abstract action lemma show that K centralizes S and that S has no
globally fixed marked coordinate. The map q₂:K/S→S, kS↦k², is therefore
well defined and equivariant and preserves the marked coordinates. The
same binary fixed-coordinate contradiction excludes this case. The
order-256 census is not needed.

## 6. Conclusion and trust boundary

I find no mathematical gap in this complete chain. The proposed
finite-two-group theorem follows by excluding a minimum counterexample.
Combining it with the earlier odd-prime proof gives the finite nilpotent
consequence, by restriction to Sylow components and multiplication of
their inequalities. The earlier hypertope reduction then gives the
source order inequality with its genuine flag-transitivity and typed
Helly hypotheses. No subgroup-IP-only substitute is being used.

The uniform argument retains the stated powerful-group structure results
and the earlier elementary arguments. It does not use the exploratory
512-map enumeration, modulo-four lift probe, group-order-2048 search,
SmallGroups catalogue, marked-isobicyclic classification, or a quotient
IP assumption. This audit is written mathematical review, not a claim
to have rerun a complete machine verification, to have formalized the
whole theorem in Lean, or to have established external priority. The
final source and review hashes are recorded in
[phase14_cyclic_tpp_audit.json](phase14_cyclic_tpp_audit.json).
