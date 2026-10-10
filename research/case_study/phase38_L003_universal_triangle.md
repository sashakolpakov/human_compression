# A triangle-group quotient of the exact universal presentation

Date: 2026-10-10. New additive result; all earlier presentation, tensor and geometry certificates remain unchanged.

## 1. Statement and source boundary

For an integer $s\geq2$, let $P_s$ be the following **literal ten-relator presentation**:
\[
\begin{split}
P_s=\langle x,y,z\mid& x^6,\ y^3,\ z^2,\ (zx)^3,\ (zy)^6,
(x^{-1}y)^2,\\
&(y^{-1}x^{-2})^3,\ (zx^3)^2,\
x^{-1}z(y^{-1}z)^2zx(zy)^2,\ [y(zy)^2]^s\rangle .
\end{split}                                                    \tag{1}
\]
This is the source presentation in Fernandes–Leemans–Ivić Weiss, *Hexagonal extensions of toroidal maps and hypermaps* (2018), section 8, page 17, at the ordered parameters $((3,0),(2,0),(1,1),(s,0))$. The primary institutional copy is [2018DFW.pdf](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf). Source assets and retained original notes are hash-bound in the accompanying intake.

Let $U_s$ be the four-involution presentation in the frozen `phase35_L003_all_universal.md`: its Coxeter pair orders, in the order $01,02,03,12,13,23$, are $(6,3,2,2,3,6)$, and its four additional words are the last four words in (1), with $x=r_0r_1$, $y=r_0r_2$, $z=r_0r_3$.

**Theorem.** For every integer $s\geq6$, both $P_s$ and $U_s$ are infinite. More precisely, a subgroup of a quotient of $P_s$ surjects onto the triangle Coxeter group
\[
K_s=\langle d,h,q\mid d^2=h^2=q^2=(dh)^2=(dq)^3=(hq)^s=1\rangle. \tag{2}
\]
There is also a direct marked quotient of $U_s$ containing that quotient of $P_s$.

Combined with the retained all-parameter geometry theorem, this proves that the actual universal regular hypertopes in that theorem are infinite at every $s\geq6$. The new algebraic proof below does not use the previous parameter-six voltage certificate, its finite computations, or any intersection-property or coset-Helly assumption.

The source Table 8, page 18, labels its entries finite universal hypertopes and reports full orders $1296,13824,165888,5184000$ at $s=2,3,4,5$. Those are **retained published computational finiteness statements**, not newly certified by this package. Subject to precisely that retained input, the finite parameters are exactly $2,3,4,5$. The unconditional new assertion of this package is infinitude for every $s\geq6$.

## 2. A fixed wreath convention

Permutations of $\{0,1,2\}$ act on the right: $(pr)(i)=r(p(i))$. In the group $K_s^3\rtimes S_3$, write an element as $[A;p]$, where $A=(A_0,A_1,A_2)$. Our multiplication convention is
\[
[A;p][B;r]=[(A_iB_{p(i)})_{i=0}^2;pr].                       \tag{3}
\]
Associativity follows immediately by applying the displayed rule twice; it is the usual coordinate-permutation semidirect product with this right-action convention.

Put $c=(2,0,1)$ in image-list notation and $v=dqd$. Thus $c^3=1$, and in $K_s$ we have
\[
v^2=1,\quad vdv=q,\quad vqv=d,\quad (vd)^3=(dv)^3=1,
\quad hdh=d.                                                 \tag{4}
\]
All of (4) follow from the involution relations, $(dq)^3=1$, and $dh=hd$; they do not use $(hq)^s=1$.

Define
\[
X=[(d,v,v);c],\qquad Y=[(1,1,1);c],\qquad Z=[(h,q,h);1].       \tag{5}
\]
Let $H_s=\langle X,Y,Z\rangle\leq K_s^3\rtimes\langle c\rangle$.

## 3. All ten relators, without a matrix-specialization assumption

Every one of the first nine words in (1), evaluated on (5), has trivial permutation part. The following table gives its coordinate words after cancelling only adjacent equal involutions. Thus it can be checked from (3) independently of (4).

| Source word | Three coordinate words after involution cancellation |
|---|---|
| $X^6$ | $(1,1,1)$ |
| $Y^3$ | $(1,1,1)$ |
| $Z^2$ | $(1,1,1)$ |
| $(ZX)^3$ | $(hdhvqv,\ qvhdhv,\ hvqvhd)$ |
| $(ZY)^6$ | $(1,1,1)$ |
| $(X^{-1}Y)^2$ | $(1,1,1)$ |
| $(Y^{-1}X^{-2})^3$ | $((vd)^3,\ (dv)^3,\ 1)$ |
| $(ZX^3)^2$ | $(hdhd,\ qvdvqvdv,\ hdhd)$ |
| $X^{-1}Z(Y^{-1}Z)^2ZX(ZY)^2$ | $(vqhdhq,\ 1,\ dhqvqh)$ |

Each entry is the identity by (4). For clarity, $vqv=d$ handles the fourth row; $vdv=q$ handles the middle coordinate of the eighth. In the last row, $hdh=d$ reduces the first coordinate to $vqdq=v^2=1$, while $qvq=d$ reduces the third to $dhdh=1$. Here $qvq=d$ is another immediate consequence of $(dq)^3=1$ and $v=dqd$.

The parameter word has the exact formula
\[
\mathcal T=Y(ZY)^2=[(hq,1,qh);1].                             \tag{6}
\]
Since $qh=(hq)^{-1}$, its $s$th power is the identity by the final defining relation of $K_s$. This checks the **tenth** source relator uniformly, rather than only at sampled parameters. Hence (1) defines an epimorphism $P_s\twoheadrightarrow H_s$.

These identities hold even before the parameter relation is imposed, in the amalgam with presentation $\langle d,h,q\mid d^2=h^2=q^2=(dh)^2=(dq)^3=1\rangle$. The accompanying checker implements finite-factor word reduction in $\langle d,h\rangle\cong C_2^2$ and $\langle d,q\rangle\cong S_3$, amalgamating their common $\langle d\rangle$. Only positive word reductions are used; no faithfulness claim about a numerical tensor representation is needed.

## 4. A subgroup surjects onto the whole triangle group

Let $H_s^0$ be the kernel of the permutation projection $H_s\to\langle c\rangle$. Coordinate projection $\pi_0:H_s^0\to K_s$ is a homomorphism. By (3)–(4),
\[
X^3=[(d,q,d);1],\qquad Z=[(h,q,h);1],\qquad
Y^{-1}ZY=[(q,h,h);1].                                        \tag{7}
\]
All three lie in $H_s^0$, and their first coordinates are $d,h,q$. Consequently $\pi_0$ is onto. Thus infinitude of $K_s$ implies infinitude of $H_s$, and hence of $P_s$. We do not claim that $P_s$ itself surjects onto $K_s$; the surjection is from this explicitly identified subgroup of its quotient.

There is also a direct four-involution quotient. Let $f=(2,1,0)$ and $F=[(1,1,1);f]$. Formula (3), with $v^2=d^2=1$, gives
\[
F^2=1,\quad FXF=X^{-1},\quad FYF=Y^{-1},\quad FZF=Z.
                                                                    \tag{8}
\]
Therefore $R_0=F$, $R_1=FX$, $R_2=FY$, $R_3=FZ$ are involutions. Their six pair-order relations are exactly the first six words in (1): in particular $R_1R_3=X^{-1}Z$ is the inverse of $ZX$, and $R_2R_3=Y^{-1}Z$ is the inverse of $ZY$. The other four defining words hold by section 3. We obtain $U_s\twoheadrightarrow\langle F,X,Y,Z\rangle$, whose subgroup $H_s$ is infinite whenever $K_s$ is. This proves infinitude of $U_s$ directly, without needing the retained identification $U_s=P_s\rtimes C_2$.

## 5. Explicit infinitude of $K_s$ for every $s\geq6$

Set $t=2\cos(\pi/s)$ and consider the following real matrices acting on column vectors:
\[
D=\begin{pmatrix}-1&0&1\\0&1&0\\0&0&1\end{pmatrix},\quad
H=\begin{pmatrix}1&0&0\\0&-1&t\\0&0&1\end{pmatrix},\quad
Q=\begin{pmatrix}1&0&0\\0&1&0\\1&t&-1\end{pmatrix}.             \tag{9}
\]
Direct multiplication gives $D^2=H^2=Q^2=I$, $DH=HD$, and $(DQ)^3=I$.
The plane spanned by the second and third standard basis vectors is $HQ$-invariant; the restriction is
\[
\begin{pmatrix}t^2-1&-t\\t&-1\end{pmatrix},
\]
which has determinant $1$ and trace $t^2-2=2\cos(2\pi/s)$. Its two eigenvalues are $e^{2\pi i/s}$ and $e^{-2\pi i/s}$. For $s\geq6$ they are distinct and neither is $1$. The action induced by $HQ$ on the one-dimensional quotient is $1$. Therefore the full matrix is diagonalizable over $\mathbb C$, with these three distinct eigenvalues, and $(HQ)^s=I$. Hence (9) defines a representation of the exact presentation (2).

Put $C=DHQ$. Its characteristic polynomial is
\[
\det(\lambda I-C)=(\lambda+1)
\bigl(\lambda^2+(1-t^2)\lambda+1\bigr).                       \tag{10}
\]
If $s>6$, then $t^2>3$, so the two roots of the quadratic are positive, reciprocal and distinct, with one strictly greater than $1$. Thus $C$ has infinite order.

At $s=6$, $t=\sqrt3$. Direct multiplication gives
\[
C^2=I+M,\qquad
M=\begin{pmatrix}1&t&-2\\t&3&-2t\\2&2t&-4\end{pmatrix},
\qquad M\ne0,\quad M^2=0.                                    \tag{11}
\]
Consequently $(C^2)^n=I+nM$ for every nonnegative integer $n$, and these matrices are distinct over $\mathbb R$. Thus $C$ has infinite order here too. This proves the theorem without invoking the classification or faithfulness of geometric triangle reflection groups.

## 6. Verification and dependency ledger

Run `python3 phase38_L003_universal_triangle_check.py --output NEW_REPORT.json`. The checker refuses to overwrite its output. It checks all nine fixed source words in the abstract amalgam, the literal word table, the parameter-word formula (6), the three surjection witnesses (7), and the four-involution lift (8). It separately checks the polynomial matrix identities, characteristic polynomial (10), and the nonzero square-zero matrix (11) in exact integer polynomial arithmetic. The tenth relation for arbitrary $s$, the real eigenvalue argument and subgroup-surjection proof are written arguments; no finite sample is offered in their place.

| Dependency | Exact role |
|---|---|
| Source section 8, page 17 | The literal marked presentation (1); no source conjecture or source target theorem is assumed. |
| Elementary group presentations and semidirect products | Convert the ten checked relators into the displayed quotient; coordinate projection proves the subgroup surjection. |
| Elementary real/complex linear algebra and trigonometry | Show that (9) satisfies (2) and has an infinite-order element; all polynomial identities are independently executable. |
| Frozen all-parameter universal geometry note | Only identifies these exact $U_s$ as universal regular hypertope groups with the asserted local residues; unnecessary for algebraic infinitude. |
| Source Table 8, rows 5–8 | Only the qualified published finite baseline at $s=2,3,4,5$, not used in the new proof. |
| Frozen integral tensor model | Motivated (5); none of its computed identities, faithfulness or geometry is needed as a proof input here. |

This package makes no new claim about orders or structure of $P_s$ or $U_s$, no equality with the wreath quotient, and no new finite-existence claim. Priority remains unverified. In particular, the incomplete prior-art comparison with Zhang's 2024 *Abelian covers of regular hypertopes* remains unresolved. The earlier finite-existence interpretation of source Problem 9.2 stays distinct from the universal-infinitude theorem proved here.
