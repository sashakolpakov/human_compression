# Author audit of the assembled endpoint manuscript

10 October 2026. This is an author audit and execution record, not independent review. The frozen source set is bound in `phase40_compress_operations_source_freeze.json`; the manuscript SHA256 is `3e605d2f9ec89324d031bd22e16a7a2d89ae324fa7bd801c2f8e3d8169b49560`.

The intake is L088 + N013. L088's six construction theorems and its central exhaustive six-object/no-higher-rank assertion are now rederived. N013's declared principal halving and generalized-cube results are covered relative to the named background and source qualifications. L108 is excluded, with its set-valued Petrial/kernel obstruction explained. No whole-paper numerical factor is assigned, and no open conjecture or publication-priority claim is made.

The earlier scope problem was substantive: merely reconstructing six examples did not rederive L088's exhaustive classification. The final manuscript removes that imported conclusion. The complete program in Appendix B uses the independent proper-residue extension theorem, the complete TomLib J1 *subgroup* catalogue, and exact group computations; it reads no earlier geometry representatives or classification outcomes as premises. The declared table counts are checked only after exhaustive enumeration. The original geometry census is not an input.

The first exploratory full run yielded the six rank-four classes and no rank-five regular residue. After adding catalogue-list checks, structured output, exact embedded-code checks and the source's incidental facet-normalizer equality, the final frozen two-program assembly was rerun in a fresh scratch directory. It passed with GAP4.15.1 and TomLib1.2.11, J1 data SHA256 `576834302b6da30248f34565d6559b857160fdbd67066d1e67c64f0191b8b143`.

| Scope | Fresh final result |
|---|---:|
| Explicit source constructions |6|
| Construction ordered marked meets |1536|
| Sufficient global typed-Helly equalities |96|
| Negative source examples |2|
| Source-presentation coset index / group order |1463 / 175560|
| Local involution-triple orbits across all maximal subgroups |245|
| Local involution-quadruple orbits |1476|
| Locally regular triple / quadruple orbits |95 / 15|
| Their J1-conjugacy classes |70 / 15|
| Rank-four extensions checked |100016|
| Successful rank-four extensions / conjugacy-and-type classes |40 / 6|
| Rank-five extensions checked, including proper-group targets |21352|
| Successful rank-five regular geometries |0|

The construction program took about2.25seconds and the complete census about268.48seconds on this run. Source hashes were unchanged; both embedded GAP blocks were byte-identical to the executed scripts. The runner's refusal to reuse an existing output directory was tested after completion: it exited2 and every existing output hash remained unchanged.

The written completeness argument is part of the manuscript. A rank-r thin regular residually connected geometry has regular residues and corresponding IP-plus-Helly markings. Any independent proper residue lies in a conjugate of a maximal proper subgroup, so the local orbits cover it. A rank≥5 geometry supplies a rank-five residue, which the all-subgroup extension stage would find. No assertion is made that all rank≥5 C-group markings are absent. Canonical unordered marking keys are actual inner-conjugacy keys obtained using an involution centralizer of order120; the six distinct parabolic-order multisets then exclude additional isomorphism identifications, without assuming the outer automorphism group is trivial.

The full manuscript includes the proofs of endpoint support, geometric recognition and graph-cover compatibility, not merely references to prior project notes. The finite application includes both complete programs. The independent review should especially check: the group/geometry distinction in the higher-rank argument; completeness of the retained subgroup-class catalogue; the orbit-action and canonical-key equivalences; the retained lattice condition in N013; the scope of the Coxeter/toroidal inputs; and all27 statement-ledger rows.

The exact reproducible command is:

```sh
python3 phase40_compress_operations_verify.py --output-dir /tmp/new-compress-C-run --gap /opt/homebrew/bin/gap
```

Use a new directory. The final manifest gives the export allowlist. Files with `discovery` in their name, the exploratory `census.g` and `census_theory.md`, and the old primary fulltexts are not part of that allowlist. Only the final manuscript, its two embedded executables, runner, source intake, ledger, freeze, fresh output evidence and this audit should be exported after independent review. The manuscript's full body through Appendix B must be included in any later length denominator.
