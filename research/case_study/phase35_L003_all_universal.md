# Universal regular objects at every integer parameter

Date: 2026-10-10. This is a separate written consequence of the now certified finite constructions. It does not change their frozen files or assert universal finiteness.

## 1. Exact statement

Let $W$ have involutory generators $r_0,r_1,r_2,r_3$ and Coxeter pair orders
$$
(m_{01},m_{02},m_{03},m_{12},m_{13},m_{23})=(6,3,2,2,3,6).
$$
Write $x=r_0r_1$, $y=r_0r_2$, $z=r_0r_3$, and $T=y(zy)^2$. For an integer $s\geq2$, let $U_s$ be the quotient of $W$ by
$$
(y^{-1}x^{-2})^3=1,\quad (zx^3)^2=1,\quad
x^{-1}z(y^{-1}z)^2zx(zy)^2=1,\quad T^s=1.             \tag{1}
$$
Let $P_s$ be the literal source rotational presentation: generators $x,y,z$, the first six words
$$
x^6,\ y^3,\ z^2,\ (zx)^3,\ (zy)^6,\ (x^{-1}y)^2,
$$
and the four words in (1).

**Corollary.** For every integer $s\geq2$, $U_s$, with its displayed marking, is the full type-preserving automorphism group of a regular rank-four hypertope with the ordered local parameters
$$
((3,0),(2,0),(1,1),(s,0)).
$$
It is universal among marked regular objects with this Coxeter diagram and these ordered marked local toroidal residues. Moreover
$$
U_s\cong P_s\rtimes C_2,                             \tag{2}
$$
where the distinguished involution acts by $x\mapsto x^{-1}$, $y\mapsto y^{-1}$, $z\mapsto z^{-1}$.

Each of these universal objects has a finite regular quotient retaining all four local marked residues. Whenever $6$ divides $s$, the universal group $U_s$ is infinite. No additional universal group orders, finiteness cases or infinitude cases are asserted here.

## 2. Local attainment and quotient transport

Use the finite parameter-two and parameter-three groups from the frozen even and multiples-of-three constructions. For $s\geq4$, use the integral tensor marking reduced modulo the Fibonacci number $F_s$, with its global IP and typed-Helly property established in `phase35_L003_tensor_geometry.md`. Denote the chosen finite marked group by $G_s$.

The source words and local presentation adapters give a marked epimorphism $U_s\to G_s$. In omitted-type order $0,1,2,3$, each maximal parabolic of $U_s$ is a quotient of a finite toroidal reflection group of order
$$
36,\qquad 12s^2,\qquad48,\qquad108.                 \tag{3}
$$
The corresponding marked subgroup of $G_s$ has exactly that order. Thus the local group, the universal parabolic, and its finite image have equal finite order; both local maps are isomorphisms. In particular every maximal parabolic of $U_s$ injects into $G_s$.

Apply the retained all-maximal-parabolic quotient transport theorem. Its hypotheses are the full marked subgroup IP and typed coset Helly downstairs, together with these injective maximal restrictions. It concludes both properties upstairs, without assuming that $U_s$ is finite. The standard chamber argument then gives an actual thin, residually connected, flag-transitive geometry with exact residues (3). Its chamber-regular action is the full type-preserving automorphism action.

Every other marked regular object with the same diagram and these ordered marked local groups satisfies the defining words (1), so receives the generator-preserving epimorphism from $U_s$. The local restrictions are isomorphisms by the same finite order argument. This proves the stated marked universality; it does not assert that two finite quotients at the same parameter are equal.

## 3. No hidden rotational relators

The even subgroup $W^+$ has the six-relator presentation displayed in section1, and $W=W^+\rtimes\langle r_0\rangle$. Conjugation by $r_0$ inverts each distinguished generator $x,y,z$. It remains to check that the normal closure of the four additional words in $W^+$ is invariant under this involution.

This is the same local lattice argument as in the frozen universal-even and parameter-six proofs, and it is independent of the parity of $s$. In the standard triangular translation lattice, take
$$
R=\begin{pmatrix}0&-1\\1&1\end{pmatrix},\qquad
S=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$
The rotation-invariant lattice associated with $(a,0)$ is $a\mathbb Z^2$. That associated with $(a,a)$ is
$$
a\langle(1,1),(-1,2)\rangle.
$$
Both are invariant under $S$: the first assertion is immediate, and $S$ fixes $(1,1)$ and sends $(-1,2)$ to $(1,1)-(-1,2)$. Consequently the orientation-preserving normal closure of each local torus word is invariant under every local reflection. All four parameters in the theorem have one of these two forms.

If a local triangle does not contain $r_0$, choose one of its reflections $h$. The product $r_0h$ is even, and conjugation by $r_0$ on the local word is local reflection-conjugation by $h$, followed by conjugation by an even word. Its global even normal closure is therefore still preserved. This applies to each of the four words separately. Their joint even normal closure is invariant, so passing from $W^+$ to $W$ adds no extra rotational relation. The surviving sign homomorphism splits through $r_0$, proving (2).

## 4. Finite quotients and infinite universal groups

The construction in section2 supplies finite regular quotients for every $s\geq2$. If $6\mid s$, all relations defining $U_s$ hold in $U_6$, so there is a marked epimorphism $U_s\to U_6$. The frozen parameter-six infinitude certificate proves that $U_6$ is infinite. Hence $U_s$ is infinite in these cases.

This distinction is essential for interpreting source Problem9.2. All-parameter finite regular existence is established. All-parameter universal finiteness is false. The present corollary supplies the actual universal regular geometries at every parameter, but does not compute their orders or classify their other finiteness cases.

## 5. Verification scope

No new finite computation is needed. Retained inputs are the independently checked finite tensor geometry and exact local groups, the parameter-two/three bases, the abstract quotient-transport theorem, the source local toroidal presentations and their triangular-lattice adapter, and the frozen parameter-six infinitude result. The group-to-geometry and normal-closure arguments above are written proofs. The generic transport and the literal parameter-six infinitude have separate Lean certificates; this complete corollary is not claimed to be formalized. Bibliographic priority remains unverified.
