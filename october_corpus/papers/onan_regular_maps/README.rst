O'Nan regular maps: corrected source and canonical evidence
=========================================================

Start with ``regular_maps.pdf`` or its adjacent TeX source. The component
atlas in ``components.json`` gives all 44 acquired proof components and
their literal TeX includes. The principal manuscript joins the complete
136-cell table, its sum 798644, the 128 positive chiral types and the exact
95 inner and 97 outer reflexible type spectra. It records the corrections
to the original source, including the absent outer type {6,12}.

Type counts are not numbers of reflexible markings. Global inner/outer
marking totals and L026 rank counts are not asserted by this package.
The exact small-row splits and the corrected {3,15} split are stated in
the manuscript. Publication status and registration credit belong to the
external admission; historical staged-status fields remain unchanged.

Portable check
--------------

Use ordinary CPython 3.11 or newer and Git. No GAP, NumPy, Lean or old
machine runtime is needed for the default command. Use a full repository
clone: some canonical objects are reused from the tracked O'Nan correction
and other acquired packets. Run from the repository root with a fresh
absolute output directory outside the checkout::

    python3 -E -B scripts/onan_regular_maps/check.py --repo "$PWD" \
      --out /absolute/fresh/l046-check \
      --admission data/onan_regular_maps/admission.json

The external publication admission supplies exact manifest and transport
hashes and is itself bound by the repository registration. During
private review add ``--stage /absolute/private/stage`` and execute the
checker in that stage, with explicit ``--expected-manifest`` and
``--expected-transport`` instead of ``--admission``. Four GiB free space plus a 64 MiB replay allowance
are required. The default materializes only the original synthesis program;
its JSON inputs are read directly from authenticated canonical streams.
All complete new packs and reused encoded streams are authenticated.

The checker then runs the unchanged acquired synthesis predicates: all
136 table entries and the sole printed-table discrepancy, exact sums,
positive/negative type envelope equality, small-row splits, component
proof/gate joins and all 44 source-clause dispositions. It compares the
whole result, table and concordance to their accepted bytes. Private
evidence reads are forbidden, even when the original study is present.
It also reruns the original integer/Fraction character-bound arithmetic
for all 136 types and the exact order-19/order-31 column subtractions,
comparing their entire outputs. These computations import the acquired
character vectors and proved subgroup/unique-overgroup premises.

This is a composition and selected arithmetic replay. It does not rerun the historical ambient
group censuses, every literal component calculation, or all historical
resource and damage controls. Exact component code, finite input arrays,
certificates, results and reviews remain canonical payload for further
selected checks. Full historical runtime replay is not claimed.

Restore and run original arithmetic directly
-------------------------------------------

Append the following to the check command to restore three named canonical
inputs under its fresh ``restored`` directory::

    --restore corpus106_L046_maximal_bounds_v1/bounds.py \
    --restore corpus106_L046_maximal_bounds_v1/maximal_vectors.g.stdout \
    --restore corpus106_L046_maximal_bounds_v1/bounds.json

Then invoke the original program without any private path or adapter::

    python3 -E -B /absolute/fresh/l046-check/restored/corpus106_L046_maximal_bounds_v1/bounds.py \
      --vectors /absolute/fresh/l046-check/restored/corpus106_L046_maximal_bounds_v1/maximal_vectors.g.stdout \
      --output /absolute/fresh/character-bounds.json

Compare that complete JSON object to the restored ``bounds.json``. Other
exact study-relative files can be selected from ``transport.json`` using
the same repeatable ``--restore`` option, up to 32 MiB per invocation.
Premise-only source or runtime records cannot be restored as payload.
Some historical component programs retain absolute paths; their sources
and data are canonical evidence, but they are not promised standalone
portable commands. The command above and the two default arithmetic
functions are the currently tested arithmetic entry points.

Publication boundary
--------------------

``data/onan_regular_maps/transport.json`` maps every logical historical
input to an exact canonical object or an explicit boundary record.
``premises.json`` lists every omitted object's original length, digest,
locator and reason. Scholarly source pages and inherited source-reading
records are documentary premises. The checker does not pretend to read
unavailable source bytes. Historical TeX scratch, raster renderings and
platform binaries are provenance only; delivered PDF/TeX and genuine
derived mathematical data remain available. Original private evidence
has not been removed or rewritten.

The retained synthesis used historical file-identity checks for several
source/render/build records. The portable adapter admits only their exact
declared metadata and cannot supply those records as mathematical bytes.
Its JSON-storage adapter reads the exact authenticated payload bytes;
the corresponding file-identity adapter uses those verified object hashes.
All mathematical predicates and output comparisons are unchanged. Its
report names each such admission. A historical accepted native-page read
is preserved as a review premise, not reported as a new native inspection.

Reading and rendering
---------------------

The canonical principal PDF is delivered. To rebuild it, run pdfLaTeX
twice from this paper directory with a fresh external output directory::

    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory /absolute/fresh/tex regular_maps.tex
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory /absolute/fresh/tex regular_maps.tex

Required packages are amsmath, amssymb, amsthm, booktabs, longtable, array,
hyperref and geometry. Component TeX files and their adjacent inputs are
under ``components/<name>``. Rendering is separate from numerical replay;
new logs/auxiliary files belong in scratch, never in canonical payload.
No platform-dependent PDF or raster byte equality is assumed for a newly
provisioned TeX installation. See ``docs/REPRODUCING.rst`` for the wider
repository's tested entry points and toolchain limitations.
