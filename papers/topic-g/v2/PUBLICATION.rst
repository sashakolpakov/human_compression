Flag relations and incidence residues
====================================

This edition contains a complete common paper and two applications for the
existing corrected principal contracts L009 and L092. Read the twelve-page
`common theory <umbrella.pdf>`_, then the eight-page `triangle application
<triangle-geometries.pdf>`_ and the twenty-two-page `Steiner application
<steiner-geometries.pdf>`_. The earlier G edition remains a separate baseline.

The common paper proves three sets of reusable statements. A directed
relation on point-line flags encodes triangles; common-neighbour counts
recover their original points and lines. For Steiner constructions, a
chamber is expressed through an ordered tuple and two successive stabilizer
orbits. This gives common proofs of chamber extension, induced automorphisms
and residue connectivity. Finally, explicit Hermitian matrices transport
vectors of equal nonzero norm. Their isotropic moves generate the group
needed to identify and connect the geometric residues in both applications.

These are mathematical deductions with their hypotheses checked in each
application. They include the required proofs from the project's earlier
work. No citation to an earlier project manuscript hides part of the common
theory's written cost.

Sources, contributions and qualifications
----------------------------------------

.. list-table:: Two existing source contracts
   :header-rows: 1
   :widths: 34 43 23

   * - Source, authors and edition
     - Recovered principal results
     - Qualifications
   * - L009: Delaby--Leemans--Tranchida, *Geometries with trialities arising
       from linear spaces*, Algebraic Combinatorics 9(2) (2026), 379--402
     - Triangle construction, reconstruction, automorphisms and correlations;
       corrected action classification, residue connectivity and diagrams
     - The affine determinant condition, circle list and polarity statement
       are corrected; the declared ancillary examples remain excluded.
   * - L092: Leemans, *A generalization of a construction due to Van
       Nypelseer*, Beiträge zur Algebra und Geometrie 46 (2005), 561--574
     - Corrected classification from linear spaces and Steiner designs;
       complete residue arguments, classical families and exceptional data
     - Exact parameter, path-convention and numerical corrections remain
       explicit. The named Pasini identifications remain unproved.

The original constructions and results retain their attribution. Classical
matrix, group-action and design theory remains classical input. The project's
contribution is the common flag and residue arguments, explicit transport
proofs, complete application deductions and the recorded source corrections.
The `scope ledger <scope.json>`_ locates all 44 L009 and 35 L092 records and
their current proofs or qualifications. These 79 records are clauses within
two contracts, not 79 manuscripts or independent new theorems.

The Buekenhout--Dehaye--Leemans classification of locally two-transitive
linear spaces and Kantor's homogeneous-design classification are retained
external results. Their exact statements were checked against the primary
texts. The full external proof costs are not measured here. Classical
automorphism identifications and specified group actions also remain stated
inputs. The literal false auxiliary source assertions are not claimed as
proved; their corrected statements and counterexamples are distinguished.

The earlier answer to the Hermitian question is reused without another
solved-question credit. L009's gonality-two question stays in its separate
accepted question packet; its nonlinear gonality-three question is unresolved
here. Excluded square and Desargues examples, external hypermap catalogue
identity, Pasini object identifications and assertions beyond the admitted
partial-linearity hypotheses are not included in the recovery claim.

Computations and Lean
---------------------

The twenty-page `program appendix <programs.pdf>`_ prints all thirteen
complete executable files, including comments. The `inventory
<program_inventory.json>`_ distinguishes four finite mathematical premises,
two programs for the independent Witt witness and its Lean tables, and seven
validations of separately proved statements. The mathematical premises check
the exceptional triangle actions, the unital residue profiles, the native
Witt designs and their full groups, and the Mathieu chamber fibres. Full-group
completeness uses GAP's DESIGN/GRAPE algorithms. A separate witness validator
does not establish that completeness from generator preservation alone.

Six reused `Lean modules <formal/scope.json>`_ supply forty distinct
standard-axiom declarations. They verify determinant transport, a generating
action criterion for connectivity, Hermitian matrix identities and transport,
a literal residue over the field of order four, three finite Witt incidence
maps and a cyclic biplane counterexample. All-rank geometry, finite-field
generation, the full classifications and computational group completeness
remain outside those formal statements. No complete source contract is
claimed to be formalized end to end.

The `program and formal review
<../../../audit/topic-g/v2/program_formal_review/review.json>`_ records a
fresh execution of all thirteen programs and all six modules, the actual
declaration statements, eight mathematical rejection controls and the
separate evidence checks. It discloses the reviewer's inherited contributions
and the distinct earlier acceptances that they use.

Review and reproduction
-----------------------

The `root adoption <../../../audit/topic-g/v2/root_adoption/review.json>`_
combines the complete common/triangle reading with the `independent Steiner
review <../../../audit/topic-g/v2/steiner_review/review.json>`_ and the
separate program/formal review. The original author freeze is preserved in
the audit directory. A separately accepted notation correction restores the
multiplicative quotient of the nonzero elements of the fields of orders
sixteen and four. Only its expression, scope binding and PDF page four change.
`assembly.json <assembly.json>`_ maps every current file to those original
records. Frozen README and author-report language about pending review
describes the submission; this guide and the `admission
<../../../audit/topic-g/v2/admission.json>`_ give the current status.

From this directory, a full computational and scoped formal replay is::

    python3 -B -O check.py --out /fresh/output --gap PATH_TO_GAP \
      --lean PATH_TO_LEAN --packages PATH_TO_PINNED_PACKAGES --render

Use ``--bindings-only`` for file and proof-context integrity. An optional
``--study-root`` checks the four separately supplied primary PDFs; it never
downloads them. The exact Lean and package revisions are in
``formal/dependency_manifest.json``. The separate renderer is::

    python3 -B -O render.py --out /fresh/render --xelatex PATH_TO_XELATEX

Its fresh assembly replay compiled all 62 pages with exact per-page text
agreement and checked inclusion of all thirteen programs. Independent visual
readings cover every page. Three operational files, ``check.py``, ``render.py``
and ``binding_controls.py``, are inventoried separately from proof programs.

Costs and completion
--------------------

This edition pays its whole common paper once within Topic G, plus both
complete applications. It receives no discount for overlap with other topics.
The combined ratio will use the full source manuscripts; each conditional
ratio will compare its source with the complete application after the whole
common theory and declared program boundary have been acquired. Complete
program costs will be shown explicitly. Lengths and paired dependency costs
are not yet admitted, and no numerical factor is claimed here. Unknown
external and source-graphics costs remain unknown.

This publication supplies the missing complete L092 application and the
common theory it needs. Twenty-four of the existing twenty-seven principal
contracts now have complete canonical applications and common theory. It adds
no source, principal-result, solved-question or formal-declaration credit.
