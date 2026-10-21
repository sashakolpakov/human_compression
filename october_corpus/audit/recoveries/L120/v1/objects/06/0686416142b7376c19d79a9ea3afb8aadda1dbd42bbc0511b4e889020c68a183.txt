# The remaining diagonal index-two unitary groups

10 October 2026. Private phase-seventeen proposed theorem, under internal review. This is a separate extension of [the one-modulo-four construction](phase17_unitary_diagonal.md). Earlier frozen phases are unchanged; publication priority is unverified.

**Theorem.** Let $q=p^e\equiv3\pmod4$ be an odd prime power, and let $U_2(q)$ be the unique index-two extension of $\operatorname{PSU}_4(q)$ inside $\operatorname{PGU}_4(q)$. Then $U_2(q)$ has a rank-four string C-group representation of type $\{4,2(q+1),2p\}$. Its maximum rank is four by the retained phase-nine bound. The proof is uniform for $q\ge7$; $q=3$ uses an explicit natural-matrix finite certificate for generation, while its intersection proof remains uniform.

The full $\operatorname{PGU}_4(q)$ has cyclic socle quotient of order four and is not involution-generated. It must not be confused with $U_2(q)$.

## 1. Parameters and projective unitary membership

Let $E=\mathbb F_{q^2}$, $\bar x=x^q$, and choose $i\in E$ with $i^2=-1$. Here $\bar i=-i$. Choose $\lambda\in E^*$ of order $2(q+1)$ and set

$$k=\lambda-\lambda^{-1}.$$

Since $\lambda^{q+1}=-1$, one has $\bar\lambda=-\lambda^{-1}$, giving $k\in\mathbb F_q^*$. Also $\mathbb F_p(k^2)=\mathbb F_q$. Indeed $\lambda^2$ has order $q+1$ and is a root of

$$X^2-(k^2+2)X+1.$$

If $k^2$ belonged to a proper subfield $\mathbb F_r$, its Frobenius would fix or interchange the two distinct roots $\lambda^2,\lambda^{-2}$. Their order would then divide $r-1$ or $r+1$, contradicting $q>r$. Finally $1+k^2\ne0$, since $-1$ is nonsquare in $\mathbb F_q$.

Use exactly the matrices $H,r_0,r_1,r_2,r_3,R,S$ in §2 of the companion one-modulo-four proof. Their algebraic squares, determinants, string signs and bilinear-form identities are unchanged. Their Hermitian multipliers are now

$$r_jH\bar r_j^T=\epsilon_jH,\qquad
(\epsilon_0,\epsilon_1,\epsilon_2,\epsilon_3)=(1,1,-1,1).$$

Thus $r_2$ is an anti-isometry; its projective image is nevertheless unitary. Explicitly, for a primitive $\xi\in E^*$ put $\eta=\xi^{(q-1)/2}$, so $\eta\bar\eta=-1$. Then $\eta r_2$ is an isometry. If $\zeta=\xi^{q-1}$ generates the norm-one scalar group, then

$$\det(\eta r_2)=\eta^4=\zeta^2.$$

This is the unique nonidentity order-two class in the cyclic determinant quotient of order four. The other determinant classes are $1,-1,1$, and $-1=\zeta^{(q+1)/2}$ also has even exponent. Consequently every projective generator lies in $U_2(q)$, and $[r_2]$ is outside the socle.

## 2. The three adjacent orders

The first and last product orders remain four and $2p$, by the identical matrix identities in the companion proof. The middle polynomial is again

$$ (X^2+1)(X^2-kX-1),$$

with four distinct roots $i,-i,\lambda,-\lambda^{-1}$. Write $q+1=4m$. A primitive fourth root is a power $\lambda^{2m}$ or $\lambda^{6m}$. Therefore the ratio $\lambda/i$ has order $8m=2(q+1)$: its exponent $1-2m$ or $1-6m$ is relatively prime to $8m$, because any common divisor divides four and the exponent is odd. All eigenvalues have orders dividing $8m$, so the projective middle order is exactly $2(q+1)$.

## 3. Generation when q is at least seven

Normalize the anti-isometry by setting $\widetilde r_2=\eta r_2$; this does not change any projective generator. Put $d=(r_0r_1)^2=\operatorname{diag}(Z,Z)$ as before. Consider the block-diagonal unitary group

$$L=\langle d,\widetilde r_2,(\widetilde r_2r_3)^2\rangle.$$

Its second projective block image contains $[Z],[\eta S]$ and the unipotent represented by

$$V=\begin{pmatrix}1+ik&-ik\\ik&1-ik\end{pmatrix}.$$

The point-stabilizer, torus-normalizer and subfield exclusions are exactly as in the companion proof: $Z$ moves the unique fixed point of $V$, the projective element $V$ has order $p$, and the scalar/conjugacy invariant of $ZS$ is $-4k^2$, generating the full field. The rank-one identification $\operatorname{PGU}_2(q)\cong\operatorname{PGL}_2(q)$ is realized inside $\operatorname{PGL}_2(E)$, so the trace-square subfield exclusion applies to its conjugate subfield groups.

The outer witness now is $[\eta S]$, rather than $[Z]$. Its determinant $\eta^2=\zeta$ is nonsquare in the norm-one group, so it lies outside $\operatorname{PSU}_2(q)$. The only remaining exceptional type in the retained Dickson list is $S_4$. Its trace-square invariants belong to $\{0,1,2,4\}\subseteq\mathbb F_p$, so $\mathbb F_p(k^2)=\mathbb F_q$ excludes it when $e>1$, including characteristic three. For prime $q=p\ge7$, its element orders exclude the element of order $p$. Thus the second image is the full $\operatorname{PGU}_2(q)$.

Let $N$ be the kernel of the first projective block projection of $L$. The word $(d\widetilde r_2)^2$ lies in $N$ and has nonscalar second block, because $(ZR)^2=I$ whereas $(ZS)^2$ is nonscalar. Thus the second projective image of $N$ is nontrivial and normal in $\operatorname{PGU}_2(q)$. Simplicity and the trivial projective centralizer of $\operatorname{PSU}_2(q)$ imply that it contains $\operatorname{PSU}_2(q)$.

This time a first-block scalar in $N$ need not be $\pm I$; no such restriction is used. Let $D$ be the second ordinary block image of $N$. The first block is scalar, so the first block of $N'$ is identity. Also $D'\le\operatorname{SU}_2(q)$, and its projective image contains the perfect group $\operatorname{PSU}_2(q)$. Thus

$$D'Z(\operatorname{SU}_2(q))=\operatorname{SU}_2(q).$$

Perfection of $\operatorname{SU}_2(q)$ gives $D'=\operatorname{SU}_2(q)$. Therefore $N'=\{I_2\}\times\operatorname{SU}_2(q)$. The coordinate-pair conjugations and unitary elimination in the companion proof now yield $\operatorname{SU}_4(q)$.

Together with the determinant computation in §1, this proves that the projective group is exactly $U_2(q)$. The rank-one simplicity and perfection inputs apply because $q\ge7$. They are deliberately not asserted for $q=3$.

## 4. The projective intersection with pseudo-unitary lifts

Keep the **unnormalized** matrices for this argument, and write $P=\langle r_1,r_2,r_3\rangle$. They fix $v=(1,1,1,1)^T$ with eigenvalues $1,i,1$. Thus every $g\in P$ satisfies

$$gv=\alpha v,\quad\alpha\in\mu_4,\qquad
gH\bar g^T=\epsilon H,\quad\epsilon=\alpha^2.$$

The equality between multiplier and squared eigenvalue holds on each generator and therefore on the whole group. It is the extra constraint needed in this congruence class.

The facet subgroup preserves the same symmetric matrix

$$B=\operatorname{diag}(i+k,i+k,i-k,i+k)$$

up to scalar. Define $\sigma(x)=BH\bar x$. Now

$$\sigma^2=(1+k^2)I,\qquad
h(\sigma x,\sigma y)=(1+k^2)\overline{h(x,y)}.$$

As before $v,\sigma v$ are isotropic and $h(v,\sigma v)=4i+2k\ne0$, since $i\notin\mathbb F_q$. Their span $W$ is a nondegenerate Hermitian plane stable under $\sigma$.

Suppose $g\in P$ also satisfies $gBg^T=\mu B$, initially with **arbitrary** multiplier $\mu$. The pseudo-unitary relation gives

$$g\sigma=(\mu/\epsilon)\sigma g.$$

Apply the Hermitian form to $gv$ and $g\sigma v$. Its nonzero cross-pair yields

$$\mu\bar\alpha^2=\epsilon^2=1,$$

and hence $\mu=\alpha^2=\epsilon$. An element in the kernel of the eigenvalue map $g\mapsto\alpha$ therefore is an ordinary isometry, fixes $W$ pointwise, and commutes with $\sigma$.

The identical quadratic-descent argument from the companion proof embeds this kernel in a binary orthogonal group over $\mathbb F_q$, of size at most $2(q+1)$. There are at most four eigenvalue fibers. The scalar subgroup of $P$ is exactly $\{I,-I\}$: if $g=\alpha I$ were scalar, its Hermitian multiplier would be $\alpha\bar\alpha=1$ for all $\alpha\in\mu_4$, whereas the group relation says it equals $\alpha^2$. Thus $\alpha=\pm1$, and $-I=r_2^2$ occurs.

It follows that the projective intersection of the two maximal parabolics has order at most $4(q+1)$. It contains the middle dihedral group of that order, so equality holds. No projective-scalar multiplier is omitted in this argument.

## 5. The smaller meets and q=3

Both rank-three arguments in the companion proof use algebraic identities unchanged in this branch. The first dihedral group's orbit of $[v]$ has size four. For the second, the possible order-four intersection would contain the central involution represented by

$$C=M\bigl(I+(M^2+I)/2\bigr),\qquad M=r_2r_3.$$

Here $Cv=iv$, so §4 again forces its potential $B$ multiplier to be $-1$. The same nonzero defect $(CBC^T+B)_{12}=-ik^2/2$ rules this out. Thus both triples satisfy IP, and the recursive criterion proves full IP in every odd characteristic, including three.

For $q=3$, use $E=\mathbb F_3[\lambda]/(\lambda^2-\lambda-1)$, with $\lambda$ primitive of order eight. In the displayed template take $i=\lambda+1$ and $k=1$. Thus the lower block of $r_2$ is explicitly

$$\begin{pmatrix}1&\lambda\\\lambda-1&-1\end{pmatrix}.$$

These coordinates, together with the three signed permutation matrices already displayed, are the entire finite witness. The [standalone q3 checker](phase17_unitary_q3_check.g) verifies that $r_0,r_1,\lambda r_2,r_3$ are isometries and have square determinants, with $\det(\lambda r_2)=-1$. Hence their projectivities lie in $U_2(3)$, including a nontrivial diagonal class.

The natural action on the 112 totally isotropic planes has generated image order $6531840$, equal to twice $|\operatorname{PSU}_4(3)|$. Scalars act trivially. Consequently

$$6531840=|\text{permutation image}|\le|\text{generated projective subgroup}|\le|U_2(3)|=6531840.$$

This order sandwich certifies the whole ambient group; it neither assumes faithfulness of the action nor invokes a group-recognition oracle. The same executable constructs all 16 marked subgroups and checks all 256 meets. It gives type $\{4,8,6\}$.

The finite base supplies only generation at $q=3$; the general written intersection argument above applies there without change. The uniform group-generation proof for $q\ge7$ does not depend on any finite sampling.

## 6. Combined scope

Together with the companion one-modulo-four theorem, the index-two diagonal extension of $\operatorname{PSU}_4(q)$ has maximum rank four for **every odd prime power q≥3**, using the retained phase-nine bound. This includes an extension of $\operatorname{PSU}_4(3)$ even though that simple socle itself has no string C-group representation, by the retained published simple-group classification. The cyclic index-four extensions have no involution generating set.

No rank-three existence theorem for these extensions is inferred, and field/graph extensions remain outside scope. This is a proposed mathematical result under internal review, not an externally peer-reviewed publication or a verified novelty claim.

The [twisted symbolic checker](phase17_unitary_twisted_symbolic.py) passed 43 exact identities with $\bar i=-i$ and $\bar k=k$. The [natural-action checker](phase17_unitary_twisted_check.g) passed for $q=3,7,11$, with all 48 marked subgroup closures and 768 exact meets. The additional standalone $q=3$ certificate verifies the explicit-coordinate base separately. The source/status audit is [shared with the companion branch](phase17_unitary_diagonal_status.md). No new Lean formalization is claimed.
