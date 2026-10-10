# Two raw presentations and the exceptional order-1024 case

10 October 2026. Private source-bound reconstruction of N009 Theorem 5.5, using the exhaustive rank-four kernel census as a separate completeness input. This is a rederivation of a published classification component, not a new classification claim or a whole-paper coverage claim.

## Exact target and transcription

The primary source is Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics 13(1) (2018), [DOI 10.55016/ojs/cdm.v13i1.62475](https://doi.org/10.55016/ojs/cdm.v13i1.62475). Theorem 5.5 on printed p. 20 gives two rank-four groups with facet of order 128 and vertex figure of order 64, both of type {4,4}. The displayed groups have type {4,4,4}.

Write a,b,c,d for the ordered source generators s0,s1,s2,s3. In both presentations impose

    a^2=b^2=c^2=d^2=1,
    (ac)^2=(ad)^2=(bd)^2=1,
    (ab)^4=(bc)^4=(cd)^4=1,
    (abcb)^4=(bcd)^4=1.

Presentation P1 adds

    (dcbabdc)^2=1.

Presentation P2 instead adds

    (bdcdba)^2(cbab)^2=1,
    (abcb)^2(babdcd)^2=1.

The transcription was checked against the complete displayed Theorem 5.5 statement and the immediately preceding second-presentation display in the primary extraction. The source PDF SHA256 is `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`; extraction SHA256 is `091caf4266f2ac595aec76def47d451700fff7c80f6d0f3eabeee2e6f31f38e7`. No nilpotency-class relation, order bound, or extra commutator identity is included in either raw presentation.

## A finite upper bound, not just a finite quotient

The standalone original script `phase21_N009_presentations_check.g` constructs each raw finitely presented group and runs GAP's Todd–Coxeter coset enumeration over its trivial subgroup. Both completed tables have exactly 1024 cosets. This supplies the upper bound on the raw presented group itself, which would not follow from an NQ computation or from finding a permutation quotient.

The permutations read from each table generate a group of order 1024; GAP verifies a homomorphism from the raw presentation onto it. This supplies the matching lower bound and identifies the entire presented group with that faithful permutation group. In each group the four marked generators are involutions, all three adjacent products have exact order four, and the two ordered facets have orders 128 and 64. All 16 marked subgroups are constructed, and all 256 intersection equalities are checked. Thus both raw presentations define string C-groups with the asserted marking, type and facet orders.

The script also tests the unique possible homomorphism carrying the four ordered generators of P1 to those of P2; there is no marked isomorphism. Reversal cannot identify these two fixed-orientation markings because it would exchange the unequal facet orders 128 and 64. The finite scope is two raw presentations, 32 subgroup closures and 512 actual intersections. GAP 4.15.1 is the retained exact computational input. No NQ, SmallGroups catalogue, assumed faithfulness or group-recognition oracle is used in this check.

## Why there are only two

The separate `phase21_kernel_ladder.md` supplies the complete finite search mechanism. Every nondegenerate rank-four group of order 1024 has gamma3 of order eight and class at most five by the reviewed canonical forest quotient. It is therefore the marked quotient of the universal rank-four/class-five path group by an ambient-normal index-eight subgroup of gamma3.

The invariant index-two ladder enumerates every such subgroup: for an intermediate normal M, index-two ambient-normal subgroups are precisely the hyperplane preimages in M/(Phi(M)[M,U]); every target kernel admits such a chain by a fixed nonzero character of the ambient 2-group action. Canonical induced pc generating sequences remove only exact duplicate subgroups. The implementation explicitly verifies that the ambient pc sequence has relative orders two before using its binary-coordinate keys.

The final guarded rank-four run examines 1483 kernels. Kernel-profile intersection recognition rejects 1284; all 199 surviving full quotients are then independently checked against all 256 actual marked intersections. It finds exactly two ordered markings with type {4,4,4} and ordered facet orders (128,64). The standalone source-comparison script checks this directly from the accepted-kernel records. At this step facet orders are not used as a general substitute for marked isomorphism. The already reviewed first-excess classification (`phase17_k1_classification.md`) gives exactly one ordered rank-three type-{4,4} marking of order 64, and the reviewed second-excess classification (`phase19_k2_classification.md`) gives exactly one of order 128. Thus these type-and-order conditions do identify the two named source facets in this particular case. The two distinct raw presentations above belong to that class, so they exhaust it. This establishes the completeness portion of Theorem 5.5 without reproducing the source's separate analysis of an infinite universal amalgam.

This dependency is explicit: the Todd–Coxeter check alone proves existence and the displayed presentations; completeness additionally uses the universal-kernel census. The source's quoted infinite-group structure theorem is not claimed as rederived by this argument.

## Source census comparison and coverage boundary

`phase21_N009_source_compare.py` reads the final guarded accepted-kernel records and compares every one of the 13 canonical rank-four type totals with Table 6, printed pp. 14–17. It uses the source's generator-set isomorphism convention (Definition 2.6), which for a connected path means identifying an ordered marking with its reversal. The result is 199 ordered markings, 11 reversal-fixed markings and 105 classes up to reversal. The palindromic types use the fixed-point term explicitly; the equality of the grand total alone is not the check.

That comparison certifies the rank-four census and type totals, not a label-by-label identification of every source facet entry or every presentation elsewhere in the paper. Theorem 5.5 is the particular presentation component additionally recovered here. The rank-three order-1024 component still requires a separate exhaustive calculation. The earlier `phase21_scope_targets.md` is preserved as a historical intake; its outstanding raw-presentation obligation is discharged by this note and executed check, without rewriting the intake's earlier state.

For reproduction, run the presentation script with GAP from any working directory. Run the source-comparison script with `--accepted` pointing to the final rank-four accepted-kernel JSON and `--output` to a fresh report path. The expected input hash is recorded in `phase21_N009_source_compare.json`; no third-party full text is needed for either executed check. The source text remains a private reference for transcription and scope review.
