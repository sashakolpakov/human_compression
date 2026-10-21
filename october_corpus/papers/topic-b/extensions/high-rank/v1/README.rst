L040: high-rank symmetric markings from finite cores
==================================================

This is an author-frozen candidate for independent mathematical review. It
recovers the five principal targets of Fernandes–Leemans, *C-groups of high
rank for the symmetric groups*, using the exact 2018 accepted institutional
manuscript: 20 authored pages plus publisher cover. It is not a final-journal
PDF claim. The two current papers are actual TeX sources with full proofs.
No new source admission, question answer or compression factor is assigned
by this packet.

Read ``umbrella.pdf`` and ``high-rank-symmetric-markings.pdf`` together.
The former proves the common normal-module and simple-kernel bounds, the
finite-core attachment interface and the tree presentation. The latter
proves both classification directions, all allowed tree constructions,
flag completion and exact marking presentations. ``scope.json`` records
35 source dispositions and 25 complete written contexts. The entire
common paper is a dependency; another topic's acquisition is not free.

Exact scope
-----------

* Theorem 1.1: degree n, rank n−1, n≥7; tree classification, symmetric group,
  line graph and regular hypertope.
* Theorem 1.2: S_n, rank n−2, n≥9; all three families, necessity and
  sufficiency, all allowed branching and regular hypertopes.
* Proposition 3.1: complete Coxeter-plus-triangle tree presentation.
* Corollary 6.5: the intended general presentation is recovered by an
  explicit corrected inverse-word construction. The literal clause (2)
  fails when the bridge meets two further tail edges. The nine-letter
  counterexample and all correct local pair/word identities are explicit.
  No claim is made that the source's entire shorter printed list is an
  equivalent presentation for arbitrary branches.
* Theorem 6.6: full flag transitivity, proved by decorated core objects
  and laminar subset completion; not inferred from intersection property.

The complete source's separate degree-eight example is checked exactly.
The auxiliary table of exact primitive C-ranks and the ambiguous numerical
leaf-count convention are not claimed as recovered outputs. General
background assertions unused by our argument remain explicitly outside
the contract. These qualifications do not disappear in a principal result
count. No historical conjecture or priority claim is made.

Dependencies and computation
----------------------------

Whiston's maximum independent-family bound, its equality implication and
the exact omission-subgroup alternatives remain classical inputs, through
the complete authored Cameron–Cara interfaces. Whiston's own full text is
not locally available in this packet. Maróti's original Theorem 1.1 is
retained with the lower alternating-group containment that the source's
reprint omits. Its original authored PDF is privately hash-bound. All
normal-module, simple-subdirect and tree arguments used here are written
in full. The bound is on maximum irredundant length, not minimum number
of generators.

``program-appendix.pdf`` prints four entire mathematical programs:

* ``primitive_bound.g`` is required for the bounded primitive-catalogue
  and exact finite-group inputs to the uniform converse. Catalogue
  completeness and GAP's exact algorithms remain retained inputs.
* ``core_attachment.g`` validates all 156 written finite-core identities.
* ``local_obstructions.py`` validates the 18 completely derived local
  splitting cases and rejects five altered witnesses.
* ``boundary_example.g`` is required only for the additional degree-eight
  example, checking all 4,096 intersections and 156 flag-product tests.
  Its branching calculation also validates an already written proof.

The second and third programs are validation, not substitutes for the
uniform proof or for completeness of the local cases. No program is
pruned from the appendix. ``check.py`` and ``formal/check.py`` are complete
operational drivers and remain separately visible.

Eight Lean declarations certify quotient normalization, generated-subgroup
equality and independence under base/all conjugation, with the actual
normality, commutativity, correction-word and factorization hypotheses.
They do not formalize the cardinal bounds, classification, catalogue,
fracture converse, attachment theorem, presentations or geometry.
Six finite countermodels demonstrate omitted hypotheses. All saved axiom
reports use only the standard Lean axioms. Pinned cached dependency
objects are trusted; this is not a full mathlib rebuild.

Replay
------

Use Python with pypdf, GAP with its primitive catalogue, and XeLaTeX with
STIXGeneral, STIX Two Math and Menlo. From an unpacked packet::

  python3 -B -O check.py --out /fresh/absolute/output \
    --programs --formal --render \
    --gap /path/to/gap --xelatex /path/to/xelatex \
    --lean /path/to/lean --packages /path/to/pinned/packages

The declared Lean version is 4.32.2; every package revision is in
``formal/dependency_manifest.json``. Fresh output is required. Optional
``--study-root /path/to/private/study`` verifies the exact source and
retained primary bindings. It is not needed for the portable mathematical
program/formal/render replay. Omitting any execution flag is reported by
its absent execution section, not converted into a fresh-run claim.

The checker validates every bound source row, proof span and complete
program inclusion and rejects eleven semantic scope/binding mutations.
It also compares fresh render text on every page with the authoritative
PDFs. The saved author replay is author evidence only. Independent
mathematical acceptance is a separate artifact and remains pending.

Publication boundary
--------------------

Only the manifest's explicit exports may be distributed. Private source
PDFs, original TeX, extractions, raster/contact views and exploratory
working drafts are not exports. They are retained privately for source
review. Original external proof, catalogue-construction and graphic costs
remain unknown, not zero. No factor has been calculated.
