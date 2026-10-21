A chiral polytope of rank four for a Suzuki group
================================================

The `complete five-page proof <proof/rank4_counterexample.pdf>`_ constructs
a chiral polytope of type {31,31,25} with automorphism group Sz(32768).
It refutes Theorem 1.1 in Pablo Spiga, *On the rank of Suzuki polytopes:
an answer to Hubard and Leemans*, `arXiv:2010.04080v1, 8 October 2020
<https://arxiv.org/abs/2010.04080v1>`_. The assertion concerns that fixed edition.

The matrix marking, face intersection and chirality argument are the new
contribution. Classical Suzuki coordinates, subgroup and automorphism structure,
and the rotation reconstruction criterion remain attributed inputs. The
`provenance <proof/provenance.json>`_ records the division of contributions.
The source diagnosis is separate from the counterexample: the proof applies
a product identity outside its stated domain. The full construction refutes
the principal statement, rather than merely finding a gap in its proof.

Read the `distinct mathematical review <independent_review/review.rst>`_,
`v2 citation addendum <v2_addendum/review.rst>`_, and
`public transport review <../../../audit/principal-refutations/F003/v1/portable_review/review.rst>`_.
The `admission <admission.json>`_ and
`registration <../../../audit/principal-refutations/F003/v1/registration.json>`_
record the separate principal-refutation category. F003 is removed from pending
intake but is not added to recovered or measured originals. The current partition
is 72 recovered, one refuted, 32 pending and one editorial. The frozen earlier
proposal documents are retained as historical steps, not current pending gates.

From the repository root, with Python and GAP installed::

  python corrections/suzuki-rank/v1/check.py --out /absolute/new/output

Add ``--render`` to rebuild the full TeX manuscript with pdflatex and pypdf.
The replay checks exact field arithmetic and an independent GAP reconstruction
of both face actions; it does not enumerate the ambient group or repeat discovery.
The public package supplies all required proof and computation files. Primary
papers remain identified by edition and hash without redistributing their PDFs.

This result has no ordinary recovery credit, compression factor, new
open-conjecture credit or complete Lean verification. No claim is made about
the journal text, later editions, historical priority or absence of an erratum.
