# Matched replacement proof for two nonexceptional counting theorems

10 October 2026. Measurement specimen, not a claim to compress an entire
paper. The targets are Theorems 1.1 and 1.2 of Kiefer–Leemans, *On pairs
of commuting involutions in Sym(n) and Alt(n)*, restricted to degrees
N≥4, N≠6. Their exceptional degree-six clauses and both polyhedron
theorems are excluded. The displayed counts below are exactly their
floor-sum formulas, with n=floor(N/2).

The common retained background B is elementary finite group and
permutation theory: orbit-stabilizer and coset actions, uniqueness of
cycle decomposition, conjugacy in S_N by cycle type, signs of
permutations, the usual centralizer of an involution in S_N, and
Aut(S_N)=S_N, Aut(A_N)=S_N for N≥4, N≠6. The source uses these facts
without proving the general automorphism or centralizer theorems.
The action classification and all counting steps needed here are proved
below; no counting formula, computer enumeration, or source lemma is
retained as background.

## Shared proof core

<!-- core-start -->
Two distinct commuting involutions a,b generate V=C₂². A finite V-set
is a disjoint union of transitive orbits V/K. Since V is abelian, K is
the same stabilizer at every point of its orbit. Thus the multiplicities
of the five possible stabilizers V, ⟨a⟩, ⟨b⟩, ⟨ab⟩, 1 completely
determine the action up to permutation conjugacy. Write them f,x,y,z,t,
respectively. Their orbit sizes give

    N=f+2(x+y+z)+4t.

The action is faithful exactly when t>0 or at least two of x,y,z are
positive: its kernel is the intersection of the occurring stabilizers.
This is equivalent to a,b being distinct nonidentity permutations.
Swapping a,b interchanges x,y. Consequently the number of unordered
classes equals half the sum of the number of ordered classes and the
number fixed by this interchange: nonfixed classes occur in pairs.

Put n=floor(N/2). Let k be the number of transpositions of a, and l the number of
transpositions of b inside the support of a. Then

    k=y+z+2t,   l=z+2t,   x=number of b-transpositions outside that support.

For fixed k, the choices are precisely

    0≤l≤k,   0≤t≤floor(l/2),   0≤x≤n−k,
    z=l−2t,   y=k−l,   f=N−2(x+k).

These formulas give a bijection in both directions; in particular they
identify exactly the parameters counted by the source's centralizer
argument. The final f is nonnegative. Its parity is the parity of N,
so the choices are identical in degrees 2n and 2n+1.

Define

    λ(k)=sum over l=0,…,k of (floor(l/2)+1)
        =floor((k/2+1)²).

The equality follows by grouping consecutive even and odd l. For k≥1,
exactly two of these choices must be removed: b=1 has x=l=t=0, and
b=a has x=t=0,l=k. All remaining choices are faithful.

A class is fixed by swapping a,b exactly when x=y. Equivalently the
two permutations have the same number k of transpositions. Then
x=y=k−l, so the permitted l satisfy max(0,2k−n)≤l≤k. Only b=a must
be removed. The number D(k,n) of these fixed classes is therefore

    D(k,n)=λ(k)−ψ(k,n)−1,

where ψ(k,n)=0 for k≤floor(n/2). For h=2k−n>0, the omitted sum over
l=0,…,h−1 is h(h+2)/4 if h is even and (h+1)²/4 if h is odd.
Since h and n have the same parity, this is exactly

    ψ(k,n)=(2k−n)²/4+(2k−n)/2                 if n is even,
    ψ(k,n)=(2k−n−1)²/4+(2k−n)                if n is odd.

Finally, the retained automorphism facts identify these S_N-conjugacy
classes with the source's isomorphism classes in each nonexceptional
degree, also when the permutations lie in A_N.
<!-- core-end -->

## Adapter S: Theorem 1.1 outside degree six

<!-- symmetric-start -->
For fixed k there are λ(k)(n−k+1)−2 ordered classes. Summing k=1,…,n
gives O(n)=sum λ(k)(n−k+1)−2n. The fixed classes number
D(n)=sum λ(k)−sum over k>floor(n/2) ψ(k,n)−n.
Thus (O(n)+D(n))/2 equals

    −3n/2 + sum over k=1,…,n λ(k)((n−k)/2+1)
           −(1/2) sum over k>floor(n/2) ψ(k,n).

This is the exact formula in Theorem 1.1, with its exceptional degree-six
clause excluded as stipulated.
<!-- symmetric-end -->

## Adapter A: Theorem 1.2 outside degree six

<!-- alternating-start -->
The permutation a is even exactly when k is even, and b is even exactly
when l+x is even. Fix an even k. The numbers of choices of (l,t) with l
even or odd are respectively

    γ(k)=sum over j=0,…,k/2 (j+1)=k²/8+3k/4+1,
    δ(k)=sum over j=0,…,k/2−1 (j+1)=k²/8+k/4.

Among x=0,…,n−k, there are ceil((n−k+1)/2) even values and
floor((n−k+1)/2) odd values. Both excluded choices b=1 and b=a have
even parity. The number of ordered even classes is consequently

    μ(n)=−2floor(n/2)
      + sum over even k=1,…,n [γ(k)ceil((n−k+1)/2)
                              +δ(k)floor((n−k+1)/2)].

For a swap-fixed class x=y, the two cycle counts are equal. Hence a
fixed class is even exactly when k is even, and its count is simply
the sum of D(k,n) over even k. The unordered count is

    (1/2)[μ(n)+sum over even k=1,…,n D(k,n)].

The source's φ(k,n) is exactly D(k,n): it is λ(k)−1 below the threshold
and λ(k)−ψ(k,n)−1 above it. This proves the exact formula of Theorem 1.2.
No finite comparison of generating-function coefficients is used in this
proof of equivalence.
<!-- alternating-end -->

The three marked spans form the measured replacement. This surrounding
target statement, background declaration, and measurement explanation
are reported separately from the proof length. The corresponding source
target statements and bibliography are likewise outside its proof spans.
