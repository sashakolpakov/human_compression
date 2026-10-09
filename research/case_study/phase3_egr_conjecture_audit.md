# The generalized-polygon EGR conjecture: a construction and literature audit

9 October 2026. The existential statement in Araujo-Pardo–Leemans, [arXiv:2108.06636, Conjecture 4.5](https://arxiv.org/abs/2108.06636), asks for graphs with parameters

    egr(2 q^(d−1), q, 2d, (q−1)^(d−1)(q−2)),  d=4,6.

The corresponding extremality assertion is already disproved by Goedgebeur–Jooken; that does not settle this existence statement. This note also does **not** disprove the existence statement. It checks the proposed construction and a later claimed partial resolution.

## 1. Conflicting primary sources

Porupsánszki, [*On edge-girth-regular graphs: lower bounds and new families*, arXiv:2305.17014, Theorem 2.5](https://arxiv.org/html/2305.17014), gives the chamber-deleted generalized-quadrangle graph the parameter

    λ=(q−1)²((q−2)²+1).                                 (1)

Yang–Sun–Zhang, [*The edge-girth-regularity of Wenger graphs*, arXiv:2311.04401v1, Theorem 1(2) / Theorem 3.3](https://arxiv.org/html/2311.04401), claims instead that the Wenger graph W₂(q) has parameter `(q−1)³(q−2)` for odd q, and explicitly presents this as a partial answer to the Leemans conjecture. Their even-q formula simplifies to (1). The downloaded [Wenger paper](https://arxiv.org/pdf/2311.04401v1) preserves the primary statement checked here. The [current arXiv version history](https://arxiv.org/abs/2311.04401), checked on 9 October 2026, lists only v1, submitted 8 November 2023. A targeted search located no corrected or journal version. Porupsánszki's [15-page final published version](https://amc-journal.eu/index.php/amc/article/download/3107/2122), [AMC 25 (2025), #P4.07](https://doi.org/10.26493/1855-3974.3107.9df), retains formula (1) in Theorem 2.5; the final PDF was downloaded directly from the journal and checked. Source and certificate hashes are in [the machine-readable manifest](phase3_gq_certificate.json).

The characteristic-free proof below gives (1) for the exact defining Wenger graph, including odd q. Thus the claimed odd-q construction-based resolution in that version cannot be used as a valid resolution of Conjecture 4.5. The existence of some other graph with the desired parameters remains a separate question.

## 2. Exact graph and coordinate conversion

The recursive model in Example 2.2 of the Wenger paper has points `(x,u,v)` and lines `[y,r,s]`, with incidence

    u+r=xy,              v+s=xr.                        (2)

Change the point's third coordinate to `V=v+xu`, and then exchange the two vertex types. Equation (2) becomes the moment model

    u+r=xy,              v+s=xy².                       (3)

Explicitly, a source point `(x,u,v)` becomes the target line `[x,u,v+xu]`, and a source line `[y,r,s]` becomes the target point `(y,r,s)`. This is a bijection preserving every edge, in every characteristic. The computation checks this map on every edge at q=3,5,7.

There are 2q³ vertices, and each vertex has q neighbours. The graph is edge-transitive without any characteristic restriction. For example, (3) is preserved by the following transformations:

* Add constants α,β to u,v and subtract them from r,s.
* Replace x by x+a and replace `(r,s)` by `(r+ay,s+ay²)`.
* Replace y by y+b, `(u,v)` by `(u+bx,v+2bu+b²x)`, and s by `s+2br`.

Given any edge, the second transformation first makes x zero, the first makes the point zero and the line's last two coordinates zero, and the third then makes y zero. Thus it suffices to count cycles through the all-zero edge.

## 3. Uniform moment-matrix cycle count

Consider an oriented 8-cycle whose first edge is the zero point followed by the zero line. Let its successive line first coordinates be

    y₀=0, y₁, y₂, y₃,

and let d_i be the change in the point first coordinate across line i. Closure is equivalent to

    Σd_i=Σd_i y_i=Σd_i y_i²=0.                          (4)

Each d_i must be nonzero. Adjacent y_i, including cyclic adjacency, must differ. These are exactly the non-backtracking conditions: once a first coordinate is fixed, the incidence equations uniquely determine the other coordinates. Conversely, any solution of (4) satisfying them constructs one closed non-backtracking walk beginning with the fixed oriented edge.

The same Vandermonde argument for two or three lines rules out 4- and 6-cycles. A 4-cycle would have two distinct y-values and a rank-two matrix; a 6-cycle would have three distinct y-values and a rank-three matrix. Neither permits all nonzero d_i. Therefore any non-backtracking closed walk of length eight is a genuine 8-cycle.

Group the four columns of the 3×4 matrix in (4) by their y-values.

* **Four distinct values.** There are `(q−1)(q−2)(q−3)` choices of the ordered y₁,y₂,y₃. The matrix has a one-dimensional kernel, and every coordinate of a nonzero kernel vector is nonzero, since every three columns are independent. Hence each choice gives q−1 cycles.
* **Three distinct values.** After combining the repeated columns, the three distinct Vandermonde columns are independent. The coefficient on each singleton column must be zero, which is forbidden. Hence there are no cycles of this kind.
* **Two distinct values.** Cyclic adjacency forces `(y₀,y₁,y₂,y₃)=(0,y,0,y)`, with y nonzero. Equation (4) is exactly `d₂=−d₀` and `d₃=−d₁`. The choices y,d₀,d₁ are independently nonzero, giving `(q−1)³` cycles.

Every unoriented cycle through the fixed edge has exactly one traversal beginning with that fixed oriented edge, so there is no extra factor of two. Consequently

    λ=(q−1)²(q−2)(q−3)+(q−1)³
      =(q−1)²(q²−4q+5)
      =(q−1)²((q−2)²+1).

This is positive for every prime power q, proving girth eight as well as the exact count. In particular it differs from the conjectured parameter by

    λ − (q−1)³(q−2) = −(q−1)²(q−3).

The two counts agree at q=3, but disagree for every q>3, odd or even.

The same short argument recovers the other Wenger girth formulas from the moment representation. Here is the coordinate conversion for every n. Write the recursive equations as `l_i=x l_(i−1)−p_i`, where x=p₁. They imply

    l_i + Σ_(j=2)^i x^(i−j) p_j = x^(i−1) l₁.

The triangular change `P_i=Σ_(j=2)^i x^(i−j)p_j` is invertible (its diagonal coefficients are one). Exchanging vertex types gives the moment equations `p_i+l_i=p₁ l₁^(i−1)`, for i=2,...,n+1. Edge normalization works as above: translation of the line parameter expands by the binomial theorem and induces an invertible triangular change of the other coordinates. Thus the all-zero edge count applies to every edge.

For W₁(q), the 2×3 moment matrix gives girth six and λ=`(q−1)²(q−2)` when q≥3; W₁(2) is an 8-cycle. For W_n(q), n≥3, the four-distinct-column case also has full rank, leaving precisely `(q−1)³` 8-cycles through an edge. Thus the argument compresses the whole classical-Wenger girth-counting statement into one rank calculation, while correcting its W₂ odd-characteristic case. It does not count the separate linearized Wenger family.

## 4. Independent exact checks

[phase3_gq_cycle_check.py](phase3_gq_cycle_check.py) constructs three graphs independently: the chamber deletion in the symplectic generalized quadrangle W(3,q), the exact recursive model (2), and the moment model (3). The symplectic model constructs every projective point and every totally isotropic line directly from the alternating form, and deletes the vertices at distance at most two from a chosen chamber edge.

The script checks orders, degrees and girth. It then counts cycles through four sample edges by explicit simple-path recursion, and independently checks the first edge by matching two internally disjoint length-three paths across their middle edge. It verifies the explicit recursive-to-moment isomorphism on every edge. All checks pass; the reproducible [JSON results](phase3_gq_cycle_check.json) are:

| q | vertices | exact λ in all three models | claimed odd-q λ |
|---|---:|---:|---:|
| 3 | 54 | 8 | 8 |
| 5 | 250 | 160 | 192 |
| 7 | 686 | 936 | 1080 |

These finite checks corroborate the all-q proof; they are not a substitute for it. The generalized-quadrangle formula was already published by Porupsánszki, so no priority is claimed for that formula. The literature discrepancy and the proposed elementary proof have received only internal checking so far.

## 5. Separate exploratory hexagon calculation

[phase3_hexagon_probe.py](phase3_hexagon_probe.py) separately implements the four equations for the five-coordinate Lie graph displayed in the Wenger paper's Section 2. It builds only the two depth-five non-backtracking branches from a fixed zero edge, and counts connecting edges between their boundaries. The [exact output](phase3_hexagon_probe.json) gives 36, 1680, 24660 and 678900 cycles at q=3,5,7,11 respectively. The conjectured values are 32, 3072, 38880 and 900000.

These are local facts about that explicitly defined graph. No generalized-hexagon identification, global girth, connectivity, or universal formula is asserted from these probes, particularly in bad characteristic. They supply no counterexample to the existential Conjecture 4.5 and are kept separate from the proved Wenger result above.
