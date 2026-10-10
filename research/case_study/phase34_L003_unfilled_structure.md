# A free quotient inside the unfilled hexagonal group

Private structural result, 10 October 2026. The group in this note is rotational, and its final torus relation is **omitted**. The result does not assert anything about an individual odd source parameter.

## 1. Source and statement

Let $P_{\mathrm{omit}}$ be the group on $x,y,z$ with the nine relators

$$
\begin{gathered}
x^6,\quad y^3,\quad z^2,\quad(zx)^3,\quad(zy)^6,\quad(x^{-1}y)^2,\\
(y^{-1}x^{-2})^3,\quad(zx^3)^2,\\
\bigl(x^{-1}z(y^{-1}z)^2\bigr)\bigl(zx(zy)^2\bigr).
\end{gathered} \tag{1}
$$

Put $T=y(zy)^2$. Adding $T^s=1$ gives the rotational presentation $P_s$ associated with parameters $((3,0),(2,0),(1,1),(s,0))$ in Fernandes–Leemans–Ivić Weiss, [*Hexagonal extensions of toroidal maps and hypermaps*](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf), internal pages 17–19, Table 8 and Problem 9.2. This identification is with a presentation; it does not by itself identify a faithful geometry or its residues. The selected source presentation and problem were reread; there is no new complete-paper reading or priority claim.

**Theorem.** The group $P_{\mathrm{omit}}$ has a subgroup of index $648$ that maps onto the rank-two free group. In particular, $P_{\mathrm{omit}}$ is large, contains a rank-two free subgroup, and is not virtually solvable. It also has an explicit integral block-monomial representation of dimension $1296$ whose image contains a rank-two free subgroup.

The certificate below proves the index and free quotient directly. It does not require trusting a computed Reidemeister–Schreier presentation, Tietze transformations, a nilpotent quotient, or a finite-group identification.

## 2. Nonabelian voltage certificate

Let $F=F(u,v)$ be the free group, represented by freely reduced words in $1,-1,2,-2$. The literal file [phase34_L003_free_voltage_data.json](phase34_L003_free_voltage_data.json) contains three permutations $p_x,p_y,p_z$ of $\Omega=\{1,\ldots,648\}$ and three functions $w_a:\Omega\to F$. Every edge word has length at most four. Define right actions on $\Omega\times F$ by

$$
(i,f)^a=(p_a(i),f w_a(i)). \tag{2}
$$

The inverse of this bijection sends $(i,f)$ to

$$
\bigl(p_a^{-1}(i),f w_a(p_a^{-1}(i))^{-1}\bigr).
$$

Consequently a word acts trivially if and only if it fixes every base state and has trivial free-word voltage at every state. The standard-library checker [phase34_L003_free_voltage_check.py](phase34_L003_free_voltage_check.py) builds the nine words (1) directly, including their inverses, and verifies all $9\cdot648=5832$ identities by literal free reduction. It also checks that the base permutations are bijections and their generated action is transitive. Thus (2) gives an action of $P_{\mathrm{omit}}$, and the stabilizer $H$ of the base state $1$ has index exactly $648$.

For $h\in H$, let $\phi(h)$ be its voltage at state $1$. The action law gives $\phi(hk)=\phi(h)\phi(k)$, so this is a homomorphism $H\to F$.

The certificate contains, among 151 checked closed words, the following two short witnesses:

$$
\begin{aligned}
w_u&=z y^2 z y z^{-1}y^{-1}z^{-1}y^{-2},\\
w_v&=x z x^2 y x z^{-1}x^{-1}y^{-1}z^{-1}.
\end{aligned} \tag{3}
$$

Both fix state $1$, and their voltages are respectively $u$ and $v$. Hence $\phi$ is onto. Conversely, the homomorphism $F\to H$ sending $u,v$ to $w_u,w_v$ has composite with $\phi$ equal to the identity of $F$. It is therefore injective. This proves both the free-quotient and free-subgroup statements.

A quotient of a virtually solvable group is virtually solvable, and so is every subgroup of such a group. The rank-two free group is not virtually solvable: a finite-index subgroup is again free of rank at least two. Thus the theorem also excludes every virtually solvable model for $P_{\mathrm{omit}}$ itself. It does not exclude solvable images, including the previously constructed abelian-voltage images.

## 3. An explicit arithmetic image

For completeness the same data provide actual integer matrices, rather than only an action on an infinite set. Represent the two free letters by

$$
U=\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad
V=\begin{pmatrix}1&0\\2&1\end{pmatrix}. \tag{4}
$$

These matrices freely generate: on the projective line, nonzero powers of $U$ take $\{|t|<1\}$ into $\{|t|>1\}$, and nonzero powers of $V$ take the latter set into the former. Indeed their transformations are $t\mapsto t+2n$ and $t\mapsto t/(2nt+1)$. The elementary ping-pong argument applies. This is the usual classical free-matrix construction, not a new representation theorem.

On a direct sum of $648$ copies of $\mathbb Z^2$, place the matrix word $w_a(i)(U,V)$ in block $(i,p_a(i))$ and zero elsewhere, using row-vector convention. These are invertible $1296\times1296$ integer matrices. The checks from §2 prove all nine relator matrices equal the identity. Words (3) preserve block $1$ and act on it as $U,V$; the subgroup they generate in this matrix image is therefore free.

No faithfulness of this representation of $P_{\mathrm{omit}}$ is claimed. Its dimension is moderate relative to the certificate, but it is not the sought compact three-factor model. The proof of the theorem rests on free words, independently of the optional matrix realization.

## 4. Why this does not yet supply odd parameters

The base permutation of $T$ has order two: the checker verifies its square fixes every state, while the literal data give $1^T=251$. Its square has nontrivial free-word voltage at 432 of the 648 states, including individual free generators and their conjugates. In particular, $T$ has infinite order in this image.

Every construction that retains this base action must give $T$ even order or infinite order. Merely reducing the matrix coefficients modulo an integer retains the block permutation and cannot directly produce an odd parameter. An odd-parameter construction must change or further collapse the base action while preserving the required local groups and geometric conditions.

Largeness alone does not solve that relative quotient problem. It supplies many finite quotients of a finite-index subgroup, but it does not ensure an extension to the whole group with prescribed $T$ order, faithful fixed parabolics, subgroup intersection property, or typed coset Helly. None of those conditions is silently inferred here.

The existing even family and the separate multiples-of-three construction remain distinct results. In particular the present theorem makes no claim for every $P_s$, for odd $s$ coprime to six, for the orders of universal groups, or for a complete answer to Problem 9.2.

## 5. Discovery and structural leads

The discovery began with the parameter-two quotient and a reduced Reidemeister–Schreier presentation for its index-$648$ kernel in $P_{\mathrm{omit}}$. GAP simplified that presentation to nine generators and 88 relators. Its computed abelianization was $\mathbb Z^6\oplus C_3^3$; its class-two and class-three nilpotent quotients had Hirsch lengths 9 and 15. These are exploratory computations, not dependencies of §2.

In the nine-generator presentation, the assignment

$$
g_1,g_2\mapsto u^{-1}v^{-1},\quad g_5,g_6\mapsto u,\quad
g_8\mapsto v,\quad g_3,g_4,g_7,g_9\mapsto1
$$

annihilates all 88 relators. The finder [phase34_L003_free_voltage_find.g](phase34_L003_free_voltage_find.g) traces this assignment back through the subgroup rewriting and simplification, then exports the nonabelian edge voltages and original-word witnesses. The standalone verification of those exported data removes those discovery algorithms from the trust boundary.

A second exploratory calculation gave an index-three kernel, under $x,y\mapsto$ the same generator of $C_3$ and $z\mapsto1$, with a four-involution presentation. The source's small groups and free-rank sequence suggest examining triangle-group or central-product factors. These observations are leads only. In particular no isomorphism with a product of modular or triangle groups has been proved. Central extensions matter in the parameter-five example, so a naive wreath product should not be substituted for a verified marked model.

## 6. Reproduction and boundaries

Run in any directory with the three certificate files available:

```sh
python3 phase34_L003_free_voltage_check.py \
  --data phase34_L003_free_voltage_data.json \
  --output /tmp/L003-free-voltage-review.json
```

The checker refuses to overwrite an existing report. The saved report [phase34_L003_free_voltage_check.json](phase34_L003_free_voltage_check.json) binds exact data and checker hashes. Python's standard library suffices. The finder additionally needs GAP, but rerunning it is unnecessary to check the theorem.

This is a structural result about one explicitly presented group with a relator omitted. It is neither a finite census nor a new hypertope construction. Current bibliographic priority has not been established. No third-party article text or PDF is part of the original certificate package.
