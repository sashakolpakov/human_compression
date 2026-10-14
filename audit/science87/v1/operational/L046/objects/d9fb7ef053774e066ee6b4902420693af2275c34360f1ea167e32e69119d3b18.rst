Bounds for generating pairs from maximal subgroups
==================================================

The `four-page proof <proof/maximal_bounds.pdf>`_ shows that the O'Nan
group has at least **798,370** generating-pair orbits in the counting
convention of Thomas Connor and Dimitri Leemans, *Algorithmic enumeration
of regular maps*, Ars Mathematica Contemporanea 10 (2016), 211–222.
Their fixed published Theorem 1.1(2) reports **796,772**. The entry for
type (20,31) is determined exactly: **9,118**, rather than **7,246**.
The claim concerns the `fixed source edition
<https://amc-journal.eu/index.php/amc/article/download/544/857>`_, with
its exact hash and counting convention in `source_statement.json
<source_statement.json>`_. No claim about later corrections or priority
is made.

**L046 remains pending. This is not a recovery of the whole paper.**
The exact full total, **116 exact table entries**, six remaining
zero-type exclusions, and the full chirality and inversion spectra still
require work. The `remaining obligations <remaining_obligations.json>`_
are part of this publication. No recovered, terminally refuted or handled
original is added to the programme counts by this component.

Every nongenerating pair lies in a maximal proper subgroup. Counting all
pairs by characters and subtracting an upper bound for their union gives
a lower bound for generating pairs. The complete thirteen maximal classes
and their character tables are borrowed classification data. The method
uses the standard union bound and ordinary character theory; the present
contribution is their checked application and the resulting contradiction.
The complete `common proof <common/generating_pairs.pdf>`_ states the
character, subgroup-incidence and stabilizer interfaces and recovers two
source inversion obstructions. Its independent review is separate from
the `review of the new bound <independent_review/review.rst>`_.

The `136-row comparison <results.csv>`_ contains all proved intervals and
the literal source values. Twenty intervals are exact and all 129 types
asserted to exist have positive lower bounds. An interval containing a
source entry is not an exact verification of that entry. A zero lower
bound is not a nonexistence proof. The exact all-pair counts and all thirteen
maximal-class contributions are retained in `bounds.json
<proof/bounds.json>`_.

Replay with Python, GAP and CTblLib installed::

  python corrections/onan-map-count/v1/check.py --out /absolute/new/output

Add ``--render`` to rebuild both complete four-page manuscripts; that
also needs pdflatex and pypdf. The public checker freshly extracts the
named character tables, evaluates the 136 intervals, runs the finite
controls and compares 574 independently computed class-multiplication
counts. It reads no private study files. The exact extracted vectors are
public. Historical installed-library hashes remain explicit external
software/data records; the fresh extraction must match the accepted
vectors exactly. Source PDFs and their review screenshots are hash-bound
references, not redistributed prerequisites.

This is a correction to a published numerical assertion. It receives no
open-conjecture credit, compression factor or Lean verification claim.
The `publication proposal <admission_proposal.json>`_ and `catalogue plan
<catalogue_patch_plan.json>`_ reserve registration to a separate publication gate and
preserve the pending status and existing programme counts.
