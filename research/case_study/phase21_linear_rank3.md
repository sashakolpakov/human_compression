# Phase 21: two independent parabolic factors give a linear rank-three marking

Date: 2026-10-10. **Proposed theorem under internal review.** Publication priority is unverified. Earlier snapshots remain unchanged.

Let $L_2(q)$ be the unique subgroup between $\operatorname{PSL}_4(q)$ and $\operatorname{PGL}_4(q)$ with index two over the socle. For odd $q$, this exists; it is the whole $\operatorname{PGL}_4(q)$ when $q\equiv3\pmod4$, and a proper index-two subgroup of that group when $q\equiv1\pmod4$.

**Theorem.** For every odd prime power $q\ge5$, the group $L_2(q)$ has a rank-three string C-group representation given by the explicit matrices below. In particular the construction covers the remaining linear diagonal family $q\equiv1\pmod4$.

The $q\equiv3\pmod4$ existence statement is already a consequence of the published Markovskaya–Nuzhin theorem recorded in [N011](phase20_linear_rank3_intake.md). It is not claimed as a newly resolved case. The source also covers $q=3$, which our new matrix argument does not require.

## 1. The three matrices

Put $F=\mathbb F_q$, choose a primitive element $\nu\in F^*$, and use column vectors. Write $E_{ij}$ for the elementary matrix and $x_{ij}(s)=I+sE_{ij}$. Set
\[
 A=\begin{pmatrix}0&I_2\\\nu I_2&0\end{pmatrix},\qquad
 C=\operatorname{diag}(I_2,-I_2),\qquad
 v=e_1+e_4,\quad \phi=(0,1,1,1),\quad B=I-2v\phi.
\]
Since $\phi(v)=1$, one has
\[
 A^2=\nu I,\quad B^2=C^2=I,\quad AC=-CA,\quad
 \det A=\nu^2,\quad\det B=-1,\quad\det C=1.
\]
Thus their projective images are involutions with distinct commuting endpoints. The endpoint $A$ has nonsquare square scalar, which supplies the missing diagonal determinant class.

Let $G=\langle A,B,C\rangle$. We prove $\operatorname{SL}_4(F)\le G$. It then follows from the determinant map modulo fourth powers that its projective image is precisely $L_2(q)$: the determinant exponents are $2$ and $(q-1)/2$ modulo $\gcd(4,q-1)$. They generate the unique order-two subgroup, for either odd congruence class.

Put $U=(BC)^2$ and $V=AUA^{-1}$. Both preserve $W=\langle e_1,e_3\rangle$. In the ordered basis $(e_1,e_3;e_2,e_4)$,
\[
 U=\begin{pmatrix}
 1&4&-8&4\\0&1&0&0\\0&0&1&0\\0&0&-4&1
 \end{pmatrix},\qquad
 U_W=x(4),\quad U_{F^4/W}=y(-4),
\]
where $x(s)=\left(\begin{smallmatrix}1&s\\0&1\end{smallmatrix}\right)$ and $y(s)=\left(\begin{smallmatrix}1&0\\s&1\end{smallmatrix}\right)$. Similarly,
\[
 V_W=y(4\nu),\qquad V_{F^4/W}=x(-4/\nu).
\]
In the original basis,
\[
 (U-I)^2=-16E_{12}\ne0,\qquad(U-I)^3=0.
\]
So $U$ has Jordan type $(3,1)$ in every odd characteristic.

## 2. Each rank-one projection is full

The two projected groups are
\[
 D_1=\langle x(4),y(4\nu)\rangle,\qquad
 D_2=\langle y(-4),x(-4/\nu)\rangle.
\]
Both are $\operatorname{SL}_2(F)$. Here is the complete rank-one check, retaining the Dickson subgroup list.

The opposite nontrivial unipotents have distinct fixed lines, excluding a Borel. A torus normalizer has order prime to $p$, excluding it as well. For $j=\pm1$, the trace-square invariants of the two corresponding words are
\[
 (2+16j\nu)^2\quad\hbox{and}\quad(2+16j/\nu)^2.
\]
Their differences within each pair are $128\nu$ and $128/\nu$. Since the characteristic is odd and a primitive element generates $F$ over its prime field, these invariants generate $F$. This excludes every proper conjugate subfield subgroup, including PGL subfield subgroups.

For $p\ge7$, the unipotent order excludes $A_4,S_4,A_5$. For $p=5$, only $A_5$ remains; its trace-square invariants lie in $\mathbb F_5$. Thus it is excluded for $q>5$, while for $q=5$ it is the whole target $\operatorname{PSL}_2(5)$. In characteristic three, the exceptional trace-square invariants lie in $\mathbb F_9$, so they cannot have full field $F$ unless $q=9$ (the case $q=3$ is outside the theorem).

For $q=9$, every primitive $w\in F^*$ has minimal equation $w^2=sw+1$ with $s\in\{1,-1\}$: its norm is $-1$, and trace zero would give order at most four. In characteristic three, one of $(2+w)^2,(2-w)^2$ is $2$. A determinant-one element with trace square $2$ has projective order four, excluding $A_5$; the full trace field excludes $S_4$ and $A_4$, whose trace-square invariants lie in $\mathbb F_3$. This applies to both $w=\nu$ and $w=\nu^{-1}$, since $16=1$ in this field.

Thus each projected group maps onto $\operatorname{PSL}_2(q)$. Perfection lifts the conclusion: if $DZ=\operatorname{SL}_2(q)$, where $Z$ is its center, then $\operatorname{SL}_2(q)=[DZ,DZ]=[D,D]\le D$.

## 3. The two factors are independent

Let $P$ be the diagonal-block image of $\langle U,V\rangle$. It is a subdirect subgroup of $\operatorname{SL}_2(q)\times\operatorname{SL}_2(q)$. On quotienting both centers, a subdirect product of two copies of the nonabelian simple $S=\operatorname{PSL}_2(q)$ is either $S\times S$ or the graph of an automorphism. This elementary Goursat consequence follows by taking the kernels of its two coordinate projections: each image of a kernel is normal in $S$, so is either trivial or all of $S$.

Every automorphism of $S$ is induced by a projective linear conjugation and a field automorphism, including $q=9$. Hence it sends the projective trace-square invariant $\tau$ to $\tau^{p^k}$ for some fixed $0\le k<e$, where $q=p^e$. If the graph alternative held, applying it to $U^jV$, for $j=1,-1$, and subtracting the two trace-square equations would give
\[
 (128\nu)^{p^k}=128/\nu,\qquad\nu^{p^k+1}=1.
\]
This is impossible: $\nu$ has order $q-1$, and $p^k+1<q-1$ for every such $k$ when $q\ge5$. For $e=1$ this is $2<q-1$; for $e>1$ it follows from $p^{e-1}+1\le q/3+1<q-1$.

The projective image is therefore the full product. If $Z$ is the center of $\operatorname{SL}_2(q)^2$, then $PZ=\operatorname{SL}_2(q)^2$. Perfection again gives
\[
 P\ \supseteq\ [PZ,PZ]=\operatorname{SL}_2(q)^2.
\]
Thus the full, independently acting product occurs as the diagonal-block image.

## 4. A Jordan block forces the entire radical

Let $R$ be the additive block group
\[
 R=\left\{\begin{pmatrix}I&X\\0&I\end{pmatrix}:X\in M_2(F)\right\}
\]
in the basis $(e_1,e_3;e_2,e_4)$, and put $K=\langle U,V\rangle\cap R$.

First $K\ne1$. Otherwise the block map on $\langle U,V\rangle$ would be an isomorphism onto $\operatorname{SL}_2(q)^2$. The central element $(-I,I)$ would have a lift
\[
 Z_0=\begin{pmatrix}-I&X\\0&I\end{pmatrix},
\]
which is an involution and centralizes $U$. Its two eigenspaces have dimension two. Since $U$ preserves both, its Jordan blocks have size at most two, contradicting $(U-I)^2\ne0$.

The additive group $M_2(F)$ is irreducible under the independent left and right $\operatorname{SL}_2(F)$ actions, even when invariant subgroups are only assumed $\mathbb F_p$-linear. Indeed, from a nonzero matrix $X$ with entry $x_{ij}\ne0$, choose $k\ne i$ and $l\ne j$. The successive left and right root differences give
\[
 (I+uE_{ki})X(I+wE_{jl})-(I+uE_{ki})X-X(I+wE_{jl})+X
 =uwx_{ij}E_{kl}.
\]
Varying $u,w\in F$ gives every scalar multiple of this matrix unit. The two rank-one Weyl elements then give every matrix unit, hence all of $M_2(F)$. No $F$-linearity was assumed at the start.

The action on $K$ factors through the full diagonal product because $R$ is abelian. Therefore $K=R$. Removing off-diagonal blocks from lifts now shows that $G$ contains both $R$ and the standard Levi product $\operatorname{SL}(W)\times\operatorname{SL}(F^4/W)$.

## 5. One explicit root extraction completes generation

In original coordinates the available radical roots are $x_{12},x_{14},x_{32},x_{34}$, and the Levi gives $x_{13},x_{31},x_{24},x_{42}$, with every parameter in $F$. Put
\[
 T=I-E_{14}+\tfrac12E_{34}\in R.
\]
Direct multiplication gives, for every $s\in F$,
\[
 Q(s):=TBx_{31}(s)BT^{-1}
 =I-2s(E_{41}-2E_{42}-2E_{43}).
\]
Conjugating by $x_{13}(u)$ and subtracting the original transvection multiplicatively yields
\[
 x_{13}(u)Q(s)x_{13}(-u)Q(s)^{-1}=x_{43}(2su).
\]
Hence the full $x_{43}$ root group is present. The elementary commutators
\[
 [x_{43}(a),x_{31}(b)]=x_{41}(ab),\quad
 [x_{24}(a),x_{41}(b)]=x_{21}(ab),\quad
 [x_{21}(a),x_{13}(b)]=x_{23}(ab)
\]
give all remaining roots. Here $[g,h]=ghg^{-1}h^{-1}$. The twelve elementary root groups generate $\operatorname{SL}_4(F)$ by Gaussian elimination. This proves the generation claim and the determinant-class identification in §1.

## 6. The marking has the intersection property

The projective images $a,b,c$ are distinct nonidentity involutions and $ac$ has order two. The characteristic polynomial of $BC$ is $(X-1)^3(X+1)$, and the displayed Jordan-three calculation shows $|bc|=2p$. The pair $a,b$ does not commute projectively: ordinary commutation would preserve the exceptional eigenline $Fv$ of $B$, whereas $Av=(0,1,\nu,0)^t$ is not proportional to $v$. Anticommutation is impossible because the two eigenspaces of $B$ have unequal dimensions. Thus $|ab|>2$.

The generated almost-simple group has no nontrivial cyclic normal subgroup: such a subgroup would intersect the nonabelian simple socle trivially and then centralize it, contradicting its trivial centralizer in the almost-simple group. The elementary same-marking rank-three argument in [phase20, §6](phase20_unitary_rank3.md) consequently gives
\[
 \langle a,b\rangle\cap\langle b,c\rangle=\langle b\rangle.
\]
That argument handles both rotations and the mixed rotation/reflection alternative; it is not an inference from the existence-only wording of an intersection theorem. This is the rank-three string C-group criterion, completing the proof.

With the retained [rank upper bound](phase9_linear_unitary.md), [rank-four construction](phase16_linear_diagonal.md), and published rank-three existence for $q=3$, the exact rank set of $L_2(q)$ is therefore $\{3,4\}$ for all odd $q\ge3$, subject to the same internal-review status.

## 7. Retained inputs and verification boundary

The external group inputs are the Dickson list (for example [Leemans–Moerenhout–O'Reilly-Regueiro, Proposition 2.3](https://arxiv.org/abs/1606.08017)), simplicity and perfection in rank one, and $\operatorname{Aut}(\operatorname{PSL}_2(q))=\operatorname{P\Gamma L}_2(q)$. The latter is explicitly recalled in the appendix of [Guralnick–Zieve, *Polynomials with PSL(2) monodromy*](https://websites.umich.edu/~zieve/papers/gz.html). Goursat's special case, radical irreducibility, the nonzero-kernel argument and the elementary root extraction are proved above. No maximal-subgroup classification of $\operatorname{SL}_4(q)$ is used.

The [exact GAP checker](phase21_linear_rank3_check.g) tests $q=5,7,9,13,17,25$: both rank-one projected orders, the full projective group order, all eight marked subgroups and all 64 meets in every field. These are diagnostics for the universal proof, not its substitute. The target is identified by an order sandwich between the projective point-action image and its determinant-constrained ambient subgroup, without assuming faithfulness or using a group-recognition oracle. No new Lean or publication-priority claim is made.
