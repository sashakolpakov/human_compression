# Independent audit of the missing Suzuki lattice

10 October 2026. Internal reviewer: the recent-conjectures agent, separate from the authoring survey agent and the root reviewer. This is a source-hypothesis, mathematical and executable review, not external peer review or a priority determination.

**Conclusion:** the explicit rank-three configuration is a counterexample to the asserted completeness of the printed L114 Theorem 5.5 list and its L110 Theorem 3 restatement. The supplied matrix certificate and all source RWPRI conditions check. The example is also firm, residually connected and flag transitive under the designated Suzuki group. Neither the rank-two geometric intersection property nor a replacement exhaustive classification has been established here.

## 1. Exact source hypotheses

The primary sources are Leemans, [*The rank 3 geometries of the simple Suzuki groups Sz(q)*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837), Note di Matematica 19 (1999), 43–63 (L114), and [*The residually weakly primitive pre-geometries of the Suzuki simple groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995), Note di Matematica 20 (2000/01), 1–20 (L110).

I reread the source definitions, the applicable classification branch and its residue discussion. I also visually checked L114 printed pages 46, 59 and 60, rather than relying on OCR for the key inequalities and subgroup labels.

- L114's introduction explicitly allows geometries which are not flag transitive. On page 46, RWPRI means that for every proper type subset J, some unused type i makes the intersection G_(J∪{i}) a maximal subgroup of G_J. L110 pages 4–5 repeat this definition.
- The separate local two-transitivity condition is not a hypothesis of L114 Theorem 5.5 or L110 Theorem 3. No geometric intersection axiom is included in these theorem hypotheses.
- L114 page 47 reserves the phrase “of Suzuki type” for simple Suzuki groups and excludes Sz(2) from that terminology. This does not forbid Sz(2) as an intersection of simple subfield groups.
- For the field exponent 15=3·5, the sum of its prime exponents is two. Only shapes 1–5 in L114 apply. The sole matching maximal-parabolic pattern is shape 5, which explicitly gives the meet of the two simple Suzuki groups as C4×C2, of order eight. L110 repeats it as R8.
- L114 shape 8 is in the branch where the sum of the exponent multiplicities exceeds two. Substituting t=2 and a torus parameter one there would not put the proposed rank-three example into the applicable branch.

Thus lack of flag transitivity cannot explain the missing entry. In any event, flag transitivity follows directly below.

## 2. Exact subgroup lattice and all maximality checks

Set G=Sz(2^15), S=Sz(8), T=Sz(32), and K=C533:C4 in the simultaneous standard coordinate position supplied by the certificate. Write B=C4 for the triple intersection. The intersections are

| Meet | Order | Structure |
|---|---:|---|
| S∩T | 20 | Sz(2)=C5:C4 |
| S∩K | 52 | C13:C4 |
| T∩K | 164 | C41:C4 |
| S∩T∩K | 4 | C4 |

The standard subfield maximality theorem makes S and T maximal in G, since their field extension degrees are respectively five and three. The torus normalizers C13:C4 and C41:C4 are maximal in Sz(8) and Sz(32), respectively: 13=8+4+1 and 41=32+8+1 are the full nonsplit torus orders. These are retained classical Suzuki subgroup results; neither the source's disputed candidate completeness nor a computer subgroup catalogue is needed.

There are seven proper subsets J of the three types. For J empty use S<G. For J={S} or {T}, use its torus-normalizer intersection with K. For J={K}, use S∩K, of index 41. For each two-type J, the final meet B has prime index: five in S∩T, thirteen in S∩K, and forty-one in T∩K. This proves exactly the source RWPRI condition. All eight intersection subgroups are distinct; no independence issue is hidden by the labels.

The group-labelled lattice does not match the list after any permutation of types. Its two nonsolvable maximal parabolics must correspond to the listed simple Suzuki parabolics, leaving their order-20 intersection to be compared with the printed order-eight intersection. Other applicable shapes have different maximal-parabolic types.

## 3. Flag transitivity, firmness and residual connectedness

The simple order calculation

    |(K∩S)(K∩T)| = 52·164/4 = 2132 = |K|

proves K=(K∩S)(K∩T). Here the product-size formula applies to finite subgroups regardless of whether their product was known in advance to be a subgroup.

Normalize a chamber's K-coset to K. Since the other two cosets meet K, write them h1S and h2T with h1,h2 in K. Factor h1^−1 h2=s t with s in K∩S and t in K∩T. Then h1s=h2t^−1 belongs to K, h1S and h2T. Every chamber therefore has a common group element, hence is a translate of the base chamber. Every rank-three coset pregeometry is a geometry because a two-element flag has a common representative and extends to a base-chamber translate. Consequently the action is flag transitive on all flag types.

The panel sizes are 5, 13 and 41, so the geometry is firm (indeed thick). Residual connectedness reduces, using flag transitivity, to generation of the rank-two base residues and the ambient incidence graph. Inside K, the pair intersections generate K by the factorization. Inside S and T, the torus-normalizer intersection is maximal and the common Sz(2) is not contained in it, because the latter has an element of order five while 52 and 164 are not divisible by five. Thus those residues generate S and T. Finally the two distinct maximal subfields generate G. These are all the required connected residues in rank three.

The example does not satisfy local two-transitivity: on a thirteen-point panel, its point stabilizer has order four and cannot be transitive on the other twelve points; the forty-one-point panel gives the same obstruction. This is consistent with the exact scope of the source theorem being contradicted. No rank-two intersection assertion follows from the argument.

## 4. Matrix and executable review

I read the entire new checker and the arithmetic portions of both imported modules. The reviewer reran a byte-identical copy with both dependencies in a disposable directory; the independent run exited successfully in about 1.8 seconds. The historical output files were not changed. This is an independent execution and code audit, not an independently implemented second arithmetic library.

The important checks are:

1. The degree-15 field is certified by a multiplicative orbit containing every nonzero polynomial class. The degree-105 field used for the extension is separately certified by Rabin's irreducibility criterion. Arithmetic is exact binary polynomial arithmetic.
2. The binary matrix M satisfies M^4+M+I=0 and has order 15. The matrix r=U(1,0) has order four and conjugates M to M². The source's finite-field algebra construction therefore has its claimed common position.
3. The generated order-13 and order-41 matrices commute, lie in the indicated coefficient subfields, and lie in the ambient Suzuki group. Their product has order 533 and conjugation by r has exponent 278, whose square is −1 modulo 533.
4. The checker closes the full 2,132-element group K. It individually verifies every element against the Suzuki Bruhat decomposition and tests field-fixed entries to compute both subfield intersections. It also closes the order-20 binary Sz(2) and calculates the triple intersection exactly.
5. The Bruhat membership test has the correct orientation: in the open cell, the first-row entries recover the right U parameters and λ^(θ+1); multiplying on the right by the inverse U, then w, then h(λ)^−1 leaves the left U. In the other cell, division by the diagonal h leaves U. The unique parameter recovery also justifies identifying Suzuki matrices over a coefficient subfield with its standard subfield group.

The run also passes the separate degree-105 extension. Its eight Frobenius tests identify the prime cyclic factors surviving in each standard subfield. Because distinct prime components can be isolated by integer powers, their product belongs to a subfield exactly when its nontrivial components do. Multiplication by the binary r preserves coefficient-field membership. This verifies the recorded intersection formulas; the written fifteen-case RWPRI argument then follows from subfield maximality, full prime-order torus normalizers and prime subgroup indices. **The rank-four geometry axiom and flag transitivity have not been proved by this review.** Its maximal-parabolic types are not claimed to be absent from L110 Construction 6.

I also read the root agent's [RankThreeFactorization.lean](formal/RankThreeFactorization.lean). Its exact theorem proves the common-coset-point statement for an arbitrary group from the stated subgroup factorization; its hypotheses do not assume flag transitivity. I did not rerun Lean here. The separate root compilation record is the evidence for machine acceptance. The finite Suzuki construction and classical subgroup maximality are outside that formal theorem's scope.

## 5. Source diagnosis, scope and records

The Residue 7 discussion on L114 printed page 57 discards a pair of subgroups by concluding that they generate the ambient Sz(q). In this example, the subgroups C5:C4 and C41:C4, of orders 20 and 164, instead lie in the proper standard Sz(32), where they generate that subgroup. Here C5:C4 is the full C5-normalizer in Sz(8), but not in Sz(32), where that normalizer is C25:C4. The explicit witness establishes the missing case independently of a complete reconstruction of the historical argument.

A bounded exact-title/theorem/erratum search on 2026-10-10 found no later primary correction addressing this exact configuration. That search does not establish priority. The previous project's per-shape realization and obstruction results remain separate; the printed list's completeness can no longer be retained as an input for a global classification claim.

The companion audit JSON binds the reviewed proof/checker/source versions by SHA-256. The independent run is in [phase6_suzuki_counterexample_audit_run.json](phase6_suzuki_counterexample_audit_run.json). No proof note or historical certificate was edited in this review.
