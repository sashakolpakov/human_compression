# Independent audit of the exact third-excess transition theorem

10 October 2026. Internal mathematical and code review by the `recent_conjectures` agent, separate from the author. This is not external peer review. The review found no mathematical gap in the frozen proof and its stated computational dependencies.

Reviewed proof: `phase22_excess3_transitions.md`, SHA256
`c020a14935ccb51a20d95485ff34d5a5c796dc98da6385f76f9a79eea43001aa`.
The exact companion source and data bindings are in the audit JSON. No author or public file was modified.

## 1. Mathematical coverage

**Deletion defects.** The proof works in the established class-two quotient, not by assuming a deletion retraction on an arbitrary string C-group. The normal closure of the omitted markers has precisely their vertex coordinates and incident-edge coordinates. Those are disjoint from the retained parabolic's coordinates. The exact canonical-kernel restriction then gives $R\le\gamma_3(B)$. This holds for the stated forest marking, including a disconnected retained subset.

**Finite and complete alphabet.** Excess at most three gives $|\gamma_3|\le8$ and nilpotency class at most five. Every rank-five window has at most the same excess by exact parabolic restriction. The frozen universal-kernel ladder is consequently complete for all needed windows. The reconstruction uses every saved index-two and index-four candidate, and all previously accepted index-eight kernels. It verifies normality, index, small-kernel profiles and every actual meet of each survivor. Expected counts are assertions after reconstruction, not filters selecting a conjectured family. The accepted index-eight list's exhaustiveness remains an explicit retained phase21 computation.

**Marked boundary matching.** Both boundaries are images of the same rank-four universal marked group. Equality of the homomorphism kernels is exactly equality of their ordered marked isomorphism types. Canonical induced pc sequences in one fixed group give subgroup keys, with the relative-order-two assertion needed for the binary element encoding. Every key match also receives an actual bijective marked homomorphism check. There is no quotient by additional automorphisms or path reversal.

**States and compatibility.** The state retains the actual subgroup $R$ in a specified boundary, not just its order or abstract type. I checked the code against both phase20 conditions: the transported $R$ centralizes the incoming final-generator normal closure, and the previous outside marker centralizes the incoming intersection $J$. The exact update is the last parabolic intersected with the normal closure of $R$ and the first incoming marker. Neither test is discarded. Since class is at most five, $[\gamma_3,\gamma_3]\le\gamma_6=1$; thus each boundary kernel is abelian of order at most eight and has at most sixteen subgroups. This justifies finite termination of the state search.

**Weighted pruning and completeness.** An edge weight is $\log_2|H:B|-2\ge0$. The initial cost is the window excess. The exact extension-order formula makes costs telescope to total excess. Processing minimum-cost states therefore safely discards only edges whose minimum possible total exceeds three. A later path reaching the same state with a larger cost cannot make a discarded edge admissible. Conversely, every retained edge satisfies the actual compatibility rules, and coefficient truncation discards over-budget paths. The marked walk bijection from phase20 prevents duplicate ordered markings.

**All-rank formula in the authored proof.** I read the relevant central-join counting argument, not just its theorem statement. Its finite support patterns contribute $mz^b/(1-z)^r$, with $r\le4$ and $b\le17$ at excess three. Terms with $r=0$ disappear before rank17. Therefore a polynomial of degree at most three is established for every $d\ge17$ independently of the transfer values. The lower-bound construction used elsewhere to prove exact degree is unnecessary. Four exact values at ranks17–20 determine the stated polynomial. Values at ranks5–16 extend it downward, and the separate complete rank-four census supplies 199. Rank three is separately37, not the polynomial's29. The graph itself is never used below its initial rank five.

## 2. Executable review and fresh arithmetic

I read the full final GAP transition source, Python input runner and sparse recount checker. The runner verifies the frozen kernel-data hashes and uses the original marked images of the universal presentation. The implementation checks both transition conditions before computing the next subgroup. The saved records retain all states and edges, rather than only census totals.

A fresh execution of the unchanged author sparse checker passed, producing a report byte-for-byte equal to the author's saved report. The separate run record states the exact executed hash and output. I did **not** regenerate the universal GAP groups or the full transition graph in this review; GAP 4.15.1/NQ 2.5.11 and the frozen group computations remain retained inputs.

I also wrote a distinct integer-graph checker. It verifies all canonical boundary matches and weights from the pc-key lengths, every minimum cost by monotone relaxation, and every budget-eligible boundary pair. It recounts all saved rows through rank24. Its new annihilator calculation is described in the next section and must not be confused with an independent group census.

The recorded compatibility rejection counts are both zero. The two independently constructed extra-state rank-six examples have trivial gluing intersection $J$ and a nontrivial deletion kernel of order two. Their 8,192 actual meets test those two positive constructions; they do not computationally cover a rejected compatibility case or a nontrivial diagonal quotient. The general claims about such cases retain the written phase20 proof.

## 3. Separate new supplement

During this audit, a new exact identity was found in the saved graph: on all 2,832 integer state/excess coordinates,
\[
 (T-I)^3v_7=125e_{1,3},\qquad Te_{1,3}=e_{1,3}.
\]
The separate [annihilator supplement](phase22_excess3_annihilator.md) proves from this identity that the same formula holds for all ranks at least seven, with ranks4–6 handled separately. This removes the central-join eventual-polynomiality theorem from an **alternate** proof route. It is co-development of an additional proof, not part of the claim that the author's original argument was independently audited. The author's original bytes remain unchanged and its existing argument already passes.

## 4. Exact boundary of this review

This audit supports the number of **ordered marked** nondegenerate path string C-groups of the stated two-power orders. It does not classify unmarked groups, count reversal orbits by dividing by two, establish publication priority, or claim full Lean formalization. The forest canonical quotient, finite-state theorem and complete prior kernel censuses are retained and explicitly linked dependencies. I read their relevant mathematical adapters, but did not independently reimplement the entire preceding research chain or re-prove the NQ algorithm.
