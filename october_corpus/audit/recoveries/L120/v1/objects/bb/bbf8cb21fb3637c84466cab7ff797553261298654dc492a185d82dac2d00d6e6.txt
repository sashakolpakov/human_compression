# A conditional intersection theorem for q congruent to three modulo four

10 October 2026. Original phase-fifteen proposed conditional proof. Separate internal reviews and exact symbolic checks record their own scopes; this note alone does not prove parameter existence for every field.

Use the matrices and parameters in [phase15_unitary_generation.md](phase15_unitary_generation.md). In addition to $q\ge7$, $q\equiv3\pmod4$ and $txy\ne0$, assume

$$h=t^2+2y+2\ne0,\qquad
m=\operatorname{ord}_{\mathrm{proj}}(r_1r_2)\in
\{(q^2-1)/2,(q^2+1)/2\}.$$

**Theorem.** The four projective involutions have the full string C-group intersection property. If the generation criterion in the companion note holds, they form a string C-group for $\operatorname{PSU}_4(q)$ of type $\{4,m,2d\}$, where $d$ is the projective order of $RS$.

## 1. Two forms and the exact multiplier restriction

Put $a=it$, $b=x+iy$, $c=-x+iy$. Define

$$B=\operatorname{diag}(c,c,b,c),$$

and, writing $z=ia$, $u=ib-1$, $v=1-ic$, define

$$A=\begin{pmatrix}
0&z&u&-z\\-z&0&-z&v\\-u&z&0&z\\z&-v&-z&0
\end{pmatrix}.$$

Direct identities give

$$r_0Br_0^T=B,\quad r_1Br_1^T=B,\quad r_2Br_2^T=-B,$$
$$r_1Ar_1^T=-A,\quad r_2Ar_2^T=A,\quad r_3Ar_3^T=A,$$

and

$$B\bar B=(1-t^2)I,\qquad A\bar A=-hI,\qquad\det A=h^2.$$

Here $b\ne0$: its norm is $x^2+y^2$, and $-1$ is a nonsquare in $\mathbb F_q$, so this can vanish only when $x=y=0$. Thus $1-t^2\ne0$. The form $A$ is alternating and nonsingular; $B$ is symmetric and nonsingular.

Let $M$ consist of the elements of SU4 that multiply each of $A,B$ by a sign, and let $K$ preserve both exactly. Then $[M:K]\le4$. This restriction to signs is deliberate: general unitary similitudes of these forms may have other fourth-root multipliers, but the two actual marked parabolics have only sign multipliers. The whole scalar center $\{\lambda I:\lambda^4=1\}$, of order four, lies in $M$. Consequently

$$|\operatorname{proj}(M)|=|M|/4\le |K|.$$

The exact $A$-stabilizer in SU4 is isomorphic to $\operatorname{Sp}_4(q)$. The descent proof in [phase11_unitary_intersection.md](phase11_unitary_intersection.md), §1, applies with Hermitian matrix $I$ and $A\bar A=-hI$: normalize the semilinear operator $w\mapsto A\bar w$ to square one, take its four-dimensional fixed space over $\mathbb F_q$, and rescale the restricted alternating form. This does not require $q\equiv1\pmod4$; that earlier congruence was used for the multiplier group, which has been handled separately here.

## 2. The middle rotation bounds the maximal-parabolic intersection

Put $T=r_1r_2$ and $W=AB^{-1}$. The multiplier identities give $TW=WT$, and $T^2$ preserves both forms exactly. Direct calculation gives

$$\chi_T(X)=X^4+aX^3-aX+1,\qquad
\det(e_1,Te_1,T^2e_1,T^3e_1)=-ib\ne0.$$

Since the scalar kernel has order four and $m$ is prime to the characteristic, $T$ is semisimple. Its cyclicity makes all four eigenvalues distinct. Moreover no eigenvalues are negatives of one another: subtracting $\chi_T(\lambda)$ and $\chi_T(-\lambda)$ would give $\lambda^2=1$, whereas $\chi_T(\pm1)=2$. Thus $T^2$ is also regular semisimple. The polynomial discriminant is $4(a^2-8)^2(a^2+1)$, so in particular $a^2\ne8$.

For explicit regularity of $W$, substitute $c=-(1+a^2)/b$ and put

$$f=a^2b-ia^2+ib^2-2b-i.$$

Then

$$\operatorname{disc}(\chi_W)=
\frac{-16a^4(a^2-8)^2(a^2+b^2+1)^4f^2}{(a^2+1)^{11}}.$$

All factors are nonzero: $a\ne0$, $a^2\ne8$, $a^2+1\ne0$,
$a^2+b^2+1=b(b+\bar b)=2xb\ne0$, and $f/b=-h\ne0$.
Hence the full matrix centralizers of $W,T,T^2$ are the same diagonal algebra in their common eigenbasis. Every element of $K$ therefore centralizes $T^2$ in the exact $A$-stabilizer $\operatorname{Sp}_4(q)$.

That centralizer is a rank-two symplectic torus. The possible structures are

$$C_{q-1}^2,\quad C_{q-1}\times C_{q+1},\quad C_{q+1}^2,
\quad C_{q^2-1},\quad C_{q^2+1}.$$

This is the elementary reciprocal-eigenline classification used in the previous intersection proof. If $m=(q^2-1)/2$, the projective order of $T^2$ is $(q^2-1)/4>q+1$ for $q\ge7$. If $m=(q^2+1)/2$, it is $m>q+1$. These inequalities exclude the two equal-factor tori by their exponents. The opposite-sign torus is excluded by

$$\gcd((q^2-1)/4,q^2+1)\le2,\qquad
\gcd((q^2+1)/2,q^2-1)=1.$$

In the minus case, both the mixed torus $C_{q-1}\times C_{q+1}$ and the cyclic torus $C_{q^2-1}$ remain possible, but both have order $q^2-1=2m$. In the plus case the mixed torus is excluded together with the cyclic minus torus by the displayed coprimality, leaving order $q^2+1=2m$. Thus $|K|\le2m$ and $|\operatorname{proj}(M)|\le2m$. The latter group contains the middle dihedral subgroup $\langle\rho_1,\rho_2\rangle$ of order $2m$, so it equals that subgroup. Since the first maximal parabolic preserves $B$ by signs and the second preserves $A$ by signs, their intersection is exactly the middle subgroup. For this assertion, a common projective element can be represented by a lift in the first parabolic and by a lift in the second. The two lifts differ by a scalar in $\mu_4$, whose square is a sign; hence a single lift has both multipliers in $\{1,-1\}$, as required.

## 3. The two rank-three intersection checks

For the first triple, $\langle\rho_0,\rho_1\rangle$ is dihedral of order eight, represented by $r_1$ and the diagonal Klein four group generated by $r_0$ and $\operatorname{diag}(Z,Z)$. Every off-diagonal position of $A$ is nonzero: $z=-t\ne0$, and $u=-y-1+ix$, $v=1+y+ix$ cannot vanish when $x\ne0$. A diagonal sign matrix multiplying $A$ by a scalar must therefore have all four signs equal. Only the identity in that displayed Klein four is scalar. Since $r_1$ multiplies $A$ by $-1$, the intersection with its projective similitude stabilizer is exactly $\langle\rho_1\rangle$. This proves the first triple's intersection property.

For the second triple, put $w=r_2r_3$ and

$$U=-RS=\begin{pmatrix}y+ix&-t\\t&y-ix\end{pmatrix},\qquad
V=-SR=R^{-1}UR.$$

We have $w^2=\operatorname{diag}(U,V)$. For every integer $j$, Cayley–Hamilton gives $s,r\in\mathbb F_q$ such that

$$U^j=\begin{pmatrix}s+irx&-rt\\rt&s-irx\end{pmatrix},\qquad
V^j=\begin{pmatrix}s-irx&rt\\-rt&s+irx\end{pmatrix}.$$

For $w^{2j}$, the upper-left block of the transformed $B$ has off-diagonal entry $2icr^2xt$. If $w^{2j}$ preserves $B$ up to scalar, this forces $r=0$. Both blocks are then the same scalar $sI$, so $w^{2j}$ is projectively trivial.

For $w^{2j+1}$, the upper-right block is $RV^j$. The transformed upper-left $B$ block has off-diagonal entry and difference of its diagonal entries

$$2rtx(s+ry),\qquad 2x\big((s+ry)^2-r^2\big).$$

They cannot both vanish: the first gives $r=0$ or $s+ry=0$; in the first case the second is $2xs^2\ne0$, and in the second it is $-2xr^2\ne0$. Invertibility excludes $r=s=0$. Thus no odd power of $w$ preserves $B$ up to scalar. Since $r_2$ already does so, the dihedral subgroup $\langle\rho_2,\rho_3\rangle$ intersects the projective $B$-similitude stabilizer in precisely $\langle\rho_2\rangle$. This proves the second triple's intersection property.

The standard recursive string C-group criterion now gives the complete rank-four intersection property. Finally a power of $w$ is scalar exactly when it is an even power $w^{2j}$ with $U^j$ scalar, so $\operatorname{ord}_{\mathrm{proj}}(w)=2\operatorname{ord}_{\mathrm{proj}}(U)=2d$ as asserted.

## 4. The remaining existence problem

The result is conditional on a large-middle parameter and, for the full group, the separately stated generation criterion. The uniform existence theorem and its finite coordinate certificates are given separately in [phase15_unitary_sieve.md](phase15_unitary_sieve.md). The symbolic identities alone do not prove that theorem. Publication priority and external review remain unestablished.
