# What the phase256 Lean file verifies

`formal/HomologyCoverAvoidance.lean` contains five proved declarations.
There are no additional axioms, unfinished proofs, or native decision calls.

| Declaration | Mathematical statement | Use in the manuscript |
|---|---|---|
| `affine_line_unique` | If u is outside a vector subspace S, at most one scalar a puts au+x in a specified affine coset of S. | Lemma 7, one forbidden scalar per visited end fiber. |
| `exists_avoiding_affine_translates` | A family of transverse affine constraints indexed by fewer elements than a finite field cannot exclude every scalar. | Lemma 7, finite union bound. |
| `exists_avoiding_two_subspaces` | For n visited vertices and two subspaces, a permitted scalar exists when 2n is smaller than the field. | Exact two-end specialization. |
| `path_constraint_bound` | L≤2g−1 and p>4g imply 2(L+1)<p, for g>0. | Spanning-tree loops. |
| `odd_repetition` | Repeating an odd-length walk an odd number of times preserves odd parity. | Lemma 8. |

The file does not define surfaces, cellular homology, deck coverings or
polytopes. In particular it does not assume an opaque predicate meaning
that the desired cover exists, and does not claim a formal proof of the
whole theorem. The geometric identification of V_A and V_B, the boundary
membership test, connectedness of the actual complement, the homological
intersection argument, and the regular-polytope correspondence are proved
in the manuscript, with the stated classical background.

Replay uses Lean4.32.2 and mathlib revision
905b95818eb32af7874a58b427f50c1711a5e96c. Each declaration's axiom report is
restricted to `propext`, `Classical.choice`, and `Quot.sound`. Three altered
assumptions are tested and must fail compilation. The finite program also
rejects coincident distant marks under Python optimization.
