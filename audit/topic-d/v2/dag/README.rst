Stabilizers, support and enumeration: proof dependencies and costs
=================================================================

This audit connects the three complete Topic D applications to their historical
proofs and to the common theory. Start with the `two-page explanation
<costs/reader.pdf>`_ and the `acquisition plot <costs/acquisition.pdf>`_. Download
the `interactive explorer <costs/explorer.html>`_ and open it within a repository
checkout to follow any of the 37 source clauses or the three complete results.
It works without a server or network connection. The `static proof graph
<costs/default_graph.pdf>`_ illustrates one route through the Suzuki argument.

The two comparisons
-------------------

The complete source manuscripts cost 47,894 characters. Our whole common paper
costs 15,632 and the three complete applications cost 29,855. The combined
written ratio remains::

  47,894 / (15,632 + 29,855) = 1.053.

After acquiring the **whole common theory and all eight complete programs**,
the three source/application ratios remain:

.. list-table:: Complete individual comparisons
   :header-rows: 1

   * - Source and application
     - Source characters
     - Application characters
     - Conditional factor
   * - L066 / D1: commuting involutions
     - 20,916
     - 10,989
     - 1.903
   * - L074 / D2: Suzuki polyhedra
     - 20,661
     - 13,367
     - 1.546
   * - L104 / D3: Hall–Janko geometries
     - 6,317
     - 5,499
     - 1.149

The full printed program appendix adds 27,070, giving 47,894 / 72,557 = 0.660.
All eight raw programs instead give denominator 71,672 and factor 0.668.
These are alternative representations. The two operational drivers cost 10,038
characters separately, outside these denominators. Five programs supply
mathematical premises and three are diagnostics; all eight remain charged.
The `length admission <../measurement/admission.json>`_ supplies the accepted
counts and thirty measurement coordinates. This graph changes none of them.

How the dependencies are charged
--------------------------------

Arrows run from a prerequisite to the proof using it. The graph has 137 nodes
and 284 typed arrows. Historical assertions, mathematical premises, attribution
and verification evidence have different roles. A historical arrow documents
the source's argument; it does not certify a corrected historical assertion.

Every extracted passage belongs to one of 220 exclusive cost owners. A named
result and several proof branches may refer to the same statement or setup.
The cost of a route is the sum over the union of its owners after all
prerequisites have been collected. Adding displayed node costs would count
some passages twice. There is no compression ratio based on node counts.

The complete comparison also pays for context, references and unused common
results. In particular, the normalizer theorem stays in the full common-paper
cost. The acquisition plot adds the common paper, the entire program appendix,
and then each complete application. Already acquired prerequisites are shown
as reused text; they are not subtracted from an application's measured length.
Other topics still pay for their own whole common papers. This reading order
does not establish a research chronology or a sawtooth pattern.

Review and corrections
----------------------

The `logical review <logical_review/review.json>`_ corrected five documentary
interfaces in the original graph. A subsequent `single-edge review
<logical_delta_review/review.json>`_ added the common support theorem as a
direct premise of D2's support proof. The `ownership and reader review
<independent_review/review.json>`_ corrected a historical statement category
and restored two shared setup passages. All complete-document and owner costs
remain unchanged; only the relevant individual routes change.

Independent checking reproduced 240 document metric cells, 6,600 owner cells,
116 unions for outputs and context, and 137 individual prerequisite closures.
All 215 selected-text boundaries were read, and all 740 spans across the three
extraction variants were checked. Root replayed the independent allocation,
revision and reader checks. The reader was exercised in 168 selected DOM views
and thirty metric settings; its figures and both PDF pages were inspected.
These are behavior and static-layout checks, not a real-browser layout test.

The five required programs enter mathematical routes. Diagnostics, the ten
original Lean declarations and the later supplement of 28 declarations retain
their separate verification roles. They do not provide complete source-specific
formalizations. The supplement contains twelve plus sixteen declarations;
the first twelve are not added again to the twenty-eight.

The source qualifications remain explicit: L066's reversal and degree-six
cases, the classical Suzuki inputs, and L104's excluded diagrams, full
automorphism/correlation groups, doubling relation and supplement annotations.
Expanded external proofs, historical software, catalogue construction and
graphic costs remain unknown. No source, question or formal credit is added.

Current and historical records
------------------------------

``logical`` and ``costs`` hold the current accepted versions. The original
and preceding graphs and the first cost proposal are preserved in distinct
historical folders. Frozen author readers keep their submission wording;
`admission.json <admission.json>`_ and the independent reviews record the
subsequent acceptance without altering those bytes.

The current cost manifest, ``input_bindings.json`` and generated viewer
bindings select logical version 3. The unchanged ``reader_input_bindings.json``
inside the cost packet is provenance for the earlier version; it is not the
current graph selection. Full re-extraction requires the privately held source
PDFs. The public snapshot verifier checks the frozen files, complete-document
conservation, prerequisite unions, exact public proof locations and acquisition
costs against the already accepted measurement.
