# Module B: Forest coordinates and primitive coset geometries

Author plan, 10 October 2026. The four-source contract is prospective, not admitted.

The common geometric construction is a tree with positive integer vertex weights. Its edge cuts form a laminar family; partition refinement computes subgroup intersections, and matching Boolean atoms completes flags. Unit weights give the inductively minimal geometries of N001. A distinguished edge, followed by its contraction to a vertex of weight two, gives the second extremal marking family of N003. A star with r leaves of weight k and a central vertex of weight N−rk gives exactly L030's disjoint-k-subset geometry. Thus these three applications have an actual common construction and flag proof.

N008 supplies the complementary primitive coordinate theorem. Residual maximality permits the same relative-generator description of all parabolics, now through U.Relative; U.FrattiniLadder and U.Coset remove the invisible normal subgroup. For a finite p-group the remaining geometry is the coordinate geometry of a vector space. The proof of these shared algebraic results belongs to U and is not repeated in B. All application hypotheses, the alternating-group parity correction, the symmetric-group omission recognition, and the uncolored Kneser graph automorphism proof remain in B.

## Exact intake

- N001, Buekenhout–Cara (1998), four clauses of Theorem 1, all positive ranks. Complete authored browser text, with imperfect mathematical/diagram rendering; no faithful PDF acquired. B97 classification and uniqueness retained in the exact source-recalled form.
- N003, Cameron–Cara (2002), twelve-page author manuscript: all eight numbered principal results, finite-group scope for the general numerical bounds and n≥7 for classification. Whiston bound and its separate CFSG-dependent omission consequence remain retained. Small-degree exceptional remarks are not in this established contract.
- N008, Archer–Cara–Krempa (2005), complete nine-page published PDF: eleven previously reviewed principal/operational assertions. Infinite geometric scope is kept; the unrestricted infinite relative-generation converse is corrected. Gaschütz's quoted earlier theorem and Archer's quoted earlier primitive-group reduction remain identified prior inputs, not newly derived targets.
- L030, Garcia-Colin–Leemans (published 2021), revised institutional author manuscript, exact bytes bound in intake. Theorem 1.2, Corollaries 1.3, 1.4, 4.8 and 5.1, with the construction and all necessary auxiliary distance/residue/automorphism assertions. Do not transfer arXiv-v1 numbering.

N002 (2001), N004 (2003) and L089 (2005) remain excluded: existing partial contracts or primary-text gaps do not justify whole-main-result intake. No repeated broad N002 access search is planned.

## Corrections and scope obligations

L030 has three explicit corrections in this version: (i) panel order is binom(n−k,k)−1; (ii) k=1,n=3 has panel size two, so is thin, whereas all other allowed parameters are thick; (iii) the 63-vertex locally Desargues graph has full graph group S7×S3, not S7. The last conclusion requires reconstructing the type classes of the uncolored graph, and is proved using the inclusion-indicator filtration and equality in the least-eigenvalue bound. None is hidden by reducing the parameter range.

N008's Theorem 2.1 is proved for finite groups or with the maximal-overgroup hypothesis of U.FrattiniTransport; a Prüfer-product counterexample explains the unrestricted infinite failure. Its finite-rank geometric Frattini containment remains valid for infinite groups. The subgroup-family quotient correspondence uses a fixed quotient map and is not an assertion about automorphism-orbit counts.

## Proof and cost organization

B.F is the common weighted-forest theorem; B.P the sign-kernel marking. The symmetric-group branch proves B.Overgroups, B.Minimal, B.Extremal and B.MaxRank. The star branch proves B.Star, B.Distance and B.Aut. The primitive branch proves B.Flags, B.RelativeApplication, B.FrattiniApplication and B.Coordinates. Each source has explicit adapters to these statements.

U dependencies: U.RelativeBound, U.Relative, U.Maximal, U.FrattiniTransport, U.FrattiniLadder and U.Coset. Every U call records its concrete hypotheses in B. U.Geometry is not silently applied to thick coset geometries: the general coset criterion is explicitly retained in the source's precise form. The source general coset correspondence, Cayley's tree formula, symmetric-group inner automorphisms for n≥7 and finite-p-group Frattini quotient are also retained and attributed.

There are no computational proof dependencies for these four all-parameter derivations. Existing finite Kneser diagnostics are optional corroboration only, and will not be rerun unchanged. A later ledger will account for the entire required U dependency closure, B mathematical text, and any genuinely required artifacts. No proof is moved to an unpriced note. No length factor, historical novelty, newly solved open conjecture or full Lean verification is claimed. Normal academic rendering will determine the actual page count after completion; 20–25 pages is an exposition goal, not an excuse to omit proofs.
