# Suzuki subfield positions: realization and obstruction

10 October 2026. Proposed proofs, with the source-specific scope kept explicit.
The assertions below concern embedded subgroup lattices. They do not identify
abstract subgroup types with actual geometric residues or assume flag
transitivity.

## 1. Exact source target and later papers

L114 is Dimitri Leemans, [*The rank 3 geometries of the simple Suzuki groups
Sz(q)*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837),
Note di Matematica 19 (1999), 43–63. Its final paragraph on p.61
explicitly says that Theorems 5.3–5.5 list possible subgroup lattices and that
the existence of subgroups meeting as prescribed has not been proved for all
of them. The Sz(8) computation realizes all three shapes of Theorem 5.3.

L110, [*The residually weakly primitive pre-geometries of the Suzuki simple
groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995),
Note di Matematica 20 (2000/2001), reprints the rank-three shapes as
R1–R13, then derives higher-rank patterns. Its p.11 uncertainty explicitly
concerns flag transitivity. That sentence is not evidence that realization
remained open. Nevertheless the construction statements specify subgroup
types and prescribed intersections, without establishing every simultaneous
embedding by coordinates.

L085, [*Almost simple groups of Suzuki type acting on polytopes*](https://www.math.auckland.ac.nz/~dleemans/abstracts/szpoly.html) (2006),
concerns string C-group representations and regular polyhedra. Its author
abstract states existence of at least one polyhedron for every simple Sz(q)
and excludes larger almost simple groups. This does not assert the prescribed
RWPRI lattices of L114. The full article has not yet been retrieved in this
phase; neither the author abstract nor the primary 2007 restatement specifies
all the parameters needed to close L114.

For L114 Theorem 5.5, printed pp.58–60 have been visually checked against the
scanned PDF. Its shapes 1,2,3 correspond to L110 R4,R5,R6. They require

  * q=2^(ab), s=2^a, t=2^b, where a,b are distinct odd primes;
  * the displayed branch assumes s−1 prime, and its preceding case analysis
    also requires t−1 prime; in particular s,t≥8 (the obstruction does not
    require either Mersenne primality);
  * S≅Sz(s), T≅Sz(t), D≅D_(2(s−1)(t−1));
  * S∩D≅D_(2(s−1)), T∩D≅D_(2(t−1));
  * S∩T∩D≅C2;
  * S∩T≅D10, C2×C2, or C4 respectively.

Shape 5 (L110 R8) has the same coprime odd-prime field degrees, with a
nonsplit torus normalizer between S,T, and demands S∩T≅C4×C2. Its chosen
torus orders, one of s±sqrt(2s)+1 and one of t±sqrt(2t)+1, are primes.
The obstructions below do not need these primality assumptions.

These are historical candidate shapes, not assertions here that their
nonrealization has never been noticed subsequently. A bounded forward search
has not yet located a later treatment of these exact shapes.

## 2. Retained Suzuki inputs and standard coordinates

Write q=2^n with n odd, and θ=2^((n+1)/2). Use the matrices in
Bray–Bäärnhielm, [*A new method for recognising Suzuki groups*](https://arxiv.org/abs/1706.05697),
equations (1)–(5):

    U(a,b) = [[1,0,0,0],
              [a,1,0,0],
              [a^(θ+1)+b,a^θ,1,0],
              [a^(θ+2)+ab+b^θ,b,a,1]],
    h(λ) = diag(λ^(θ+1),λ,λ^(-1),λ^(-θ-1)),
    w = antidiagonal(1,1,1,1).

Set U_q={U(a,b)}, Z_q={U(0,b)}, H_q={h(λ)}, and G=Sz(q).
The Bruhat decomposition is U_q H_q disjoint union U_q H_q w U_q.
For odd d|n, restricting all parameters to F_(2^d) gives the standard
subfield subgroup S_d. Restriction of θ agrees with the Suzuki automorphism
on that subfield. Consequently

    S_a ∩ S_b = S_gcd(a,b).

This equality also holds when the gcd is 1: S_1=Sz(2) has order20 and is
isomorphic to C5:C4; it is not D10.

The following classical subgroup facts are retained, not proved anew:

  1. All subgroups of G isomorphic to a given Sz(2^d), d>1, form one
     G-conjugacy class.
  2. A nonidentity involution z is in a unique Sylow 2-subgroup U, and
     C_G(z)=U. All involutions in G, and in each simple subfield subgroup,
     form one class. All involutions of U are its nonidentity central
     elements.
  3. Every nonidentity split-torus element has centralizer H_q, and the
     normalizer of H_q is H_q:<w>. Its order is 2(q−1).
  4. The maximal split dihedral subgroups of a simple subfield subgroup
     S_d form one conjugacy class within S_d.

L114 itself uses inputs 1,3,4 in Lemma 3.11. The standard matrix model and
Bruhat decomposition make the displayed field-intersection equality exact:
the Bruhat parameters are uniquely recovered from entries, so matrices over
both subfields have parameters in their intersection.

## 3. Split-dihedral rigidity

The rigidity in the next lemma is an application of the same retained
normalizer argument already used in L114 Lemma3.11, rather than a claim of
a new general normalizer principle.

**Lemma A.** Let d>1 be odd and divide n. Put
D_d=H_(2^d):<w>, of order 2(2^d−1). Then
N_G(D_d)=D_d. Exactly one conjugate of S_d contains D_d.

**Proof.** The characteristic odd-order subgroup H_(2^d) of D_d has
centralizer H_q. Thus its normalizer is contained in H_q:<w>.
A torus element h normalizes D_d precisely when h² belongs to H_(2^d).
The quotient H_q/H_(2^d) has odd order, so this is equivalent to h belonging
to H_(2^d). This proves the normalizer statement.

If S_d^g contains D_d, then D_d^(g^-1) is conjugate within S_d to D_d,
because it is a maximal split dihedral subgroup there. Adjust g by that
internal conjugation. The adjusted element normalizes D_d, so it belongs
to D_d⊆S_d and S_d^g=S_d. ∎

**Theorem B.** Let a,b>1 be odd divisors of n, and let S,T be conjugates
of S_a,S_b. Suppose a split dihedral subgroup D of G contains maximal
split dihedrals D_S⊆S and D_T⊆T, and these dihedrals have a common
involution. Then the pair S,T is simultaneously conjugate to the standard
pair S_a,S_b. In particular S∩T≅Sz(2^gcd(a,b)).

**Proof.** Embed D in its unique ambient split-torus normalizer and conjugate
that normalizer to H_q:<w>. Conjugating further by H_q puts the common
reflection at w: squaring is bijective in H_q. The odd rotation subgroups
are the unique subgroups of H_q of orders 2^a−1 and 2^b−1. Thus D_S,D_T
are exactly D_a,D_b. Lemma A forces S=S_a and T=S_b. ∎

**Consequence.** L114 Theorem 5.5 shapes 1,2,3 (L110 R4,R5,R6) are not
realizable by embedded subgroups. Their required common reflection forces
S∩T≅Sz(2), of order20, contradicting each of the listed orders10,4,4.
This proves nonrealization, rather than merely the failure of a convenient
coordinate choice.

## 4. Involution-center rigidity

**Lemma C.** Fix z=U(0,1). If K is any conjugate of S_d containing z,
d>1, then the identity together with the involutions in C_K(z) is
exactly Z_(2^d).

**Proof.** The involutions of S_d form one conjugacy class, so any
conjugate K containing z has the form S_d^u for u∈C_G(z)=U_q.
Consequently C_K(z)=U_(2^d)^u. The identity and involutions in
U_(2^d) are Z_(2^d). Conjugation by U_q fixes Z_q pointwise, and hence
fixes Z_(2^d) pointwise. This proves the assertion. ∎

**Theorem D.** If S,T are conjugates of S_a,S_b and share an involution,
then after conjugating that involution to U(0,1), the identity and all
common involutions commuting with it form Z_(2^gcd(a,b)).
For gcd(a,b)=1, the intersection S∩T cannot contain a Klein four group.

**Proof.** Intersect the two sets in Lemma C; finite-field intersections
give the result. In a Klein four group the other two involutions commute
with the chosen one, whereas Z_2 has just one nonidentity element. ∎

**Consequence.** L114 Theorem 5.5 shape 5 (L110 R8) is not realizable:
C4×C2 contains a Klein four group, and the required field degrees are
coprime. Shape 2 is independently excluded by the same argument.

## 5. A uniformly realized family

L114 Theorem 5.5 shapes 4 and6 (L110 R7,R9) have a direct realization.
Let q=s^r where r is an odd prime and s≥8 an odd power of2. For any prime
ℓ dividing (q−1)/(s−1), set m=(s−1)ℓ and use the standard subgroups

    G0=S_log2(s),    G1=H_m:<w>,    G2=Z_q H_m,

where H_m is the unique order-m subgroup of H_q. Then

    G01=H_s:<w> ≅ D_(2(s−1)),
    G02=Z_s H_s ≅ E_s:C_(s−1),
    G12=H_m ≅ C_m,
    G012=H_s ≅ C_(s−1).

The intersections follow directly from standard matrix coordinates. The
source's lattice RWPRI condition also holds: G0 is maximal in G; G01 is
maximal in G0 and in G1; G012 is maximal in each Gij, using the prime
indices2 andℓ and the irreducible action of H_s on Z_s. Finally H_m is
maximal in Z_q H_m, because H_m acts irreducibly on the additive group
Z_q. To check this last claim, its scalar field contains F_s and has degree
over F_s dividing r. It cannot be F_s, since m>s−1. Thus it is F_q.
The torus action on Z_q differs from the parameter λ by a power relatively
prime to q−1, which leaves this field-generation argument unchanged.

This verifies actual embedded subgroups and the source's exact lattice
axiom for every permitted parameter. It does not claim that all alternative
relative positions are conjugate, nor that an abstract lattice alone
determines the incidence geometry.

## 6. A trace transversal and all shapes with q−1 prime

Here assume q−1 is prime, exactly as in L114 Theorem5.3. Write z(x)=U(0,x)
and H=H_q. The order of a product of two involutions determines the order
of the dihedral group they generate.

We additionally retain the standard Suzuki facts that every nonidentity
odd-order element lies in a conjugate of one of the cyclic tori of orders
q−1, α=q+sqrt(2q)+1, β=q−sqrt(2q)+1, that the normalizer indices in these
tori are2,4,4, and that the nonidentity elements in the complementary
Sylow-2 part have trace zero. These facts are weaker than the source's full
subgroup classification.

**Lemma E (trace transversal).** The q−1 matrices w z(x), x≠0, represent
all nonidentity odd-order conjugacy classes of G, one each.

**Proof.** Matrix multiplication gives tr(w z(x))=x^θ. These are distinct
and nonzero, so the matrices lie in distinct odd-order classes. The total
number of such classes is

    (q−2)/2 + (α−1)/4 + (β−1)/4 = q−1.

Indeed fusion within a cyclic torus is controlled by its normalizer, because
the centralizer of every nonidentity element is that torus. The normalizer
quotients act freely on nonidentity elements. This gives the displayed
count and proves exhaustion. In particular, for every prime p dividing
(q−1)(q²+1), some x gives |w z(x)|=p. There are (q−2)/2 parameters giving
order q−1. ∎

**Theorem F.** Every parameter shape in L114 Theorem5.3 is realized by
actual embedded subgroups.

**First shape (R1).** Choose involutions a,b with |ab|=q−1; such a pair
exists in a split-torus normalizer. Their unique ovoid fixed points P,Q
are distinct: otherwise both belong to the elementary abelian involution
center at the same point, and their product has order at most2. Let T be
the pointwise stabilizer of P,Q, and let Z_P,Z_Q be the centers of the
Sylow-2 point stabilizers. Set

    G0=<a,b>,   G1=Z_P T,   G2=Z_Q T.

Then G1∩G2=T, of order q−1. The intersection G0∩G1 is <a>: any
nonidentity rotation in G0 fixes precisely its two split-torus points,
and a swaps those two points, so the fixed point P of a is not one of
them. Thus no nonidentity rotation fixes P. Two reflections fixing P
would commute, impossible in an odd dihedral group. Similarly
G0∩G2=<b>. Their triple intersection is1.

**Second shape (R2).** Choose x with |w z(x)|=p and put

    G0=H:<w>,   G1=Z_q H,   G2=<w,z(x)>.

The first two groups intersect in H. The other two intersections are
<w> and <z(x)>, and the triple intersection is1. For example, a subgroup
of D_(2p) properly containing one reflection is the whole group. Equality
with G0 would place z(x) in G0, which is impossible since no reflection
of G0 fixes the ovoid point fixed by Z_q. Equality with G1 is impossible
since w does not fix that point.

**Third shape (R3), p=2 and p′ odd.** Choose t with |w z(t)|=q−1 and x≠t with
|w z(x)|=p′. Such x,t exist: if p′=q−1 there are at least three choices
of its parameter by Lemma E. Take the three parabolics generated by the
pairs from w,z(t),z(x). Their orders are 2(q−1),4,2p′. The elementary
abelian order-four group cannot lie in either odd dihedral group. If the
two odd dihedral groups had an intersection larger than their common
reflection, primality would force equality and hence place two distinct
commuting involutions in an odd dihedral group. Thus the pairwise
intersections are the three indicated order-two groups, with trivial
triple intersection.

**Third shape, distinct odd p,p′.** Choose x,y with |wz(x)|=p and
|wz(y)|=p′. Since p≠p′ their traces differ. The map λ↦λ^(θ+1) is
bijective on F_q^*: gcd(θ+1,q−1)=1. Choose λ so that
λ^(θ+1)x^θ=y^θ and put

    a=w,   b=h(λ)w,   c=z(x).

Now |ac|=p, and tr(bc)=y^θ gives |bc|=p′ by Lemma E and trace
invariance. Also ab=h(λ)^(-1) has order q−1 since λ≠1 and q−1 is
prime. The pair-generated dihedral groups have pairwise intersections
<a>,<b>,<c>: a larger intersection containing a reflection would force
equality of the relevant prime-rotation dihedrals, which would put c
in H:<w>, impossible.

**Third shape, p=p′ odd (including p=5).** Choose t,x with
|w z(t)|=q−1, |w z(x)|=p and t≠x, and set

    a=w,   b=z(t)wz(t),   c=z(x).

Then ab=(wz(t))² has order q−1. Since z(t) commutes with c, bc is
conjugate to ac, so both have order p. Furthermore
<a,b>=<w,z(t)>: in a dihedral group of odd rotation order, squaring
generates the same rotation subgroup. The involution c does not lie in
that group, since it is distinct from and commutes with z(t).
The same prime-dihedral intersection argument proves the required
intersections.

Finally every displayed triple satisfies the source's lattice RWPRI
axiom. The split dihedral G0 is maximal in G. In the odd dihedral
parabolics the indicated reflection subgroups are maximal because their
rotation orders are prime. In Z_q:H the torus complement is maximal
because it acts irreducibly on Z_q. Each triple intersection has the
required maximality in at least one remaining pair intersection (in fact
in all in the thin third shape). For the first two shapes this also uses
the primality of q−1. Thus these are realizations of the requested axiom,
not only group-order matches. ∎

Lemma E's facts and the short constructions may overlap later polytope
constructions; novelty of their application to every prescribed parameter
in the 1999 list is not asserted without a fuller comparison. None of the
argument assumes every rank-three C-group yields a flag-transitive geometry.

## 7. Reproducible checks and remaining scope

The standard-library script [phase5_suzuki_check.py](phase5_suzuki_check.py)
has passed. Its [record](phase5_suzuki_check.json) checks the trace
transversal and the R1,R2 subgroup intersections at q=8,32,128, all
32 unordered R3 prime-parameter combinations at those three field sizes, all
subfield intersections of F_(2^15) and F_(2^9), the order20 group over F2,
and five R7 realizations at q=512 and32768. Binary polynomial quotients
are certified to be fields by enumerating a primitive element through all
nonzero classes. These are finite coordinate checks supporting the
uniform proofs. They do not enumerate all conjugate subfield groups in a
large Suzuki group, and do not certify every geometric axiom.

The full flag-transitivity problem remains outside this proof. Higher
composite field-degree shapes 7–10 require separate checks before being
counted as realized. Root's independent mathematical review found no gap
in Lemmas A–D, the shape4/6 construction, or LemmaE/TheoremF under the
stated classical Suzuki inputs. The [review record](phase5_suzuki_audit.json)
distinguishes this internal mathematical review from independent external
review, which has not occurred. The [intake record](phase5_suzuki_intake.json)
binds the source versions, proof and exact checker by hashes.
