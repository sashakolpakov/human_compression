Regular graphs of girth four
===========================

These proof notes give common arguments for minimum orders and an ordinary
isomorphism classification. The proofs have received independent mathematical
review and project acceptance. Their original source editions are preserved;
the preparation status in their front matter predates those reviews.

For finite simple connected regular graphs of degree k >= 3, exact girth four
and exact diameter 4r, with integer r >= 2, the minimum order is

* 2k(r+1), when k is composite;
* 2k(r+1)+2, when k is prime.

``minimum_orders.tex`` proves the bound and gives constructions attaining it.
It uses disjoint neighborhoods along a geodesic, the equality case of the
independent set bound, a divisibility obstruction and explicit graph assemblies.

For degree four there are exactly six graphs at the minimum order 8(r+1),
for every r >= 2. ``quartic_classes.tex`` proves that equality forces a chain
of complete incidences. Removing its intrinsic centre and reversing the chain
reduces the classification to three halves of order eleven. Their six unordered
pairs give the ordinary graph classes. ``diameter_eight.tex`` preserves the
earlier argument from which these proofs developed.

The ``reviews`` directory contains the independent hand reviews. ``REVIEW.json``
records the relative files, their exact identities and the scope of acceptance.
No graph census or literature count is used as a premise. The notes make no
claim of literature novelty, a newly solved conjecture, Lean verification,
completed manuscript intake or a measured compression ratio. F009 still has
a separate order-80 census and final synthesis obligation.

The mathematical development is by the project's coordinating and writing
agents, using standard degree counting, geodesic arguments and graph invariants.
Attribution and full comparisons with the source manuscripts remain separate
audits. These notes are supporting theory for the intake, not final application
papers in the compression programme.
