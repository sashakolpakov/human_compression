# Kernel transport for chiral regular covers

Private source adapter, 10 October 2026. This is a new application of the common kernel theorem, not a claim that the theorem or the chiral-cover criterion is new. It covers the proved conclusions in Gabe Cunningham, *Chiral polytopes whose smallest regular cover is a polytope*, subject to the older geometric and classification inputs specified below. The finite example is charged separately to the accompanying exact GAP computation. The conjectures in the source are not proved here.

The source is published in *Journal of Combinatorial Theory, Series A* **204** (May 2024), article 105839, DOI [10.1016/j.jcta.2023.105839](https://doi.org/10.1016/j.jcta.2023.105839). Our complete reading is of the [author manuscript](https://gabrielcunningham.com/WhichChiralPolytopes.pdf), headed 25 July 2023. The full publisher version was not acquired; the publisher's indexed abstract, main theorem and acknowledgements were checked. Consequently the contract is an author-version contract with publication metadata confirmed, not a claim of bytewise equivalence to the version of record.

## 1. Common theorem and geometric input

**Kernel transport K.** Let \(\pi:H\to G\) be a group homomorphism and let \(C\le A\cap B\le H\). Suppose
\[
 \pi(A)\cap\pi(B)=\pi(C).
\]
Then
\[
 A\cap B=C\quad\Longleftrightarrow\quad
 A\cap B\cap\ker\pi\le C.                         \tag{K}
\]
**Proof.** The forward implication is immediate. For the reverse implication take \(x\in A\cap B\). The image hypothesis gives \(c\in C\) with \(\pi(c)=\pi(x)\). Thus \(xc^{-1}\in A\cap B\cap\ker\pi\le C\), and hence \(x\in C\). This proves the assertion. No finiteness, centrality, or surjectivity assumption is needed. This is the theorem already formalized as `LeemansLift.intersection_of_image_and_kernel` in `formal/LiftCertificate.lean`.

We retain the following standard geometric correspondence, with its actual scope. Set
\[
 W_n=\langle r_0,\ldots,r_{n-1}\mid r_i^2=1,
 [r_i,r_j]=1\ (|i-j|>1)\rangle,
 \qquad U_n=W_n^+=\langle s_1,\ldots,s_{n-1}\rangle,
 \quad s_i=r_{i-1}r_i.
\]
The presentation of \(U_n\) has relations \((s_i\cdots s_j)^2=1\) for \(i<j\). Marked quotients of \(U_n\) satisfying the string \(C^+\) intersection property correspond to chiral or directly regular polytopes. Recursively, a marked quotient of rank at least three is such a group precisely when its facet and vertex-figure subgroups are such groups and their intersection is the medial subgroup. Rank two starts with a nontrivial cyclic group, including the infinite cyclic group; rank one has trivial rotation group. Direct regularity is equivalent to existence of the automorphism induced by conjugation with \(r_0\). Marked epimorphisms correspond to covers. The analogous quotients without the intersection property describe the relevant oriented maniplexes. This standard correspondence is retained, not proved by K.

We also retain the geometric section theorem: the facets of facets and the vertex-figures of vertex-figures of a chiral polytope are directly regular. This is the Schulte–Weiss result cited as Proposition 9 in the source. All sections of a directly regular polytope are directly regular. These are the only geometric ingredients needed to remove the local polytopality assumptions in the main criterion. In particular, we do **not** retain the target's Proposition 2.2 or Theorem 3.1 as background.

## 2. Mirror, mix, and local kernels

Write an oriented polytope group as \(\Gamma=U_n/N\). Conjugation by \(r_0\) induces the involutory automorphism \(\mu\) of \(U_n\) given by
\[
 \mu(s_1)=s_1^{-1},\qquad \mu(s_2)=s_1^2s_2,
 \qquad \mu(s_i)=s_i\quad(i>2).
\]
Put \(\overline N=\mu(N)\), \(\overline\Gamma=U_n/\overline N\), and
\[
 \Lambda=\operatorname{im}\bigl(U_n\longrightarrow
             \Gamma\times\overline\Gamma\bigr).
\]
This is the marked mix: its generators are the pairs of corresponding generators. It is \(U_n/(N\cap\overline N)\). The isomorphism \(\overline\Gamma\to\Gamma\), induced by \(\mu\), identifies its marking with
\((\sigma_1^{-1},\sigma_1^2\sigma_2,\sigma_3,\ldots)\).

**Universal cover assertion.** \(\Lambda\) is the rotation group of the smallest regular maniplex covering the given oriented polytope.

**Proof.** Its relation kernel \(N\cap\overline N\) is \(\mu\)-invariant and contained in \(N\), so it is a regular cover. If a regular marked quotient \(U_n/J\) covers \(\Gamma\), then \(J\le N\) and \(\mu(J)=J\), whence \(J\le\overline N\). Thus \(J\le N\cap\overline N\), giving the asserted factorization. This proves smallestness in the marked cover order. A regular cover of a chiral polytope is orientable: pull back the two-coloring of its flag graph. Thus the argument includes all regular polytope covers of interest.

Define the chirality subgroup by
\[
 X(\Gamma)=(N\overline N)/N\le U_n/N.
\]
It is trivial exactly when \(N=\overline N\), equivalently when the oriented object is directly regular. The product \(N\overline N\) is the least \(\mu\)-invariant normal subgroup containing \(N\).

**Kernel identity.** Under the first-coordinate identification,
\[
 X(\Gamma)=\{g\in\Gamma:(g,1)\in\Lambda\}.             \tag{1}
\]
**Proof.** Elements in the right side are exactly images in \(U_n/N\) of words in \(\overline N\). Their image is \(N\overline N/N\). This proves the identity and the chirality interpretation without any counting argument.

Let \(A=\Lambda_{n-1}\), \(B=\Lambda_0\), and \(C=\Lambda_{0,n-1}\) denote the subgroups generated respectively by the first \(n-2\), last \(n-2\), and middle \(n-3\) paired generators. Let \(K,L,M\) be the correspondingly marked facet, vertex-figure, and medial section of the original polytope. For \(\pi:\Lambda\to\overline\Gamma\), the identities needed below are
\[
 A\cap\ker\pi=X(K)\times1,\quad
 B\cap\ker\pi=X(L)\times1,\quad
 C\cap\ker\pi=X(M)\times1.                       \tag{2}
\]
Here the chirality groups are embedded in the **same** ambient first factor \(\Gamma\) with its fixed base flag. Merely knowing their abstract isomorphism types is insufficient.

For clarity, the local mirror convention in (2) is not an unmentioned automorphism of a chiral group. On the facet universal subgroup, \(\mu\) is precisely its intrinsic mirror. On the vertex universal subgroup generated by \(s_2,\ldots,s_{n-1}\), the intrinsic mirror is conjugation by \(r_1\). Since \(r_0=s_1r_1\), global conjugation by \(r_0\) is intrinsic conjugation by \(r_1\), followed by conjugation by \(s_1\). Conjugating the second coordinate by the image of \(s_1^{-1}\) therefore identifies the local paired subgroup with the intrinsic mirror mix, without changing its first-coordinate kernel. The same argument applies to the medial subgroup. Formula (1), applied to those local universal subgroups, proves (2). It also identifies the end subgroups of \(\Lambda\) with the smallest regular covers of \(K\) and \(L\).

## 3. One-line criterion and its local prerequisites

**Lemma 3.1 (regular end).** An oriented rotary polytope having directly regular facets or directly regular vertex-figures has a polytopal smallest regular cover.

**Proof.** Induct on rank; the polygon and directly regular cases are immediate. Suppose the facets \(K\) are directly regular. Their mixes are graph subgroups and hence are isomorphic marked copies of their rotation groups, so \(A\) is polytopal and \(A\cap\ker\pi=1\). A vertex-figure \(L\) has directly regular facets, since these are vertex-figures of \(K\); by induction its mirror mix \(B\) is polytopal. The original mirrored polytope has the intersection property, giving \(\pi(A)\cap\pi(B)=\pi(C)\). The kernel condition in K is automatic because \(A\cap\ker\pi=1\). Hence \(A\cap B=C\), and the recursive correspondence gives polytopality of \(\Lambda\). Duality handles directly regular vertex-figures. This proves, rather than imports, source Proposition 2.2.

For an arbitrary chiral polytope, the two end groups \(A,B\) are polytopal: apply Lemma 3.1 to its facets and vertex-figures using the depth-two regularity theorem. It follows that \(\Lambda\) is polytopal exactly when \(A\cap B=C\). This proves source Proposition 2.3, including its local prerequisites.

**Theorem 3.2 (chiral-cover adapter).** For a chiral polytope \(P\) with compatibly marked sections \(K,L,M\),
\[
 \text{the smallest regular cover of }P\text{ is polytopal}
 \quad\Longleftrightarrow\quad X(K)\cap X(L)\le X(M).       \tag{3}
\]
**Proof.** The mirrored polytope gives \(\pi(A)\cap\pi(B)=\pi(C)\). By (2), the kernel condition in K is exactly \(X(K)\cap X(L)\le X(M)\). The preceding paragraph converts \(A\cap B=C\) into polytopality. This proves both directions of source Theorem 3.1.

The following consequences contain all the general conclusions in its Section 3.

1. If either end section is regular, its chirality subgroup is trivial, and (3) holds. This recovers Remark 3.2 consistently with Lemma 3.1.
2. If the medial section is regular, its chirality subgroup is trivial, so the criterion is \(X(K)\cap X(L)=1\). Since this intersection already lies in \(\Gamma_{n-1}\cap\Gamma_0=\Gamma_{0,n-1}\), this is exactly Corollary 3.3's condition that its intersection with the medial subgroup is trivial.
3. In rank four the medial section is a polygon and its group is \(\langle\sigma_2\rangle\). Thus the criterion says that \(X(K)\cap X(L)\) contains no **nonidentity** power of \(\sigma_2\). This is the logically correct reading of Corollary 3.4; the identity belongs to every subgroup.
4. If the facet and vertex-figure are totally chiral, their chirality groups are their full rotation groups. Their intersection is \(\Gamma_{0,n-1}\), so (3) holds precisely when \(X(M)=\Gamma_{0,n-1}\), which is total chirality of \(M\). This proves Proposition 3.6.
5. Suppose a chiral facet \(K\) satisfies \(X(K)\cap\Gamma_0(K)=1\). In every chiral extension having these facets, the intersection \(X(K)\cap X(L)\) lies in \(X(K)\cap\Gamma_{0,n-1}=X(K)\cap\Gamma_0(K)=1\). This proves Corollary 3.7 for every such extension, without assuming the existence of extensions of arbitrary rank.

## 4. The two infinite-family applications and their exact retained cost

**Square torus maps.** For the chiral maps \(\{4,4\}_{(b,c)}\) in the standard square-torus parametrization (the source writes \(bc(b-c)\ne0\) with the usual parameter conventions), use the usual lattice quotient of the square tessellation. Its oriented marked group has the affine model
\[
 \bigl(\mathbb Z[i]/(b+ic)\bigr)\rtimes\langle i\rangle,
 \qquad u:z\mapsto iz,\quad v:z\mapsto iz+1.
\]
The identification with the torus map is the retained standard tessellation model; it is not a new classification of toroidal maps. The indicated affine maps generate the translations and quarter-turn, and \((uv)^2=1\). In the abstract semidirect product the linear-part map \(\ell\) onto \(C_4\) sends both \(u,v\) to \(i\). Both generators have exact order four: their fourth powers vanish and their linear parts have order four.

The mirror sends \((u,v)\) to \((u^{-1},u^2v)\), whose linear parts are both \(i^{-1}\). Thus \(\ell\mu\) is inversion composed with \(\ell\) on the universal marked group. Its relation kernel and its mirror both lie in \(\ker\ell\); consequently \(X(K)\le\ker\ell\). But \(\ell\) is injective on \(\langle v\rangle\). Hence \(X(K)\cap\langle v\rangle=1\), and consequence 5 proves Example 3.8. This argument only uses a regular **marked quotient** \(C_4\); it does not need the one-cell quotient map \(\{4,4\}_{(1,0)}\) to satisfy the abstract-polytope axioms. Negative or noncanonical integer parameters are not silently added to the source's chiral-map assertion.

**Five tight families.** Here the retained input is substantial and explicit. Cunningham–Pellicer, *Tight chiral polytopes*, J. Algebraic Combin. **54** (2021), 837–878, [DOI](https://doi.org/10.1007/s10801-021-01023-z), constructs the five chiral-facet/chiral-vertex rows of its Table 4. Its published Proposition 11 is cited by the target; the checked [arXiv author version](https://arxiv.org/pdf/2009.04566) calls the corresponding result Proposition 4.2 (printed page 20). For an atomic tight chiral rank-four polytope with both ends chiral it gives
\[
 X(P)=\langle\sigma_2^{q'}\rangle,\qquad q/q'\text{ prime},
 \qquad X(K)=X(L)=X(P)
\]
as embedded subgroups. Although part (b)'s sentence uses “isomorphic”, its proof and the immediately following arguments identify these embedded groups. Alternatively, local chirality is contained in global chirality by (2), and its nontriviality together with global prime order gives equality. Thus no inference from abstract isomorphism alone is being made.

The retained families and the resulting nonidentity obstruction are:

| Type | Parameter range and choices in the classified family | Element in both local chirality subgroups |
|---|---|---|
| \(\{2m,m^\alpha,2m\}\) | \(m\) odd prime, \(\alpha\ge2\), \(1\le k\le m-1\) | \(\sigma_2^{m^{\alpha-1}}\), order \(m\) |
| \(\{8,2^\beta,8\}\) | \(\beta\ge5\), \(\epsilon_1,\epsilon_2\in\{\pm1\}\) | \(\sigma_2^{2^{\beta-1}}\), order 2 |
| \(\{2^{\beta-1},2^\beta,2^{\beta-1}\}\) | same \(\beta,\epsilon_1,\epsilon_2\) range | same |
| \(\{8,2^\beta,2^{\beta-1}\}\) | same range | same |
| \(\{2^{\beta-1},2^\beta,8\}\) | same range | same |

The parameters refer to the marked groups in that table, not to every polytope sharing the same Schläfli type. Existence, atomicity and the chirality statement are retained from that older work; none of its all-parameter classification is replaced by sampling. The displayed obstruction and consequence 3 immediately prove the target's Example 3.5 for every parameter in those families. The classification of all tight chiral polytopes is neither a new target nor claimed as compressed here.

## 5. Two distinct minimal regular polytope covers

Use \(a,b,c\) for the three rotation generators and impose
\[
 (ab)^2=(bc)^2=(abc)^2=1.                         \tag{4}
\]
Let \(P\) be given by (4) together with
\[
 a^6=b^9=c^6=1,\quad ba^2=a^2b^4,\quad c^2b=b^4c^2. \tag{5}
\]
Let \(T\) be given by (4) and
\[
 a^6=b^9=c^2=1,\quad (ab^{-2})^2=1,
 \quad ab^2a(ab^{-1}a)^2=1,                         \tag{6}
\]
and let \(T^\delta\) be given by (4) and
\[
 a^2=b^9=c^6=1,\quad(c^{-1}b^2)^2=1,
 \quad bc^2b(c^{-1}bc^{-1})^2=1.                    \tag{7}
\]
These are the three literal presentations in the source, not extra quotients chosen to fit its order claims. Put
\[
 R=P\diamond\overline P,\qquad Q=R\diamond T,
 \qquad Q'=R\diamond T^\delta,
\]
where the mirror marking is \((a^{-1},a^2b,c)\).

The accompanying `phase41_chiral_cover_check.g`, replayed by `phase41_chiral_cover_check.py`, starts from the bare finitely presented groups (5)–(7), obtains GAP isomorphisms to finite permutation groups, and constructs every mix as the subgroup generated by paired generators in a direct product. Exact GAP group algorithms are retained for this finite proof. RAMP, a group catalogue, random sampling, and the source's output are not dependencies. The checker asserts the following full table; all orders are rotation-group orders.

| Group | Order | Orders of \(a,b,c\) | Facet, vertex orders | End intersection | Mirror automorphism |
|---|---:|---|---|---:|---|
| \(P\) | 324 | 6,9,6 | 54,54 | 9 | no |
| \(T\) | 324 | 6,9,2 | 162,18 | 9 | yes |
| \(T^\delta\) | 324 | 2,9,6 | 18,162 | 9 | yes |
| \(R\) | 972 | 6,9,6 | 162,162 | 27 | yes |
| \(Q\) | 2916 | 6,9,6 | 162,162 | 9 | yes |
| \(Q'\) | 2916 | 6,9,6 | 162,162 | 9 | yes |

In each row \(\langle b\rangle\) has order nine, \(\langle a\rangle\cap\langle b\rangle=\langle b\rangle\cap\langle c\rangle=1\), and (4) holds. The check tests subgroup equality, not merely numerical resemblance, for the successful end intersections. Thus the retained \(C^+\) correspondence proves that \(P\) is chiral, \(T,T^\delta,Q,Q'\) are directly regular polytopes, and \(R\) is not a polytope. The mirror maps are verified automorphisms; chirality of \(P\) is verified by the failure of the specified generator assignment to define a homomorphism.

The first-coordinate images of the second-projection kernels in the two end subgroups are both exactly \(\langle b^3\rangle\le\Gamma(P)\), of order three, as the checker also asserts. Thus K identifies the same nonpolytopality obstruction directly: the medial polygon has trivial chirality while its nonidentity element \(b^3\) lies in both end chirality groups.

The checker additionally verifies the marked facet isomorphism between \(T\) and \(R\), and the dual isomorphism \((a,b,c)_T\mapsto(c^{-1},b^{-1},a^{-1})_{T^\delta}\). Since \(T\) has two facets, it is the trivial extension of that facet in the source's sense. The maps \(R\to P\), \(Q\to R\), and \(Q'\to R\) are marked epimorphisms, each with kernel order three. Multiplying rotation orders by two gives exactly the source's 648, 1944, and 5832 flags.

For nonisomorphism there is an explicit short certificate:
\[
 w=(bc^{-1})^2ac^2a^{-1},\qquad
 \operatorname{ord}_Q(w)=1,\quad\operatorname{ord}_{Q'}(w)=3.       \tag{8}
\]
Hence the marked relation kernels differ. An isomorphism of regular polytopes can be composed with a target automorphism to match any chosen base flags, and would then preserve their marked relations. Therefore (8) excludes an unbased polytope isomorphism as well. This assertion concerns isomorphisms preserving face ranks; it does not assert nonduality.

**Minimality proof.** Any regular polytope cover of \(P\) factors through its smallest regular maniplex \(R\), by Section 2. An intermediate regular polytope between \(Q\) and \(P\) therefore gives an intermediate quotient between \(Q\) and \(R\). The latter map has prime degree three, so its kernel has no intermediate subgroup: the quotient is \(Q\) or \(R\). The second is not a polytope, so \(Q\) is minimal. The same argument proves minimality of \(Q'\). Equation (8) proves there are at least two different minimal regular polytope covers. This establishes every numerical and structural assertion about the example in source Section 4.

More generally, if the smallest regular maniplex is polytopal, its universal property makes it the unique minimal regular polytope cover. This implication requires no finite hypothesis. Its converse, and the proposed analogous multiplicity for all five tight families, are **not** consequences of K or of this finite example.

## 6. Relation to the 2025 general mix criterion and current boundaries

Cunningham–Hubard, *Polytopality criteria for the mix of polytopes and maniplexes*, [arXiv:2506.19334](https://arxiv.org/abs/2506.19334), explicitly recovers this chiral criterion in Corollary 6.17. Its Theorem 6.3 treats a polytope mixed with a premaniplex under the stated symmetry-type admissibility hypotheses: local facet and vertex-figure mixes must be polytopal, and a variance-group intersection inclusion must hold at every relevant flag. Section transitivity can reduce the multiple flag checks. The two-orbit specialization has additional hypotheses, including medial-section transitivity and the specified orbit class with the two end colors excluded. Chiral polytopes satisfy that specialization. Thus the later paper already records the extension; no priority or novelty claim is made here.

Both criteria express the obstruction to polytopality of a specified smallest mixed cover. Neither, by itself, constructs or classifies larger minimal regular polytope covers when that cover fails the intersection condition. Section 5 adds precisely such a construction in one finite case. It does not turn the 2025 criterion into a solution of the target's Section 4 conjectures.

As of 10 October 2026, the arXiv record for 2506.19334 shows only v1, submitted 24 June 2025, and no journal reference. This is a statement about the checked primary record, not a claim that no other publication exists. A bounded current search for the chiral unique/multiple-minimal-cover question, inspection of the full 2025 paper's concluding questions, and a text search of Hubard–Schulte's 2026 *Two-Orbit Polytopes* did not locate a resolution of the two multiplicity conjectures. That absence is not a proof of their current open status. We leave them unproved and make no novelty claim about them.

## 7. Version corrections and compression claim

The source extraction prints “no power” in Corollary 3.4 and Example 3.8; this manuscript explicitly says “no nonidentity power”. Definition 2.1's extracted rank-one base case is incompatible with the displayed \(U_1\); we use the standard rank-two cyclic base case. The source's unconditional wording for a mix “polytope” is read as a mix object, which is polytopal only after checking the intersection property. Lost overbars in web extraction are restored using the universal mirror convention, not interpreted as equality of marked copies. The publisher acknowledgement mentions an earlier error in Corollary 3.3; we use and prove the author version's stated condition through (3), and do not certify the text of an unacquired publisher PDF.

The mathematical reduction is genuine: one proved homomorphism theorem supplies the common intersection step; the regular-end induction, universal-kernel identity, torus argument, older classified-family input, and finite calculation account explicitly for every other obligation. This adds one conditional source adapter to the existing framework. It is not a claim of a quantitative compression ratio, a replacement of the older tight-family classification, a proof of the conjectures, or a new Lean formalization of all geometric conclusions.
