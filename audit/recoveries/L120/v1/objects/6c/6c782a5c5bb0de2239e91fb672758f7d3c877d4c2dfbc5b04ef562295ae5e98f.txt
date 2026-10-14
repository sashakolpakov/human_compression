# Phase 19: a rank-three unitary generation template

Date: 2026-10-10. **Proposed theorem under internal review; not externally peer reviewed.** No publication-priority claim. This note is independent of the unsuccessful direct folds. The main generation argument is written explicitly below; bounded computations alone are not its justification.

## 1. Statement and matrices

Let $q=p^e\ge5$ be odd, $E=\mathbb F_{q^2}$, and $\bar x=x^q$. Choose $z\in E$ with
\[
 \bar z=-z,\quad z\ne0,\quad \mathbb F_p(z^2)=\mathbb F_q.
\]
Such a parameter always exists: take $z^2$ to be any primitive element of $\mathbb F_q$, which is a nonsquare. Put $s=-z^2$, so $s\ne0,-1$, and set
\[
 H=\operatorname{diag}(1,-1,1,-1),\quad
 A=\operatorname{diag}(1,1,-1,-1),\quad
 C=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix},\quad
 v=(z,-1,s-z,s+1)^t,\qquad
 B=I+v\bar v^tH.
\]
Use the column Hermitian form $h(x,y)=\bar x^tHy$. Direct calculation gives $h(v,v)=-2$, so $B$ is its unitary reflection with exceptional eigenline $Ev$. In particular $B^2=I$ and $\det B=-1$. Also $A,C$ are unitary involutions of determinant one and $AC=-CA$.

**Proposed theorem.** The matrix group $\langle A,B,C\rangle$ contains $\operatorname{SU}_4(q)$ for every such parameter and every odd $q\ge5$. Its projective image therefore is:

- $\operatorname{PGU}_4(q)$ when $q\equiv1\pmod4$;
- the diagonal index-two extension of $\operatorname{PSU}_4(q)$ when $q\equiv3\pmod8$;
- $\operatorname{PSU}_4(q)$ when $q\equiv7\pmod8$.

The projective triple $(A,B,C)$ is a rank-three string C-group in every case. This does **not** address the diagonal index-two extension when $q\equiv7\pmod8$, nor the exceptional field $q=3$.

The final C-group deduction uses the rank-three intersection principle of Conder--Oliveros, with the precise same-marking criterion in Baktybekov--Conder--Nuzhin--Rezantseva (2025), Theorem B. Section 6 gives the full elementary argument needed here: absence of a nontrivial cyclic normal subgroup forces the actual marking to satisfy IP.

## 2. The parabolic projection and its field

Let $U=(BC)^2$, $n=v+Cv=s(1,1,1,1)^t$, and $m=An=s(1,1,-1,-1)^t$. The plane $W=\langle n,m\rangle$ is totally isotropic. Calculation gives
\[
 U|_W=\begin{pmatrix}1&t\\0&1\end{pmatrix},\quad
 A|_W=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 C|_W=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
 t=2s(z-1).
\]
Moreover $(U-I)^2=2n\bar n^tH\ne0$ and $(U-I)^3=0$: $U$ has Jordan type $(3,1)$. To verify this without division by three, write $w=Cv$, $\phi=\bar v^tH$, $\psi=\bar w^tH$. Then $U-I=v\phi+w\psi+2v\psi$, $(U-I)v=2n$ and $(U-I)w=-2n$. Equivalently $BC$ has eigenvalues $1,1,1,-1$ with one size-three block at eigenvalue one. The parameter is nonzero.

We have $\mathbb F_p(t^2)=E$. Indeed,
\[
 t+\bar t=-4s,\qquad t-\bar t=4sz,\qquad
 t^2-\bar t^2=-16s^2z\ne0.
\]
Let $E_0=\mathbb F_p(t^2)$. Since $E_0\not\subseteq\mathbb F_q$, the extension degree $[E:E_0]$ is odd: a divisor of $2e$ not dividing $e$ has the same two-adic valuation as $2e$. Since $t^2\in E_0$, odd degree gives $t\in E_0$. Finite subfields are stable under the bar automorphism, so $s=-(t+\bar t)/4\in E_0$. Its full field generates $\mathbb F_q$, and then $z=(t-\bar t)/(4s)\in E_0$. Thus $E_0=E$.

The image on $W$ of $L=\langle A,C,U\rangle$ contains $\operatorname{SL}_2(E)$. More precisely, put $D=\langle x(t),y(t)\rangle\le\operatorname{SL}_2(E)$, where $x(t)=U|_W$ and $y(t)=U^A|_W$. The full image of $L$ also contains determinant-minus-one matrices; the following argument concerns $D$. Here is the retained rank-one classification input and all exclusions. The upper and lower unipotents $x(t),y(t)$ have different fixed lines, excluding a Borel. Their order $p$ excludes cyclic groups and torus normalizers. For $j=\pm1$, the projective trace invariants of $x(jt)y(t)$ are $(2+jt^2)^2$; their difference is $8t^2$. Thus the projective trace field is $E$, excluding all proper subfield groups, including conjugate PGL groups. The exceptional $A_4,S_4,A_5$ are excluded by their orders when $p\ge7$. When $p=5$, the trace invariants of the only possible $A_5$ lie in $\mathbb F_5$, whereas $E$ properly contains it. When $p=3$, $q\ge9$ and $[E:\mathbb F_3]\ge4$, whereas all exceptional trace invariants lie in $\mathbb F_9$. Dickson's subgroup list now gives projective image $\operatorname{PSL}_2(E)$. Since $\operatorname{SL}_2(E)$ is perfect, a subgroup surjecting onto its projective quotient is the whole group: if $DZ=\operatorname{SL}_2(E)$ with $Z$ central, then $[DZ,DZ]=[D,D]\le D$.

This uses the standard conjugate-subfield interpretation of the projective trace invariant; it does not rely on an unproved recognition of a finite computed subgroup.

## 3. A trivial parabolic kernel is impossible

The pointwise stabilizer of $W$ inside its stabilizer in $\operatorname{SU}_4(q)$ is the abelian radical $R$. In a hyperbolic basis extending $n,m$, it consists of
\[
 \begin{pmatrix}I&X\\0&I\end{pmatrix},\qquad X+\bar X^t=0.
\]
Suppose $L\cap R=1$. The subgroup of $L$ whose restriction to $W$ belongs to $\operatorname{SL}_2(E)$ is then isomorphic to $\operatorname{SL}_2(E)$; call it $L_0$. It contains $U$.

The diagonal torus $T\cong E^*$ has order prime to $p$, so choose a $T$-stable complement to $W$ in $V$. The four torus weights are $1,-1,-q,q$ modulo $q^2-1$, respectively on $W$ and its unitary dual quotient. The two weight pairs are disjoint. The complement is automatically totally isotropic: none of its Hermitian weight products has exponent zero modulo $q^2-1$. Choose its dual basis so the Hermitian matrix is $\left(\begin{smallmatrix}0&I\\I&0\end{smallmatrix}\right)$.

For the lifted upper root element $x(u)\in L_0$, write
\[
 x(u)=\begin{pmatrix}P(u)&D(u)\\0&Q(u)\end{pmatrix},\quad
 P(u)=\begin{pmatrix}1&u\\0&1\end{pmatrix},\quad
 Q(u)=\begin{pmatrix}1&0\\-u^q&1\end{pmatrix}.
\]
Write $D(u)=(d_{ij}(u))$. The identity $x(u+w)=x(u)x(w)$ shows first that $d_{22}$ is additive. If it vanishes, $d_{12}$ and $d_{21}$ are additive. If those vanish, $d_{11}$ is additive. Explicitly, the four equations are
\[
\begin{aligned}
 d_{22}(u+w)&=d_{22}(u)+d_{22}(w),\\
 d_{12}(u+w)&=d_{12}(u)+d_{12}(w)+u d_{22}(w),\\
 d_{21}(u+w)&=d_{21}(u)+d_{21}(w)-w^q d_{22}(u),\\
 d_{11}(u+w)&=d_{11}(u)+d_{11}(w)+u d_{21}(w)-w^q d_{12}(u).
\end{aligned}
\]
Torus conjugation supplies weights, respectively,
\[
 d_{11}:q+1,\quad d_{12}:1-q,\quad
 d_{21}:q-1,\quad d_{22}:-q-1,
\]
under the scaling $u\mapsto a^2u$.

Every additive function $E\to E$ is a linearized polynomial $\sum_{j=0}^{2e-1}b_j u^{p^j}$. Such a nonzero function of torus weight $w$ requires
\[
 2p^j\equiv w\pmod{q^2-1}.
\]
None of the four weights above has this form when $q\ge5$. Their positive residues are $q-1,q+1,q^2-q-2,q^2-q$. If $j<e$, then $2p^j\le2q/p<q-1$. If $j\ge e$, then
\[
 q+1<2q\le2p^j\le2q^2/p<q^2-q-2.
\]
For $p\ge5$ the final inequality follows already at $q=5$ and increases thereafter; for $p=3$ one has $q\ge9$, where the same inequality holds. All values are less than $q^2-1$, so reduction introduces no other residue. Successively, all four entries of $D$ vanish.

The Weyl element normalizes $T$ and inverts its characters. Consequently it also preserves the chosen complement: it exchanges the weights $1,-1$ within $W$ and $q,-q$ within the complement. The torus, upper root group and Weyl element generate $\operatorname{SL}_2(E)$, so this entire representation is the direct sum of its two natural two-dimensional modules. In particular $U$ would have Jordan blocks of size at most two. This contradicts its calculated type $(3,1)$. Therefore $L\cap R\ne1$.

## 4. The nonzero kernel is the full radical

The additive module $R$ is irreducible over $\mathbb F_p$ under the conjugation action of $\operatorname{SL}_2(E)$. Multiplication by a fixed nonzero trace-zero scalar identifies skew-Hermitian matrices with Hermitian matrices, with the action $X\mapsto gX\bar g^t$ (or its contragredient, which is equivalent).

For completeness, let $M$ be a nonzero additive invariant subgroup of the Hermitian matrices. Take
\[
 X=\begin{pmatrix}a&b\\\bar b&d\end{pmatrix}\in M\setminus\{0\}.
\]
If both diagonal entries vanish, upper-root conjugation produces a nonzero diagonal entry for some parameter, because the trace pairing $u\mapsto u\bar b+\bar u b$ is nonzero. Interchanging the coordinates if necessary gives an element with $d\ne0$.

For $g(u)=\left(\begin{smallmatrix}1&u\\0&1\end{smallmatrix}\right)$, the difference
\[
 g(u)X\bar g(u)^t+g(-u)X\bar g(-u)^t-2X
 =\begin{pmatrix}2u\bar u\,d&0\\0&0\end{pmatrix}
\]
belongs to $M$. Surjectivity of the norm $E^*\to\mathbb F_q^*$ gives every matrix $\operatorname{diag}(a,0)$, $a\in\mathbb F_q$. Lower-root conjugation and subtracting its positive/negative parameter versions then give all off-diagonal Hermitian matrices, while its sum gives every lower diagonal entry. Hence $M$ is the full four-dimensional $\mathbb F_q$ space. This proves the claim using only additive subgroup operations; no assumed $\mathbb F_q$-linearity is needed.

The group $L\cap R$ is invariant under the full projected $\operatorname{SL}_2(E)$, since $R$ is abelian and its action depends only on the restriction to $W$. Thus $R\le L$. Multiplying lifts by elements of $R$ now removes their off-diagonal blocks. In particular $L$ contains the standard Levi copy $\{\operatorname{diag}(g,\bar g^{-t}):g\in\operatorname{SL}_2(E)\}$.

## 5. Extracting the missing root groups

The reflection $B$ fixes $n$, since $h(v,n)=0$, and moves $m$ out of $W$. More precisely
\[
 h(m,Bm)=4s^2(1+s)\ne0.
\]
Thus $W\cap BW=En$, and $BW=\langle n,Bm\rangle$ is adjacent to $W$.

Choose a hyperbolic basis $e_1=n,e_2=m,f_1,f_2$ with $h(e_i,f_j)=\delta_{ij}$. Rescale $Bm$ to $w$ so that $h(e_2,w)=1$. Since $w$ is orthogonal to $e_1$ and isotropic, it has the form
\[
 w=x e_1+y e_2+f_2,\qquad y+\bar y=0.
\]
An element of $R$ fixes $W$ pointwise and removes $x,y$: its skew-Hermitian parameter matrix may have arbitrary $(1,2)$ entry and arbitrary trace-zero $(2,2)$ entry. Hence $\langle A,B,C\rangle$ contains the entire unitary transvection root group with center $Ef_2$, by conjugating the corresponding center-$Ew$ root group from $R^B$. It already contains the root group with center $Ee_2$ from $R$.

These opposite root groups generate the rank-one $\operatorname{SU}_2(q)\cong\operatorname{SL}_2(q)$ acting on $\langle e_2,f_2\rangle$ and fixing its orthogonal complement. In particular they supply its Weyl element interchanging $Ee_2$ and $Ef_2$. Conjugation by the Levi element interchanging the two coordinate pairs supplies the corresponding Weyl element for $e_1,f_1$. Their product exchanges $W$ and $\langle f_1,f_2\rangle$, so the group contains both opposite parabolic radicals.

Equivalently, these operations give all the elementary unitary root groups: the original radical provides the mixed roots, its opposite gives their negatives, the Levi provides the two extension-field roots, and the rank-one groups provide the diagonal torus elements with determinant in $\mathbb F_q^*$. Standard unitary Gaussian elimination now gives $\operatorname{SU}_4(q)$. One may formulate the last retained elementary fact as: a split four-dimensional special unitary group is generated by its upper and lower elementary unitary root groups. No classification of maximal subgroups of $\operatorname{SU}_4(q)$ is used.

## 6. Projective quotient, adjacent orders, and limitations

The three matrices have determinants $1,-1,1$. The diagonal quotient of $\operatorname{PGU}_4(q)$ by its socle is $C_{\gcd(4,q+1)}$, and the class of $-1$ is the exponent $(q+1)/2$ modulo that order. This gives precisely the three groups in the statement.

The adjacent products have characteristic polynomials
\[
 \chi_{AB}(X)=(X-1)(X+1)(X^2-2sX+1),\qquad
 \chi_{BC}(X)=(X-1)^3(X+1).
\]
The second has a size-three unipotent block, giving projective order $2p$. The first has projective order greater than two because $A$ and $B$ do not commute projectively. Indeed, anticommutation of their lifts is impossible since the reflection $B$ has unequal eigenspace dimensions. Ordinary commutation would force $A$ to preserve the exceptional eigenline $Ev$, whereas both two-coordinate blocks of $v$ are nonzero. (The second coordinate is $-1$, and the fourth is $s+1\ne0$.) This argument also covers the possible repeated-root case $s=1$. The projective endpoints are distinct and commute because $AC=-CA$.

The field $q=3$ is deliberately excluded: the torus-weight argument admits coincidences there, and the trial triple generates a proper subgroup. The diagonal extension for $q\equiv7\pmod8$ is also outside the result because all three generators then belong to the simple socle. The phase-16 linear rank-three existence question remains open in this investigation.

Here is a self-contained same-marking intersection argument for any nontrivial finite group $G=\langle a,b,c\rangle$ with involutions, distinct commuting endpoints, adjacent product orders greater than two, and no nontrivial cyclic normal subgroup. Write $D_{ab}=\langle a,b\rangle$ and $D_{bc}=\langle b,c\rangle$. If $c\in D_{ab}$ or $a\in D_{bc}$, then $G$ itself is dihedral and has a nontrivial cyclic normal subgroup, a contradiction. If their intersection is larger than $\langle b\rangle$, choose an element $g$ outside $\{1,b\}$; multiplying by $b$ if needed makes $g$ a nonidentity rotation in $D_{ab}$. If it is also a rotation in $D_{bc}$, all three generators invert $g$, so $\langle g\rangle$ is a nontrivial cyclic normal subgroup. Otherwise $g$ is a reflection in $D_{bc}$. It then has order two and is the central rotation of $D_{ab}$. The element $h=gb$ is a nonidentity rotation in $D_{bc}$ and an involution, hence central in $D_{bc}$. Consequently
\[
 G=\langle a,h\rangle\langle g,c\rangle,
 \qquad [\langle a,h\rangle,\langle g,c\rangle]=1.
\]
Indeed, $g$ commutes with $a,b$, $h$ commutes with $b,c$, and $a,c$ commute. Each displayed factor is dihedral. Any nontrivial rotation subgroup of either is cyclic and normal in the whole product, again a contradiction. If both rotation subgroups are trivial, the whole group is abelian, which also supplies a nontrivial cyclic normal subgroup. Thus $D_{ab}\cap D_{bc}=\langle b\rangle$, and the rank-three intersection property follows. This argument resolves explicitly the mixed rotation/reflection alternative isolated in the 2025 Theorem B. It applies here because a cyclic normal subgroup of an almost-simple group intersects the nonabelian simple socle trivially and therefore centralizes it, whereas the socle centralizer is trivial.

## 7. Retained inputs, exact checks, and source scope

The rank-one subgroup input is the classical Dickson list in [Leemans--Moerenhout--O'Reilly-Regueiro, Proposition 2.3](https://arxiv.org/html/1606.08017). Simplicity of $\operatorname{PSL}_2(E)$, perfection of $\operatorname{SL}_2(E)$, and generation of a finite special unitary group by its elementary root groups are retained standard group facts; the proof above supplies the parameter-field, nonsplit-kernel and root-extraction arguments needed to apply them. The last root-generation fact is the usual unitary Gaussian elimination, also used in [the earlier unitary template, §4](phase11_unitary_template.md). No maximal-subgroup classification of $\operatorname{SU}_4(q)$ is assumed.

For the intersection step, the primary [2025 article, Theorem B and its proof](https://elib.sfu-kras.ru/bitstream/2311/156158/1/Baktybekov-Nuzhin.pdf) was read directly. Its Theorem A restates Conder--Oliveros (2013), Theorem 4.1. The original 2013 full article was not obtained during this check; [Conder's primary slides, pp. 21--22](https://www.fields.utoronto.ca/programs/scientific/13-14/discretegeom/Slides/Conder.pdf), also state that theorem. Section 6 explicitly handles the extra alternative isolated by the 2025 refinement.

The [symbolic checker](phase19_unitary_rank3_symbolic.py) verifies 29 exact identities. The [GAP checker](phase19_unitary_rank3_check.g) freshly passed six markings: $q=5,7,9,11,13$ with the default full-field parameter, and a second $q=7$ parameter with $s=1$. It constructs all eight marked subgroup closures and checks all 64 meets in each case, for 48 closures and 384 exact intersection checks overall. The natural action is on the $(q+1)(q^3+1)$ totally isotropic planes. Scalars act trivially; containment in the stated projective group and equality of its order with the computed permutation image give an order sandwich. Faithfulness is a consequence of these equalities, not an assumed recognition oracle. These finite checks corroborate the written universal proof and do not replace it. No new Lean formalization is claimed.

Run `python phase19_unitary_rank3_symbolic.py` with SymPy installed, and `gap -q phase19_unitary_rank3_check.g`. Use scratch copies to preserve the historical timestamped report. The separate [status audit](phase19_unitary_rank3_status.md) distinguishes already known simple-socle existence from the diagonal-extension subfamilies; publication priority has not been established.
