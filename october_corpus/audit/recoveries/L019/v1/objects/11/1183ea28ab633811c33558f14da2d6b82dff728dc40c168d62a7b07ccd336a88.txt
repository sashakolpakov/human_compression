# Rank stability and rank gaps: source audit, 2026-10-09

## Conjectures that are no longer open

1. **Symmetric-group high-rank stability is proved.** Cameron, Fernandes and Leemans, *The number of string C-groups of high rank*, Advances in Mathematics 453 (2024), 109832, proves stabilization (up to isomorphism and duality) under `(n,r) -> (n+1,r+1)` for `r >= (n+3)/2`. It computes the stable first seven numbers `1,1,7,9,35,48,135`. This resolves Conjecture 1 in the Leemans survey; it must not be sold as an open target.
   - Author's publication list: https://leemans.dimitri.web.ulb.be/papers.html
   - Primary institutional record: https://research-portal.st-andrews.ac.uk/en/publications/the-number-of-string-c-groups-of-high-rank/
   - Paper: https://doi.org/10.1016/j.aim.2024.109832
2. **The non-perfect-split graph conjecture is false.** Leemans and Mulpas, *Two gluing methods for string C-group representations of the symmetric groups*, Combinatorial Theory 6(1) (2026), #13, disproves the conjecture in Section 5.2 of the above 2024 paper. Graph (X) of its Table 6 fails the intersection property (see Proposition 4.8). The new paper's own Conjecture 4.1 is introduced and disproved within the same paper; it is not an open conjecture.
   - Primary published article: https://escholarship.org/uc/item/1qn7796p
   - Author preprint with readable full text: https://arxiv.org/html/2504.17535v1
3. **Alternating-group rank intervals are proved.** Fernandes–Leemans proves all ranks `3 <= r <= floor((n-1)/2)` for every `n >= 12`; the maximal rank had been settled earlier. Thus the only alternating exception is A11, whose rank spectrum is `{3,6}`. The old transitive-group conjecture about removing alternating groups from the exceptional list is therefore also obsolete.
   - https://arxiv.org/abs/1810.12450

## Significant remaining conjecture

Brooksbank–Leemans Conjecture 5.1 (2019), reproduced as Conjecture 3 in the 2021 survey: **A11 is the only finite simple group whose set of ranks of string C-group representations is not an integer interval.** Empty and singleton spectra satisfy the no-gap condition. It unifies the rank-spectrum classification across finite simple groups and is substantially broader than one computation.

- Original primary source: https://arxiv.org/html/1812.01055v2 (Section 5)
- Survey: https://arxiv.org/html/1910.08843v2 (Conjecture 3)
- 2025 primary paper still calls A11 the unique *known* example: https://oro.open.ac.uk/100498/1/100498.pdf (source independently checked by survey-audit agent).
- No resolution was found in the author's current publication list or targeted searches. This is a literature-search conclusion, not a proof that no unpublished or unindexed resolution exists.

## Elementary rigorous narrowing, not a solution

If a group has 2-rank `e` (maximum dimension of an elementary abelian 2-subgroup), any string C-group representation has rank `r <= 2e`. Indeed, the generators of even indices commute, and the intersection property makes them independent, so they generate an elementary abelian subgroup of dimension `ceil(r/2)`. Consequently, if rank 3 is present and `e <= 2`, no gap is possible: the only permitted ranks are 3 and possibly 4. This observation is elementary and no novelty is claimed.

The standard reduction of `[a,b,c,d]` to `[b,ac,d]` always has the intersection property for the subgroup it generates, assuming the original rank-four representation is irreducible. The two rank-two parabolics have intersection contained in `<a,c>`; a larger intersection than `<ac>` would force the irreducible rank-three group `<a,b,c>` to be dihedral. This is already implicit in the base-case proof of Brooksbank–Leemans. The unresolved issue is preserving generation of the original group; in higher ranks there are additional intersection obstructions. Merely checking that adjacent generators have the required orders does not prove the conjecture.

Work on this direction was paused to independently audit a more concrete construction found by the recent-conjectures agent. No new rank-gap theorem or counterexample is claimed.
