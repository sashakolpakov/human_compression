Borel subgroups and duality in coset twisting
===========================================

This is a bounded independent audit of literal N006 statements, with a
complete five-page mathematical correction note. The full 22-page primary
text was read; the displayed definitions and affected statements were
visually checked on eight specified pages. No complete N006 recovery,
historical priority, new question credit, or Lean formalization is claimed.

The note gives exact admissible countermodels to Theorems 4.4(d), 5.2(d),
and the universal nonlinear-diagram clause of 5.2(b). It derives the actual
Proposition 4.3 parabolics, distinguishes Borel and generation failures in
Lemma 2.4(c-e), and proves a nonsplit outer-automorphism example. The
all-digon rank-three and rank-four examples are explicitly constructed as
abstract polytopes, string C-groups, and coset geometries. The rank-four
argument uses an elementary partition of involutions, with no L128 input.

Root proposed the three principal examples. This reviewer independently
checked their source hypotheses and supplied the complete proof note and
standard-library finite models. The additional proof supplement still
requires root evaluation before admission as part of a new common theory.
The exact observed root GAP script is preserved separately, without changing
its historical wording or treating it as the independent calculation.

Portable replay, from any working directory::

  python -B -O check.py --out /fresh/output

Optional full local replay::

  python -B -O check.py --out /fresh/output \
    --study-root /path/leemans --gap /path/gap \
    --render --xelatex /path/xelatex

The base model checks need only Python's standard library. Rendering and
primary page-count verification use pypdf; rendering uses XeLaTeX with
STIXGeneral and STIX Two Math. The optional GAP replay checks the three
sentinels of the unchanged observed proposal. No primary PDF, text, raster,
compiled object, or cached TeX build product is exported. Each theorem has
an exact complete statement/proof span in proof_spans.json.

All five model corruption controls are executable under Python -O. They
check sensitivity of the finite interfaces, not the truth of the written
general proofs. The fresh replay also reproduces all five PDF page texts
and checks for unresolved glyphs and TeX diagnostics.
