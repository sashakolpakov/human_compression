# A central cyclic lift closes the small even-exponent gap

Status: proposed proof, checked by internal agent reviews and exact computations in this session, not by external peer review. Novelty is provisional pending a fuller literature search and external mathematical review. No submission or message to authors has been made.

## Result

For every odd prime p and every integer m >= 5, there is a non-tight chiral abstract polyhedron whose full automorphism group has order 2 p^m.

The new range covered here is **m even, 6 <= m <= p+1**. Since p is odd, this is precisely the even range m >= 5 omitted by Theorem 1.4 of Kong, Feng, Hou, Leemans and Qu, *Chiral 3-polytopes of order 2p^m*, [accepted manuscript](https://amc-journal.eu/index.php/amc/article/download/3716/2232), accepted 19 January 2026, DOI [10.26493/1855-3974.3716.b64](https://doi.org/10.26493/1855-3974.3716.b64); earlier version [arXiv:2508.20654](https://arxiv.org/abs/2508.20654). Their theorem covers odd m >= 5 and even m >= p+3. Their Theorems 1.1 and 1.2 exclude non-tight examples for m < 5. Thus, conditional only on those results, the existence criterion becomes m >= 5.

The construction in the new range has Schlaefli type **{p^2, 2p^2}**.

## Central lift lemma

Let p be an odd prime. Suppose G0 has a canonical generating pair (a0,b0) for a chiral polyhedron, with

    |a0| = p^2,   |b0| = 2p,   |a0 b0| = 2,
    <a0> intersect <b0> = 1.

Suppose additionally there is a homomorphism phi: G0 -> C_p = <c> such that

    phi(a0) = c,   phi(b0) = c^(-1).

Let C_(p^2) = <x>, and set

    a = (a0,x),   b = (b0,x^(-1)),
    H = <a,b> <= G0 x C_(p^2).

Then (H,a,b) is a chiral polyhedron group of order p|G0| and type {p^2,2p^2}.

### Proof

Let pi: H -> G0 be projection, which is surjective. The two generators lie in the fiber product

    F = {(g,x^j) : phi(g)=c^j}.

Projection F -> G0 has kernel <(1,x^p)> of order p, so |F|=p|G0|. On the other hand,

    b^(2p) = (1,x^(-2p))

generates <(1,x^p)>, because p is odd. Thus H contains that kernel and projects onto G0. Consequently H=F and |H|=p|G0|. In particular,

    K = ker(pi) = <b^(2p)>.

The direct product formula gives |a|=p^2 and |b|=2p^2, while ab=(a0b0,1) has order 2. The restriction of pi to <a> is injective, because |a|=|a0|. If h belongs to <a> intersect <b>, then pi(h) belongs to <a0> intersect <b0>=1; injectivity on <a> gives h=1.

These conditions give an abstract polyhedron that is directly regular or chiral. To establish chirality, suppose that rho is an automorphism of H sending a to a^(-1) and b to b^(-1). The explicit formula K=<b^(2p)> implies rho(K)=K. Hence rho induces an automorphism of H/K=G0 sending a0 to a0^(-1) and b0 to b0^(-1), contradicting the chirality of the original pair. Thus the lifted polyhedron is chiral. QED.

This argument does **not** assume that arbitrary covers of chiral polyhedra remain chiral. Preservation of the particular kernel <b^(2p)> is essential.

## Application to the omitted range

Fix an even m with 6 <= m <= p+1 and put r=m-2. Thus r is even and 4 <= r <= p-1. Use the e=1 case of the p-group construction in Section 3 of the cited paper:

    P = <beta,s1,...,sr>,
    A = <s1,...,sr> = C_p^r,
    [si,beta] = s_(i+1)  (1 <= i < r),
    [sr,beta] = 1,
    beta^p = sr.

Here [u,v]=u^(-1)v^(-1)uv. The paper gives |P|=p^(r+1)=p^(m-1) and, since r is even, an involutory automorphism sigma defined by

    sigma(s1)=s1,   sigma(beta)=beta^(-1).

Section 6, Case 1 constructs the chiral group

    G0 = P semidirect <sigma>,
    a0 = beta s1,   b0 = s1^(-1) sigma,

with orders |a0|=p^2, |b0|=2p and |G0|=2p^(m-1).

There is a homomorphism phi: G0 -> C_p determined by

    phi(s1)=c,
    phi(beta)=phi(sigma)=phi(s2)=...=phi(sr)=1.

Every relation of P is respected. The action of sigma is also respected: it fixes s1, inverts beta, and sends each si for i>=2 into <s2,...,sr>. Therefore phi(a0)=c and phi(b0)=c^(-1), as required by the lemma.

The resulting H has order 2p^m and type {p^2,2p^2}. The product of its two type entries is 2p^4, strictly smaller than 2p^m since m>=6. Hence the polyhedron is non-tight.

## Independent exact computation

[central_lift.g](central_lift.g) constructs the source p-group with a consistent polycyclic presentation, verifies its involutory automorphism, builds its semidirect product, verifies the base chirality, constructs the fiber product generators, and independently verifies the lifted pair. It uses GAP 4.15.1 and no external packages.

    gap -q research/leemans/central_lift.g

The following cases passed:

| p | m | Base order | Lift order | Type | Cyclic intersection order | Kernel order | Simultaneous inversion homomorphism |
|---|---|------|-----|------|---------------------------|--------------|-------------------------------------|
| 5 | 6 | 6,250 | 31,250 | {25,50} | 1 | 5 | none |
| 7 | 6 | 33,614 | 235,298 | {49,98} | 1 | 7 | none |
| 7 | 8 | 1,647,086 | 11,529,602 | {49,98} | 1 | 7 | none |

For every row, the two generators generate the displayed group, their product has order 2, and the type product is smaller than the group order. GAP's `GroupHomomorphismByImages(H,H,[a,b],[a^-1,b^-1])` returned `fail`, an exact check that no such homomorphism exists. These finite checks supplement the uniform proof; they do not substitute for it.

## Source interpretation and open-status limits

The arXiv version is dated 28 August 2025. The publisher's 22-page accepted manuscript, accepted 19 January 2026, retains the incomplete range in Theorem 1.4. Section 7 on page 20 identifies even m<=p+2 as unhandled and p=5,m=6 as its first case. Its exact conjectural sentence is: “We conjecture that tight chiral polyhedra also exist in this case.” However, its surrounding paragraph and Theorem 1.4 concern non-tight examples, and the introduction already cites Cunningham's tight examples. This appears to be a typographical omission of “non-”; the literal wording and our interpretation must be distinguished.

The mathematical result above closes the non-tight existence gap of Theorem 1.4 regardless of that wording. It does not settle the Brooksbank–Leemans rank-spectrum conjecture or the Mondrian conjecture.
