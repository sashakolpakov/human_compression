# Merging and splitting a bipartition: L111 §6 and two exact boundaries

Date: 2026-10-10. Private mathematical/source adapter. The earlier Theorem 4.1 package is unchanged.

## 1. Target and access

The selected [primary author-indexed text](https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes) now exposes the complete verbal Theorems 6.1 and 6.2, Constructions 6.1 and 6.2, Corollary 6.1 and its proof. Direct primary-PDF access remains unavailable. This note proves the construction, connectivity, diagram and disjoint-pair claims, and the forward symmetry transfer. It separates the printed symmetry converse and local-bipartiteness corollary, which fail under the hypotheses visible in that primary text. No priority or whole-paper claim follows; unread application tables remain excluded.

All incidence geometries below satisfy the all-flags chamber-extension axiom. Types and flags may be infinite. Graphs are simple, without isolated vertices; when aligning with the source's graph convention, exclude the graph reduced to one edge. Connectivity uses finite paths. Strong connectivity concerns every truncation retaining at least two types, in every residue.

## 2. A universal merging construction

Let \(\Gamma\) have types \(\{0,1\}\cup J\). Its lower incidence graph \(X\) has the disjoint union \(S_0\sqcup S_1\) as vertex set and one edge \(\{p,q\}\) for each incident pair \(p\in S_0,q\in S_1\). It has the specified bipartition \((S_0,S_1)\).

Define \(M\Gamma\) with type 0 equal to that vertex set, type 1 equal to the edges of \(X\), and higher objects unchanged. A vertex–edge flag means containment; vertex–higher and higher–higher incidence are inherited; an edge meets a higher object exactly when both endpoints do. Thus the graph/endpoint conditions G and E hold by definition. No coset realization is assumed.

Every original chamber \((p,q,F)\) gives exactly two new chambers,
\[
 (p,\{p,q\},F),\qquad(q,\{p,q\},F). \tag{1}
\]
These are all the new chambers. A new flag containing an edge corresponds to the original flag containing both endpoints; a flag containing only one lower vertex is already an original flag; a higher-only flag is unchanged. Extending that original flag proves that every new flag lies in a chamber. This works without finiteness of the flag.

The exact residue models are:

- At a lower vertex \(p\), the new residue is the original residue at \(p\). Edges \(\{p,q\}\) correspond to the opposite original lower objects \(q\); higher objects are fixed.
- At an edge \(\{p,q\}\) but no chosen endpoint, the residue is the join of the two endpoints with the original residue at \(\{p,q\}\). All incidences from either endpoint to any remaining object occur.
- At an endpoint together with its edge, the remaining residue is the original residue at \(\{p,q\}\).
- Taking a residue at a higher-only flag commutes with \(M\). At remaining rank two it is the vertex–edge incidence of the original rank-two incidence graph.

All four statements restrict to arbitrary additional higher flags.

## 3. Connectivity and diagram: exact affirmative scope

**Theorem A.** The construction \(M\) preserves and reflects connectedness, residual connectivity and strong connectivity. It also preserves and reflects G and E at every disjoint type pair.

For global connectedness, the new vertex–edge incidence subdivides each original lower–lower incidence. Its additional edge–higher incidences do not change components: either endpoint already meets that higher object. All other incidences are unchanged. Hence the connected components agree after suppressing the new edge objects.

Apply this fact to every higher-only residue. Vertex-containing residues are covered by the first local model. Edge-only residues of rank at least two are connected because both endpoints meet every remaining higher object. Every original residue containing an original lower object occurs as a new vertex-containing residue, with an edge additionally fixed when both original lower objects were fixed. This proves residual connectivity in both directions.

Here is the strong-connectivity argument without a finite-rank shortcut. It suffices to treat two-type truncations, since any object in a larger retained truncation lies in a chamber and meets an object of any fixed retained type.

Assume \(\Gamma\) strongly connected. The new \(\{0,1\}\) truncation is the subdivision of the connected original lower incidence graph. The new \(\{0,j\}\) truncation is the union of the connected original \(\{0,j\}\) and \(\{1,j\}\) truncations, sharing their nonempty type-\(j\) part. For new \(\{1,j\}\), any two lower edges sharing an endpoint \(p\) can be connected through their corresponding lower objects in the \(\{\text{opposite lower},j\}\) truncation of \(\Gamma_p\). Such paths exist by strong connectivity. Any two edges of the connected lower graph are joined by a finite chain of shared endpoints; concatenate these paths. Every type-\(j\) object meets an edge by chamber extension. Higher–higher truncations are unchanged. Apply the same argument in every higher-only residue; the other residue models give the remaining cases.

Conversely, let \(M\Gamma\) be strongly connected. The old lower graph is connected by suppressing its subdivision vertices. To connect original objects of type 0 in an old \(\{0,j\}\) truncation, join them along the bipartite lower graph. Consecutive type 0 vertices on this path share a type 1 neighbor \(q\). The new residue at that vertex \(q\) is the old residue \(\Gamma_q\); strong connectivity supplies a path of types \(\{0,j\}\) between them. Concatenate. Every type-\(j\) object meets an original type 0 object, so the whole truncation is connected. Interchange 0 and 1 for the other lower–higher truncation. Higher–higher pairs are unchanged. For an arbitrary original flag, a lower-containing residue is already a new flag residue; a higher-only residue is handled by the same argument applied there. Thus all original truncations in all residues are connected.

For a disjoint selected pair \(k,l\), its truncation is unchanged. The endpoint-incidence condition with unchanged objects is unchanged. Testing it against a merged type 0 object is exactly testing it against that original object, of original type 0 or 1. Testing it against a new edge \(\{p,q\}\) follows by applying the original condition twice, to \(p\) and \(q\). This proves the forward implication; testing against all merged vertices proves the reverse implication. Simplicity and endpoint sizes at \(k,l\) are unchanged.

The complete rank-two diagram follows from the residue models:

| New residue types | Exact description |
|---|---|
| \(\{0,1\}\) | Vertex–edge incidence of each original rank-two lower residue |
| \(\{0,j\}\) | A complete bipartite residue on the two endpoints and the remaining type-\(j\) objects |
| \(\{1,j\}\) | Union of the original classes on \(\{0,j\}\) and \(\{1,j\}\), with the remaining lower type renamed 1 |
| \(\{i,j\}\subseteq J\) | Exactly the original class on \(\{i,j\}\) |

If the original two lower–higher classes are both contained in the designated class \(K_j\), the new \(\{1,j\}\) class is contained in \(K_j\). This is the input diagram used in source Theorem 6.1. We need no equality of individual residues beyond that diagram condition.

## 4. Splitting is the exact inverse when a global bipartition exists

Let \(\Lambda\) satisfy G and E, and let its selected graph \(Y\) have a chosen bipartition \(Y_0\sqcup Y_1\). Construct \(S\Lambda\) by making \(Y_i\) type \(i\), dropping the old graph-edge objects, and making opposite lower vertices incident when adjacent in \(Y\). Keep all higher objects and incidences; a lower vertex meets a higher object precisely when the old vertex did.

A flag with both lower vertices determines a unique old edge, and E puts that edge in the residue of its higher part. Extend the old flag to a chamber. A flag with one or no lower vertex is handled by extending it first and using the two endpoints of the resulting old edge. Thus \(S\Lambda\) is a geometry.

The object formulas immediately give
\[
 M(S\Lambda)\cong\Lambda,\qquad S(M\Gamma)\cong\Gamma, \tag{2}
\]
where the second identity uses the original specified bipartition. No connectivity is needed for these inverses. On a disconnected graph the choice of bipartition matters, since its components can be recolored independently.

This proves the construction and inverse asserted by source Theorem 6.2, including its diagram: copied-vertex residue models recover the two lower–higher classes from the old edge–higher classes. The same local argument identifies higher–higher residue classes exactly. In particular, the **global** bipartiteness hypothesis in that theorem is sufficient and is indispensable for this inverse construction.

There is also a direct link to the cover formulation: splitting a bipartite graph-incidence geometry is its lower-type compression. The operation is reversible when the chosen bipartition is retained as data. It is not an inference from local bipartiteness alone.

## 5. Symmetry: valid transfer and the exact obstruction

Suppose \(\Sigma\) preserves every original type and is chamber-transitive on \(\Gamma\). It has two chamber orbits on \(M\Gamma\), distinguished by which original lower type supplies the selected endpoint in (1). If an automorphism \(\sigma\) interchanges the two original lower types and fixes all other types, then \(\langle\Sigma,\sigma\rangle\) is type-preserving and chamber-transitive on \(M\Gamma\). This does not require \(\sigma\) to be an involution or to normalize \(\Sigma\). It proves the forward assertion of source Theorem 6.1(iii).

If the lower graph \(X\) is connected, every automorphism of \(M\Gamma\) either preserves or interchanges its two color classes. For a chamber-transitive group \(\Omega\), this gives a surjective homomorphism
\[
 \Omega\longrightarrow C_2. \tag{3}
\]
Its kernel \(\Sigma\) acts faithfully and chamber-transitively on the split geometry \(\Gamma\): lift two original chambers to the new chambers using their type 0 endpoints, then use \(\Omega\)-transitivity; the transporting element preserves colors because it takes one type 0 endpoint to another in a connected bipartite graph. Faithfulness follows because new edges are determined by their endpoints. Thus an index-two extension is justified under this connectedness assumption. Splitting further requires an involution outside the kernel; (3) alone does not establish that.

Without connectedness the printed converse can fail even at the level of orders, independently of how its colon notation is interpreted. Here is the explicit example proposed by the root reviewer.

Take \(\Gamma\) to be the disjoint union of two rank-three geometries, each with two objects of every type, with all cross-type pairs incident inside a component. Every flag lies in a chamber, all panels have two completions, and every rank-two residue is a digon. Its full type-preserving automorphism group has order
\[
 (2^3)^2\cdot2=128. \tag{4}
\]
Each merged component has a lower graph \(K_{2,2}\), its four edges, and two indistinguishable higher objects. Its full type-preserving automorphism group is \(D_8\times C_2\), of order 16, where \(D_8\) denotes the order-eight automorphism group of the square. The full group \(\Omega\) of the two-component merged geometry has order
\[
 16^2\cdot2=512 \tag{5}
\]
and is chamber-transitive. Were \(\Omega\) an extension by a group of order two of a faithful type-preserving automorphism group of the original \(\Gamma\), that group would have order 256, exceeding the full order 128 in (4).

This example satisfies the unrestricted geometry and diagram hypotheses visible in the primary Theorem 6.1. It is disconnected, so it does not challenge a converse with an added connected-lower-graph assumption. No conclusion is made here about whether every connected case splits.

## 6. A regular thin counterexample to the local-bipartiteness corollary

For each odd integer \(m\ge5\), construct the usual square incidence geometry on the toroidal grid \((\mathbb Z/m\mathbb Z)^2\). Its vertices are pairs \((x,y)\). Its edges join pairs differing by one in exactly one coordinate. Its faces are the four-vertex squares
\[
 Q_{x,y}=\{(x,y),(x+1,y),(x,y+1),(x+1,y+1)\}. \tag{6}
\]
Incidence is containment, with edges regarded as their two endpoints. There are \(m^2\) vertices, \(2m^2\) edges and \(m^2\) faces.

Every face is an induced four-cycle: for \(m\ge5\) there are no additional adjacency edges between its vertices. Thus G and E hold. A vertex and incident face determine two containing edges; an edge lies in two faces and has two endpoints. Every flag extends to a chamber and all panels have size two.

The whole incidence graph is connected. At a vertex, the four incident edges and four incident faces form an eight-cycle. At an edge, its two endpoints and two incident faces form \(K_{2,2}\). At a face, its four vertices and four edges form an eight-cycle. These exhaust residues of rank at least two in rank three, proving residual connectivity. Translations and the square's signed coordinate permutations give a chamber-transitive group of order \(8m^2\); indeed they move any vertex to any other, and the order-eight vertex stabilizer moves freely among its eight incident edge–face flags. Hence these are regular thin examples, not merely nonfirm incidence systems.

They satisfy the source's explicitly permitted weak geometric shadow condition \((I_{01})\). For any edge \(e\) and face \(Q\), their common vertex shadow is empty, one vertex, or both endpoints. In the singleton case use that vertex as a one-object flag. In the two-endpoint case E gives \(eIQ\), so use the one-object flag \(\{e\}\). Each witness is incident with both \(e\) and \(Q\) and has exactly the required vertex shadow. This verifies the condition directly without confusing it with the subgroup intersection property.

Every rank-two residue of types \(\{0,1\}\) is a square graph and has no odd cycle. The other missing lower–higher edge of the diagram is a digon, as just checked. But the full selected graph contains the row cycle
\[
 (0,0),(1,0),\ldots,(m-1,0),(0,0), \tag{7}
\]
which has odd length. Therefore it is not bipartite and cannot be \(M\Gamma\) for any geometry with two original lower types: that graph is always bipartite by construction.

This contradicts the implication in the indexed Corollary 6.1 from its stated finite-rank, residual-connectivity, local-bipartiteness and \((I_{01})\) hypotheses to existence of a global splitting. It leaves Theorem 6.2 with its explicit global bipartiteness hypothesis intact. The correction is to require a global two-coloring, or an equivalent vanishing condition on parity around all closed graph walks. Local square boundaries alone do not force that condition; the odd toroidal row exhibits the missing parity obstruction. More explicitly, assigning 1 in \(\mathbb F_2\) to every graph edge gives a cellular 1-cocycle because every square boundary has even length. A global bipartition is exactly a vertex function whose coboundary is this assignment. Summing around (7) gives 1, whereas every coboundary sums to 0 around a closed walk. Hence this class in \(H^1(\mathbb F_2)\) is nonzero. Equivalently, the parity double cover has no section that sends every base edge to a lifted edge. This explains the obstruction in the same torsor language; it supplies no claim that stronger unverified shadow axioms are needed for this example.

## 7. Coverage and evidence

The [new checker](phase32_L111_section6_check.py) and [report](phase32_L111_section6_check.json) enumerate all flags and residues for the \(m=5\) torus, verify every \((I_{01})\) witness, and record the literal odd cycle. The checker also constructs the two-component symmetry example, checks the full order bounds through explicit component automorphisms, and tests the merging/splitting formulas on additional examples. At \(m=5\) it verifies all 601 flags, 101 connected residues, 300 thin panels and 1,250 weak-shadow pairs, together with a 200-element chamber-transitive group. The symmetry example has full group orders 128 and 512. These are finite certificates for the stated examples. The uniform proofs and the infinite-rank construction statements are written mathematics, not conclusions from a finite search.

| Source target | Result of this adapter |
|---|---|
| Construction 6.1; Theorem 6.1 construction/diagram | Recovered by §2 and the exact table in §3, subject to the source graph nondegeneracy convention |
| Theorem 6.1(i), connected/residual/strong equivalences | Recovered at arbitrary rank by §3 |
| Theorem 6.1(ii), disjoint-pair equivalence | Recovered by §3 |
| Theorem 6.1(iii), forward symmetry transfer | Recovered by §5 |
| Theorem 6.1(iii), unrestricted converse | Fails on the two-component order 128/order 512 example |
| Theorem 6.2 and Construction 6.2 | Recovered with their explicit global bipartition by §4 |
| Corollary 6.1 | Its literal local-to-global implication fails on the odd square tori, even using the allowed weak shadow condition |
| Section 6 auxiliary automorphism/parameter lemmas and later tables | Not completely audited or credited here |

Source definitions and statements were read from primary indexed passages. No complete-paper reading, later-version verification, correction priority, or whole-principal-paper coverage is claimed by this package. The numerical examples do not depend on the unverified auxiliary automorphism assertions elsewhere in L111.
