# Dihedral RWPRI geometries: a uniform arithmetic classification

Status: independently derived paper proof, with an exact finite-set check described below. This rederives an already published classification; it is not a new conjecture resolution or a claim of priority. No external peer review is represented.

## 1. Source boundary

Dimitri Leemans, *The residually weakly primitive geometries of the Dihedral Groups*, Atti Sem. Mat. Fis. Univ. Modena **48** (2000), 179–190, MR1767379, is catalogue L109. Its [author abstract](https://www.math.auckland.ac.nz/~dleemans/abstracts/d2n.html) explicitly announces an all-n classification and automatic firmness, residual connectivity, flag transitivity and the intersection property in rank-two residues. The [ULB repository record](https://difusion.ulb.ac.be/vufind/Record/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/232363/Holdings) says that no files are associated with the record. Searches on 2026-10-10 did not obtain the article full text.

There is, however, an exact primary anchor: Leemans, *The rank 3 geometries of the simple Suzuki groups Sz(q)*, Note Mat. **19** (1999), 43–63, [publisher PDF](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837), §2 and Theorem 5.1, printed pp. 45–46 and 51–52. The theorem explicitly attributes the complete dihedral rank-two classification to L109. It gives one class for the Klein four group, and, for $n\ge3$, exactly $2m+\binom m2$ classes, where $m$ is the number of distinct prime divisors of $n$. Its three subgroup families are recovered in §6 below. The §2 definition of RWPRI is the subgroup condition used here; no locally two-transitive axiom is imposed.

The all-rank principal classification also has an exact primary anchor: Leemans, *The residually weakly primitive pre-geometries of the Suzuki simple groups*, Note Mat. **20** (2000/2001), [publisher PDF](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995), Theorem 4, printed pp.9–10. It cites L109 as reference [20] and reproduces its three dihedral families, automatic firmness, residual connectivity and flag transitivity, and the complete rank-$\alpha$ count

\[
\binom m{\alpha-1}+\binom m\alpha+m\binom{m-1}{\alpha-2},
\qquad 2\le\alpha\le m+1,
\]

for $n>2$. The three diagrams correspond respectively to our rotation factor, single prime factors, and one polygon factor. Thus the all-rank published theorem, including its class count, is recovered by Theorem A and Corollary A.1 below; the identification is stronger than an abstract-level comparison.

The unavailable L109 full text still prevents a statement-by-statement comparison with every result of that paper, so this is a rederived principal component rather than a whole-paper reduction claim. Our equivalence convention is explicit: **group–coset-system pairs up to an automorphism of the specified group and permutation of types**. The source's reproduced subgroup diagrams and count agree with this convention. These are not bare incidence structures after forgetting the action; the latter counts can be smaller.

## 2. Definitions and the result

Write

\[
 D_{2n}=\langle r,s\mid r^n=s^2=1, srs=r^{-1}\rangle,
 \qquad n\ge2.
\]

For a family of proper subgroups $G_i<G$ indexed by a nonempty finite set $I$, put $G_J=\bigcap_{j\in J}G_j$, with $G_\varnothing=G$. Its standard coset pregeometry has typed left cosets $gG_i$, incident when their intersections are nonempty. Call the family RWPRI if, for every proper subset $J\subsetneq I$, at least one $i\notin J$ satisfies

\[
G_{J\cup\{i\}}\text{ is a maximal proper subgroup of }G_J. \tag{R}
\]

This permits a kernel in the group action. Faithfulness is not silently added.

Let $\mathcal P$ be the set of distinct prime divisors of $n$, and define

\[
 R=\langle r\rangle,\qquad H(p,a)=\langle r^p,r^as\rangle
 \quad(p\in\mathcal P, a\in\mathbb F_p).
\]

**Theorem A (all ranks, all $n$).** Every RWPRI family in $D_{2n}$ is exactly one of the following, with arbitrary indicated residues $a$:

1. **Single prime factors:** choose a nonempty subset $S\subseteq\mathcal P$, and one $H(p,a_p)$ for each $p\in S$.
2. **Rotation factor:** choose any $S\subseteq\mathcal P$, take $R$, and one $H(p,a_p)$ for each $p\in S$.
3. **One polygon factor:** choose $p\in\mathcal P$, distinct $a,b\in\mathbb F_p$, and any $S\subseteq\mathcal P\setminus\{p\}$; take $H(p,a),H(p,b)$ and one $H(q,a_q)$ for each $q\in S$.

Conversely, each listed family is RWPRI. In fact, **every** edge of its parabolic intersection lattice is a maximal-subgroup inclusion, strengthening the existential condition (R).

Every listed coset system is a firm, residually connected, flag-transitive geometry. Its incidence structure is respectively:

1. the join of rank-one sets of sizes $p$, for $p\in S$;
2. those factors together with a rank-one set of size $2$;
3. a $2p$-cycle as a rank-two incidence geometry, joined with rank-one sets of sizes $q\in S$.

A join declares all elements from different factors incident. Every rank-two residue is consequently either a complete bipartite graph or a cycle. In particular it has the geometric rank-two intersection property.

**Corollary A.1 (exact counts).** For $n>2$, put $m=|\mathcal P|$, and use the convention $\binom ab=0$ if $b<0$ or $b>a$. The number of rank-$k\ge1$ families up to group automorphism and type permutation is

\[
 N_{n,k}=\binom mk+\binom m{k-1}+m\binom{m-1}{k-2}. \tag{1}
\]

The maximum rank is $m+1$, and there are $m+1$ classes of that rank. For $n=2$, the Klein four group has one rank-one and one rank-two class, and none of higher rank.

The three summands in (1) must not be merged merely because two underlying geometries happen to be isomorphic. For example, when $n>2$ is even, the families $\{R,H(2,0)\}$ and $\{H(2,0),H(2,1)\}$ both give a four-cycle but are not equivalent under an automorphism of $D_{2n}$: its rotation subgroup is characteristic.

## 3. A reusable maximality theorem

Call a subgroup-closed class of finite groups **rank-two rigid** if, whenever $A,B<H$ are distinct proper subgroups of a member $H$, $A$ is maximal in $H$, and $A\cap B$ is maximal in both $A$ and $B$, then $B$ is maximal in $H$.

**Lemma B.** In a rank-two-rigid, subgroup-closed class, every RWPRI family has all its parabolic lattice edges maximal.

**Proof.** Induct on the rank $k$. Rank one is the definition and rank two is the rigidity property. For $k\ge3$, the family $(G_i\cap G_j)_{j\ne i}$ inside each $G_i$ is RWPRI. By induction all its edges are maximal; in particular $G_i\cap G_j$ is maximal in both $G_i$ and $G_j$. Condition (R) at the empty set supplies some $G_0$ maximal in $G$. Rank-two rigidity applied to $G_0,G_j$ makes every $G_j$ maximal in $G$. All remaining edges lie in a lower-rank residue, so the induction covers them too. □

This removes hypotheses rather than merely renaming them: checking existential weak primitivity supplies every local maximality condition for this class. It is not valid for arbitrary finite groups; the rank-two rigidity assumption is essential.

## 4. Cyclic and dihedral groups are rank-two rigid

Every subgroup of a cyclic or dihedral group is cyclic or dihedral. We include the trivial group in the class.

In a cyclic group $C_n=\langle r\rangle$, write a subgroup as $C(d)=\langle r^d\rangle$, $d\mid n$. Intersections replace $d,e$ by $\operatorname{lcm}(d,e)$. Suppose $A=C(p)$ is maximal, so $p$ is prime. If $B=C(d)$ and $p\mid d$, then $B\le A$, contradicting that their intersection is proper in $B$. Thus $p\nmid d$. The index of $A\cap B$ in $A$ is $d$; maximality forces $d$ prime, so $B$ is maximal in $C_n$.

In $D_{2n}$, all subgroups are either $C(d)=\langle r^d\rangle$, or

\[
 H(d,a)=\langle r^d,r^as\rangle,\qquad d\mid n,\quad a\pmod d.
\]

Their maximal subgroups in $D_{2n}$ are precisely $R=C(1)$ and the $H(p,a)$ for prime $p\mid n$. To verify rigidity choose a maximal $A$.

* If $A=R$, then $B$ cannot be cyclic. Write $B=H(d,b)$. The intersection is $C(d)$, and maximality in $R$ forces $d$ prime. Hence $B$ is maximal.
* Let $A=H(p,a)$ and $B=C(d)$. Their intersection is $C(\operatorname{lcm}(p,d))$. Its properness in $B$ forces $p\nmid d$. The intersection lies in the rotation subgroup $C(p)<A$, so maximality in the whole group $A$ forces it to equal $C(p)$; hence $\operatorname{lcm}(p,d)=p$, so $d=1$ and $B=R$.
* Let $A=H(p,a)$ and $B=H(d,b)$. If $p\nmid d$, the congruences for the reflection exponents are compatible, so their intersection is dihedral with rotation step $pd$. Its index in $A$ is $d$, and maximality forces $d$ prime. If $p\mid d$ and $b\equiv a\pmod p$, then $B\le A$, which is impossible. Otherwise their intersection is $C(d)$. Maximality in $A$ forces $C(d)=C(p)$, whence $d=p$.

These cases include reflection subgroups of order two and the Klein four group. They prove rigidity and, by Lemma B, every maximal parabolic of a dihedral RWPRI family is a maximal subgroup of $G$.

The same argument also completely classifies cyclic RWPRI families: in $C_n$ they are exactly nonempty selections of its prime-index subgroups. For $m$ distinct prime divisors there are $\binom mk$ rank-$k$ classes, and every resulting geometry is the join of rank-one sets of those prime sizes. Intersections and coset Helly are respectively the lcm rule and CRT.

## 5. Irredundancy leaves exactly three patterns

Condition (R) with $J=I\setminus\{i\}$ makes $G_I<G_{I\setminus\{i\}}$, so deleting any subgroup changes the total intersection. Thus the family is irredundant.

Among the maximal subgroups, two distinct $H(p,a),H(p,b)$ intersect in the rotation subgroup $C(p)$. Any third subgroup indexed by the same prime contains that intersection and is redundant. If there are two doubled primes, one member of either pair is redundant: the other doubled prime already removes all reflections, while its partner imposes the same rotational divisibility. A doubled prime together with $R$ is redundant for the same reason. There can only be one $R$.

This leaves exactly the three patterns in Theorem A. In each, all intersections are obtained by multiplying distinct prime steps, retaining a reflection exactly until either $R$ or a doubled prime occurs. Each additional condition has prime index $p$, or index $2$ when it first removes the reflections. The index is always greater than one. Hence every parabolic edge is maximal, proving the converse and the algebraic classification.

## 6. Cosets, Chinese remainders and the geometry

Represent a group element as $r^z s^\epsilon$, with $z\in\mathbb Z/n\mathbb Z$, $\epsilon\in\{0,1\}$. A left coset of $H(p,a)$ is exactly one level set

\[
 z-\epsilon a=x\pmod p,\qquad x\in\mathbb F_p, \tag{2}
\]

and a coset of $R$ fixes $\epsilon$.

Conditions (2) at distinct primes are independent by the Chinese remainder theorem. Every such coset is incident with every coset of a different prime, and with both cosets of $R$. Two selected types at the same prime, $a\ne b$, are incident exactly when their labels satisfy

\[
 y-x\in\{0,a-b\}. \tag{3}
\]

The resulting bipartite graph is a $2p$-cycle: each vertex has two neighbors and moving two steps translates its label by the nonzero element $a-b$, which generates the additive group of $\mathbb F_p$. For $p=2$ this is the complete bipartite graph $K_{2,2}$.

Every pairwise incident set of typed cosets has common intersection. Indeed, in the rotation pattern its $R$-coset chooses $\epsilon$; in the polygon pattern, if both polygon types occur, (3) chooses $\epsilon$; otherwise choose either value. The remaining equations independently determine $z$ modulo distinct primes, and CRT solves them. No pattern contains both a rotation type and a doubled prime.

This is the typed Helly property, proved here rather than imposed. A common element translates a flag to a subflag of the standard chamber, so the coset system is a flag-transitive geometry. Prime panel indices prove firmness. Every residue of rank at least two is a join of nonempty factors, or the surviving polygon: its incidence graph is connected. Finally, its rank-two residues are complete bipartite graphs or cycles. A pair of vertices on one side has at most one common neighbor unless the whole graph is complete bipartite; this proves the rank-two shadow intersection condition directly.

In rank two, the three cases are exactly the primary Theorem 5.1:

| Family | Subgroups | Borel subgroup | Incidence graph |
| --- | --- | --- | --- |
| Rotation plus prime $p$ | $R,H(p,a)$ | $C(p)$, order $n/p$ | $K_{2,p}$ |
| Doubled prime $p$ | $H(p,a),H(p,b)$, $a\ne b$ | $C(p)$, order $n/p$ | cycle of length $2p$ |
| Distinct primes $p,q$ | $H(p,a),H(q,b)$ | dihedral, order $2n/(pq)$ | $K_{p,q}$ |

## 7. Counting group–geometry pairs and an optional local-action consequence

For $n>2$, every automorphism of $D_{2n}$ has

\[
r\longmapsto r^u,\qquad s\longmapsto r^vs,\qquad (u,n)=1,
\]

and sends $a\pmod p$ to $ua+v\pmod p$. CRT lets us independently prescribe the nonzero $u\pmod p$ and the shifts $v\pmod p$ at the distinct primes. It is therefore transitive on all residue choices in each of the three patterns, including any distinct ordered pair at the one doubled prime. It preserves $R$, each prime index, and the doubled-prime pattern, so different listed choices of $S,p$ cannot fuse. Counting these choices gives (1). The $n=2$ automorphism group is $S_3$, permuting all three maximal subgroups, and fuses the exceptional patterns as stated.

There is no locally two-transitive requirement in Theorem A. If one elects to add it, the panel actions above give an additional exact corollary:

* For the single-prime-factor pattern, every selected prime must be $2$ or $3$: the panel action is the dihedral action on $p$ points (faithful for odd $p$, and with image $C_2$ for $p=2$).
* For the rotation pattern, every selected prime must be $2$: after the rotation condition, the panel action is a cyclic group of prime order $p$, which is two-transitive only for $p=2$.
* For the polygon pattern, the polygon panels always have size two; every extra prime factor must be $2$, because its panel action is cyclic of that prime order.

Consequently rank is at most three under this extra axiom. Rank three occurs exactly by joining a $2p$-cycle, for an odd prime $p\mid n$, to a two-point factor, with $2\mid n$. In particular, odd dihedral groups have no rank-three RWPRI and locally two-transitive geometry. This recovers the dihedral obstruction used in L114 §6 without subgroup enumeration.

## 8. What was compressed, and what was not

The substantive common input is Lemma B plus elementary subgroup arithmetic and the CRT typed-Helly argument. Together they replace all-n searches for (a) parabolic candidates, (b) weak primitivity in every residue, (c) flag transitivity, (d) residual connectivity and (e) rank-two intersection. Formula (1) is an immediate finite combinatorial consequence.

This does **not** replace the subgroup structure of Suzuki, sporadic or classical groups, and rank-two rigidity is a real restriction. It does provide a proved replacement for every dihedral residue-classification call in those programs. It also illustrates why retaining the common group torsor matters: bare geometry isomorphism can merge different actions and lose the subgroup information needed in an ambient-group classification.

The exact checker `phase5_dihedral_check.py` independently builds small dihedral subgroup lattices from multiplication, tests the RWPRI condition, compares the predicted patterns and automorphism-orbit counts, and verifies typed coset Helly in representative systems. These finite checks audit the proof; they are not the basis for its all-n assertion. Source assets and executable/report hashes are recorded separately in `phase5_dihedral_intake.json` after the run.
