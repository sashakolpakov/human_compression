# Higher composite-degree Suzuki shapes: separate investigation

10 October2026. Proposed proof extending the initial
[Suzuki realization note](phase5_suzuki_realization.md). Two independent
internal mathematical reviews found no gap under the retained Suzuki inputs.
All numbering refers to L114 Theorem5.5,
with the L110 restatement in parentheses.

## A. Exact meaning of the extension notation

L110 p.5 explicitly defines E_q as an elementary abelian group of orderq,
and the hat-dot as a nonsplit extension. Its p.6 maximal-subgroup table
identifies (E_q hat-dot E_q):(q−1), of orderq²(q−1), as the Sylow-2
normalizer/ovoid point stabilizer.

L114 p.57–58, “Residue16”, first places the mixed subgroup inside this
point stabilizer. It gives the two smaller intersections as
E_s hat-dot E_t:(t−1) and E_s′ hat-dot E_t:(t−1). It then asserts that
maximality of one of these forces their generated group to have type
E_q hat-dot E_t:(t−1). The final diagram on p.60 is shape9; L110 p.9
repeats it as R12.

Thus the first elementary abelian factor has orderq, not an unspecified
subspace size. This distinction is essential.

## B. A useful extension of the retained rigidity lemma

The general mechanism is the normalizer/transporter method used in the
[classification note](classification_compression.md). Suppose L≤K≤G,
all relevant copies of K are G-conjugate, and all relevant copies of L
inside K are K-conjugate. The overgroups conjugate to K and containing L
form the homogeneous space

    N_G(L) / (N_G(L) ∩ N_G(K)).

Pull a conjugate's inclusion back into K, adjust it by internal
K-conjugation to match L, and the remaining conjugator normalizes L.
The stabilizer of K is the displayed intersection. When K is
self-normalizing the denominator is N_K(L). In particular, N_G(L)≤K
forces a single overgroup. The conjugacy hypotheses are essential;
subgroup orders alone do not imply this conclusion.

Let d>1 and a be odd with d|a|n. In Sz(2^n), exactly one conjugate of the
standard subfield group S_a contains the standard split dihedral
D_d=H_(2^d):<w>.

The proof of LemmaA in the companion note extends directly. The normalizer
of D_d in G is D_d. Every subgroup of S_a isomorphic to D_d is conjugate
to the standard one: its odd cyclic subgroup must lie in a split torus
because its order divides2^a−1, which is coprime to the nonsplit torus
orders; split tori are conjugate, and squaring acts bijectively on the odd
torus, making the reflection choices conjugate. Adjusting the embedding
by this internal conjugation puts its defining element in N_G(D_d).

Consequently, if two conjugate subfield groups share a simple subfield
S_d, they are simultaneously conjugate to the standard field-defined
groups. This is an application of classical Suzuki conjugacy facts, not
an independent classification of all subgroups.

## C. Proposed obstruction for shape9 / R12

Let t≥8 be an odd power of2 and let a,b be distinct odd primes. Write

    q=t^(ab),   s=t^a,   s′=t^b.

In SectionsC–D, S_s denotes the standard group Sz(s), using a field-size
index; SectionB uses field-exponent indices.

These are the consistent field relationships required by the source's
maximal subfield groups; the letters indexing the two primes may be
interchanged between its displays. Shape9 requires

    G0≅Sz(s),   G2≅Sz(s′),   G02≅Sz(t),
    G1≅E_q hat-dot E_t:C_(t−1),
    G01≅E_s hat-dot E_t:C_(t−1),
    G12≅E_s′ hat-dot E_t:C_(t−1),
    G012≅E_t hat-dot E_t:C_(t−1).

**Theorem.** No such embedded lattice satisfies the source's
RWPRI axiom.

**Proof.** Conjugate G02 to the standard S_t. SectionB then forces
G0,G2 to be the standard S_s,S_s′. Their common Borel
G012 may be conjugated within S_t to B_t=U_t H_t.

The displayed extension gives a normal Sylow-2 subgroup P of G1 of
orderqt, containing an elementary abelian subgroup E_q of orderq. Put P
inside an ambient Sylow-2 subgroup U. Every involution of U lies in Z(U),
whose order isq, so E_q=Z(U). In particular E_q is the identity together
with all involutions of P. It is characteristic in P and hence normal
in G1. Normality makes G1 stabilize the unique
ovoid point fixed by Z_q. Since it contains B_t, this point is the
standard point at infinity. Therefore the normal E_q is the standard
Z_q. Containment and orders now give

    G1=Z_q U_t H_t,
    G01=Z_s U_t H_t,
    G12=Z_s′ U_t H_t.

Conversely these standard groups do have all the printed intersections:
G0∩G2=S_t by field intersection, intersecting G1 with S_s or S_s′
restricts its central parameter to that field, and the triple intersection
is B_t. Thus the bare embedded subgroup lattice exists. The remaining
argument shows why it fails RWPRI.

For any F_t-linear subspace V with F_s⊆V⊆F_q, the set

    K_V=Z_V U_t H_t

is a subgroup: Z_V is central in U_q, and H_t acts on its parameter by
a scalar in F_t. If V=F_s+F_t v for v∉F_s, then
dim_(F_t)V=a+1<ab. Hence

    G01 < K_V < G1.

Likewise choose V′=F_s′+F_t v′ and use b+1<ab to obtain

    G12 < K_V′ < G1.

Thus neither G01 nor G12 is maximal in G1. Taking J={1} in the
source's RWPRI definition contradicts the required existence of a
maximal remaining intersection. ∎

The argument does not merely reject one coordinate realization. The
normal E_q and the shared simple subfield force the coordinates. It
does not claim that every mixed-subfield incidence construction is
impossible: it excludes this exact displayed lattice and axiom.

The final step is an invariant-subspace obstruction. H_t acts by
F_t-scalars, so its invariant centers include every F_t-subspace.
Maximality would require an irreducible quotient, while these center
quotients have F_t-dimension greater than one. This is the same
module-theoretic test underlying the semilinear/descent reductions
elsewhere in the repository; here it gives an obstruction.

## D. Standard realizations of shapes7,8,10

These use the same field alignment, so there is no need to search conjugate
subfield positions. The source's full candidate classification is retained.

**Shape7 / R10.** With q,s,s′,t as above, choose distinct primes p,p′
dividing (s−1)/(t−1), (s′−1)/(t−1), respectively. Put m=(t−1)pp′ and
take the standard S_s,S_s′ together with D=H_m:<w>, where here H_m
denotes the cyclic subgroup of orderm of the ambient split torus.
The field gcd identity gives gcd(s−1,s′−1)=t−1. Hence m dividesq−1 and

    gcd(m,s−1)=(t−1)p,   gcd(m,s′−1)=(t−1)p′.

The intersections are precisely the displayed dihedrals, S_t, and the
common D_(2(t−1)). The latter is maximal in S_t; the two larger
dihedrals contain it with prime indices. The two intermediate subfield
groups S_t⊂S_s,S_s′ are maximal, as are the ambient S_s,S_s′.
Consequently every stage of the lattice RWPRI condition is satisfied.

**Shape8 / R11.** Choose a maximal nonsplit torus A_t of S_t of order
m=t±sqrt(2t)+1. Its ambient centralizer is a unique cyclic nonsplit
torus A_q. Let A_s=C_(S_s)(A_t) and A_s′=C_(S_s′)(A_t), of orders
one of s±sqrt(2s)+1 and one of s′±sqrt(2s′)+1, respectively.
Their intersection is A_t. Choose primes p,p′ such that mp divides
|A_s| and mp′ divides|A_s′|. These primes are necessarily distinct,
since gcd(|A_s|,|A_s′|)=m. Choose r of order4 in N_(S_t)(A_t), and set

    K=<C_(mpp′),r>⊂N_G(A_q).

Then K∩S_s=C_(mp):<r>, K∩S_s′=C_(mp′):<r>, and
K∩S_t=A_t:<r>. The common normalizer is maximal in S_t, the cyclic
extension indices are prime, and the subfield steps are maximal.
This verifies the exact intersections and lattice RWPRI condition.
The ambient torus has the correct sign automatically because the
nonidentity A_t lies in it. Its order is coprime to the other ambient
nonsplit torus order.

**Shape10 / R13.** Let n be the odd field exponent and select three
distinct prime divisors a,b,c. Assume n/(abc)>1, as in the source's
sum-of-exponents≥4 condition. Reverting to exponent indices, take

    G0=S_(n/a),   G1=S_(n/b),   G2=S_(n/c).

Their pairwise and triple intersections are exactly the field-gcd
subgroups S_(n/(ab)), S_(n/(ac)), S_(n/(bc)), S_(n/(abc)).
Every one-step inclusion is a maximal subfield inclusion of prime
relative degree, so RWPRI holds at every subset of the type set.

## E. Exact scope of the proposed resolution

The final paragraph on source p.61 asks whether subgroups with the printed
intersections exist. This bare-embedding question must be separated from
whether the resulting lattice satisfies RWPRI. Together with the companion
note, the proposed answer for every permitted parameter is:

| Source target | Printed embedded intersections exist | RWPRI realization |
|---|---|---|
| Theorem5.3, all three shapes | Yes | Yes |
| Theorem5.5, shapes1,2,3,5 | No | No |
| Theorem5.5, shapes4,6,7,8,10 | Yes | Yes |
| Theorem5.5, shape9 / R12 | Yes | No |

Thus among the ten composite-degree shapes, four have impossible
intersections, six have realizable intersections, and five satisfy RWPRI.
Theorem5.4's published nonexistence is retained. The R12 distinction
prevents counting a failure of maximality as failure of bare embedding.

This is not a classification of flag transitivity, of all relative
positions within a realizable shape, or of geometric isomorphism classes.
Nor does it independently reprove the completeness of the source's
candidate list.

## F. Retained inputs, checks and review

The retained group theory comprises the standard Suzuki matrix model,
involution/Sylow structure, subfield conjugacy, torus centralizers and
normalizers, maximality of prime-degree subfield inclusions, and
maximality of full torus normalizers. The candidate classification is a
source input. These arguments do not independently derive those facts.

The standard-library checker
[phase5_suzuki_higher_check.py](phase5_suzuki_higher_check.py) constructs
F_(2^45) as the quotient by x^45+x^4+x^3+x+1; it verifies irreducibility
by the exact Rabin criterion. Binary linear algebra computes bases for
F_(2^9), F_(2^15) and F8 and verifies actual strict intermediate centers
of F2-dimensions9<12<45 and15<18<45. It checks normalization by a
generator of the order-seven torus and commutation with all64 elements
of U8 on the center bases. The two intermediate subgroup orders are
229376 and14680064, while G1 has order1970324836974592.
The [saved output](phase5_suzuki_higher_check.json) also contains two
shape7 and two shape8 integer torus-parameter checks at this field size.

These exact checks verify the finite examples and the arithmetic
implementation. The uniform classification statement depends on the
written proofs. No group of order comparable to Sz(2^45) is enumerated.

Root and recent_conjectures independently reviewed SectionsA–D against
the primary source. The second reviewer also inspected and reran the
checker in a temporary copy, preserving the historical output. Their
[record](phase5_suzuki_higher_audit.json) is an internal review, not
independent external review. The [intake](phase5_suzuki_higher_intake.json)
records exact scope and hashes. The bounded forward search in the
companion intake did not establish publication priority. In particular,
the flag-transitivity and embedding-isomorphism questions remain separate.
