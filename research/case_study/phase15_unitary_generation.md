# A generation criterion in the second unitary congruence class

10 October 2026. Original phase-fifteen conditional generation theorem; separate companion notes establish the intersection and existence statements. Frozen phase-fourteen artifacts are unchanged.

Let $q=p^e\equiv3\pmod4$, $q\ge7$, and $E=\mathbb F_{q^2}$. Choose $i^2=-1$, so $\bar i=-i$. Take $t,x,y\in\mathbb F_q$ with

$$t^2+x^2+y^2=1,\qquad txy\ne0,$$

and put $a=it$, $b=x+iy$, $c=-x+iy=-\bar b$. Define

$$R=\begin{pmatrix}0&i\\i&0\end{pmatrix},\quad
S=\begin{pmatrix}a&b\\c&-a\end{pmatrix},\quad
Z=\operatorname{diag}(1,-1),$$

and use the four matrices $r_0,r_1,r_2=\operatorname{diag}(R,S),r_3$ in [the frozen q=7 note](phase14_unitary_q7.md). They belong to $\operatorname{SU}_4(q)$ for the identity Hermitian form and have the stated projective string relations.

**Generation criterion.** Suppose $\mathbb F_p(a^2)=\mathbb F_q$. If $e>1$, these four matrices generate $\operatorname{SU}_4(q)$. If $e=1$, the same conclusion holds provided one of $ZS$, $RS$, $(ZR)S$ has projective order greater than five.

This is sufficient, not necessary. In particular the previously certified q=7 marking has $y=0$ and lies outside this criterion. It nevertheless generates the whole group by its separate exact certificate. The middle characteristic polynomial remains $X^4+aX^3-aX+1$, independent of $b$; generation and the intersection property must still be separated.

## 1. The rank-one projection

Let $J=\langle[Z],[R],[S]\rangle\le\operatorname{PGU}_2(q)$. In this congruence class $i\bar i=1$, and $iZ$ has determinant one. Thus all three projective generators lie in $\operatorname{PSU}_2(q)\cong\operatorname{PSL}_2(q)$. The matrices $Z,R$ anticommute and give two distinct commuting projective involutions. They generate a Klein four subgroup whose nontrivial elements are $[Z],[R],[ZR]$.

We retain the classical maximal-subgroup list, explicitly stated in Proposition 2.3 of Leemans–Moerenhout–O'Reilly-Regueiro, [*Projective linear groups as automorphism groups of chiral polytopes*](https://arxiv.org/html/1606.08017). The rank-one unitary/linear identification is by conjugacy over $E$, so trace-square invariants test its subfield subgroups. We use the standard simplicity of $\operatorname{PSL}_2(q)$ and perfection of $\operatorname{SL}_2(q)$ for $q\ge4$.

The Borel subgroup has odd order $q(q-1)/2$, so cannot contain this Klein four subgroup. In a dihedral group containing a Klein four group, one of the latter's nonidentity elements is central in the whole dihedral group. But $[S]$ commutes with none of $[Z],[R],[ZR]$. Indeed,

$$\operatorname{tr}(ZS)=2it,\qquad
\operatorname{tr}(RS)=-2y,\qquad
\operatorname{tr}((ZR)S)=-2ix$$

are nonzero. For two nonscalar traceless two-by-two matrices, anticommutation is equivalent to the product having trace zero; ordinary commutation makes them proportional. Here proportionality is excluded by $txy\ne0$. Projective commutation has exactly those two possibilities. Thus no dihedral maximal subgroup contains $J$.

For the subfield cases, the scalar/conjugacy invariant

$$\tau(ZS)=\frac{\operatorname{tr}(ZS)^2}{\det(ZS)}=-4a^2$$

does not lie in a proper subfield by hypothesis. This excludes every conjugate proper subfield group. Since $e$ is odd, the square-field $\operatorname{PGL}_2$ maximal subgroup cannot occur either. If $e>1$, the stated maximal-subgroup list has no exceptional $A_4,S_4,A_5$ case. If $e=1$, the additional order hypothesis excludes them, because their element orders are at most five. Therefore $J=\operatorname{PSU}_2(q)$.

## 2. The block kernel supplies a coordinate SU2

Put $d=(r_0r_1)^2=\operatorname{diag}(Z,Z)$ and

$$u=(r_2r_3)^2=\operatorname{diag}(-RS,-SR),\qquad
L=\langle d,r_2,u\rangle.$$

The second projective block image of $L$ is exactly $J$: it contains $[Z],[S],[SR]$, hence $[R]$. Let $N$ be the kernel of the first projective block projection. For $w=dr_2$, the first block of $w^2$ is $(ZR)^2=I$. The second is $(ZS)^2$, which is nonscalar: $ZS$ is nonscalar with nonzero trace $2a$, while a nonidentity projective involution in odd characteristic has trace zero. Hence the second projective image of $N$ is a nontrivial normal subgroup of the simple group $J$, and is all of $J$.

Taking the commutator subgroup removes every scalar first block. The second blocks of $N'$ have determinant one, and their projective image is $J'=J$. Let their subgroup be $D\le\operatorname{SU}_2(q)$. Then $D Z(\operatorname{SU}_2(q))=\operatorname{SU}_2(q)$. Perfection implies

$$\operatorname{SU}_2(q)=\operatorname{SU}_2(q)'=D'\le D,$$

so $D=\operatorname{SU}_2(q)$ and

$$N'=\{I_2\}\times\operatorname{SU}_2(q).$$

This argument permits first-block scalars $\pm i$, which occur in the present congruence class; it does not copy the earlier $\pm1$-only assertion.

Conjugation by $r_3$ supplies the other coordinate SU2. Conjugation by $r_1$ gives coordinate pairs $\{1,4\}$ and $\{2,3\}$. These four pairs form a connected graph. Their SU2 subgroups generate SU4 by the explicit unitary elimination argument in [phase11_unitary_template.md](phase11_unitary_template.md), §4, applied here to the identity Hermitian form. This proves the criterion.

## 3. Scope and next steps

The criterion reduces full generation to the sphere $t^2+x^2+y^2=1$, a full-field condition on $t^2$, and simple rank-one exclusions. This generation theorem alone does not show parameter existence or any subgroup intersection property. Those are proved in the separately reviewed companion notes.

The companion intersection theorem uses projective middle order $(q^2-1)/2$ or $(q^2+1)/2$, reflecting the order-four scalar center of SU4 in this congruence class. This order condition is separate from the generation argument.
