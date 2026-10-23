Side incidence types for the diameter-eight graph problem
========================================================

This package contains a complete finite catalogue of the six-column
incidence types used in the order 32, degree 5, girth 4, diameter 8 reduction.
There are 45 orbits of admissible five-edge loopless multigraphs on six
vertices under S6. Together with the six five-column partition types,
the written argument proves that every target has a side with one of
these 51 unmarked incidence types, after permitted global root exchange.

``ARGUMENT.rst`` gives the full mathematical guide, including the seed,
complement encoding, two-cover condition, parity and marked transport.
It reuses the earlier `common argument <../common/ARGUMENT.rst>`_ and
the reviewed notes under ``provenance/``. The contributions developed here
are the complement encoding, its parity consequence and the finite
catalogue with a supplied-certificate checker. The provenance records
attribute each contribution to its authoring agent and disclose the
reviewers' related work. The arguments use standard methods; historical
priority has not been established.

`COUNT.rst <COUNT.rst>`_ gives a separate analytic proof of the count:
Burnside's formula gives 52 multigraph types, and seven have degree 5,
leaving 45. Its `mathematical review <provenance/analytic_count_review.rst>`_
checks the complete calculation without using the catalogue output.

The `nonempty middle set theorem <provenance/middle_nonempty_argument.rst>`_
rules out the case m=0 by degree counting and triangle-freeness. Its
`review <provenance/middle_nonempty_review.rst>`_ checks the full argument.
There are therefore six necessary oriented side-size cases, with m=1,...,4.
This exclusion has not yet been applied to the current census families.

Verified finite artifact
-------------------------

``catalogue.py`` and ``catalogue.json`` preserve the exact verified bytes.
The original Root execution passed all 11 controls, complete enumeration,
and the separate supplied-catalogue check. The producer and checker
catalogue files were byte-identical, with SHA256

  3644a5f80f423ab4964af19ef9ad6c7f6b447df1aef9ec4e6f3b9a63e4bff88b

The catalogue contains all 10,887 admissible cases among the 11,628 raw
five-edge multisets; 741 have a vertex degree above 4. Every valid raw
case has an explicit vertex transporter to one of 45 representatives.
Representatives also retain their orbit/stabilizer sizes, missing degrees,
A degrees, two-cover graph and residual port budgets.

Saved checking verifies canonical representatives once under all 720
permutations, then checks complete raw coverage and each supplied carrying
permutation. It accepts any valid representative/mapping list order and
valid transporters. It does not rerun the producer's orbit-cache search.
This is a separate verification path in the same programme, not a claim
of independently authored software. The exact canonical supplied bytes
must equal the emitted verified catalogue bytes.

``SourceManifest.json`` binds every package file with relative paths,
sizes and hashes. ``provenance.json`` records exact original Source,
certificate, mathematical-review and execution references. Absolute
private paths there are historical provenance only, never runtime inputs.
The small original checker result is retained under ``evidence/``; no
runtime archives, Root callers, admission inventories or large traces
are needed for reproduction. Frozen notes retain their historical
preparation statements, including ``UNRUN``; later actual verification
is recorded separately.

Standalone reproduction
-----------------------

Use Python 3 with its standard library on macOS or Linux, where the
``resource`` module is available. No graph library, GAP, solver, private
project, class list or external data is used. From the root of a clone,
run the following in a POSIX shell. Outputs are fresh directories outside
the checkout::

  set -e
  SIDE_INCIDENCE_PACKAGE="$(pwd -P)/october_corpus/research/graphs/diameter_eight/side_incidence"
  SIDE_INCIDENCE_OUTPUT="$(python3 -E -B -S - <<'PY'
  from pathlib import Path
  import tempfile
  repo = Path.cwd().resolve()
  output = Path(tempfile.mkdtemp(prefix="side_incidence_")).resolve()
  assert output != repo and repo not in output.parents
  print(output)
  PY
  )"

  python3 -E -B -S "$SIDE_INCIDENCE_PACKAGE/catalogue.py" \
    --mode controls --out "$SIDE_INCIDENCE_OUTPUT/controls"

  python3 -E -B -S "$SIDE_INCIDENCE_PACKAGE/catalogue.py" \
    --mode check --supplied "$SIDE_INCIDENCE_PACKAGE/catalogue.json" \
    --sha256 3644a5f80f423ab4964af19ef9ad6c7f6b447df1aef9ec4e6f3b9a63e4bff88b \
    --out "$SIDE_INCIDENCE_OUTPUT/check"

  printf '%s\n' "$SIDE_INCIDENCE_OUTPUT"

Controls write ``controls.json`` and ``result.json``. Check writes the
verified ``catalogue.json`` and ``result.json``. Their output directories
must not already exist. The programme enforces a shared 20-second internal
deadline, 10 million charged finite/permutation actions, 128 MiB own RSS and
a 16 MiB artifact bound; exceeding a bound leaves the result incomplete.
The commands above are standalone reproduction, not the original external
Root guard or a kernel resource quota. ``-B`` avoids bytecode writes.

Both commands also passed from an isolated copy of the package under the
existing resource guard. The compact `reproduction record <evidence/portable_reproduction.json>`_
retains the exact programme and catalogue hashes, outcomes and resource use.

To independently regenerate the catalogue as well, use a further fresh
output directory::

  python3 -E -B -S "$SIDE_INCIDENCE_PACKAGE/catalogue.py" \
    --mode produce --out "$SIDE_INCIDENCE_OUTPUT/producer"

Scope of the result
--------------------

The 51 entries classify bare A--side incidence only. A-row labels are
forgotten; a marked application must restore the distinguished seed row,
hyperedge occurrences, vertex 9, port 21 and every required H edge, with
simultaneous boundary transport. An arbitrary fixed H need not allow
root exchange. Both (4,1) and (3,2) five-column types have one eligible internal
pair; that pair is still optional and subject to degree and port demands.

There is no complete library of side graphs, port assignments, central
graphs or compatible gluings here. The package does not show that all 51
entries extend to targets, close a current family or debt, complete the
25,408-class census, supply a Lean proof, change Original credit, or
establish a manuscript compression ratio.
