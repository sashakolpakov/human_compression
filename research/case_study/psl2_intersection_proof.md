# Proposed proof of Leemans–Moerenhout–O'Reilly-Regueiro Conjecture 6.2

Status: original derivation in this session, with internal agent audit; not externally peer reviewed. Novelty remains subject to literature verification.

Source: D. Leemans, J. Moerenhout and E. O'Reilly-Regueiro, *Projective linear groups as automorphism groups of chiral polytopes*, J. Geom. 108 (2017), 675–702; [arXiv:1606.08017, Section 6](https://arxiv.org/html/1606.08017#S6).

This proves the intersection assertion **whenever the parameters required by Conjecture 6.1 exist**. It does not prove their existence, and consequently does not by itself settle the full chiral-existence conjecture for PSL(2,q).

## Setup

Let p be odd, let e1,e2>1 be coprime odd integers, and put

    F = F_p,  F1 = F_(p^e1),  F2 = F_(p^e2),  L = F_(p^(e1 e2)).

Let j_i be primitive in Fi, and write u=j1+j1^(-1), v=j2+j2^(-1). Suppose D belongs to L and

    D^2 = u^2 v^2 - 4(u^2+v^2).

Use determinant-one representatives of the matrices in the source:

    alpha = (1/2) [[u,u+2],[u-2,u]],
    beta  = (1/2) [[2+u,u],[-u,2-u]],
    gamma = (1/(2u)) [[v(u-2),D],[D,v(u+2)]].

The source's final displayed gamma omits the scalar factor 1/(2u) because its matrices are projective representatives. Restoring it gives determinant one and trace v, as required for the following computations. Either choice of square root D is allowed.

We prove, in PSL(2,L),

    <alpha,beta> intersect <beta,gamma> = <beta>.

## Two field observations

First, u^2 and v^2 do not belong to F. Indeed, if u^2 belongs to F, then u has degree at most two over F. Since u belongs to an odd-degree extension F1, it follows that u belongs to F. Then j1 satisfies X^2-uX+1=0 over F, and the same odd-degree argument implies j1 belongs to F, contrary to its primitiveness in F1. The argument for v is identical. In particular u,v are nonzero.

Second, if x belongs to F1 and y belongs to F2 and xy belongs to F1+F2, then x or y belongs to F. Here F1+F2 denotes their additive sum inside L. To prove this, write xy=a+b with a in F1 and b in F2. Let tau be the p^e1-power Frobenius, which fixes F1 and acts on F2 with fixed field F. If y is not in F, then y^tau-y is nonzero. Subtracting the original identity from its tau image gives

    x = (b^tau-b)/(y^tau-y) in F2.

As F1 intersect F2=F, this forces x in F.

Put z=D/(uv). Then

    z^2 = 1-4/u^2-4/v^2.

We claim z does not belong to F1+F2. Otherwise write z=x+y with x in F1 and y in F2. The square identity gives 2xy in F1+F2; p is odd, so the preceding observation makes x or y belong to F. Therefore z lies in F1 or F2. If z lies in F1, the square identity gives 4/v^2 in F1 intersect F2=F, contradicting the first observation. The other case is identical. This proves the claim. It also proves D is nonzero.

## Normalizing the shared unipotent

Define

    U(t) = [[1,t],[0,1]],
    A(w) = [[1,(2-w)/w],[-w,w-1]],
    T = [[1,2/u],[-1,0]].

Write M^T=T^(-1)MT. Direct multiplication gives

    beta^T = U(1),   alpha^T = A(u),

    gamma^T = [[(-D+v(u+2))/(2u), -D/u^2],
               [-v, (D+v(u-2))/(2u)]].

Set

    t = D/(2uv) + 1/v - 1/2 - 1/u.

Then (gamma^T)^U(t)=A(v). One can verify this by checking its upper-left entry is 1, lower-left entry is -v, trace is v and determinant is 1; those conditions determine its upper-right entry. The earlier field claim shows t does not belong to F1+F2, since its last three summands belong to that sum and its first summand is z/2.

Consequently the normalized subgroups are contained in

    <alpha,beta>^T <= PSL(2,F1),
    <beta,gamma>^T <= U(t) PSL(2,F2) U(-t).

Equality with these containing subfield groups is not needed.

## Intersection of the containing groups

Let M=[[a,b],[c,d]] be a determinant-one representative over F1 of an element in both containing projective groups. Because both representatives have determinant one, their possible scalar discrepancy is only +/-1, which can be absorbed into the representative over F2. Therefore

    U(-t) M U(t)
       = [[a-tc, b+t(a-d)-t^2 c], [c,d+tc]]

has all its entries in F2.

The lower-left entry implies c belongs to F1 intersect F2=F. If c is nonzero, the upper-left entry gives t=(a-(a-tc))/c in F1+F2, a contradiction. Thus c=0.

The two diagonal entries now imply a,d belong to F. If a differs from d, the upper-right entry gives t in F1+F2, another contradiction. Hence a=d, and determinant one implies a=d=+/-1. Finally b belongs to F1 intersect F2=F.

Thus the containing groups intersect precisely in the projective images of +/-U(b), b in F, namely <U(1)> of order p. Both actual normalized subgroups contain U(1), so their intersection is also exactly <U(1)>. Conjugating back proves the conjectured equality. QED.

## Scope

The proof is uniform in p,e1,e2 and both square-root choices. It uses the existence of D but no unproved group-generation assertion and no classification of finite simple groups. The remaining obstacle for the source's broad existence conjecture is Conjecture 6.1, the primitive-element square condition.

## Reproducible finite-field certificate

Run [psl2_intersection_check.g](psl2_intersection_check.g) with GAP 4.15.1:

    gap -q -b -T research/leemans/psl2_intersection_check.g

The script checks the first residual case p=3,e1=3,e2=5, so q=3^15=14,348,907. It uses compatible Conway-field primitives j1=Z(27) and j2=Z(243)^7, both embedded in GF(3^15), and constructs an explicit square root D. It checks all three matrix normalization identities exactly.

It then enumerates all 19,656 matrices of the small containing group SL(2,27), conjugates each by U(t), and tests each entry for membership in GF(243) by x^(3^5)=x. Exactly six matrices pass, all of the form +/-U(b) with b in GF(3). The projective intersection therefore has exactly three elements. This verifies the first case without enumerating the enormous PSL(2,3^15).

The complete output is in [psl2_intersection_check.log](psl2_intersection_check.log). This exact finite computation supplements the general proof rather than establishing its uniform statement.
