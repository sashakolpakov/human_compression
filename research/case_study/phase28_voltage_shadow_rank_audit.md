# Independent review of the voltage-shadow theorem

The complete written argument in [phase28_voltage_shadow_theory.md](phase28_voltage_shadow_theory.md) passes independent mathematical review. Its two conditions have different roles: typed coset Helly is exactly the flag-completion condition, while equality of common-shadow monodromy with the intersection of individual monodromies is exactly the additional residual-connectivity condition. This review does not infer either condition from subgroup intersection alone.

## Component calculation and both recognition directions

The base assumptions make each common higher-flag shadow an induced connected graph with an edge. Connectedness here follows from the proved chamber-gallery and connected-truncation lemma applied inside the base residue. It does not follow merely from connectedness of the whole base geometry.

At a common base vertex, use an equivariant identification of its deck-group torsor with $A$. Right multiplication by closed-walk voltages gives each lifted component fiber as a left coset $g_xH_x$. A common lifted vertex at another base vertex can be transported through the connected pairwise common shadow. Consequently two components meet somewhere if and only if their cosets meet in the chosen fiber. This step is valid for nonnormal, nonabelian monodromy subgroups.

When all cosets meet, translating by one common point identifies their intersection with $H=\bigcap H_x$. Paths in the total common shadow lift inside every chosen component. Two points $gh,gh'$ in its fiber are connected exactly when $h^{-1}h'\in H_F$. Therefore the connected components are the left cosets of $H_F$ in $H$. No assertion that $H_F$ is normal is required. The proof also works with infinite groups and graphs; it uses finite walks and an actual coset bijection, rather than a finite order calculation.

Typed Helly is necessary because a completed lifted chamber supplies a common vertex, which can be transported to the chosen fiber. It is sufficient because a common lifted vertex extends along a lifted edge of a base chamber, uniquely selecting all additional higher components. Flags already containing a vertex or edge are handled by fixing that object while extending the base flag. In the bipartite compression, two lower objects specify the actual lifted edge; the simplicity of the base graph ensures there is no ambiguity from parallel edges.

For residual connectivity, the monodromy equality makes the lower truncation of each higher-flag residue connected. Once geometry is known, every other residue object attaches to that truncation through a chamber. Conversely, choose all components through one lift of a common base vertex. A nontrivial monodromy index disconnects the lower truncation. Residual connectivity would force that truncation to be connected by the proved truncation lemma, even when the full residue contains more than two types. Thus necessity does not wrongly identify a disconnected truncation with a disconnected residue.

## The delicate lower-residue identification

At a lifted vertex over $v$, every base edge at $v$ lifts uniquely, and every higher object incident with $v$ has a unique lifted component containing this vertex. If two such higher objects are incident in the base, their selected components already share the chosen vertex. Conversely, lifted incidence expressly requires base incidence. This proves the exact higher–higher incidence correspondence, not just a bijection of objects. An incident base edge stays in the selected higher component by unique lifting, giving the other incidence correspondences.

At a lifted edge, the two endpoints correspond to the original endpoints, and each incident higher object has one component containing that edge. The same argument identifies the full residue with the original edge residue. These identifications restrict to flags. In the compressed system, an opposite-color neighbour of a lifted vertex corresponds to its unique original incident edge, giving the same local result with the appropriate type relabeling.

These are the reasons residues whose defining flags contain lower objects require no separate monodromy equality. They also justify the stated firmness/thinness equivalences. For the compressed system, panels missing a new lower type correspond to original panels missing the edge type; original panels missing the vertex type already have two completions by B1/B2. Every original panel needed for the converse is obtained from a lifted chamber.

## Group actions and the parity specialization

The optional action theorem assumes liftability of every induced base graph automorphism. Retaining the base automorphism as part of a lift matters when its graph action has a kernel. The resulting group acts on higher components and is chamber-transitive because the base group is chamber-transitive and the deck group is transitive on the lifts of a fixed base chamber. This is not a claim that every graph automorphism lifts to an arbitrary cover.

If the cover is bipartite while the connected base graph is not, the deck group must interchange the two colors: otherwise colors descend through the fibers to a bipartition of the base. Its color-preserving subgroup has index two and is regular on the lifts of either color at a fixed base vertex. Adjusting a chosen lift by a color-swapping deck transformation proves the claimed surjection to the base acting group and chamber transitivity of the color-preserving lift group. The statement correctly stops short of identifying the full automorphism group.

For the canonical all-edges-odd $C_2$ voltage assignment, monodromy is trivial exactly on bipartite connected shadows. Cosets are singletons or the whole group, so the typed Helly condition is automatic. The monodromy equality is therefore exactly the phase27 parity condition. This conclusion is correctly restricted to the canonical voltage assignment; bipartiteness alone does not determine the monodromy of an arbitrary $C_2$ cover.

## Sources, evidence and limits

I independently read Schluchter, [arXiv:1411.4358v3](https://arxiv.org/html/1411.4358v3), §2.2 and Theorem 3.1 / Lemma 3.2, together with the subgraph form in Lemma 3.4. The source uses right multiplication by voltages and left deck transformations, matching the proof. It explicitly treats finite groups and graphs. The new note's infinite allowance is supported by its own walk-lifting and coset-bijection argument; it is not silently imported from an infinite version of that source.

I also read the complete [finite diagnostic](phase28_voltage_shadow_check.py) and freshly executed it into a separate output. The saved independent run, bound in the companion audit JSON, is byte-identical to the author's saved report. It verifies 28 component/coset instances and 2,350 families in a connected $S_3$-cover of $K_4$. The vertex-edge lift has 144 chambers and the compressed geometry, using the fixed permutation-sign bipartition, has 72. Every flag, extension and residue of these two rank-three incidence systems is checked. Their objects have sizes $(24,36,12)$ and $(12,12,12)$ respectively, so the two constructions are concretely distinct.

The diagnostic scope is limited and accurate. The complete geometric examples have rank three and hence no multiple-higher-object flag. The broader intersection-family loop checks the graph/coset formula; it is not an independent high-rank geometry classification. A second connected $S_3$ cover supplies a nontrivial component-index check: the two selected triangle monodromies are both $\langle(12)\rangle$, whereas their common edge has trivial monodromy, giving two components of size two. This agrees with an immediate direct closed-walk calculation because the three edges at the base vertex have identity voltage. The displayed $C_2^2$ family with pairwise nonempty but empty total coset intersection is an algebraic Helly obstruction only, as the note says.

Reproduce the author diagnostic without overwriting its evidence:

```sh
python3 phase28_voltage_shadow_check.py --output /tmp/phase28-fresh-review.json
```

This is a full written-proof review of the specified two constructions, with a fresh execution of the inspected author diagnostic. It is not a classification of voltage covers, a proof of unrestricted automorphism lifting, a Lean certificate, or a novelty assessment. The finite diagnostics are distinct evidence and are not assumptions in the uniform proof. Frozen phase26 and phase27 artifacts are unchanged.
