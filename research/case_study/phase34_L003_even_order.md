# Exact orders of the even-parameter voltage quotients

Date: 2026-10-10. Separate supplement to the frozen even-parameter family.

**Theorem.** Let \(G_m\), \(m\ge1\), be the finite group defined by the frozen literal voltage data in [the even-parameter construction](phase33_L003_even_family.md). Then
\[
 |G_m|=1296m^6.
\]
More precisely, the integer-action group \(\widetilde G\) and its underlying permutation group \(Q=G_1\) fit into
\[
 1\longrightarrow L\cong\mathbb Z^6
 \longrightarrow\widetilde G\longrightarrow Q\longrightarrow1,
 \qquad |Q|=1296,
\]
and coordinate reduction modulo \(m\) has kernel exactly \(mL\). Consequently
\[
 1\longrightarrow C_m^6\longrightarrow G_m\longrightarrow Q\longrightarrow1.
 \tag{1}
\]
No splitting of either sequence is asserted. In source parameters \(s=2m\), the finite regular hypertope constructed there has exactly \(1296(s/2)^6\) chambers. This is the order of a specified finite quotient, not the order of the universal group \(U_s\) or its rotation subgroup \(P_s\).

## 1. A direct Schreier calculation

The original data give four involutions acting on \(D\times\mathbb Z\), with \(|D|=1296\), by
\[
 (i,t)(p,v)=(p(i),t+v(i)).
\]
For right actions,
\[
 (p,v)(q,w)=(q\circ p,\ v+w\circ p).
 \tag{2}
\]
Projecting to the first coordinate gives \(Q\). A transformation in the kernel is exactly an integer translation vector in \(\mathbb Z^D\), and multiplication of two such elements is vector addition.

The verifier enumerates the underlying permutation group by breadth-first search, starting at its identity and trying the distinguished generators \(r_0,r_1,r_2,r_3\) in that order. Simultaneously it stores one integer-action representative \(s(q)\) for each permutation \(q\). Each representative is an actual word in the generators, and \(s(1)=1\). For every \(q\in Q\) and \(j\in\{0,1,2,3\}\), put
\[
 h_{q,j}=s(q)r_j s(q\overline r_j)^{-1}. \tag{3}
\]
These are \(1296\cdot4=5184\) elements of the translation kernel \(L\).

They generate all of \(L\), with no Reidemeister–Schreier software assumption. For a word \(r_{j_1}\cdots r_{j_t}\) whose underlying permutation is the identity, write \(q_i=\overline r_{j_1}\cdots\overline r_{j_i}\), \(q_0=1\). The product
\[
 \prod_{i=1}^t \bigl(s(q_{i-1})r_{j_i}s(q_i)^{-1}\bigr)
\]
telescopes to the original word because \(q_t=1\). Every element of the kernel is represented by such a word, since the generators are involutions. Thus \(L\) is exactly the integer span of the vectors (3).

To compute each vector, let \(s(q)r_j=(p,v)\) and \(s(q\overline r_j)=(p,w)\). Formula (2) gives
\[
 h_{q,j}=(1,v-w). \tag{4}
\]
The verifier checks the equal underlying permutations before using this subtraction.

## 2. A six-vector integral basis

Use zero-based breadth-first representative indices and choose the six vectors \(b_1,\ldots,b_6\) from the edges
\[
 (143,0),\ (152,3),\ (162,2),\ (172,1),\ (223,2),\ (244,0).
 \tag{5}
\]
Their values on coordinate indices \(0,1,2,4,5,6\), with vectors as columns, form
\[
 M=
 \begin{pmatrix}
 0&0&1&-1&0&0\\
 0&0&0&0&-1&-1\\
 1&0&0&1&1&0\\
 0&0&-1&0&-1&1\\
 0&0&0&0&1&0\\
 1&1&-1&0&0&0
 \end{pmatrix},
 \qquad \det M=1. \tag{6}
\]
The verifier computes this determinant and inverse by exact rational elimination and checks that every inverse entry is an integer.

For each of all 5184 vectors \(z=h_{q,j}\), let \(z_C\) be its six selected coordinates and put \(c=M^{-1}z_C\in\mathbb Z^6\). The checker then verifies, on **every** coordinate of \(D\),
\[
 z=\sum_{\ell=1}^6 c_\ell b_\ell. \tag{7}
\]
This is 6,718,464 coordinate equalities. Conversely each \(b_\ell\) is one of the generators (3). Equations (6)–(7) therefore prove
\[
 L=\mathbb Zb_1\oplus\cdots\oplus\mathbb Zb_6,
\]
and the coordinate projection \(L\to\mathbb Z^6\) is an integral isomorphism. This proves a saturated embedding in the literal coordinate lattice; rational rank alone would not suffice.

As an additional check, the six words in (3) are re-evaluated directly as integer transformations rather than by subtraction. The report stores those words, the matrix and its inverse. It also records the four exact integral conjugation matrices on this basis and verifies that they square to the identity. These action matrices are corroborating data, not an extra hypothesis in the order proof.

## 3. Coordinate reduction has exactly the claimed kernel

Coordinate reduction is the actual action on \(D\times(\mathbb Z/m\mathbb Z)\). A transformation becomes the identity only if its underlying permutation is already the identity. Its kernel on \(\widetilde G\) is consequently
\[
 L\cap m\mathbb Z^D.
\]
If \(z=\sum c_\ell b_\ell\) belongs to this intersection, all its selected coordinates are divisible by \(m\). Since \(M^{-1}\) is integral, \(c=M^{-1}z_C\) has all entries divisible by \(m\). Therefore \(z\in mL\). The reverse inclusion is immediate, giving
\[
 L\cap m\mathbb Z^D=mL. \tag{8}
\]
This proves (1) and the exact order formula for every positive integer \(m\), including \(m=1\) and arbitrary composite moduli. There is no assumption that a lattice has full image after reduction; equation (8) establishes the required fact from the specific unimodular minor.

## 4. Evidence, reproduction and scope

Run the standalone original verifier with a new output file:

    python3 phase34_L003_even_order_check.py --output NEW_REPORT.json

It imports only Python's standard library and reads the frozen phase33 voltage JSON. It independently reconstructs the integer representatives and underlying group, verifies all generators are involutions, checks every Schreier vector against the integral basis, and refuses to overwrite existing evidence. The report binds its exact source and data hashes. The discovery probe is not a proof input and is excluded from the export package.

The finite calculation is exhaustive for the one fixed integral representation. The passage to every modulus is the elementary uniform argument in §3. The previously reviewed phase33 theorem supplies IP, typed coset Helly and the exact toroidal residues for every modulus; those geometric facts are not recomputed here.

For example \(G_1\) and \(G_2\) have orders 1296 and 82944. The source's universal presentation can be larger than these quotients, and the separately proved universal object is infinite whenever \(6\mid s\). This supplement gives no universal-group order formula, no odd-parameter family, no external peer review, and no new priority claim.
