Chamber orbits and regular covers
================================

This private canonical edition reworks two already admitted source contracts.
It does not add a source, a conjecture answer or a compression factor. The full
common paper and both complete applications are separate documents.

* ``umbrella.tex/pdf``: extension fibers; propagation and reconstruction from
  chamber adjacencies; the explicit reflection on two regular group orbits;
  intersection transport; mirror-invariant relation kernels; local mirror
  identifications; and prime-degree minimality. The geometric string C+
  correspondence and its exact limits are stated openly.
* ``testing-chirality.tex/pdf``: L008 Theorem 1.1, including necessity using the
  full automorphism group, sufficiency, all residue ranks and the infinite-group
  qualification. All ten primary pages were read; the printed Magma programs
  and ancillary claims are not added to the admitted principal target.
* ``minimal-regular-covers.tex/pdf``: every proved conclusion of the eight-page
  July 25, 2023 N016 author manuscript, including every general corollary, the
  square-torus family, the five retained atomic families and all six groups in
  the explicit minimal-cover example. The publisher PDF remains unavailable.
* ``programs.tex/pdf``: the whole required GAP proof program and a separately
  identified whole diagnostic program. Two old operational runners remain
  visible as complete files; the current runner does not rely on their obsolete
  manuscript paths or optimization-sensitive assertions.

``scope.json`` records 27 detailed rows across these two contracts and 22 proof
spans. This is not 27 newly covered manuscripts: the project principal-source
count remains unchanged. Its rows retain excluded software and separate
questions as such. ``question_map.json`` binds the existing unrestricted-cover,
finite rank-four and interval results, while preserving the unresolved all-rank
finite question. None of those later proofs is a mathematical premise of the
two applications, and the three previous cover TeX papers are not unpriced
common theory.

Attribution and proof roles
---------------------------

The normalized group-action argument and kernel transport are elementary
interfaces already used in the proof bank. The source chirality and cover
criteria are credited to their authors. The explicit chamber reflection gives
the actual map that the earlier source correspondence described implicitly;
no historical novelty claim is made. The standard polytope correspondence,
Schulte--Weiss section theorem, affine square-tessellation identification and
specified Cunningham--Pellicer classification are retained at their points of
use. Their full expanded costs are unknown, not zero.

The mathematical computation is the exact prior ``phase41_chiral_cover_check.g``
with unchanged bytes, now ``programs/chiral_cover.g``. It establishes the finite
example from bare presentations with trusted GAP algorithms. It is not a
sampling argument for the infinite families. ``reflection_models.py`` checks
four small action models and three assumption countermodels; it is validation,
not a premise for the quantified proof. ``program_inventory.json`` distinguishes
one required mathematical file, one diagnostic and three operational files.

The formal packet has seven newly proved declarations for the actual G x Bool
reflection formula, and seven compiled declarations in two unchanged earlier
modules. Their uses are specified declaration by declaration in
``formal/scope.json``. Only the general algebraic/action interfaces are checked;
incidence reconstruction, geometric correspondence, local source hypotheses,
older classification and the six GAP groups are not end-to-end Lean proofs.
The independent scientific review is still required before public adoption.

Reproduction
------------

With the already acquired primary files and pinned local Lean packages::

  python -B -O check.py --out /fresh/output \
    --study-root /Users/sasha/medusa/research/leemans \
    --public-root /Users/sasha/medusa/math_compression --render

The script accepts explicit ``--gap``, ``--lean``, ``--packages`` and
``--xelatex`` paths. It downloads nothing. ``--bindings-only`` checks the bound
proof and source files without repeating mathematical computations.
``--skip-formal`` explicitly omits Lean; such a run is not a formal replay.
An existing output directory is refused. All acceptance checks remain active
under Python optimization. The source PDFs and primary text are not exported.

The authoring script ``bind_author.py`` describes the private input bindings;
it is not the public reproduction command and must not be rerun over a frozen
packet. A future independent topic measurement must pay the full common paper,
both full applications and the required program once within this topic. No
measurement is performed here.
