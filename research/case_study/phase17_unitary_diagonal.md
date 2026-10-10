# Rank four for PGU4(q) when q is one modulo four

10 October 2026. Private phase-seventeen proposed theorem, under internal review. Frozen phase-sixteen and earlier files are unchanged. Publication priority is unverified.

**Theorem.** For every odd prime power $q=p^e\equiv1\pmod4$, the group $\operatorname{PGU}_4(q)$ has a rank-four string C-group representation of type $\{4,2(q+1),2p\}$. Its maximum rank is four by the retained phase-nine upper bound. This is the full diagonal index-two extension of $\operatorname{PSU}_4(q)$. No statement about rank-three existence or the diagonal index-two extension when $q\equiv3\pmod4$ follows from this theorem.

## 1. A primitive norm-one parameter

Let $E=\mathbb F_{q^2}$ and $\bar x=x^q$. Choose $i\in\mathbb F_q$ with $i^2=-1$, and let $\lambda\in E^*$ have order $q+1$. Set

$$k=\lambda-\lambda^{-1}.$$

Then $\bar k=-k$ and $k\ne0$. Thus $k^2$ is a nonsquare in $\mathbb F_q$: if it were a square, then $k$ itself would belong to $\mathbb F_q$, contrary to odd characteristic and $\bar k=-k$.

Moreover $\mathbb F_p(k^2)=\mathbb F_q$. To prove this, suppose $k^2$ belongs to a proper subfield $\mathbb F_r$, where $q=r^d$. Since $k^2$ is a nonsquare in $\mathbb F_q$, the degree $d$ must be odd. In particular $d\ge3$. Now $k\in\mathbb F_{r^2}$, and $\lambda$ is a root of $X^2-kX-1$, so $\lambda\in\mathbb F_{r^4}$. Since also $\lambda\in\mathbb F_{q^2}$, the finite-field intersection formula gives $\lambda\in\mathbb F_{r^2}$, because $\gcd(4,2d)=2$. This contradicts $\operatorname{ord}(\lambda)=r^d+1>r^2-1$.

In particular $1+k^2\ne0$, because $-1$ is a square in $\mathbb F_q$.

## 2. Four explicit unitary projectivities

Use the row-Hermitian matrix $H=\operatorname{diag}(1,-1,1,-1)$, and put

$$R=\begin{pmatrix}0&i\\i&0\end{pmatrix},\qquad
S=\begin{pmatrix}k&i-k\\i+k&-k\end{pmatrix}.$$

Define

$$r_0=\operatorname{diag}(1,1,-1,-1),\quad
r_1=\begin{pmatrix}1&0&0&0\\0&0&0&1\\0&0&1&0\\0&1&0&0\end{pmatrix},\quad
r_2=\operatorname{diag}(R,S),\quad
r_3=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}.$$

Every generator satisfies $r_jH\bar r_j^T=H$. Their squares are $I,I,-I,I$, and their determinants are $1,-1,1,1$. The distant relations are

$$r_0r_2=r_2r_0,\qquad r_0r_3=-r_3r_0,\qquad r_1r_3=r_3r_1.$$

Write $\rho_j=[r_j]$. The projective involutions form a string marking. The first adjacent product has projective order four. For $M=r_2r_3$, the matrix $N=M^2+I$ is nonzero, $N^2=0$, and the characteristic polynomial of $M$ is $(X^2+1)^2$, with both eigenvalues $i,-i$ present. Hence $[M]$ has exact order $2p$.

The middle product has characteristic polynomial

$$\chi_{r_1r_2}(X)=(X^2+1)(X^2-kX-1),$$

whose four distinct roots are $i,-i,\lambda,-\lambda^{-1}$. Distinctness follows from $\operatorname{ord}(\lambda)=q+1\equiv2\pmod4$ and $q+1\ge6$. Put $q+1=2m$, with $m$ odd. A scalar power of this matrix must have even exponent, and comparison of $i$ and $\lambda$ forces that exponent to be divisible by $m$. Thus it is divisible by $q+1$. At exponent $q+1$, the two powers are $-1$ and $1$, respectively, so the least scalar exponent is $2(q+1)$. This proves the asserted type.

## 3. Generation of the full diagonal extension

The coordinate-$\operatorname{SU}_2$ argument in [phase eleven, §§2–4](phase11_unitary_template.md) applies, with the following exact comparison so that no intersection assertion is imported.

Set $d=(r_0r_1)^2=\operatorname{diag}(Z,Z)$, where $Z=\operatorname{diag}(1,-1)$. The generators $d,r_2$ are exactly those of the earlier construction, while $(r_2r_3)^2$ is the negative of its earlier value. Therefore their first and second **projective** block projections are unchanged. The group $L=\langle d,r_2,(r_2r_3)^2\rangle$ still consists of block-diagonal unitary matrices whose block determinants are equal and in $\{1,-1\}$.

For clarity, the required two-dimensional argument is as follows. The second projective block contains $[Z],[S]$ and the nonidentity unipotent represented by

$$V=\begin{pmatrix}1+ik&-ik\\ik&1-ik\end{pmatrix}.$$

The involution $Z$ moves the unique fixed line of $V$, excluding a point stabilizer. The element of order $p$ excludes torus normalizers. The element $[Z]$ is outside $\operatorname{PSU}_2(q)$, and $\operatorname{Tr}(ZS)^2/\det(ZS)=-4k^2$ excludes every proper subfield subgroup. The retained Dickson list for $\operatorname{PGL}_2(q)\cong\operatorname{PGU}_2(q)$ leaves only the exceptional $S_4$ case. Its trace-square invariants belong to $\{0,1,2,4\}\subseteq\mathbb F_p$, as follows from its element orders $1,2,3,4$. Thus the full trace field excludes it when $e>1$; for prime $q=p\ge5$, its lack of an element of order $p$ excludes it. The second image is consequently $\operatorname{PGU}_2(q)$.

The word $(dr_2)^2$ lies in the kernel $N$ of the first projective block projection and has nonscalar second block. That kernel's second image is a nontrivial normal subgroup of $\operatorname{PGU}_2(q)$ and contains $\operatorname{PSU}_2(q)$. A first-block scalar $cI$ in this kernel satisfies $c^2\in\{1,-1\}$ and $c^{q+1}=1$. As $q+1\equiv2\pmod4$, this forces $c=\pm1$. Equal block determinants now put the second block in $\operatorname{SU}_2(q)$. If $D$ is the ordinary second-block image, then $D Z(\operatorname{SU}_2(q))=\operatorname{SU}_2(q)$. Taking commutators and using perfection gives $D=\operatorname{SU}_2(q)$. Taking the derived subgroup $N'$ then strips the first scalar while retaining all of $D$, yielding the whole coordinate $\operatorname{SU}_2$ on coordinates $\{3,4\}$.

Conjugation by $r_3$ gives the pair $\{1,2\}$, and conjugation by $r_1$ gives $\{1,4\}$ and $\{2,3\}$. These pairs form a connected graph. The unitary row-elimination proof in phase eleven, §4, therefore gives the entire $\operatorname{SU}_4(q)$.

The projective image also contains $[r_1]$, whose determinant is $-1$. In the cyclic determinant quotient of order two, $-1$ is the nonidentity class: the norm-one scalar group has order $q+1\equiv2\pmod4$, so $-1$ is not a square in it. Hence the projective generated group is precisely $\operatorname{PGU}_4(q)$.

The retained external inputs in this generation step are the rank-one maximal-subgroup list, the standard rank-one unitary/projective-linear identification, simplicity of $\operatorname{PSL}_2(q)$ and perfection of $\operatorname{SL}_2(q)$ for $q\ge4$. They do not assert the rank-four intersection property.

## 4. A common isotropic line and a semilinear involution

The facet subgroup $F=\langle r_0,r_1,r_2\rangle$ preserves the nondegenerate symmetric form

$$B=\operatorname{diag}(i+k,i+k,i-k,i+k)$$

up to scalar: the multipliers are $1,1,-1$. The vertex subgroup $P=\langle r_1,r_2,r_3\rangle$ preserves the column line spanned by

$$v=(1,1,1,1)^T,$$

and its eigenvalue on this chosen vector belongs to $\mu_4=\{1,-1,i,-i\}$, since the three generator eigenvalues are $1,i,1$.

On columns use the equivalent Hermitian form $h(x,y)=\bar x^THy$. Define the semilinear map

$$\sigma(x)=BH\bar x,\qquad \nu=-1-k^2.$$

Directly $\sigma^2=\nu I$ and $h(\sigma x,\sigma y)=\nu\overline{h(x,y)}$. Both $v$ and $\sigma v$ are isotropic, while

$$h(v,\sigma v)=4i+2k\ne0.$$

The last inequality follows from $k\notin\mathbb F_q$. Thus $W=\langle v,\sigma v\rangle_E$ is a nondegenerate Hermitian plane. It is $\sigma$-stable, as is $W^\perp$.

If a unitary matrix $g$ satisfies $gBg^T=\mu B$, then

$$g\sigma=\mu\sigma g.$$

Indeed $gH\bar g^T=H$ gives $g^T=H\bar g^{-1}H$, and substitution yields $gBH=\mu BH\bar g$.

Now suppose also $g\in P$, so $gv=\alpha v$ with $\alpha\in\mu_4\subseteq\mathbb F_q$. Then

$$g\sigma v=\mu\bar\alpha\,\sigma v.$$

Preservation of the nonzero Hermitian cross-pair gives $\mu\bar\alpha^2=1$. Consequently

$$\mu=\alpha^2\in\{1,-1\}.$$

This conclusion permits arbitrary initial similitude multiplier $\mu$. It is essential for projective intersections: a chosen vertex lift of an element of $[F]$ may differ from a facet lift by an arbitrary unitary scalar, so its multiplier must not be presumed to equal a facet generator's multiplier.

## 5. Bounding the maximal-parabolic intersection

Consider $J=P\cap\operatorname{GO}(B)$. Its action on $v$ is a homomorphism into $\mu_4$. An element of its kernel fixes both vectors $v,\sigma v$ and commutes with $\sigma$.

Choose $c\in E^*$ with $c\bar c=\nu^{-1}$, possible by norm surjectivity. The semilinear map $\tau=c\sigma$ squares to one and is antiunitary. Its fixed subspace in $W^\perp$ is a two-dimensional vector space over $\mathbb F_q$, spanning $W^\perp$ over $E$. For completeness, if $\delta\ne0$ has $\bar\delta=-\delta$, then every vector $x$ is the sum of the fixed vector $(x+\tau x)/2$ and $\delta$ times the fixed vector $(x-\tau x)/(2\delta)$. This is the elementary quadratic descent used here.

The Hermitian form restricts on that fixed space to a nondegenerate symmetric bilinear form over $\mathbb F_q$. The restriction is nondegenerate because the fixed space spans the nondegenerate Hermitian space. Every kernel element restricts to an isometry of this binary form. Restriction is injective since the element already fixes $W$ pointwise. A nondegenerate binary orthogonal group over an odd field has order $2(q-1)$ or $2(q+1)$. Therefore

$$|J|\le4\cdot2(q+1)=8(q+1).$$

The scalar subgroup of $P$ has exactly two elements. Its scalar eigenvalues must lie in $\mu_4\cap\mu_{q+1}=\{1,-1\}$, and $-I=r_2^2$ belongs to $P$. Hence the projective image of $J$ has order at most $4(q+1)$.

Every projective element common to $[F]$ and $[P]$ has a lift in $J$, because scalar multiplication preserves the property of being a $B$-similitude. On the other hand it contains the middle dihedral subgroup $\langle\rho_1,\rho_2\rangle$ of order $4(q+1)$. Thus

$$[F]\cap[P]=\langle\rho_1,\rho_2\rangle.$$

This argument does not identify either maximal parabolic with a whole classical subgroup and does not require the vertex group order.

## 6. Both rank-three intersection properties

For the first triple, every element of $\langle\rho_1,\rho_2\rangle$ fixes the projective line $[v]$. Set $T=r_0r_1$. Its projective cyclic subgroup has order four, and the four vectors $T^jv$, $0\le j<4$, have sign patterns

$$++++,\quad ++--,\quad +-+-,\quad +--+.$$

They define distinct projective lines in odd characteristic. Since $r_1v=v$, the stabilizer of $[v]$ in the order-eight dihedral group $\langle\rho_0,\rho_1\rangle$ is exactly $\langle\rho_1\rangle$. This proves the first triple's IP.

For the second triple, the two adjacent dihedral groups have orders $4(q+1)$ and $4p$. Their intersection has order dividing four and contains $\rho_2$. If its order were four, it would be a Sylow two-subgroup of the order-$4p$ dihedral group and would contain its central involution $[M^p]$, where $M=r_2r_3$.

With $N=M^2+I$, put

$$C=M(I+N/2).$$

Since $N^2=0$, one has $C^2=-I$ and $M^p=(-1)^{(p-1)/2}C$. Also $Cv=iv$. If $C$ were a $B$-similitude, §4 would force its multiplier to be $-1$. But direct multiplication gives

$$\bigl(CBC^T+B\bigr)_{12}=-ik^2/2\ne0.$$

Thus $[M^p]$ is not a projective $B$-similitude and cannot belong to the middle dihedral subgroup, which lies in $[F]$. This rules out order four, proving that the second intersection is exactly $\langle\rho_2\rangle$.

The standard recursive string C-group criterion (McMullen–Schulte, Proposition 2E16) now proves full IP for the four generators. Together with generation and the orders in §2, this proves the theorem.

## 7. Scope, retained inputs and verification boundary

The explicit norm-one primitive choice works for every $q\equiv1\pmod4$, including nonprime fields; no asymptotic sieve or exceptional-field catalogue is used. The proof newly verifies the intersection property for this modified template. It retains the previously written generation mechanism, elementary quadratic Galois descent and the binary orthogonal-group order formula. The maximum-rank consequence retains [phase nine](phase9_linear_unitary.md).

This note does not address $q\equiv3\pmod4$, where $\operatorname{PGU}_4(q)$ has cyclic diagonal quotient of order four and cannot be generated by involutions. Its index-two subgroup in that congruence class is addressed in [the twisted companion](phase17_unitary_twisted.md). Nor does this note import rank-three existence from the simple socle to its extension.

The [symbolic checker](phase17_unitary_diagonal_symbolic.py) verifies 43 exact identities over the parameter ring with $i^2=-1$, $\bar i=i$ and $\bar k=-k$. The [finite checker](phase17_unitary_diagonal_check.g) uses natural actions on isotropic planes for $q=5,9,13,17$. In every case it checks the expected ambient order, all generator/string relations, all 16 marked subgroup closures and all 256 meets. These bounded computations corroborate the written proof; they are not its universal justification. Run the Python checker from a scratch copy to preserve its historical timestamped report.

The source/status boundary is recorded in [the separate bounded audit](phase17_unitary_diagonal_status.md). No new Lean formalization or publication-priority claim is made. The theorem has two internal written reviews, which are not external peer review.
