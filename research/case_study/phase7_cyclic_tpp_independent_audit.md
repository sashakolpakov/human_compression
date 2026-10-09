# Independent audit of the metacyclic cyclic-TPP theorem

10 October 2026. Internal independent-agent review; no claim of publication priority or external peer review.

**Verdict: the written universal proof and the stated finite-search implication pass review.** This audit applies to the exact source hashes below. It does not establish the full hypertope order conjecture or the cyclic-TPP inequality for arbitrary finite 2-groups.

## Universal proof

The induction remains within metacyclic p-groups: both subgroups and quotients retain a cyclic normal subgroup with cyclic quotient. The central quotient preserves TPP and the ratio of the product of subgroup orders to the ambient order. The proper pair-generated subgroup step uses the exact intersection with the third factor and a coset injection; it does not assume the triple-product map itself is injective.

TPP is invariant under permuting three subgroup factors: cyclic rotation of a relation and inversion generate all factor permutations. Hence the pair-generation and center-avoidance reductions apply to all three factors. Burnside's basis theorem then supplies three different lines in a two-dimensional Frattini quotient.

For a cyclic normal subgroup N, every intersection with a cyclic factor is characteristic in N and therefore normal in P. A nontrivial such intersection would meet Z(P), contrary to the reduction. One factor surjects onto the cyclic p-group P/N; its trivial intersection with N gives the claimed split extension. The complement acts faithfully because its centralizer of N also centralizes the cyclic complement itself. Thus its order is at most the p-part of |Aut(N)|.

The Frattini coordinates and the power formula are correct. Pair-generation forces the normal coordinate of the second generator to be a unit modulo p. Its order equals its image order in the cyclic quotient, because its cyclic subgroup avoids N. The geometric-sum valuation is strictly smaller than the exponent of N, contradicting the required power relation. At p=2, choosing the factor on the Frattini line (1,0) supplies an even complement coordinate. This parity step is essential: arbitrary odd coordinates allow the dihedral counter-control. No extra semisimplicity, classification of metacyclic groups, or order cutoff is used.

The Sylow-product extension is valid for finite nilpotent groups whose Sylow subgroups are metacyclic. The hypertope consequence retains the earlier, separately proved identification G'=Phi(G), index eight, and the cyclic TPP triple. It is not a statement about all hypertope derived subgroups being metacyclic.

## Program and finite scope

The arithmetic checker was inspected, then copied byte-for-byte to an isolated temporary directory and run there. Its own report was not overwritten. The independent rerun passed 3898 faithful actions, 1020498 forbidden-generator contexts and 4369 direct power-sum cross-checks. The retained JSON report binds the rerun to the exact checker hash. These finite calculations support the power identity; they are not a substitute for the all-parameter proof.

The order-512 GAP script and completed transcript were read. The library's printed range explicitly places all rank-two groups at IDs 2 through 2044, and the script checks order and Frattini index for every entry. The exclusions use the earlier proved class-two and abelian-index-two results. For a cyclic 2-subgroup, a central unique involution is exactly the obstruction to avoiding the center. Enumerating elements outside Phi(P), and identifying their odd-power generators, therefore lists every required cyclic factor in each of the three Frattini classes. Their separate maximum orders give a necessary upper bound for any candidate triple.

The transcript covers 2,043 groups: 4 abelian, 26 further class-at-most-two, 63 further abelian-index-two, and 1,950 remaining. No remaining group has a product of the three class maxima exceeding 512. The TPP-test branch is consequently unused, as the note states. Together with the frozen smaller-order result and the smallest-counterexample reduction, this proves the auxiliary inequality for all 2-groups through order 512, conditional on SmallGroups completeness and exact GAP computation. The derived hypertope range is through order 2^12. I reviewed the search and transcript rather than independently rerunning this GAP census.

No mathematical gap was found in either claimed scope. The only retained boundaries are those already stated: library completeness for the finite census, the earlier hypertope-to-TPP reduction, and written rather than Lean proof of the new theorem.

## Reviewed hashes

- `phase7_cyclic_tpp.md`: `8a9cde4764906e363afdec4e5ac19b5088570daacbb7ed84981a98f7feaba0ab`
- `phase7_cyclic_tpp_arithmetic.py`: `a638ce3d3e2474e3f2dd68c91dbb476ec8be04fa070af859c697194217b3b774`
- `phase7_cyclic_tpp_search.g`: `61de4b6e0de85ee27d088ba5825bfcba61fee470998f5fea5f767eccbe299e4e`
- `phase7_cyclic_tpp_search.log`: `bd28b1dfff48b50431554f42b202d8ff3ebbb32f7fe277dc2dbe2b4d37da89da`
- `phase3_cyclic_tpp_exploration.md`: `f9b3f87ce26939b8870aac1196576cf5e37c94384390450f5b4bb16405090a06`
- `phase3_order_bound.md`: `6426fcc543720e450ec83bcbb55a9a3d9c78a34da8a7687963baabb5ac775d7f`
- `phase7_cyclic_tpp_independent_arithmetic.json`: `4fd1a1d916cc527cea5a9486c2ac7327be5c71e0ca6556c75a30e9543b711dd3`
