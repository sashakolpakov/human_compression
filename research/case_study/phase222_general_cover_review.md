# Independent review: minimal regular covers in arbitrary finite rank

Review date: 10 October 2026. **Accepted independent written-proof review, with the exact formal limits below.**

The written argument in `phase216_general_covers.md`, Sections 1–5, together with `phase216_geometric_filling.md`, proves the following conclusion, subject to the retained primary theorems explicitly listed below:

> An abstract polytope of finite rank has a unique minimal regular polytopal cover if and only if its distinguished monodromy group is a string C-group. Every such polytope has a minimal regular polytopal cover.

The statement allows infinite polytopes and infinite covers. It does not prove that all the newly constructed covers, or the minimal covers lying below them, are finite. It does not prove infinitely many minimal covers in every negative case. The separately reviewed surface construction proves that stronger multiplicity conclusion for its stated families.

## 1. The exact cover problem and its algebraic interpretation

Cunningham–Pellicer, *Open problems on k-orbit polytopes*, Problem 5 on printed page 8 of the bound author manuscript dated 1 July 2018, asks whether a polytope whose monodromy is not a string C-group can nevertheless have a unique minimal regular polytopal cover. There is no finiteness restriction in that question. Proposition 3.1 on page 7 identifies rooted coverings with inclusion of flag stabilizers. Its preceding definition requires rank, incidence, and flag-adjacency preservation. These conventions exclude identifying a polytope with its dual by a rank-reversing map. The associated arXiv identifier is 1608.07993; the historical local filename `korbit2016v1.pdf` must not be used to infer the edition of its contents.

Here is the unbased-cover detail needed to use the normal-subgroup argument. Fix the universal string Coxeter group $W_n$, a flag $\Phi$ of $P$, its stabilizer $H$, and $K=\operatorname{core}_{W_n}(H)$. A regular polytope $R$ determines a normal subgroup $N\trianglelefteq W_n$: the stabilizer of any flag of $R$. Its normality makes this subgroup independent of the flag chosen. By Proposition 3.1, $R$ covers $P$ if and only if $N\leq H$, equivalently $N\leq K$. Conversely a normal $N\leq K$ with the intersection property yields the usual regular coset polytope and a covering of $P$. Nontriviality and distinctness of the distinguished involutions follow from $N\leq K$, since adjacent flags of an actual polytope differ in the indicated face.

Two rank-preservingly isomorphic regular polytopes have the same $N$: their isomorphism commutes with every coloured flag adjacency, and all their flag stabilizers coincide. Thus distinct normal subgroups here represent genuinely distinct isomorphism classes of regular polytopes, not alternative choices of base flags. For two regular covers, a covering exists precisely when their normal subgroups are ordered by inclusion. The statement about a unique maximal admissible subgroup therefore has exactly the unbased meaning required by the source question.

The use of arbitrary sets causes no class-size problem. All admissible subgroups belong to the powerset of the fixed group $W_n$. The trivial subgroup is admissible by the graph-product normal form, which gives $W_I\cap W_J=W_{I\cap J}$. A chain union preserves normality, containment in $K$, and every intersection witness: a relation modulo the union already holds modulo one member. Zorn therefore supplies maximal admissible subgroups, including one above every specified admissible subgroup. This is the earlier phase211 argument, not a new geometric theorem.

## 2. Splitting actual flag relations

The disjoint-support lemma is valid and uses more than an arbitrary string-generated quotient. If permutations induced by $a\in W_I$ and $b\in W_J$, $I\cap J=\varnothing$, are inverse, their common action fixes every rank coordinate. For a rank in $I$, use the inverse action of $b$; for a rank outside $I$, use $a$. Inverses preserve the same coordinate functions. A flag is determined by its faces, so the permutation is the identity. For several factors, isolate each factor using the inverse of the product of the others, or cyclically rotate the identity; no unmentioned commutativity assumption is needed for this lemma.

After cyclic reduction, the graph-product pure factors do commute, have disjoint supports, and correspond to the connected components of the induced noncommutation graph. In the universal string group those components are consecutive intervals. The flag lemma puts every factor back in $K$. A singleton factor would be a distinguished generator in $K$, which is impossible. Every remaining component has at least two letters and infinite order; all powers of a cyclically reduced full-support factor remain reduced. Consequently these interval-supported factors normally generate all of $K$. There is no finite-generation assumption.

## 3. The interval extension is exact

Adjoining a new end involution $t$ to a string C-group $H$, with only the required commuting relations, gives

\[
H*_{A}(A\times C_2),\qquad A=\langle s_0,\ldots,s_{d-2}\rangle.
\]

This is an identity of presentations. If $B=\langle s_1,\ldots,s_{d-1}\rangle$ and $C=A\cap B$, the subgroup generated by $B,t$ is $B*_{C}(C\times C_2)$. Indeed, each reduced alternating syllable from $B\setminus C$ lies outside $A$, so it remains reduced in the larger amalgam. The same normal form gives $H\cap\langle B,t\rangle=B$. Induction and the recursive string intersection criterion prove the extension lemma for finite or infinite groups. Reversing indices handles the other end. Thus the interval filling introduces no relations beyond the proposed power relation and the original string relations.

## 4. The factor system and the comparison of graphs

I checked BHS Definition 8.1 against the proposed collection of all nonempty-generator standard parabolic cosets. Single vertices are excluded and the threshold is $\xi=1$; a zero-diameter gate is allowed as the small-projection alternative. There are at most $2^{|S|}-1$ members through any vertex. Convexity is the usual graph-product gate property.

For two cosets, normalize a closest pair to $1,g$. BHS Lemmas 2.4 and 2.6 give a product bridge between their gate images. Its squares force every gate-edge label to belong to both generating subsets and to commute with, and differ from, every label of a shortest path from $1$ to $g$. Conversely those commutations construct the product strip for every word $h$ in that common link. Equivalently, $h\in V_I$, $gh\in gV_J$, and $d_1(h,gh)=|g|$, the minimal distance of the two cosets; hence $h$ is the gate of $gh$. Thus the gate image is exactly the stated parabolic subcomplex. This is a justified adaptation of the cubical proof underlying BHS Proposition 8.3, rather than treating its Artin-group statement as a Coxeter-group theorem without explanation.

A convex subcomplex parallel to a combinatorial hyperplane crosses exactly the same hyperplanes. The bridge gives the corresponding copy of its entire parabolic subcomplex, so all the nontrivial copies required by the factor-system definition are present. More generally, the union of a parallel class of $gX_I$ is exactly

\[
gV_{I\cup\operatorname{link}(I)}.
\]

For the reverse inclusion, translate a closest pair and use that the gate image is all of $X_I$; the separating path uses only common-link labels. The forward inclusion is the cubical product on $I$ and its common link. Connectedness of the noncommutation graph makes this a proper parabolic whenever $I$ is nonempty and proper. It likewise makes every hyperplane carrier, whose labels form a vertex star in the commutation graph, a proper parabolic coset.

These facts validate both metric estimates. The map $g\mapsto gH_s$ is exactly equivariant and changes distance by at most four per proper-parabolic edge. Conversely associate to an ordinary contact-graph vertex its carrier, and to a cone vertex the full parallel-class union just computed. These sets have diameter at most one in $Y=\operatorname{Cay}(V,\mathcal Q)$; consecutive sets intersect. A contact-graph path of length $k$ therefore gives a $Y$-path of length at most $k+1$. The coarse-surjectivity bound is two. The argument explicitly handles parallel classes and does not replace them by unjustified individual cosets.

BHS Proposition 8.25 and Corollary 14.5 now provide hyperbolicity and acylindricity. The transfer of acylindricity uses the displayed equivariant estimates directly, so it does not appeal to a general assertion that arbitrary quasi-isometries preserve actions. The Davis cubical action is proper, cocompact, and preserves this factor system; local finiteness follows from the finite generating set.

## 5. Full support remains loxodromic after coning

Chen–Heuer's centralizer theorem gives a common primitive cyclic centralizer for every nonzero power of the cyclically reduced full-support word. There is one pure factor and no common-link factor. Caprace–Fujiwara Corollary 4.6(ii) therefore gives rank one on the Davis complex, and Bestvina–Fujiwara Theorem 5.4 supplies a contracting CAT(0) axis. The right-angled Davis realization is the stated cubical CAT(0) realization, so no change of metric is hidden here.

The missing-label argument is uniform over all proper cosets. A chosen coset misses at least one generator $j$. Between $w^k$ and $w^l$, the reduced periodic path crosses at least $|k-l|$ distinct $j$-walls. None crosses the coset. Each separates one of the two orbit vertices from its chosen nearby coset vertex. The metric comparison $d_1\leq\sqrt{\dim X}\,d_2$ bounds the total by $2M_R$, independently of the coset or missing label. The period-to-axis error is also uniform. Hence the diameter of the axis within distance $R$ of any proper coset is uniformly bounded.

The projection argument uses precisely the conclusion available from BF Corollary 3.4: a sufficiently long contracting interval has a close pair with the segment joining points projecting to its endpoints. It does not assert that the whole joining segment stays near the interval. Applying this fact to two disjoint intervals at opposite ends of the projected segment produces two widely separated points of the axis near the convex coset. The preceding bound limits their separation. Subinterval contraction constants depend only on the axis constant; restriction of CAT(0) projection to a subinterval truncates its coordinate. This proves a uniform projection-diameter bound for every proper coset.

Each $\mathcal Q$-edge has bounded projected displacement, while $w^k$ has projected displacement $|k|\tau$. Thus $w$ is loxodromic on $Y$. This proves the missing geometric hypothesis for the filling theorem, rather than presuming it from rank one on a different space.

## 6. All large powers and the infinite set of protected elements

Hull Corollary 3.17 applies to the one-element collection $\{w\}$. It hyperbolically embeds $E_V(w)$ relative to this same generating set $\mathcal Q$; it does not replace that set by an uncontrolled enlargement. The acylindrical action supplies WPD.

DGO Lemma 6.5 and Corollary 6.6 say that every member of $E_V(w)$ conjugates some nonzero power of $w$ to itself or its inverse. It therefore normalizes the common cyclic centralizer $\langle u\rangle$, acting on $u$ by sign. Every subgroup $\langle w^m\rangle=\langle u^{em}\rangle$ is normal in $E_V(w)$, for every $m$. Properness of the relative metric means bounded relative balls are finite. For sufficiently large $m$, no nonidentity multiple $u^{emk}$ lies in the fixed finite forbidden ball. This is true for **all sufficiently large integers**, not just multiples of one special exponent.

DGO Theorem 7.15(c) gives injectivity on the entire relative generating set $\mathcal Q$. Since $\mathcal Q$ contains every element of every proper standard parabolic (and the identity), equality of two parabolic images implies equality of their representatives in $V$. All intersection identities therefore survive simultaneously. The elementary rank-two dihedral case is separate and valid. Combining this with the interval extension makes both normal closures of $w^m$ and $w^{m+1}$ admissible in the original $W_n$. They lie in $K$, and their join contains $w$. Normal generation from Section 2 gives the required join equal to $K$.

If there were a unique maximal admissible subgroup, the Zorn extension property would place every admissible subgroup inside it. The join computation would make it $K$, so the monodromy would be a string C-group. The converse is immediate from $K$ itself being admissible. This completes the proposed proof, with the precise cover interpretation established in Section 1.

## 7. Attribution, formal scope, and review status

The proof retains substantial geometric group theory: graph-product normal forms and centralizers; the Coxeter rank-one criterion; contraction of periodic rank-one axes; convex cubical bridges; factor systems, quasi-trees and acylindricity; hyperbolically embedded elementary subgroups; and Dehn filling. These are not newly proved by the project. The project contribution consists of the explicit parabolic-coset comparison and uniform projection argument, together with their application to actual flag kernels and coprime-power joins.

I read the complete written arguments and the precise primary interfaces. I also visually checked the original PDF pages for BHS Definitions 8.1 and 8.14 and Corollary 14.5, Hull Corollary 3.17, DGO Theorem 7.15, and BF Corollary 3.4. Requested clarifications concerned the proximity estimate, the elementary-subgroup citation, the identity in the generating set, and the source edition; all were incorporated before the author freeze. No mathematical gap remains in the reviewed argument.

This acceptance binds `phase216_export.json`, SHA256 `daba2e40dc03b5c7f6067e9ea938ff4e408d82d45e412b4ff9b72e70b0269f13`, and its fourteen files. In particular the main proof has SHA256 `99ebf6ee8f97c48d7a8e4565335057d7a44b0aae47bd95f1b6dad13743ef5494` and the geometric companion has SHA256 `ae5137decf572a4eabfd4e45642a56b036ccb206c879c3d7dfc95afbc0e7fa00`. The associated source-interface ledger records the retained and newly supplied steps individually.

I read both actual Lean sources, including their definitions. The five new phase216 theorems verify disjoint-coordinate permutation splitting; preservation of intersection identities from injectivity on the union of proper parabolics; the admissible-kernel join from normal generation and consecutive powers; and the two deductions from unique maximality. They use the six retained phase211 theorems for chains, Zorn, and coprime powers. Normal generation and the power supply are explicit hypotheses in this formal argument. The geometric proof establishes them on paper; neither is smuggled into Lean as an axiom.

A fresh independent execution under optimized Python, with primary verification enabled, passed in 8.84 seconds. All eight source PDF hashes were checked. The five new and six retained theorem reports contain only `propext`, `Classical.choice`, and `Quot.sound`. All three altered-proof controls were rejected. The independent review runner repeats those checks against the frozen bindings and additionally reconstructs four finite countermodels to dropping disjointness, dropping coordinate separation, replacing consecutive exponents by exponents differing by two, and dropping normal generation. These finite models explain why the hypotheses matter; they are not experimental evidence for the geometric theorem.

The complete geometric argument, its imported primary theorems, and the regular-polytope correspondence are **not formalized in Lean** by this packet. They receive a complete written mathematical review. This establishes the unrestricted finite-rank conclusion stated at the start, including the negative answer to Problem 5. It does not establish the finite-cover-only variant, infinitely many minimal covers in all cases, an effective filling exponent, a whole-paper compression ratio, or an exhaustive priority claim.
