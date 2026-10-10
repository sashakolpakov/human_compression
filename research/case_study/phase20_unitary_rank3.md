# Phase 20: rank three for every odd unitary diagonal index-two extension

Date: 2026-10-10. **Proposed theorem under internal review, not externally peer reviewed.** Priority is unverified. All previous snapshots remain unchanged. The uniform argument below proves generation for every odd $q\ge5$; the field $q=3$ is covered by the separate exact finite certificate in §6.

## 1. Statement and the outer determinant mechanism

Write $U_2(q)$ for the unique subgroup of $\operatorname{PGU}_4(q)$ containing $\operatorname{PSU}_4(q)$ with index two over that socle. When $q\equiv1\pmod4$, this is the full projective general unitary group. When $q\equiv3\pmod4$, it is the index-two subgroup of that group.

**Proposed theorem.** For every odd prime power $q\ge3$, the group $U_2(q)$ has a rank-three string C-group representation.

For $q=p^e\ge5$, let $E=\mathbb F_{q^2}$, $\bar x=x^q$, and choose a primitive element $t\in E^*$. Choose $\eta\in E^*$ such that $\eta^2$ generates the norm-one group and $\eta\bar\eta=-1$; for example, if $\omega$ generates $E^*$, take $\eta=\omega^{(q-1)/2}$. Put
\[
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 H=\begin{pmatrix}J&0\\0&-J\end{pmatrix},\quad
 A=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix},\quad
 C=\begin{pmatrix}I_2&0\\0&-I_2\end{pmatrix},
\]
\[
 v=(1,0,2/t,\bar t/2)^t,\qquad B=I+v\bar v^tH.
\]
The proposed marking consists of the projective images of
\[
 a_0=\eta A,\qquad b_0=B,\qquad c_0=C.
\]
We use the column Hermitian form $h(x,y)=\bar x^tHy$.

Directly, $A^2=C^2=I$, $AC=-CA$, $\bar A^tHA=-H$, and $\bar C^tHC=H$. Also $h(v,v)=-2$, so $B$ is the unitary reflection with exceptional eigenline $Ev$, with $B^2=I$ and determinant $-1$. Multiplication by $\eta$ turns the anti-isometry $A$ into an isometry. Its square is the scalar $\eta^2I$, so it gives a projective involution. This scalar normalization is essential: ordinary unitary involutions alone have determinant $\pm1$, whose diagonal class is trivial when $q\equiv7\pmod8$.

The matrix group $G_0=\langle\eta A,B,C\rangle$ will be proved to contain $\operatorname{SU}_4(q)$. Its determinant image is $\langle\eta^4,-1\rangle$. If $\zeta=\eta^2$ generates the norm-one group, these determinant classes have exponents $2$ and $(q+1)/2$ modulo $d=\gcd(4,q+1)$. For $d=2$, the latter exponent is odd; for $d=4$, the first exponent is exactly two. Thus the projective image is precisely $U_2(q)$ in every odd congruence class.

## 2. A Jordan-three element and the full rank-one projection

Let $U=(BC)^2$, $n=v+Cv=2e_1$, and $m=An=2e_3$. The plane $W=\langle n,m\rangle$ is totally isotropic. On its displayed basis,
\[
 U|_W=\begin{pmatrix}1&t\\0&1\end{pmatrix},\quad
 A|_W=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 C|_W=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\]
Also
\[
 (U-I)^2=2n\bar n^tH\ne0,\qquad (U-I)^3=0.
\]
For a direct characteristic-independent calculation, set $w=Cv$, $\phi=\bar v^tH$, $\psi=\bar w^tH$. Then $h(v,w)=2$, $U-I=v\phi+w\psi+2v\psi$, $(U-I)v=2n$ and $(U-I)w=-2n$. Therefore $U$ has Jordan type $(3,1)$, including in characteristic three. Moreover
\[
 \chi_{BC}(X)=(X-1)^3(X+1),\qquad
 h(m,Bm)=t\bar t\ne0.
\]

The primitive choice implies $\mathbb F_p(t^2)=E$: $t^2$ has order $(q^2-1)/2$, whereas every proper subfield of $E$ has at most $q$ elements and its multiplicative group has order at most $q-1$.

Let $L=\langle\eta A,C,U\rangle\le\operatorname{U}(H)$. It preserves $W$, and its image contains
\[
 D=\langle x(t),y(t)\rangle\le\operatorname{SL}_2(E),\qquad
 x(t)=\begin{pmatrix}1&t\\0&1\end{pmatrix},\quad
 y(t)=\begin{pmatrix}1&0\\t&1\end{pmatrix}.
\]
The lower root comes from conjugating $U$ by $\eta A$; its scalar cancels in conjugation. The full image of $L$ is not assumed to have determinant one.

Here are all exclusions needed to apply the retained Dickson rank-one subgroup list. The two unipotents have different fixed lines, excluding a Borel; their order $p$ excludes cyclic groups and torus normalizers. For $j=\pm1$, the trace-square invariants of $x(jt)y(t)$ are $(2+jt^2)^2$, whose difference is $8t^2$. Thus the projective trace field is $E$, excluding all proper conjugate subfield groups, including PGL subfield groups. For $p\ge7$, the orders exclude the exceptional $A_4,S_4,A_5$. For $p=5$, the only possible exception is $A_5$, whose trace-square invariants lie in $\mathbb F_5$. For $p=3$, the hypothesis $q\ge5$ forces $q\ge9$, so $[E:\mathbb F_3]\ge4$, whereas all exceptional invariants lie in $\mathbb F_9$. These invariant assertions follow from the possible projective element orders $1,2,3,4,5$; the order-five values satisfy $X^2-3X+1=0$.

Consequently $D$ maps onto $\operatorname{PSL}_2(E)$. Since $\operatorname{SL}_2(E)$ is perfect, $D$ is the whole group: if $DZ=\operatorname{SL}_2(E)$ with $Z$ its center, then $[DZ,DZ]=[D,D]\le D$. Hence the projection of $L$ contains the full $\operatorname{SL}_2(E)$.

## 3. A trivial parabolic kernel is impossible

The pointwise stabilizer of $W$ inside the full unitary group $\operatorname{U}(H)$ is the abelian radical $R$; in particular, it already lies in $\operatorname{SU}_4(q)$. In a hyperbolic basis extending $n,m$, it consists of
\[
 \begin{pmatrix}I&X\\0&I\end{pmatrix},\qquad X+\bar X^t=0.
\]
Suppose $L\cap R=1$. The subgroup of $L$ whose restriction to $W$ belongs to $\operatorname{SL}_2(E)$ is then isomorphic to $\operatorname{SL}_2(E)$; call it $L_0$. It contains $U$. Although $L$ need not lie in $\operatorname{SU}_4(q)$, this subgroup does: a unitary lift with restriction $g$ to $W$ has full determinant $\det(g)/\overline{\det(g)}$, which is one when $g\in\operatorname{SL}_2(E)$.

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
 h(m,Bm)=t\bar t\ne0.
\]
Thus $W\cap BW=En$, and $BW=\langle n,Bm\rangle$ is adjacent to $W$.

Choose a hyperbolic basis $e_1=n,e_2=m,f_1,f_2$ with $h(e_i,f_j)=\delta_{ij}$. Rescale $Bm$ to $w$ so that $h(e_2,w)=1$. Since $w$ is orthogonal to $e_1$ and isotropic, it has the form
\[
 w=x e_1+y e_2+f_2,\qquad y+\bar y=0.
\]
An element of $R$ fixes $W$ pointwise and removes $x,y$: its skew-Hermitian parameter matrix may have arbitrary $(1,2)$ entry and arbitrary trace-zero $(2,2)$ entry. Hence $G_0$ contains the entire unitary transvection root group with center $Ef_2$, by conjugating the corresponding center-$Ew$ root group from $R^B$. It already contains the root group with center $Ee_2$ from $R$.

These opposite root groups generate the rank-one $\operatorname{SU}_2(q)\cong\operatorname{SL}_2(q)$ acting on $\langle e_2,f_2\rangle$ and fixing its orthogonal complement. In particular they supply its Weyl element interchanging $Ee_2$ and $Ef_2$. Conjugation by the Levi element interchanging the two coordinate pairs supplies the corresponding Weyl element for $e_1,f_1$. Their product exchanges $W$ and $\langle f_1,f_2\rangle$, so the group contains both opposite parabolic radicals.

Equivalently, these operations give all the elementary unitary root groups: the original radical provides the mixed roots, its opposite gives their negatives, the Levi provides the two extension-field roots, and the rank-one groups provide the diagonal torus elements with determinant in $\mathbb F_q^*$. Standard unitary Gaussian elimination now gives $\operatorname{SU}_4(q)$. One may formulate the last retained elementary fact as: a split four-dimensional special unitary group is generated by its upper and lower elementary unitary root groups. No classification of maximal subgroups of $\operatorname{SU}_4(q)$ is used.

## 6. Projective intersection and the finite field $q=3$

The projective generators are nonidentity involutions. The two endpoints are distinct and commute because $AC=-CA$. The product $BC$ has projective order $2p$: its unipotent block has size three, and its eigenvalue ratio $-1$ requires an even power to become scalar. The first adjacent product also has projective order greater than two. Anticommutation of normalized $A$ and $B$ is impossible because $B$ has eigenspace dimensions $3+1$. Ordinary commutation would preserve $Ev$, but the two blocks $(1,0)$ and $(2/t,\bar t/2)$ of $v$ are linearly independent, so $Av$ is not proportional to $v$.

For completeness, a finite group generated by such a string triple $a,b,c$ and having no nontrivial cyclic normal subgroup satisfies IP for this very marking. Put $D_1=\langle a,b\rangle$, $D_2=\langle b,c\rangle$. Redundancy of either endpoint makes the whole group dihedral, which is excluded. If $g\in D_1\cap D_2$ lies outside $\{1,b\}$, multiply it by $b$ if necessary so it is a nonidentity rotation in $D_1$. If it is a rotation in $D_2$ too, all three generators invert it, giving a nontrivial cyclic normal subgroup. Otherwise it is a reflection in $D_2$, hence the central involution of $D_1$. Now $h=gb$ is a nonidentity central involution of $D_2$, and
\[
 G=\langle a,h\rangle\langle g,c\rangle,
 \qquad [\langle a,h\rangle,\langle g,c\rangle]=1.
\]
A nontrivial rotation subgroup of either dihedral factor is cyclic and normal in the whole product. If both rotation subgroups are trivial, the nontrivial group is abelian and again has a cyclic normal subgroup. Thus $D_1\cap D_2=\langle b\rangle$, which gives rank-three IP. This is the elementary adapter to the Conder--Oliveros intersection principle and its precise 2025 refinement. It applies to $U_2(q)$ because a cyclic normal subgroup would centralize its nonabelian simple socle, whose centralizer is trivial.

The uniform projection/kernel proof above deliberately excludes $q=3$. Here use the exact field
\[
 E=\mathbb F_3[T]/(T^2-T-1),\qquad t=T,
 \quad t^4=-1,\quad t^8=1,\quad\bar t=1-t.
\]
Take $\eta=t$ and the same $A,C,H$. The reflection is explicitly
\[
 B=\begin{pmatrix}
 1&1&t&-t\\
 0&1&0&0\\
 0&1-t&0&1\\
 0&t-1&1&0
 \end{pmatrix}.
\]
The exact checker verifies these polynomial coordinates, their unitary relations and the action on all 112 totally isotropic planes. Its projective permutation image has order $6\,531\,840=|U_2(3)|$ and type $\{8,6\}$. Unitary containment and the determinant classes give
\[
 6\,531\,840=|\text{permutation image}|
 \le |\text{generated projective subgroup}|
 \le |U_2(3)|=6\,531\,840.
\]
Scalars act trivially on planes; this order sandwich proves equality without assuming faithfulness or invoking a group-recognition oracle. The checker also constructs all eight marked subgroups and checks all 64 meets directly. Thus this exceptional finite field is a certified base, not an inference from the $q\ge5$ projection argument.

## 7. Consequence, retained inputs, and verification boundary

Combined with the previously reviewed [uniform upper bound](phase9_linear_unitary.md) and the rank-four constructions in [the diagonal](phase17_unitary_diagonal.md) and [twisted](phase17_unitary_twisted.md) notes, the theorem gives the exact rank set $\{3,4\}$ for $U_2(q)$ for every odd $q\ge3$. Ranks one and two cannot occur for these almost-simple groups, which are neither order-two cyclic nor dihedral. This statement concerns the diagonal extension; it does not change the published nonexistence of string C-group representations for the simple socle $\operatorname{PSU}_4(3)$, nor the cyclic-index-four obstruction for $\operatorname{PGU}_4(q)$ when $q\equiv3\pmod4$.

Retained external inputs are the Dickson list [Leemans--Moerenhout--O'Reilly-Regueiro, Proposition 2.3](https://arxiv.org/html/1606.08017), rank-one simplicity/perfection, and generation by elementary unitary root groups via Gaussian elimination. The Hermitian-module and nonsplit-kernel arguments are supplied in full above. No maximal-subgroup classification of $\operatorname{SU}_4(q)$ is used. The elementary IP argument explicitly addresses the mixed alternative in [Baktybekov--Conder--Nuzhin--Rezantseva (2025), Theorem B and §2](https://elib.sfu-kras.ru/bitstream/2311/156158/1/Baktybekov-Nuzhin.pdf); it does not reinterpret the existence-only wording of their Theorem A as a same-marking statement.

The [symbolic checker](phase20_unitary_rank3_symbolic.py) verifies 31 exact identities, including the $q=3$ polynomial coordinates. The [finite checker](phase20_unitary_rank3_check.g) checks $q=3,5,7,9,11,13$, with all eight marked subgroup closures and all 64 meets in every field. Apart from the explicit $q=3$ base, these are corroborating diagnostics, not the justification of the universal proof. Python requires SymPy; the group checks use GAP. Run timestamp-writing scripts from scratch copies to preserve historical reports. No new Lean formalization or publication-priority claim is made.
