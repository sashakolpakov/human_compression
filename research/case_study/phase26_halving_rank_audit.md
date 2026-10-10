# Independent review of the endpoint-halving criterion

10 October 2026. **PASS** for the complete written criterion, including finite-rank markings of infinite groups. This is an internal mathematical review and a fresh bounded diagnostic replay. It is not an external peer review, priority assessment or formalization of the whole theorem.

The reviewed theorem is [phase26_halving_core.md](phase26_halving_core.md), SHA256 `b6e44afe1dae7426b54241e971e5b1fe6fbc0fc5db44eae994fdf70a625eb9f5`. The companion JSON binds the exact final proof, checker and reports. I read the entire proof and standard-library implementation. No classification catalogue is needed by either.

## All-subset necessity and sufficiency

Conjugation by the old endpoint `a` exchanges `b` and `a'=aba` and fixes the remaining generators. Thus each `H_J` is normal in `U_J=H_J<a>`, with index at most two. This is valid for infinite groups and uses no order count. The family `F={J:a∈H_J}` is upward closed. Full-group generation is equivalent to this **family** being nonempty, not to the rest-index set being nonempty.

I checked every unordered pairing of the three labelled-subset types in the proof:

- **A–A:** both are old marked subgroups, so old IP applies directly.
- **A–B:** containment in `U_J` bounds the meet by the old subgroup on common labels; all its displayed generators belong to `H_J`, so equality follows.
- **C–C:** conjugation transports the old subgroup meet exactly.
- **B–C:** conjugation fixes `H_I` setwise and reduces this to A–B; it does not require `H_I=U_I`.
- **A–C:** the specified equality `P∩P^a=R` confines the meet to the pointwise fixed subgroup `R`. The two old restricted intersections then give precisely the common rest labels.
- **B–B:** the actual intersection lies between `H_(I∩J)` and `U_(I∩J)`. If these differ, their index is exactly two, so there is no intermediate subgroup. The larger intersection occurs exactly when it contains `a`, equivalently when both `I` and `J` recover `a`. Closure of `F` rules out precisely that extra possibility.

For necessity, the endpoint-deleted pair gives the overlap equality, and the B–B pairs give closure of `F`. The proof does not assume independence of the new generators: they are nonidentity involutions, and the established full intersection property rules out their redundancy. They generate `H` by definition. The finite-rank assumption is used to turn a nonempty intersection-closed upward family into a principal filter by taking its finite total intersection; it is not a finiteness assumption on the group.

The odd-order recovery formula, proper index-two case, even-order full-group example and infinite-order endpoint statement all follow as written. In ranks at most three, an upward family on at most one rest label is automatically intersection closed, so an obstruction of the second kind first becomes possible in rank four.

## Genuine separation of the two conditions

The S6 example supplies that rank-four obstruction. With `a=(12)`, `b=(13)(24)(56)`, `c=(45)`, `d=(46)`, the old marking has full IP. The subgroup `P` is `Sym({1,3}) × Sym({2,4,5,6})`. Its conjugate by `a` preserves the analogous partition with 1 and 2 interchanged. Their common refinement leaves only `{4,5,6}` as a nonsingleton cell, so their intersection is exactly `R=Sym({4,5,6})`.

Nevertheless the recovering family is `{ {c}, {d}, {c,d} }`. The two new three-generator subgroups both contain `a`; each has order 72. Their intersection is the old group `<a,b>` of order eight, while their required common new subgroup `<a',b>` has order four. These are the two ordered failing meet tests. Thus the support condition does not follow from the overlap condition and the old IP. It is a counterexample to dropping one condition from this criterion, not a claimed refutation of a published result.

I also read the complete [separate example note](phase26_halving_filter_example.md), including the two block-stabilizer descriptions and the exact recovery words. Its frozen reproduction line contains a spacing typo; the correct invocation is `python3 phase26_halving_filter_check.py`. This review does not alter that frozen source.

## Fresh diagnostic replay and limits

I ran the unchanged [standard-library checker](phase26_halving_check.py) into [phase26_halving_rank_audit.run.json](phase26_halving_rank_audit.run.json). The saved result is byte-identical to the author's report. The code constructs permutation closures and every marked subgroup directly, checks all ordered meets, and computes the recovering family by actual membership. The theorem is compared with the resulting full IP rather than used to infer it.

The fresh run passes nine named examples, including the separating S6 marking, proper index-two signed-permutation cases, even full-group cases, and a rank-five least support containing all three rest labels. It also examines all 168 distinct involution triples in the natural S4 action whose first and third markers commute: 72 old markings satisfy IP and 48 changed markings do. In total it checks 21888 ordered subgroup meets, with no criterion mismatch. These are bounded diagnostics; the six-case written argument proves the uniform result.

I read the scope statement of the separate `EndpointDoublingIntersections` Lean module. Its mixed-intersection theorem matches A–C, conditional on the stated subgroup and automorphism hypotheses. This review does not claim a fresh Lean compilation, and that module does not certify the entire halving criterion, the index-two support argument, or geometric flag transitivity.

The conclusion here is a C-group marking. For a nonstring diagram, a separate typed-coset Helly or equivalent argument is still required for the geometric conclusions. No exhaustive J1 geometry classification, open-conjecture resolution, or numerical proof-length compression ratio is inferred.

I checked the selected primary statements and immediate proofs cited in §6: Piedade–Tranchida, arXiv:2405.19050v1, Theorem 4.4 and Lemma 4.5 on PDF pages 14–15, together with the definitions of (B1) and (B2). The stated prior attribution is accurate. Their regular-hypertope and shadow-incidence hypotheses are retained in the comparison; the S6 C-group example alone cannot refute their geometric result. This is a selected-source check, not a full-paper reduction or an exhaustive priority search.
