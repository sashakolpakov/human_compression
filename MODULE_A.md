# Module A: Construction and classification of two-group polytopes and hypertopes

Read the complete [24-page manuscript](research/case_study/phase138_render_A_v2/application.pdf)
or its [Markdown source](research/case_study/phase138_module_A_v2.md).
This second edition integrates six sources, the corrected hypertope
construction and the corrected diagonal decomposition. It cites the
[16-page umbrella U](UMBRELLA.md) for shared proofs and supplies the full
application arguments and computational interface.

    U + Construction and classification of two-group polytopes and hypertopes
        -> declared principal results of L032, L035, F013, F016, N009 and L034.

| Source | Results derived |
|---|---|
| Hou–Feng–Leemans, *On regular polytopes of 2-power order* | Prescribed rank, type and exact-order existence |
| Hou–Feng–Leemans, *Existence of regular 3-polytopes of order 2^n* | Existence and all eight high-type marked classes, with complete presentations |
| Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group* | The canonical class-two quotient and geometric covering |
| Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* | Prescribed square sections, universal presentations, alternating assembly and free extensions |
| Gomi–Loyola–De Las Peñas, *String C-groups of order 1024* | Central descent, complete marked classifications, named facets and universal orders |
| Hou–Feng–Leemans, *Existence of regular 3-hypertopes with 2^n chambers* | The complete presentation, exact order and type, regular geometry, cyclic kernels and corrected quotient structure |

These specified editions span 2018–2026. The
[contract ledger](research/case_study/phase138_module_A_v2_ledger.json)
contains 50 records and 23 detailed multipart clauses, preserving the
previous 44 records. Records include retained inputs and tables; they are
not 50 new theorems. Read its required
[six-locator metadata correction](research/case_study/phase138_detailed_locator_erratum.md).
The main proof spans and mathematical statements are unchanged by that
correction. Source versions, borrowed inputs and exclusions remain explicit.

One forest quotient supplies the common finite search space. One affine
square family and U's supported-kernel theorem give several existence
constructions. The coordinate-kernel coset-intersection theorem provides
the geometric step for three dihedral attachments. The cyclic-core
classification, source-presentation upper bounds and exhaustive census
remain complete application arguments.

The 24 pages include the application prose, tables, references and
computational interface. All four external programs and data files are
required proof inputs and are charged in full:

| Charged component | UTF-8 bytes |
|---|---:|
| Complete Module A, version 2 | 90,910 |
| Complete U, version 3, charged once | 61,576 |
| Four complete computational artifacts | 56,375 |
| Complete integrated package | **208,861** |

This is a raw inventory, not a source compression ratio. Compared with the
fully corrected six-source additive package of 214,717 bytes, integration
removes a net 5,856 bytes. The uncorrected historical package is not used
as a valid proof comparator. One reduction does not establish a long-run
sawtooth pattern. Matched source measurement is a separate task.

The independent and root reviews are recorded in the
[publication review](provenance/phase99_review.md). The general
supported-kernel construction, its principal consequences and typed-Helly
transfer have [scoped Lean certificates](research/case_study/formal/README.md).
Full geometry recognition, source-specific application bindings and the
whole module are not yet formally verified. The unchanged exact census
retains its earlier successful executions and reviews.

```sh
python3 -B -O research/case_study/phase138_verify.py --rebuild --output /tmp/NEW-integrated-UA-check.json
```

This verifies documentary bindings and exact regeneration, not mathematical
truth. The four complete classification programs have their separate replay
command in the manuscript's Appendix C. Primary publications are referenced,
not bundled. The [first five-source edition](MODULE_A_V1.md) and
[earlier hypertope attachment](MODULE_A_HYPERTOPES.md) remain archived with
their mandatory corrections and historical accounting.
