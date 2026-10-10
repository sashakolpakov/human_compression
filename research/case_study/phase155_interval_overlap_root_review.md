# Interval-overlap cancellation: independent proof review and admission

Reviewed on 2026-10-10. Root read the complete natural-number Lean proof,
the complete finite-marker adapter, both scope notes and both compilation
and control programs. The mathematics was checked against the interval
argument used by the written parity-mixing proof. This is independent of
the author of these formal modules; it is not external peer review or an
admission of the unfinished group application.

The unchanged core manifest has SHA-256
`83ea1fd8fe05abe9c404b459ff1adc0d0328df788456a712a1f2423171df9c90`;
the adapter manifest has SHA-256
`b4c9a0dd27e9c31bd6e8f161a935ae8072e65c1784160e123693cc2474905b1c`.

## Proof and hypotheses

The core considers two finite families of finite, order-convex subsets of
the natural numbers. Sets within each family are pairwise disjoint.
The first lemma shows that, for overlapping intervals, the earlier right
endpoint belongs to the other interval. The overlap supplies the necessary
nonemptiness, so the supremum convention for an empty finite set creates
no omitted case.

The second theorem allows any nonempty edge relation supported on these
overlaps. It chooses an edge minimizing the smaller of its two right
endpoints. That endpoint lies in every interval adjacent to the selected
earlier-ending interval. Internal disjointness in the opposite family
therefore leaves exactly one neighbor. This proves the leaf property for
every nonempty subgraph of the overlap graph; no forest property is an
assumption.

The final core theorem gives a weight in any additive commutative monoid
to each pair, with zero weights on disjoint pairs and zero row and column
sums. Apply the preceding leaf theorem to the edges with nonzero weight.
At its leaf, the row or column sum is just the selected nonzero weight,
contradicting the zero-sum hypothesis. Thus all weights vanish. This needs
neither additive cancellation nor subtraction; finite index types,
intervals and one or both families may be empty.

Convexity and internal pairwise disjointness are substantive hypotheses.
Dropping either can create a four-cycle with nonzero weights over Z/2Z
and zero row/column sums, as the author scope explains. The theorem does
not assert zero-sum cancellation for arbitrary bipartite graphs.

The adapter proves that taking `Fin.val` images of finite subsets of
`Fin n` preserves order-convexity and preserves and reflects disjointness.
A natural number between values a and b satisfies z <= b.val < n and
therefore determines an element of `Fin n`; this discharges convexity
without assuming a nonempty ambient type. Injectivity of `Fin.val`
discharges both disjointness implications. Applying the unchanged core
theorem then yields the exact finite-marker statement, including n=0.
Weights and sums are unchanged by this transport. No group-theoretic
premise or stronger cancellation hypothesis has entered through the
adapter.

## Fresh builds and reproduction

Root freshly ran the dedicated core build and its isolated portable replay;
all seven controls passed. Root separately ran the adapter build, which
first recompiles the unchanged core, and its isolated five-input replay;
all nine controls passed. The reports are
[core build](phase155_interval_overlap_root_build.json),
[core controls](phase155_interval_overlap_root_controls.json),
[adapter build](phase155_fin_interval_root_build.json) and
[adapter controls](phase155_fin_interval_root_controls.json).
Each run uses a new output directory. The controls reject occupied paths
and changed bound inputs and verify that retained inputs remain unchanged.

The exact public copies were then freshly compiled with the generic runner,
compiling the core before the adapter. All six declaration audits use only
subsets of `propext`, `Classical.choice` and `Quot.sound`, with no placeholders
or native-evaluation axioms. Lean 4.32.2 and the dependency revisions were
checked. The installed compiler and compiled standard-package objects
remain trusted; they were not all rebuilt.

The source hashes are:

- `IntervalOverlapCancellation.lean`:
  `7a1072ffb966606b7d0371b7c123220a0498d00a2299b8c76f5ccb7c2f8f4ae5`.
- `FinIntervalOverlapCancellation.lean`:
  `a951b853c7a33512a2d0293bdef7f8c101d4f1dcf55d8a87482d38fbb3851417`.

Admission covers the complete interval theorem and its representation
adapter. The parity-mixing consumer must still construct the actual group
coordinates and weights and prove the two sum identities. No full mixed
intersection property, finite-field construction or polytope theorem
follows from the certificates alone. This supplies reusable formal proof,
not a historical-novelty claim, another solved conjecture, source coverage
or a compression factor. The adapter is counted as a separate scoped
module, not as a separate research result. Frozen author status labels
retain their historical meaning.
