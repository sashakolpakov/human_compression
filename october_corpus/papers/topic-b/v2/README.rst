Forest coordinates and relative generation
=========================================

The complete common paper and four applications have passed independent
review for the source contracts recorded in the `current admission
<../../../audit/topic-b/v2/admission.json>`_. They give written proofs of
the thirty declared clauses from four previously admitted manuscripts.
This publication adds no new source or solved-question credit.

* `Common theory <umbrella.pdf>`_: coset recognition, relative generation,
  weighted forests and two-block overgroups (5 pages).
* `Inductively minimal geometries <inductively-minimal-geometries.pdf>`_:
  Buekenhout and Cara's four clauses (3 pages).
* `Extremal symmetric-group markings <maximal-symmetric-markings.pdf>`_:
  Cameron and Cara's eight stated results, with the recorded degree and
  finiteness restrictions (5 pages).
* `Frattini coordinate geometries <frattini-coordinate-geometries.pdf>`_:
  Archer, Cara and Krempa's eleven clauses, with the corrected infinite
  converse and an explicit counterexample (4 pages).
* `Disjoint-subset geometries <disjoint-subset-geometries.pdf>`_:
  Garcia-Colin and Leemans's seven clauses, including the full graph
  automorphism group and the recorded source corrections (5 pages).

The `corrected source map <mapping_correction/source_contract_map.json>`_
is authoritative. Its `change record <mapping_correction/correction.json>`_
fixes two proof references, C10 and C11, in the frozen author's map. Source
statements and all mathematical TeX, PDFs and Lean proofs are unchanged.
The original map, manifest and `author scope reader <scope.pdf>`_ remain
historical snapshots; their pending-review wording describes that earlier
stage. The admission above records the accepted publication and its limits.

The `Lean proof <formal/ResidualGeneration.lean>`_ establishes the subgroup
induction used in the common paper and five related statements. It does
not formalize the forest geometry or any entire source contract. It is a
separately checked module in this packet, outside the existing 100-module
default library. Its exact hypotheses, retained geometric obligations and
axiom reports are in `the formal scope <formal/scope.json>`_.

Replay the frozen proof packet with the pinned Lean 4.32.2 compiler and
package cache, using a fresh output directory::

    python3 -B -O check.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/topic-b-replay

Add ``--render`` with pypdf and XeLaTeX installed to rebuild all six PDFs
and compare every page's extracted text. The original checker preserves
the author's original map; the repository's ``scripts/verify_snapshot.py``
also checks the corrected map against the exact written proof spans.
No mathematical enumeration is required by these uniform proofs. The
checker and its finite counterexamples validate hypotheses and artifacts.

No compression factor has yet been admitted for this edition. The five
scientific papers total 22 pages; these page counts are not a length ratio.
The source PDF for N001 remains unavailable, and its PDF cost is unknown.
It remains one of the four applications. Outside classification and
linear-algebra inputs remain explicit in the papers. A subsequent length
audit must charge this entire common theory once, then show the whole
topic and the four conditional source/application comparisons.
