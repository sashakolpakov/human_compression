# Finite regular hypertopes for every source parameter divisible by three

Date: 2026-10-10. This is a separate construction; the frozen even-parameter and fixed-parameter-six packages remain unchanged.

**Theorem.** For every integer \(m\ge1\), there is a finite regular rank-four hypertope with the ordered toroidal parameters
\[
 ((3,0),(2,0),(1,1),(3m,0))
\]
of Fernandes–Leemans–Ivić Weiss (2018), §8. Its maximal parabolic groups, in omitted-type order \(0,1,2,3\), have orders
\[
 36,\qquad108m^2,\qquad48,\qquad108.
\]
These are exact marked toroidal residues. The construction has a base group of order \(13824\) at \(m=1\). No full-group order formula for general \(m\), universal-group identification, or priority claim is made.

Together with the frozen even-parameter construction, this proves finite regular existence at every parameter \(s\ge2\) divisible by two or three. It does not cover all parameters coprime to six. The source already supplies \(s=5\); that isolated input does not establish a uniform remaining family.

## 1. Literal integral action and the exact varying parameter

The file phase34_L003_triple_voltage.json specifies three permutations \(p_x,p_y,p_z\) of a set \(\Omega\) of size \(272\), with integer weights \(v_x,v_y,v_z\). Use right actions
\[
 (i,t)g=(p_g(i),t+v_g(i)),\qquad (i,t)\in\Omega\times\mathbb Z.
\]
On two copies of this space, let
\[
 X=\operatorname{diag}(g_x,g_x^{-1}),\quad
 Y=\operatorname{diag}(g_y,g_y^{-1}),\quad
 Z=\operatorname{diag}(g_z,g_z^{-1}),
\]
let \(r_0\) exchange the copies, and put \(r_1=r_0X,r_2=r_0Y,r_3=r_0Z\). These four transformations are involutions. Write
\[
 x=r_0r_1=X,\qquad y=r_0r_2=Y,\qquad z=r_0r_3=Z.
\]
The standalone checker verifies, over the integers at all \(544\) states,
\[
 x^6=y^3=z^2=(zx)^3=(zy)^6=(x^{-1}y)^2=1,
\]
\[
 (y^{-1}x^{-2})^3=(zx^3)^2
 =(x^{-1}z(y^{-1}z)^2)(zx(zy)^2)=1. \tag{1}
\]
These are the first nine source rotational relators. There are \(4896\) relator/state checks.

Let \(\widetilde G\) be this integer-action group. Define \(G_m\) by reducing the integer coordinate modulo \(2m\), so \(G_m\) is a finite permutation group on \(1088m\) points. The base \(G_1\) is reduction modulo two, and \(G_m\) maps onto \(G_1\) for every \(m\).

For the source parameter word and its conjugate set
\[
 T=y(zy)^2,\qquad A=T^3,\qquad
 u=y^{-1}z,\qquad B=u^{-1}Au.
\]
The checker verifies that \(A,B\) are pure translations, each with coordinates in \(\{-2,0,2\}\), and that the underlying permutation of \(T\) is nonidentity. At the zero-based integer-state coordinates \(1,0\), the translation vectors have matrix
\[
 \begin{pmatrix}v_A(1)&v_B(1)\\v_A(0)&v_B(0)\end{pmatrix}
 =\begin{pmatrix}0&-2\\-2&0\end{pmatrix}. \tag{2}
\]

Because \(T^3\) has identity underlying permutation, that permutation has exact order three. In reduction modulo \(2m\), \(A\) has exact order \(m\): all coordinates are divisible by two, and one coordinate equals \(-2\). Thus \(T\) has exact order \(3m\).

Moreover, (2) proves
\[
 \langle A,B\rangle\cong C_m\times C_m
 \quad\hbox{inside }G_m. \tag{3}
\]
Indeed \(A,B\) commute and both have order dividing \(m\). If \(A^aB^b=1\) modulo \(2m\), the two selected coordinates imply \(2m\mid2a\) and \(2m\mid2b\), hence \(m\mid a,b\). This cancellation is an integer-divisibility argument and holds for even and composite \(m\); no inversion of two modulo \(2m\) is being assumed.

Both translations vanish modulo two. They therefore lie in the kernel of \(G_m\to G_1\).

## 2. Exact local groups

Write \(P_{m,i}=\langle r_j:j\ne i\rangle\) inside \(G_m\). The checker enumerates the three corresponding integer subgroups \(\widetilde P_0,\widetilde P_2,\widetilde P_3\) completely. Whenever two encountered elements have the same underlying permutation, it checks equality of their full integer weights. Closure terminates with orders
\[
 |\widetilde P_0|=36,\qquad
 |\widetilde P_2|=48,\qquad
 |\widetilde P_3|=108. \tag{4}
\]
Their underlying-permutation projections are injective. Hence they inject into every coordinate modulus, and the homomorphisms
\[
 P_{m,i}\longrightarrow P_{1,i},\qquad i=0,2,3,
\]
are isomorphisms.

The exceptional parabolic \(P_{m,1}\) contains \(y,z,A,B\). Its image \(P_{1,1}\) has exact order \(108\), established by finite closure below. Equation (3) supplies a kernel of order at least \(m^2\), giving
\[
 |P_{m,1}|\ge108m^2. \tag{5}
\]

For the matching upper bound use the source toroidal-map presentation, equation (2.3), with local rotations
\[
 (u,v)=(y^{-1}z,y^{-1}).
\]
Its standard translation \(v^{-1}u^{-2}\) is exactly \(T=y(zy)^2\). Relations (1) supply the local triangle presentation, and \(T^{3m}=1\) supplies the torus relation for parameter \((3m,0)\). Thus the full three-involution parabolic is a quotient of the corresponding regular toroidal-map group, of order
\[
 12(3m)^2=108m^2.
\]
The lower bound (5) proves equality and an isomorphism preserving the local marked generators.

For clarity, all four substitutions into the same source presentation are:

| Omitted type | Local rotations | Exact torus parameter | Full local order |
|---|---|---|---|
| \(0\) | \((zy,zx)\) | \((1,1)\) | \(36\) |
| \(1\) | \((y^{-1}z,y^{-1})\) | \((3m,0)\) | \(108m^2\) |
| \(2\) | \((x^{-1},x^{-1}z)\) | \((2,0)\) | \(48\) |
| \(3\) | \((x,y)\) | \((3,0)\) | \(108\) |

For the three fixed entries, the torus relators are respectively the ninth, eighth and seventh relations of (1). Their standard upper orders equal the attained integer orders (4). This proves the marked local identifications, not merely matching numerical orders. The retained input is the triangular-lattice toroidal presentation with full order \(12(a^2+ab+b^2)\).

## 3. One finite base, with subgroup IP and typed Helly checked separately

The checker constructs the actual coordinate-modulus-two action of \(G_1\), enumerates it completely and finds order \(13824\). It closes all sixteen marked subgroups and verifies all \(256\) equalities
\[
 G_{1,I}\cap G_{1,J}=G_{1,I\cap J}. \tag{6}
\]
Its four maximal parabolics have orders \(36,108,48,108\).

It separately verifies every typed-Helly cardinality used in §3 of the frozen fixed-parameter-six note. For each type \(i\) and each two- or three-element set \(J\) of other types, the number of \(P_{1,i}\)-cosets incident with the base flag of types \(J\) equals
\[
 \left[\bigcap_{j\in J}P_{1,j}:
 P_{1,i}\cap\bigcap_{j\in J}P_{1,j}\right]. \tag{7}
\]
All sixteen tests pass. The right-hand side is the orbit of the base flag stabilizer, which is always contained in the incident set; equality gives transitivity on the possible extensions. Induction on flag size therefore moves every flag to a base flag and proves that each pairwise incident typed coset family has a common point. This is a distinct check from (6).

## 4. Uniform geometric transport

Apply the one-exceptional-maximal-parabolic quotient theorem to
\[
 G_m\longrightarrow G_1,
\]
with exceptional type \(1\). The downstairs full marked intersection property and typed Helly are established in §3. Section2 proves injectivity on the other three maximal parabolics. The theorem, with its proof in the even-family note and its separate generic Lean certificate, supplies both properties for every \(G_m\).

The group-theoretic reason no injectivity on \(P_{m,1}\) is necessary is exact. Among proper generator subsets, only the exceptional maximal subset can fail to lie inside an injective maximal parabolic; its intersection with itself is tautological. For typed Helly, every flag with at least two types has a nonexceptional type at which to anchor the common-point lifting argument. Empty and singleton flags require no injectivity.

Consequently the standard coset system of \(G_m\) is a flag-transitive geometry. Full marked IP makes the chamber stabilizer trivial and the panel stabilizers the relevant groups of order two, proving thinness. In each residue, its remaining distinguished involutions generate the residue chamber action, so its chamber graph is connected. Thus the geometry is residually connected. A type-preserving automorphism fixing a chamber fixes every adjacent chamber by thinness, and hence every chamber; therefore the chamber-regular group \(G_m\) is the full type-preserving automorphism group. The exact residue identifications in §2 complete the theorem.

## 5. Reproduction, discovery and scope

Run the standard-library checker with a new output:

    python3 phase34_L003_triple_check.py --output NEW_REPORT.json

It reads only the literal phase34_L003_triple_voltage.json, refuses an existing output, and does not import a finder, GAP, or symbolic algebra. It checks all integer relators, the three fixed integer parabolics, the exact translation minor, the complete base group, all marked subgroup intersections, and the necessary typed-Helly counts. The passage to every \(m\) is the written divisibility, local-order and quotient-transport argument.

The data were discovered through an abelian character of a parameter-three quotient kernel, compressed to its character orbit and combined with a finite quotient action. Those discovery computations are not verification inputs: all resulting integer transformations and required identities are explicit and independently checkable.

The primary source is [Fernandes–Leemans–Ivić Weiss (2018)](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf), equations (2.3)–(2.4), §8, Table8 and Problem9.2. This result proves finite regular existence for all source parameters divisible by three, and the earlier even-family theorem covers parameters divisible by two. It does not establish finite universal groups; the universal groups at parameters divisible by six are already known to be infinite from the separate frozen result. It also does not prove all-parameter existence or establish a current-literature priority claim.
