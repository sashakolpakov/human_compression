Permutation certificates for generation tests
============================================

This C11 kernel checks explicit cycles, a tree proving transitivity, and
nonempty proper invariant sets for three involutions. It also proposes
certificates under fixed limits on work, time and output size. A stopped
search leaves its remaining cases unpaid.

From this directory, build and run the existing synthetic suite::

  build_dir=$(mktemp -d)
  cc -std=c11 -O2 -Wall -Wextra -Werror orbit_components_controls/controls.c -o "$build_dir/controls"
  "$build_dir/controls"
  rm -r "$build_dir"

The test translation unit includes the kernel; compile that unit alone.
It reports 25 passing checks. These cover conjugation order, rotation words,
supplied cycles, supplied trees, invariant sets, malformed inputs and work
and output limits. No group download, GAP installation or prebuilt binary
is needed for these examples.

The three source files have exactly the bytes used in a successful Clang
build and guarded test run on macOS. ``SourceManifest.json`` records them;
``verification.json`` identifies the historical acceptance. Builds and tests
belong outside the checkout. Comments saying “UNRUN” describe the original
source freeze, preceding the recorded execution.

Mathematical scope
------------------

A supplied cycle is checked at every edge. A supplied tree has one root,
and each other vertex reaches a lower level along a specified involution.
A supplied proper set is checked for closure under all three involutions.
The caller must provide valid, authenticated permutation buffers.

Cycles and transitivity alone do not prove generation in an arbitrary
group. The strings ``GENERATING`` in the interface are intended for the
O'Nan application, where generation requires separate group identification
and subgroup theorems. Those premises, the original group data and the
production adapter are outside this package. Passing these tests adds no
completed manuscript, census result, Lean proof or compression measurement.

Attribution and implementation
------------------------------

The implementation carries forward the explicit certificate criteria from
the earlier Python computation. Its conjugation convention comes from the
`packed permutation kernel <../packed_keys/README.rst>`_. The new C kernel,
bounded proposals and tests were prepared by the Navigation agent; a
separate agent reviewed the compiler caller, and Root reviewed the kernel
and actual execution. Standard facts about permutation orbits and invariant
sets are used throughout. No historical novelty is claimed for those facts.

The earlier fixture expected 100 for a root orbit. That orbit has 38 points;
the separate 100-point closed-set test remains valid. This package contains
the corrected fixture and its successful execution. The earlier edition
remains preserved in the project's historical evidence.
