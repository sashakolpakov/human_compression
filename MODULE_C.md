# Module C: Halving and Petrial operations on regular geometries

The separately reviewed [Graph incidences and stabilizer orbits](GRAPH_INCIDENCE.md)
attachment connects C's two J1 polytope markings to the literal graph
objects of L068. One source construction agrees exactly; the other needs
an explicit incidence repair. Its additional costs and partial coverage
are recorded separately from this three-source edition.

Read the complete [18-page manuscript](research/case_study/phase150_module_C_render/application.pdf)
or its [Markdown source](research/case_study/phase150_module_C_manuscript.md).
The [independent review](research/case_study/phase162_module_C_review.md)
and [root admission](research/case_study/phase170_module_C_root_admission.md)
accept the three corrected principal-result contracts below, with the
retained inputs and required finite programs stated explicitly.

    U + Halving and Petrial operations on regular geometries
      + complete J1 construction and census programs
        -> corrected principal results of L088, N013 and L108.

| Source | Results derived |
|---|---|
| Hartley–Leemans, *On the thin regular geometries of rank four for the Janko group J1* (2005), L088 | All six constructions and their invariants, exhaustive rank-four classification, and exclusion of higher ranks for thin regular residually connected geometries |
| Montero–Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes* (2020, v1), N013 | Halving, parity groups, polygon parameters, locally spherical cases, exceptional orders and the exact original and halved toroidal geometries |
| Bonheure–Buekenhout–Leemans, *On the Petrials of thin rank 3 geometries* (2001), L108 | Thinness obstruction, connectivity, faithful regularity and recovery by a second Petrial, including infinite groups and residues, with corrected action-kernel and length assertions |

The common argument tracks a change of chamber generators and the objects
retained by that change. Endpoint conjugation has an exact subgroup
intersection criterion. Graph double covers realize halving, while the
kernel of the action on retained vertices and edges controls Petrials.
The manuscript proves the geometry, toroidal lattice identifications,
finite classification and recovery arguments in full.

The [ledger](research/case_study/phase150_module_C_ledger.json) attaches
35 source and qualification records to 29 proof spans. Danzer's cube
construction, classical Coxeter results and the complete TomLib J1
subgroup catalogue remain attributed inputs. The old geometry census is
not an input to our census. Source figure labels, nondegeneracy and rank
qualifications, and the false unconditional Petrial assertions are
addressed explicitly. L108 was read through a complete saved authored
rendering; its original PDF remains unavailable.

The complete C text is 68,972 UTF-8 bytes. All of U adds 61,576 bytes;
the two finite programs and their standalone runner add 15,578. The
resulting core inventory is **146,126 bytes**. Binding, planning and render
infrastructure are [itemized separately](research/case_study/phase150_module_C_costs.json).
The 18 exposition pages exclude U and the programs. A matched source
compression ratio has not yet been measured.

Independent review read the entire manuscript, all three available source
texts and both complete programs, and inspected all 18 rendered pages.
Fresh public checks verify the exact bindings of proofs, dependencies and
earlier executed census records and reject eight altered-input cases.
The unchanged census was not rerun for this publication. Its recorded
execution checks 100,016 rank-four extensions and 21,352 rank-five extensions.
Full Lean formalization remains incomplete; the existing endpoint helper
covers only a fixed-overlap subgroup identity.

```sh
python3 -B -O research/case_study/phase150_module_C_verify.py --output /tmp/NEW-C-integrity.json
python3 -B -O research/case_study/phase162_module_C_checks.py --output-dir /tmp/NEW-C-independent
```

To rerun the full finite construction and census with GAP and TomLib:

```sh
python3 -B research/case_study/phase150_module_C_run.py --output-dir /tmp/NEW-C-J1
```

These checks do not formalize the uniform written proofs. Open-question
results remain in the separate [question-results catalogue](CONJECTURE_RESULTS.md).
