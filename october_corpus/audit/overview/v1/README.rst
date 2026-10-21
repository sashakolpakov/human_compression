All ten measured topics
=======================

Read the `five-page consolidated report <packet/summary.pdf>`_ for every
whole-topic and individual comparison. It covers27 distinct original
manuscripts, with full common theories and all complete applications.
The `current corpus record <../../corpus/current.json>`_ also includes
F015 and L028 as recovered originals; their measurements remain pending.
All accessible originals remain in the programme.

For each topic, the complete written factor is the sum of original manuscript
costs divided by the full common paper plus all applications. Each individual
factor divides the original by its complete application after acquiring the
entire topic's common theory and declared programs. Overlapping common
mathematics is charged independently to each topic.

.. list-table:: Complete written factors
   :header-rows: 1

   * - Topic
     - Originals
     - Whole written factor
   * - A: Supported kernels and group presentations
     - 6
     - 1.535×
   * - B: Forest coordinates and primitive geometries
     - 4
     - 1.236×
   * - C: Chamber operations and binary translations
     - 4
     - 1.037×
   * - D: Orbit counts and incidence geometries
     - 3
     - 1.053×
   * - E: Projective string markings
     - 3
     - 1.816×
   * - F: Cyclotomic groups and tight hypertopes
     - 1
     - 1.264×
   * - G: Flag relations and incidence residues
     - 2
     - 0.630×
   * - Affine: Affine groups and lattice quotients
     - 1
     - 0.786×
   * - Representation: Finite groups and incidence geometries
     - 1
     - 1.015×
   * - Chamber: Chamber orbits and regular covers
     - 2
     - 0.982×

The `whole-topic graph <packet/whole_topics.svg>`_ separates common theory
from applications. The `individual graph <packet/conditional_applications.svg>`_
shows every original beside its application. The `topic table
<packet/topics.csv>`_ and `application table <packet/applications.csv>`_
are downloadable; `results.json <packet/results.json>`_ preserves exact fractions.

These are character counts with NFC normalization and whitespace removed.
B/C use literal complete renderings for N001/L108 and untrimmed PDFs for the
remaining texts. Other blocks retain their accepted calibrated PDF extraction
and removal of running furniture. No combined factor across these different
representations is asserted. Factors below one remain visible.

The report separately prices complete programs, identifies diagnostics and
retains unknown external, graphical and historical software costs as unknown.
It does not replace the source-specific proof scopes or claim all ancillary
assertions of each original have been recovered.

Review and reproduction
-----------------------

Root read and visually inspected all five pages, independently recomputed
57 fractions and both CSV tables, and checked 84 actual bars in each SVG/PDF
representation without importing the author's calculation. The public-only
replay reproduces eight files exactly and all five reader pages text-for-text.
No source extraction, mathematical proof or Lean build is repeated by this
numerical consolidation. Earlier author/reviewer roles are disclosed.

The `root admission <admission.json>`_ supersedes the candidate status in
the unchanged author packet. With pypdf, matplotlib and XeLaTeX installed::

  python -B -O audit/overview/v1/replay.py --out /fresh/output

The 20 input bindings resolve to public repository paths; no private source
files are needed. The independent checker and review are in
`independent_review <independent_review>`_.
