Paired proof dependencies for the projective-groups topic

Open explorer.html in any modern browser. It is self-contained and makes no
network requests. Choose historical sources or the new common proofs, select
a paper, and switch between whole results and expanded proof branches. Click
a node for its exact locators, weights, dependencies and source qualifications.
The visible graph can be saved as SVG. default_view.svg is the static initial
view of the new proofs with branches collapsed and NFC nonspace weights.
overview.dot is an additional Graphviz
source; Graphviz is not required to use the explorer.

The headline is the accepted complete-manuscript comparison and the conditional
application factors after acquiring the common theory. The graph explains that
comparison. It does not calculate a node-count ratio or a minimum proof cost.
Historical numbered items and new expanded proof branches have different
counting conventions. All original source statements, context and references
remain paid, including ancillary claims outside the declared recovery contract.

Accounting replay (Python 3 and pypdf 6.13.0):

  python -B check.py --sources-root /path/to/primary-pdfs \
    --artifacts-root /path/to/human_compression --layout public \
    --out /fresh/report.json

Supply these exact primary PDFs yourself; none is distributed here:
  catalogue_L083.pdf
  catalogue_L079.pdf
  psl2_maniplex2023.pdf
Their byte hashes, editions and extraction boundaries are in
measurement_protocol.json. The explicit source directory should contain the
three filenames directly. For the original private layout, use --layout private
and an artifacts root containing the paths bound by that protocol.

The replay checks every disjoint owned span, all five length metrics in NFC and
NFKC, the accepted whole-document totals, actual reuse IDs, all documentary
qualifications, full required/optional program inclusion and negative controls.
Per-output closures follow every recorded prerequisite. For Lemma 3.9 of L021
(and other grouped alternative proofs), this includes both printed alternatives;
it does not assert that either proof individually needs their union.

Unknown retained proof costs are null, not zero. Historical computation costs
are unknown. Required GAP calculations retain their declared algorithmic trust
boundary. Existing Lean results cover supporting interfaces, not these complete
papers. Automatic replay verifies accounting and bindings, not mathematical
truth or the validity of a defective source inference.

Regenerate the browser artifact from a successful accounting report:

  python -B render.py --result /fresh/report.json --out /fresh/visual-directory

Optional JavaScript rendering smoke test (Node.js):

  node test_explorer.js /fresh/visual-directory/explorer.html

This is a deterministic rendering/interaction test with a small DOM substitute,
not a real-browser layout test. The packet contains no primary text or rasters.
