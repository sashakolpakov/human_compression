# Recognizable extensions and finite incidence representations

This application gives a complete written deduction of the principal constructive results of Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel, *Every finite group is represented by a finite incidence geometry*, arXiv:2511.02410v2 (16 December 2025), inventory F010. The full thirteen-page primary text has been read; the arrow gadget, chamber completion, cleaning gadget, and both examples have also been checked against their original PDF figures. The finite-pair representation theorem is the authors' theorem, proved in 2025. It is not an open conjecture solved by this project.

The reusable ingredient is a restriction-and-extension criterion. Its group-theoretic content is elementary; the substantive work lies in recognizing the retained structure and proving that every new object is determined by it. We state that criterion once, then supply the local recognition arguments for all three constructions. The constructions themselves, including their explicit sizes and the symmetric-group family, are borrowed from F010. The present treatment makes their common proof mechanism explicit and corrects two numerical statements and one base-case qualification. Those corrections do not affect the main representation theorem.

## 1. The reconstruction criterion

A finite incidence system is a nonempty finite simple graph $X$ with a surjective proper coloring $t:X\to I$. Write $C(X)$ for the automorphisms of the graph which permute its color classes, and $K(X)$ for those which preserve each class. Thus $K(X)$ is the kernel of the induced action of $C(X)$ on $I$. An incidence geometry is an incidence system in which every clique is contained in a clique meeting every color class.

Suppose that a construction $X\mapsto Y$ retains a specified copy of $V(X)$ in $V(Y)$. The edges between retained vertices need not be retained.

**Lemma R.Reconstruction.** Assume the following.

1. Every member of $C(Y)$ preserves $V(X)$, and its restriction is a member of $C(X)$.
2. A member of $C(Y)$ fixing every vertex of $X$ fixes every vertex of $Y$.
3. Every member of $C(X)$ extends to a member of $C(Y)$.
4. An extension preserves every color of $Y$ if and only if its restriction preserves every color of $X$.

Then restriction is an isomorphism of pairs
\[
(C(Y),K(Y))\cong(C(X),K(X)).
\]

**Proof.** Restriction is a homomorphism by the first assumption. The second identifies its kernel with the identity subgroup, and the third makes it surjective. The fourth identifies the two distinguished kernels. The extension in the third assumption is automatically unique by the second. In particular, no separate compatibility calculation is needed to show that these unique extensions respect multiplication. ∎

This is an instance of the retained umbrella's action-kernel interface U.Action. That interface alone does not rule out additional automorphisms of a constructed graph: assumptions 1 and 2 pay for precisely that issue. In each application below we verify all four assumptions.

## 2. Encoding a finite group and a normal subgroup

**Theorem R.PairEncoding (F010, Theorem 3.1).** Let $G\ne1$ be finite and $H\lhd G$. There is a finite properly colored graph $X(G,H)$, of minimum degree at least two and with no triangles, such that
\[
(C(X(G,H)),K(X(G,H)))\cong(G,H).
\]

**Construction.** Enumerate $G=\{g_1=1,g_2,\ldots,g_q\}$. Begin with a vertex $P_x$ for each $x\in G$. The ordered pair $x\ne y$ has label $k$ when $yx^{-1}=g_k$. For each ordered pair introduce distinct vertices
\[
T_{x,y},\quad S_{x,y,0},\ldots,S_{x,y,k+2}.
\]
Vertices belonging to different ordered pairs are distinct. Suppressing the pair subscripts, add exactly the following edges:
\[
P_xS_0,\quad S_0P_y,\quad
S_iS_{i+1}\ (0\le i<k+2),\quad
P_xT,\quad TS_{k+2},\quad S_{k+2}P_y.
\tag{R1}
\]
There are no edges between the original vertices. Formula (R1) is the explicit edge list of the source's arrow diagram.

Color $P_x$ by its coset $xH$. Give all $T$-vertices one new color, the even-indexed $S$-vertices a second, and the odd-indexed $S$-vertices a third. These three colors are disjoint from $G/H$.

**Proof.** The coloring is proper: every edge joining an original vertex to a new vertex joins disjoint palettes, each $T$-to-$S$ edge does the same, and each successive pair of $S$-vertices has opposite index parity. The graph contains no triangle. Within one gadget the two short routes between its original endpoints have lengths two and three, while the remaining route uses the chain of length $k+2\ge4$. Distinct gadgets meet only at original vertices, and there is no edge between original vertices. These facts exclude a triangle both within a gadget and across gadgets.

The original vertices have degree $4(q-1)$, the vertices $S_0,S_{k+2}$ have degree three, and all remaining vertices have degree two. In particular the minimum degree is two and the original vertices are exactly those of degree at least four.

Let $f$ be any uncolored graph automorphism, and write $f(P_x)=P_{\rho(x)}$. For $x\ne y$, the vertex $T_{x,y}$ is the unique degree-two neighbor of $P_x$ whose distance from $P_y$ is two. Indeed the degree-two neighbors of $P_x$ are precisely the $T_{x,z}$, and the other neighbor of $T_{x,z}$ is $S_{x,z,k(z)+2}$, which is adjacent to the original vertex $P_z$ and to no other original vertex. Thus $f$ preserves the ordered-pair labeling of the $T$-vertices. Its unique degree-three neighbor determines the terminal $S_{x,y,k+2}$.

Starting from that terminal vertex, follow the maximal chains whose internal vertices have degree two. Exactly one ends at a degree-three vertex; the other such chain passes through $T$ and ends at an original vertex of degree at least four. The first chain is therefore intrinsically determined. Its other endpoint is the degree-three vertex $S_{x,y,0}$, and its length is $k+2$. Therefore $\rho$ preserves both the orientation and the label of every ordered pair. Conversely a permutation of the original vertices preserving all these labels extends uniquely by preserving every displayed gadget index. This is the recognition-and-extension argument underlying R.Reconstruction, before colors are introduced.

Preservation of labels says
\[
\rho(y)\rho(x)^{-1}=yx^{-1}\qquad(x\ne y).
\]
Taking $x=1$ proves $\rho(y)=y\rho(1)$ for every $y\ne1$, and the same formula holds at $y=1$. Hence the full uncolored automorphism group consists exactly of the right translations. To obtain a homomorphism with the usual left composition of permutations, use $g:P_x\mapsto P_{xg^{-1}}$, extending it to every gadget by the same right translation on its two indices.

Every such permutation fixes the three auxiliary colors. Since $H$ is normal, right translation permutes the cosets $xH$; thus every uncolored automorphism is a correlation. It fixes all coset colors if and only if $g\in H$: necessity follows from the coset of $1$, and normality gives sufficiency on every coset. This identifies the pair with $(G,H)$. ∎

If $q=|G|$, the uncolored graph has
\[
q+q\sum_{k=2}^{q}(k+4)
=\frac{q^3+9q^2-8q}{2}
\]
vertices. This size is a property of the borrowed construction, not an optimality assertion.

## 3. Completing edges to chambers

**Theorem R.ChamberCompletion (F010, Theorem 4.1).** Let $X$ be a finite properly colored triangle-free graph of minimum degree at least two. There is a finite incidence geometry $J(X)$, with the same palette, satisfying
\[
(C(J(X)),K(J(X)))\cong(C(X),K(X)).
\]

**Construction.** Put $r=|I|$. For each edge $e=\{v,w\}$ and every color $i\notin\{t(v),t(w)\}$, add a new vertex $u_{e,i}$ of color $i$. Make
\[
B_e=\{v,w\}\cup\{u_{e,i}:i\notin\{t(v),t(w)\}\}
\]
a complete graph. Add no other edges.

**Proof.** Each $B_e$ has exactly one vertex of each color. A clique containing a new vertex lies entirely in its $B_e$, since all neighbors of that vertex are there. A clique containing only original vertices has at most two vertices, by triangle-freeness, and hence is contained in some $B_e$: a singleton extends because its degree is positive, and a two-element clique already supplies the edge. The empty clique also extends because the graph has an edge. Thus every clique lies in a chamber.

A new vertex has degree $r-1$. An old vertex $v$ has degree
\[
\deg_{J(X)}(v)=\deg_X(v)(r-1).
\tag{R2}
\]
For different edges incident to $v$, the other $r-1$ vertices of their chambers are disjoint. Since $r\ge2$ and $\deg_X(v)\ge2$, precisely the old vertices have degree greater than $r-1$. The old induced graph is $X$, so every correlation restricts to a correlation of $X$.

If a correlation fixes all old vertices, surjectivity of the old coloring implies that it fixes every color. Every new vertex is then determined by its old endpoint pair and its color. Thus restriction is injective. If $f\in C(X)$ induces the palette permutation $\sigma$, the formula
\[
\widetilde f(u_{e,i})=u_{f(e),\sigma(i)}
\]
extends $f$, preserves every chamber, and hence preserves the graph in both directions. It fixes every color precisely when $f$ does. R.Reconstruction now applies. For $r=2$ the construction adds nothing, and the same argument remains valid. ∎

The source's proof writes the old and new degree bounds with an offset of one. Formula (R2) gives the actual graph degrees; the strict separation needed by the proof is unchanged. The construction has $|V(X)|+(r-2)|E(X)|$ vertices.

## 4. Removing the graph hypotheses without changing the pair

**Theorem R.Cleaning (F010, Theorem 4.2).** Every nonempty finite properly colored graph $X$ has a finite properly colored triangle-free graph $L(X)$, of minimum degree at least two, with the same correlation–automorphism pair.

**Construction.** Set
\[
M=\max_{i\in I}|t^{-1}(i)|,\qquad
W=\{v:\deg_X(v)\le1\},\qquad
q=|E(X)|+|W|.
\]
Then $M\ge1$ and $q\ge1$. For each edge $e$ and each vertex $w\in W$, introduce its own copy of the gadget with vertices $u_0,\ldots,u_{2M+4}$, chain edges $u_ju_{j+1}$, and two additional edges
\[
u_{2M+4}u_{2M-1},\qquad u_{2M+3}u_{2M}.
\tag{R3}
\]
Delete every old edge $\{v,w\}$ and join both its endpoints to the root $u_{e,0}$ of its edge gadget. For $w\in W$, join $w$ to $u_{w,0}$; if $w$ was isolated, also join it to $u_{w,2}$. Keep the old colors, and give even and odd gadget indices two distinct new colors $\alpha,\beta$.

**Proof.** All new edges either join an old color to a new one or join opposite index parities. The graph is properly colored. An old vertex of degree at least two retains that degree, a former leaf has degree two, and a former isolated vertex also has degree two. Every new vertex has degree at least two. No two old vertices are adjacent. The graph on the new vertices is bipartite, and a triangle involving an old vertex would require two of its new neighbors to be adjacent. The only old vertex with two neighbors in one gadget is a former isolated vertex, whose neighbors $u_0,u_2$ are not adjacent. Hence there are no triangles.

The two new color classes have sizes $q(M+3)$ and $q(M+2)$. They are different and both are larger than every old color class. Therefore every correlation fixes these two classes separately and preserves the old vertices. An old edge is recovered exactly as a pair of old vertices having a common new neighbor: such a neighbor is the root of their edge gadget, while the additional gadgets have only one old neighbor. Thus restriction is a correlation of $X$.

We next prove uniqueness of extension. Removing the old vertices leaves one connected component for each gadget. An edge gadget is identified by its two old neighbors. A gadget attached to a leaf or isolated vertex is identified by that old vertex, because there is exactly one such additional gadget there. Consequently a correlation fixing all old vertices preserves each gadget.

In every gadget the root $u_0$ is fixed. For an edge gadget or a former leaf, it is the unique vertex of that gadget adjacent to the old vertices. For an isolated old vertex, the two attachment vertices $u_0,u_2$ have different degrees: $u_0$ has degree two, while $u_2$ has degree at least three. Starting at $u_0$, successive vertices along the chain are forced until $u_{2M-1}$. At this branching vertex the two forward neighbors $u_{2M}$ and $u_{2M+4}$ have different degrees within the gadget, respectively three and two. At $u_{2M}$, the remaining two neighbors $u_{2M+1}$ and $u_{2M+3}$ likewise have degrees two and three. The last vertex $u_{2M+2}$ is then forced. These degree statements concern the induced gadget, so they remain true in the exceptional small case $M=1$, even when the isolated-vertex attachment increases a degree in the full graph. Thus the rooted gadget is rigid and restriction is injective.

Finally a correlation $f$ of $X$ preserves old degrees. Extend it by
\[
u_{e,j}\longmapsto u_{f(e),j},\qquad
u_{w,j}\longmapsto u_{f(w),j}.
\]
The edge list proves that this is a correlation. It fixes both new colors, and it fixes the old colors exactly when $f$ does. R.Reconstruction proves the assertion. ∎

This construction adds $q(2M+5)$ vertices. Applying R.ChamberCompletion to $L(X)$ proves the source's general conversion from arbitrary finite incidence systems to finite incidence geometries with the same pair.

**Corollary R.FinitePairs (F010, Theorem A).** Every finite pair $H\lhd G$ is the correlation–automorphism pair of a finite incidence geometry.

**Proof.** For $G\ne1$, apply R.PairEncoding and then R.ChamberCompletion. For $G=1$, use the rank-one geometry with one vertex; its two groups are trivial. ∎

## 5. The completed hexagon example

F010, Example 5.1 is the following graph. Number the vertices of a hexagon by $i\in\mathbb Z/6\mathbb Z$, color them by the parity of $i$, and add a third-colored tip on each edge $\{i,i+1\}$ with $i$ even. The three tips have degree two, and the six old vertices have degree three, so every correlation preserves the hexagon. Its permitted dihedral symmetries are the stabilizer of the alternating edge set. They form $S_3$, generated by $i\mapsto i+2$ and $i\mapsto1-i$. The first preserves the two old colors and the second exchanges them. Hence the pair is $(S_3,C_3)$, as in the source.

Now put a third-colored tip on all six edges. This is an incidence geometry: every edge belongs to its displayed triangle, each triangle has all three colors, and these are the maximal cliques. Its correlations form the full dihedral group of the hexagon, of order twelve. Its type-preserving subgroup has order six, not three. Indeed the rotations by even increments and the reflections $i\mapsto 2a-i$ preserve the parity classes. In particular
\[
i\longmapsto-i,\qquad
\text{tip on }\{i,i+1\}\longmapsto
\text{tip on }\{-i-1,-i\}
\tag{R4}
\]
is a nonidentity type-preserving involution.

Thus the completed pair is $(D_{12},S_3)$, where the subscript denotes the group order. The source prints $(D_{12},C_3)$. Formula (R4) corrects its second entry. The intended lesson remains valid: naive chamber completion can enlarge the correlation group when the triangle-free recognition argument is unavailable. The example by itself does not prove that every hypothesis of R.ChamberCompletion is necessary in every possible formulation.

## 6. The smaller symmetric-group family

We retain the more economical family of F010, Example 5.2, since its explicit construction is additional information not supplied by the mere existence theorem.

**Theorem R.SymmetricFamily.** For every $n\ge2$ there is a connected, properly colored, triangle-free graph $X_n$, with colors $0,\ldots,n$, such that
\[
(C(X_n),K(X_n))\cong(S_n,A_n).
\]
Its color classes satisfy
\[
|t^{-1}(n)|=n,\qquad
|t^{-1}(i)|=\frac{n!}{2(i-1)!}\quad(0\le i<n),
\tag{R5}
\]
where $(-1)!=0!=1$. The action on the $n$ vertices of color $n$ is the natural faithful $S_n$-action. For $n\ge3$, the minimum degree is at least two.

**Construction.** Let $X_2$ be the four-vertex path with successive colors $2,0,1,2$. Its two end vertices are labeled $1,2$. Suppose $X_{n-1}$ has been constructed, with its top vertices labeled $1,\ldots,n-1$. Introduce top vertices $v_1,\ldots,v_n$ of color $n$, and vertices $v_{\{i,j\}}$ of color $n-1$, with edges $v_i v_{\{i,j\}}$ and $v_j v_{\{i,j\}}$.

For each $j$, choose an even permutation $g_j\in A_n$ sending $n$ to $j$, with $g_n=1$. Attach a copy of $X_{n-1}$ at $j$, identifying its top vertex labeled $i$ with $v_{\{g_j(i),j\}}$. The internal vertices of distinct copies are disjoint. All lower colors are inherited. Such even permutations exist because $A_n$ is transitive for $n\ge3$.

**Proof.** The base path has precisely its identity and its reversal as correlations. Reversal exchanges colors zero and one, so its pair is $(S_2,A_2)$. The two endpoints have degree one; they are a pre-induction object, not an instance of the minimum-degree assertion.

The inductive graph is connected. Each attached copy is properly colored and triangle-free by induction. Copies meet only at top vertices of their own color $n-1$, which are pairwise nonadjacent. Every new top vertex has neighbors only of color $n-1$, also pairwise nonadjacent. Therefore no triangle is created. An internal vertex has the same degree as in its copy. A new top vertex has degree $n-1$, and a pair vertex receives its two new top neighbors and the neighbors contributed by its two attached copies. At $n=3$, only the pair vertices were endpoints of the base paths, and their new degree is four. All other vertices have degree two. For larger $n$, minimum degree two follows by induction.

There are $n$ top vertices and $\binom n2$ pair vertices. Each lower color occurs in $n$ disjoint copies of its previous class. These recurrences prove (R5).

We establish the claimed action, keeping track of its palette action. Given $\sigma\in S_n$, send $v_i$ to $v_{\sigma(i)}$ and $v_{\{i,j\}}$ to $v_{\{\sigma(i),\sigma(j)\}}$. On the copy at $j$, use the inductively available automorphism corresponding to
\[
h_{\sigma,j}=g_{\sigma(j)}^{-1}\sigma g_j,
\]
which fixes $n$ and hence is a permutation of the other $n-1$ labels. It has the same sign as $\sigma$, since both chosen representatives are even. By induction, an even permutation fixes every color of a copy and an odd permutation exchanges exactly colors zero and one. The local maps therefore have one consistent palette permutation on the whole graph. Their actions agree on every shared pair vertex, so they define a correlation. Moreover
\[
h_{\tau,\sigma(j)}h_{\sigma,j}=h_{\tau\sigma,j},
\]
and the inductive actions are homomorphisms. Consequently these correlations form an $S_n$-action extending the natural action on the top vertices, with type kernel $A_n$.

It remains to exclude additional correlations. For $n\ge4$, the top class is the unique smallest color class: its size is $n$, the next size is $\binom n2>n$, and all lower classes are larger. Thus every correlation preserves it. For $n=3$, all four classes have size three, but the top vertices are exactly the degree-two vertices whose two neighbors both have degree four. The other degree-two vertices have one neighbor of degree two and one of degree four. The top class is again intrinsic. The base case was already checked.

Suppose a correlation fixes all top vertices. Every pair vertex is characterized by its two top neighbors, so it fixes every pair vertex. We show that it then preserves each attached copy. The graph $X_m$ with its top vertices removed is connected for every $m\ge2$. For $m=2$ it is an edge. For $m\ge3$, it is the union of the $m$ copies of $X_{m-1}$; each is connected and each pair of copies has their common pair vertex, so their union is connected. Therefore, in $X_n$, deleting both the top and the pair vertices leaves exactly one connected component for each copy's interior. The boundary of the interior of the copy at $j$ is the star $\{v_{\{i,j\}}:i\ne j\}$. These stars are distinct for $n\ge3$. Since all pair vertices are fixed, every interior component is preserved.

Restriction to each attached copy is now a correlation fixing its top vertices. By inductive faithfulness it fixes the entire copy. Thus the original correlation is the identity. The full correlation group embeds in $S_n$, and the constructed action already gives all of $S_n$. Its palette kernel is precisely $A_n$, as proved above. ∎

For $n\ge3$, R.ChamberCompletion gives the source's corresponding $(S_n,A_n)$-geometries immediately. For $n=2$, one may first use R.Cleaning, or simply use the general finite-pair theorem. This states the base-case qualification explicitly instead of asserting minimum degree two for the four-vertex path.

## 7. Contract, attribution, and verification boundary

The written deductions above recover Theorems 3.1, 4.1, 4.2 and A, the explicit smaller symmetric-group family, and the intended obstruction in Example 5.1, with its second group corrected. All local recognition, extension, triangle-free, minimum-degree, and family-faithfulness arguments are included. The main finite-pair theorem and the three gadgets are attributed to Díaz Ramos, Molinier and Viruel; their discussion in turn credits earlier graph-representation constructions of Frucht and König. Our restriction-and-extension organization is a reusable proof interface, without a claim that the underlying elementary group principle is historically new.

The source's results are thereby candidates for a complete *written* principal contract, subject to independent review. This does not yet supply a fully Lean-checked replacement. The local corrected-example certificate, bounded graph checks, and the complete all-rank proofs must have separately stated scopes. No compression ratio is inferred from the source count, and no new open-conjecture resolution is claimed.
