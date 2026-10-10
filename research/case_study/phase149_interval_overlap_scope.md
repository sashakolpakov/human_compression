# Vanishing overlap weights for two families of disjoint intervals

Let `(L_j)` and `(R_k)` be two finite families of finite subsets of the natural numbers. Every member is order-convex: if it contains `x ≤ y`, it contains every integer between them. Different members of the same family are disjoint. Empty members are allowed. Let `w(j,k)` lie in an additive commutative monoid, and suppose it is zero when `L_j` and `R_k` are disjoint. If every row sum and every column sum of `w` is zero, then every `w(j,k)` is zero.

This is the exact statement of `MathCompression.IntervalOverlapCancellation.weights_eq_zero` in `formal/IntervalOverlapCancellation.lean`. In particular, the result applies to parity weights in `ZMod 2`. It does not assume additive cancellation, that the weights are nonnegative, or that the overlap graph is a forest. The two finite index types may be empty. Indices for distinct empty intervals need not be identified.

## Complete proof

For a nonempty finite set `S`, write `r(S)` for its largest element. If intervals `S,T` intersect and `r(S) ≤ r(T)`, choose `x` in their intersection. Then `x ≤ r(S) ≤ r(T)`, and order-convexity of `T` gives `r(S) ∈ T`. This is `endpoint_mem`. The implementation uses `Finset.sup id`, which is defined even for the empty set; the intersection hypothesis provides nonemptiness whenever the endpoint argument is used.

More generally, retain any nonempty collection of overlap edges. Choose an edge `(j,k)` minimizing `min(r(L_j), r(R_k))` among retained edges. Suppose first that `r(L_j) ≤ r(R_k)`. Every other retained edge `(j,k')` has `r(R_k') ≥ r(L_j)` by minimality. The endpoint observation places `r(L_j)` in both `R_k` and `R_k'`. Disjointness within the right family forces `k'=k`. Thus `L_j` is incident to exactly one retained edge. If `r(R_k) ≤ r(L_j)`, the symmetric argument gives a right vertex with exactly one retained edge. This proves `exists_leaf` for every nonempty edge subgraph, deriving the relevant forest property from the intervals themselves.

Now retain exactly the edges with nonzero weight. If any exist, the leaf statement supplies one whose row or column has exactly one nonzero entry. The sum along that row or column equals that entry by the additive identity law. Its assumed zero sum therefore makes the entry zero, a contradiction. This proves `weights_eq_zero`. No subtraction and no recursive removal of vertices is necessary.

## Hypotheses and application boundary

Both the interval and the same-family disjointness conditions matter. Without order-convexity, take left sets `{0,2}`, `{1,3}` and right sets `{0,1}`, `{2,3}`. Every pair from different families intersects, while each family is disjoint. Assigning all four weights the value `1` in `ZMod 2` gives zero row and column sums but nonzero entries. Without same-family disjointness, duplicate the singleton `{0}` twice in each family to obtain the same counterexample with intervals.

The intended application uses the actual interval components of two marked supports and weights measuring their overlap parity discrepancy. This module proves the complete interval argument; the separate group assembly must still derive the weights, their zero row and column sums, and the parity-fiber interpretation from its group hypotheses. No group construction, mixed intersection property, finite-field choice, orthogonal-group identification or polytope theorem is a premise or conclusion of this module. It does not certify the whole source conjecture. The exact natural-number formulation is sufficient for finite marker indices; no claim about an arbitrary ambient ordered set is needed.

This is a new formal proof within the repository of an elementary interval fact used in the previously written parity-mixing proof (`phase124_even_label_mix.md`). It is not a claim of historical novelty. The proof pattern is the classical earliest-right-endpoint leaf argument, here applied directly to the support of nonzero weights. This package belongs to the formal verification of question-solving work, separately from compression of published principal results.

## Replay and trust boundary

Run `python3 -O phase149_interval_overlap_check.py --packages PACKAGES --lean LEAN --output-dir NEW`, with the exact package checkouts listed in `formal/dependency_manifest.json` and Lean 4.32.2. The default source directory is the sibling `formal` directory. The runner requires a new output path, checks exact source/dependency hashes, package revisions and tracked cleanliness, copies the source, compiles it, and validates three axiom reports. All three use only `propext`, `Classical.choice` and `Quot.sound`; there is no `sorryAx`, new axiom or native evaluation certificate. The installed compiler and cached compiled standard-package objects remain trusted. The fresh build does not claim those caches were rebuilt.

The output directory contains the exact copied Lean source and dependency manifest, the fresh compiler object, build log and JSON report. The control script checks refusal of occupied paths, modified bound inputs, and a replay from an isolated portable layout. No primary-source PDF, private group model or predecessor proof is needed to reproduce the interval certificate.
