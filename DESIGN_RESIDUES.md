# Residues and automorphisms of design constructions

Two reviewed corrections to the 2005 source L092 are now available. They
are part of the older-paper intake, with complete written arguments and
finite checks. They do not yet replace all the principal results of that
paper or change the measured compression rates.

The source is D. Leemans, *A Generalization of a Construction due to
Van Nypelseer*, Beiträge zur Algebra und Geometrie 46 (2005), 561–574.
The constructions and their earlier geometric ingredients remain
attributed to the source and its cited predecessors.

| Construction | Reviewed conclusion | Relation to the printed assertion |
|---|---|---|
| Apply Construction3 to the deleted-line residue of an affine plane, q>3 | Firm for every q; residually connected exactly for q>4; flag-transitive exactly for q=4 or8. All three properties hold exactly for **q=8**. | Corrects Theorem6, which selects q=4. |
| Apply Construction2 to the subline design S(3,q+1,q^e+1), q≥3, e≥2 | Firm for all these parameters; residually connected exactly for **e=2**. In dimension two, flag transitivity holds exactly for q=4. | Corrects Lemma5's connectivity assertion. The subline branch of Theorem11 remains valid. |

The [deleted-line proof](research/case_study/phase182_deleted_line_independent_theorem.md)
recovers the full automorphism group from the two omitted parallel classes
of an affine net. Residue connectivity becomes an elementary calculation
in a product of two cyclic groups. The
[subline proof](research/case_study/phase182_inversive_residues.md) determines
every residue type. Its flag-transitivity exclusion retains Kantor's
published classification, explicitly identified in the proof.

Lean verifies the literal 18-vertex residue over the four-element field
as **three disjoint hexagons**. The
[formal source](research/case_study/formal/DeletedLineFourResidue.lean)
derives the component invariant from the field incidence equation and
proves disconnection. The
[source-to-graph identification](research/case_study/phase182_deleted_line_lean_bridge.md)
is written; the two uniform theorems and the positive q=8 case are not
fully formalized.

Exact finite checks examine every flag and residue for q=4 and q=8.
For the subline counterexample q=3,e=2, an independently written GAP
construction agrees with the complete Python incidence structure. All1881
residues of rank at least two are connected. Its full type-preserving
automorphism group has order1440, whereas it has2160 chambers, so this
example is not flag-transitive.

The [independent subline review](research/case_study/phase183_independent_review.md)
and [root admission](research/case_study/phase185_root_admission.md) state the
reading depth, source corrections, trust boundaries and fresh checks.
These are corrections to published assertions, with historical priority
unverified; they are separate from the
[open-question results](CONJECTURE_RESULTS.md). No whole-paper credit or
new conjecture-resolution count is assigned.

With GAP, the pinned Lean compiler and its package checkout available:

```sh
python3 -B -O research/case_study/phase185_corrections_check.py \
  --output-dir /tmp/NEW-design-residues \
  --packages PACKAGES --lean LEAN --gap GAP
```

This public replay needs no private source PDFs. It runs both finite
constructions, the independent subline check, a fresh Lean compilation,
and four targeted rejection controls. It does not mechanically verify
the written uniform proofs.
