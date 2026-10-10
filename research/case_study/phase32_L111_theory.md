# The finite-rank neighbourhood construction as a graph-cover adapter

Date: 2026-10-10. Private proposed statement-level reduction; no novelty claim.

## 1. Exact target and access boundary

L111 is Lefèvre-Percsy, Percsy and Leemans, *New geometries for finite groups and polytopes*, Bull. Belg. Math. Soc. Simon Stevin 7 (2000), 583–610, [DOI](https://doi.org/10.36045/bbms/1103055618). The [author-uploaded indexed text](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes) exposes the definitions on p.586, graph convention/Definition 3.1, the complete verbal Theorem 4.1, Construction 5.1, and the relevant local proofs in §5. Direct access still returns HTTP429; a complete primary PDF has not been obtained. Diagram typography is incomplete. The residue descriptions below determine its classes without guessing the picture.

The exact target is **all finite-rank conclusions of Theorem 4.1**, under its explicit graph and endpoint-incidence hypotheses. Infinite rank, the hypothesis conversion in Corollary 4.1, §6, and the application tables are excluded. This is neither a whole-paper reduction nor a claim to have read the entire paper. The old construction keeps every higher object single. Its local connectivity requirement must not be omitted or confused with a later component-splitting operation.

## 2. Independent formulation

Let \(\Gamma\) be an incidence geometry on a finite type set \(I\), with \(|I|\ge3\). A flag is a set of mutually incident objects; every flag extends to a chamber containing one object of each type. Distinct objects of the same type are not incident. Its incidence graph has the objects as vertices, with incidence between distinct types as edges.

Select types \(0,1\). Write \(V=S_0\), and assume:

- **G:** The objects of type1 are exactly the unordered edges of a simple graph \(X\) on \(V\); vertex–edge incidence is containment. No vertex is isolated.
- **E:** For an edge \(e=\{p,q\}\) and any object \(x\) of another type,
  \[
  eIx\quad\Longleftrightarrow\quad pIx\text{ and }qIx. \tag{1}
  \]

For alignment with the source's graph convention, one may exclude a graph consisting of one edge, and impose the same convention on its relevant graph residues. The proof below also works when such a residue occurs: its bipartite double is disconnected. It does not require the source's hypothesis-conversion lemmas.

Define \(U\Gamma\) by keeping the objects of every type outside \(\{0,1\}\), replacing each of types0 and1 by a distinct copy of \(V\), and setting
\[
 (p,0)I_U(q,1)\iff\{p,q\}\in E(X),\qquad
 (p,i)I_Ux\iff pIx\quad(i=0,1).
 \tag{2}
\]
Higher-type incidences remain unchanged. These formulas are the object-level definition, not merely a coset or subgroup encoding.

For a higher flag \(F\), let \(X_F\) be the graph on the vertices incident with all of \(F\), with the original edges whose endpoints both belong to that set. Equation (1) identifies this graph with the vertex–edge truncation of \(\operatorname{Res}_\Gamma(F)\). It has no isolated vertices, by chamber extension.

**Theorem A.** With this notation:

1. \(U\Gamma\) is a geometry, and its chambers are in equivariant bijection with those of \(\Gamma\).
2. \(U\Gamma\) is residually connected if and only if \(\Gamma\) is residually connected and every \(X_F\), for \(F\) of cotype \(\{0,1\}\), is nonbipartite.
3. The same equivalence holds for strong connectivity, meaning that every truncation of rank at least two, in every residue, is connected.
4. Each type-preserving automorphism group of \(\Gamma\) acts on \(U\Gamma\), with the same action kernel and the same chamber orbits. In particular, chamber transitivity is preserved.
5. The rank-two residue classes of \(U\Gamma\) are as listed in §6. Conditions G and E at a disjoint pair of types persist, so the operation can be repeated there.

Residual connectivity includes the empty flag and requires connectivity only for residues of rank at least two. No finiteness of the object sets, chamber transitivity, thinness or subgroup intersection property is assumed.

## 3. Chambers and all residue models

A chamber of \(\Gamma\) has the form \((p,e,F)\), where \(e=\{p,q\}\) and \(F\) has cotype \(\{0,1\}\). The map
\[
 (p,\{p,q\},F)\longmapsto((p,0),(q,1),F) \tag{3}
\]
is a bijection onto the chambers of \(U\Gamma\). To prove that every new flag extends, consider the number of copied vertices it contains. With none, extend its higher flag in \(\Gamma\) and orient the resulting edge arbitrarily. With one, extend that vertex together with the higher flag and orient the edge so that the vertex has the specified new type. With two, (2) gives their common edge, and (1) puts that edge in the residue of the higher flag. Extend the resulting original flag. This also proves surjectivity of (3); injectivity uses simplicity of \(X\).

The following exact models handle every new residue. Here \(F\) is any higher flag, and all displayed unions are flags.

**A copied vertex.** There is an incidence isomorphism
\[
 \operatorname{Res}_{U\Gamma}(F\cup\{(p,i)\})
 \cong\operatorname{Res}_\Gamma(F\cup\{p\}). \tag{4}
\]
It fixes all higher objects and maps the opposite copied vertex \((q,1-i)\) to \(\{p,q\}\). This is a bijection on the remaining lower-type objects. Its preservation of higher incidence is exactly (1), since those objects are already incident with \(p\). This proof also handles residues of rank one or zero.

**Both copied vertices.** Restricting (4) gives
\[
 \operatorname{Res}_{U\Gamma}(F\cup\{(p,0),(q,1)\})
 \cong\operatorname{Res}_\Gamma(F\cup\{p,\{p,q\}\}). \tag{5}
\]
All remaining objects and incidences are literally the same.

**Only higher objects.** Taking a residue commutes with (2):
\[
 \operatorname{Res}_{U\Gamma}(F)
 =U\bigl(\operatorname{Res}_\Gamma(F)\bigr). \tag{6}
\]
For cotype \(\{0,1\}\), this is the bipartite double \(D(X_F)\), whose vertices are \((p,i)\) and whose edges join \((p,i)\) to \((q,1-i)\) when \(p\sim q\).

One original residue has no direct analogue in (4): a flag containing an edge but no vertex. Its remaining type0 consists of the two endpoints. Every other remaining object is incident with both endpoints by (1). If the residue has rank at least two, it has another object by chamber extension. Its incidence graph is consequently connected, regardless of incidences among those other objects. This observation is required for the reverse implication in Theorem A(2).

## 4. Connectivity, including the reverse implication

First suppose the remaining rank is at least three. There is an elementary connectivity equivalence
\[
 U\Gamma\text{ connected}\quad\Longleftrightarrow\quad
 \Gamma\text{ connected}. \tag{7}
\]
Indeed, for each \(p\), chamber extension gives a higher object \(x\) incident with it, so \((p,0)-x-(p,1)\) is a path. Contracting these color-switch paths identifies the connected components of \(U\Gamma\) with those of the graph obtained from \(\Gamma\) by removing each edge-object and joining its endpoints directly. Reintroducing an edge-object as a subdivision does not change components. An incidence from that edge-object to a higher object is redundant for components: by (1) its endpoints already meet that object. This proves both directions of (7) without assuming that the truncation \(X\) is connected.

For rank two, path lifting in \(D(X)\) changes the color coordinate exactly when a step is taken. Thus \(D(X)\) is connected precisely when \(X\) is connected and has an odd closed walk, equivalently an odd cycle. If \(X\) is connected and bipartite, its double has exactly two components. This works for infinite graphs as well, since paths and cycles are finite.

Apply these two facts to (4)–(6). A new residue containing a copied vertex is connected exactly when its corresponding original residue is. A higher-flag residue of rank at least three has the same connectedness on both sides by (7). A higher-flag residue of rank two is connected exactly when its graph is connected and nonbipartite. Finally, the original edge-only residues are connected by the last paragraph of §3. This proves Theorem A(2), including all original residues needed in the reverse direction.

For completeness, finite-rank residual connectivity implies the strong connectivity used here. Induct on rank to show chamber-gallery connectivity: the chambers containing any given object are gallery-connected by induction in its residue; a path of incident objects, completed pairwise to chambers, joins these chamber sets. Rank one is immediate. A gallery projected to any chosen two types is a walk through incident pairs, so their truncation is connected. The same argument applies to every residue. A larger truncation is connected because each of its objects lies in a chamber and hence meets an object of a fixed two-type truncation. Conversely, strong connectivity includes the whole incidence graph of each residue. The two notions are therefore equivalent at finite rank, proving Theorem A(3). No infinite-rank version is inferred from this induction.

## 5. Symmetry and repeated operations

For a type-preserving automorphism \(g\), define \((p,i)^g=(p^g,i)\) and use the original action on higher objects. Equations (1)–(2) prove that this is an automorphism; (3) is equivariant. Hence it preserves every chamber orbit and stabilizer, not merely transitivity. If it fixes all new objects, it fixes every original vertex and higher object, and also every original edge because edges are determined by their endpoints. The action kernels coincide. This does **not** identify the full automorphism groups: new automorphisms or type permutations are not excluded.

Now suppose G and E also hold for types \(k,l\), with \(\{k,l\}\cap\{0,1\}=\varnothing\), where \(k\) is the vertex type. Their truncation is unchanged. For an edge-object \(e\) of type \(l\) and an unchanged object of another type, E is unchanged. For a new object \((p,i)\), incidence with \(e\) means \(pIe\); the original condition E at \(k,l\) says exactly that both \(k\)-endpoints of \(e\) meet \(p\), which means that they meet \((p,i)\). Thus both conditions persist.

An additional direct consequence of the formulas is that operations at disjoint pairs commute up to the canonical identification: an incidence between two copied objects is the original incidence between their original vertices, whichever replacement is done first. This is an adapter consequence, not additional source-result credit. Residual connectivity at each stage still requires the relevant odd-cycle condition; iteration alone does not supply it.

## 6. Exact diagram reconstruction

Let \(\mathcal R_{ij}(\Gamma)\) denote the isomorphism classes of all residues of cotype \(\{i,j\}\), retaining the indicated types. Formulae (4)–(6), in both directions, give:

| New residue types | Exact class description |
|---|---|
| \(\{0,1\}\) | \(\{D(X_F):F\text{ has cotype }\{0,1\}\}\) |
| \(\{0,j\}\), \(j\notin\{0,1\}\) | \(\mathcal R_{1j}(\Gamma)\), with old type1 renamed0 |
| \(\{1,j\}\), \(j\notin\{0,1\}\) | \(\mathcal R_{1j}(\Gamma)\) |
| \(\{i,j\}\subseteq I\setminus\{0,1\}\) | \(\mathcal R_{ij}(\Gamma)\) |

For the last row, a complementary new flag contains the two copied vertices and corresponds to an original flag containing their vertex and edge. Every original such flag has a unique image by (3) restricted to those types. For the middle rows, a complementary flag contains exactly one copied vertex, and (4) applies. Thus these are equalities of classes, not merely inclusions or numerical parameter matches.

## 7. Relation to the monodromy theorem

Under the positive conditions of Theorem A(2), every common higher shadow \(X_F\), including the empty flag, is connected: it is a two-type truncation of a residually connected finite-rank residue. Extend \(F\) to a flag \(F'\) of cotype \(\{0,1\}\). The nonbipartite graph \(X_{F'}\) lies inside \(X_F\), so every \(X_F\) contains an odd cycle.

In the parity cover \(D(X)\), the monodromy subgroup of every such shadow is therefore the whole deck group \(C_2\). Both deck-coset Helly and monodromy-intersection equality in [the general cover theorem](phase28_voltage_shadow_theory.md) become automatic. Each individual higher shadow has only one lifted component. Its compressed graph-cover construction is exactly (2). This recovers the forward residual-connectivity assertion from the common cover theory, while §§3–6 supply the converse, symmetries, diagram and repetition.

When some relevant graph is bipartite, keeping that higher object single can produce a disconnected residue. Splitting its lifted components would be a different construction. Neither construction can be silently substituted for the other in a source comparison.

## 8. Verification and coverage boundary

The companion [checker](phase32_L111_check.py) tests the literal object construction, all flags and residues, all local maps (4)–(6), chamber bijections, pair-truncation connectivity and the iteration statement in finite positive and negative examples. Its exact report is [phase32_L111_check.json](phase32_L111_check.json). The input sweep contains 316 graph/subset geometries and checks 12,628 residue isomorphisms and 26,802 flags. It includes 307 residually connected inputs and 48 residually connected outputs. Separate examples include dihedra, simplices through rank five, and disjoint-pair iterations. The common-edge control also tests the broader formulation allowing a one-edge graph residue; that boundary is not attributed to the source's stricter graph convention. Finite checks corroborate the proof; they do not establish its unbounded scope.

The source alignment is statement-level: finite-rank Theorem 4.1, with the convention and construction read from primary indexed passages. This recovers one substantial principal construction theorem, not all principal results of L111. No application table, source converse in §6, infinite-rank claim, full automorphism-group equality, novelty assertion, or compression ratio is claimed.
