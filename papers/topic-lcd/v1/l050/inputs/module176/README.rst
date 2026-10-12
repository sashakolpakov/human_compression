The 176-coordinate ternary module
================================

This author-frozen bounded supplement awaits a distinct mathematical review.
Start with modules.pdf (three pages), source_map.json and scope.json.
It treats L050 Theorem 1(c) and Proposition 4, not the whole source paper.

The shared residual-Steiner factorization gives dimension 21 and the LCD
and complement-dual identities. Two explicit permutations preserve the
actual graph and generate M22 of order 443520. The already accepted full
enumeration gives 924 minimum words. One literal seed and its negative
have disjoint orbits of 462 words each, yielding all 462 minimum supports.
Elementary incidence refinement bounds the full code automorphism group
by 176*70*6*2*3 = 443520. The subgroup attains that bound, hence the full
graph and code groups agree. No graph-isomorphism backend is required for
the final bound. A separate matrix-word certificate has rank 441 and proves
absolute irreducibility of the actual 21-dimensional code.

The existing exhaustive enumeration is reused, never rerun. All retained
files are exact copies from the frozen completed-enumeration packet; their
manifest, receipt and distinct method-review pin are included. The original
complete enumeration algorithm and basis construction remain dependencies,
with full inventory in scope.json. The full dual distribution is computed
again from the classical MacWilliams identity.

Replay, from this directory or an export-only copy::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --out /fresh/output --render

Optionally add ``--study-root /Users/sasha/medusa/research/leemans`` to check
the private original source/proof/acceptance bindings too. GAP defaults to
``/opt/homebrew/bin/gap``; ``--gap`` and ``--pdflatex`` can override tools.
NumPy supplies exact int64 modular arithmetic only. The GAP file checks an
actual isomorphism to its standard MathieuGroup(22), and independently
confirms the matrix-algebra dimension. The Python checker independently
closes the coordinate group and proves its upper bound by refinement.
Eight weakening/calibration controls are distinct from mathematical premises.

The local whole mathematical executables are steiner_construction.py,
certificate.py and identify.g. Literal module_data.json and the retained
enumeration/basis are mandatory data. check.py is the operational driver
and control suite. Discovery-only GRAPE and sparse-message search are
documented in provenance.json; neither is a final replay premise.

The source's Atlas classification of the unique 21-dimensional irreducible
module and the least nontrivial dimension is retained, not inferred from
this one module. Proposition 4's dimension-free final sentence is qualified
using Theorem 1(c) and its own proof. Historical optimal-code comparisons
remain outside this bounded certificate. No new source, question, novelty,
ratio or Lean credit is asserted. Historical source-software cost is
unknown; it is not assigned zero.
