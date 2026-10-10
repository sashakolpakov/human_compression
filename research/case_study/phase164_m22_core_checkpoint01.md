# M22 core checkpoint 01

Frozen author mathematics and census, pending independent review. This is not a complete L073 table replacement; §6.3 records the remaining obligations.

## 6. Primitive rank-three geometries of the Mathieu group

For the next application the object stabilizers, rather than the panel stabilizers, are maximal. The distinction permits a smaller recognition test. Let $G$ be finite and let $H_1,H_2,H_3$ be distinct maximal proper subgroups. Put $H_{ij}=H_i\cap H_j$ and $B=H_1\cap H_2\cap H_3$. For distinct $i,j$ define
\[
R_{ij}=\{H_i h:h\in H_j\}.
\]
These are precisely the $H_i$-cosets incident to the base object $H_j$.

**Corollary E.PrimitiveTriples.** The right-coset system of $H_1,H_2,H_3$ is flag-transitive and residually connected if and only if
\[
\begin{split}
H_i&=\langle H_{ij},H_{ik}\rangle\quad(i=1,2,3),\\
|R_{ij}\cap R_{ik}|&=[H_{jk}:B]
\end{split}\tag{E6}
\]
where the second equality need only be checked for one choice of $i$. Every such geometry is firm.

**Proof.** Every incident pair of right cosets has a common element. Right multiplication therefore makes $G$ transitive on the flags of each two-type combination. Fix the base pair $H_j,H_k$. Its possible $i$-type completions are the elements of $R_{ij}\cap R_{ik}$. The stabilizer $H_{jk}$ has an orbit of size $[H_{jk}:B]$ containing $H_i$. The equality in (E6) says precisely that this orbit is the entire completion set. Thus all chambers can be moved to the base chamber. Conversely, flag transitivity implies this equality. This is U.Helly in rank three, with a finite cardinality test for its common-element condition.

In the flag-transitive system, the residue at $H_i$ is the bipartite coset graph of $H_i$ on $H_{ij},H_{ik}$. A path is a successive multiplication by elements of those two subgroups, and every such product gives a path. Its connectedness is therefore equivalent to the corresponding generation equality. The whole geometry is connected because any two distinct maximal subgroups generate $G$. These are all the residual-connectedness conditions in rank three.

If a panel had only one completion, one of the groups $H_{jk}$ would equal $B$. The residue-generation equality at $H_j$ would then give
$H_j=\langle H_{ij},B\rangle=H_{ij}$, contrary to distinct maximality of $H_i,H_j$. Hence every panel has at least two completions. This also derives the firmness hypothesis of E.PanelRecognition in this application. ∎

### 6.1. Exhaustive augmentation and the equivalence relation

Let $\mathcal M$ be the complete set of maximal subgroups of $G$, and let $A=\operatorname{Aut}(G)$ act on it. Apply U.ExtensionOrbits first to pairs of distinct members of $\mathcal M$. One may fix a representative of each $A$-orbit of the first member and then take orbits of its stabilizer on the second members. Fuse the resulting unordered pairs under $A$. For each surviving pair $e$, take the orbits of its setwise stabilizer $A_e$ on $\mathcal M\setminus e$, attach one third member, and test (E6). Finally fuse accepted unordered triples under $A$.

Every triple has a distinguished pair. Moving that pair to its orbit representative and then using its stabilizer puts the third member in one of the tested positions. All tests are invariant under the action. Thus the search is exhaustive. Different choices of distinguished pair may give the same triple orbit, which is why the last fusion is necessary. Conversely every accepted triple satisfies the geometric recognition theorem. The equivalence being computed is full group-automorphism conjugacy together with arbitrary type reordering. No assertion that arbitrary incidence isomorphisms of every coset geometry lift to automorphisms of $G$ is needed.

The action may be replaced by its actual permutation image on $\mathcal M$: each image element has an automorphism lift, so its orbits and transporters give exactly the same equivalence. This matters for the catalogue model of $M_{22}$, which has two fixed points on a 24-point domain. Its ambient permutation normalizer has order $1\,774\,080$, while the centralizer of $G$ in that normalizer has order two. The conjugation image has order $887\,040$, equal to the order of the separately computed full automorphism group. Counting normalizer elements as distinct automorphisms would be unjustified; taking the image gives the correct action.

### 6.2. The finite census and its geometric realization

Take $G=M_{22}$. The retained TomLib subgroup catalogue has 156 conjugacy classes. Its maximal-class indices are independently compared with the maximal elements of the supplied subgroup-containment relation. There are eight maximal classes and 2,300 maximal subgroups. The independent-input search finds 81 unordered maximal-pair orbits and 431 accepted maximal-triple orbits. It tests 11,866 triples and accepts 1,193 before full automorphism fusion. No source geometry list, table row or anticipated count is an input.

**Corollary E.M22.** Conditional on the declared complete subgroup catalogue and exact finite-group algorithms, there are 81 rank-two and 431 rank-three flag-transitive residually connected geometries for $M_{22}$ with maximal object stabilizers, under the source's automorphism/type equivalence.

**Proof.** Two distinct maximal subgroups give a connected, firm, flag-transitive rank-two coset geometry: they generate $G$, and their intersection has index at least two in each. Corollary E.PrimitiveTriples gives exactly the rank-three test. The complete augmentation argument and its finite output prove exhaustion. The independent witnesses are checked again, including all three choices in the cardinality test, all residue-generation equalities and all panel indices. Exact orbit transporters prove inequivalence. ∎

The object names can also be recovered directly from the same subgroup action. Let $\Lambda$ be the 22 moved points and $p,q$ the fixed points. In source order the maximal classes have orders
\[
20\,160, 5\,760, 2\,520, 2\,520, 1\,344, 1\,920, 720, 660.
\]
Their distinguished orbits on $\Lambda$ have sizes
$1,6,7,7,8,2,12,11$. Each of the first seven classes has a unique distinguished orbit; the last has two complementary 11-point orbits. Every distinguished subset is checked to have precisely the corresponding subgroup as its set stabilizer. The eight families contain respectively
\[
22, 77, 176, 176, 330, 231, 616, 1\,344
\]
subsets. The last family gives only 672 different stabilizers.

Add $\{p,q\}$ to every six-set, add $p$ to the first seven-set family and $q$ to the other, and retain the eight-sets. The result consists of 759 eight-subsets of a 24-point set. The finite certificate checks that every one of its $\binom{24}{5}=42\,504$ five-subsets occurs in exactly one block. Thus this is an actual Steiner system $S(5,8,24)$. The group $G$ preserves it and fixes $p,q$. We retain the classical uniqueness of this Steiner system and the standard identification of its automorphism group with $M_{24}$, with two-point stabilizer of order $443\,520$. Since $|G|=443\,520$, the embedding is the required two-point stabilizer. This identifies the construction with the source's MOG model up to relabeling and possible interchange of $p,q$.

The certificate next forms the symmetric differences of every pair of octads meeting in two points. The resulting 2,576 dodecads give exactly the 616 dodecads contained in $\Lambda$, and deleting $p$ or $q$ from a dodecad containing exactly that fixed point gives exactly the 1,344 endecads. Hence the eight maximal-class names are the source's point, hexad, two heptad classes, octad, duad, dodecad and endecad. The endecad complement ambiguity is an actual two-to-one shadow-to-stabilizer map. The action on the corresponding coset objects is faithful: by U.Orbits its kernel is the intersection of the subgroup cores, and every proper-subgroup core in the simple group $M_{22}$ is trivial. The two complementary shadows still define the same object stabilizer; they are not separate types in the subgroup census.

### 6.3. Scope of the fourth-source comparison

The preceding theorem independently recovers the numerical classification in Leemans–Rowley (2010), with explicit witnesses and geometric shadows. Its full printed table has a stronger comparison obligation. Each of the 431 printed rows is recorded separately, including its physical page, Number, maximal-class label, pairwise intersection values and Borel-group label. These source rows are read only after the census.

At the present draft stage the exact meanings of some refined pair-orbit subscripts and colon labels remain unverified because the older Kilic–Rowley source defining them has not been acquired. The source's linked external witness file currently returns a 404 response. A coarse comparison that forgets those refinements finds 419 order-compatible matches in a maximum bipartite matching, not a complete source-row identification. The source also literally prints Number 61 twice and no Number 62. Its row $M_{133}(0,3,1)$ assigns intersection size three to a point and a heptad, contrary to its own definition. Neither observation determines the authors' intended replacement labels.

The independent census and canonical witness table therefore stand as a proved author component of the proposed fourth-source expansion, subject to external review. They do not yet discharge the full source-table contract. The outstanding source-specific labels and all diagnostic discrepancies are retained explicitly in the accompanying comparison ledger; no four-source whole-contract credit follows from this section alone.

