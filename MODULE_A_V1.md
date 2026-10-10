**Archived first-edition page.** The current [Module A](MODULE_A.md) has a
24-page integrated six-source edition. The text below preserves the first
edition's scope, correction and accounting.

# Module A: Construction and classification of two-group polytopes

**Required correction:** the quoted diagonal factors in §7.4 of this
frozen draft are incorrect. Read the
[complete correction](research/case_study/phase138_N009_decomposition_erratum.md)
and [independent review](research/case_study/phase143_n009_decomposition_review.md).
The corrected affine proof preserves the classification targets and
recorded census; the new edition will incorporate it directly.

Read the [21-page manuscript PDF](research/case_study/phase117_two_group_application_render/application.pdf)
or [complete Markdown source](research/case_study/phase117_two_group_application.md).
This first full application draft cites [U](UMBRELLA.md) for shared proofs
and supplies the construction, recognition and classification arguments
specific to its five-paper bundle.

The intended deduction is:

    U + Construction and classification of two-group polytopes
        -> the declared principal results of L032, L035, F013, F016, N009.

| Source | Results addressed |
|---|---|
| Hou–Feng–Leemans, *On regular polytopes of 2-power order* | Prescribed rank, type and exact-order existence |
| Hou–Feng–Leemans, *Existence of regular 3-polytopes of order 2^n* | Existence and the eight high-type marked classes, with complete presentations |
| Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group* | The canonical class-two quotient and geometric covering |
| Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* | Prescribed square sections, universal presentations, alternating assembly and free extensions |
| Gomi–Loyola–De Las Peñas, *String C-groups of order 1024* | Central descent, complete marked classifications, named facets and universal orders |

These specified editions span 2018–2026. The
[contract ledger](research/case_study/phase117_two_group_application_ledger_checkpoint04.json)
has 44 records and 17 multipart clauses. Records include retained inputs,
definitions and tables; they are not 44 newly proved theorems. Source
corrections are explicit, including the auxiliary common-quotient kernel
and several literal presentation entries.

One forest quotient supplies the common finite search space. One affine
square family and U's supported-kernel theorem supply several existence
constructions. The cyclic-core classification, presentation upper bounds
and exact finite census remain complete application arguments.

The 21 pages include all application prose, tables, references and the
computational interface. The four complete external programs and data
files remain required proof inputs and are charged in full:

| Charged component | UTF-8 bytes |
|---|---:|
| Module A | 78,524 |
| Complete U manuscript, charged once | 56,096 |
| Four complete computational artifacts | 56,375 |
| Original frozen package | 190,995 |
| Required diagonal-factor correction | 5,967 |
| Current complete package | 196,962 |

This is a raw inventory, **not a compression ratio**. A matched comparison
of the complete package with the source bodies remains to be made. The
old mixed manuscript supplies reused proofs; its length is not the baseline.

Root has read the complete U and A proofs; the
[review record](research/case_study/phase127_modular_root_review.md) gives
the scope. The 21 pages were individually inspected by the author, and
root sampled pages 1, 12 and 20. Complete source admission and formalization
remain pending. The unchanged finite certificates retain their earlier
reviews. A4.3 exactly matches the existing Lean four-marker theorem;
other formal coverage is narrower than the complete manuscript.

To check the frozen files, all source-contract spans, the full cost and a
byte-exact rebuild from the retained proof material, run:

```sh
python3 -B -O research/case_study/phase117_two_group_application_verify_v2.py --output /tmp/NEW-module-A-check.json --rebuild
```

This checks integrity, not mathematical validity. The separately bound
correction above is also required. Use the
[corrected portable checker](research/case_study/phase117_two_group_application_portability.md);
the original author manifest's command assumed a different directory
layout. No primary publication PDF is included in this export.

A separately reviewed [three-generator hypertope attachment](MODULE_A_HYPERTOPES.md)
now derives the full corrected principal construction of a sixth source,
L034 (2019), through a coordinate-kernel coset-intersection theorem. Its
mandatory involutivity correction is explicit. Integration into a new
edition is pending; the five-source 21-page draft above remains frozen.
