# Recent Leemans conjecture audit

Checked 9 October 2026. Primary sources inspected include the author's [publication list](https://leemans.dimitri.web.ulb.be/papersbyyear.html), linked arXiv papers, and institutional manuscripts. “No resolution found” is not a guarantee that no unpublished or unindexed solution exists.

## 1. Brooksbank–Leemans rank-spectrum conjecture

Conjecture 5.1 of [Rank reduction of string C-group representations](https://arxiv.org/pdf/1812.01055), Proc. AMS 147 (2019), 5421–5426: A11 is the only finite simple group whose ranks of string C-group representations fail to form an integer interval.

This is a significant structural conjecture connecting regular abstract polytopes to all finite simple groups; a proof needs to control attainable ranks rather than just one representation. No general resolution was found in the searched literature through the stated date. The 2026 Leemans–Vandenschrick paper [On simple groups that admit a string C-group representation](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf) classifies which simple groups admit any representation. It does not itself determine each group's full rank spectrum.

For purposes of this conjecture, empty spectra must be treated as intervals or excluded. The intended nontrivial case is groups admitting a representation. A11 has ranks {3,6}, while the previously conjectured alternating maximal rank was resolved in 2017.

## 2. Non-tight chiral polyhedra of order 2p^m: concrete new-range candidate

Kong–Feng–Hou–Leemans–Qu, [Chiral 3-polytopes of order 2p^m](https://amc-journal.eu/index.php/amc/article/download/3716/2232), 22-page manuscript accepted 19 January 2026, DOI 10.26493/1855-3974.3716.b64; [earlier arXiv version](https://arxiv.org/abs/2508.20654).

Theorem 1.4 constructs non-tight examples when m>=5 is odd, or m is even and m>=p+3. This leaves even 6<=m<=p+1 for odd prime p. The first case is p=5,m=6, group order 31,250. The later manuscript's concluding remark explicitly identifies this gap but appears to contain a typo “tight” for “non-tight”.

This is a smaller, concrete research problem with a clear contribution: completing the existence classification by group order. It is not comparable in breadth to the rank-spectrum conjecture. A central cyclic lift discovered in this session appears to fill its full missing range. See [central_lift_proof.md](central_lift_proof.md) and [central_lift.g](central_lift.g). The proof received internal agent reviews, not external peer review, and exact GAP checks passed p5m6, p7m6, p7m8. Novelty remains provisional.

## 3. Chiral existence for PSU(3,q)

Leemans–Vandenschrick, [On chiral polytopes having a group PSL(3,q) as automorphism group](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf), JLMS 106 (2022), 85–111, concluding section.

The final institutional manuscript identifies PSU(3,q), q>17, among groups for which chiral-polytope existence remains unknown; it supplies examples at q=11 and q=17 and excludes listed smaller q. Any such polytope has rank 4 or 5. This is a significant remaining family in the finite-simple-group existence program, but it is an open classification problem, not a precise uniform-existence conjecture stated there. No newer resolution was found by targeted searches. The old arXiv version omits the q=17 update, so use the final manuscript.

The same conclusion refers residual PSL(2,q) cases to the 2017 Leemans–Moerenhout–O'Reilly-Regueiro conjecture. These deserve separate exact statement/status verification before choosing them as targets.

## 4. Exclusions: conjectures already solved

* Highest possible regular-polytope rank for alternating groups: Cameron–Fernandes–Leemans–Mixer, *Highest rank of a polytope for A_n*, Proc. LMS 115 (2017), 135–176, resolves the 2012 conjecture.
* Stabilization of numbers of high-rank symmetric-group string C-groups: Cameron–Fernandes–Leemans, [The number of string C-groups of high rank](https://arxiv.org/abs/2212.12723), Adv. Math. 453 (2024), 109832, proves the earlier conjecture.
* All chiral polytopes with Suzuki simple automorphism groups have rank three: Spiga, [On the rank of Suzuki polytopes: an answer to Hubard and Leemans](https://arxiv.org/abs/2010.04080), Discrete Math. 2021, proves the Hubard–Leemans conjecture.
* Leemans–Vandenschrick 2022 already provides rank-four chiral PSL(3,q) polytopes for every q>=5 and excludes ranks>=6 for PSL(3,q), PSU(3,q). Do not present those as open.
* Zhang–Leemans, [Testing chirality on hypertopes](https://arxiv.org/abs/2511.14562), J. Algebraic Combin. 63 (2026),61, gives the group-theoretic chirality test; its older motivating algorithmic obstacle is not an unsolved conjecture after this paper.

## Search caution

An indexed search result advertises *Hypertopes with prescribed diagram symmetries*, arXiv:2610.09711. Its exact submission date must be checked against 9 October 2026 before using it; it was not needed for this audit.
