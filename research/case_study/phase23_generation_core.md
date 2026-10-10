# Phase 23: forcing an additive parabolic kernel by a Jordan block

Date: 2026-10-10. Proposed synthesis for internal review. This note replaces two repeated generation steps by one precise module argument, and extends the independent-factor step to arbitrary block sizes and fields. It does not assert a new cohomology classification, a new polytope existence theorem, or a reduction of entire papers. Earlier proof snapshots are unchanged.

## 1. The kernel-or-complement principle

Let $R$ be an abelian group acted on by a group $L$. Write $R\rtimes L$ additively in the first coordinate, so
\[
 (v,g)(w,h)=(v+gw,gh).
\]
A cocycle is a function $c:L\to R$ satisfying $c(gh)=c(g)+gc(h)$. A coboundary has the form $c(g)=(g-1)v$. The assertion $H^1(L,R)=0$ means that every cocycle is a coboundary.

**Theorem A.** Suppose that $R$ has no nonzero proper $L$-invariant additive subgroup and that $H^1(L,R)=0$. If $D\le R\rtimes L$ projects onto $L$, then either $D=R\rtimes L$ or $D$ is conjugate by an element of $R$ to the standard complement $L$.

**Proof.** The subgroup $K=D\cap R$ is invariant under the projected $L$: conjugation on $R$ depends only on the second coordinate. Thus $K=R$ or $0$. In the first case, removing the first coordinate of each lift gives the whole semidirect product. In the second, each $g\in L$ has a unique lift $(c(g),g)$ in $D$. Closure gives the cocycle identity. A coboundary graph is conjugate to the standard complement. No finiteness or semisimplicity is used. $\square$

Suppose now that this semidirect product is represented by block matrices
\[
 \begin{pmatrix}g&Xh\\0&h\end{pmatrix}
 \quad\text{on }F^a\oplus F^b,
\]
where $X$ belongs to an additive invariant subspace or subgroup of $\operatorname{Hom}_F(F^b,F^a)$ and $(g,h)$ is the corresponding image of $L$. A block-diagonal unipotent has all Jordan blocks of size at most $\max(a,b)$. Conjugation preserves this property. Therefore, under Theorem A's hypotheses, a subgroup projecting onto $L$ and containing a unipotent with a larger Jordan block is the whole semidirect product. Jordan block size here can equivalently be expressed as the nilpotency index of $u-I$, so no algebraic closure assumption is needed.

## 2. Independent factors: an elementary product cohomology lemma

**Lemma B.** Let $G,H$ be arbitrary groups, $F$ any field, and $V,W$ finite-dimensional $FG$- and $FH$-modules. Let $G\times H$ act on $M=V\otimes_F W$ by its two factors. If $V^G=0$ and $W^H=0$, then
\[
 H^1(G\times H,M)=0.
\]

**Proof.** For a cocycle $c$, abbreviate $c(g,1)$ by $c_G(g)$ and $c(1,h)$ by $c_H(h)$. Computing $c((g,1)(1,h))$ in the two orders gives the elementary identity
\[
 (h-1)c_G(g)=(g-1)c_H(h).                 \tag{2.1}
\]
Thus the class of $c_G$ in $H^1(G,M)$ is fixed by $H$: its change under $h$ is the coboundary associated with $c_H(h)$.

Because $W$ is finite dimensional and $G$ acts trivially on it, choosing a basis of $W$ identifies the inhomogeneous cochain complexes in every degree as
\[
 C^\bullet(G,V\otimes_F W)=C^\bullet(G,V)\otimes_F W.
\]
This remains valid for infinite $G$; finite dimensionality allows arbitrary functions into the tensor product to be written using one fixed finite basis. Tensoring over a field is exact, so
\[
 H^1(G,M)=H^1(G,V)\otimes_F W.
\]
The action of $H$ is solely on the second factor. Its fixed space is $H^1(G,V)\otimes W^H=0$. This fixed-space equality is valid even if $H^1(G,V)$ is infinite dimensional: each tensor involves only finitely many linearly independent first coordinates. Hence $c_G(g)=(g-1)v$ for some $v\in M$.

Subtract this coboundary from $c$ on the entire product. The resulting $c_G$ is zero. Equation (2.1) now puts every $c_H(h)$ in $M^G=V^G\otimes W=0$. Since the two factors generate their direct product, the normalized cocycle is zero. $\square$

For comparison, a shorter sufficient criterion is available whenever $z\in Z(L)$ acts on $R$ with $z-1$ invertible. The same commuting calculation yields
\[
 (z-1)c(g)=(g-1)c(z),
\]
so $c(g)=(g-1)(z-1)^{-1}c(z)$. This familiar central-element argument explains the earlier odd-characteristic use of $(-I,I)$. Lemma B removes the need for such an element, including in characteristic two.

## 3. An all-field block-generation theorem

For any field $F$ and integers $a,b\ge2$, let
\[
 P_{a,b}(F)=\left\{\begin{pmatrix}g&D\\0&h\end{pmatrix}:
 g\in\operatorname{SL}_a(F),\ h\in\operatorname{SL}_b(F),\ D\in M_{a\times b}(F)\right\}.
\]
Its additive radical is $R=M_{a\times b}(F)$, acted on by $(g,h):X\mapsto gXh^{-1}$.

**Theorem C.** If $D\le P_{a,b}(F)$ has full diagonal-block image $\operatorname{SL}_a(F)\times\operatorname{SL}_b(F)$ and contains a unipotent $u$ with
\[
 (u-I)^{\max(a,b)}\ne0,
\]
then $D=P_{a,b}(F)$. This holds for finite or infinite fields, in every characteristic.

**Proof.** The natural modules of $\operatorname{SL}_a(F)$ and the dual natural module of $\operatorname{SL}_b(F)$ have no fixed vectors. Indeed, the elementary transvections with parameter one already force every coordinate of a fixed vector to vanish. Lemma B therefore gives $H^1(L,R)=0$.

The required additive irreducibility is also elementary. If $M\le R$ is a nonzero invariant additive subgroup, choose $X\in M$ with $x_{ij}\ne0$, $k\ne i$, and $\ell\ne j$. Independent left and right root operations give
\[
 (I+sE_{ki})X(I+tE_{j\ell})-(I+sE_{ki})X
 -X(I+tE_{j\ell})+X=stx_{ij}E_{k\ell}\in M.
                                                        \tag{3.1}
\]
Varying $s,t$ gives every $F$-multiple of $E_{k\ell}$. Signed coordinate permutations in the two special linear groups move this to every matrix unit; in characteristic two the signs disappear. Adding these units gives all of $R$. This uses only additive closure, not any assumed $F$-linearity of $M$. Apply Theorem A and the Jordan-block observation. $\square$

The full diagonal-block image is an essential hypothesis. It is established by the separate trace-field and Goursat argument in the linear application; Theorem C does not prove that step. A diagonal copy of $\operatorname{SL}_2$ can have nonsplit four-dimensional representations, as §5 explicitly demonstrates.

## 4. Frobenius-coupled factors and an exact nonresonance test

Let $E=\mathbb F_{p^m}$ with $p$ odd, $m\ge2$, and $1\le f<m$. Write $r=p^f$, $\sigma:x\mapsto x^r$, and let $L=\operatorname{SL}_2(E)$ act on $M=M_2(E)$ by
\[
 g\cdot X=gX(g^\sigma)^t.
\]

**Theorem D.** One has $H^1(L,M)=0$ if
\[
 2p^j\not\equiv 1+r,\ 1-r,\ r-1,\ -r-1
       \pmod{p^m-1}\qquad(0\le j<m).                  \tag{4.1}
\]
Condition (4.1) holds exactly when either $p\ge5$, or $p=3$ and $2\le f\le m-2$.

**Proof of vanishing.** A cocycle $c$ gives a block representation
\[
 \pi(g)=\begin{pmatrix}g&c(g)(g^\sigma)^{-t}\\0&(g^\sigma)^{-t}\end{pmatrix}.
\]
The upper-left plane is invariant. The diagonal torus $T$ has order $p^m-1$, prime to the characteristic, so averaging any projection onto that plane gives a $T$-invariant complement. Choose its basis compatibly with the quotient; this changes the cocycle by a coboundary and makes every torus matrix block diagonal. Its four weights are $1,-1,-r,r$ modulo $p^m-1$. The first and second pairs are disjoint, since $1<r<p^m-1$ and $r\not\equiv-1$.

For an upper root $x(u)$, the two diagonal blocks are
\[
 P(u)=\begin{pmatrix}1&u\\0&1\end{pmatrix},\qquad
 Q(u)=\begin{pmatrix}1&0\\-u^r&1\end{pmatrix}.
\]
Write its off-diagonal block as $D(u)=(d_{ij}(u))$. Multiplication of $\pi(x(u))\pi(x(w))=\pi(x(u+w))$ gives
\[
\begin{aligned}
 d_{22}(u+w)&=d_{22}(u)+d_{22}(w),\\
 d_{12}(u+w)&=d_{12}(u)+d_{12}(w)+u d_{22}(w),\\
 d_{21}(u+w)&=d_{21}(u)+d_{21}(w)-w^r d_{22}(u),\\
 d_{11}(u+w)&=d_{11}(u)+d_{11}(w)+u d_{21}(w)-w^r d_{12}(u).
\end{aligned}                                                    \tag{4.2}
\]
Torus conjugation scales $u$ by $a^2$ and assigns the respective weights
\[
 d_{11}:1+r,\quad d_{12}:1-r,\quad
 d_{21}:r-1,\quad d_{22}:-r-1.                        \tag{4.3}
\]
Every additive function $E\to E$ is uniquely a linearized polynomial $\sum_{j=0}^{m-1}b_j u^{p^j}$. Such a function of weight $w_0$ can be nonzero only if some $2p^j\equiv w_0\pmod{p^m-1}$: compare coefficients after substituting $a^2u$, for all $a\in E^*$. Condition (4.1) first kills $d_{22}$, then $d_{12},d_{21}$, and finally $d_{11}$ by (4.2).

The Weyl element inverts the torus characters, so it preserves the two separate weight pairs and hence the chosen complement. The torus, upper root group and Weyl element generate $\operatorname{SL}_2(E)$. Thus the complement is invariant under the full group and the original cocycle is a coboundary.

**Proof of the parameter assertion.** Put $Q=p^m$. The four positive weight residues are
\[
 r-1,\quad r+1,\quad Q-r-2,\quad Q-r.
\]
For $p\ge5$ and $j<f$,
\[
 2p^j\le2r/p<r-1.
\]
For $j\ge f$,
\[
 r+1<2r\le2p^j\le2Q/p<Q-r-2.
\]
The last strict inequality follows from $r\le Q/p$, $Q\ge p^2$, and $(1-3/p)Q>2$. These quantities lie below $Q-1$, so no further modular reduction is involved. For $p=3$ and $2\le f\le m-2$, the same inequalities follow from $r\ge9$ and $r\le Q/9$: specifically $2Q/3<Q-r-2$ because $2Q/9>2$. Conversely, for $p=3,f=1$ the residue $r-1=2$ equals $2p^0$, while for $p=3,f=m-1$ the residue $Q-r=2r$ equals $2p^{m-1}$. $\square$

## 5. The characteristic-three exceptions are real

The exceptional congruences do not merely expose a weakness in that proof. For $p=3$ and $f\in\{1,m-1\}$ one actually has
\[
 H^1(\operatorname{SL}_2(3^m),M_2(\mathbb F_{3^m}))\ne0
\]
for the action in §4. No assertion about its dimension is needed here.

Let $U$ be the natural two-dimensional module over $E=\mathbb F_{3^m}$. In the cubic symmetric power, the cube subspace is a submodule and there is an exact sequence
\[
 0\longrightarrow U^{(3)}\longrightarrow\operatorname{Sym}^3 U
     \longrightarrow U\longrightarrow0.             \tag{5.1}
\]
On the basis $e_1^3,e_1^2e_2,e_1e_2^2,e_2^3$, the upper root $x(1)$ has matrix, with entries read in characteristic three,
\[
 S=\begin{pmatrix}1&1&1&1\\0&1&-1&0\\0&0&1&0\\0&0&0&1\end{pmatrix}.
\]
Its nilpotent part has rank two, nonzero square, and zero cube, so its Jordan type is $(3,1)$. Both two-dimensional factors in (5.1) have unipotent blocks of size at most two, so the extension is nonsplit. The quotient identification in (5.1) can be checked on the elementary roots and torus: in the quotient basis $e_1^2e_2,e_1e_2^2$, root parameters acquire a minus sign, removed by conjugation with $\operatorname{diag}(1,-1)$.

Dualizing (5.1), and using the invariant alternating form to identify each natural module with its dual, yields a nonsplit extension of $U^{(3)}$ by $U$. Its off-diagonal cocycle has coefficients in $\operatorname{Hom}(U^{(3)},U)\cong U\otimes U^{(3)}$, precisely the module in §4 with $f=1$. Twisting (5.1) instead by $3^{m-1}$ yields a nonsplit extension of $U^{(3^{m-1})}$ by $U$, since $3^m$ acts trivially on $E$. This gives $f=m-1$. The action of $x(1)$ is unchanged by these field twists; dualizing preserves its Jordan block sizes.

These graphs project onto the coupled diagonal copy, have zero additive kernel, and still contain a Jordan-three element. Thus a general rule that “a large Jordan block always forces the radical” is false without the complement-splitting hypothesis. This is an explicit limitation of the proposed core theory.

## 6. The unitary parabolic as a direct application

Let $q=p^e$ be odd and at least five, $E=\mathbb F_{q^2}$, and $\bar x=x^q$. Let
\[
 R_- =\{X\in M_2(E):X+\bar X^t=0\},\qquad
 P_U(q)=\left\{\begin{pmatrix}g&X\bar g^{-t}\\0&\bar g^{-t}\end{pmatrix}:
 g\in\operatorname{SL}_2(E),\ X\in R_-\right\}.
\]
This is the determinant-one Levi part of the stabilizer of a totally isotropic plane for the Hermitian form $\left(\begin{smallmatrix}0&I\\I&0\end{smallmatrix}\right)$.

**Corollary E.** If $D\le P_U(q)$ projects onto $\operatorname{SL}_2(E)$ and contains a unipotent $u$ with $(u-I)^2\ne0$, then $D=P_U(q)$.

First, $R_-$ is an equivariant additive direct summand of $M_2(E)$: the projection is $X\mapsto(X-\bar X^t)/2$, and it commutes with $gX\bar g^t$. Every $R_-$-valued cocycle that is a coboundary in $M_2(E)$ is therefore a coboundary in $R_-$. Theorem D applies with $m=2e,f=e$. Its only exceptional odd unitary parameter is $p=3,e=1$, namely $q=3$, excluded here.

For clarity, additive irreducibility is also supplied rather than assumed. Multiplication by a nonzero trace-zero scalar identifies $R_-$ with Hermitian matrices. Let $M$ be a nonzero invariant additive subgroup of that space. Take
\[
 X=\begin{pmatrix}a&b\\\bar b&d\end{pmatrix}\in M\setminus\{0\}.
\]
If both diagonal entries vanish, an upper-root conjugate has a nonzero diagonal entry for some parameter, by the nondegenerate trace pairing $s\mapsto s\bar b+\bar s b$. A coordinate interchange then produces an element with $d\ne0$. For $x(s)=\left(\begin{smallmatrix}1&s\\0&1\end{smallmatrix}\right)$,
\[
 x(s)X\bar x(s)^t+x(-s)X\bar x(-s)^t-2X
       =\operatorname{diag}(2s\bar s\,d,0)\in M.
\]
Norm surjectivity gives all $\operatorname{diag}(a,0)$ with $a\in\mathbb F_q$. Applying lower roots and subtracting the values at $s,-s$ gives every off-diagonal Hermitian matrix; summing those values and subtracting the original diagonal gives every lower diagonal matrix. Additive closure suffices throughout. Thus $M$ is the whole Hermitian space. Theorem A and the $2+2$ Jordan observation prove the corollary.

**The restriction $q\ge5$ is necessary for this parabolic criterion.** At $q=3$ there is a proper complement in $P_U(3)$ containing a Jordan-three element. Here are explicit formulas. Over $E=\mathbb F_9$, with $\bar x=x^3$, put
\[
 S_0=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
 D_3(g)=\begin{pmatrix}a^2b&ab^2\\c^2d&cd^2\end{pmatrix},
 \quad c_0(g)=-gS_0D_3(g)^t,
 \qquad g=\begin{pmatrix}a&b\\c&d\end{pmatrix}\in\operatorname{SL}_2(E).
\]
The cubic representation in the ordered basis $(e_1^3,e_2^3;e_1^2e_2,e_1e_2^2)$ has upper-right block $D_3(g)$, upper-left block $\bar g$, and lower-right block $D_0gD_0$, where $D_0=\operatorname{diag}(1,-1)$. Dualize, interchange the two block positions, and conjugate the first block by $S_0$. The resulting representation has diagonal blocks $g,\bar g^{-t}$ and off-diagonal block $c_0(g)\bar g^{-t}$. Thus $c_0$ is a cocycle for exactly the required action.

Project it to the skew-Hermitian summand:
\[
 c_-(g)=\tfrac12\bigl(c_0(g)-\overline{c_0(g)}^t\bigr),\qquad
 \pi_-(g)=\begin{pmatrix}g&c_-(g)\bar g^{-t}\\0&\bar g^{-t}\end{pmatrix}.
\]
Equivariance of the projection makes $\pi_-$ a representation preserving the displayed Hermitian form. Its image projects isomorphically onto $\operatorname{SL}_2(9)$, so it meets the additive radical trivially and is proper. At $g=x(1)$,
\[
 c_-(g)=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
 c_-(g)\bar g^{-t}=\begin{pmatrix}1&-1\\1&0\end{pmatrix},\quad
 (\pi_-(g)-I)^2=\begin{pmatrix}0&-E_{11}\\0&0\end{pmatrix}\ne0.
\]
Its cube is zero because $g$ has order three. This is the promised Jordan-three complement. More generally, the same phenomenon follows by splitting a cubic cocycle into its Hermitian and skew-Hermitian parts: the off-block of its nilpotent square is linear in the cocycle, and multiplication by a trace-zero scalar converts the Hermitian part to a skew-Hermitian one. The explicit formula above avoids needing that existence argument.

The existing rank-three construction for $q=3$ remains valid through its exact finite certificate; the counterexample concerns a general intermediate generation criterion, not that particular construction.

## 7. Exact compression and what is retained

| Existing argument | Uniform replacement supplied here | Work still required in that application |
|---|---|---|
| [Linear rank-three construction, phase21 §4](phase21_linear_rank3.md) | Theorem C at $a=b=2$ replaces both the zero-kernel exclusion and additive-kernel enlargement. It also works in characteristic two and arbitrary dimensions. | The rank-one images, their independence by Goursat and trace invariants, the actual Jordan-three word, ambient root extraction, determinant class, and IP remain separate. |
| [Unitary rank-three construction, phase20 §§3–4](phase20_unitary_rank3.md) | Corollary E replaces the nonsplit-kernel weight calculation and Hermitian-kernel enlargement after projection onto $\operatorname{SL}_2(E)$. | Full rank-one projection, containment of its preimage in the special unitary parabolic, the Jordan-three word, adjacent-plane/root extraction, determinant class, IP, and the $q=3$ certificate remain separate. |

Theorem A can be reused wherever the additive radical is irreducible and complements split. The product lemma proves the splitting hypothesis for independent factors without group classification; the explicit weight test proves it for the coupled rank-one case. It is the elimination of this hypothesis, and the demonstrated exceptional boundary, that make this more than a restatement of the two original arguments.

## 8. Prior art and verification scope

The cocycle/complement correspondence, tensor cohomology argument and central-element criterion are standard mechanisms, reproduced here with their precise hypotheses. Rank-one extension theory is established prior art. In particular, Grazian–Parker–Semeraro–van Beek, [*Fusion systems related to polynomial representations of SL2(q)*](https://arxiv.org/html/2502.20873v2), Lemma 2.4 and Lemma 5.6/Proposition 5.7, discuss the polynomial extension and the adjacent Frobenius-twist exceptions; their source is Andersen–Jørgensen–Landrock's extension calculation. The paper appeared in 2026, [DOI 10.1112/jlms.70481](https://doi.org/10.1112/jlms.70481). The elementary calculation here avoids importing that classification and does not claim it as new.

Korhonen's [*Unipotent elements forcing irreducibility in linear algebraic groups*](https://arxiv.org/html/1712.03861), §5 and Theorem 5.1, supplies closely related algebraic-group extension context. Its algebraic-group statements are not silently substituted for finite-group cohomology. The scope read for this comparison was the introductory metadata, the cited extension statements/proofs, and the polynomial exact sequence, not a full audit of either paper.

The [companion checker](phase23_generation_core_check.py) verifies 22 exact check groups, including all 5,184 cocycle equations for the characteristic-two product $\operatorname{SL}_2(2)^2$, all 720 matrices and 2,880 generator products for the explicit unitary complement over $\mathbb F_9$, the cubic identities, and 2,880 integer parameter cases. Its [saved report](phase23_generation_core_check.json) records the bounds and hashes. Run `python3 phase23_generation_core_check.py` with SymPy installed, preferably from a scratch copy because the command writes a timestamped report. The [source record](phase23_generation_core_sources.json) states exactly which primary sections were read.

Those diagnostics do not prove the universal statements; the proofs are above. This note makes no publication-priority or whole-paper compression claim, and no new Lean certification is asserted.
