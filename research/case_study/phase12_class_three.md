# Cyclic subgroup TPP for nilpotent groups of class at most three

10 October 2026. Private proof for independent review. Frozen phase11
artifacts are unchanged. The new step is a commutator argument for a
marked Frattini subgroup; the final powerful-group obstruction is retained
from the reviewed phase11 proof. No group classification is used.

**Theorem.** If G is a finite nilpotent group of class at most
three, and cyclic subgroups A,B,C have the triple product property, then

    |A||B||C| <= |G|.

Together with the already reviewed odd-order theorem, the proof below
also gives this bound whenever the Sylow 2-subgroup has class at most
three, without a class restriction on the odd Sylow subgroups.

## 1. A marked Frattini lemma

**Lemma.** Let P be a finite 2-group of class at most three. Suppose

    P=<a,b>,  K=Phi(P),  c in abK,
    K=<x,y,z>,  x=a^2, y=b^2, z=c^2.

Then K is powerful: [K,K] <= K^4, where K^4 is the subgroup generated
by all fourth powers of elements of K.

The assertion includes dependent images of x,y,z in K/Phi(K). It does
not assume TPP, equal cyclic orders, or an ordered factorization of K.

**Proof.** Factor P by the characteristic subgroup K^4. The Frattini
subgroup of the quotient is K/K^4, and its Frattini quotient is still
K/Phi(K), since K^4 <= K^2=Phi(K). It is enough to prove that the image
of K is abelian. Suppress bars for the rest of this proof. Thus K has
exponent dividing four.

Use [u,v]=u^(-1)v^(-1)uv and u^v=v^(-1)uv. Put

    d=[b,a],  e=[d,a],  f=[d,b].

Class at most three gives e,f in Z(P), P'=<d,e,f>, and

    K=<x,y,d,e,f>.

The collection identities are

    [x,d]=e^(-2),  [y,d]=f^(-2),
    [y,x]=d^4 e^2 f^2.

For the last identity, [b^2,a]=d^2 f, and taking the commutator with
a^2 gives [b^2,a^2]=(d^2 f)(d^2 f)^a=d^4 e^2 f^2.
Since d^4=e^4=f^4=1 in our quotient, all displayed commutators are
central involutions, and

    [K,K]=<e^2,f^2>.                                 (1)

In particular K has class at most two. A class-two group of exponent
dividing four has elementary abelian central square subgroup: the formula
(uv)^4=u^4 v^4[v,u]^6 gives [v,u]^2=1, and then [u^2,v]=1.
Consequently

    W=Phi(K)=K^2 <= Z(K),  exp(W) divides 2,
    V=K/W is an F_2-vector space of dimension at most three.   (2)

If dim V<=1, K is cyclic. If dim V=2 and K were nonabelian, its
alternating commutator map

    beta: V x V -> [K,K]

would have zero radical. Indeed, for a basis u,v its nonzero value
beta(u,v) makes each of u,v,u+v pair nontrivially with another basis
vector. Since e,f are central, their images would vanish in V. Then
e,f lie in W and have square one by (2), contradicting (1).
This covers dimensions at most two.

Suppose dim V=3. Now x,y,z form a basis. Let S,T be the actions of a,b
on V. The binary square-action lemma from
[phase11_abelian_frattini.md, section 4](phase11_abelian_frattini.md)
applies: K/W is abelian, c=abk for some k in K, and the same conjugation
and square identities hold in P/W. That lemma says either S=T=I, or

    im(S-I)=im(T-I)=L,

where L is one of the three coordinate lines <x>,<y>,<z>.
The images of e=[d,a] and f=[d,b] belong to im(S-I) and im(T-I),
respectively. If both images vanish, (2) again gives e^2=f^2=1,
and (1) finishes the proof.

Otherwise a nonzero central element e or f represents the line L.
By (2), the corresponding coordinate x, y or z differs from that
central element by an element of the central subgroup W. That
coordinate itself therefore lies in Z(K).

The three images aK,bK,cK are the three nonzero elements of P/K.
Any pair generates P, and their remaining product is the third modulo
K. We may thus permute a,b,c and arrange that the central coordinate
is x=a^2. Reapply the same collection identities with this labeling.
From [x,d]=1 obtain e^2=1; from [y,x]=1 and d^4=1 obtain f^2=1.
Equation (1) proves K abelian. Before quotienting, this says
[K,K] <= K^4. QED.

## 2. Why the lemma applies to a minimum counterexample

Suppose a finite 2-group of class at most three violates the cyclic TPP
bound, and choose such a P of minimum order. This class is closed under
subgroups and quotients. The following elementary reductions therefore
apply within this class, without requiring that all smaller 2-groups
satisfy the bound.

Every pair of factors generates P. If H=<A,B> were proper, minimality
for A,B,C intersect H, followed by the coset injection
C/(C intersect H) -> P/H as sets, would give the required bound.
The other pairs follow by permutation invariance of subgroup TPP.

Also each factor intersects Z(P) trivially. If a central order-two
subgroup Z0 lay in A, the images of A,B,C in P/Z0 would retain TPP:
absorb any resulting element of Z0 into the A factor. Their order
product and the group order both fall by two. This contradicts
minimality in the quotient. The same argument applies to B and C.

Thus P is noncyclic, two-generated, and |P:K|=4 for K=Phi(P).
The nontrivial cyclic factors have three distinct nonzero images in
P/K. Let r=|A||B||C|/|P|. Their squared subgroups lie in K and retain
TPP; minimality in K implies r<=2, so r=2. Consequently

    |A^2||B^2||C^2|=|K|.                            (3)

These three subgroups generate K: otherwise the same triple would
violate the inequality in its proper generated subgroup. Choose cyclic
generators a,b,c. The hypotheses of the marked Frattini lemma hold,
so K is powerful.

For completeness, the squared factors in (3) are all nontrivial. If
the cyclic orders are alpha>=beta>=gamma, a cyclic factor A avoiding
the center has a conjugate A^g intersecting it trivially: choose g moving
its unique involution. A maximal subgroup containing A is normal and
also contains A^g. Hence alpha^2 <= |P|/2. As |P|=alpha beta gamma/2,
we obtain 4alpha<=beta gamma and gamma>=4.

## 3. The retained powerful-group contradiction

The proof in [phase11_powerful_frattini.md, sections 4-6](phase11_powerful_frattini.md)
now applies verbatim to this minimum counterexample. Its relevant
assumptions are exactly the equality (3), generation by the three
squared factors, pair generation, avoidance of the center, and
powerfulness of K. Its use of minimum order was entirely in the
reductions already established above.

More explicitly, Lubotzky-Mann's ordered-factorization theorem for a
powerful group gives K=A^2 B^2 C^2. Only at this point does (3) make
this particular multiplication map bijective. Powerful power-subgroup
structure then gives dim K/K^2=3 and a nonzero, linear, P-equivariant
top-power map from K/K^2. The binary square-action lemma forces a
nonzero fixed top-power image of one coordinate. This is a nonidentity
element of A, B or C centralized by a and b, contradicting avoidance
of Z(P).

This proves the 2-group assertion. The frozen odd-prime theorem and
the Sylow direct-product argument prove the stated finite nilpotent
versions. QED.

## 4. Proof and status boundaries

The new argument is the marked Frattini lemma, including its
dimension-at-most-two case. The binary action lemma and the powerful
top-power obstruction are retained reviewed arguments. The published
powerful-group results are listed with exact source locators in
phase11_powerful_frattini.md; they are not re-proved here.

The argument neither assumes that TPP plus equality gives product-map
injectivity nor assumes that all subgroups of a powerful group are
powerful. The equality is used first only to prove generation by
minimality. No catalogue exhaustion, group-order cutoff, or nilpotency
class exceeding three is asserted. Full cyclic TPP for finite 2-groups
and the unrestricted Hou-Feng-Leemans conjecture remain unresolved.

Bounded searches on 10 October 2026 for the exact phrases "triple
product property" with "class three" or "class 3", and cyclic TPP
with nilpotency class, found the already recorded class-two work
[Murthy, arXiv:2602.15796](https://arxiv.org/abs/2602.15796), but did not
locate this class-three cyclic statement. That is a search limit,
not a novelty or priority determination. A separate independent written
audit records the review status; the group theorem is not fully formalized.

## 5. Focused checks and a strict extension of the previous family

The original [GAP/NQ script](phase12_class_three_check.g) first checks
the three collection identities in the free torsion-free nilpotent group
of class three on two generators. This is a check of the universal
collection calculation, rather than a collection of random finite tests.

It also constructs the class-three quotient R of the presentation

    <a,b | a^8=b^8=d^4=e^4=f^4=1>,
    d=[b,a], e=[d,a], f=[d,b].

The [exact transcript](phase12_class_three_check.log) gives |R|=4096
and Phi(R) of order 1024, exponent four and generator number five.
Moreover |Phi(R)'|=4 while Phi(R)^4=1. Thus Phi(R) is not powerful.
The new theorem covers R, whereas the hereditary-powerful-Frattini
hypothesis does not. This is a precise sense in which the class-three
theorem extends the previous sufficient condition. R is not claimed
to violate TPP; it does not satisfy the marked hypothesis of section 1.

Reproduce with `gap -q phase12_class_three_check.g`, using GAP and the
NQ package. The recorded versions are GAP 4.15.1 and NQ 2.5.11. The
script uses no SmallGroups catalogue, and neither its finite witness
nor its collection check replaces the uniform written argument above.
