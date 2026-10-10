## 25. Commuting involutions and complete exceptional polyhedra

The new intake L066 is Ann Kiefer and Dimitri Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*, in its nine-page author PDF. Its four principal statements are Theorems 1.1, 1.2, 3.6 and 4.4. We recover the two formulas including the degree-six clauses, all five exceptional endpoint representatives, and both polyhedron classifications. All subsidiary numbered items and Table 1 are accounted for below. The group automorphisms used in the counting equivalence are automorphisms of the ambient S_N or A_N, not just conjugations inside A_N.

### 25.1. Multiplicities, parity, and the centralizers

Two distinct nonidentity commuting involutions a,c generate V=⟨a,c⟩≅C₂². Conversely any faithful permutation action of this marked V supplies such a pair. Apply K(e) with orbit stabilizers V,⟨a⟩,⟨c⟩,⟨ac⟩,1 and multiplicities f,x,y,z,t, respectively. The complete invariant under permutation conjugacy is

\[
 N=f+2(x+y+z)+4t,\qquad
 t>0\ \text{or at least two of }x,y,z\text{ are positive}.
 \tag{CPI1}
\]

The second condition is precisely K(c)'s trivial-core condition. Interchanging the named generators exchanges x,y and fixes f,z,t. Both permutations are even exactly when y+z and x+z are even, equivalently x≡y≡z (mod 2). These are the two coordinate values of the single character equation (Ke4). Every tuple occurs as the disjoint union of the indicated coset actions, so the classification is an existence and uniqueness theorem, not only a count.

For an involution ρ with k transpositions in S_N, (Ke2) for C₂ gives

\[
 C_{S_N}(\rho)\cong(C_2\wr S_k)\times S_{N-2k}.
 \tag{CPI2}
\]

If ρ∈A_N, its alternating centralizer is the kernel of the sign on this product. A flip on one two-point orbit is an odd element in the centralizer. Thus this kernel has index two and order 2^{k-1}k!(N−2k)!. This proves source Propositions 3.1 and 4.1 directly; their general centralizer structure is not an additional retained theorem here. The same odd centralizer element also shows that a single involution's S_N-class does not split in A_N. This statement about individual involutions is not a replacement for the required pair-orbit equivalence.

### 25.2. Exact floor formulas in every nonexceptional degree

Let n=⌊N/2⌋. For a pair with a containing k transpositions, let l be the number of c-transpositions inside the support of a. Its multiplicities satisfy the reversible coordinate change

\[
 k=y+z+2t,\quad l=z+2t,\quad
 0\le l\le k,\quad 0\le t\le\lfloor l/2\rfloor,\quad0\le x\le n-k,
 \quad z=l-2t,\quad y=k-l,\quad f=N-2(x+k).
 \tag{CPI3}
\]

For k≥1 the only nonfaithful choices are c=1 (x=l=t=0) and c=a (x=t=0,l=k). Indeed any other commuting involution distinct from a yields a faithful marked V, by (CPI1). Define

\[
 \lambda(k)=\sum_{l=0}^k(\lfloor l/2\rfloor+1)
 =\lfloor(k/2+1)^2\rfloor.
 \tag{CPI4}
\]

The equality follows by pairing consecutive even and odd l; it holds for both parities of k. Thus the number of ordered conjugacy classes is

\[
 O(n)=\sum_{k=1}^n\lambda(k)(n-k+1)-2n.
 \tag{CPI5}
\]

This is exactly source Lemma 3.2. Swapping the endpoints fixes a multiplicity vector precisely when x=y, equivalently the two permutations have the same transposition count. If those counts differ the ordered classes are paired by reversal; if equal, reversal fixes the ordered class itself. This proves source Lemma 3.3, without using its printed inference from conjugacy of a single second involution to conjugacy fixing the first.

For a fixed class with common cycle count k, put x=y=k−l. The lower bound on l is max(0,2k−n). The choice c=a is excluded. Set ψ(k,n)=0 for k≤⌊n/2⌋. For h=2k−n>0, the omitted initial sum is

\[
 \psi(k,n)=\sum_{l=0}^{h-1}(\lfloor l/2\rfloor+1)
 =\begin{cases}h^2/4+h/2,&n\text{ even},\\(h-1)^2/4+h,&n\text{ odd}.
 \end{cases}
 \tag{CPI6}
\]

This follows from the same even/odd pairing and h≡n (mod 2). Consequently the number fixed at k is D(k,n)=λ(k)−ψ(k,n)−1. An involution on any finite set has one orbit per fixed point and one per two-element orbit, so its orbit count is half the sum of its number of points and fixed points. Applying this to reversal gives

\[
 s_n=-\frac{3n}{2}+\sum_{k=1}^n\lambda(k)\left(\frac{n-k}{2}+1\right)
 -\frac12\sum_{k=\lfloor n/2\rfloor+1}^n\psi(k,n).
 \tag{CPI7}
\]

For even endpoints, k must be even and l+x must be even. When k is even the numbers of (l,t) with l even or odd are respectively

\[
 \gamma(k)=\sum_{j=0}^{k/2}(j+1)=k^2/8+3k/4+1,\qquad
 \delta(k)=\sum_{j=0}^{k/2-1}(j+1)=k^2/8+k/4.
 \tag{CPI8}
\]

Among x=0,…,n−k, exactly ⌈(n−k+1)/2⌉ are even and ⌊(n−k+1)/2⌋ odd. The two removed choices are even. Therefore

\[
 \mu(n)=-2\lfloor n/2\rfloor+
 \sum_{\substack{1\le k\le n\\k\text{ even}}}
 \left[\gamma(k)\left\lceil\frac{n-k+1}{2}\right\rceil+
 \delta(k)\left\lfloor\frac{n-k+1}{2}\right\rfloor\right],\qquad
 a_n=\frac12\left(\mu(n)+\sum_{\substack{1\le k\le n\\k\text{ even}}}D(k,n)\right).
 \tag{CPI9}
\]

The first expression proves source Lemma 4.2 and the second is exactly Theorem 1.2's formula, since its φ(k,n) is D(k,n). These formulas count S_N-conjugacy classes for all N≥4, including six. To obtain the source's isomorphism relation we retain the standard theorem that Aut(S_N) is induced by S_N conjugation and Aut(A_N) by S_N conjugation for N≥4, N≠6. Thus (CPI7) and (CPI9) prove the nonexceptional parts of source Theorems 1.1 and 1.2. For N=6 the full automorphism action is computed below. All nontrivial V-orbits have even size, so removing one fixed point in odd degree and adding one in even degree is a bijection of the multiplicity sets. This proves the even/odd degree pairing; N=6 and N=7 differ only when the ambient exceptional automorphisms are allowed.

As a compact alternative encoding of the same classification, let v record half-degree. With x≤y for unordered pairs,

\[
 \sum_{n\ge0}s_nv^n=\frac1{(1-v)^3(1-v^2)^2}-\frac{1+v}{(1-v)^2},\qquad
 \sum_{n\ge0}a_nv^n=\frac{1+v^3}{(1-v)(1-v^2)^3(1-v^4)}-
 \frac{1+v^2}{(1-v)(1-v^2)}.
 \tag{CPI10}
\]

Here s_n,a_n continue to denote conjugacy counts, without the six-point automorphism fusion. To verify every factor, write y=x+d: x,d,z,t and unused pairs of fixed points have weights 2,1,1,2,1. The nonfaithful tuples have t=0 and at most one positive coordinate among x,y,z. Their series is (1+v)/(1−v)^2. For even endpoints write x=2x′+e,y=2y′+e,z=2z′+e with e∈{0,1}. The common odd shift has weight3; the other weights are4,2,2,2,1. The nonfaithful even tuples have e=t=0 and give the second subtraction. This proves the rational expressions independently of a finite coefficient check.

### 25.3. Full automorphism orbits in degree six

Apply (Ke5) with B=Aut(G), E the unordered pairs {a,c} of distinct commuting involutions, and Z the pairs together with an involution b. An automorphism acts on the unordered endpoints and on b; it may interchange a,c. Thus its orbit on Z is exactly an isomorphism of the marked triple with endpoint reversal allowed. This is precisely the equivalence of regular polyhedra up to isomorphism and duality.

Appendix I constructs every involution by enumerating Elements(G), then every distinct unordered commuting pair, and its full automorphism orbit. For each orbit it enumerates every middle involution modulo the endpoint-pair stabilizer. It tests generation and, for every generating triple, all 64 ordered pairs of subsets I,J⊆{0,1,2} for ⟨r_i:i∈I⟩∩⟨r_i:i∈J⟩=⟨r_i:i∈I∩J⟩. There is no shortcut based solely on group orders, endpoint type, or a published classification list. The existing exact marked recognition and the retained string-C-group/polytope correspondence then identify the surviving triples with all required polyhedra.

The exact finite output is:

| G | Automorphism order | Involutions | Commuting pairs | Endpoint orbits | Middle orbits | Generating triples | IP survivors |
|---|---:|---:|---:|---:|---:|---:|---:|
| S₆ | 1440 | 75 | 495 | 5 | 80 | 2 | 2 |
| A₆ | 1440 | 45 | 90 | 1 | 8 | 0 | 0 |

The two S₆ survivors have unordered adjacent orders {5,6} and {6,6}. Exact representatives, separately checked for generation and all meets, are

\[
 (a,b,c)=((5\ 6),(2\ 3)(4\ 5),(1\ 2)(3\ 4)),\qquad
 ((5\ 6),(2\ 3)(4\ 5),(1\ 2)(3\ 4)(5\ 6)).
 \tag{CPI11}
\]

Reversing the first gives the source's convention {6,5}. Appendix I also verifies that the five representatives printed in source equation (2) are pairwise inequivalent and exhaust the five endpoint orbits:

\[
 \begin{array}{c|c}
 a&c\\\hline
 (1\ 2)&(3\ 4)\\
 (1\ 2)&(3\ 4)(5\ 6)\\
 (1\ 2)&(1\ 2)(3\ 4)\\
 (1\ 2)&(1\ 2)(3\ 4)(5\ 6)\\
 (1\ 2)(3\ 4)&(1\ 3)(2\ 4)
 \end{array}
 \tag{CPI12}
\]

Only the second and fourth endpoint orbits admit a generating middle. The last pair represents the unique Aut(A₆) orbit. The nine S₆-conjugacy orbits of S₆ pairs fuse to five under Aut(S₆); the two S₆-conjugacy orbits of A₆ pairs fuse to one under Aut(A₆). These observations and the table complete the exceptional clauses of Theorems 1.1 and 1.2 and source Lemma 4.3. They prove Theorem 3.6 and Theorem 4.4: exactly the two stated S₆ polyhedra and no A₆ regular polyhedron exist.

The argument is exhaustive by (Ke5): every triple moves to a chosen endpoint orbit and then to a chosen middle orbit under its stabilizer. Generation and every IP meet are invariant under these moves. Each retained marking conversely is a string C-group, and source equivalence allows exactly its automorphism and reversal orbit. The supplied program is therefore a computational proof of the exceptional classification, not merely a check of two constructions. It retains GAP's exact group, automorphism and orbit algorithms; no SmallGroups or polytope catalogue is imported. The change from the source's computer-free exceptional analysis to this exact finite computation is part of the proof cost.

### 25.4. Complete source inventory and boundaries

Table 1 is recovered by (CPI7), (CPI9) and the degree-six correction. Its fourteen printed rows, including the row for degrees 1,2,3, are:

| Degree N | Symmetric | Alternating |
|---|---:|---:|
|1,2,3|0|0|
|4,5|3|1|
|6|5|1|
|7|9|2|
|8,9|21|7|
|10,11|39|10|
|12,13|67|21|
|14,15|105|28|
|16,17|158|48|
|18,19|226|61|
|20|315|93|
|30|1169|315|
|40|3105|855|
|50|6774|1795|

The ordinary formulas give zero below degree four, where no faithful V-action fits. Appendix J verifies the printed rows, the reversible coordinates, and rational-series agreement with the floor formulas through half-degree 500. These controls do not prove the all-degree formulas: their proof is (Ke1), (Ke4) and (CPI3)–(CPI9). The whole control program is nevertheless charged.

All thirteen numbered source items are now located: Theorems 1.1 and 1.2 in §§25.2–25.3; Proposition 3.1 in §25.1; Lemmas 3.2 and 3.3 in §25.2; Definition 3.5 is the existing IP/string convention; Theorem 3.6 in §25.3; Proposition 4.1 in §25.1; Lemma 4.2 in §25.2; Lemma 4.3 and Theorem 4.4 in §25.3. Remark 3.7 is historical attribution to the earlier Leemans–Vauthier computation, not an additional new mathematical target. Remark 3.4 has the exact endpoint-reversal meaning proved above: equal-cycle endpoints form a reversal-fixed orbit. Endpoints alone neither specify a polyhedron nor prove a completed triple self-dual; a middle generator must also be preserved by the relevant automorphism. We do not promote that remark to an unconditional self-duality theorem. The printed Theorem 4.4 is read in its section's regular-polyhedron context; the proof does not exclude arbitrary nonregular polyhedra with group A₆.

All nine author-PDF pages, including all proofs, the exceptional representatives, the table and bibliography, were read afresh, with every page also rendered and viewed. The archived journal metadata gives Communications in Algebra 41(12) (2013), 4408–4418; a publisher full-text comparison was not made. The contract binds the exact nine-page author version. The formulas, exceptional results and original problem are credited to Kiefer–Leemans; the orbit decomposition, wreath-product centralizer, sign character and orbit–stabilizer methods are standard mathematics. The self-contained shared assembly and fresh certificate are repository work, with no historical-novelty claim and no open conjecture identified as solved.

