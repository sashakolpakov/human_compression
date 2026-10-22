Graphs of diameter eight: reductions, certificates and two examples
=================================================================

This package contains written mathematics, independent mathematical
reviews and standalone Python checkers.  The common setting is a simple
5-regular, triangle-free graph on32 vertices with a marked distance-eight
geodesic.  Its three spaced center neighborhoods form an independent15-set;
the complementary induced graph has exactly five edges.

``common/`` contains the independent-set identity, the prime-degree lower
bound, the reduction using the prescribed seed and its mathematical review.
``cyclic/`` contains two cyclic-shape exclusions and a literal nonbipartite
32-vertex example with defect support ``C4 disjoint union K2``.  ``star/``
contains a literal bipartite example with defect support ``K1,5``.  Both
examples have girth4 and diameter8 by the written arguments.  Their checker
Sources independently specify finite checks of those literal artifacts.
Defect-shape names ignore isolated vertices in the17-point complement.

``middle_vertices/`` adds an independently reviewed local bound on defect
degrees and literal certificates excluding two specified partial families.
It has its own source manifest and standalone reproduction instructions.
Its check does not change the unfinished census or supply a Lean proof.

All ten files under these three directories preserve the original bytes.
``SourceManifest.json`` gives every original path, destination, byte count
and SHA256.  Original absolute paths are provenance, not dependencies.
Authorship and independent-review qualifications remain in the copied files.
The elementary methods carry no historical-priority claim.

Scope
-----

The obstructions are written arguments under their stated hypotheses.  The
examples refute uniform shape exclusions under those hypotheses.  Identifying
their classes within the ongoing census and proving census completeness
remain separate obligations.  The package has no measured compression factor
and does not complete the source manuscript or provide Lean proofs.

Project paths, accepted-boundary numbers and preparation statements such as
``UNRUN`` in the frozen notes describe their original provenance and time.
They are not current selectors or instructions to access the original project.
Later checker executions are separate evidence.  Both checkers have now passed
from an isolated copy containing only this package.  The complete actual
returns, receipts and results are in ``evidence/reproduction.json``.  Each
check used less than 29 MiB of sampled resident memory.  These checks verify
the examples; the general exclusion arguments have independent written reviews.

The example checkers use only Python 3's standard library.  They do not import
the original project, a graph library, GAP, a solver, runtime helpers, class
lists or current census data.  A successful run verifies one supplied literal
graph only.  It does not mechanically verify the general written exclusion
proofs or identify the graph's ordinary isomorphism class.

Standalone reproduction from a clone
-----------------------------------

Run the following in a POSIX shell from the root of a ``human_compression``
checkout.  The first command block verifies all copied Sources against the
manifest and creates a fresh output directory outside the checkout, using
only the standard library.  It does not execute either checker::

  set -e
  DIAMETER_EIGHT_REPO="$(pwd -P)"
  DIAMETER_EIGHT_OUTPUT="$(python3 -E -B -S - <<'PY'
  from pathlib import Path
  import hashlib
  import json
  import tempfile

  repo = Path.cwd().resolve()
  package = repo / "october_corpus/research/graphs/diameter_eight"
  manifest = json.loads((package / "SourceManifest.json").read_text())
  assert manifest["copied_files"] == len(manifest["copies"]) == 10
  for row in manifest["copies"]:
      relative = Path(row["repository_path"])
      assert not relative.is_absolute() and ".." not in relative.parts
      raw = (repo / relative).read_bytes()
      assert len(raw) == row["bytes"], row["repository_path"]
      assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["repository_path"]
  output = Path(tempfile.mkdtemp(prefix="diameter_eight_", dir="/tmp")).resolve()
  assert output != repo and repo not in output.parents, "output must be outside checkout"
  print(output)
  PY
  )"

Then run the two independent literal checks.  Input paths are clone-relative
through the physical checkout root; the output paths are absolute and fresh::

  python3 -E -B -S \
    october_corpus/research/graphs/diameter_eight/cyclic/check_example.py \
    --input "$DIAMETER_EIGHT_REPO/october_corpus/research/graphs/diameter_eight/cyclic/example.json" \
    --input-sha256 d3ba8e87686ce32c3b05a2472934eec5dc30d954a4fb29a322725abde2694f21 \
    --out "$DIAMETER_EIGHT_OUTPUT/cyclic-result.json"

  python3 -E -B -S \
    october_corpus/research/graphs/diameter_eight/star/check_example.py \
    --input "$DIAMETER_EIGHT_REPO/october_corpus/research/graphs/diameter_eight/star/example.json" \
    --input-sha256 bf45d3eda5cc616fd9eb19e0c5dafe76ddad5647cfe56a1dbbe1efc72b7c45d9 \
    --out "$DIAMETER_EIGHT_OUTPUT/star-result.json"

  printf '%s\n' "$DIAMETER_EIGHT_OUTPUT"

On success each checker writes one result JSON and prints its pin.  Both
check strict labels, simplicity, symmetry, five neighbors per vertex,
connectedness, exact girth4, all-pairs diameter8, the marked geodesic, all25
seed edges, the exact independent set and induced defect.  The cyclic check
also checks a literal odd cycle; the star check verifies the balanced16+16
bipartition and every literal distance layer.  Neither writes into the
checkout, and ``-B`` avoids bytecode output.  Repeating the first block gives
new fresh result paths.  Root's separate bounded execution admission and
evidence capture are not supplied by these shell commands.

Reading order
-------------

Start with ``common/ARGUMENT.rst`` and ``common/independent_review.rst``.
Then read each example's ``ARGUMENT.rst``, ``example.json`` and
``independent_readme_review.rst`` before inspecting its ``check_example.py``.
The manifest binds these exact proofs, reviews, inputs and checkers.  The small
execution record is kept separately in ``evidence/``; no compilation products,
census checkpoints or original payloads are needed.
