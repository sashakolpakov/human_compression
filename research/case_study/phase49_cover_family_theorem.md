# Two minimal regular covers in the odd-prime tight family

Private author manuscript, 10 October 2026. The all-parameter proof below is new work in this investigation, subject to review. Finite probes are diagnostics and are not used to infer the theorem. No literature-priority claim is made.

## 1. Exact source contract and retained input

Fix an odd prime p, an integer α≥2, and k∈{1,...,p−1}. Put q=p^α, h=p^(α−1), d=kh. Let P=P(p,α,k) be the marked tight chiral rank-four polytope whose rotation group has generators a,b,c and presentation

    a^(2p)=b^q=c^(2p)=1,
    (ab)^2=(bc)^2=(abc)^2=1,
    b a²=a² b^(1+d),        c² b=b^(1+d)c².       (5)

The retained source is Cunningham–Pellicer, *Tight chiral polytopes*, author version [arXiv:2009.04566](https://arxiv.org/pdf/2009.04566), Table 2 and Theorem 4.7 (printed pages 22–26). That theorem identifies this exact presentation with the tight chiral polytope for every parameter stated above. We retain its existence and its intersection property, exact marked orders, and tight order

    |P|=(2p)q(2p)=4p²q.

Equivalently, every element has a unique normal form a^i b^j c^ℓ with 0≤i,ℓ<2p and 0≤j<q. The normal-form assertion follows from the retained tightness, not from experimental enumeration. We do not reprove the earlier classification of all tight polytopes. The source's equal-parameter condition k1=k2 is essential; (5) uses that equality. There is no p=2 or k=0 case here.

We also retain the standard string-C/C+ recognition and marked group/polytope correspondence, and the universal property of the smallest regular maniplex cover. Every additional group order, quotient, and intersection needed for the new covers is proved below. No source assertion of multiple minimal covers is used.

**Theorem.** For every parameter in (5), P has two nonisomorphic, rank-preserving minimal regular polytope covers Q and Q′, interchanged by duality. Their rotation groups have order 4p⁴q. The smallest regular maniplex cover R has rotation order 4p³q and is nonpolytopal; each of Q,Q′ covers R with degree p.

The rotational mix H=Q⋄Q′ is polytopal, has order 4p⁵q, and maps onto R with elementary abelian kernel C_p². Exactly two minimal covers of P are quotients of H: Q and Q′. The join of all finite admissible universal kernels over the monodromy kernel of P is that full monodromy kernel. This last claim is join-density for this family, not for arbitrary polytopes.

## 2. Coordinate identities and the smallest regular cover

We use right conjugation z^g=g⁻¹zg and [z,g]=z⁻¹z^g. In P put x=b^h, u=a² and y=c². Then x,u,y have order p, x commutes with u and y, and

    x^a=x⁻¹,    x^b=x,      x^c=x⁻¹,
    u^b=u x^(−k),
    y^b=y x^k,  y^a=y⁻¹x^k,  y^(a⁻¹)=y⁻¹x^(−k).       (6)

Here is a derivation, so no chirality-group classification is needed for these identities. Since d²≡0 (mod q), the first extra relation in (5) also gives u b=b^(1−d)u. Using (ab)²=1, we obtain

    a b⁻¹=b^(1−d)a³,
    a b^d=b^(1−d)a³ b^(1+d)=b^(−d)a.

As k is nonzero modulo p, b^d generates ⟨x⟩, so a inverts x. The presentation (5) is preserved by a↦c⁻¹,b↦b⁻¹,c↦a⁻¹: the two extra relations are exchanged after inversion, and the rotation relations are preserved. Thus this assignment is an involutory marked duality, and the dual argument shows that c inverts x. Consequently u and y centralize x. Reordering the extra relations gives u^b=u x^(−k) and y^b=y x^k. The involution ab inverts c because (abc)²=1; hence y^(ab)=y⁻¹, and conjugating back by b yields y^a=y⁻¹x^k. Inverting the resulting automorphism on ⟨x,y⟩ gives the final identity.

Write P0=P/⟨x⟩. This quotient exists because (6) proves normality. Its marked generators admit an automorphism

    a↦a⁻¹,   b↦a²b,   c↦c.                     (7)

To check this directly, note that in P0, a² commutes with b and c². The second commutation follows by applying y^a=y⁻¹ twice. Also p divides h, so (a²b)^h=1 in P0. Thus all generator-order and extra relations are preserved. The three square relations are preserved because a′b′=ab, a′b′c′=abc, and b′c′=a²(bc) is an involution: bc inverts a by (abc)²=1. Applying (7) twice fixes every generator, proving it is an automorphism; call it μ0.

Now form the marked mix R⊆P×P with generators

    A=(a,a⁻¹),     B=(b,a²b),     C=(c,c).

Swapping the coordinates is the mirror automorphism μ of R: μ(A)=A⁻¹, μ(B)=A²B and μ(C)=C. Thus R is the smallest regular maniplex cover, by the usual intersection-of-a-kernel-with-its-mirror construction. Equation (7) places R inside the twisted fiber product over P0, of order p|P|.

For completeness, it is the entire twisted fiber product. The relation (ab)²=1 gives a²b=a b⁻¹ a⁻¹. Since a inverts x, we obtain

    B^h=(x,x).                                  (8)

Moreover (u b)^d=x^k, so (u b)^(1+d)=u b^(1+d). Since u b u⁻¹=b^(1−d), the literal facet relator

    B A² (A² B^(1+d))⁻¹

has coordinates (1,x^(−2k)). Since p is odd and k≠0, it generates 1×⟨x⟩. The first projection of R is onto P, so |R|≥p|P|, attaining the upper bound. Therefore

    |R|=4p³q,
    R={ (g1,g2) : g2 mod ⟨x⟩=μ0(g1 mod ⟨x⟩) }.

An explicit unique normal form is A^i B^j C^ℓ (1,x)^t with the same ranges for i,j,ℓ as in P and 0≤t<p. Uniqueness follows first from projection to P and then from the order of (1,x).

## 3. The two end groups and a normal closure

Let F=⟨A,B⟩ and V=⟨B,C⟩. Define

    Y=C²=(y,y),       Z=(x^k,x^(−k)).

Using (6) in each coordinate gives

    [C²,B]=Z=[A²,B]⁻¹.                          (9)

For the second coordinate in [C²,B], use y^(a²)=y x^(−2k). For [A²,B], use u^b=u x^(−k) and the fact that u commutes with x. This proves (9) without an order argument. In particular Z lies in both F and V. Together with (8), it generates all of ⟨x⟩×⟨x⟩, since the determinant −2k is nonzero modulo p. Thus the first projections of F and V have exactly the full kernel 1×⟨x⟩. Their images are the source facet and vertex rotation groups, each of order 2pq. It follows that

    |F|=|V|=2p²q,
    F∩V=⟨B,Z⟩=⟨B⟩×⟨Z⟩,     |F∩V|=pq.        (10)

Indeed the intersection projects into ⟨a,b⟩∩⟨b,c⟩=⟨b⟩; conversely both ends contain its full preimage ⟨B,1×x⟩. The latter is ⟨B,Z⟩ by (8). The cyclic subgroup ⟨B⟩ has order q and meets ⟨Z⟩ trivially: if B^j=Z^t then j is divisible by h, (8) makes both coordinates equal, and oddness of p forces t=0 and j=0 modulo q.

The local cyclic intersections are trivial by projection to P and the exact orders of A,B,C. The mirror μ preserves F, so F is a directly regular polyhedron group by rank-three recognition. V is also directly regular: the intrinsic mirror ν(v)=A⁻¹μ(v)A sends B↦B⁻¹ and C↦B²C, as follows from the rotation relations. In particular (10) proves that R fails the required rank-four intersection equality and is nonpolytopal.

The subgroup W=⟨Y,Z⟩ is elementary abelian of order p². Its generators commute and have order p; if Y^i Z^j=1, then y^i=x^(−kj) in P. The source cyclic intersection ⟨b⟩∩⟨c⟩=1 gives i=j=0. The action table is

| operator | Y | Z |
|---|---|---|
| conjugation by A | Y⁻¹Z | Z⁻¹ |
| conjugation by B | YZ | Z |
| conjugation by C | Y | Z⁻¹ |
| mirror μ | Y | Z⁻¹ |

Hence W is normal and mirror-invariant. Equation (9) shows that W is exactly the normal closure of C². Moreover

    W≤V,       W∩F=⟨Z⟩,       W∩⟨B⟩=1.         (11)

For W∩F, project Y^iZ^j to P. Membership in the facet forces c^(2i) to lie in that facet, hence to be trivial by the source IP. The last equality then follows from (10).

## 4. A trivial extension and the exact common quotient

Adjoin an involution t to F implementing μ|F, and put

    T=F⋊⟨t⟩,      a_T=A,  b_T=B,  c_T=tAB.

The three elements r0=t,r1=tA,r2=tAB are involutions with r0r2=AB an involution. Therefore the marked triple (A,B,c_T) satisfies all three rank-four rotation square relations, and c_T has order 2. This is the rotation group of the trivial rank-four extension of the regular facet F. One can check its polytopality directly: its facet is F, its vertex group ⟨B,c_T⟩ is dihedral of order 2q, and this vertex group meets F in ⟨B⟩ because c_T lies outside the index-two subgroup F. The local cyclic intersections are trivial. Conjugation by t is the required mirror, fixing c_T, so T is directly regular. In particular |T|=2|F|=4p²q.

Let J=⟨Z⟩≤F≤T. Its conjugation actions by (A,B,c_T) are respectively (−1,+1,+1), and its mirror action is −1. The first two follow from the table; the third follows from

    Z^(c_T)=(Z^t)^(AB)=(Z⁻¹)^(AB)=Z.

Thus J is a normal mirror-invariant subgroup of order p.

There is an exact marked isomorphism

    R/W ≅ T/J.                                  (12)

Here is a normal-form proof. By (11), the image of F in R/W is F/J; its index is two, since |R/W|=4pq and |F/J|=2pq. The image of C lies outside it (otherwise R/W would be generated by F/J), and has square 1. In any quotient with C²=1, the rotation relations give

    C B C=B⁻¹,          C A C=A B².

Exactly the same formulas hold for c_T in T. Both quotient groups therefore have the unique forms f C^ε or f c_T^ε, with f∈F/J and ε∈{0,1}, and the same multiplication. Matching these forms proves (12), including the marked generators.

It is also the largest common marked quotient of R and T. Any common quotient must kill C² in R, since c_T²=1; it therefore factors through R/W, whose common-quotient property was just proved. This argument uses the actual normal closure W, not only its order.

We use the elementary mix/fiber-product lemma: if two marked groups G1,G2 have largest common marked quotient U, their marked mix is the full fiber product G1×_U G2. To recall the proof, in the generated subdirect product S, the two projection kernels determine normal subgroups N1≤G1,N2≤G2, and S consists exactly of pairs with matching cosets under the induced isomorphism G1/N1≅G2/N2. This quotient is common. Conversely any common quotient identifies every pair of marked words represented by an element of S, so factors through it. Thus it is the largest common quotient and gives the claimed fiber product.

## 5. The first polytopal cover and its minimality

Set Q=R⋄T. By (12) and the fiber-product lemma, Q→R has kernel J and degree p, so

    |Q|=4p⁴q.

Its facet is the graph of the identity copy of F inside R and T, hence maps isomorphically onto F. Its vertex group is the graph of the marked homomorphism

    V→V/W ≅ ⟨B,c_T⟩,

where V/W is dihedral of order 2q by (11). Hence both end restrictions of Q→R are injective.

To compute their intersection, write an element of F∩V uniquely as B^j Z^s using (10). Its facet lift has T-coordinate B^j Z^s; its vertex lift has T-coordinate B^j, since Z∈W. The two lifts agree exactly when s=0. Thus the intersection in Q is the medial ⟨(B,B)⟩, and all local cyclic intersections follow from the isomorphic ends. Recursive C+ recognition proves Q polytopal. Both factors R and T have mirror automorphisms, which preserve the generated mix, so Q is directly regular.

The covering kernel J in Q has the conjugation character

    A : −1,       B : +1,       C : +1.           (13)

This is read from its T-coordinate; the R-coordinate is trivial. Its mirror action is −1.

Finally Q is a minimal regular polytope cover of P among **all** regular covers of P. Every regular cover of P factors through the smallest regular maniplex R. Any proper marked quotient of Q that still covers P is therefore intermediate between Q and R. Their index is the prime p, so the only possibilities are Q and R. The latter is nonpolytopal by (10). A quotient of a finite group cannot introduce an infinite-cover exception.

## 6. The distinct dual cover

The explicit duality of (5) proves that P is self-dual. Duality preserves regularity, polytopality, and covers; it therefore takes its smallest regular maniplex cover to the smallest regular maniplex cover of its dual. By the universal property, the latter identifies canonically, as a marked cover, with R. Consequently the dual of Q gives another degree-p regular polytope cover Q′→R→P, with the same order and the same global minimality proof. Dualizing the injective end restrictions shows that Q′→R is injective on both ends.

The kernel character of Q′ is obtained by reversing and inverting the rotation generators in (13):

    A : +1,       B : +1,       C : −1.           (14)

These characters differ because p is odd. A marked isomorphism Q≅Q′ would commute with the unique marked maps to R and identify their cyclic kernels. That would identify the conjugation actions (13) and (14), which is impossible: inversion on C_p is not the identity. Thus Q and Q′ are nonisomorphic under rank-preserving polytope isomorphisms. No equivalence by permutation of ranks is intended; they are duals.

The mirror on the Q′ kernel is +1. Indeed, on the Q kernel the full reflection r0 acts by −1. Since a=r0r1,b=r1r2,c=r2r3 and its rotation signs are (−,+,+), the reflection signs are (−,+,+,+). The dual first reflection is the old r3. This also makes every normal/mirror condition in the next section explicit.

## 7. The shared cover interval and global join-density

Let H=Q⋄Q′ and let L be the kernel of H→R. It is a subdirect subgroup of J×J′≅C_p²: each coordinate projection of L is onto because H projects onto Q and Q′. A proper subdirect subgroup would be the graph of an isomorphism between the two one-dimensional modules. The different A-actions in (13) and (14) rule this out. Thus

    L=C_p²,       |H|=4p⁵q.

Its two coordinate axes are distinct one-dimensional characters. They are invariant under conjugation and mirror, with the signs just established. Every end subgroup of H projects isomorphically onto the corresponding end of R, because each is the graph of the two injective end identifications for Q and Q′. The projection H→Q is consequently injective on both ends. Since Q is polytopal, lifting its end intersection proves the end intersection in H is the medial subgroup; local intersections follow as well. The componentwise mirror makes H directly regular. Thus the locally injective hypotheses of phase46 apply.

Both axes are admissible kernels: their quotients are Q and Q′, in the opposite projection order. The whole L is not admissible since H/L=R is nonpolytopal. There are no other nonzero proper conjugation-invariant subspaces: two distinct one-dimensional characters over F_p have only their coordinate axes as invariant lines. Therefore the interval has exactly two maximal admissible kernels and exactly the claimed two minimal covers among quotients of H. Their join is L. Write U=W4⁺ for the universal rotation group and K=ker(U→R). Pullback under U→H sends the join of the two axes to K. The corresponding full regular covers use the same relation kernels inside U≤W4; mirror stability is exactly the additional condition making these kernels normal in W4. Both pullbacks are finite admissible universal kernels, so the join of all such kernels is K, the kernel of W4→Mon(P). Here the full monodromy group is the reflection extension of the rotational R. Every cover of the orientable P is orientable, since its flag graph maps into the bipartite flag graph of P; thus the universal cover kernels under discussion do lie inside U.

This proof also recovers the support-hypergraph form of phase46: the defect set has size p by (10), and meets neither axis nontrivially because their quotients are polytopal. Every nonidentity defect has support on both axes, so the hypergraph has the single edge {1,2}. It is not necessary to assume the defect set is a subgroup.

## 8. Verification and boundaries

The exact GAP file `phase49_cover_family_check.g` rebuilds the bare source presentation, forms the mirror mix, and constructs the facet's trivial extension by a semidirect product. It checks eight cases: p=3 with α=2 or 3 and both k, and p=5 with α=2 and all four k. The respective orders (P,R,T,Q,Q′,H), independent of k within each tested type, are

    (324,972,324,2916,2916,8748),
    (972,2916,972,8748,8748,26244),
    (2500,12500,2500,62500,62500,312500).

All have kernel C_p², injective ends, polytopal Q,Q′,H, the distinct sign characters, and normal closure ⟨C²⟩^R≅C_p². The certificate also checks the literal coordinate identities, actual subgroup equalities, source and cover dualities, and the marked quotient isomorphism (12). These calculations cross-check the proof; the all-parameter conclusion rests on §§2–7. The safe runner `phase49_cover_family_check.py` records exact finite diagnostics with fresh outputs. The earlier exploratory probe is excluded from the certificate intake.

This resolves the proposed multiplicity assertion for the first specified family, conditional on the openly retained source construction of P and geometric correspondence. It does not classify all minimal covers of a member of that family, settle the other four source families, or prove the arbitrary-monodromy conjecture. No additional Lean formalization is claimed for this family theorem. The source-status search in phase44 remains bounded and does not establish priority.
