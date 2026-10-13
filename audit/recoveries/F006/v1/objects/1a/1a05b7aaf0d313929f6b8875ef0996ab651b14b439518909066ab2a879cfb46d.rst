Finite boundary for two equal blocks
===================================

This is a bounded root-authored proof component, pending distinct review.
It closes ten explicit normalized actions in the two-neighbor branch;
it does not establish the reduction to these actions or recover L047 alone.

Read boundary.pdf and scope.json. The complete required GAP programs are
search.g and run.g. Replay from an exported copy with::

    python3 check.py --out /absolute/fresh/output --gap /opt/homebrew/bin/gap

The output directory must not exist. The run uses GAP finite permutation
group algorithms and the degree-six transitive catalogue. The author
report records all ten exact summaries and the genuine rank-three positive
control. This is not a Lean proof. No source text, primary PDF, or raster
render is exported. Normalizing by the block swap is attributed to the
original paper; the complete finite neighbor analysis is the contribution.
