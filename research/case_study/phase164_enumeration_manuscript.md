# Module D: Marked actions, field orbits and geometry enumeration

## Abstract

We classify regular polytopes and coset geometries by actions on marked configurations. Orbit multiplicities describe commuting involutions in symmetric and alternating groups; normalized field coordinates describe Suzuki polyhedra; and panel subgroups describe finite geometries with nontrivial chamber stabilizer. In each case, classification of an extension reduces to a stabilizer acting on an explicit fiber. We derive the all-degree commuting-pair formulas, the exceptional six-point polyhedra, the complete Suzuki counting formulas, and the residually weakly primitive $J_2$ census. A second finite application gives the 81 rank-two and 431 rank-three primitive geometries of $M_{22}$ and recovers their geometric shadows; the finer labels in the source table remain a separate comparison obligation. The arguments use the action and intersection results of the companion manuscript *Marked groups, kernels and intersections*. Classical finite-group structure and the complete finite certificates are specified separately.

## 1. Markings, equivalence and geometric recognition

Counting configurations is useful only after their equivalence and admissibility conditions have been identified. A pair of commuting involutions is a faithful action of a marked four-group. Completing such a pair to a regular polyhedron requires a third involution, generation and the subgroup intersection property. A family of panel subgroups gives a different type of marking: its chamber stabilizer need not be trivial, and subgroup intersections alone do not ensure flag transitivity. These distinctions explain the separate local recognition arguments below.

For a finite group $A$ acting on a set $X$, U.Orbits identifies $X$ with the disjoint union of transitive actions $A/H$ and describes its action kernel, equivariant permutations and faithful-image normalizer. In §3 we apply this theorem to the marked group $C_2^2$. We do not identify automorphisms of that small marked group with arbitrary automorphisms of the ambient symmetric or alternating group.

For an equivariant map $p:Z\to E$, U.ExtensionOrbits gives
\[
A\backslash Z\cong\coprod_{e\in A\backslash E}A_e\backslash p^{-1}(e).
\tag{E0}
\]
We use this same statement for an endpoint pair with a middle involution, a first field coordinate with a second coordinate, and a lower-rank panel system with a further panel. The admissibility tests are invariant under the displayed actions and are proved in each application. Replacing an acting group by its permutation image on the actual objects preserves these orbit relations, since every image element has an acting lift.

Our initial source conclusions are the four principal theorems of Kiefer–Leemans (2013), both principal counting theorems of Kiefer–Leemans (2010), and the complete principal $J_2$ census of Leemans (2002). Section 6 adds a qualified comparison with Leemans–Rowley (2010). We keep their exact equivalence conventions. The source-specific results, classical retained inputs and written or computational proofs have distinct roles throughout.

The relation between the applications is more precise than the observation that each uses a group action. One first fixes a partial marking, identifies its actual stabilizer, and proves that the remaining data form the required fiber. One then imposes generation, intersection and geometric conditions before counting the resulting orbits. In the field case, the generation condition becomes an exact field-of-definition condition. In the finite geometry cases it becomes a collection of subgroup and coset identities. The shared orbit theorem performs the same reduction in all four settings; the local recognition proofs and the finite-group data remain necessary.

## 2. Exact support and orbit counting

**Theorem E.ExactSupportOrbits.** Let a finite group $A$ act on a finite set $X$ and on a finite poset $L$ with greatest element $1$. Let $s:X\to L$ be equivariant. Write $X_l=\{x:s(x)\le l\}$ and let $\mu$ be the Möbius function of $L$. Then the number of $A$-orbits of points having exact support $1$ is

\[
\frac1{|A|}\sum_{a\in A}\sum_{l\in L}
\mu(l,1)\,|\operatorname{Fix}_X(a)\cap X_l|.
\tag{E1}
\]

No $X_l$ is required to be $A$-invariant. The exact-top-support subset is invariant because $1$ is fixed.

**Proof.** For $x\in X$, the defining inverse relation for the incidence-algebra Möbius function gives
\[
\sum_{s(x)\le l\le1}\mu(l,1)=
\begin{cases}1&s(x)=1,\\0&s(x)<1.\end{cases}
\]
Summing this identity over the points fixed by $a$ gives the inner sum in (E1). On any finite $A$-set $Y$, counting pairs $(a,y)$ with $ay=y$ gives $\sum_a|\operatorname{Fix}_Y(a)|=\sum_y|A_y|$. Each orbit contributes $|A|$, since $|A\cdot y|\,|A_y|=|A|$. Division by $|A|$ therefore gives its number of orbits. Apply this to the invariant exact-support subset. ∎

For nested finite-field data, $L$ is the divisor poset of $N$ and $X_d$ is the data defined over the unique subfield $\mathbb F_{2^d}$. The application must prove that these sets are exactly the support sublevel sets, rather than assuming generation follows from a coordinate count. If exact-degree data have free Frobenius orbits of length $N$, and an additional involution is free on those orbits, the count reduces to $E(N)/(2N)$, where $E(N)=\sum_{d\mid N}\mu(N/d)|X_d|$. Section 4 supplies these hypotheses by normalization, the subfield-position lemma and the odd-degree inversion argument. For commuting pairs in symmetric groups, reversal has fixed orbits, so the free-action simplification is not used: the same fixed-point identity gives half the sum of the total and the fixed count.


## 3. Commuting involutions in symmetric and alternating groups

### 3.1. Multiplicities, parity, and the centralizers

Two distinct nonidentity commuting involutions $a,c$ generate $V=\langle a,c\rangle\cong C_2^2$. Conversely any faithful permutation action of this marked $V$ supplies such a pair. Apply U.Orbits with orbit stabilizers $V,\langle a\rangle,\langle c\rangle,\langle ac\rangle,1$ and multiplicities $f,x,y,z,t$, respectively. The complete invariant under permutation conjugacy is

\[
 N=f+2(x+y+z)+4t,\qquad
 t>0\ \text{or at least two of }x,y,z\text{ are positive}.
 \tag{CPI1}
\]

The second condition is precisely U.Orbits' trivial-kernel condition. Interchanging the named generators exchanges $x,y$ and fixes $f,z,t$. Both permutations are even exactly when $y+z$ and $x+z$ are even, equivalently $x\equiv y\equiv z\pmod2$. Indeed an element outside an index-two stabilizer flips that two-point orbit; on a regular four-point orbit it makes two transpositions and is even. Thus only the three two-point orbit multiplicities contribute to the sign character. Every tuple occurs as the disjoint union of the indicated coset actions, so the classification is an existence and uniqueness theorem, not only a count.

For an involution $\rho$ with $k$ transpositions in $S_N$, U.Orbits, equation (5.4) for $C_2$ gives

\[
 C_{S_N}(\rho)\cong(C_2\wr S_k)\times S_{N-2k}.
 \tag{CPI2}
\]

If $\rho\in A_N$, its alternating centralizer is the kernel of the sign on this product. A flip on one two-point orbit is an odd element in the centralizer. Thus this kernel has index two and order $2^{k-1}k!(N-2k)!$. This proves source Propositions 3.1 and 4.1 directly from the shared finite-action theorem. The same odd centralizer element also shows that a single involution's $S_N$-class does not split in $A_N$. This statement about individual involutions is not a replacement for the required pair-orbit equivalence.

### 3.2. Exact floor formulas in every nonexceptional degree

Let $n=\lfloor N/2\rfloor$. For a pair with $a$ containing $k$ transpositions, let $l$ be the number of $c$-transpositions inside the support of $a$. Its multiplicities satisfy the reversible coordinate change

\[
 \begin{gathered}
 k=y+z+2t,\qquad l=z+2t,\\
 0\le l\le k,\qquad 0\le t\le\lfloor l/2\rfloor,\qquad0\le x\le n-k,\\
 z=l-2t,\qquad y=k-l,\qquad f=N-2(x+k).
 \end{gathered}
 \tag{CPI3}
\]

For $k\ge1$ the only nonfaithful choices are $c=1$ ($x=l=t=0$) and $c=a$ ($x=t=0,l=k$). Indeed any other commuting involution distinct from $a$ yields a faithful marked $V$, by (CPI1). Define

\[
 \lambda(k)=\sum_{l=0}^k(\lfloor l/2\rfloor+1)
 =\lfloor(k/2+1)^2\rfloor.
 \tag{CPI4}
\]

The equality follows by pairing consecutive even and odd $l$; it holds for both parities of $k$. Thus the number of ordered conjugacy classes is

\[
 O(n)=\sum_{k=1}^n\lambda(k)(n-k+1)-2n.
 \tag{CPI5}
\]

This is exactly source Lemma 3.2. Swapping the endpoints fixes a multiplicity vector precisely when $x=y$, equivalently the two permutations have the same transposition count. If those counts differ the ordered classes are paired by reversal; if equal, reversal fixes the ordered class itself. This proves source Lemma 3.3, without using its printed inference from conjugacy of a single second involution to conjugacy fixing the first.

For a fixed class with common cycle count $k$, put $x=y=k-l$. The lower bound on $l$ is $\max(0,2k-n)$. The choice $c=a$ is excluded. Set $\psi(k,n)=0$ for $k\le\lfloor n/2\rfloor$. For $h=2k-n>0$, the omitted initial sum is

\[
 \psi(k,n)=\sum_{l=0}^{h-1}(\lfloor l/2\rfloor+1)
 =\begin{cases}h^2/4+h/2,&n\text{ even},\\(h-1)^2/4+h,&n\text{ odd}.
 \end{cases}
 \tag{CPI6}
\]

This follows from the same even/odd pairing and $h\equiv n\pmod2$. Consequently the number fixed at $k$ is $D(k,n)=\lambda(k)-\psi(k,n)-1$. An involution on any finite set has one orbit per fixed point and one per two-element orbit, so its orbit count is half the sum of its number of points and fixed points. Applying this to reversal gives

\[
 s_n=-\frac{3n}{2}+\sum_{k=1}^n\lambda(k)\left(\frac{n-k}{2}+1\right)
 -\frac12\sum_{k=\lfloor n/2\rfloor+1}^n\psi(k,n).
 \tag{CPI7}
\]

For even endpoints, $k$ must be even and $l+x$ must be even. When $k$ is even the numbers of $(l,t)$ with $l$ even or odd are respectively

\[
 \gamma(k)=\sum_{j=0}^{k/2}(j+1)=k^2/8+3k/4+1,\qquad
 \delta(k)=\sum_{j=0}^{k/2-1}(j+1)=k^2/8+k/4.
 \tag{CPI8}
\]

Among $x=0,\ldots,n-k$, exactly $\lceil(n-k+1)/2\rceil$ are even and $\lfloor(n-k+1)/2\rfloor$ odd. The two removed choices are even. Therefore

\[
 \begin{gathered}
 \mu(n)=-2\lfloor n/2\rfloor+
 \sum_{\substack{1\le k\le n\\k\text{ even}}}
 \left[\gamma(k)\left\lceil\frac{n-k+1}{2}\right\rceil+
 \delta(k)\left\lfloor\frac{n-k+1}{2}\right\rfloor\right],\\
 a_n=\frac12\left(\mu(n)+\sum_{\substack{1\le k\le n\\k\text{ even}}}D(k,n)\right).
 \end{gathered}
 \tag{CPI9}
\]

The first expression proves source Lemma 4.2 and the second is exactly Theorem 1.2's formula, since its $\varphi(k,n)$ is $D(k,n)$. These formulas count $S_N$-conjugacy classes for all $N\ge4$, including six. To obtain the source's isomorphism relation we retain the standard theorem that $\operatorname{Aut}(S_N)$ is induced by $S_N$ conjugation and $\operatorname{Aut}(A_N)$ by $S_N$ conjugation for $N\ge4$, $N\ne6$. Thus (CPI7) and (CPI9) prove the nonexceptional parts of source Theorems 1.1 and 1.2. For $N=6$ the full automorphism action is computed below. All nontrivial $V$-orbits have even size, so removing one fixed point in odd degree and adding one in even degree is a bijection of the multiplicity sets. This proves the even/odd degree pairing; $N=6$ and $N=7$ differ only when the ambient exceptional automorphisms are allowed.

As a compact alternative encoding of the same classification, let $v$ record half-degree. With $x\le y$ for unordered pairs,

\[
 \begin{aligned}
 \sum_{n\ge0}s_nv^n&=\frac1{(1-v)^3(1-v^2)^2}-\frac{1+v}{(1-v)^2},\\
 \sum_{n\ge0}a_nv^n&=\frac{1+v^3}{(1-v)(1-v^2)^3(1-v^4)}-
 \frac{1+v^2}{(1-v)(1-v^2)}.
 \end{aligned}
 \tag{CPI10}
\]

Here $s_n,a_n$ continue to denote conjugacy counts, without the six-point automorphism fusion. To verify every factor, write $y=x+d$: $x,d,z,t$ and unused pairs of fixed points have weights $2,1,1,2,1$. The nonfaithful tuples have $t=0$ and at most one positive coordinate among $x,y,z$. Their series is $(1+v)/(1-v)^2$. For even endpoints write $x=2x'+e,y=2y'+e,z=2z'+e$ with $e\in\{0,1\}$. The common odd shift has weight 3; the other weights are $4,2,2,2,1$. The nonfaithful even tuples have $e=t=0$ and give the second subtraction. This proves the rational expressions independently of a finite coefficient check.

### 3.3. Full automorphism orbits in degree six

Apply U.ExtensionOrbits with $B=\operatorname{Aut}(G)$, $E$ the unordered pairs $\{a,c\}$ of distinct commuting involutions, and $Z$ the pairs together with an involution $b$. An automorphism acts on the unordered endpoints and on $b$; it may interchange $a,c$. Thus its orbit on $Z$ is exactly an isomorphism of the marked triple with endpoint reversal allowed. This is precisely the equivalence of regular polyhedra up to isomorphism and duality.

The complete degree-six certificate constructs every involution by enumerating the elements of $G$, then every distinct unordered commuting pair, and its full automorphism orbit. For each orbit it enumerates every middle involution modulo the endpoint-pair stabilizer. It tests generation and, for every generating triple, all 64 ordered pairs of subsets $I,J\subseteq\{0,1,2\}$ for $\langle r_i:i\in I\rangle\cap\langle r_i:i\in J\rangle=\langle r_i:i\in I\cap J\rangle$. There is no shortcut based solely on group orders, endpoint type, or a published classification list. The explicitly tested intersection property and the retained string-C-group/polytope correspondence then identify the surviving triples with all required polyhedra.

The full certificate interface is stated in the appendix. Its exact finite output is:

| Quantity | $S_6$ | $A_6$ |
|---|---:|---:|
| Automorphism-group order | 1440 | 1440 |
| Involutions | 75 | 45 |
| Unordered commuting pairs | 495 | 90 |
| Endpoint orbits | 5 | 1 |
| Middle orbits | 80 | 8 |
| Generating triples | 2 | 0 |
| Intersection-property survivors | 2 | 0 |

The two $S_6$ survivors have unordered adjacent orders {5,6} and {6,6}. Exact representatives, separately checked for generation and all meets, are

\[
 (a,b,c)=((5\ 6),(2\ 3)(4\ 5),(1\ 2)(3\ 4)),\qquad
 ((5\ 6),(2\ 3)(4\ 5),(1\ 2)(3\ 4)(5\ 6)).
 \tag{CPI11}
\]

Reversing the first gives the source's convention {6,5}. The complete degree-six certificate also verifies that the five representatives printed in source equation (2) are pairwise inequivalent and exhaust the five endpoint orbits:

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

Only the second and fourth endpoint orbits admit a generating middle. The last pair represents the unique Aut($A_6$) orbit. The nine $S_6$-conjugacy orbits of $S_6$ pairs fuse to five under Aut($S_6$); the two $S_6$-conjugacy orbits of $A_6$ pairs fuse to one under Aut($A_6$). These observations and the table complete the exceptional clauses of Theorems 1.1 and 1.2 and source Lemma 4.3. They prove Theorem 3.6 and Theorem 4.4: exactly the two stated $S_6$ polyhedra and no $A_6$ regular polyhedron exist.

The argument is exhaustive by U.ExtensionOrbits: every triple moves to a chosen endpoint orbit and then to a chosen middle orbit under its stabilizer. Generation and every IP meet are invariant under these moves. Each retained marking conversely is a string C-group, and source equivalence allows exactly its automorphism and reversal orbit. The supplied program is therefore a computational proof of the exceptional classification, not merely a check of two constructions. It retains GAP's exact group, automorphism and orbit algorithms; no SmallGroups or polytope catalogue is imported. The change from the source's computer-free exceptional analysis to this exact finite computation is part of the proof cost.

### 3.4. Complete source inventory and boundaries

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

The ordinary formulas give zero below degree four, where no faithful V-action fits. The exact formula diagnostic verifies the printed rows, the reversible coordinates, and rational-series agreement with the floor formulas through half-degree 500. These controls do not prove the all-degree formulas: their proof is U.Orbits, the preceding sign calculation and (CPI3)–(CPI9). The whole control program is nevertheless charged.

All thirteen numbered source items are now located: Theorems 1.1 and 1.2 in §§3.2–3.3; Proposition 3.1 in §3.1; Lemmas 3.2 and 3.3 in §3.2; Definition 3.5 is the existing IP/string convention; Theorem 3.6 in §3.3; Proposition 4.1 in §3.1; Lemma 4.2 in §3.2; Lemma 4.3 and Theorem 4.4 in §3.3. Remark 3.7 is historical attribution to the earlier Leemans–Vauthier computation, not an additional new mathematical target. Remark 3.4 has the exact endpoint-reversal meaning proved above: equal-cycle endpoints form a reversal-fixed orbit. Endpoints alone neither specify a polyhedron nor prove a completed triple self-dual; a middle generator must also be preserved by the relevant automorphism. We do not promote that remark to an unconditional self-duality theorem. The printed Theorem 4.4 is read in its section's regular-polyhedron context; the proof does not exclude arbitrary nonregular polyhedra with group $A_6$.


## 4. Suzuki polyhedra in two field coordinates

### 4.1. Retained structure and the normalization theorem

Write $q=2^N$, where $N>1$ is odd, and $S_N=\operatorname{Sz}(q)$.
Use its usual ovoid action, with distinguished points $\infty,0$, and
root group $U_q$ at infinity. Write its central involutions as $z(b)$,
$b\in\mathbb F_q$, with $z(b)z(c)=z(b+c)$. A Weyl involution $w$ swaps
infinity and zero and is defined over $\mathbb F_2$.

We retain these standard Suzuki-group facts, also used in the older
construction notes and in the sources:

1. The ovoid action is doubly transitive. Every involution fixes exactly
   one ovoid point. $U_q$ acts regularly on the points other than infinity.
2. $C_{S_N}(z(b))=U_q$ for $b\ne0$, and all involutions in $U_q$ are
   its central elements $z(b)$. All involutions of $S_N$ are conjugate.
3. The ordered two-point stabilizer is the split torus $H_q$. Its
   conjugation acts as $z(b)\mapsto z(tb)$ and
   $wz(c)w\mapsto wz(t^{-1}c)w$, as $t$ ranges bijectively over
   $\mathbb F_q^*$. This uses a reparametrization of the usual diagonal
   torus. Its central-coordinate exponent is coprime to $q-1$.
4. $\operatorname{Aut}(S_N)=S_N\rtimes\langle F\rangle$, where
   $F:x\mapsto x^2$ has order $N$. Canonical subfield groups $S_d$ for
   $d\mid N$ have the corresponding subfield coordinates and ovoids.
5. Proper maximal subgroups are point stabilizers, odd-torus normalizers
   with cyclic Sylow 2-subgroups, and conjugates of proper subfield groups.
   A nonidentity odd-order element has a unique maximal odd cyclic torus
   as its centralizer. The normalizer of such a torus is proper.
6. $S_N$ is nonabelian simple. String C-groups correspond to regular
   abstract polytopes, with reversing the generator order corresponding
   to duality.

The root/torus assertions can equally be read in the standard four-by-four
matrix model. Restricting them to a subfield is compatible with the Suzuki
field automorphism: since $N/d$ is odd, its exponent restricts to the
canonical exponent for $\mathbb F_{2^d}$. In particular, the central
torus scaling parameter lies in a subfield exactly when its diagonal
parameter does. The torus acts faithfully on the nonzero central elements.

**Normalization theorem.** Inner-conjugacy classes of ordered triples
$(r_0,r_1,r_2)$ of involutions with $r_0\ne r_2$, $[r_0,r_2]=1$, and
$[r_0,r_1]\ne1$ are in bijection with

$$X_N=(\mathbb F_q\setminus\mathbb F_2)\times\mathbb F_q^*.$$

The representative for $(b,c)$ is

$$\bigl(z(1),\ wz(c)w,\ z(b)\bigr).$$

**Proof.** Conjugate $r_0$ to $z(1)$. Its commuting involutions are
exactly $z(b)$, and excluding the identity and $r_0$ means $b\ne0,1$.
Its centralizer $U_q$ fixes every such $z(b)$. The involution $r_1$
fixes a point other than infinity, since otherwise it would belong to
$U_q$ and commute with $r_0$. There is a unique element of $U_q$ that
moves that point to zero. The resulting $r_1$ is a central involution
of the root group at zero, hence $wz(c)w$ with $c\ne0$. No further
element of $U_q$ fixes zero, proving uniqueness. Conversely every
displayed pair gives a triple with the stated properties. ∎

Thus field automorphisms act on normalized coordinates simultaneously:

$$F(b,c)=(b^2,c^2).$$

Reversing the endpoints gives $(z(b),wz(c)w,z(1))$. Normalize its first
entry by split-torus scaling $t=b^{-1}$ to obtain the duality action

$$D(b,c)=(b^{-1},bc).$$

It is an involution commuting with $F$.

### 4.2. Generation is the field-of-definition test

**Subfield-position lemma.** If a conjugate of a canonical $S_d$, $d\mid N$,
contains $z(1)$ and $wz(c)w$, then it is the canonical $S_d$ itself.

**Proof.** The embedded ovoid of that conjugate contains infinity and
zero, because those are the unique fixed ovoid points of the two
involutions. The canonical $S_d$ is doubly transitive on its own ovoid.
Changing the conjugator on its $S_d$ side therefore makes it fix the
ordered pair $(\infty,0)$, so it belongs to $H_q$. Suppose its central
scaling is $t$. The conjugate root center is then $z(t\mathbb F_{2^d})$.
Since it contains $z(1)$, $t\in\mathbb F_{2^d}^*$. The torus/subfield
compatibility in §4.1 implies that the conjugator is in $H_{2^d}\le S_d$.
It consequently normalizes $S_d$, proving the claim. ∎

**Generation theorem.** The group generated by the normalized triple is
exactly $S_d$, where

$$\mathbb F_{2^d}=\mathbb F_2(b,c).$$

**Proof.** The displayed generators belong to $S_d$, and $d>1$ because
$b\notin\mathbb F_2$. If they generated a proper subgroup of $S_d$,
place it in a maximal subgroup. A point stabilizer cannot contain the
triple: its involutions would all fix that point, whereas the first
and middle generators fix different points. An odd-torus normalizer
cannot contain the four-group $\langle z(1),z(b)\rangle$, because its
Sylow 2-subgroups are cyclic. The remaining possibility is a conjugate
of $S_e$ for a proper divisor $e$ of $d$. The position lemma makes it
canonical, forcing $b,c\in\mathbb F_{2^e}$, a contradiction. ∎

This proves generation from field coordinates without retaining the
source's enumeration formula or its generation-count lemma.

### 4.3. Intersection property and the rank restriction

The first and middle involutions in a normalized triple do not commute;
neither do the middle and last, by their different fixed points. The
dihedral group generated by either adjacent pair has odd rotation order.
Indeed, if that order had 2-part at least four, its dihedral Sylow
2-subgroup would have noncommuting involutions, impossible inside a
Suzuki root group. If the rotation order had 2-part exactly two, its
central involution would centralize both generators, placing both in
one root group, whose involutions commute. Rotation order two is also
excluded by noncommutation.

Suppose these two odd-rotation dihedral subgroups intersect beyond their
common middle involution. Their intersection then contains a nontrivial
odd-order rotation $x$. Both rotation subgroups lie in the unique
maximal torus $C_{S_d}(x)$. Each adjacent dihedral subgroup normalizes
that torus, so all three generators lie in its proper normalizer. This
contradicts the generation theorem. Their intersection is consequently
exactly the order-two group generated by the middle involution.

The outer four-group intersects either odd-rotation dihedral subgroup
in exactly the appropriate endpoint subgroup, by order divisibility.
Together these statements give every rank-three subgroup-intersection
identity. Every normalized triple is therefore a nondegenerate string
C-group for its generated subfield group. Its adjacent product orders
are at least three.

There is no string C-group representation of $S_N$ of rank at least
four. In such a representation, $r_0$ commutes with every $r_j$ for
$j\ge2$. These involutions lie in the center of one root group and
therefore commute with each other. In particular $r_3$ commutes with
all $r_j$ for $j\ge2$, as well as with $r_0,r_1$ by the string
relations. This would be a nontrivial central element of $S_N$.
Ranks one and two cannot generate a nonabelian simple group.

Rank three always occurs: take $b$ of full field degree $N$ and $c=1$.
Finally, every involution of a group $S_N\le G\le\operatorname{Aut}(S_N)$
maps trivially to $G/S_N$, since that quotient has odd order. A proper
extension cannot be generated by involutions. This recovers the full
rank/existence statement of L085 quoted as L074, Theorem 3, without
using that theorem as an input.

### 4.4. One orbit theorem and the two counting formulas

Apply Theorem E.ExactSupportOrbits to the divisor poset of $N$. The normalization and generation theorems prove that the support is the joint field degree. If $A(d)$ counts data defined over $\mathbb F_{2^d}$, the exact-degree count is
\[
E(N)=\sum_{d\mid N}\mu(N/d)A(d).
\tag{E3}
\]
Every exact-degree datum has a Frobenius orbit of length $N$. The additional duality quotient requires the freeness argument that follows; it is not an automatic division by two.

For pairs of distinct commuting involutions, normalized data are just
$b\in\mathbb F_q\setminus\mathbb F_2$. Put

$$\lambda(d)=\frac1d\sum_{e\mid d}\mu(d/e)2^e.$$

For $d>1$, this is the number of Frobenius orbits of elements of exact
degree $d$; the two degree-one elements have already been excluded.
Unordered-pair reversal sends $b$ to $b^{-1}$. It fixes no Frobenius
orbit: if $b^{2^j}=b^{-1}$, then $F^{2j}b=b$, and the odd orbit
length implies $F^jb=b$, giving $b=b^{-1}$ and hence $b=1$ in
characteristic two. Therefore the number of unordered-pair classes is

$$\boxed{\frac12\sum_{d\mid N,\ d>1}\lambda(d).}$$

This is exactly L074, Theorem 1.

For polyhedra whose full group is $S_N$, the marked data are $X_N$
with exact joint field degree $N$. Here

$$A(d)=(2^d-2)(2^d-1).$$

Their Frobenius orbits all have length $N$. Duality fixes no orbit,
by its first-coordinate inversion and the same odd-degree argument.
Consequently the number of polyhedra up to isomorphism and duality is

$$\boxed{P(N)=\frac1{2N}\sum_{d\mid N}
   \mu(N/d)(2^d-2)(2^d-1).}$$

There are no self-dual examples. The formula also gives the complete
polytope count, by the rank restriction in §4.3. For prime $N$ it reduces
to $(q-2)(q-1)/(2N)$, the source's Theorem 4. For $N=3,5,9,15$ it
gives respectively $7,93,14476,35788085$.

### 4.5. Exact equivalence with the source's nested formula

This section proves equivalence for every odd $N$, not just agreement
of a finite table. Let $Q(N)$ be the number of Frobenius orbits on
all of $X_N$, including data of smaller joint degree.

Apply U.ExtensionOrbits to the projection onto the first coordinate, and stratify by its degree $n>1$. There are
$\lambda(n)$ first-coordinate orbits. After choosing a representative,
its stabilizer is generated by $F^n$ and acts on $\mathbb F_q^*$.
For $m\mid N/n$, the number of points fixed by $(F^n)^m$ is
$2^{nm}-1$. Möbius inversion gives

$$\psi(n,N)=\sum_{m\mid N/n}\frac1m
       \sum_{e\mid m}\mu(m/e)(2^{ne}-1)$$

orbits of this stabilizer. Therefore

$$Q(N)=\sum_{n\mid N,\ n>1}\lambda(n)\psi(n,N).$$

Alternatively stratify by the joint field degree $d$. Orbits on
exact-degree-$d$ pairs have length $d$, and their Frobenius equivalence
is the same whether computed in $\mathbb F_{2^d}$ or the larger
field. Thus $Q(N)=\sum_{d\mid N}E(d)/d$. Möbius inversion now gives

$$\frac12\sum_{d\mid N}\mu(N/d)Q(d)=\frac{E(N)}{2N}=P(N).$$

The expression on the left is precisely L074, Theorem 2. This derives
its full parameter range and nondegeneracy conclusion from the marked
field theorem, with all field-automorphism orbit corrections included.

### 4.6. Source auxiliaries and retained background

The preceding proof also locates the source's auxiliary counting statements. Lemma 7 is the divisor-poset instance of Möbius inversion used in §2; Lemma 8 is the formula for $\lambda$; Lemma 9 is the stabilizer-fiber formula for $\psi$; and Lemma 10 is $Q(N)/2$, before removing data of smaller joint field degree. Remark 1 is the prime-degree specialization. The source's second example follows by substituting $N=15$: the values of $\lambda$ at $3,5,15$ are $2,6,2182$, the corresponding values of $\psi(n,15)$ are $6559,10943,32767$, and $Q(15)/2=35788185$. Removing the smaller-degree counts $7$ and $93$ gives $35788085$. Its first example illustrates the same stabilizer $\langle F^n\rangle$: a degree-three coordinate in $\mathbb F_{2^{15}}$ is fixed by $F^3$, whereas a general second coordinate is not.

The earlier structural lemmas have a different status. Source Lemma 1 follows from the cyclic automorphism group of a finite field: a Frobenius power $F^j$ has square $F$ exactly when $2j\equiv1\pmod N$, which has a unique solution for odd $N$ and none for even $N$. The finite ovoid action and root-group consequences of Lemma 2, the ovoid size in Lemma 3, and the maximal-subgroup classification in Table 1 are retained in §4.1. We do not rederive Lemma 2's arbitrary-field Bruhat description or Lemma 3's assertion about plane sections of general ovoids. Those broader statements are not premises of our counting proof. Lemma 4's torus-order coprimality is likewise not used in place of the intersection argument: §4.3 uses uniqueness of the centralizer torus and proves the intersection directly. Lemma 5's involution count is $(q^2+1)(q-1)$ because each of the $q^2+1$ ovoid points supports $q-1$ central root involutions and every involution fixes exactly one point; its conjugacy assertion is among the retained structure facts. Lemma 6 is the classical Fermat congruence, and the definitions of ovoids, Möbius inversion and the counting function are inherited notation. This inventory distinguishes recovery of the principal classification from reproving every background statement printed in the source.


## 5. Panel systems with a nontrivial Borel subgroup

**Lemma E.CosetRealization.** Let a group $G$ act type-preservingly and flag-transitively on an incidence geometry of finite rank, and let $(x_i)_{i\in I}$ be a base chamber. Write $H_i=\operatorname{Stab}_G(x_i)$ and use a right action. Then
\[
H_i g\longmapsto x_i^g
\]
is a type-preserving $G$-equivariant isomorphism from the subgroup coset system to the given geometry.

**Proof.** Transitivity on one-object flags makes the map onto each type. It is well defined and injective because $x_i^g=x_i^h$ holds exactly when $gh^{-1}\in H_i$, which is equivalent to $H_i g=H_i h$. If two cosets share a representative $k$, their images are $x_i^k,x_j^k$ and are incident, as the base objects are incident. Conversely, if two images are incident, transitivity on flags of their two types supplies a $k$ carrying the base pair to them. The injective object correspondence then writes both cosets with that common representative. The map therefore preserves and reflects incidence. ∎


Let $G$ be finite, let $I$ be a finite type set, and let each panel subgroup $P_i$ contain $B$. Put $K_\varnothing=B$ and $K_S=\langle P_i:i\in S\rangle$ for nonempty $S$, with $K_I=G$. This marking by subgroups is different from a marking by individual involutions.

**Theorem E.PanelRecognition.** Suppose
\[
K_S\cap K_T=K_{S\cap T}\quad(S,T\subseteq I),\qquad [P_i:B]\ge2,
\tag{E4}
\]
and suppose the maximal parabolics $H_i=K_{I\setminus\{i\}}$ have typed coset Helly. Then their coset incidence system is a firm flag-transitive residually connected geometry with chamber stabilizer $B$. Conversely every finite-rank firm flag-transitive residually connected coset geometry is obtained this way by taking the panel stabilizers.

**Proof.** Equation (E4) identifies the stabilizer of every partial base flag with the corresponding $K_S$. U.Helly supplies a common group element in the cosets of every flag, and hence flag transitivity and identification of the residues with the corresponding coset systems in $K_S$. Each rank-one residue has $[P_i:B]$ elements, giving firmness. A rank-two residue is connected because its two panel subgroups generate $K_{\{i,j\}}$. For larger rank, all panel subgroups occur in proper deletions, so the residue group is generated by its maximal parabolics. The usual coset-path argument proves connectedness: paths multiply successive elements of those subgroups, and conversely their products give paths.

Conversely let $K_S$ stabilize the complementary base flag. Stabilizer intersections give (E4). In a connected residue, the subgroup generated by its maximal parabolics has exactly the orbit reachable by coset paths, so it is the whole residue group. Induction on $|S|$ reconstructs $K_S$ from the panels, starting with $K_\varnothing=B$. Flag transitivity gives typed Helly by moving a flag to the base flag. ∎

The source's remaining axioms are separate, exact local tests. RWPRI means that for every nonempty $S$ there is an $i\in S$ with $K_{S\setminus\{i\}}$ maximal proper in $K_S$. Local two-transitivity means that $P_i$ has two orbits on ordered pairs in $B\backslash P_i$; equivalently $B$ has two orbits on that coset set. The source's geometric $(\mathrm{IP})_2$ means that every rank-two residue is a partial linear space or a generalized digon. It is not the subgroup identity (E4).

For the last test let $P,Q$ be two panels, $P\cap Q=B$ and $K=\langle P,Q\rangle$. The coset graph is a digon exactly when $|P||Q|=|K||B|$. Otherwise local two-transitivity makes a single common-neighbour count sufficient. Choose $x\in Q\setminus B$. Neighbours of $P$ are the $Q$-cosets represented by a right transversal of $B$ in $P$; neighbours of $Px$ are their translates by $x$. The stabilizer $Q$ is two-transitive on its incident $P$-type points, so all distinct points having a common $Q$-type neighbour have the same number of common neighbours. This number must be one. Pairs with no common neighbour already satisfy partial linearity. This argument also applies when a local action has a nontrivial kernel.

### 5.1. Complete maximal-residue augmentation

**Lemma E.Transport.** Suppose representatives of all ambient $G$-conjugacy classes of subgroups $K$ and all $K$-conjugacy classes of maximal subgroups $H_0<K$ are given. For a specified $H$, choose any transporter $c$ with $H_0^c=H$ when one exists. All maximal overgroups of $H$ in that inclusion class are precisely $(K^c)^n$ with $n\in N_G(H)$.

**Proof.** Conjugate any maximal inclusion $H<L$ to a representative $K$ of the class of $L$. Its image of $H$ is $K$-conjugate to one of the listed $H_0$. Comparing the resulting transporter with $c$ leaves an element normalizing $H$. Conversely each displayed conjugate contains $H$ maximally. Taking the union over all inclusion classes gives every maximal overgroup. ∎

Let $\mathcal P(B)$ be the finite set of overgroups $P$ of $B$ such that $B$ is maximal proper in $P$ and $P$ acts two-transitively on $B\backslash P$. E.Transport computes this entire set by retaining only the relevant local inclusions. The normalizer $N_G(B)$ acts on $\mathcal P(B)$, and its permutation image has exactly the same configuration orbits. We retain the actual subgroups behind the permutation labels, so kernel reduction does not change any geometric test.

**Theorem E.MaximalAugmentation.** Start with all rank-one panels modulo $N_G(B)$. For every accepted panel tuple, let $H$ be its generated join. For every maximal overgroup $K$ of $H$, try every $P\in\mathcal P(B)$ with $P\le K$ and $P\nsubseteq H$, modulo the pointwise stabilizer of the old panel tuple. Apply E.PanelRecognition and all the local source tests, then remove duplicates under $N_G(B)$ and type permutations. Iterating until the next level is empty gives every target geometry with Borel $B$ and acting group a subgroup of $G$.

**Proof.** For a target rank-$r$ geometry, RWPRI supplies at least one maximal parabolic $H$ in its acting group $K$. Deleting its complementary panel gives a rank-$(r-1)$ residue with the same Borel and all inherited source axioms. Induction puts its panel tuple in a previously enumerated orbit. Its remaining panel lies inside $K$ and outside $H$, and E.Transport includes $K$ among the maximal overgroups to be tried. U.ExtensionOrbits shows that taking pointwise-stabilizer representatives loses no extension; a smaller stabilizer than the full setwise one merely permits duplicates. Final orbit tests remove those duplicates. Conversely every accepted tuple satisfies exactly the recognition and local conditions.

By (E4) and proper panels, adjoining a new type strictly enlarges the generated join: if $P_i$ lay in $K_S$ for $i$ outside $S$, then $P_i\cap K_S=B$ would force $P_i=B$. Hence every tuple gives a chain of strict subgroup inclusions from $B$. Its rank is at most $\Omega([G:B])$, the number of prime factors with multiplicity. Thus a run through the next level must reach an empty level. The certificate requires that emptiness, not merely a chosen numeric cap. Finally take $B$ over all $G$-conjugacy classes of subgroups. ∎

### 5.2. The Hall–Janko census

Apply this theorem to $G=J_2$. The retained TomLib catalogue has 146 subgroup classes and 568 maximal-inclusion classes, of which 417 are locally two-transitive. These are finite-group classification data, not a geometry list. The complete search tests 4,072 maximal-augmentation orbit representatives, distributed by ranks two through six as $644,1226,1931,271,0$. Every one of its 146 Borel anchors reaches an empty terminal level.

| Rank | Inner conjugacy and type permutations | Aut(J2) and type permutations |
| --- | ---: | ---: |
| 2 | 8 | 8 |
| 3 | 24 | 19 |
| 4 | 5 | 3 |
| At least 5 | 0 | 0 |

The final fusion uses the full automorphism group and exact successive subgroup transporters, not just equality of subgroup-order signatures. All 30 final representatives pass a separate check through their maximal parabolics: generation by panels, reconstruction of every panel by intersections, firmness, typed Helly, all residue-generation conditions, all RWPRI deletions, two-transitive panels and every rank-two partial-linearity/digon test. The three rank-four Borel orders are 1,1,8; their maximal-parabolic order multisets are respectively [12,150,60,60], [150,150,60,60] and [384,384,6048,6048].

**Corollary E.J2.** Under the stated complete subgroup catalogue and exact finite-group operations, these are all firm flag-transitive residually connected $J_2$ geometries satisfying RWPRI, $(2T)_1$ and $(\mathrm{IP})_2$: eight in rank two, nineteen in rank three and three in rank four, with none in any higher rank.

**Proof.** E.MaximalAugmentation proves exhaustion, including proper acting subgroups during intermediate stages. The complete finite output and separate final-witness tests give existence and exact full-automorphism/type equivalence. An empty terminal level at every Borel anchor excludes every further rank. This is not an inference from the absence of a rank-five object alone. ∎

## 6. Primitive rank-three geometries of the Mathieu group

For the next application the object stabilizers, rather than the panel stabilizers, are maximal. The distinction permits a smaller recognition test. Let $G$ be finite and let $H_1,H_2,H_3$ be distinct maximal proper subgroups. Put $H_{ij}=H_i\cap H_j$ and $B=H_1\cap H_2\cap H_3$. For distinct $i,j$ define
\[
R_{ij}=\{H_i h:h\in H_j\}.
\]
These are precisely the $H_i$-cosets incident to the base object $H_j$.

**Corollary E.PrimitiveTriples.** The right-coset system of $H_1,H_2,H_3$ is flag-transitive and residually connected if and only if
\[
\begin{split}
H_i&=\langle H_{ij},H_{ik}\rangle\quad(i=1,2,3),\\
|R_{ij}\cap R_{ik}|&=[H_{jk}:B]
\end{split}\tag{E6}
\]
where the second equality need only be checked for one choice of $i$. Every such geometry is firm.

**Proof.** Every incident pair of right cosets has a common element. Right multiplication therefore makes $G$ transitive on the flags of each two-type combination. Fix the base pair $H_j,H_k$. Its possible $i$-type completions are the elements of $R_{ij}\cap R_{ik}$. The stabilizer $H_{jk}$ has an orbit of size $[H_{jk}:B]$ containing $H_i$. The equality in (E6) says precisely that this orbit is the entire completion set. Thus all chambers can be moved to the base chamber. Conversely, flag transitivity implies this equality. This is U.Helly in rank three, with a finite cardinality test for its common-element condition.

In the flag-transitive system, the residue at $H_i$ is the bipartite coset graph of $H_i$ on $H_{ij},H_{ik}$. A path is a successive multiplication by elements of those two subgroups, and every such product gives a path. Its connectedness is therefore equivalent to the corresponding generation equality. The whole geometry is connected because any two distinct maximal subgroups generate $G$. These are all the residual-connectedness conditions in rank three.

If a panel had only one completion, one of the groups $H_{jk}$ would equal $B$. The residue-generation equality at $H_j$ would then give
$H_j=\langle H_{ij},B\rangle=H_{ij}$, contrary to distinct maximality of $H_i,H_j$. Hence every panel has at least two completions. This also derives the firmness hypothesis of E.PanelRecognition in this application. ∎

### 6.1. Exhaustive augmentation and the equivalence relation

**Lemma E.DistinctMaximals.** In a residually connected rank-three flag-transitive geometry whose three object stabilizers are maximal proper subgroups of $G$, the stabilizers of a base chamber are pairwise distinct.

**Proof.** Apply E.CosetRealization. If all three stabilizers equal $H$, cosets of different types are incident exactly when their underlying right cosets are equal. The whole incidence graph is a disjoint union of three-vertex complete graphs indexed by $H\backslash G$. Since $H$ is proper there are at least two components, contrary to residual connectedness at the empty flag.

Otherwise suppose $H_1=H_2=H$ and $H_3=K\ne H$. In the residue of the base third-type object $K$, the objects of either remaining type are precisely the cosets $Hk$ with $k\in K$. Two of opposite types are incident exactly when their underlying cosets coincide. The residue is therefore a disjoint union of edges indexed by $(H\cap K)\backslash K$. Distinct maximality implies $K\nsubseteq H$, so the index is at least two. The residue has rank two and is disconnected, again a contradiction. Every equality among two of the three stabilizers falls under one of these cases. ∎

By E.CosetRealization, every source flag-transitive geometry is the coset system of a base-chamber stabilizer family. E.DistinctMaximals makes that family one of the distinct maximal triples considered here.

Let $\mathcal M$ be the complete set of maximal subgroups of $G$, and let $A=\operatorname{Aut}(G)$ act on it. Apply U.ExtensionOrbits first to pairs of distinct members of $\mathcal M$. One may fix a representative of each $A$-orbit of the first member and then take orbits of its stabilizer on the second members. Fuse the resulting unordered pairs under $A$. For each surviving pair $e$, take the orbits of its setwise stabilizer $A_e$ on $\mathcal M\setminus e$, attach one third member, and test (E6). Finally fuse accepted unordered triples under $A$.

Every triple has a distinguished pair. Moving that pair to its orbit representative and then using its stabilizer puts the third member in one of the tested positions. All tests are invariant under the action. Thus the search is exhaustive. Different choices of distinguished pair may give the same triple orbit, which is why the last fusion is necessary. Conversely every accepted triple satisfies the geometric recognition theorem. The equivalence being computed is full group-automorphism conjugacy together with arbitrary type reordering. No assertion that arbitrary incidence isomorphisms of every coset geometry lift to automorphisms of $G$ is needed.

The action may be replaced by its actual permutation image on $\mathcal M$: each image element has an automorphism lift, so its orbits and transporters give exactly the same equivalence. This matters for the catalogue model of $M_{22}$, which has two fixed points on a 24-point domain. Its ambient permutation normalizer has order $1\,774\,080$, while the centralizer of $G$ in that normalizer has order two. The conjugation image has order $887\,040$, equal to the order of the separately computed full automorphism group. Counting normalizer elements as distinct automorphisms would be unjustified; taking the image gives the correct action.

### 6.2. The finite census and its geometric realization

Take $G=M_{22}$. The retained TomLib subgroup catalogue has 156 conjugacy classes. Its maximal-class indices are independently compared with the maximal elements of the supplied subgroup-containment relation. There are eight maximal classes and 2,300 maximal subgroups. The independent-input search finds 81 unordered maximal-pair orbits and 431 accepted maximal-triple orbits. It tests 11,866 triples and accepts 1,193 before full automorphism fusion. No source geometry list, table row or anticipated count is an input.

**Corollary E.M22.** Conditional on the declared complete subgroup catalogue and exact finite-group algorithms, there are 81 rank-two and 431 rank-three flag-transitive residually connected geometries for $M_{22}$ with maximal object stabilizers, under the source's automorphism/type equivalence.

**Proof.** Two distinct maximal subgroups give a connected, firm, flag-transitive rank-two coset geometry: they generate $G$, and their intersection has index at least two in each. Corollary E.PrimitiveTriples gives exactly the rank-three test. The complete augmentation argument and its finite output prove exhaustion. A separate author-written checker tests all witnesses again, including all three choices in the cardinality test, all residue-generation equalities and all panel indices. Exact orbit transporters prove inequivalence. ∎

The object names can also be recovered directly from the same subgroup action. Let $\Lambda$ be the 22 moved points and $p,q$ the fixed points. In source order the maximal classes have orders
\[
20\,160, 5\,760, 2\,520, 2\,520, 1\,344, 1\,920, 720, 660.
\]
Their distinguished orbits on $\Lambda$ have sizes
$1,6,7,7,8,2,12,11$. Each of the first seven classes has a unique distinguished orbit; the last has two complementary 11-point orbits. Every distinguished subset is checked to have precisely the corresponding subgroup as its set stabilizer. The eight families contain respectively
\[
22, 77, 176, 176, 330, 231, 616, 1\,344
\]
subsets. The last family gives only 672 different stabilizers.

Add $\{p,q\}$ to every six-set, add $p$ to the first seven-set family and $q$ to the other, and retain the eight-sets. The result consists of 759 eight-subsets of a 24-point set. The finite certificate checks that every one of its $\binom{24}{5}=42\,504$ five-subsets occurs in exactly one block. Thus this is an actual Steiner system $S(5,8,24)$. The group $G$ preserves it and fixes $p,q$. We retain the classical uniqueness of this Steiner system and the standard identification of its automorphism group with $M_{24}$, with two-point stabilizer of order $443\,520$. Since $|G|=443\,520$, the embedding is the required two-point stabilizer. This identifies the construction with the source's MOG model up to relabeling and possible interchange of $p,q$.

The certificate next forms the symmetric differences of every pair of octads meeting in two points. The resulting 2,576 dodecads give exactly the 616 dodecads contained in $\Lambda$, and deleting $p$ or $q$ from a dodecad containing exactly that fixed point gives exactly the 1,344 endecads. Hence the eight maximal-class names are the source's point, hexad, two heptad classes, octad, duad, dodecad and endecad. The endecad complement ambiguity is an actual two-to-one shadow-to-stabilizer map. The action on the corresponding coset objects is faithful: by U.Orbits its kernel is the intersection of the subgroup cores, and every proper-subgroup core in the simple group $M_{22}$ is trivial. The two complementary shadows still define the same object stabilizer; they are not separate types in the subgroup census.

### 6.3. Scope of the fourth-source comparison

The preceding theorem independently recovers the numerical classification in Leemans–Rowley (2010), with explicit witnesses and geometric shadows. Its full printed table has a stronger comparison obligation. Each of the 431 printed rows is recorded separately, including its physical page, Number, maximal-class label, pairwise intersection values and Borel-group label. These source rows are read only after the census.

At the present draft stage the exact meanings of some refined pair-orbit subscripts and colon labels remain unverified because the older Kilic–Rowley source defining them has not been acquired. The source's linked external witness file currently returns a 404 response. A coarse comparison that forgets those refinements finds 419 order-compatible matches in a maximum bipartite matching, not a complete source-row identification. The source also literally prints Number 61 twice and no Number 62. Its row $M_{133}(0,3,1)$ assigns intersection size three to a point and a heptad, contrary to its own definition. Neither observation determines the authors' intended replacement labels.

The independent census and canonical witness table therefore stand as a proved author component of the proposed fourth-source expansion, subject to external review. They do not yet discharge the full source-table contract. The outstanding source-specific labels and all diagnostic discrepancies are retained explicitly in the accompanying comparison ledger; no four-source whole-contract credit follows from this section alone.

## 7. Source scope and retained inputs

The exact source editions are the nine-page author manuscript of Kiefer–Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*; the twelve-page author manuscript dated 27 September 2011 of *On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)*, whose journal year is 2010; and the five-page 2002 journal article *The residually weakly primitive geometries of J2*. Publisher-edition collation of the first two is not silently presumed.

For commuting involutions, the full ambient automorphism equivalence is essential in degree six. The nonexceptional automorphism theorem is retained; in degree six the complete exact automorphism action is computed. The source's Remark 3.4 concerns reversal of an endpoint pair and does not establish self-duality of every completed polyhedron. Theorem 4.4 concerns regular polyhedra. Both boundaries are preserved.

For Suzuki groups, the root groups, ovoid action, torus and odd-element centralizers, compatible subfield embeddings, maximal-subgroup types, automorphism group and simplicity are named retained classical inputs. The principal formulas and generation theorem are proved from those inputs. The rank/existence result restated as the source's Theorem 3 is also derived, but the original 2006 L085 full body has not been acquired and is not a separate whole-source intake.

For $J_2$, the subgroup catalogue and the exact GAP algorithms remain substantial inputs. Neither the original geometry list nor the supplementary representatives are used to establish completeness. The principal contract is the census with its stated local conditions. The source's main body also prints rank-four diagrams, full automorphism and correlation groups, and a doubling relation; these printed statements and the complete collection of secondary supplement annotations are not all rederived here. Agreement with the principal census does not establish every assertion in either the body or the supplement.

The intake and its precise deductions can be summarized as follows. A complete principal contract concerns the declared main conclusions; it is not an assertion that every source lemma has been replaced.

| Source | Shared result and local argument | Recovered conclusion | Boundary |
| --- | --- | --- | --- |
| Kiefer–Leemans (2013), L066 | U.Orbits and U.ExtensionOrbits; §§3.1–3.3 | Both all-degree formulas, the five exceptional endpoint classes, and the full $S_6/A_6$ polyhedron classification | Ambient automorphism theorem and polytope correspondence retained; Remarks 3.4 and 3.7 keep their stated scope |
| Kiefer–Leemans (2010), L074 | U.ExtensionOrbits and E.ExactSupportOrbits; §§4.1–4.5 | Both counting theorems for every odd exponent, generation, nondegeneracy, no self-duality and the prime specialization | Classical Suzuki structure retained; the older L085 body is not an additional complete intake |
| Leemans (2002), L104 | U.Helly and U.ExtensionOrbits; panel recognition and maximal augmentation in §5 | The complete $8/19/3$ census and exclusion of every higher rank | Complete subgroup catalogue retained; further printed diagrams, correlation groups and doubling data not all recovered |
| Leemans–Rowley (2010), L073 | U.ExtensionOrbits, E.CosetRealization and E.PrimitiveTriples | The complete $81/431$ census, explicit witnesses and eight geometric shadow families | Qualified component: refined source-table labels remain unmatched |

The general orbit, Möbius and subgroup-transporter arguments are standard methods. Their shared organization, explicit applications and independent certificates are the work of this manuscript; no historical priority or newly solved open conjecture is claimed. Mathematical recognition, exact finite computation and formal proof assistants are distinct forms of evidence. No complete source theorem in this manuscript is currently claimed to have an end-to-end Lean certificate.

## Appendix. Complete certificate interfaces

The degree-six classification uses the full `phase110_commuting_pairs_integration_finite.g`, with the independently reviewed exact execution and all output classes. The all-degree floor formulas are written proofs; `phase110_commuting_pairs_integration_formula.py` is an additional exact diagnostic, not their premise. Its fourteen source table rows, reversible multiplicity coordinates and coefficient comparisons remain available in full. The corrected phase116 ledger governs the old source-bank spans; `phase164_enumeration_ledger.json` binds the complete sections of this manuscript and distinguishes its three principal source contracts from its qualified fourth-source component.

The J2 computation consists of `phase5_j2_search.g`, `phase5_j2_fuse.g`, `phase5_j2_verify.g`, and the complete shared `phase4_geometry_checks.g`. The first program enumerates every Borel anchor and writes an empty terminal checkpoint. The second fuses all accepted J2 witnesses under the full automorphism group and type permutations. The third reconstructs and verifies every final geometry through its maximal parabolics. The exact 146 terminal checkpoints, output representatives, complete input/output hashes and prior independent audit are part of the finite evidence. The full executable programs, actual driver infrastructure and retained-data assumptions are charged; a short table of totals alone is not the certificate.

The Suzuki written proofs hold for all allowed odd exponents. The separate finite-field diagnostic checks exact formula equivalence in 49 odd degrees and exhausts normalized pairs at $q=8,32,512$. The matrix diagnostic checks all 42 normalized $q=8$ triples, 2,688 subgroup intersections and the duality conjugations. These finite samples support implementation and are not substitutes for the normalization, generation or all-parameter orbit proofs.

The $M_{22}$ computation uses `phase164_m22_census.g`, `phase164_m22_validate.g` and `phase164_m22_shadows.g`. The census constructs all 2,300 maximal subgroups from the declared catalogue, forms the full automorphism image and exhausts the pair-extension fibers. The separate author-written validator checks every returned pair and triple, every required coset-cardinality and residue-generation equality, and pairwise inequivalence. It cannot replace the census's exhaustiveness proof. The shadow program reconstructs the actual Steiner system, its dodecads and endecads, and the geometric data of each representative. The frozen checkpoint and its additive source-to-coset bridge are retained intact. The source table is used only in the separate post hoc diagnostic and is not an input to these three programs.

The portable driver is invoked as follows, from the artifact directory:

```text
python3 phase164_enumeration_run.py --part all --output-dir NEW
```

The alternatives `--part small`, `--part j2` and `--part m22` select the degree-six/Suzuki diagnostics, the complete Hall–Janko census, and the complete Mathieu census respectively. Every mode refuses an existing output path, verifies the exact mathematical programs before execution, and stages all source-relative paths under a new working directory. The driver records GAP and TomLib versions, hashes the installed subgroup-data files and checks completion markers and output counts. The $J_2$ branch independently checks that all 146 terminal checkpoints exist and end with an empty level. Python assertions remain enabled for the historical Suzuki diagnostic. No existing certificate is overwritten.

The written proofs reuse the exact reviewed predecessor arguments; a fresh execution of an unchanged program validates the portable interface and is not a new theorem. Full code is distributed as mathematical artifacts rather than printed in long pages of the exposition. The complete U body, application proofs, necessary mathematical programs, executable drivers and retained-data assumptions remain separately charged. The ledger distinguishes mathematical input, computational output, audit infrastructure and the renderer. No source-length ratio follows from the page count of this exposition, and the new $M_{22}$ computation carries no whole-source credit until its table contract is resolved.

## References

[U] *Marked groups, kernels and intersections*, companion manuscript, third edition. Interfaces U.Orbits, U.ExtensionOrbits and U.Helly.

[KL13] A. Kiefer and D. Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*, Communications in Algebra 41 (2013), 4408–4418; declared nine-page author edition.

[KL10] A. Kiefer and D. Leemans, *On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)*, Journal of Combinatorial Theory A 117 (2010), 1248–1257; declared author manuscript dated 27 September 2011.

[L02] D. Leemans, *The residually weakly primitive geometries of J2*, Note di Matematica 21 (2002), 77–81.

[LR10] D. Leemans and P. Rowley, *Rank three residually connected geometries for M22, revisited*, Electronic Journal of Combinatorics 17 (2010), N4, 9 pages.

[C76] R. T. Curtis, *A new combinatorial approach to M24*, Mathematical Proceedings of the Cambridge Philosophical Society 79 (1976), 25–42. Classical Steiner-system uniqueness and the Mathieu-group identification are retained.

[MS] P. McMullen and E. Schulte, *Abstract Regular Polytopes*, Cambridge University Press, 2002. The string-C-group/polytope correspondence is retained.

The classical Suzuki structure and full subgroup data are specified in the exact source/retained-input ledger. The related 2006 Suzuki rank theorem is used only through its primary restatement. Section 6 proves a new author derivation of the 2010 M22 census, but complete recovery of its refined source table remains a separate, explicitly open intake obligation.
