# An odd-prime class-three corollary

10 October 2026. Private short consequence for review of
phase11_powerful_frattini.md, Theorem B. No conclusion for class-three
2-groups is asserted.

**Corollary.** If p is odd and P is a finite p-group of nilpotency class
at most three, every cyclic subgroup TPP triple A,B,C satisfies
|A||B||C|≤|P|. Consequently the same holds for every finite nilpotent
group of odd order and class at most three.

**Proof.** Every subgroup H≤P has class at most three. Put K=Φ(H),
and work in the quotient H/K^p; this is permitted because K^p is
characteristic in H. The image of K has exponent dividing p. In
particular the image of H′ has exponent dividing p and is abelian,
since [H′,H′]≤γ₄(H)=1. Its subgroup γ₃(H) is central and also has
exponent dividing p.

For any a,b∈H, the class-three commutator formula is

    [a^p,b]=[a,b]^p [a,b,a]^(p(p−1)/2).

Both factors vanish in H/K^p: the first because H′ has exponent p,
the second because p is odd and divides p(p−1)/2. Thus every p-th
power is central in this quotient. The image of

    K=H^p H′

is therefore abelian, being the product of a central subgroup and an
abelian subgroup. Equivalently [K,K]≤K^p, so K is powerful. This
holds for every H≤P, proving precisely the hereditary hypothesis in
Theorem B of phase11_powerful_frattini.md. Its inequality applies.
For a nilpotent group of odd order, split the cyclic factors into Sylow
components, apply the p-group assertion and multiply. ∎

The commutator identity is the elementary class-three collection formula;
it follows by induction from [xy,b]=[x,b]^y[y,b], with the third-level
commutator central. The argument works for p=3 as well as larger odd
primes. Its use of oddness occurs exactly at p | p(p−1)/2.

This is a written consequence of the retained powerful-group structure
theorems and the reviewed action obstruction. It is not an independent
classification or a formalized group theorem. No publication-priority
determination is made. The unrestricted cyclic-TPP problem remains open.
