# Petrial obstruction through a retained-object action

Private source-bound reduction, 10 October 2026. This note rederives the principal obstruction of L108 and its thin-case biduality statement, while recording a boundary in the unconditional automorphism assertion. It is a mathematical review, not a novelty or current-priority claim. No finite-group hypothesis is required in the proofs.

## 1. Primary source and exact targets

D. Bonheure, F. Buekenhout and D. Leemans, *On the Petrials of thin rank 3 geometries*, Journal of Geometry 71 (2001), 19–25, [DOI 10.1007/s00022-001-8548-2](https://link.springer.com/article/10.1007/s00022-001-8548-2). The complete authored [rendered article](https://www.academia.edu/82511046/On_the_Petrials_of_thin_rank_3_geometries), linked from the coauthor's collection, has been read: all seven printed pages, definitions, numbered statements, proofs and references. No publisher PDF was obtained. The private source capture and access distinction are recorded in [the access audit](phase25_older_access.json).

**Source ledger.** Theorem 1 (p.20; proof p.24) says that a thin regular residually connected rank-three geometry with thin regular Petrial has linear diagram. Lemma 3.1 (p.23) identifies the chamber walk with the conventional Petrie walk for maps. Lemma 3.2 (pp.23–24) asserts residual connectivity and an unconditional automorphism inclusion; under thinness it further asserts biduality and equality of automorphism groups. The paper notes that the converse of Theorem 1 fails and refers to earlier examples.

The principal obstruction, residual connectivity, and the two conditional conclusions are proved below. The unconditional inclusion needs correction: there is always a natural action, but it need not be faithful. A seven-example certificate includes an elementary counterexample and a control for the face-stabilizer step. No classification or further examples from the cited atlas are assumed.

## 2. The marked action and the geometric face object

Let $\Gamma$ be a thin regular residually connected rank-three geometry. Its types are vertex, edge and face. Automorphisms preserve types. Fix a chamber $C=(v,e,f)$ and write $G=\operatorname{Aut}(\Gamma)$. Use the source's involutions:

- $a$ fixes $v,e$ and exchanges the two faces of their panel;
- $b$ fixes $v,f$ and exchanges the two edges of their panel;
- $c$ fixes $e,f$ and exchanges the two vertices of their panel.

Thinness and residual connectivity make the chamber graph connected. One elementary proof is to use connected rank-two residues to join chambers sharing an object, and then use a path in the incidence graph to join arbitrary chambers. An automorphism fixing one chamber consequently fixes every chamber: the other chamber of each panel is unique. Thus the chamber action is free. Regularity then gives

$$
G=\langle a,b,c\rangle,\qquad
G_v=\langle a,b\rangle,\quad
G_e=\langle a,c\rangle,\quad
G_f=\langle b,c\rangle,
$$

and $G_v\cap G_e=\langle a\rangle$, with the analogous two intersections and trivial threefold intersection. These facts also follow by walking within a residue. The three pair-generated groups are dihedral, allowing an infinite dihedral group if appropriate. A diagram edge is absent when the corresponding pair commutes.

Put $w=cab$. The geometric operation changes the vertex, then the face, then the edge of a chamber. With a left $G$-action its successive chambers are $w^iC$; the flips at an arbitrary chamber $gC$ act by right multiplication on its label $g$. The Petrie face is the actual pair of sets

$$
P(C)=\bigl(\{w^iv:i\in\mathbb Z\},\{w^ie:i\in\mathbb Z\}\bigr),
$$

with the old incidence induced between them. Equal pairs of sets are the **same** Petrie face. They are not retained as distinct labelled chamber orbits. This distinction is essential for action kernels and repeated vertices.

The Petrial $\Pi\Gamma$ retains the old vertices, edges and vertex-edge incidence; its faces are these distinct pairs of sets. Incidence with a face means membership. The construction is equivariant, so $gP(C)=P(gC)$ and $wP(C)=P(C)$. Two useful identities are

$$
wv=cv,\qquad w^{-1}e=be.\tag{1}
$$

Thus $P(C)$ contains both endpoints $v,cv$ at $e$, and both edges $e,be$ at $v$. These are distinct by thinness and freeness of the original chamber action.

For an ordinary map, these successive panel changes are precisely the alternating corner changes of its usual Petrie walk: at an edge one passes to its other endpoint, crosses to the other incident face, and continues along that face. This recovers Lemma 3.1 at the level of the ordered walk. The subsequent geometric operation still identifies equal vertex-edge sets, exactly as in the source definition; it does not assert that all walks have no repetitions.

## 3. Residual connectivity and the natural action

First, $\Pi\Gamma$ is a geometry. Every old incident vertex-edge pair extends to an original chamber and hence to its Petrie face. If a vertex or edge belongs to a Petrie face, some step of its defining walk supplies an incident edge or vertex in that same face. Hence every flag extends to a chamber.

Each Petrie face residue is connected. The walk alternates the edges $e_i=w^ie$ and vertices $v_i=w^iv$; by (1), $e_i$ joins $v_i$ and $v_{i+1}$. Its image contains every object of the face residue. Extra induced incidences do not destroy connectedness.

The vertex residue is also connected. In the old residue at $v$, a two-step path $e_1-f-e_2$ with distinct edges is replaced by $e_1-P(v,e_1,f)-e_2$, because $e_2$ is the unique other edge incident to $(v,f)$ and (1) puts it in that Petrie face. Old residual connectivity joins all retained edge objects in the new residue. Every new face incident to $v$ meets one of those edges. At an edge, the same argument replaces $v_1-f-v_2$ using the two endpoints in (1).

Finally the old vertex-edge truncation is connected. In a path in the original incidence graph, passages through an old face can be replaced by paths in its connected vertex-edge residue. The Petrial retains that connected truncation and every new face is attached to it. This proves global connectivity and hence Lemma 3.2(i), without using a general truncation theorem as an external input.

Equivariance gives a homomorphism

$$
\rho:G\longrightarrow\operatorname{Aut}(\Pi\Gamma).
$$

Its kernel $N$ fixes all retained vertices and edges, so

$$N\le G_v\cap G_e=\langle a\rangle.\tag{2}$$

Faithfulness is **not** presumed. Nor is flag transitivity of the image presumed.

## 4. The principal obstruction, with the kernel retained

**Theorem A.** If $\Pi\Gamma$ is thin, then $|ab|=2$ or $|ac|=2$. In particular $\Gamma$ has linear diagram. Thus the regularity assumption on the Petrial in the displayed source Theorem 1 is unnecessary; its abstract already states the thin-only conclusion.

**Proof.** Set $P=P(C)$. If $bP\ne P$, both $P$ and $bP$ contain $e$ and $be$ at $v$. The new vertex residue contains the four-cycle

$$e-P-be-bP-e.$$

Thinness makes each vertex of this bipartite residue have degree two. The four-cycle is therefore an entire connected component; residual connectivity from §3 makes it the entire residue. There are exactly two old edges at $v$. In the old thin connected residue, each of these edges has degree two and each old face has degree two, so that residue is likewise a four-cycle. Its regular dihedral action has order four. Hence $|ab|=2$.

If $bP=P$, both $b$ and $w$ fix $P$, so $ca=wb$ fixes $P$ and $e$. In any thin residually connected geometry the stabilizer of a corank-one flag acts faithfully on its two completions: an element fixing a completion fixes a chamber and is the identity. Therefore $\rho(ca)^2=1$. By (2), $(ca)^2\in\langle a\rangle$. But the rotation subgroup $\langle ca\rangle$ of the dihedral group $\langle a,c\rangle$ meets its reflection subgroup $\langle a\rangle$ trivially. Consequently $(ca)^2=1$, and $ca\ne1$ gives $|ac|=2$. ∎

This is an action-and-residue argument, not an intersection-property assertion about a changed generating list. In particular it never assumes that $b$ stabilizes every Petrie face. The swapped tetrahedron in §7 shows why that distinction matters.

## 5. Thin-case faithfulness, regularity and biduality

Theorem A permits a short recovery of Lemma 3.2(iii),(iv), without appealing to the false unconditional faithfulness statement.

Interchanging the names vertex and edge interchanges $b,c$, changes $cab$ to $bac=w^{-1}$, and leaves each Petrie set unchanged up to that type interchange. Thus we may assume $[a,c]=1$. Now

$$bwb=w^{-1},\qquad bv=v,\qquad be=w^{-1}e,$$

so $bP=P$. The subgroup $\langle b,w\rangle=\langle b,ca\rangle$ is transitive on the chambers of the face residue $P$: its elements give $(v_i,e_i)$ and $(v_i,e_{i-1})$ for every $i$. These are the two distinct edges at $v_i$ in that thin residue, by (1) and the original panel change. Every vertex and edge of $P$ occurs in the walk. The whole group $G$ is transitive on Petrie faces, since it is transitive on the original chambers. Hence $\rho(G)$ is chamber-transitive on $\Pi\Gamma$.

The free chamber action of its full automorphism group now shows that $\rho(G)=\operatorname{Aut}(\Pi\Gamma)$. Moreover $G_{v,e}=\langle a\rangle$ must be transitive on the two new faces incident to $(v,e)$: lift an image-group element carrying one of the corresponding chambers to the other. Thus $a$ exchanges those faces. Equation (2) forces $N=1$. This proves the natural equality of automorphism groups and also proves regularity of the thin Petrial.

At the chamber $(v,e,P)$ the new panel involutions are

$$a'=a,\qquad b'=b,\qquad c'=ca.$$

Indeed $ca$ fixes $(e,P)$ and carries $v$ to $cv$, while $b$ fixes $(v,P)$ and exchanges its two edges. The second Petrie step is therefore

$$c'a'b'=cb.$$

The $cb$-orbits of $v,e$ are exactly the vertex-edge shadow of the old face $f$, because its residue is the regular dihedral geometry of $\langle b,c\rangle$.

For completeness these old face shadows are distinct. If $f\ne f'$ have the same shadow, choose $(v,e)$ in it. Thinness gives $f'=af$. At $v$ the two faces meet both $e$ and $be$, giving a four-cycle that exhausts the old thin connected vertex residue. Thus $[a,b]=1$. Together with $[a,c]=1$, this makes $a$ central in $G$. Since it fixes the base vertex and edge and $G$ is transitive on each retained type, it fixes all retained vertices and edges. That contradicts $N=1$.

Consequently old faces correspond bijectively to the second Petrie faces, with exactly the original incidence. This yields a canonical isomorphism $\Pi^2\Gamma\cong\Gamma$ preserving the retained objects; the source writes this as equality after identifying each face with its shadow. The vertex-edge-swapped branch gives the same conclusion.

## 6. Literal boundary and a failed converse

Take the complete tripartite geometry with two objects of each type, $K_{2,2,2}$. Its type-preserving automorphism group is $C_2^3$, acting regularly on its eight chambers. In the notation above, $a,b,c$ independently exchange the face, edge and vertex coordinates. The element $w=cab$ reverses all three coordinates. Every Petrie face contains both vertices and both edges, so the Petrial has one face and is $K_{2,2,1}$. Its type-preserving automorphism group is $C_2^2$.

Thus the natural action loses $\langle a\rangle$ and the unconditional group inclusion in Lemma 3.2(ii) fails literally: a group of order eight cannot embed in one of order four. The correct unconditional assertion is the natural homomorphism with kernel bounded by (2). The conditional equality in (iv) remains valid by §5. This is an explicit source-scope issue; no claim is made about whether it has previously been noticed or corrected.

The same example has a linear diagram and nonthin Petrial, so it supplies a direct converse counterexample under the paper's incidence-geometry definitions. The $C_2\times S_3$ example additionally has a six-step chamber orbit whose vertex and edge sets each have size three. Thus a geometric Petrie length need not equal the chamber-step order in the nonthin case. The obstruction and biduality proofs do not use that unnumbered length assertion.

## 7. Exact finite checks and trust boundary

The standalone [checker](phase25_L108_check.py) constructs seven small groups from explicit permutations and builds their typed coset incidences. It verifies geometry, thinness, residual connectivity and the original regular action. It then computes the Petrial directly from the three chamber flips, deduplicating faces as vertex-edge sets. No changed-marking or faithfulness conclusion is inserted as an assumption.

The [saved result](phase25_L108_check.json) passes all seven examples, totalling 188 original chambers: $C_2^3$, $C_2\times S_3$, the tetrahedron and its vertex-edge swap, the nonlinear star-transposition $S_4$ geometry, and two $B_3$ markings. Four Petrials are thin; all four have faithful regular induced actions and exact bidual face shadows. Two nonthin examples have action kernel of order two. The tetrahedron has $bP=P$, while its swapped version has $bP\ne P$ and is still thin, exercising both branches of Theorem A.

Reproduce with `python3 phase25_L108_check.py --output /tmp/L108-check.json`. The report is deterministic and records the executed source hash. These are focused diagnostics and counterexample certificates, not an exhaustive geometry classification. The uniform proofs are §§2–6; there is no Lean certificate for this package. Retained foundations are elementary group actions, dihedral normal forms and incidence-graph connectivity. No group catalogue, finite-group classification or external map classification is used.

## 8. Coverage conclusion

The principal obstruction and all valid numbered structural conclusions are recovered through the retained vertex-edge action and connected residues. Lemma 3.1 is the explicit walk/definition adapter in §2. Lemma 3.2(ii) is corrected rather than falsely counted as rederived. The cited external atlas examples and map-classification background are not reproduced. A full reading of this short article supports this exact statement-level ledger; it does not turn the separate abstract-only L103 record into a read or rederived paper.
