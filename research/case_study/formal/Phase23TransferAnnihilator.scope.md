# Exact saved-graph transfer identities, with native evaluation

This module checks the integer arithmetic of the frozen third-excess transfer graph. It does not formalize the group classification or the proof that this graph enumerates the relevant marked groups.

The input graph is `phase22_excess3_final.graph.json`, SHA256
`b3cf789f5278c773636a9e440a06115dd023b11c0519bbe3c68a51ce33b3c0d6`.
The module contains all 706 initial rows and all 1,522 edges as literal Lean arrays. Its state count is 708. It does not read the graph, Python output, GAP output or any other file at theorem-checking time.

## Precisely checked statements

Vectors are integer arrays of length 2,832. Coordinate `4*(s-1)+k` means state `s` and excess `k`, where `1 ≤ s ≤ 708` and `0 ≤ k ≤ 3`. The operator uses column vectors. For each edge `(s,t,w)`, it adds input coordinate `(s,k)` to output coordinate `(t,k+w)` when `k+w ≤ 3`. It discards higher excess. All additions use unbounded integers.

The initial vector `v5` counts the embedded initial rows, and `v7 = T(T(v5))`. With `delta(v) = T(v)-v` and `e` the coordinate vector for state 1, excess 3, the module checks:

- `dimension = 2832`, 706 initial rows and 1,522 edges;
- `delta(delta(delta(v7))) = 125*e`;
- `T(e) = e`;
- `delta(delta(delta(delta(v7)))) = 0`;
- summing excess-three coordinates of the first four difference vectors gives `[2499, 1780, 715, 125]`.

These are complete array equalities, not equality of total counts alone. The four arithmetic propositions have no hypotheses. The dimension/count assertion uses kernel reduction.

## Additional trust from `native_decide`

The four larger arithmetic claims use Lean's `native_decide`. The compiler/interpreter evaluates the decidable proposition, and Lean records a generated native-evaluation axiom for that result. The saved `#print axioms` output explicitly lists one such axiom for each of:

- `third_difference._native.native_decide.ax_1_1`;
- `terminal_basis_fixed._native.native_decide.ax_1_1`;
- `fourth_difference._native.native_decide.ax_1_1`;
- `newton_coefficients._native.native_decide.ax_1_1`.

Each also lists the ordinary axioms `propext` and `Quot.sound`. The dimension/count assertion has no axioms. There is no `sorryAx`. This is **not a kernel-only arithmetic certificate**, and its additional compiler-evaluation trust must not be silently merged with the standard-axiom-only certificates elsewhere in the project.

Two bounded kernel-only attempts, including one that supplied separately checkable intermediate arrays, exceeded the private runner's 120-second limit. The final module uses the smaller direct native calculation. Those unsuccessful attempts are not evidence for the final theorem statements; the successful final compilation is recorded separately.

## What remains written or computationally retained

The all-rank consequence in `phase22_excess3_annihilator.md` also uses linearity of this transfer and the binomial expansion for `T = I + delta`. Those general algebra steps are not asserted by this module. Neither are the finite-state reconstruction theorem, the universal-group and kernel censuses, the compatibility tests, or the group-to-graph bijection. The separate rank-four count also remains an external certificate. In particular, this module alone does not prove the all-rank polytope enumeration theorem.

The generator is a data renderer, not a proof oracle. A separate standard-library checker compares the two embedded arrays with the frozen graph byte-for-byte at the decoded row level and verifies that the saved successful compile report binds the current Lean source. The original Python annihilator checker and the independently implemented root calculation provide additional arithmetic checks with separately stated trust boundaries.

## Reproduction

From the private research directory, with the existing pinned dependency checkout:

```sh
python3 phase23_transfer_lean_generate.py
python3 formal/verify_lean.py Phase23TransferAnnihilator.lean
python3 phase23_transfer_lean_data_check.py
```

The generator accepts explicit `--graph` and `--output` paths. The data checker accepts explicit `--inputs`, `--source`, `--compile-report` and `--output` paths. It uses only the Python standard library. Regeneration must reproduce the exact Lean source hash recorded by the companion manifest. The existing verifier supplies the pinned Lean and mathlib environment; no change to that runner or any historical certificate is required.

This is an internal formal-methods supplement. It is not external peer review or a claim of publication priority.
