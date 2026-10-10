# A six-dimensional integral affine model for the even L003 family

This note replaces the 1,296-coordinate voltage realization by four explicit affine transformations of \(\mathbb Z^6\). It gives an independently checkable construction of the same marked finite groups, with order \(1296m^6\) for every integer \(m\geq1\). It does **not** identify the universal source group with an affine group, prove a split extension, or assert a new priority claim.

The finite calculations below are exhaustive certificates for a single explicit marking. The passage to every modulus is a lattice and quotient argument, not extrapolation from several moduli.

## 1. The four maps and the statements

For column coordinates \(a=(a_1,\ldots,a_6)\), put
\[
\begin{aligned}
r_0(a)&=(-a_1-a_2+a_6,\ a_2,\ a_4+a_5+a_6,\ a_4,\ a_3-a_4-a_6,\ a_6),\\
r_1(a)&=(a_4,\ -a_2,\ -a_2+a_3,\ a_1,\ -a_6,\ -a_5),\\
r_2(a)&=(a_1,\ -a_1-a_2+a_4,\ -a_3+a_4-a_5+a_6-1,\ a_4,\ a_5,\ a_6),\\
r_3(a)&=(a_1+a_2-a_6,\ -a_2,\ -a_4-a_5-a_6,\ -a_3-a_5,\ a_5+a_6,\ -a_6).
\end{aligned}
\]
Products are ordinary composition: \((A,u)(B,v)=(AB,u+Av)\). Let \(\Gamma=\langle r_0,r_1,r_2,r_3\rangle\), let \(Q\) be its linear image, and let \(H_m\) be its image on \((\mathbb Z/2m\mathbb Z)^6\).

**Theorem.** The maps are involutions and the following assertions hold.

1. \(|Q|=1296\), the reduction of \(Q\) modulo 2 is faithful, and the translation kernel of \(\Gamma\to Q\) is exactly \(2\mathbb Z^6\).
2. For every \(m\geq1\),
   \[
   1\longrightarrow (\mathbb Z/m\mathbb Z)^6
   \longrightarrow H_m\longrightarrow Q\longrightarrow1,
   \qquad |H_m|=1296m^6.
   \]
3. These are exactly the previously constructed marked groups \(G_m\): the isomorphism sends each distinguished involution to the involution with the same index.
4. The four generators of \(H_m\) have the subgroup intersection property and typed coset Helly. Their coset geometries are finite regular rank-four hypertopes with source parameter \(s=2m\). The same intersection and Helly conclusions hold for \(\Gamma\).

The exact local source parameters in omission order \(0,1,2,3\) are
\[
(1,1),\quad (2m,0),\quad (2,0),\quad(3,0).
\]
Thus this statement uses the finite-quotient interpretation of L003 Problem 9.2. It says nothing about finite universal orders.

## 2. Relations and the lattice kernel

Set \(x=r_0r_1,\ y=r_0r_2,\ z=r_0r_3\). Direct integral affine multiplication gives
\[
\begin{gathered}
x^6=y^3=z^2=(zx)^3=(zy)^6=(x^{-1}y)^2=1,\\
(y^{-1}x^{-2})^3=(zx^3)^2=1,\\
x^{-1}z(y^{-1}z)^2\,zx(zy)^2=1.
\end{gathered}
\tag{1}
\]
These are the first nine rotational relators of the source presentation, before the parameter relation.

The standalone checker closes the four \(6\times6\) integral linear matrices. It finds exactly 1296 matrices, which remain pairwise distinct modulo 2. Alongside each matrix \(q\), breadth-first search retains an actual affine word \(s(q)\). There are exactly \(1296\cdot4=5184\) Schreier words
\[
s(q)r_i s(q\bar r_i)^{-1}.
\]
Their linear parts are identity; their translation vectors are the differences of the two affine offsets having the same linear part. Every such difference is even in all six coordinates.

Six of them are exactly \(2e_1,\ldots,2e_6\). The zero-based breadth-first edge indices are
\[
(143,0),(152,3),(162,2),(172,1),(223,2),(244,0).
\]
The report also records and directly reevaluates the six literal generator words, so this basis claim is not inferred solely from an offset-subtraction convention.

Schreier rewriting, or telescoping consecutive prefixes of a word with trivial linear part, says these 5184 translations generate the entire kernel. Therefore that kernel is precisely \(2\mathbb Z^6\). This argument makes no splitting assumption.

If an element of \(\Gamma\) is identity modulo \(2m\), its linear part is identity modulo 2 and hence identity over the integers. It is therefore a translation \(2v\), and it vanishes modulo \(2m\) exactly when \(v\in m\mathbb Z^6\). Consequently the kernel of reduction is \(2m\mathbb Z^6\), proving assertions 1 and 2, including composite \(m\).

## 3. The local groups and actual geometry

Write
\[
T=y(zy)^2,\qquad u=y^{-1}z.
\]
The same integral calculation gives
\[
T^2=(-2e_1),\qquad u^{-1}T^2u=(-2e_2)
\tag{2}
\]
as pure translations. The linear part of \(T\) has exact order 2. Hence \(T\) has exact order \(2m\) in \(H_m\): every trivial power is even, and \(T^{2j}=1\) there exactly when \(m\mid j\). The translations in (2) generate a group \(C_m^2\).

The three integral maximal parabolics omitting \(0,2,3\) close with orders \(36,48,108\), respectively. Their projections to \(Q\) are injective. Thus they inject under every reduction modulo \(2m\), and also under \(\Gamma\to H_1\).

The parameter parabolic, omitting 1, maps onto the order-48 base parabolic and contains the independent translations (2) in its reduction kernel. It therefore has order at least \(48m^2\). The source toroidal presentation with parameter \((2m,0)\) has full order
\[
12(2m)^2=48m^2.
\]
The marked triangle and source-word adapters are the ones proved in the frozen even-family note; (1) and \(T^{2m}=1\) give that presentation as an upper bound. The bounds coincide. The other three toroidal upper bounds are likewise attained. No quotient preservation of intersection properties is presumed in this local argument.

For the base \(H_1\), the checker computes all sixteen marked subgroups and all 256 subgroup meets. In mask order their orders are
\[
1,2,2,12,2,6,4,108,2,4,6,48,12,48,36,1296.
\]
It constructs right cosets as components of the left Cayley action, enumerates every pairwise incident flag of maximal-parabolic cosets, and tests that the total intersection is nonempty. All 5287 flags pass. The 1296 chambers have singleton common intersection.

Apply the one-exceptional-parabolic quotient theorem to \(H_m\to H_1\), protecting all omission types except 1. The three protected maximal parabolics inject, and the image has full subgroup IP and typed Helly. Therefore both properties lift to \(H_m\). The identical argument applies to \(\Gamma\to H_1\). This uses the written general transport theorem; the existing Lean module certifies that abstract transport, not the finite matrix calculations here.

The associated coset systems are therefore actual flag-transitive geometries. The subgroup intersection property gives trivial chamber stabilizer and two chambers through each panel; their residues are connected because their corresponding marked parabolics are generated by their distinguished involutions. Thus they are regular hypertopes. This geometry step is separate from merely verifying the source relations.

## 4. Exact comparison with the earlier voltage model

This section is unnecessary for constructing \(H_m\), but proves the marked identification in assertion 3.

The frozen voltage group acts on 1296 copies of \(\mathbb Z\) on the right:
\[
(i,t)g=(p_g(i),t+v_g(i)).
\]
Its pullback action on rational functions is
\[
F_g(f)=v_g+f\circ p_g.
\]
Under the right-action convention \(p_{gh}=p_h\circ p_g\), one has \(F_g\circ F_h=F_{gh}\). Hence this is the same multiplication convention as the affine maps above.

Let \(B=(b_1,\ldots,b_6)\) be the six-column integer basis of the frozen Schreier translation lattice \(L\), obtained from the same six indexed edges. Its minor on rows \(0,1,2,4,5,6\) has determinant 1. Let \(s(q)\) be the deterministic earlier voltage transversal and put
\[
c=(-44,-6,36,-80,210,-94)^{\mathsf T},\qquad
\theta=\frac{\sum_{q\in Q}v_{s(q)}+Bc}{1296}.
\]
Define the injective affine map
\[
E:\mathbb Q^6\longrightarrow\mathbb Q^{1296},
\qquad E(a)=\theta+\tfrac12Ba.
\]
For each of the four old voltage generators \((p_i,v_i)\), the comparison checker verifies, coordinate by coordinate,
\[
B\circ p_i=BM_i,\qquad
v_i+\theta\circ p_i-\theta=\tfrac12B\,b_i^{\rm aff},
\tag{3}
\]
where \(M_i\) and \(b_i^{\rm aff}\) are the literal matrix and offset of \(r_i\). The second identity is checked after multiplication by \(2\cdot1296\), using integers only. There are 31,104 linear and 5,184 affine coordinate equalities. Thus \(F_{r_i}E=E r_i\).

This intertwining is faithful on the old integer group. Its underlying permutation quotient has order 1296, and its induced six-dimensional linear image also has order 1296, so no nonidentity permutation lies in the kernel. Any remaining kernel element would be a pure translation fixing \(E(a)\), which forces its voltage vector to be zero.

Moreover translation by \(b_i\) restricts to translation by \(2e_i\). The frozen saturated-lattice theorem identifies the kernel of old coordinate reduction modulo \(m\) with \(mL\), while §2 identifies the new kernel modulo \(2m\) with \(2m\mathbb Z^6\). The integer marked isomorphism carries these kernels to one another, and therefore induces \(G_m\cong H_m\) for every \(m\).

## 5. Certificates, dependencies and scope

Run the independent compact construction with:

    python3 phase35_L003_affine_check.py --output /tmp/affine-fresh.json

It uses only the Python standard library and literal six-dimensional matrices, with no data input. The separate comparison uses the previously published mathematical voltage data:

    python3 phase35_L003_affine_compare.py \
      --data phase33_L003_even_voltage.json \
      --output /tmp/affine-comparison-fresh.json

Both commands refuse to overwrite existing evidence. The saved reports record source and input hashes. Neither checker calls GAP, a rewriting package, or numerical floating-point algebra.

Retained inputs are precisely:

- The source toroidal presentation and order formula, and the four local adapters recorded in [the even-family proof](phase33_L003_even_family.md). These identify the local map names and parameters; they are not needed for the kernel or group-order calculation.
- [The general quotient transport](phase33_one_exceptional_transport.md) for IP/Helly lifting, and the standard coset characterization of regular hypertopes.
- Only for §4, [the saturated-lattice theorem](phase34_L003_even_order.md) and its certificate, plus the frozen original voltage data.

The source is Fernandes–Leemans–Ivić Weiss, *Hexagonal extensions of toroidal maps and hypermaps* (2018), §2, §8 and Problem 9.2. The checked primary version is the [institutional PDF](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf), SHA256 ac8c635fef77acdb14c43c81ce083bb26bbe784852735c0f9486fda73af1d873. Copyrighted source text is not distributed with these certificates.

The contribution here is a compact explicit model and its exact verification, not a new general hypertope construction theorem. The affine image is virtually abelian. The omitted-parameter universal group, or a universal group with a parameter imposed, need not equal this image. No extension splitting or identification as a wreath product is asserted.
