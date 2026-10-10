# Odd-prime family: source and proof ledger

Author package, 10 October 2026. Complete independent review is pending. The theorem concerns one specified infinite family; it is not a new compression claim for the whole older classification paper.

## Source contract

The input family is the Γ1 row of Table 2 and Theorem 4.7 in the author version of Cunningham–Pellicer, *Tight chiral polytopes*, arXiv:2009.04566, printed pages 22–26. The published work is J. Algebraic Combin. 54 (2021), 837–878, DOI 10.1007/s10801-021-01023-z. Numbering here explicitly refers to the checked author version, not an assumed identical journal numbering.

Parameters are an odd prime p, α≥2, k1=k2=k with 1≤k≤p−1, and type {2p,p^α,2p}. The exact bare rotation presentation is (5) in the manuscript. This is the first chiral-facet/chiral-vertex family in Table 4, and the first family considered in Example 3.5 of Cunningham's subsequent smallest-regular-cover paper. The theorem does not concern every polytope of that Schläfli type.

The earlier theorem's complete identification of that presentation with the tight chiral polytope P is retained. In particular, it supplies the exact generator orders, group order 4p²q, unique tight normal form, and source intersection property. Its proof uses the earlier atomic-polyhedron classification (Table 1), the amalgamation and permutation-recognition argument of Lemma 4.6, and the atomicity criterion Corollary 4.5. None of that source-specific work is silently charged to the new quotient lemma or to finite sampling. Atomicity itself is not used in the new argument after P is identified. The chirality-group Proposition 4.2 is also not needed for the new construction: normality of ⟨b^(q/p)⟩ and the full mirror mix are proved directly from (5).

The relevant primary presentation table, all of the Theorem 4.7 argument, and its local setup were read through web extraction for this task. The saved extraction files record that access. They are not local PDF-byte bindings or a claim to have reread the entire 43-page paper. The older source-version limitations of phase41 remain explicit. No new literature-priority search is contained in this package.

## Obligations

| Claim | Evidence | Retained input or limitation |
|---|---|---|
| P exists with the exact presentation, orders and IP | Source Theorem 4.7 and tightness | Retained all-parameter theorem, including its older classification dependencies |
| x normal; coordinate identities (6) | Literal relation manipulation in §2 | Uses p odd and k nonzero |
| Mirror on P/⟨x⟩ | Check of all quotient defining relations | No assumed global chirality-group theorem |
| R full twisted fiber product, order and unique normal form | Explicit facet relator generates 1×⟨x⟩; matching upper bound | Source normal form of P retained |
| F,V and exact bad intersection | Projection kernels and source IP | Rank-three C+ recognition retained |
| W≅C_p² and W is normal closure of C² | Independence via source cyclic IP, full action table | No guessed dimension or sampled extrapolation |
| T directly regular and J normal/mirror-stable | Explicit reflection extension and exact end intersection | Standard group/polytope correspondence retained |
| R/W≅T/J and largest common quotient | Unique index-two normal forms and literal C action | Actual subgroup equality W∩F=J already proved |
| Q=R⋄T order and polytopality | Full fiber-product lemma and explicit end-lift comparison | No assertion that arbitrary mixes preserve IP |
| Global minimality | Prime degree above the universal smallest regular maniplex | Covers and isomorphisms preserve ranks |
| Q′ exists and differs from Q | Presentation duality, universal-cover duality, distinct conjugation characters | They may be identified only by reversing the ranks; no claim of different abstract groups |
| H order, exact two-cover interval, global join-density | Distinct one-dimensional kernel modules and local injection | Does not classify covers outside H |

The geometric inputs retained throughout are recursive string-C/C+ recognition, the marked group/polytope correspondence, and the universal marked-kernel description of the smallest regular maniplex cover. They are distinct from the new all-parameter group calculations.

## Diagnostics and exclusions

`phase49_cover_family_check.g` independently rebuilds the source groups from the bare presentations in eight finite cases: p=3, α=2 or 3, both nonzero k; and p=5, α=2, all four nonzero k. It verifies the actual word identities, subgroup equalities, normal closures, marked quotient isomorphisms, cover maps, intersection properties, and conjugation/mirror signs. Stock exact GAP algorithms are retained. These computations are diagnostics for the written proof, never an all-parameter inference.

`phase49_cover_family_check.py` requires fresh `--report` and `--log` outputs, uses an isolated temporary execution directory, and verifies that every bound phase41/44/46/48 file remains unchanged before and after the run. The earlier exploratory `phase49_cover_family_probe.g` is excluded from the certificate intake.

No new Lean theorem is claimed for this family. The frozen phase48 algebraic criterion supplies a related formal core, but the normal forms, cover geometry, and family construction here are written mathematics. The other four source families and the general arbitrary-monodromy multiple-cover problem remain unresolved by this package. No literature-priority claim is made.
