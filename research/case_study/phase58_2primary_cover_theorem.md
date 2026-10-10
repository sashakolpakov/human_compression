# A uniform obstruction in the first 2-primary tight family

Private author manuscript, 10 October 2026. This is a theorem about one specified cover construction, not a solution of the general multiple-minimal-cover question. The source family is retained; all claims about the covers constructed here are proved below. Finite extension searches are separately labeled. No historical-priority claim is made.

## 1. Source and scope

Let β≥5, q=2^β, h=q/4, and ε1,ε2∈{−1,1}. We retain Cunningham–Pellicer, *Tight chiral polytopes*, author version arXiv:2009.04566v1, Table 2 row Γ2 and Theorem 4.8, as the construction of the tight chiral polytope P with rotation presentation

    a^8=b^q=c^8=1,
    (ab)^2=(bc)^2=(abc)^2=1,
    b a²=a² b^(1+ε1h),       c² b=b^(1+ε2h)c².       (1)

Thus |P|=64q, the marked orders are (8,q,8), the end groups have order 8q, and their intersection is ⟨b⟩. Tightness gives the unique normal form a^i b^j c^k, 0≤i,k<8 and 0≤j<q. The earlier atomic classification, local polyhedron constructions, and the source's Lemma 4.6 and Corollary 4.5 remain retained dependencies of this source input. We do not count the source classification as newly proved. The primary PDF was reopened at Table 2 and Theorem 4.8 for this package; β=5 is included, not excluded by an asymptotic congruence.

We retain standard marked rotation-group/string-C recognition, the correspondence with regular polytopes, and the smallest regular maniplex cover as the mix with the mirror. We use rank-preserving marked maps throughout. Orders below are rotation-group orders unless “full” is specified.

The construction by mixing a smallest regular cover with trivial extensions of a regular facet and vertex figure is motivated by Cunningham's earlier finite example in *Chiral polytopes whose smallest regular cover is a polytope* and by the odd-prime family analyzed in phase49. Attribution is to that strategy; the present claim is the following exact obstruction, with no assertion that it was historically unknown.

**Theorem.** For every parameter in (1), the smallest regular maniplex cover R is nonpolytopal and has order 128q. The facet and cofacet trivial-extension mixes Qf and Qv are polytopal covers of R with cyclic kernels of order four. Each has a unique minimal regular quotient over P, of degree two over R. These two quotients are the **same marked polytope S**, of order 256q.

The mix H=Qf⋄Qv is polytopal, has order 1024q, and has kernel C4×C2 over R. Exactly one minimal cover of P is a quotient of H: S. This does not prove that P has only one minimal regular cover. Covers outside this finite interval are not classified.

## 2. The mirror mix and its end intersection

Use right conjugation z^g=g^−1zg and [z,g]=z^−1z^g. Put x=b^h, u=a² and y=c² in P. Then x,u,y have order four, and

    x^a=x^c=x^−1,       x^b=x,
    [x,u]=[x,y]=1,
    u^b=u x^−ε1,
    y^b=y x^ε2,         y^a=y^−1x^ε2,
    y^u=y x^−2ε2=y x².                           (2)

Here are algebraic derivations of the needed facts. Write d=ε1h. Since d²≡0 modulo q, the first extra relation gives u b=b^(1−d)u. Combining it with (ab)²=1 yields

    a b^−1=b^(1−d)a³,
    a b^d=b^(1−d)a³ b^(1+d)=b^−d a.

As d=±h, a inverts x. The substitution a↦c^−1, b↦b^−1, c↦a^−1 interchanges the two extra relations and their parameters ε1,ε2; the same argument gives inversion by c. This uses duality between the two parameter presentations, not self-duality for unequal parameters. Reordering the extra relations gives the two conjugation formulas by b. Since ab inverts c, conjugating y^(ab)=y^−1 back by b gives y^a=y^−1x^ε2. Applying this twice gives the last formula. In particular x² is a central involution in P.

The universal mirror on rotation generators is

    a↦a^−1,     b↦a²b,     c↦c.                  (3)

It preserves the three rotation square relations and all three generator orders: a²b=a b^−1a^−1. Under (3), each literal extra relator in (1) has value x². For the first relator, reordering u b u^−1=b^(1−ε1h) gives x^−2ε1=x². For the second, use y u=u y x², y b=b^(1+ε2h)y, and (u b)^(1+ε2h)=u b^(1+ε2h); the latter follows from (u b)^h=x. Consequently (3) induces an involutory automorphism of P/⟨x²⟩.

In P×P set

    A=(a,a^−1),   B=(b,a²b),   C=(c,c),
    R=⟨A,B,C⟩,    κ=(1,x²).

The mirror μ swaps the two coordinates. Thus R is the smallest regular maniplex cover. It lies in the twisted fiber product over P/⟨x²⟩, of order 2|P|. Each of the two literal extra relators evaluated at A,B,C equals κ, so κ∈R. The first projection is onto P; hence R is the entire fiber product and |R|=128q. This also gives a unique normal form A^iB^jC^kκ^e with the ranges from §1 and e∈{0,1}.

Let F=⟨A,B⟩, V=⟨B,C⟩, Y=C² and

    Z=(x^ε2,x^−ε2)=[C²,B].

Equation (2) also gives [A²,B]^−1=Z^(ε1ε2). Both ends contain κ and project onto the corresponding source end. Therefore |F|=|V|=16q. Moreover

    B^h=(x,x),       Z²=B^(q/2)≠1,
    F∩V=⟨B,Z⟩,      |F∩V|=2q.                  (4)

Indeed Z B^(−ε2h)=κ, so ⟨B,Z⟩ is the entire preimage of ⟨b⟩; the source IP shows that no other element can be in both ends. R consequently fails the rank-four IP. The cyclic intersections inside each end are trivial by projection to P and the exact marked orders. The mirror preserves F. The intrinsic mirror on V is A^−1μ(−)A and sends B to B^−1 and C to B²C. Thus both ends are regular polyhedron rotation groups.

## 3. A cyclic-four extension and its reduction

The subgroup W=⟨Y,Z⟩ is C4×C4. The generators commute, and Y^iZ^j=1 forces c^(2i)=b^(−ε2hj) in P, so the source cyclic intersection makes i,j divisible by four. Its action table is

| operator | Y | Z |
|---|---|---|
| conjugation by A | Y^−1 Z | Z^−1 |
| conjugation by B | Y Z | Z |
| conjugation by C | Y | Z^−1 |
| mirror μ | Y | Z^−1 |

Thus W is the normal closure of C², is mirror invariant, and

    W≤V,     W∩F=J:=⟨Z⟩,     W∩⟨B⟩=⟨B^(q/2)⟩.       (5)

For W∩F, projecting Y^iZ^j to P forces i=0 modulo four by the source IP. The final equality follows from (4). In particular J has order four; it is not an elementary abelian line independent of ⟨B⟩.

Form T=F⋊⟨t⟩, where t is an involution acting by μ|F, with marks A,B,D=tAB. It is the trivial rank-four extension of the regular facet. Directly, D²=1, the rotation square relations hold, its facet is F, and its vertex group ⟨B,D⟩ is dihedral of order 2q and meets F in ⟨B⟩. Thus T is polytopal, regular, and has order 32q. On J its rotation actions (A,B,D) are (−1,+1,+1), and its mirror action is −1; hence J is normal and mirror invariant.

There is a marked isomorphism R/W≅T/J. Each side has an index-two subgroup F/J and a complementary involution, the image of C or D, acting by

    B↦B^−1,       A↦AB².

Their unique forms fC^e and fD^e, f∈F/J, e∈{0,1}, have identical multiplication. This proves the isomorphism including all marked generators. It is the largest common marked quotient, because every common quotient must kill C² in R. A generated marked subdirect product is the fiber product over its largest common quotient: its projection kernels give the common quotient by the elementary subdirect-product argument, and every other common quotient factors through it. Consequently

    Qf=R⋄T,       |Qf|=512q,       ker(Qf→R)≅J≅C4.       (6)

The facet of Qf is the graph of F and maps injectively to both factors. Its vertex is V⋄⟨B,D⟩. The latter mix has common quotient V/W, which is dihedral of order q: C becomes an involution and B has order q/2, by (5). Hence the vertex projection to V has kernel

    M=⟨(1,Z²)⟩=⟨(1,B^(q/2))⟩,

of order two. The facet projection has trivial kernel. To verify IP in Qf, project an end-intersection element to T. It lies in ⟨B⟩ in T; since the facet maps injectively to T, its lift is exactly the corresponding medial power. Local cyclic intersections follow by projection to the source. Thus Qf is polytopal, and the factor mirrors give its regularity.

Set S=Qf/M. Both end restrictions S→R are now injective. The quotient remains polytopal. For clarity, the elementary quotient-intersection criterion says that q(E)∩q(F)=q(E∩F) exactly when N∩EF=(N∩E)(N∩F), for N=ker q. Here N=M is contained in the vertex and meets the facet trivially, so both sides equal M. A proof of the criterion is immediate from q(e)=q(f) iff ef^−1∈N, with the latter element factored through the two kernel intersections. The resulting local ends are the original regular ends F,V of R. Hence |S|=256q and S→R has degree two. Since R is not polytopal, this prime-degree cover is minimal among all regular polytopal covers of P: every regular cover of P maps to its smallest regular maniplex R, and there is no proper intermediate group between S and R.

The cyclic kernel of Qf→R has only one nontrivial proper subgroup, namely M. Thus S is also the unique minimal quotient of Qf over P. The character (−,+,+) reduces to the trivial character on J/J². This explains why the odd-prime character separation cannot simply be repeated in characteristic two; the following exact presentation proves the stronger coincidence of the two reductions.

## 4. Both reductions are the same marked cover

For arbitrary marked generators a,b,c satisfying the power and square relations of (1), write

    r1=b a²(a² b^(1+ε1h))^−1,
    r2=c² b(b^(1+ε2h)c²)^−1.

Then S has the exact presentation consisting of those power and square relations together with

    r1²=r2²=1,       [ri,a]=[ri,b]=[ri,c]=1  (i=1,2).       (7)

To prove this, view S as R⋄(T/J²): the evident map Qf→R×(T/J²) has kernel M. In R, both ri equal the central involution κ. In T/J², r1 is the image of κ and r2 is B^(−ε2h)=B^h. The latter is a central involution: A and D invert B^h before quotienting and its square B^(2h)=Z² is killed. The element κ commutes with F, and μ(κ)=κB^(2h), so κ is central also in T/J². Therefore (7) holds in S. Conversely the group presented by (7) has a central subgroup ⟨r1,r2⟩ of order at most four and quotient P. Its order is at most 4|P|=256q, which is attained by S. The surjection is an isomorphism.

The presentation (7) is preserved by reversing and inverting the marks and swapping ε1,ε2. Explicitly, if r2 is central, then

    b^−1 c^−2 b^(1+ε2h)c² = r2^−1;

this is the first extra relator in the reversed presentation. The second follows by the reverse calculation with r1. The square and power relations are preserved as well. Applying the facet construction to the dual parameter presentation and dualizing back is exactly the cofacet trivial-extension construction Qv. The preceding characterization therefore proves that its reduced quotient is the **same marked group (7)**, not merely a group of the same order or a cover with the same kernel character. The two reduced covers are isomorphic under a rank-preserving marked isomorphism commuting with R.

## 5. The complete interval under the shared mix

Put H=Qf⋄Qv and L=ker(H→R). Both cyclic-four kernels reduce onto the same kernel of S→R, so

    L≤{(i,j)∈C4×C4 : i≡j (mod 2)}.               (8)

Each projection of L onto C4 is onto. A proper subdirect subgroup of order four would be the graph of an automorphism of C4. The rotation action of A on the first factor is inversion and on the second is identity; this rules out such a graph. Therefore equality holds in (8), L≅C4×C2, and |H|=8|R|=1024q. Write

    E=2C4×2C4≤L,       |E|=4.

The quotient H/E is S. The kernel of H→S meets the facet in 0×2C4 and the vertex in 2C4×0: on one side the corresponding raw cover has an injective end projection to S, while the other has the order-two kernel described in §3, and the generated end projects onto both factors. These two intersections meet trivially. Projecting an end-intersection element to S and removing its unique medial power consequently gives the identity. The local cyclic intersections follow from projection to R and then P. Thus H is polytopal and regular.

Every proper conjugation-invariant subgroup N<L is contained in E. Indeed, an element of L outside E has both coordinates odd. Subtracting its conjugate by A produces (2,0), and subtracting its conjugate by C produces (0,2). Hence any invariant subgroup containing that odd element contains E and the element, and equals L. Every subgroup of E is invariant under the rotation group and mirror, since all the relevant actions are coordinate inversions; no extra rank permutations are being allowed.

The subgroup E is admissible because H/E=S is polytopal. The whole L is not admissible because H/L=R is not polytopal. All proper admissible invariant subgroups are contained in E. Therefore E is the unique maximal admissible subgroup, and S is the unique minimal cover of P among quotients of H. This proves the uniform obstruction claimed in §1. It proves neither global uniqueness nor the failure of global join-density.

## 6. A small presentation and finite extension diagnostics

A useful exact presentation of R follows from §2. Start with the power and rotation square relations of (1), and replace its two extra relations by

    r1=r2,       r1²=1,       [r1,a]=[r1,b]=[r1,c]=1.       (9)

The presented group has central kernel of size at most two over P, while R realizes its nontrivial kernel κ. Thus (9) presents R exactly. Substituting a=r0r1, b=r1r2, c=r2r3 into (9), and imposing the four involution relations and nonadjacent commutations on r0,...,r3, presents the full reflection extension of R. Its rotation subgroup has the bound just proved; the actual reflection extension supplies equality. The use of r1 both as a relator label above and as a reflection in this substitution is purely local notation; the certificate calls the extra relators w1,w2.

For a finite marked 2-group G with full presentation W/⟨⟨w1,...,wk⟩⟩, where W already imposes the involution/string relations, define E by retaining W and requiring every wi to be central of order dividing two. Its kernel over G is central elementary abelian, generated by the images of the wi. It is finite. If G has lower exponent-two central class c, E has class at most c+1. Thus a p-quotient computed through class c+1 is the whole presented E, not an unspecified initial quotient. Every marked central elementary-abelian extension of G satisfying those same involution/string relations is a quotient of E. Hyperplane quotients of its kernel enumerate all marked double covers of G; all kernel subgroups enumerate the entire central-elementary-abelian interval. This is an exact finite search boundary, not a search over all covers.

The exact finite certificate fixes **β=5 and ε1=ε2=+1**. It constructs the full R of order 8192 and lower exponent-two central class five. The central extension above has order 131072 and kernel C2^4. Of its 15 hyperplane quotients, exactly one is polytopal. Of all 67 kernel subgroups, exactly four give polytopal quotients; their kernel orders are 2,4,4,8. There is one maximal admissible kernel, of order eight. All polytopal quotients in this interval therefore cover the same double cover S. In particular two of these quotients have central V4 kernel over R.

The remaining degree-four possibilities can also be exhausted by bounded relative presentations. A kernel of order four is either C4 or V4 and is abelian, so conjugation factors through the full R.

* For a C4 kernel, fix its action character χ:R→{±1}. There are at most the sixteen assignments to the four reflection generators, and all sixteen are tested. Retain W and require wi^4=1, pairwise commutation of the wi, and wi^rj=wi^(χ(rj)). The kernel is an abelian group of exponent dividing four generated by the wi. Its conjugation action is the chosen scalar character. Its lower exponent-two central filtration has at most two nontrivial layers, so the presented extension has class at most c+2. Every marked extension with that cyclic kernel action is a quotient. In the resulting finite abelian kernel L, enumerate all surjections L→C4, identify duplicate kernels, and take those quotient groups. This lists every cyclic-four kernel extension for this character, once as a marked quotient. Its unique normal subgroup of order two supplies the only possible proper intermediate quotient over R; the certificate checks that quotient's IP whenever the degree-four cover is polytopal.
* For a noncentral V4 kernel, the image of the 2-group R in Aut(V4)≅S3 has order two. In a suitable basis its nonidentity action is the single Jordan involution. Fix one of the fifteen nonzero characters χ:R→C2, written as bits χj on the reflections, and choose a reflection rp with χp=1. Put vi=[wi,rp]. Require wi²=vi²=1, pairwise commutation of the wi, every vi central, and [wi,rj]=vi^(χj). The kernel is elementary abelian, generated by the wi and vi, and again has at most two relative central layers. Computing through class c+2 therefore gives the whole presented extension. Enumerate every codimension-two subgroup of its kernel, retain those normal in the extension, and exclude central quotient kernels, which were already covered. This enumerates all noncentral V4 kernel extensions with this action. A noncentral V4 has exactly one invariant line under that Jordan action. The certificate checks the quotient by this line whenever the degree-four extension is polytopal.

In both constructions the images of the wi normally generate the kernel, so the displayed commutation and action relations prove the claimed finite bounds; finiteness is not being inferred from termination of a p-quotient algorithm. Every kernel of index four in an elementary abelian group lies in a hyperplane and is a hyperplane of that hyperplane, which justifies the explicit two-step enumeration. Duplicate subgroup kernels are removed. No untested normal quotient is omitted. Different action characters cannot give the same marked extension, since its action on its abelian kernel is intrinsic. Changes of basis for a fixed action identify quotient maps with the same kernel and do not add new marked covers.

The result is one polytopal marked degree-two cover, sixteen polytopal cyclic-four covers, two polytopal central-V4 covers, and eleven polytopal noncentral-V4 covers. **Every one of the twenty-nine degree-four covers has a proper polytopal quotient of degree two.** By the complete degree-two computation this quotient is S. Consequently S is the only minimal regular polytopal cover in this sample among covers having degree two or four over R. This is a finite theorem supported by the bound exact certificate, not an all-parameter degree-four classification.

The IP check on four involutory string generators g0,...,g3 is recursive: the two rank-three end groups have their adjacent-dihedral intersections equal to the common involution, and their mutual intersection is ⟨g1,g2⟩. The marked images in R ensure nontrivial and distinct generators and exact rank-two nondegeneracy. The defining W relations ensure all nonadjacent commutations. Thus the checks are exactly string-C recognition, not merely a group-order filter. All proper intermediate normal kernels in each tested prime-square case are accounted for as described above. The universal property of R then gives the stated global minimality or nonminimality over P, within the tested degree scope.

The standalone GAP program `phase58_2primary_cover_check.g` separately rebuilds the bare presentation (1) for β∈{5,6} and **all four** pairs of signs. It verifies the orders, literal coordinate identities, independent central relators in S, end IP and mirrors, exact normal closure, the equality of the reduced marked covers by their mix order, and the full normal-and-mirror-invariant quotient interval under H. These eight finite checks cross-check §§2–5; the uniform theorem follows from the written proof, not interpolation.

The standalone GAP program `phase58_2primary_cover_extension_check.g` performs the complete degree-two/four sample computation just described. The safe runner `phase58_2primary_cover_check.py` uses fresh output paths, checks explicit expected rows, and verifies the earlier bound source packages before and after execution. The exploratory files with `_probe` in their names are excluded from the certificate.

The other three 2-primary presentation families have not been analyzed here. No claim is made about higher-degree kernels, odd-order kernels, all global minimal covers, or global join-density for this family. The Cunningham multiple-minimal-cover question remains unresolved by this package outside the earlier odd-prime subfamily. No complete current-literature or historical-priority claim is made.
