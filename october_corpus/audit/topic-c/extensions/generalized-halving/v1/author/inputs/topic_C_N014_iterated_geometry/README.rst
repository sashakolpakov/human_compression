Iterated cubic halving: Section 5 geometry
========================================

``iterated_geometry.tex`` and its complete seven-page PDF prove the
nondegeneracy, parity-shadow compatibility, literal quotient models,
diagram bonds and exhaustion of admissible leaf halvings for the cubic
toroids in N014 Section 5.  The last page is bibliography.  The source
edition is exactly arXiv:2405.19050v1 (29 May 2024).

The written proof is uniform.  No new finite certificate or Lean proof is
required.  ``check_coordinates.py`` is optional validation: 39 small-rank
affine diagram checks, 48 lattice cases and three mutation controls.
``check.py`` is an operational binding/render runner, not a mathematical
proof checker.  Neither program is silently a premise of the all-rank
argument.

Author roles
------------

Enumeration_volume authored the complete written argument and this
packet.  Root supplied the initial coordinate and PC strategy.  A distinct
third-party mathematical review remains required.  Enumeration_volume's
earlier distinct review of the coset-identification packet is disclosed;
it is not an independent review of this newly authored proof.

The constructions and proposed diagram families are Piedade--Tranchida's.
The classical cubical model is retained through their Theorem 5.1 and its
McMullen--Schulte reference.  Exact accepted phase27, coset and affine
proof dependencies are bound in ``dependencies.json``.  The original
single-relator group-presentation defects remain as corrected in the
separate affine packet.  No source-wide admission, priority, new question
answer, measurement factor or complete formalization is claimed here.

Boundary
--------

The initial period (k,s)=(1,2) is excluded.  A second operation at one end
also excludes (k,s)=(2,2).  Up to duality and the fork choices, the states
are 00, 10, 11, 20; 21 exists for n>=4, and 22 for n>=5.  The precise
small-rank overlap bonds are tabulated explicitly.  The PC proof checks
all higher flags, not only singleton shadows.  All geometric operations
are identified at the level of objects and incidence, not merely by
group order or diagram agreement.

``source_map.json`` gives fourteen Section 5 routing items.  This is not a
full-source N014 disposition map.  No primary PDF, extracted primary text,
font or source raster is exported.  Private source-page views and the
author's seven own-page views are recorded in ``visual_review.json``.

Replay
------

From a copy of the manifest and its exact exports::

  /Users/sasha/.venvs/global/bin/python -B -O check.py --out /fresh/output --render

Add ``--study-root /Users/sasha/medusa/research/leemans`` to verify all exact
external source and prior-proof bindings.  PDF reading uses pypdf; the
default renderer is ``/opt/homebrew/bin/pdflatex``, overridable by
``--pdflatex``.  The output directory must not already exist.  Portable
replay needs no source PDF, prior finite computation, GAP or Lean run.
