L122: explicit triality examples and a precisely bounded general interface
=========================================================================

This author packet proves every finite example in Leemans–Stokes, ``Coset
geometries with trialities and their reduced incidence graphs`` (2019).
It also supplies the full coset/chamber/reduction arguments and explicit
counterexamples to the source's proposed higher-order normalization.
One general principal assertion remains unresolved: literal Lemma 1 assumes
only cyclic transport of three parabolics, whereas its proof establishes a
type cycle without establishing order three.  This packet does not claim
that the bare existence theorem is false, or that the whole original has
been recovered.  The exact remaining obligation is in
``remaining_obligation.json``.  No source, question, formal or numerical
credit is asserted.

The complete mathematical reader consists of:

* ``triality_coordinates.tex`` / ``triality_coordinates.pdf`` (four pages):
  exact induced-order criterion; all-flag rank-three coset recognition;
  full typed-group recognition; lossless reduced relation and its full
  centralizer; precise voltage/dart conventions; six-cycle and nine-cycle
  normalization counterexamples; arbitrary-order labeled reconstruction.
* ``finite_triality_examples.tex`` / ``finite_triality_examples.pdf`` (four
  pages): all six explicit matrix markings and field definitions; exact
  finite proof premises; all full automorphism claims and inner/outer
  distinctions; the Suzuki absolute subgeometry; complete Mathieu proof;
  retained classical inputs and the remaining general qualification.

Original constructions and terminology remain attributed to Dimitri
Leemans and Klara Stokes, with Artzy/Pisanski reduction attribution retained.
Enumeration_volume authored the present witnesses and explanatory proofs;
this is an author handoff, not independent acceptance.  The earlier phase5
Suzuki/Bruhat and phase10 marked-field work was inspected and reused as
provenance.  It did not contain these six markings or the full current
graph-group proofs.  The named standard Suzuki model and the classical
three-transitive M11 action/Aut(M11) fact remain explicit borrowed inputs.
No unprovided historical Magma/Sage/GAP run is treated as evidence.

Finite proof boundary
---------------------

The whole required closure is ``programs/verify_examples.g`` plus
``data/seeds.g``.  It constructs the natural permutation images, checks the
literal field polynomials and matrix seeds, performs eighteen fresh
permutation-order verifications, verifies every marked subset intersection
and every chamber-completion product, and checks the Suzuki absolute
objects and induced incidence exactly.  Field permutations outside the
natural groups, together with double transitivity, certify the stated
outer automorphisms.  The whole Sz(8) fixed set is checked directly.

The six finite records are:

================= ========== ========== ========= =============
Group             Group order Parabolic Objects   Reduced group
================= ========== ========== ========= =============
Sz(8)                  29120         14      2080            20
PSL2(8)                  504         14        36             9
PSL2(27)                9828         28       351            12
PSL2(64)              262080        130      2016            60
PSL2(125)             976500         62     15750            60
PSL2(512)         134217216       1026    130816           504
================= ========== ========== ========= =============

All six have an actual order-three correlation.  Full typed automorphism
groups follow from the complete written thin/chamber argument; full reduced
graph groups follow from the complete centralizer theorem, not from
finding a subgroup of an unknown graph automorphism group.  The Suzuki
fixed group is C5:C4, not D10.  Its twenty absolute triples are exactly
twenty disjoint chambers.  The q=8 projective case has cyclic reduced group
of order nine.  The source did not specify that exceptional reduced group.

GAP's exact finite-field, matrix, permutation and subgroup implementations
are trusted software.  Every order verification starts with a fresh group
built from copied permutation generators, without a cached size, chain,
ambient parent, size hint or limit.  The stabilizer-chain option is
``random=1000`` (guaranteed verification); internal random construction is
not claimed absent.  ``reports/finite`` preserves the complete required
receipt.  Exploratory search scripts and intermediate seed files outside
the manifest are private discovery provenance, not shortened proof inputs.
The final seeds and polynomial data are wholly supplied.

``optional_small_oracle.py`` independently checks coordinate versions of
the written small counterexamples and the distinct-label Mathieu incidence
model.  It is optional validation, not a proof premise.  It does not prove
the borrowed M11 identity.  ``check.py`` is the whole operational replay
and scope driver.  All four current file roles and all saved evidence are
listed in ``program_inventory.json``.  No complete printed-program
alternative or software-inclusive scalar is asserted.  Historical source
software and retained external proof/library costs remain unknown, not zero.

Portable replay
---------------

With Python/pypdf, GAP and pdfLaTeX installed, run from this directory::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --out /private/tmp/L122_review_FRESH --programs --optional --render

``--gap`` and ``--pdflatex`` accept alternate executable paths.  Add
``--study-root /Users/sasha/medusa/research/leemans`` only to verify exact
private source/provenance bindings; it is unnecessary for copied-export
replay.  The output directory must be new.  The replay checks all source
and role controls, reruns the six required certificates, performs three
actual malformed finite-input controls, optionally runs the small oracle,
and rebuilds both whole native papers twice with exact page-text equality.
No old census, Lean run or private source text is needed at runtime.

The metadata entry points are ``source_contract.json`` (36 unique source
routes), ``proof_map.json`` (six entire theorem/proof environments plus all
prose proof sections), ``dependencies.json``, and
``review_checklist.rst``.  All six primary pages and all eight native pages
were read and viewed; the private source PDF/text/rasters are not exported.
The graphical reduction conventions are explicitly part of the claims and
must not be silently replaced by an unlabeled undirected graph.
