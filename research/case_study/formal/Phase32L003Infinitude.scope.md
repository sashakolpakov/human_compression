# Scope of Phase32L003Infinitude.lean

This module embeds three literal permutations on 216 states, their inverse tables, three integer-voltage tables, and the ten words of the L003 rotational presentation after setting the parameter to six. The data are bound to `phase32_L003_voltage.json`, SHA256 `7bccd053824176bd6abbb5a7a11b16e3ed52c41ce0332b108d2c52ce1d188cc4`. The separate [transcription checker](../phase32_L003_formal_data_check.py) compares every literal table entry and every relator word with the reviewed data and factored source expressions.

Three finite theorems use `decide +kernel`:

- `table_inverse` proves that every forward and backward table is mutually inverse.
- `literal_relations` proves that all ten words return each of the 216 states with zero total voltage.
- `literal_witness` proves that `(xyxz)^2` returns state zero with voltage −1.

The final theorem `presentation_infinite` has conclusion `Infinite P6`, where `P6` is mathlib's `PresentedGroup` of the exact ten encoded words. It applies the fully proved generic right-voltage criterion in `Phase32VoltageTheory.lean`. Thus the finite checks are formally connected to infinitude of the presented group, not only asserted to imply it in prose.

The finite theorems report only `propext`; the infinitude theorem reports `propext`, `Classical.choice`, and `Quot.sound`. All proof terms are kernel-checked. There are no unproved placeholders or native evaluation axioms. The saved reports give the fresh final compilation timings and the checked dependency revisions.

The interpretation of the ten words as the source manuscript's parameter-six specialization is independently reviewed outside Lean. The formal module does not prove the written extension to every positive multiple of six, identify the whole image as a crystallographic group, prove hypertope axioms, exclude finite quotients, or resolve the literal Problem 9.2.

From the research directory, with a previously built checkout matching `formal/dependency_manifest.json`:

```sh
python3 phase32_L003_formal_check.py \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2/bin/lean \
  --output-dir /tmp/new-L003-formal-run
```

The fresh output contains compiled objects and `report.json`. The runner compiles missing `Mathlib.GroupTheory.Coprod.Basic` and `Mathlib.GroupTheory.PresentedGroup` objects into a private overlay; it never modifies the dependency checkout or distributes third-party source text. The two recorded source hashes are included in the report.

The runner verifies all package Git revisions and tracked-file cleanliness against the pinned manifest before compiling. Earlier development and successful-run provenance is recorded in [the build history](../phase32_L003_formal_provenance.md).
