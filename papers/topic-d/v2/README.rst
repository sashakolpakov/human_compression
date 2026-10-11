Topic D: finite actions and geometry enumeration
================================================

This is a private author edition, pending independent mathematical review.
The intake is closed. It recovers the already admitted principal results of
L066, L074 and L104, with exactly the qualifications in ``scope.json``.
It adds no source or question credit and reports no compression factor.

Read the common paper ``umbrella.pdf`` and the three applications:

* ``commuting-involutions.pdf``: all-degree pair counts and the complete
  exceptional six-point classification;
* ``suzuki-polyhedra.pdf``: all odd field exponents, the two counting formulas,
  generation, intersection, rank and duality, with classical structure retained;
* ``hall-janko-geometries.pdf``: the complete 8/19/3 census and absence of higher
  ranks, under the complete subgroup catalogue and exact group algorithms.

The final application's source also prints diagrams, automorphism and
correlation groups, and a doubling relation. Those assertions remain outside
its fixed principal census boundary. They are not described as merely absent
supplementary material. No M22 result belongs to this edition.

The common extension theorem combines stabilizer fibers and exact support.
Its orbit-stabilizer, fixed-point and Mobius ingredients are classical. A
single lemma about odd-order actions now supplies both Suzuki orbit-freeness
arguments. Every local coordinate, generation and geometry hypothesis is still
proved or explicitly retained. The previous arbitrary-chamber-stabilizer
recognition and complete augmentation proofs are included in full.

Programs and Lean
-----------------

``program-appendix.pdf`` prints all eight mathematical programs. Five are
required computations: the exceptional six-point census and four Hall--Janko
programs. The other three are complete formula/field/matrix diagnostics,
conservatively retained in the program boundary. The two full execution
drivers are separately inventoried. The selected driver modes are ``small``
and ``j2``; an unused historical M22 branch is preserved without being used.
No mutating historical certificate builder is invoked. The driver clears
``PYTHONOPTIMIZE`` before running the historical assertion-based field control.
All 146 J2 anchors must finish at an empty level, and all thirty final
geometries are checked separately. The fresh logs and complete final witnesses
are in ``author_replay``; every intermediate checkpoint is reproducible, and
its exact hash is recorded.

The new ``formal/ExtensionOrbits.lean`` proves eight generic statements about
actual orbit quotients, equivariant fibers and odd-period actions. The unchanged
``InvolutionCentralizers.lean`` supplies two abstract rank-obstruction statements.
``formal/scope.json`` says exactly how these match the written arguments.
There is no claim that Lean certifies the Mobius formula, the classical Suzuki
structure, geometry recognition, subgroup catalogue or GAP census. The pinned
Lean is 4.32.2; package revisions are in ``formal/dependency_manifest.json``.
Fresh local sources and absent pinned dependencies are compiled, while the
remaining pinned package caches are trusted; this is not a full mathlib rebuild.

Replay
------

Use Python with pypdf 6.13.0. From this directory, select a new output path::

  python -B -O check.py --out /tmp/topic-d-fresh

This checks every bound proof, program and PDF, all 37 clause rows, the eight
complete code inclusions, and seven negative controls. To replay the full
mathematical programs, scoped Lean and all five XeLaTeX documents, add::

  --programs --formal --render --gap /path/to/gap --xelatex /path/to/xelatex

The formal runner accepts ``--lean`` and ``--packages`` for the pinned compiler
and package tree. GAP 4.15.1 and TomLib 1.2.11 were used in the author replay.
The complete J2 subgroup data are an explicit retained mathematical input.

``--study-root /path/to/private/study`` additionally checks the exact three
primary PDFs and the prior proof-bank bytes. These externally obtained inputs
are not redistributed. Omitting the option leaves their byte verification
explicitly unperformed; it does not remove their mathematical assumptions.
No primary text is emitted by the verifier. The local source map identifies
physical pages in the exact bound editions, not unspecified publisher editions.

Cost and attribution
--------------------

Any later whole-topic comparison must pay the entire common paper once, the
three complete applications and the declared complete program boundary.
Overlap with another topic does not discount this common theory. Conditional
application costs must name the full prepaid common theory and full prepaid
required program. Historical code and image costs remain unknown, not zero.
The inherited results retain their original authors. No historical priority is
claimed for the new arrangement of classical arguments or its generic Lean
interfaces.
